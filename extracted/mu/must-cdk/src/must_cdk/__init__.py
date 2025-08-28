r'''
# Must CDK

A collection of AWS CDK constructs that implement common architectural patterns and best practices for AWS services. This library aims to simplify the deployment of common cloud infrastructure patterns while maintaining security, scalability, and operational excellence.

## Getting Started

### TypeScript/JavaScript

```bash
npm install must-cdk
# or
yarn add must-cdk
```

### Python

```bash
pip install must-cdk
```

### CLI Tool

Install globally to quickly initialize Amplify projects:

```bash
# Install CLI globally
npm install -g must-cdk

# Initialize Amplify project with React template
must-cdk amplify init

# Initialize in specific directory
must-cdk amplify init -d /path/to/project
```

## Features

### 🏗️ Amplify Patterns

* Next.js application deployment optimizations
* Multi-environment branch configurations
* Custom domain and SSL setup
* GitHub personal access token authentication
* Automated build and deployment pipelines
* Migration path to GitHub Apps for production
* CLI tool for quick project initialization

### 🚢 ECS CodeDeploy Patterns

* Blue/Green deployment strategies
* Load balanced service deployments
* Auto-scaling configurations
* Health check implementations
* Environment variables support
* Secrets management integration
* Custom container names
* Enhanced container configuration
* Container access after creation

### 🌐 CloudFront Patterns

* API Gateway integrations
* Multi-origin configurations
* Cross-region setups
* Security headers and WAF integration
* Caching strategies
* Custom domain configurations

### 🔌 API Gateway Lambda Patterns

* REST API implementations
* WebSocket API setups
* Custom domain configurations
* Lambda authorizers
* Rate limiting and API key management

## 🏷️ Tags Management

Must CDK provides a unified tagging system that automatically applies tags to all resources across all constructs. This system supports both environment-based tags and construct-specific tags.

### Environment Tags

Set tags globally using the `TAGS` environment variable:

```bash
# Format: key1=value1,key2=value2
export TAGS="Product=MyApp,Owner=TeamName,Environment=production,CostCenter=engineering"

# Deploy with environment tags
cdk deploy
```

### Construct-Specific Tags

Add tags directly to individual constructs:

```python
// TypeScript
new AmplifyApp(this, 'MyApp', {
  appName: 'my-application',
  repository: 'https://github.com/user/repo',
  tags: {
    Team: 'frontend',
    Version: 'v1.0.0',
    Component: 'web-app'
  }
});
```

```python
# Python
AmplifyApp(self, 'MyApp',
  app_name='my-application',
  repository='https://github.com/user/repo',
  tags={
    'Team': 'frontend',
    'Version': 'v1.0.0',
    'Component': 'web-app'
  }
)
```

### Tag Precedence

Environment tags take precedence over construct-specific tags:

```bash
# Environment variable
export TAGS="Environment=production,Team=platform"

# In your code
tags: {
  Team: 'frontend',      # Will be overridden by environment
  Component: 'web-app'   # Will be preserved
}

# Final tags applied:
# Environment=production (from env)
# Team=platform (from env, overrides construct tag)
# Component=web-app (from construct)
```

## Documentation

Detailed documentation for each construct can be found in:

* [Python API Reference](./docs/python/api.md)
* [Tags Documentation](./docs/TAGS.md)
* [Examples](./examples/README.md)

## Examples

The [examples](./examples) directory contains working examples for each construct category:

* Amplify deployment patterns
* ECS with CodeDeploy configurations
* CloudFront distribution setups
* API Gateway with Lambda integrations

Each example is provided in both TypeScript and Python with detailed comments and instructions.
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
import aws_cdk.aws_amplify as _aws_cdk_aws_amplify_ceddda9d
import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_apigatewayv2 as _aws_cdk_aws_apigatewayv2_ceddda9d
import aws_cdk.aws_certificatemanager as _aws_cdk_aws_certificatemanager_ceddda9d
import aws_cdk.aws_cloudfront as _aws_cdk_aws_cloudfront_ceddda9d
import aws_cdk.aws_cloudfront_origins as _aws_cdk_aws_cloudfront_origins_ceddda9d
import aws_cdk.aws_codedeploy as _aws_cdk_aws_codedeploy_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_route53 as _aws_cdk_aws_route53_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import constructs as _constructs_77d1e7e8


class AmplifyApp(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="must-cdk.AmplifyApp",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_name: builtins.str,
        repository: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        basic_auth: typing.Optional[typing.Union["BasicAuthConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        branches: typing.Optional[typing.Sequence[typing.Union["BranchOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
        build_settings: typing.Optional[typing.Union["BuildSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[typing.Union["CustomDomainOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        custom_rules: typing.Optional[typing.Sequence[typing.Union["CustomRule", typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: The name for the Amplify app.
        :param repository: The Git repository URL for the Amplify app. Format: https://github.com/user/repo or similar.
        :param access_token: GitHub personal access token for repository access. If not provided, will attempt to use GitHub CLI token or MUFIN_PUSH_TOKEN environment variable. Note: For production deployments, consider migrating to GitHub Apps for better security, organization support, and higher rate limits after initial setup.
        :param basic_auth: Basic authentication configuration for the Amplify app.
        :param branches: Branch configurations for the Amplify app. If not provided, a default 'main' branch will be created.
        :param build_settings: Build settings for the Amplify app.
        :param build_spec: Build specification for the Amplify app. Defines the build commands and output artifacts.
        :param custom_domain: Custom domain configuration for the Amplify app.
        :param custom_rules: Custom rules for the Amplify app. Used for redirects, rewrites, and other routing rules.
        :param environment_variables: Environment variables for the Amplify app. These will be available during the build process.
        :param platform: Platform for the Amplify app. Default: "WEB"
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777b9bbab56e86272a20ea4d9e3f1efad25bb7fea282e210cf563e8923d584d0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AmplifyAppProps(
            app_name=app_name,
            repository=repository,
            access_token=access_token,
            basic_auth=basic_auth,
            branches=branches,
            build_settings=build_settings,
            build_spec=build_spec,
            custom_domain=custom_domain,
            custom_rules=custom_rules,
            environment_variables=environment_variables,
            platform=platform,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="app")
    def app(self) -> _aws_cdk_aws_amplify_ceddda9d.CfnApp:
        return typing.cast(_aws_cdk_aws_amplify_ceddda9d.CfnApp, jsii.get(self, "app"))

    @builtins.property
    @jsii.member(jsii_name="branches")
    def branches(self) -> typing.List[_aws_cdk_aws_amplify_ceddda9d.CfnBranch]:
        return typing.cast(typing.List[_aws_cdk_aws_amplify_ceddda9d.CfnBranch], jsii.get(self, "branches"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[_aws_cdk_aws_amplify_ceddda9d.CfnDomain]:
        return typing.cast(typing.Optional[_aws_cdk_aws_amplify_ceddda9d.CfnDomain], jsii.get(self, "domain"))


class ApiGatewayToLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="must-cdk.ApiGatewayToLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api_name: builtins.str,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        create_usage_plan: typing.Optional[builtins.bool] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        custom_routes: typing.Optional[typing.Sequence[typing.Union["CustomRoute", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        lambda_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        proxy: typing.Optional[builtins.bool] = None,
        rest_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_name: API configuration.
        :param lambda_function: Primary Lambda function for the API.
        :param binary_media_types: Binary media types for the API This setting will be applied regardless of whether LambdaRestApi or RestApi is used.
        :param create_usage_plan: Whether to create a Usage Plan.
        :param custom_domain_name: Optional custom domain name for API Gateway.
        :param custom_routes: Custom routes for manual API setup (when proxy is false) If provided, will use RestApi instead of LambdaRestApi.
        :param enable_logging: Enable CloudWatch logging for API Gateway.
        :param existing_certificate: Optional ACM certificate to use instead of creating a new one.
        :param hosted_zone: Optional Route53 hosted zone for custom domain.
        :param lambda_api_props: 
        :param log_group_props: CloudWatch Logs configuration.
        :param proxy: 
        :param rest_api_props: 
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88385340a9ac0a3d345bb5f8b9e0334655a117a97d92f90c383b720f4bbd4824)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApiGatewayToLambdaProps(
            api_name=api_name,
            lambda_function=lambda_function,
            binary_media_types=binary_media_types,
            create_usage_plan=create_usage_plan,
            custom_domain_name=custom_domain_name,
            custom_routes=custom_routes,
            enable_logging=enable_logging,
            existing_certificate=existing_certificate,
            hosted_zone=hosted_zone,
            lambda_api_props=lambda_api_props,
            log_group_props=log_group_props,
            proxy=proxy,
            rest_api_props=rest_api_props,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        *,
        handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        method: builtins.str,
        path: builtins.str,
        method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _aws_cdk_aws_apigateway_ceddda9d.Method:
        '''Add a custom route after construction (for dynamic route addition).

        :param handler: 
        :param method: 
        :param path: 
        :param method_options: 
        '''
        route = CustomRoute(
            handler=handler, method=method, path=path, method_options=method_options
        )

        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.Method, jsii.invoke(self, "addRoute", [route]))

    @builtins.property
    @jsii.member(jsii_name="apiGateway")
    def api_gateway(self) -> _aws_cdk_aws_apigateway_ceddda9d.RestApi:
        return typing.cast(_aws_cdk_aws_apigateway_ceddda9d.RestApi, jsii.get(self, "apiGateway"))

    @builtins.property
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiUrl"))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayLogGroup")
    def api_gateway_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup]:
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup], jsii.get(self, "apiGatewayLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="aRecord")
    def a_record(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.ARecord]:
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.ARecord], jsii.get(self, "aRecord"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainName]:
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.DomainName], jsii.get(self, "domain"))

    @builtins.property
    @jsii.member(jsii_name="usagePlan")
    def usage_plan(self) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.UsagePlan]:
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.UsagePlan], jsii.get(self, "usagePlan"))


@jsii.data_type(
    jsii_type="must-cdk.BasicAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "username": "username",
        "enable_basic_auth": "enableBasicAuth",
    },
)
class BasicAuthConfig:
    def __init__(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
        enable_basic_auth: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Basic authentication configuration for an Amplify application.

        :param password: Password for basic authentication.
        :param username: Username for basic authentication.
        :param enable_basic_auth: Whether to enable basic authentication. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__097b1dc50c0b38ab7552cceb5b206127e52e3d3f36506f52f873d369bbe70ef3)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }
        if enable_basic_auth is not None:
            self._values["enable_basic_auth"] = enable_basic_auth

    @builtins.property
    def password(self) -> builtins.str:
        '''Password for basic authentication.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Username for basic authentication.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_basic_auth(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable basic authentication.

        :default: true
        '''
        result = self._values.get("enable_basic_auth")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.BranchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "enable_auto_build": "enableAutoBuild",
        "environment_variables": "environmentVariables",
        "framework": "framework",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
    },
)
class BranchOptions:
    def __init__(
        self,
        *,
        branch_name: builtins.str,
        build_spec: typing.Optional[builtins.str] = None,
        enable_auto_build: typing.Optional[builtins.bool] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        framework: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Branch configuration for an Amplify application.

        :param branch_name: The name of the branch.
        :param build_spec: Branch-specific build specification.
        :param enable_auto_build: Whether to enable automatic builds for this branch. Default: true
        :param environment_variables: Environment variables specific to this branch.
        :param framework: The framework for this branch.
        :param pull_request_preview: Whether to enable pull request previews for this branch. Default: false
        :param stage: The stage for the branch (e.g., PRODUCTION, BETA, DEVELOPMENT). Default: "PRODUCTION"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bdd7acb58378cad16e462f75882a091b44e7545c30579297f524f5212ec7923)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch_name": branch_name,
        }
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if enable_auto_build is not None:
            self._values["enable_auto_build"] = enable_auto_build
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if framework is not None:
            self._values["framework"] = framework
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''The name of the branch.'''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''Branch-specific build specification.'''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_build(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable automatic builds for this branch.

        :default: true
        '''
        result = self._values.get("enable_auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables specific to this branch.'''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def framework(self) -> typing.Optional[builtins.str]:
        '''The framework for this branch.'''
        result = self._values.get("framework")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable pull request previews for this branch.

        :default: false
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''The stage for the branch (e.g., PRODUCTION, BETA, DEVELOPMENT).

        :default: "PRODUCTION"
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
    jsii_type="must-cdk.BuildSettings",
    jsii_struct_bases=[],
    name_mapping={
        "cache_type": "cacheType",
        "compute_type": "computeType",
        "enable_auto_branch_creation": "enableAutoBranchCreation",
        "enable_auto_branch_deletion": "enableAutoBranchDeletion",
        "enable_branch_auto_build": "enableBranchAutoBuild",
    },
)
class BuildSettings:
    def __init__(
        self,
        *,
        cache_type: typing.Optional[builtins.str] = None,
        compute_type: typing.Optional[builtins.str] = None,
        enable_auto_branch_creation: typing.Optional[builtins.bool] = None,
        enable_auto_branch_deletion: typing.Optional[builtins.bool] = None,
        enable_branch_auto_build: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''Build settings for an Amplify application.

        :param cache_type: Cache type for the build. Default: "AMPLIFY_MANAGED"
        :param compute_type: Compute type for the build. Default: "STANDARD"
        :param enable_auto_branch_creation: Whether to enable automatic branch creation when a new branch is pushed to the repository. Default: false
        :param enable_auto_branch_deletion: Whether to enable automatic branch deletion when a branch is deleted from the repository. Default: false
        :param enable_branch_auto_build: Whether to enable automatic builds when code is pushed to a branch. Default: true
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c76ab27a2495b9f4e651b178bb37566be40717e7134787251b8db015853ba53)
            check_type(argname="argument cache_type", value=cache_type, expected_type=type_hints["cache_type"])
            check_type(argname="argument compute_type", value=compute_type, expected_type=type_hints["compute_type"])
            check_type(argname="argument enable_auto_branch_creation", value=enable_auto_branch_creation, expected_type=type_hints["enable_auto_branch_creation"])
            check_type(argname="argument enable_auto_branch_deletion", value=enable_auto_branch_deletion, expected_type=type_hints["enable_auto_branch_deletion"])
            check_type(argname="argument enable_branch_auto_build", value=enable_branch_auto_build, expected_type=type_hints["enable_branch_auto_build"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cache_type is not None:
            self._values["cache_type"] = cache_type
        if compute_type is not None:
            self._values["compute_type"] = compute_type
        if enable_auto_branch_creation is not None:
            self._values["enable_auto_branch_creation"] = enable_auto_branch_creation
        if enable_auto_branch_deletion is not None:
            self._values["enable_auto_branch_deletion"] = enable_auto_branch_deletion
        if enable_branch_auto_build is not None:
            self._values["enable_branch_auto_build"] = enable_branch_auto_build

    @builtins.property
    def cache_type(self) -> typing.Optional[builtins.str]:
        '''Cache type for the build.

        :default: "AMPLIFY_MANAGED"
        '''
        result = self._values.get("cache_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_type(self) -> typing.Optional[builtins.str]:
        '''Compute type for the build.

        :default: "STANDARD"
        '''
        result = self._values.get("compute_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_branch_creation(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable automatic branch creation when a new branch is pushed to the repository.

        :default: false
        '''
        result = self._values.get("enable_auto_branch_creation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_auto_branch_deletion(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable automatic branch deletion when a branch is deleted from the repository.

        :default: false
        '''
        result = self._values.get("enable_auto_branch_deletion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_branch_auto_build(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable automatic builds when code is pushed to a branch.

        :default: true
        '''
        result = self._values.get("enable_branch_auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BuildSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.CacheBehaviorConfig",
    jsii_struct_bases=[],
    name_mapping={
        "origin_id": "originId",
        "path_pattern": "pathPattern",
        "allowed_methods": "allowedMethods",
        "cached_methods": "cachedMethods",
        "cache_policy": "cachePolicy",
        "cache_policy_id": "cachePolicyId",
        "compress": "compress",
        "origin_request_policy": "originRequestPolicy",
        "origin_request_policy_id": "originRequestPolicyId",
        "response_headers_policy": "responseHeadersPolicy",
        "response_headers_policy_id": "responseHeadersPolicyId",
        "viewer_protocol_policy": "viewerProtocolPolicy",
    },
)
class CacheBehaviorConfig:
    def __init__(
        self,
        *,
        origin_id: builtins.str,
        path_pattern: builtins.str,
        allowed_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods] = None,
        cached_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods] = None,
        cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
        cache_policy_id: typing.Optional[builtins.str] = None,
        compress: typing.Optional[builtins.bool] = None,
        origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
        origin_request_policy_id: typing.Optional[builtins.str] = None,
        response_headers_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy] = None,
        response_headers_policy_id: typing.Optional[builtins.str] = None,
        viewer_protocol_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy] = None,
    ) -> None:
        '''
        :param origin_id: Origin ID to route this pattern to.
        :param path_pattern: Path pattern for this behavior (e.g., "/api/*", "*.jpg").
        :param allowed_methods: Allowed HTTP methods. Default: ALLOW_GET_HEAD for S3, ALLOW_ALL for HTTP
        :param cached_methods: Methods to cache. Default: CACHE_GET_HEAD_OPTIONS
        :param cache_policy: Cache policy (alternative to cachePolicyId).
        :param cache_policy_id: Cache policy ID (use AWS managed policies).
        :param compress: Enable compression. Default: true
        :param origin_request_policy: Origin request policy (alternative to originRequestPolicyId).
        :param origin_request_policy_id: Origin request policy ID.
        :param response_headers_policy: Response headers policy (alternative to responseHeadersPolicyId).
        :param response_headers_policy_id: Response headers policy ID.
        :param viewer_protocol_policy: Viewer protocol policy. Default: REDIRECT_TO_HTTPS
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09e71190d617032adb23312ff8a226e4f3a3a9c6a6886244b17283984821ac0f)
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
            check_type(argname="argument path_pattern", value=path_pattern, expected_type=type_hints["path_pattern"])
            check_type(argname="argument allowed_methods", value=allowed_methods, expected_type=type_hints["allowed_methods"])
            check_type(argname="argument cached_methods", value=cached_methods, expected_type=type_hints["cached_methods"])
            check_type(argname="argument cache_policy", value=cache_policy, expected_type=type_hints["cache_policy"])
            check_type(argname="argument cache_policy_id", value=cache_policy_id, expected_type=type_hints["cache_policy_id"])
            check_type(argname="argument compress", value=compress, expected_type=type_hints["compress"])
            check_type(argname="argument origin_request_policy", value=origin_request_policy, expected_type=type_hints["origin_request_policy"])
            check_type(argname="argument origin_request_policy_id", value=origin_request_policy_id, expected_type=type_hints["origin_request_policy_id"])
            check_type(argname="argument response_headers_policy", value=response_headers_policy, expected_type=type_hints["response_headers_policy"])
            check_type(argname="argument response_headers_policy_id", value=response_headers_policy_id, expected_type=type_hints["response_headers_policy_id"])
            check_type(argname="argument viewer_protocol_policy", value=viewer_protocol_policy, expected_type=type_hints["viewer_protocol_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "origin_id": origin_id,
            "path_pattern": path_pattern,
        }
        if allowed_methods is not None:
            self._values["allowed_methods"] = allowed_methods
        if cached_methods is not None:
            self._values["cached_methods"] = cached_methods
        if cache_policy is not None:
            self._values["cache_policy"] = cache_policy
        if cache_policy_id is not None:
            self._values["cache_policy_id"] = cache_policy_id
        if compress is not None:
            self._values["compress"] = compress
        if origin_request_policy is not None:
            self._values["origin_request_policy"] = origin_request_policy
        if origin_request_policy_id is not None:
            self._values["origin_request_policy_id"] = origin_request_policy_id
        if response_headers_policy is not None:
            self._values["response_headers_policy"] = response_headers_policy
        if response_headers_policy_id is not None:
            self._values["response_headers_policy_id"] = response_headers_policy_id
        if viewer_protocol_policy is not None:
            self._values["viewer_protocol_policy"] = viewer_protocol_policy

    @builtins.property
    def origin_id(self) -> builtins.str:
        '''Origin ID to route this pattern to.'''
        result = self._values.get("origin_id")
        assert result is not None, "Required property 'origin_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path_pattern(self) -> builtins.str:
        '''Path pattern for this behavior (e.g., "/api/*", "*.jpg").'''
        result = self._values.get("path_pattern")
        assert result is not None, "Required property 'path_pattern' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_methods(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods]:
        '''Allowed HTTP methods.

        :default: ALLOW_GET_HEAD for S3, ALLOW_ALL for HTTP
        '''
        result = self._values.get("allowed_methods")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods], result)

    @builtins.property
    def cached_methods(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods]:
        '''Methods to cache.

        :default: CACHE_GET_HEAD_OPTIONS
        '''
        result = self._values.get("cached_methods")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods], result)

    @builtins.property
    def cache_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy]:
        '''Cache policy (alternative to cachePolicyId).'''
        result = self._values.get("cache_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy], result)

    @builtins.property
    def cache_policy_id(self) -> typing.Optional[builtins.str]:
        '''Cache policy ID (use AWS managed policies).'''
        result = self._values.get("cache_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compress(self) -> typing.Optional[builtins.bool]:
        '''Enable compression.

        :default: true
        '''
        result = self._values.get("compress")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def origin_request_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy]:
        '''Origin request policy (alternative to originRequestPolicyId).'''
        result = self._values.get("origin_request_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy], result)

    @builtins.property
    def origin_request_policy_id(self) -> typing.Optional[builtins.str]:
        '''Origin request policy ID.'''
        result = self._values.get("origin_request_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def response_headers_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy]:
        '''Response headers policy (alternative to responseHeadersPolicyId).'''
        result = self._values.get("response_headers_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy], result)

    @builtins.property
    def response_headers_policy_id(self) -> typing.Optional[builtins.str]:
        '''Response headers policy ID.'''
        result = self._values.get("response_headers_policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def viewer_protocol_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy]:
        '''Viewer protocol policy.

        :default: REDIRECT_TO_HTTPS
        '''
        result = self._values.get("viewer_protocol_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CacheBehaviorConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudFrontToOrigins(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="must-cdk.CloudFrontToOrigins",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_behaviors: typing.Optional[typing.Sequence[typing.Union[CacheBehaviorConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        create_route53_records: typing.Optional[builtins.bool] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        default_origin_id: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_pages: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        http_origins: typing.Optional[typing.Sequence[typing.Union["HttpOriginConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_include_cookies: typing.Optional[builtins.bool] = None,
        log_prefix: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        s3_origins: typing.Optional[typing.Sequence[typing.Union["S3OriginConfig", typing.Dict[builtins.str, typing.Any]]]] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param additional_domain_names: Additional domain names (aliases) for the distribution Note: All domains must be covered by the same certificate. CloudFront only supports one certificate per distribution.
        :param cache_behaviors: Cache behaviors for specific path patterns.
        :param certificate: Existing ACM certificate to use for the CloudFront distribution Certificate must be in us-east-1 region for CloudFront. The certificate must cover all domains (customDomainName + additionalDomainNames). CloudFront only supports one certificate per distribution.
        :param comment: Comment for the distribution.
        :param create_route53_records: Create Route53 records for all domain names. Default: true if hostedZone is provided
        :param custom_domain_name: Primary custom domain name for the CloudFront distribution.
        :param default_origin_id: ID of the origin to use as default behavior If not specified, will use the first HTTP origin, then first S3 origin.
        :param default_root_object: Default root object for the distribution. Default: "index.html"
        :param enabled: Whether the distribution is enabled. Default: true
        :param enable_ipv6: Enable IPv6 for the distribution. Default: false
        :param enable_logging: Enable CloudFront access logging. Default: true
        :param error_pages: Custom error page configurations If not provided, intelligent defaults will be applied based on origin types.
        :param geo_restriction: Geographic restriction configuration.
        :param hosted_zone: Route53 hosted zone for the custom domain Required for creating Route53 records.
        :param http_origins: HTTP origins configuration.
        :param http_version: HTTP version to support. Default: HttpVersion.HTTP2
        :param log_bucket: Existing S3 bucket for logs If not provided and logging is enabled, a new bucket will be created.
        :param log_include_cookies: Include cookies in access logs. Default: false
        :param log_prefix: Prefix for log files. Default: "cloudfront"
        :param price_class: CloudFront distribution price class. Default: PRICE_CLASS_100
        :param s3_origins: S3 origins configuration.
        :param web_acl_id: Web Application Firewall (WAF) web ACL ID.
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5595cb0fd40f1755eb3336459cd050240b0464ea7a04fa1bf71ac0f843be019)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudFrontToOriginsProps(
            additional_domain_names=additional_domain_names,
            cache_behaviors=cache_behaviors,
            certificate=certificate,
            comment=comment,
            create_route53_records=create_route53_records,
            custom_domain_name=custom_domain_name,
            default_origin_id=default_origin_id,
            default_root_object=default_root_object,
            enabled=enabled,
            enable_ipv6=enable_ipv6,
            enable_logging=enable_logging,
            error_pages=error_pages,
            geo_restriction=geo_restriction,
            hosted_zone=hosted_zone,
            http_origins=http_origins,
            http_version=http_version,
            log_bucket=log_bucket,
            log_include_cookies=log_include_cookies,
            log_prefix=log_prefix,
            price_class=price_class,
            s3_origins=s3_origins,
            web_acl_id=web_acl_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="getHttpOrigin")
    def get_http_origin(
        self,
        origin_id: builtins.str,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin]:
        '''Get HTTP origin by origin ID.

        :param origin_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e649c2726a6488e46170e86657ba3afb312a168dbc1015cde22b0b69336f53f)
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin], jsii.invoke(self, "getHttpOrigin", [origin_id]))

    @jsii.member(jsii_name="getS3Bucket")
    def get_s3_bucket(
        self,
        origin_id: builtins.str,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''Get S3 bucket by origin ID.

        :param origin_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf9864ad4075688df20b9dbf44e995106eb63bf50d190ab2434b56d977a3129)
            check_type(argname="argument origin_id", value=origin_id, expected_type=type_hints["origin_id"])
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], jsii.invoke(self, "getS3Bucket", [origin_id]))

    @builtins.property
    @jsii.member(jsii_name="aRecords")
    def a_records(self) -> typing.List[_aws_cdk_aws_route53_ceddda9d.ARecord]:
        return typing.cast(typing.List[_aws_cdk_aws_route53_ceddda9d.ARecord], jsii.get(self, "aRecords"))

    @builtins.property
    @jsii.member(jsii_name="distribution")
    def distribution(self) -> _aws_cdk_aws_cloudfront_ceddda9d.Distribution:
        return typing.cast(_aws_cdk_aws_cloudfront_ceddda9d.Distribution, jsii.get(self, "distribution"))

    @builtins.property
    @jsii.member(jsii_name="distributionDomainName")
    def distribution_domain_name(self) -> builtins.str:
        '''Get the CloudFront distribution domain name.'''
        return typing.cast(builtins.str, jsii.get(self, "distributionDomainName"))

    @builtins.property
    @jsii.member(jsii_name="distributionUrl")
    def distribution_url(self) -> builtins.str:
        '''Get the CloudFront distribution URL with protocol.'''
        return typing.cast(builtins.str, jsii.get(self, "distributionUrl"))

    @builtins.property
    @jsii.member(jsii_name="httpOriginIds")
    def http_origin_ids(self) -> typing.List[builtins.str]:
        '''Get all HTTP origin IDs.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "httpOriginIds"))

    @builtins.property
    @jsii.member(jsii_name="httpOrigins")
    def http_origins(self) -> typing.List["HttpOriginInfo"]:
        '''Get all HTTP origins as an array of objects with ID and origin.'''
        return typing.cast(typing.List["HttpOriginInfo"], jsii.get(self, "httpOrigins"))

    @builtins.property
    @jsii.member(jsii_name="s3OriginIds")
    def s3_origin_ids(self) -> typing.List[builtins.str]:
        '''Get all S3 bucket origin IDs.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "s3OriginIds"))

    @builtins.property
    @jsii.member(jsii_name="s3Origins")
    def s3_origins(self) -> typing.List["S3OriginInfo"]:
        '''Get all S3 buckets as an array of objects with ID and bucket.'''
        return typing.cast(typing.List["S3OriginInfo"], jsii.get(self, "s3Origins"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="customDomainUrl")
    def custom_domain_url(self) -> typing.Optional[builtins.str]:
        '''Get the custom domain URL (if configured).'''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomainUrl"))

    @builtins.property
    @jsii.member(jsii_name="domainNames")
    def domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domainNames"))

    @builtins.property
    @jsii.member(jsii_name="logBucket")
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], jsii.get(self, "logBucket"))


@jsii.data_type(
    jsii_type="must-cdk.CodeDeployApplicationConfig",
    jsii_struct_bases=[],
    name_mapping={"application_name": "applicationName"},
)
class CodeDeployApplicationConfig:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CodeDeploy application configuration options.

        :param application_name: The name of the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5502fecaec2fcacb90758335131c1b764d3da7ff95d6f9252571099bb02703)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.'''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeDeployApplicationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.ContainerConfig",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "options": "options"},
)
class ContainerConfig:
    def __init__(
        self,
        *,
        name: builtins.str,
        options: typing.Union[_aws_cdk_aws_ecs_ceddda9d.ContainerDefinitionOptions, typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''Container configuration using native CDK interfaces.

        :param name: Container name.
        :param options: Native CDK container definition options.
        '''
        if isinstance(options, dict):
            options = _aws_cdk_aws_ecs_ceddda9d.ContainerDefinitionOptions(**options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a8f326881db7c040d8f4c23992dd449f63d8cd8f46a42695a34a87d6f822a7)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "options": options,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Container name.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def options(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerDefinitionOptions:
        '''Native CDK container definition options.'''
        result = self._values.get("options")
        assert result is not None, "Required property 'options' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerDefinitionOptions, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.CustomDomainOptions",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
    },
)
class CustomDomainOptions:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomainOptions", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Custom domain configuration for an Amplify application.

        :param domain_name: The custom domain name for the Amplify app.
        :param auto_subdomain_creation_patterns: Patterns for automatic subdomain creation.
        :param enable_auto_subdomain: Whether to enable automatic subdomain creation. Default: false
        :param sub_domains: Subdomain configurations for the custom domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a9aef33f07ee4b94fd871c1fa5450b39a9a6f85d609e53d9f8d6d9d18666169)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
        }
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The custom domain name for the Amplify app.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Patterns for automatic subdomain creation.'''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''Whether to enable automatic subdomain creation.

        :default: false
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomainOptions"]]:
        '''Subdomain configurations for the custom domain.'''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomainOptions"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.CustomRoute",
    jsii_struct_bases=[],
    name_mapping={
        "handler": "handler",
        "method": "method",
        "path": "path",
        "method_options": "methodOptions",
    },
)
class CustomRoute:
    def __init__(
        self,
        *,
        handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        method: builtins.str,
        path: builtins.str,
        method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param handler: 
        :param method: 
        :param path: 
        :param method_options: 
        '''
        if isinstance(method_options, dict):
            method_options = _aws_cdk_aws_apigateway_ceddda9d.MethodOptions(**method_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__037506344a4229895450ab2466c4a39abd0da2085c3a5d744bc1a0bdaf3a2c8d)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument method_options", value=method_options, expected_type=type_hints["method_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "handler": handler,
            "method": method,
            "path": path,
        }
        if method_options is not None:
            self._values["method_options"] = method_options

    @builtins.property
    def handler(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def method(self) -> builtins.str:
        result = self._values.get("method")
        assert result is not None, "Required property 'method' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def method_options(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions]:
        result = self._values.get("method_options")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.CustomRule",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "condition": "condition",
        "status": "status",
    },
)
class CustomRule:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Custom routing rule for an Amplify application.

        :param source: Source pattern to match in the URL.
        :param target: Target URL to redirect or rewrite to.
        :param condition: Condition to apply the rule.
        :param status: HTTP status code for the redirect. Default: "200"
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39915f5b079be3a4939a38452e4b026fdbbc7aa3c31aef40d22288ff86d9b8cd)
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
        '''Source pattern to match in the URL.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''Target URL to redirect or rewrite to.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''Condition to apply the rule.'''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''HTTP status code for the redirect.

        :default: "200"
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.DeploymentGroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "blue_green_deployment_config": "blueGreenDeploymentConfig",
        "deployment_config": "deploymentConfig",
        "deployment_group_name": "deploymentGroupName",
    },
)
class DeploymentGroupConfig:
    def __init__(
        self,
        *,
        blue_green_deployment_config: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.EcsBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_config: typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentConfig] = None,
        deployment_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''CodeDeploy deployment group configuration options.

        :param blue_green_deployment_config: Configuration for blue-green ECS deployments.
        :param deployment_config: The deployment configuration to use.
        :param deployment_group_name: The name of the deployment group.
        '''
        if isinstance(blue_green_deployment_config, dict):
            blue_green_deployment_config = _aws_cdk_aws_codedeploy_ceddda9d.EcsBlueGreenDeploymentConfig(**blue_green_deployment_config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03d1e7127aabea4ca4381fa09bc0557271913b6524f87fae49b42a73469e9a07)
            check_type(argname="argument blue_green_deployment_config", value=blue_green_deployment_config, expected_type=type_hints["blue_green_deployment_config"])
            check_type(argname="argument deployment_config", value=deployment_config, expected_type=type_hints["deployment_config"])
            check_type(argname="argument deployment_group_name", value=deployment_group_name, expected_type=type_hints["deployment_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if blue_green_deployment_config is not None:
            self._values["blue_green_deployment_config"] = blue_green_deployment_config
        if deployment_config is not None:
            self._values["deployment_config"] = deployment_config
        if deployment_group_name is not None:
            self._values["deployment_group_name"] = deployment_group_name

    @builtins.property
    def blue_green_deployment_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.EcsBlueGreenDeploymentConfig]:
        '''Configuration for blue-green ECS deployments.'''
        result = self._values.get("blue_green_deployment_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.EcsBlueGreenDeploymentConfig], result)

    @builtins.property
    def deployment_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentConfig]:
        '''The deployment configuration to use.'''
        result = self._values.get("deployment_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentConfig], result)

    @builtins.property
    def deployment_group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the deployment group.'''
        result = self._values.get("deployment_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsCodeDeploy(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="must-cdk.EcsCodeDeploy",
):
    '''A CDK construct that creates an ECS Fargate service with CodeDeploy blue-green deployment capability.

    This construct provides a modular approach to deploy containerized applications with blue-green deployment.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
        containers: typing.Sequence[typing.Union[ContainerConfig, typing.Dict[builtins.str, typing.Any]]],
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
        service_name: builtins.str,
        task_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        code_deploy_application: typing.Optional[typing.Union[CodeDeployApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_group: typing.Optional[typing.Union[DeploymentGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer: typing.Optional[typing.Union["LoadBalancerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        production_listener: typing.Optional[typing.Union["ListenerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        production_target_group: typing.Optional[typing.Union["TargetGroupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        service: typing.Optional[typing.Union["ServiceConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        target_port: typing.Optional[jsii.Number] = None,
        task_definition: typing.Optional[typing.Union["TaskDefinitionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        test_listener: typing.Optional[typing.Union["ListenerConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        test_target_group: typing.Optional[typing.Union["TargetGroupConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cluster: ECS Cluster where the service will run.
        :param containers: Container configurations using native CDK interfaces.
        :param security_groups: Security groups for ECS service (required).
        :param service_name: Base name used for resources like log groups, roles, services, etc.
        :param task_subnets: Subnets for ECS tasks (required). IMPORTANT: This controls where your ECS containers run. Use private subnets for security. To limit to specific AZs: { availabilityZones: ['us-east-1a'] } For all private subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }
        :param vpc: VPC in which to deploy ECS and ALB resources.
        :param code_deploy_application: CodeDeploy application configuration.
        :param deployment_group: CodeDeploy deployment group configuration.
        :param load_balancer: Load balancer configuration options.
        :param load_balancer_subnets: Subnets for ALB (optional, defaults to taskSubnets). IMPORTANT: This controls where your Load Balancer runs, NOT your containers! - For internet-facing ALBs: Use PUBLIC subnets across multiple AZs - For internal ALBs: Use PRIVATE subnets across multiple AZs - Common mistake: Restricting ALB to single AZ reduces availability Examples: - All public subnets: { subnetType: ec2.SubnetType.PUBLIC } - Specific AZs: { availabilityZones: ['us-east-1a', 'us-east-1b'] } - Default (all subnets): {} or undefined
        :param production_listener: Production listener configuration.
        :param production_target_group: Production target group configuration.
        :param service: Service configuration options.
        :param target_port: The port to expose on the target group (defaults to first container's port).
        :param task_definition: Task definition configuration options.
        :param test_listener: Test listener configuration (optional - defaults will be used if not provided).
        :param test_target_group: Test target group configuration (optional - defaults will be used if not provided).
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19ac4f77d3bba1391929b87d2d23b70fe61e21aa6809f43ed4283d6ecf350909)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsCodeDeployProps(
            cluster=cluster,
            containers=containers,
            security_groups=security_groups,
            service_name=service_name,
            task_subnets=task_subnets,
            vpc=vpc,
            code_deploy_application=code_deploy_application,
            deployment_group=deployment_group,
            load_balancer=load_balancer,
            load_balancer_subnets=load_balancer_subnets,
            production_listener=production_listener,
            production_target_group=production_target_group,
            service=service,
            target_port=target_port,
            task_definition=task_definition,
            test_listener=test_listener,
            test_target_group=test_target_group,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="allListeners")
    def all_listeners(
        self,
    ) -> typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener]:
        return typing.cast(typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener], jsii.invoke(self, "allListeners", []))

    @jsii.member(jsii_name="blueListener")
    def blue_listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener, jsii.invoke(self, "blueListener", []))

    @jsii.member(jsii_name="greenListener")
    def green_listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener, jsii.invoke(self, "greenListener", []))

    @builtins.property
    @jsii.member(jsii_name="application")
    def application(self) -> _aws_cdk_aws_codedeploy_ceddda9d.EcsApplication:
        return typing.cast(_aws_cdk_aws_codedeploy_ceddda9d.EcsApplication, jsii.get(self, "application"))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> typing.List[_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition]:
        return typing.cast(typing.List[_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition], jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def listeners(
        self,
    ) -> typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener]:
        '''Get all listeners from the load balancer.'''
        return typing.cast(typing.List[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener], jsii.get(self, "listeners"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationLoadBalancer, jsii.get(self, "loadBalancer"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancerDnsName")
    def load_balancer_dns_name(self) -> builtins.str:
        '''Get the load balancer DNS name.'''
        return typing.cast(builtins.str, jsii.get(self, "loadBalancerDnsName"))

    @builtins.property
    @jsii.member(jsii_name="productionListener")
    def production_listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener:
        '''Get the production listener.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener, jsii.get(self, "productionListener"))

    @builtins.property
    @jsii.member(jsii_name="productionTargetGroup")
    def production_target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup, jsii.get(self, "productionTargetGroup"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> _aws_cdk_aws_ecs_ceddda9d.FargateService:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.FargateService, jsii.get(self, "service"))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''Get the service ARN.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> _aws_cdk_aws_ecs_ceddda9d.TaskDefinition:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.TaskDefinition, jsii.get(self, "taskDefinition"))

    @builtins.property
    @jsii.member(jsii_name="testListener")
    def test_listener(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener:
        '''Get the test listener.'''
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationListener, jsii.get(self, "testListener"))

    @builtins.property
    @jsii.member(jsii_name="testTargetGroup")
    def test_target_group(
        self,
    ) -> _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup:
        return typing.cast(_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationTargetGroup, jsii.get(self, "testTargetGroup"))


@jsii.data_type(
    jsii_type="must-cdk.HttpOriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "id": "id",
        "http_origin_props": "httpOriginProps",
        "http_port": "httpPort",
        "https_port": "httpsPort",
        "origin_path": "originPath",
        "protocol_policy": "protocolPolicy",
    },
)
class HttpOriginConfig:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        id: builtins.str,
        http_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
        http_port: typing.Optional[jsii.Number] = None,
        https_port: typing.Optional[jsii.Number] = None,
        origin_path: typing.Optional[builtins.str] = None,
        protocol_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginProtocolPolicy] = None,
    ) -> None:
        '''
        :param domain_name: Domain name of the HTTP origin (required).
        :param id: Unique identifier for this HTTP origin.
        :param http_origin_props: Additional HTTP origin properties.
        :param http_port: HTTP port (for HTTP protocol). Default: 80
        :param https_port: HTTPS port (for HTTPS protocol). Default: 443
        :param origin_path: Origin path for HTTP requests (e.g., "/api/v1").
        :param protocol_policy: Protocol policy for the origin. Default: HTTPS_ONLY
        '''
        if isinstance(http_origin_props, dict):
            http_origin_props = _aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOriginProps(**http_origin_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c46e442fdd0192863cab169d59fec779cadb566db29953677761c4940b26d818)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument http_origin_props", value=http_origin_props, expected_type=type_hints["http_origin_props"])
            check_type(argname="argument http_port", value=http_port, expected_type=type_hints["http_port"])
            check_type(argname="argument https_port", value=https_port, expected_type=type_hints["https_port"])
            check_type(argname="argument origin_path", value=origin_path, expected_type=type_hints["origin_path"])
            check_type(argname="argument protocol_policy", value=protocol_policy, expected_type=type_hints["protocol_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "id": id,
        }
        if http_origin_props is not None:
            self._values["http_origin_props"] = http_origin_props
        if http_port is not None:
            self._values["http_port"] = http_port
        if https_port is not None:
            self._values["https_port"] = https_port
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if protocol_policy is not None:
            self._values["protocol_policy"] = protocol_policy

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Domain name of the HTTP origin (required).'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier for this HTTP origin.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_origin_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOriginProps]:
        '''Additional HTTP origin properties.'''
        result = self._values.get("http_origin_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOriginProps], result)

    @builtins.property
    def http_port(self) -> typing.Optional[jsii.Number]:
        '''HTTP port (for HTTP protocol).

        :default: 80
        '''
        result = self._values.get("http_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def https_port(self) -> typing.Optional[jsii.Number]:
        '''HTTPS port (for HTTPS protocol).

        :default: 443
        '''
        result = self._values.get("https_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        '''Origin path for HTTP requests (e.g., "/api/v1").'''
        result = self._values.get("origin_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def protocol_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginProtocolPolicy]:
        '''Protocol policy for the origin.

        :default: HTTPS_ONLY
        '''
        result = self._values.get("protocol_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginProtocolPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpOriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.HttpOriginInfo",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "origin": "origin"},
)
class HttpOriginInfo:
    def __init__(
        self,
        *,
        id: builtins.str,
        origin: _aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin,
    ) -> None:
        '''HTTP origin information.

        :param id: 
        :param origin: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7feea82df6d57cdecc62c96a5730f43379b516233376c0533b57e1b1d68f58f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument origin", value=origin, expected_type=type_hints["origin"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "origin": origin,
        }

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin(self) -> _aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin:
        result = self._values.get("origin")
        assert result is not None, "Required property 'origin' is missing"
        return typing.cast(_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpOriginInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.ListenerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "certificates": "certificates",
        "default_action": "defaultAction",
        "port": "port",
        "protocol": "protocol",
    },
)
class ListenerConfig:
    def __init__(
        self,
        *,
        certificates: typing.Optional[typing.Sequence[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]] = None,
        default_action: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerAction] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    ) -> None:
        '''Listener configuration options.

        :param certificates: Certificate list of ACM cert ARNs.
        :param default_action: The default actions for the listener.
        :param port: The port on which the listener listens for requests.
        :param protocol: The protocol for connections from clients to the load balancer.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f5ab801b4e660224ccf6cf401be1529c61a4dfdb7a1404942a16c2517d178dd)
            check_type(argname="argument certificates", value=certificates, expected_type=type_hints["certificates"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificates is not None:
            self._values["certificates"] = certificates
        if default_action is not None:
            self._values["default_action"] = default_action
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol

    @builtins.property
    def certificates(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]]:
        '''Certificate list of ACM cert ARNs.'''
        result = self._values.get("certificates")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]], result)

    @builtins.property
    def default_action(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerAction]:
        '''The default actions for the listener.'''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerAction], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the listener listens for requests.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        '''The protocol for connections from clients to the load balancer.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ListenerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.LoadBalancerConfig",
    jsii_struct_bases=[],
    name_mapping={
        "idle_timeout_seconds": "idleTimeoutSeconds",
        "internet_facing": "internetFacing",
        "load_balancer_name": "loadBalancerName",
        "security_groups": "securityGroups",
        "vpc_subnets": "vpcSubnets",
    },
)
class LoadBalancerConfig:
    def __init__(
        self,
        *,
        idle_timeout_seconds: typing.Optional[jsii.Number] = None,
        internet_facing: typing.Optional[builtins.bool] = None,
        load_balancer_name: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Load balancer configuration options.

        :param idle_timeout_seconds: Idle timeout in seconds for the ALB.
        :param internet_facing: Whether the load balancer is internet facing.
        :param load_balancer_name: Load balancer name.
        :param security_groups: Security groups for the load balancer.
        :param vpc_subnets: The VPC subnets to use.
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c5a95f45a3b1f8c843cf50d6a1005817682e3d6ff84735169cc73c06e12b10f)
            check_type(argname="argument idle_timeout_seconds", value=idle_timeout_seconds, expected_type=type_hints["idle_timeout_seconds"])
            check_type(argname="argument internet_facing", value=internet_facing, expected_type=type_hints["internet_facing"])
            check_type(argname="argument load_balancer_name", value=load_balancer_name, expected_type=type_hints["load_balancer_name"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if idle_timeout_seconds is not None:
            self._values["idle_timeout_seconds"] = idle_timeout_seconds
        if internet_facing is not None:
            self._values["internet_facing"] = internet_facing
        if load_balancer_name is not None:
            self._values["load_balancer_name"] = load_balancer_name
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def idle_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Idle timeout in seconds for the ALB.'''
        result = self._values.get("idle_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def internet_facing(self) -> typing.Optional[builtins.bool]:
        '''Whether the load balancer is internet facing.'''
        result = self._values.get("internet_facing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def load_balancer_name(self) -> typing.Optional[builtins.str]:
        '''Load balancer name.'''
        result = self._values.get("load_balancer_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''Security groups for the load balancer.'''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The VPC subnets to use.'''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.S3OriginConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "id": "id",
        "origin_access_identity": "originAccessIdentity",
        "origin_path": "originPath",
        "s3_origin_props": "s3OriginProps",
        "use_legacy_oai": "useLegacyOAI",
    },
)
class S3OriginConfig:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        id: builtins.str,
        origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
        origin_path: typing.Optional[builtins.str] = None,
        s3_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
        use_legacy_oai: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bucket: Existing S3 bucket to use as origin (required).
        :param id: Unique identifier for this S3 origin.
        :param origin_access_identity: Existing Origin Access Identity (only used if useLegacyOAI is true).
        :param origin_path: Origin path for S3 requests (e.g., "/static").
        :param s3_origin_props: Additional S3 origin properties.
        :param use_legacy_oai: Use legacy Origin Access Identity instead of modern Origin Access Control. Default: false - uses OAC for better security
        '''
        if isinstance(s3_origin_props, dict):
            s3_origin_props = _aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps(**s3_origin_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c491da83cb47b60ad107d7ab3a03d121bd5de0ec3db21592303a1459dfa81ce)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument origin_access_identity", value=origin_access_identity, expected_type=type_hints["origin_access_identity"])
            check_type(argname="argument origin_path", value=origin_path, expected_type=type_hints["origin_path"])
            check_type(argname="argument s3_origin_props", value=s3_origin_props, expected_type=type_hints["s3_origin_props"])
            check_type(argname="argument use_legacy_oai", value=use_legacy_oai, expected_type=type_hints["use_legacy_oai"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "id": id,
        }
        if origin_access_identity is not None:
            self._values["origin_access_identity"] = origin_access_identity
        if origin_path is not None:
            self._values["origin_path"] = origin_path
        if s3_origin_props is not None:
            self._values["s3_origin_props"] = s3_origin_props
        if use_legacy_oai is not None:
            self._values["use_legacy_oai"] = use_legacy_oai

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        '''Existing S3 bucket to use as origin (required).'''
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''Unique identifier for this S3 origin.'''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def origin_access_identity(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity]:
        '''Existing Origin Access Identity (only used if useLegacyOAI is true).'''
        result = self._values.get("origin_access_identity")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity], result)

    @builtins.property
    def origin_path(self) -> typing.Optional[builtins.str]:
        '''Origin path for S3 requests (e.g., "/static").'''
        result = self._values.get("origin_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def s3_origin_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps]:
        '''Additional S3 origin properties.'''
        result = self._values.get("s3_origin_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps], result)

    @builtins.property
    def use_legacy_oai(self) -> typing.Optional[builtins.bool]:
        '''Use legacy Origin Access Identity instead of modern Origin Access Control.

        :default: false - uses OAC for better security
        '''
        result = self._values.get("use_legacy_oai")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3OriginConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.S3OriginInfo",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "id": "id"},
)
class S3OriginInfo:
    def __init__(
        self,
        *,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        id: builtins.str,
    ) -> None:
        '''S3 origin information.

        :param bucket: 
        :param id: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1c3ec5b8a1718b199ec940b9c6ef6af3af2ea2de8856064d69c396dd38ca634)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket": bucket,
            "id": id,
        }

    @builtins.property
    def bucket(self) -> _aws_cdk_aws_s3_ceddda9d.IBucket:
        result = self._values.get("bucket")
        assert result is not None, "Required property 'bucket' is missing"
        return typing.cast(_aws_cdk_aws_s3_ceddda9d.IBucket, result)

    @builtins.property
    def id(self) -> builtins.str:
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3OriginInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.ServiceConfig",
    jsii_struct_bases=[],
    name_mapping={
        "assign_public_ip": "assignPublicIp",
        "desired_count": "desiredCount",
        "health_check_grace_period": "healthCheckGracePeriod",
    },
)
class ServiceConfig:
    def __init__(
        self,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        desired_count: typing.Optional[jsii.Number] = None,
        health_check_grace_period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Service configuration options.

        :param assign_public_ip: Whether to assign public IP addresses to the task's ENI.
        :param desired_count: The desired number of instantiations of the task definition to keep running.
        :param health_check_grace_period: Health check grace period.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83d46c6ecc0567279ab942573549709584b26f1786fd9089e850d2bd49170b6)
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument desired_count", value=desired_count, expected_type=type_hints["desired_count"])
            check_type(argname="argument health_check_grace_period", value=health_check_grace_period, expected_type=type_hints["health_check_grace_period"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if desired_count is not None:
            self._values["desired_count"] = desired_count
        if health_check_grace_period is not None:
            self._values["health_check_grace_period"] = health_check_grace_period

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Whether to assign public IP addresses to the task's ENI.'''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        '''The desired number of instantiations of the task definition to keep running.'''
        result = self._values.get("desired_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''Health check grace period.'''
        result = self._values.get("health_check_grace_period")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.SubDomainOptions",
    jsii_struct_bases=[],
    name_mapping={"branch_name": "branchName", "prefix": "prefix"},
)
class SubDomainOptions:
    def __init__(self, *, branch_name: builtins.str, prefix: builtins.str) -> None:
        '''Subdomain configuration for a custom domain in an Amplify application.

        :param branch_name: The branch name to map to this subdomain.
        :param prefix: The prefix for the subdomain. Use empty string for the root domain.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d299494480073590a530a506b82a6958f2f0149f64e2eb929864716bb21e2e6f)
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch_name": branch_name,
            "prefix": prefix,
        }

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''The branch name to map to this subdomain.'''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def prefix(self) -> builtins.str:
        '''The prefix for the subdomain.

        Use empty string for the root domain.
        '''
        result = self._values.get("prefix")
        assert result is not None, "Required property 'prefix' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubDomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.TaggableProps",
    jsii_struct_bases=[],
    name_mapping={"tags": "tags"},
)
class TaggableProps:
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Type for tag-aware construct props.

        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1dc2cddf876ac6ea0c1f692c56ba26ce2e055e80dff32f5934853a7a20ab5a0)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags.

        Environment variable supports multiple formats:

        - Key-value pairs: TAGS=key1=value1,key2=value2
        - JSON string: TAGS='{"key1":"value1","key2":"value2"}'
        - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaggableProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.TargetGroupConfig",
    jsii_struct_bases=[],
    name_mapping={
        "health_check": "healthCheck",
        "load_balancing_algorithm_type": "loadBalancingAlgorithmType",
        "port": "port",
        "protocol": "protocol",
        "slow_start": "slowStart",
        "stickiness_cookie_duration": "stickinessCookieDuration",
        "target_group_name": "targetGroupName",
    },
)
class TargetGroupConfig:
    def __init__(
        self,
        *,
        health_check: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancing_algorithm_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType] = None,
        port: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
        slow_start: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        target_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Target group configuration options.

        :param health_check: Health check configuration.
        :param load_balancing_algorithm_type: The load balancing algorithm to use.
        :param port: The port on which the targets receive traffic.
        :param protocol: The protocol to use for routing traffic to the targets.
        :param slow_start: The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic.
        :param stickiness_cookie_duration: The stickiness cookie duration.
        :param target_group_name: Target group name.
        '''
        if isinstance(health_check, dict):
            health_check = _aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck(**health_check)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79d412fa856e93114faca93f3f3109977421ac7571097864fad7c6f77e756f3)
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument load_balancing_algorithm_type", value=load_balancing_algorithm_type, expected_type=type_hints["load_balancing_algorithm_type"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument slow_start", value=slow_start, expected_type=type_hints["slow_start"])
            check_type(argname="argument stickiness_cookie_duration", value=stickiness_cookie_duration, expected_type=type_hints["stickiness_cookie_duration"])
            check_type(argname="argument target_group_name", value=target_group_name, expected_type=type_hints["target_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if health_check is not None:
            self._values["health_check"] = health_check
        if load_balancing_algorithm_type is not None:
            self._values["load_balancing_algorithm_type"] = load_balancing_algorithm_type
        if port is not None:
            self._values["port"] = port
        if protocol is not None:
            self._values["protocol"] = protocol
        if slow_start is not None:
            self._values["slow_start"] = slow_start
        if stickiness_cookie_duration is not None:
            self._values["stickiness_cookie_duration"] = stickiness_cookie_duration
        if target_group_name is not None:
            self._values["target_group_name"] = target_group_name

    @builtins.property
    def health_check(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck]:
        '''Health check configuration.'''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck], result)

    @builtins.property
    def load_balancing_algorithm_type(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType]:
        '''The load balancing algorithm to use.'''
        result = self._values.get("load_balancing_algorithm_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on which the targets receive traffic.'''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(
        self,
    ) -> typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol]:
        '''The protocol to use for routing traffic to the targets.'''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol], result)

    @builtins.property
    def slow_start(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The time period during which the load balancer sends a newly registered target a linearly increasing share of the traffic.'''
        result = self._values.get("slow_start")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def stickiness_cookie_duration(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The stickiness cookie duration.'''
        result = self._values.get("stickiness_cookie_duration")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def target_group_name(self) -> typing.Optional[builtins.str]:
        '''Target group name.'''
        result = self._values.get("target_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TargetGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.TaskDefinitionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "execution_role": "executionRole",
        "memory_limit_mib": "memoryLimitMiB",
        "task_role": "taskRole",
    },
)
class TaskDefinitionConfig:
    def __init__(
        self,
        *,
        cpu: typing.Optional[jsii.Number] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        task_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''Task definition configuration options.

        :param cpu: The number of cpu units used by the task.
        :param execution_role: Execution role for the task.
        :param memory_limit_mib: The amount (in MiB) of memory used by the task.
        :param task_role: Task role for the task.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82cc7c746398105f3e0d633178d0221928f104cae239c86eec0d9b408385e7c6)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument task_role", value=task_role, expected_type=type_hints["task_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cpu is not None:
            self._values["cpu"] = cpu
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if task_role is not None:
            self._values["task_role"] = task_role

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''The number of cpu units used by the task.'''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Execution role for the task.'''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''The amount (in MiB) of memory used by the task.'''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Task role for the task.'''
        result = self._values.get("task_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TaskDefinitionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebSocketApiGatewayToLambda(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="must-cdk.WebSocketApiGatewayToLambda",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        api_name: builtins.str,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        custom_routes: typing.Optional[typing.Sequence[typing.Union["WebSocketRoute", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param api_name: WebSocket API configuration.
        :param lambda_function: Primary Lambda function for the API (usually handles $default route).
        :param api_props: 
        :param custom_domain_name: Optional custom domain name for API Gateway.
        :param custom_routes: Custom routes for WebSocket API Common routes: $connect, $disconnect, $default, or custom route keys.
        :param enable_logging: Enable CloudWatch logging for API Gateway.
        :param existing_certificate: Optional ACM certificate to use instead of creating a new one.
        :param hosted_zone: Optional Route53 hosted zone for custom domain.
        :param log_group_props: CloudWatch Logs configuration.
        :param stage_name: Stage name for the WebSocket API. Default: 'dev'
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15689bf8cb45b613fd6d0271ea2d2b2a40c677ff7ee1d37b34596aa645c185e9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WebSocketApiGatewayToLambdaProps(
            api_name=api_name,
            lambda_function=lambda_function,
            api_props=api_props,
            custom_domain_name=custom_domain_name,
            custom_routes=custom_routes,
            enable_logging=enable_logging,
            existing_certificate=existing_certificate,
            hosted_zone=hosted_zone,
            log_group_props=log_group_props,
            stage_name=stage_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addRoute")
    def add_route(
        self,
        *,
        handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        route_key: builtins.str,
        route_response_selection_expression: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketRoute:
        '''Add a custom route after construction (for dynamic route addition).

        :param handler: 
        :param route_key: 
        :param route_response_selection_expression: 
        '''
        route = WebSocketRoute(
            handler=handler,
            route_key=route_key,
            route_response_selection_expression=route_response_selection_expression,
        )

        return typing.cast(_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketRoute, jsii.invoke(self, "addRoute", [route]))

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, jsii.get(self, "lambdaFunction"))

    @builtins.property
    @jsii.member(jsii_name="webSocketApi")
    def web_socket_api(self) -> _aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApi:
        return typing.cast(_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApi, jsii.get(self, "webSocketApi"))

    @builtins.property
    @jsii.member(jsii_name="webSocketStage")
    def web_socket_stage(self) -> _aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketStage:
        return typing.cast(_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketStage, jsii.get(self, "webSocketStage"))

    @builtins.property
    @jsii.member(jsii_name="webSocketUrl")
    def web_socket_url(self) -> builtins.str:
        '''Get the WebSocket API URL (useful for outputs).'''
        return typing.cast(builtins.str, jsii.get(self, "webSocketUrl"))

    @builtins.property
    @jsii.member(jsii_name="apiGatewayLogGroup")
    def api_gateway_log_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup]:
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup], jsii.get(self, "apiGatewayLogGroup"))

    @builtins.property
    @jsii.member(jsii_name="aRecord")
    def a_record(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.ARecord]:
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.ARecord], jsii.get(self, "aRecord"))

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], jsii.get(self, "certificate"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[_aws_cdk_aws_apigatewayv2_ceddda9d.DomainName]:
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_ceddda9d.DomainName], jsii.get(self, "domain"))


@jsii.data_type(
    jsii_type="must-cdk.WebSocketApiGatewayToLambdaProps",
    jsii_struct_bases=[TaggableProps],
    name_mapping={
        "tags": "tags",
        "api_name": "apiName",
        "lambda_function": "lambdaFunction",
        "api_props": "apiProps",
        "custom_domain_name": "customDomainName",
        "custom_routes": "customRoutes",
        "enable_logging": "enableLogging",
        "existing_certificate": "existingCertificate",
        "hosted_zone": "hostedZone",
        "log_group_props": "logGroupProps",
        "stage_name": "stageName",
    },
)
class WebSocketApiGatewayToLambdaProps(TaggableProps):
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        api_name: builtins.str,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        custom_routes: typing.Optional[typing.Sequence[typing.Union["WebSocketRoute", typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        :param api_name: WebSocket API configuration.
        :param lambda_function: Primary Lambda function for the API (usually handles $default route).
        :param api_props: 
        :param custom_domain_name: Optional custom domain name for API Gateway.
        :param custom_routes: Custom routes for WebSocket API Common routes: $connect, $disconnect, $default, or custom route keys.
        :param enable_logging: Enable CloudWatch logging for API Gateway.
        :param existing_certificate: Optional ACM certificate to use instead of creating a new one.
        :param hosted_zone: Optional Route53 hosted zone for custom domain.
        :param log_group_props: CloudWatch Logs configuration.
        :param stage_name: Stage name for the WebSocket API. Default: 'dev'
        '''
        if isinstance(api_props, dict):
            api_props = _aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps(**api_props)
        if isinstance(log_group_props, dict):
            log_group_props = _aws_cdk_aws_logs_ceddda9d.LogGroupProps(**log_group_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f4cdf57fbe667cd56ca0962570b3a041ac0113f05528d7f2964cb201e11e6e)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument api_name", value=api_name, expected_type=type_hints["api_name"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument api_props", value=api_props, expected_type=type_hints["api_props"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument custom_routes", value=custom_routes, expected_type=type_hints["custom_routes"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument existing_certificate", value=existing_certificate, expected_type=type_hints["existing_certificate"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_name": api_name,
            "lambda_function": lambda_function,
        }
        if tags is not None:
            self._values["tags"] = tags
        if api_props is not None:
            self._values["api_props"] = api_props
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if custom_routes is not None:
            self._values["custom_routes"] = custom_routes
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if existing_certificate is not None:
            self._values["existing_certificate"] = existing_certificate
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags.

        Environment variable supports multiple formats:

        - Key-value pairs: TAGS=key1=value1,key2=value2
        - JSON string: TAGS='{"key1":"value1","key2":"value2"}'
        - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def api_name(self) -> builtins.str:
        '''WebSocket API configuration.'''
        result = self._values.get("api_name")
        assert result is not None, "Required property 'api_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''Primary Lambda function for the API (usually handles $default route).'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def api_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps]:
        result = self._values.get("api_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''Optional custom domain name for API Gateway.'''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_routes(self) -> typing.Optional[typing.List["WebSocketRoute"]]:
        '''Custom routes for WebSocket API Common routes: $connect, $disconnect, $default, or custom route keys.'''
        result = self._values.get("custom_routes")
        return typing.cast(typing.Optional[typing.List["WebSocketRoute"]], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable CloudWatch logging for API Gateway.'''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def existing_certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''Optional ACM certificate to use instead of creating a new one.'''
        result = self._values.get("existing_certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''Optional Route53 hosted zone for custom domain.'''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    @builtins.property
    def log_group_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps]:
        '''CloudWatch Logs configuration.'''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''Stage name for the WebSocket API.

        :default: 'dev'
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketApiGatewayToLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.WebSocketRoute",
    jsii_struct_bases=[],
    name_mapping={
        "handler": "handler",
        "route_key": "routeKey",
        "route_response_selection_expression": "routeResponseSelectionExpression",
    },
)
class WebSocketRoute:
    def __init__(
        self,
        *,
        handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        route_key: builtins.str,
        route_response_selection_expression: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param handler: 
        :param route_key: 
        :param route_response_selection_expression: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34bf0c8251244f50bde7c9d5fe60d88348a1be2cec9ac52b2fae8d7918d72b62)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument route_key", value=route_key, expected_type=type_hints["route_key"])
            check_type(argname="argument route_response_selection_expression", value=route_response_selection_expression, expected_type=type_hints["route_response_selection_expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "handler": handler,
            "route_key": route_key,
        }
        if route_response_selection_expression is not None:
            self._values["route_response_selection_expression"] = route_response_selection_expression

    @builtins.property
    def handler(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def route_key(self) -> builtins.str:
        result = self._values.get("route_key")
        assert result is not None, "Required property 'route_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def route_response_selection_expression(self) -> typing.Optional[builtins.str]:
        result = self._values.get("route_response_selection_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebSocketRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.AmplifyAppProps",
    jsii_struct_bases=[TaggableProps],
    name_mapping={
        "tags": "tags",
        "app_name": "appName",
        "repository": "repository",
        "access_token": "accessToken",
        "basic_auth": "basicAuth",
        "branches": "branches",
        "build_settings": "buildSettings",
        "build_spec": "buildSpec",
        "custom_domain": "customDomain",
        "custom_rules": "customRules",
        "environment_variables": "environmentVariables",
        "platform": "platform",
    },
)
class AmplifyAppProps(TaggableProps):
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        app_name: builtins.str,
        repository: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        basic_auth: typing.Optional[typing.Union[BasicAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        branches: typing.Optional[typing.Sequence[typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_settings: typing.Optional[typing.Union[BuildSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        custom_domain: typing.Optional[typing.Union[CustomDomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        custom_rules: typing.Optional[typing.Sequence[typing.Union[CustomRule, typing.Dict[builtins.str, typing.Any]]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for creating an AWS Amplify application.

        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        :param app_name: The name for the Amplify app.
        :param repository: The Git repository URL for the Amplify app. Format: https://github.com/user/repo or similar.
        :param access_token: GitHub personal access token for repository access. If not provided, will attempt to use GitHub CLI token or MUFIN_PUSH_TOKEN environment variable. Note: For production deployments, consider migrating to GitHub Apps for better security, organization support, and higher rate limits after initial setup.
        :param basic_auth: Basic authentication configuration for the Amplify app.
        :param branches: Branch configurations for the Amplify app. If not provided, a default 'main' branch will be created.
        :param build_settings: Build settings for the Amplify app.
        :param build_spec: Build specification for the Amplify app. Defines the build commands and output artifacts.
        :param custom_domain: Custom domain configuration for the Amplify app.
        :param custom_rules: Custom rules for the Amplify app. Used for redirects, rewrites, and other routing rules.
        :param environment_variables: Environment variables for the Amplify app. These will be available during the build process.
        :param platform: Platform for the Amplify app. Default: "WEB"
        '''
        if isinstance(basic_auth, dict):
            basic_auth = BasicAuthConfig(**basic_auth)
        if isinstance(build_settings, dict):
            build_settings = BuildSettings(**build_settings)
        if isinstance(custom_domain, dict):
            custom_domain = CustomDomainOptions(**custom_domain)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f2d26f324aac8877f83acfee58ebabf79ac8533e9ba6ca607e92e68086cc22)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument build_settings", value=build_settings, expected_type=type_hints["build_settings"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument custom_domain", value=custom_domain, expected_type=type_hints["custom_domain"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_name": app_name,
            "repository": repository,
        }
        if tags is not None:
            self._values["tags"] = tags
        if access_token is not None:
            self._values["access_token"] = access_token
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branches is not None:
            self._values["branches"] = branches
        if build_settings is not None:
            self._values["build_settings"] = build_settings
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if custom_domain is not None:
            self._values["custom_domain"] = custom_domain
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if platform is not None:
            self._values["platform"] = platform

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags.

        Environment variable supports multiple formats:

        - Key-value pairs: TAGS=key1=value1,key2=value2
        - JSON string: TAGS='{"key1":"value1","key2":"value2"}'
        - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def app_name(self) -> builtins.str:
        '''The name for the Amplify app.'''
        result = self._values.get("app_name")
        assert result is not None, "Required property 'app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''The Git repository URL for the Amplify app.

        Format: https://github.com/user/repo or similar.
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''GitHub personal access token for repository access.

        If not provided, will attempt to use GitHub CLI token or MUFIN_PUSH_TOKEN environment variable.

        Note: For production deployments, consider migrating to GitHub Apps for better security,
        organization support, and higher rate limits after initial setup.
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuthConfig]:
        '''Basic authentication configuration for the Amplify app.'''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuthConfig], result)

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[BranchOptions]]:
        '''Branch configurations for the Amplify app.

        If not provided, a default 'main' branch will be created.
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[BranchOptions]], result)

    @builtins.property
    def build_settings(self) -> typing.Optional[BuildSettings]:
        '''Build settings for the Amplify app.'''
        result = self._values.get("build_settings")
        return typing.cast(typing.Optional[BuildSettings], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''Build specification for the Amplify app.

        Defines the build commands and output artifacts.
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain(self) -> typing.Optional[CustomDomainOptions]:
        '''Custom domain configuration for the Amplify app.'''
        result = self._values.get("custom_domain")
        return typing.cast(typing.Optional[CustomDomainOptions], result)

    @builtins.property
    def custom_rules(self) -> typing.Optional[typing.List[CustomRule]]:
        '''Custom rules for the Amplify app.

        Used for redirects, rewrites, and other routing rules.
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.List[CustomRule]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables for the Amplify app.

        These will be available during the build process.
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''Platform for the Amplify app.

        :default: "WEB"
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmplifyAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.ApiGatewayToLambdaProps",
    jsii_struct_bases=[TaggableProps],
    name_mapping={
        "tags": "tags",
        "api_name": "apiName",
        "lambda_function": "lambdaFunction",
        "binary_media_types": "binaryMediaTypes",
        "create_usage_plan": "createUsagePlan",
        "custom_domain_name": "customDomainName",
        "custom_routes": "customRoutes",
        "enable_logging": "enableLogging",
        "existing_certificate": "existingCertificate",
        "hosted_zone": "hostedZone",
        "lambda_api_props": "lambdaApiProps",
        "log_group_props": "logGroupProps",
        "proxy": "proxy",
        "rest_api_props": "restApiProps",
    },
)
class ApiGatewayToLambdaProps(TaggableProps):
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        api_name: builtins.str,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
        create_usage_plan: typing.Optional[builtins.bool] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        custom_routes: typing.Optional[typing.Sequence[typing.Union[CustomRoute, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        lambda_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
        log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
        proxy: typing.Optional[builtins.bool] = None,
        rest_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        :param api_name: API configuration.
        :param lambda_function: Primary Lambda function for the API.
        :param binary_media_types: Binary media types for the API This setting will be applied regardless of whether LambdaRestApi or RestApi is used.
        :param create_usage_plan: Whether to create a Usage Plan.
        :param custom_domain_name: Optional custom domain name for API Gateway.
        :param custom_routes: Custom routes for manual API setup (when proxy is false) If provided, will use RestApi instead of LambdaRestApi.
        :param enable_logging: Enable CloudWatch logging for API Gateway.
        :param existing_certificate: Optional ACM certificate to use instead of creating a new one.
        :param hosted_zone: Optional Route53 hosted zone for custom domain.
        :param lambda_api_props: 
        :param log_group_props: CloudWatch Logs configuration.
        :param proxy: 
        :param rest_api_props: 
        '''
        if isinstance(lambda_api_props, dict):
            lambda_api_props = _aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps(**lambda_api_props)
        if isinstance(log_group_props, dict):
            log_group_props = _aws_cdk_aws_logs_ceddda9d.LogGroupProps(**log_group_props)
        if isinstance(rest_api_props, dict):
            rest_api_props = _aws_cdk_aws_apigateway_ceddda9d.RestApiProps(**rest_api_props)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c51143b7da8fc50ffd3240aae88642c332f9ccc1136e275abf9d1065df7ea17)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument api_name", value=api_name, expected_type=type_hints["api_name"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument binary_media_types", value=binary_media_types, expected_type=type_hints["binary_media_types"])
            check_type(argname="argument create_usage_plan", value=create_usage_plan, expected_type=type_hints["create_usage_plan"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument custom_routes", value=custom_routes, expected_type=type_hints["custom_routes"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument existing_certificate", value=existing_certificate, expected_type=type_hints["existing_certificate"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument lambda_api_props", value=lambda_api_props, expected_type=type_hints["lambda_api_props"])
            check_type(argname="argument log_group_props", value=log_group_props, expected_type=type_hints["log_group_props"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument rest_api_props", value=rest_api_props, expected_type=type_hints["rest_api_props"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "api_name": api_name,
            "lambda_function": lambda_function,
        }
        if tags is not None:
            self._values["tags"] = tags
        if binary_media_types is not None:
            self._values["binary_media_types"] = binary_media_types
        if create_usage_plan is not None:
            self._values["create_usage_plan"] = create_usage_plan
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if custom_routes is not None:
            self._values["custom_routes"] = custom_routes
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if existing_certificate is not None:
            self._values["existing_certificate"] = existing_certificate
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if lambda_api_props is not None:
            self._values["lambda_api_props"] = lambda_api_props
        if log_group_props is not None:
            self._values["log_group_props"] = log_group_props
        if proxy is not None:
            self._values["proxy"] = proxy
        if rest_api_props is not None:
            self._values["rest_api_props"] = rest_api_props

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags.

        Environment variable supports multiple formats:

        - Key-value pairs: TAGS=key1=value1,key2=value2
        - JSON string: TAGS='{"key1":"value1","key2":"value2"}'
        - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def api_name(self) -> builtins.str:
        '''API configuration.'''
        result = self._values.get("api_name")
        assert result is not None, "Required property 'api_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lambda_function(self) -> _aws_cdk_aws_lambda_ceddda9d.IFunction:
        '''Primary Lambda function for the API.'''
        result = self._values.get("lambda_function")
        assert result is not None, "Required property 'lambda_function' is missing"
        return typing.cast(_aws_cdk_aws_lambda_ceddda9d.IFunction, result)

    @builtins.property
    def binary_media_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Binary media types for the API This setting will be applied regardless of whether LambdaRestApi or RestApi is used.'''
        result = self._values.get("binary_media_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def create_usage_plan(self) -> typing.Optional[builtins.bool]:
        '''Whether to create a Usage Plan.'''
        result = self._values.get("create_usage_plan")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''Optional custom domain name for API Gateway.'''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_routes(self) -> typing.Optional[typing.List[CustomRoute]]:
        '''Custom routes for manual API setup (when proxy is false) If provided, will use RestApi instead of LambdaRestApi.'''
        result = self._values.get("custom_routes")
        return typing.cast(typing.Optional[typing.List[CustomRoute]], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable CloudWatch logging for API Gateway.'''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def existing_certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''Optional ACM certificate to use instead of creating a new one.'''
        result = self._values.get("existing_certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''Optional Route53 hosted zone for custom domain.'''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    @builtins.property
    def lambda_api_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps]:
        result = self._values.get("lambda_api_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps], result)

    @builtins.property
    def log_group_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps]:
        '''CloudWatch Logs configuration.'''
        result = self._values.get("log_group_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroupProps], result)

    @builtins.property
    def proxy(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rest_api_props(
        self,
    ) -> typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps]:
        result = self._values.get("rest_api_props")
        return typing.cast(typing.Optional[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayToLambdaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.CloudFrontToOriginsProps",
    jsii_struct_bases=[TaggableProps],
    name_mapping={
        "tags": "tags",
        "additional_domain_names": "additionalDomainNames",
        "cache_behaviors": "cacheBehaviors",
        "certificate": "certificate",
        "comment": "comment",
        "create_route53_records": "createRoute53Records",
        "custom_domain_name": "customDomainName",
        "default_origin_id": "defaultOriginId",
        "default_root_object": "defaultRootObject",
        "enabled": "enabled",
        "enable_ipv6": "enableIpv6",
        "enable_logging": "enableLogging",
        "error_pages": "errorPages",
        "geo_restriction": "geoRestriction",
        "hosted_zone": "hostedZone",
        "http_origins": "httpOrigins",
        "http_version": "httpVersion",
        "log_bucket": "logBucket",
        "log_include_cookies": "logIncludeCookies",
        "log_prefix": "logPrefix",
        "price_class": "priceClass",
        "s3_origins": "s3Origins",
        "web_acl_id": "webAclId",
    },
)
class CloudFrontToOriginsProps(TaggableProps):
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        cache_behaviors: typing.Optional[typing.Sequence[typing.Union[CacheBehaviorConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
        comment: typing.Optional[builtins.str] = None,
        create_route53_records: typing.Optional[builtins.bool] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        default_origin_id: typing.Optional[builtins.str] = None,
        default_root_object: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        enable_ipv6: typing.Optional[builtins.bool] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        error_pages: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
        geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
        hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
        http_origins: typing.Optional[typing.Sequence[typing.Union[HttpOriginConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
        log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
        log_include_cookies: typing.Optional[builtins.bool] = None,
        log_prefix: typing.Optional[builtins.str] = None,
        price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
        s3_origins: typing.Optional[typing.Sequence[typing.Union[S3OriginConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
        web_acl_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        :param additional_domain_names: Additional domain names (aliases) for the distribution Note: All domains must be covered by the same certificate. CloudFront only supports one certificate per distribution.
        :param cache_behaviors: Cache behaviors for specific path patterns.
        :param certificate: Existing ACM certificate to use for the CloudFront distribution Certificate must be in us-east-1 region for CloudFront. The certificate must cover all domains (customDomainName + additionalDomainNames). CloudFront only supports one certificate per distribution.
        :param comment: Comment for the distribution.
        :param create_route53_records: Create Route53 records for all domain names. Default: true if hostedZone is provided
        :param custom_domain_name: Primary custom domain name for the CloudFront distribution.
        :param default_origin_id: ID of the origin to use as default behavior If not specified, will use the first HTTP origin, then first S3 origin.
        :param default_root_object: Default root object for the distribution. Default: "index.html"
        :param enabled: Whether the distribution is enabled. Default: true
        :param enable_ipv6: Enable IPv6 for the distribution. Default: false
        :param enable_logging: Enable CloudFront access logging. Default: true
        :param error_pages: Custom error page configurations If not provided, intelligent defaults will be applied based on origin types.
        :param geo_restriction: Geographic restriction configuration.
        :param hosted_zone: Route53 hosted zone for the custom domain Required for creating Route53 records.
        :param http_origins: HTTP origins configuration.
        :param http_version: HTTP version to support. Default: HttpVersion.HTTP2
        :param log_bucket: Existing S3 bucket for logs If not provided and logging is enabled, a new bucket will be created.
        :param log_include_cookies: Include cookies in access logs. Default: false
        :param log_prefix: Prefix for log files. Default: "cloudfront"
        :param price_class: CloudFront distribution price class. Default: PRICE_CLASS_100
        :param s3_origins: S3 origins configuration.
        :param web_acl_id: Web Application Firewall (WAF) web ACL ID.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e35e3363ae35d50e0f0dd18a9ae11be6e9daf52ba8d2c783abfb12aff9b21376)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument additional_domain_names", value=additional_domain_names, expected_type=type_hints["additional_domain_names"])
            check_type(argname="argument cache_behaviors", value=cache_behaviors, expected_type=type_hints["cache_behaviors"])
            check_type(argname="argument certificate", value=certificate, expected_type=type_hints["certificate"])
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
            check_type(argname="argument create_route53_records", value=create_route53_records, expected_type=type_hints["create_route53_records"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument default_origin_id", value=default_origin_id, expected_type=type_hints["default_origin_id"])
            check_type(argname="argument default_root_object", value=default_root_object, expected_type=type_hints["default_root_object"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument enable_ipv6", value=enable_ipv6, expected_type=type_hints["enable_ipv6"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument error_pages", value=error_pages, expected_type=type_hints["error_pages"])
            check_type(argname="argument geo_restriction", value=geo_restriction, expected_type=type_hints["geo_restriction"])
            check_type(argname="argument hosted_zone", value=hosted_zone, expected_type=type_hints["hosted_zone"])
            check_type(argname="argument http_origins", value=http_origins, expected_type=type_hints["http_origins"])
            check_type(argname="argument http_version", value=http_version, expected_type=type_hints["http_version"])
            check_type(argname="argument log_bucket", value=log_bucket, expected_type=type_hints["log_bucket"])
            check_type(argname="argument log_include_cookies", value=log_include_cookies, expected_type=type_hints["log_include_cookies"])
            check_type(argname="argument log_prefix", value=log_prefix, expected_type=type_hints["log_prefix"])
            check_type(argname="argument price_class", value=price_class, expected_type=type_hints["price_class"])
            check_type(argname="argument s3_origins", value=s3_origins, expected_type=type_hints["s3_origins"])
            check_type(argname="argument web_acl_id", value=web_acl_id, expected_type=type_hints["web_acl_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if tags is not None:
            self._values["tags"] = tags
        if additional_domain_names is not None:
            self._values["additional_domain_names"] = additional_domain_names
        if cache_behaviors is not None:
            self._values["cache_behaviors"] = cache_behaviors
        if certificate is not None:
            self._values["certificate"] = certificate
        if comment is not None:
            self._values["comment"] = comment
        if create_route53_records is not None:
            self._values["create_route53_records"] = create_route53_records
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if default_origin_id is not None:
            self._values["default_origin_id"] = default_origin_id
        if default_root_object is not None:
            self._values["default_root_object"] = default_root_object
        if enabled is not None:
            self._values["enabled"] = enabled
        if enable_ipv6 is not None:
            self._values["enable_ipv6"] = enable_ipv6
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if error_pages is not None:
            self._values["error_pages"] = error_pages
        if geo_restriction is not None:
            self._values["geo_restriction"] = geo_restriction
        if hosted_zone is not None:
            self._values["hosted_zone"] = hosted_zone
        if http_origins is not None:
            self._values["http_origins"] = http_origins
        if http_version is not None:
            self._values["http_version"] = http_version
        if log_bucket is not None:
            self._values["log_bucket"] = log_bucket
        if log_include_cookies is not None:
            self._values["log_include_cookies"] = log_include_cookies
        if log_prefix is not None:
            self._values["log_prefix"] = log_prefix
        if price_class is not None:
            self._values["price_class"] = price_class
        if s3_origins is not None:
            self._values["s3_origins"] = s3_origins
        if web_acl_id is not None:
            self._values["web_acl_id"] = web_acl_id

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags.

        Environment variable supports multiple formats:

        - Key-value pairs: TAGS=key1=value1,key2=value2
        - JSON string: TAGS='{"key1":"value1","key2":"value2"}'
        - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def additional_domain_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional domain names (aliases) for the distribution Note: All domains must be covered by the same certificate.

        CloudFront only supports one certificate per distribution.
        '''
        result = self._values.get("additional_domain_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cache_behaviors(self) -> typing.Optional[typing.List[CacheBehaviorConfig]]:
        '''Cache behaviors for specific path patterns.'''
        result = self._values.get("cache_behaviors")
        return typing.cast(typing.Optional[typing.List[CacheBehaviorConfig]], result)

    @builtins.property
    def certificate(
        self,
    ) -> typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]:
        '''Existing ACM certificate to use for the CloudFront distribution Certificate must be in us-east-1 region for CloudFront.

        The certificate must cover all domains (customDomainName + additionalDomainNames).
        CloudFront only supports one certificate per distribution.
        '''
        result = self._values.get("certificate")
        return typing.cast(typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate], result)

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''Comment for the distribution.'''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_route53_records(self) -> typing.Optional[builtins.bool]:
        '''Create Route53 records for all domain names.

        :default: true if hostedZone is provided
        '''
        result = self._values.get("create_route53_records")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''Primary custom domain name for the CloudFront distribution.'''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_origin_id(self) -> typing.Optional[builtins.str]:
        '''ID of the origin to use as default behavior If not specified, will use the first HTTP origin, then first S3 origin.'''
        result = self._values.get("default_origin_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_root_object(self) -> typing.Optional[builtins.str]:
        '''Default root object for the distribution.

        :default: "index.html"
        '''
        result = self._values.get("default_root_object")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether the distribution is enabled.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_ipv6(self) -> typing.Optional[builtins.bool]:
        '''Enable IPv6 for the distribution.

        :default: false
        '''
        result = self._values.get("enable_ipv6")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''Enable CloudFront access logging.

        :default: true
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def error_pages(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]]:
        '''Custom error page configurations If not provided, intelligent defaults will be applied based on origin types.'''
        result = self._values.get("error_pages")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse]], result)

    @builtins.property
    def geo_restriction(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction]:
        '''Geographic restriction configuration.'''
        result = self._values.get("geo_restriction")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction], result)

    @builtins.property
    def hosted_zone(self) -> typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone]:
        '''Route53 hosted zone for the custom domain Required for creating Route53 records.'''
        result = self._values.get("hosted_zone")
        return typing.cast(typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone], result)

    @builtins.property
    def http_origins(self) -> typing.Optional[typing.List[HttpOriginConfig]]:
        '''HTTP origins configuration.'''
        result = self._values.get("http_origins")
        return typing.cast(typing.Optional[typing.List[HttpOriginConfig]], result)

    @builtins.property
    def http_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion]:
        '''HTTP version to support.

        :default: HttpVersion.HTTP2
        '''
        result = self._values.get("http_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion], result)

    @builtins.property
    def log_bucket(self) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket]:
        '''Existing S3 bucket for logs If not provided and logging is enabled, a new bucket will be created.'''
        result = self._values.get("log_bucket")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket], result)

    @builtins.property
    def log_include_cookies(self) -> typing.Optional[builtins.bool]:
        '''Include cookies in access logs.

        :default: false
        '''
        result = self._values.get("log_include_cookies")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def log_prefix(self) -> typing.Optional[builtins.str]:
        '''Prefix for log files.

        :default: "cloudfront"
        '''
        result = self._values.get("log_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def price_class(
        self,
    ) -> typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass]:
        '''CloudFront distribution price class.

        :default: PRICE_CLASS_100
        '''
        result = self._values.get("price_class")
        return typing.cast(typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass], result)

    @builtins.property
    def s3_origins(self) -> typing.Optional[typing.List[S3OriginConfig]]:
        '''S3 origins configuration.'''
        result = self._values.get("s3_origins")
        return typing.cast(typing.Optional[typing.List[S3OriginConfig]], result)

    @builtins.property
    def web_acl_id(self) -> typing.Optional[builtins.str]:
        '''Web Application Firewall (WAF) web ACL ID.'''
        result = self._values.get("web_acl_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFrontToOriginsProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="must-cdk.EcsCodeDeployProps",
    jsii_struct_bases=[TaggableProps],
    name_mapping={
        "tags": "tags",
        "cluster": "cluster",
        "containers": "containers",
        "security_groups": "securityGroups",
        "service_name": "serviceName",
        "task_subnets": "taskSubnets",
        "vpc": "vpc",
        "code_deploy_application": "codeDeployApplication",
        "deployment_group": "deploymentGroup",
        "load_balancer": "loadBalancer",
        "load_balancer_subnets": "loadBalancerSubnets",
        "production_listener": "productionListener",
        "production_target_group": "productionTargetGroup",
        "service": "service",
        "target_port": "targetPort",
        "task_definition": "taskDefinition",
        "test_listener": "testListener",
        "test_target_group": "testTargetGroup",
    },
)
class EcsCodeDeployProps(TaggableProps):
    def __init__(
        self,
        *,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
        containers: typing.Sequence[typing.Union[ContainerConfig, typing.Dict[builtins.str, typing.Any]]],
        security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
        service_name: builtins.str,
        task_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        code_deploy_application: typing.Optional[typing.Union[CodeDeployApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        deployment_group: typing.Optional[typing.Union[DeploymentGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer: typing.Optional[typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        load_balancer_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        production_listener: typing.Optional[typing.Union[ListenerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        production_target_group: typing.Optional[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        service: typing.Optional[typing.Union[ServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        target_port: typing.Optional[jsii.Number] = None,
        task_definition: typing.Optional[typing.Union[TaskDefinitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        test_listener: typing.Optional[typing.Union[ListenerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        test_target_group: typing.Optional[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for the EcsCodeDeploy construct using native AWS CDK interfaces.

        :param tags: Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags. Environment variable supports multiple formats: - Key-value pairs: TAGS=key1=value1,key2=value2 - JSON string: TAGS='{"key1":"value1","key2":"value2"}' - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        :param cluster: ECS Cluster where the service will run.
        :param containers: Container configurations using native CDK interfaces.
        :param security_groups: Security groups for ECS service (required).
        :param service_name: Base name used for resources like log groups, roles, services, etc.
        :param task_subnets: Subnets for ECS tasks (required). IMPORTANT: This controls where your ECS containers run. Use private subnets for security. To limit to specific AZs: { availabilityZones: ['us-east-1a'] } For all private subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }
        :param vpc: VPC in which to deploy ECS and ALB resources.
        :param code_deploy_application: CodeDeploy application configuration.
        :param deployment_group: CodeDeploy deployment group configuration.
        :param load_balancer: Load balancer configuration options.
        :param load_balancer_subnets: Subnets for ALB (optional, defaults to taskSubnets). IMPORTANT: This controls where your Load Balancer runs, NOT your containers! - For internet-facing ALBs: Use PUBLIC subnets across multiple AZs - For internal ALBs: Use PRIVATE subnets across multiple AZs - Common mistake: Restricting ALB to single AZ reduces availability Examples: - All public subnets: { subnetType: ec2.SubnetType.PUBLIC } - Specific AZs: { availabilityZones: ['us-east-1a', 'us-east-1b'] } - Default (all subnets): {} or undefined
        :param production_listener: Production listener configuration.
        :param production_target_group: Production target group configuration.
        :param service: Service configuration options.
        :param target_port: The port to expose on the target group (defaults to first container's port).
        :param task_definition: Task definition configuration options.
        :param test_listener: Test listener configuration (optional - defaults will be used if not provided).
        :param test_target_group: Test target group configuration (optional - defaults will be used if not provided).
        '''
        if isinstance(task_subnets, dict):
            task_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**task_subnets)
        if isinstance(code_deploy_application, dict):
            code_deploy_application = CodeDeployApplicationConfig(**code_deploy_application)
        if isinstance(deployment_group, dict):
            deployment_group = DeploymentGroupConfig(**deployment_group)
        if isinstance(load_balancer, dict):
            load_balancer = LoadBalancerConfig(**load_balancer)
        if isinstance(load_balancer_subnets, dict):
            load_balancer_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**load_balancer_subnets)
        if isinstance(production_listener, dict):
            production_listener = ListenerConfig(**production_listener)
        if isinstance(production_target_group, dict):
            production_target_group = TargetGroupConfig(**production_target_group)
        if isinstance(service, dict):
            service = ServiceConfig(**service)
        if isinstance(task_definition, dict):
            task_definition = TaskDefinitionConfig(**task_definition)
        if isinstance(test_listener, dict):
            test_listener = ListenerConfig(**test_listener)
        if isinstance(test_target_group, dict):
            test_target_group = TargetGroupConfig(**test_target_group)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e1edfc306738ea99e0bd03a55876d7f75a063970dd3103fc1bbb766dff014b1)
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument task_subnets", value=task_subnets, expected_type=type_hints["task_subnets"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument code_deploy_application", value=code_deploy_application, expected_type=type_hints["code_deploy_application"])
            check_type(argname="argument deployment_group", value=deployment_group, expected_type=type_hints["deployment_group"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument load_balancer_subnets", value=load_balancer_subnets, expected_type=type_hints["load_balancer_subnets"])
            check_type(argname="argument production_listener", value=production_listener, expected_type=type_hints["production_listener"])
            check_type(argname="argument production_target_group", value=production_target_group, expected_type=type_hints["production_target_group"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument target_port", value=target_port, expected_type=type_hints["target_port"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument test_listener", value=test_listener, expected_type=type_hints["test_listener"])
            check_type(argname="argument test_target_group", value=test_target_group, expected_type=type_hints["test_target_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cluster": cluster,
            "containers": containers,
            "security_groups": security_groups,
            "service_name": service_name,
            "task_subnets": task_subnets,
            "vpc": vpc,
        }
        if tags is not None:
            self._values["tags"] = tags
        if code_deploy_application is not None:
            self._values["code_deploy_application"] = code_deploy_application
        if deployment_group is not None:
            self._values["deployment_group"] = deployment_group
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if load_balancer_subnets is not None:
            self._values["load_balancer_subnets"] = load_balancer_subnets
        if production_listener is not None:
            self._values["production_listener"] = production_listener
        if production_target_group is not None:
            self._values["production_target_group"] = production_target_group
        if service is not None:
            self._values["service"] = service
        if target_port is not None:
            self._values["target_port"] = target_port
        if task_definition is not None:
            self._values["task_definition"] = task_definition
        if test_listener is not None:
            self._values["test_listener"] = test_listener
        if test_target_group is not None:
            self._values["test_target_group"] = test_target_group

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Additional tags to apply to resources. Note: Tags from TAGS environment variable will take precedence over these tags.

        Environment variable supports multiple formats:

        - Key-value pairs: TAGS=key1=value1,key2=value2
        - JSON string: TAGS='{"key1":"value1","key2":"value2"}'
        - JSON object (dict): TAGS={"Product":"Mufin","Owner":"Platform"}
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.ICluster:
        '''ECS Cluster where the service will run.'''
        result = self._values.get("cluster")
        assert result is not None, "Required property 'cluster' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ICluster, result)

    @builtins.property
    def containers(self) -> typing.List[ContainerConfig]:
        '''Container configurations using native CDK interfaces.'''
        result = self._values.get("containers")
        assert result is not None, "Required property 'containers' is missing"
        return typing.cast(typing.List[ContainerConfig], result)

    @builtins.property
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''Security groups for ECS service (required).'''
        result = self._values.get("security_groups")
        assert result is not None, "Required property 'security_groups' is missing"
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''Base name used for resources like log groups, roles, services, etc.'''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def task_subnets(self) -> _aws_cdk_aws_ec2_ceddda9d.SubnetSelection:
        '''Subnets for ECS tasks (required).

        IMPORTANT: This controls where your ECS containers run. Use private subnets for security.
        To limit to specific AZs: { availabilityZones: ['us-east-1a'] }
        For all private subnets: { subnetType: ec2.SubnetType.PRIVATE_WITH_EGRESS }
        '''
        result = self._values.get("task_subnets")
        assert result is not None, "Required property 'task_subnets' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''VPC in which to deploy ECS and ALB resources.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def code_deploy_application(self) -> typing.Optional[CodeDeployApplicationConfig]:
        '''CodeDeploy application configuration.'''
        result = self._values.get("code_deploy_application")
        return typing.cast(typing.Optional[CodeDeployApplicationConfig], result)

    @builtins.property
    def deployment_group(self) -> typing.Optional[DeploymentGroupConfig]:
        '''CodeDeploy deployment group configuration.'''
        result = self._values.get("deployment_group")
        return typing.cast(typing.Optional[DeploymentGroupConfig], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional[LoadBalancerConfig]:
        '''Load balancer configuration options.'''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[LoadBalancerConfig], result)

    @builtins.property
    def load_balancer_subnets(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Subnets for ALB (optional, defaults to taskSubnets).

        IMPORTANT: This controls where your Load Balancer runs, NOT your containers!

        - For internet-facing ALBs: Use PUBLIC subnets across multiple AZs
        - For internal ALBs: Use PRIVATE subnets across multiple AZs
        - Common mistake: Restricting ALB to single AZ reduces availability

        Examples:

        - All public subnets: { subnetType: ec2.SubnetType.PUBLIC }
        - Specific AZs: { availabilityZones: ['us-east-1a', 'us-east-1b'] }
        - Default (all subnets): {} or undefined
        '''
        result = self._values.get("load_balancer_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def production_listener(self) -> typing.Optional[ListenerConfig]:
        '''Production listener configuration.'''
        result = self._values.get("production_listener")
        return typing.cast(typing.Optional[ListenerConfig], result)

    @builtins.property
    def production_target_group(self) -> typing.Optional[TargetGroupConfig]:
        '''Production target group configuration.'''
        result = self._values.get("production_target_group")
        return typing.cast(typing.Optional[TargetGroupConfig], result)

    @builtins.property
    def service(self) -> typing.Optional[ServiceConfig]:
        '''Service configuration options.'''
        result = self._values.get("service")
        return typing.cast(typing.Optional[ServiceConfig], result)

    @builtins.property
    def target_port(self) -> typing.Optional[jsii.Number]:
        '''The port to expose on the target group (defaults to first container's port).'''
        result = self._values.get("target_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def task_definition(self) -> typing.Optional[TaskDefinitionConfig]:
        '''Task definition configuration options.'''
        result = self._values.get("task_definition")
        return typing.cast(typing.Optional[TaskDefinitionConfig], result)

    @builtins.property
    def test_listener(self) -> typing.Optional[ListenerConfig]:
        '''Test listener configuration (optional - defaults will be used if not provided).'''
        result = self._values.get("test_listener")
        return typing.cast(typing.Optional[ListenerConfig], result)

    @builtins.property
    def test_target_group(self) -> typing.Optional[TargetGroupConfig]:
        '''Test target group configuration (optional - defaults will be used if not provided).'''
        result = self._values.get("test_target_group")
        return typing.cast(typing.Optional[TargetGroupConfig], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsCodeDeployProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmplifyApp",
    "AmplifyAppProps",
    "ApiGatewayToLambda",
    "ApiGatewayToLambdaProps",
    "BasicAuthConfig",
    "BranchOptions",
    "BuildSettings",
    "CacheBehaviorConfig",
    "CloudFrontToOrigins",
    "CloudFrontToOriginsProps",
    "CodeDeployApplicationConfig",
    "ContainerConfig",
    "CustomDomainOptions",
    "CustomRoute",
    "CustomRule",
    "DeploymentGroupConfig",
    "EcsCodeDeploy",
    "EcsCodeDeployProps",
    "HttpOriginConfig",
    "HttpOriginInfo",
    "ListenerConfig",
    "LoadBalancerConfig",
    "S3OriginConfig",
    "S3OriginInfo",
    "ServiceConfig",
    "SubDomainOptions",
    "TaggableProps",
    "TargetGroupConfig",
    "TaskDefinitionConfig",
    "WebSocketApiGatewayToLambda",
    "WebSocketApiGatewayToLambdaProps",
    "WebSocketRoute",
]

publication.publish()

def _typecheckingstub__777b9bbab56e86272a20ea4d9e3f1efad25bb7fea282e210cf563e8923d584d0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_name: builtins.str,
    repository: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    basic_auth: typing.Optional[typing.Union[BasicAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    branches: typing.Optional[typing.Sequence[typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_settings: typing.Optional[typing.Union[BuildSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[typing.Union[CustomDomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_rules: typing.Optional[typing.Sequence[typing.Union[CustomRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88385340a9ac0a3d345bb5f8b9e0334655a117a97d92f90c383b720f4bbd4824(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api_name: builtins.str,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_usage_plan: typing.Optional[builtins.bool] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    custom_routes: typing.Optional[typing.Sequence[typing.Union[CustomRoute, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    lambda_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy: typing.Optional[builtins.bool] = None,
    rest_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__097b1dc50c0b38ab7552cceb5b206127e52e3d3f36506f52f873d369bbe70ef3(
    *,
    password: builtins.str,
    username: builtins.str,
    enable_basic_auth: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bdd7acb58378cad16e462f75882a091b44e7545c30579297f524f5212ec7923(
    *,
    branch_name: builtins.str,
    build_spec: typing.Optional[builtins.str] = None,
    enable_auto_build: typing.Optional[builtins.bool] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c76ab27a2495b9f4e651b178bb37566be40717e7134787251b8db015853ba53(
    *,
    cache_type: typing.Optional[builtins.str] = None,
    compute_type: typing.Optional[builtins.str] = None,
    enable_auto_branch_creation: typing.Optional[builtins.bool] = None,
    enable_auto_branch_deletion: typing.Optional[builtins.bool] = None,
    enable_branch_auto_build: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09e71190d617032adb23312ff8a226e4f3a3a9c6a6886244b17283984821ac0f(
    *,
    origin_id: builtins.str,
    path_pattern: builtins.str,
    allowed_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.AllowedMethods] = None,
    cached_methods: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.CachedMethods] = None,
    cache_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ICachePolicy] = None,
    cache_policy_id: typing.Optional[builtins.str] = None,
    compress: typing.Optional[builtins.bool] = None,
    origin_request_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IOriginRequestPolicy] = None,
    origin_request_policy_id: typing.Optional[builtins.str] = None,
    response_headers_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.IResponseHeadersPolicy] = None,
    response_headers_policy_id: typing.Optional[builtins.str] = None,
    viewer_protocol_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.ViewerProtocolPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5595cb0fd40f1755eb3336459cd050240b0464ea7a04fa1bf71ac0f843be019(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_behaviors: typing.Optional[typing.Sequence[typing.Union[CacheBehaviorConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    comment: typing.Optional[builtins.str] = None,
    create_route53_records: typing.Optional[builtins.bool] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    default_origin_id: typing.Optional[builtins.str] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_ipv6: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    error_pages: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    http_origins: typing.Optional[typing.Sequence[typing.Union[HttpOriginConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_include_cookies: typing.Optional[builtins.bool] = None,
    log_prefix: typing.Optional[builtins.str] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    s3_origins: typing.Optional[typing.Sequence[typing.Union[S3OriginConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e649c2726a6488e46170e86657ba3afb312a168dbc1015cde22b0b69336f53f(
    origin_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf9864ad4075688df20b9dbf44e995106eb63bf50d190ab2434b56d977a3129(
    origin_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5502fecaec2fcacb90758335131c1b764d3da7ff95d6f9252571099bb02703(
    *,
    application_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a8f326881db7c040d8f4c23992dd449f63d8cd8f46a42695a34a87d6f822a7(
    *,
    name: builtins.str,
    options: typing.Union[_aws_cdk_aws_ecs_ceddda9d.ContainerDefinitionOptions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a9aef33f07ee4b94fd871c1fa5450b39a9a6f85d609e53d9f8d6d9d18666169(
    *,
    domain_name: builtins.str,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomainOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__037506344a4229895450ab2466c4a39abd0da2085c3a5d744bc1a0bdaf3a2c8d(
    *,
    handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    method: builtins.str,
    path: builtins.str,
    method_options: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.MethodOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39915f5b079be3a4939a38452e4b026fdbbc7aa3c31aef40d22288ff86d9b8cd(
    *,
    source: builtins.str,
    target: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03d1e7127aabea4ca4381fa09bc0557271913b6524f87fae49b42a73469e9a07(
    *,
    blue_green_deployment_config: typing.Optional[typing.Union[_aws_cdk_aws_codedeploy_ceddda9d.EcsBlueGreenDeploymentConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_config: typing.Optional[_aws_cdk_aws_codedeploy_ceddda9d.IEcsDeploymentConfig] = None,
    deployment_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19ac4f77d3bba1391929b87d2d23b70fe61e21aa6809f43ed4283d6ecf350909(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
    containers: typing.Sequence[typing.Union[ContainerConfig, typing.Dict[builtins.str, typing.Any]]],
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    service_name: builtins.str,
    task_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    code_deploy_application: typing.Optional[typing.Union[CodeDeployApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_group: typing.Optional[typing.Union[DeploymentGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer: typing.Optional[typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    production_listener: typing.Optional[typing.Union[ListenerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    production_target_group: typing.Optional[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service: typing.Optional[typing.Union[ServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    target_port: typing.Optional[jsii.Number] = None,
    task_definition: typing.Optional[typing.Union[TaskDefinitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    test_listener: typing.Optional[typing.Union[ListenerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    test_target_group: typing.Optional[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c46e442fdd0192863cab169d59fec779cadb566db29953677761c4940b26d818(
    *,
    domain_name: builtins.str,
    id: builtins.str,
    http_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
    http_port: typing.Optional[jsii.Number] = None,
    https_port: typing.Optional[jsii.Number] = None,
    origin_path: typing.Optional[builtins.str] = None,
    protocol_policy: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginProtocolPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7feea82df6d57cdecc62c96a5730f43379b516233376c0533b57e1b1d68f58f(
    *,
    id: builtins.str,
    origin: _aws_cdk_aws_cloudfront_origins_ceddda9d.HttpOrigin,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f5ab801b4e660224ccf6cf401be1529c61a4dfdb7a1404942a16c2517d178dd(
    *,
    certificates: typing.Optional[typing.Sequence[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate]] = None,
    default_action: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ListenerAction] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c5a95f45a3b1f8c843cf50d6a1005817682e3d6ff84735169cc73c06e12b10f(
    *,
    idle_timeout_seconds: typing.Optional[jsii.Number] = None,
    internet_facing: typing.Optional[builtins.bool] = None,
    load_balancer_name: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c491da83cb47b60ad107d7ab3a03d121bd5de0ec3db21592303a1459dfa81ce(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    id: builtins.str,
    origin_access_identity: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.OriginAccessIdentity] = None,
    origin_path: typing.Optional[builtins.str] = None,
    s3_origin_props: typing.Optional[typing.Union[_aws_cdk_aws_cloudfront_origins_ceddda9d.S3OriginProps, typing.Dict[builtins.str, typing.Any]]] = None,
    use_legacy_oai: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1c3ec5b8a1718b199ec940b9c6ef6af3af2ea2de8856064d69c396dd38ca634(
    *,
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83d46c6ecc0567279ab942573549709584b26f1786fd9089e850d2bd49170b6(
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    desired_count: typing.Optional[jsii.Number] = None,
    health_check_grace_period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d299494480073590a530a506b82a6958f2f0149f64e2eb929864716bb21e2e6f(
    *,
    branch_name: builtins.str,
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dc2cddf876ac6ea0c1f692c56ba26ce2e055e80dff32f5934853a7a20ab5a0(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79d412fa856e93114faca93f3f3109977421ac7571097864fad7c6f77e756f3(
    *,
    health_check: typing.Optional[typing.Union[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.HealthCheck, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancing_algorithm_type: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.TargetGroupLoadBalancingAlgorithmType] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[_aws_cdk_aws_elasticloadbalancingv2_ceddda9d.ApplicationProtocol] = None,
    slow_start: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    stickiness_cookie_duration: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    target_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82cc7c746398105f3e0d633178d0221928f104cae239c86eec0d9b408385e7c6(
    *,
    cpu: typing.Optional[jsii.Number] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    task_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15689bf8cb45b613fd6d0271ea2d2b2a40c677ff7ee1d37b34596aa645c185e9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    api_name: builtins.str,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    custom_routes: typing.Optional[typing.Sequence[typing.Union[WebSocketRoute, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f4cdf57fbe667cd56ca0962570b3a041ac0113f05528d7f2964cb201e11e6e(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    api_name: builtins.str,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigatewayv2_ceddda9d.WebSocketApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    custom_routes: typing.Optional[typing.Sequence[typing.Union[WebSocketRoute, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34bf0c8251244f50bde7c9d5fe60d88348a1be2cec9ac52b2fae8d7918d72b62(
    *,
    handler: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    route_key: builtins.str,
    route_response_selection_expression: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f2d26f324aac8877f83acfee58ebabf79ac8533e9ba6ca607e92e68086cc22(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    app_name: builtins.str,
    repository: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    basic_auth: typing.Optional[typing.Union[BasicAuthConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    branches: typing.Optional[typing.Sequence[typing.Union[BranchOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_settings: typing.Optional[typing.Union[BuildSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    custom_domain: typing.Optional[typing.Union[CustomDomainOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    custom_rules: typing.Optional[typing.Sequence[typing.Union[CustomRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c51143b7da8fc50ffd3240aae88642c332f9ccc1136e275abf9d1065df7ea17(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    api_name: builtins.str,
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    binary_media_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    create_usage_plan: typing.Optional[builtins.bool] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    custom_routes: typing.Optional[typing.Sequence[typing.Union[CustomRoute, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    existing_certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    lambda_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.LambdaRestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
    log_group_props: typing.Optional[typing.Union[_aws_cdk_aws_logs_ceddda9d.LogGroupProps, typing.Dict[builtins.str, typing.Any]]] = None,
    proxy: typing.Optional[builtins.bool] = None,
    rest_api_props: typing.Optional[typing.Union[_aws_cdk_aws_apigateway_ceddda9d.RestApiProps, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e35e3363ae35d50e0f0dd18a9ae11be6e9daf52ba8d2c783abfb12aff9b21376(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    additional_domain_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    cache_behaviors: typing.Optional[typing.Sequence[typing.Union[CacheBehaviorConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    certificate: typing.Optional[_aws_cdk_aws_certificatemanager_ceddda9d.ICertificate] = None,
    comment: typing.Optional[builtins.str] = None,
    create_route53_records: typing.Optional[builtins.bool] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    default_origin_id: typing.Optional[builtins.str] = None,
    default_root_object: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    enable_ipv6: typing.Optional[builtins.bool] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    error_pages: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_cloudfront_ceddda9d.ErrorResponse, typing.Dict[builtins.str, typing.Any]]]] = None,
    geo_restriction: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.GeoRestriction] = None,
    hosted_zone: typing.Optional[_aws_cdk_aws_route53_ceddda9d.IHostedZone] = None,
    http_origins: typing.Optional[typing.Sequence[typing.Union[HttpOriginConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    http_version: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.HttpVersion] = None,
    log_bucket: typing.Optional[_aws_cdk_aws_s3_ceddda9d.IBucket] = None,
    log_include_cookies: typing.Optional[builtins.bool] = None,
    log_prefix: typing.Optional[builtins.str] = None,
    price_class: typing.Optional[_aws_cdk_aws_cloudfront_ceddda9d.PriceClass] = None,
    s3_origins: typing.Optional[typing.Sequence[typing.Union[S3OriginConfig, typing.Dict[builtins.str, typing.Any]]]] = None,
    web_acl_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e1edfc306738ea99e0bd03a55876d7f75a063970dd3103fc1bbb766dff014b1(
    *,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
    containers: typing.Sequence[typing.Union[ContainerConfig, typing.Dict[builtins.str, typing.Any]]],
    security_groups: typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup],
    service_name: builtins.str,
    task_subnets: typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]],
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    code_deploy_application: typing.Optional[typing.Union[CodeDeployApplicationConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    deployment_group: typing.Optional[typing.Union[DeploymentGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer: typing.Optional[typing.Union[LoadBalancerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    load_balancer_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    production_listener: typing.Optional[typing.Union[ListenerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    production_target_group: typing.Optional[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    service: typing.Optional[typing.Union[ServiceConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    target_port: typing.Optional[jsii.Number] = None,
    task_definition: typing.Optional[typing.Union[TaskDefinitionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    test_listener: typing.Optional[typing.Union[ListenerConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    test_target_group: typing.Optional[typing.Union[TargetGroupConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
