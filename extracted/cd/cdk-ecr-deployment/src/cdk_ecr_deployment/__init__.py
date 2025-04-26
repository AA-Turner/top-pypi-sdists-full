r'''
# cdk-ecr-deployment

[![Release](https://github.com/cdklabs/cdk-ecr-deployment/actions/workflows/release.yml/badge.svg)](https://github.com/cdklabs/cdk-ecr-deployment/actions/workflows/release.yml)
[![npm version](https://img.shields.io/npm/v/cdk-ecr-deployment)](https://www.npmjs.com/package/cdk-ecr-deployment)
[![PyPI](https://img.shields.io/pypi/v/cdk-ecr-deployment)](https://pypi.org/project/cdk-ecr-deployment)
[![npm](https://img.shields.io/npm/dw/cdk-ecr-deployment?label=npm%20downloads)](https://www.npmjs.com/package/cdk-ecr-deployment)
[![PyPI - Downloads](https://img.shields.io/pypi/dw/cdk-ecr-deployment?label=pypi%20downloads)](https://pypi.org/project/cdk-ecr-deployment)

CDK construct to synchronize single docker image between docker registries.

> [!IMPORTANT]
>
> Please use the latest version of this package, which is `v4`.
>
> (Older versions are no longer supported).

## Features

* Copy image from ECR/external registry to (another) ECR/external registry
* Copy an archive tarball image from s3 to ECR/external registry

## Examples

```python
from aws_cdk.aws_ecr_assets import DockerImageAsset


image = DockerImageAsset(self, "CDKDockerImage",
    directory=path.join(__dirname, "docker")
)

# Copy from cdk docker image asset to another ECR.
ecrdeploy.ECRDeployment(self, "DeployDockerImage1",
    src=ecrdeploy.DockerImageName(image.image_uri),
    dest=ecrdeploy.DockerImageName(f"{cdk.Aws.ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/my-nginx:latest")
)

# Copy from docker registry to ECR.
ecrdeploy.ECRDeployment(self, "DeployDockerImage2",
    src=ecrdeploy.DockerImageName("nginx:latest"),
    dest=ecrdeploy.DockerImageName(f"{cdk.Aws.ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/my-nginx2:latest")
)

# Copy from private docker registry to ECR.
# The format of secret in aws secrets manager must be either:
# - plain text in format <username>:<password>
# - json in format {"username":"<username>","password":"<password>"}
ecrdeploy.ECRDeployment(self, "DeployDockerImage3",
    src=ecrdeploy.DockerImageName("javacs3/nginx:latest", "username:password"),
    # src: new ecrdeploy.DockerImageName('javacs3/nginx:latest', 'aws-secrets-manager-secret-name'),
    # src: new ecrdeploy.DockerImageName('javacs3/nginx:latest', 'arn:aws:secretsmanager:us-west-2:000000000000:secret:id'),
    dest=ecrdeploy.DockerImageName(f"{cdk.Aws.ACCOUNT_ID}.dkr.ecr.us-west-2.amazonaws.com/my-nginx3:latest")
).add_to_principal_policy(iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["secretsmanager:GetSecretValue"
    ],
    resources=["*"]
))
```

## Sample: [test/example.ecr-deployment.ts](./test/example.ecr-deployment.ts)

After cloning the repository, install dependencies and run a full build:

```console
yarn --frozen-lockfile --check-files
yarn build
```

Then run the example like this:

```shell
# Run the following command to try the sample.
npx cdk deploy -a "npx ts-node -P tsconfig.dev.json --prefer-ts-exts test/example.ecr-deployment.ts"
```

To run the DockerHub example you will first need to setup a Secret in AWS Secrets Manager to provide DockerHub credentials.
Replace `username:access-token` with your credentials.
**Please note that Secrets will occur a cost.**

```console
aws secretsmanager create-secret --name DockerHubCredentials --secret-string "username:access-token"
```

From the output, copy the ARN of your new secret and export it as env variable

```console
export DOCKERHUB_SECRET_ARN="<ARN>"
```

Finally run:

```shell
# Run the following command to try the sample.
npx cdk deploy -a "npx ts-node -P tsconfig.dev.json --prefer-ts-exts test/dockerhub-example.ecr-deployment.ts"
```

If your Secret is encrypted, you might have to adjust the example to also grant decrypt permissions.

## [API](./API.md)

## Tech Details & Contribution

The core of this project relies on [containers/image](https://github.com/containers/image) which is used by [Skopeo](https://github.com/containers/skopeo).
Please take a look at those projects before contribution.

To support a new docker image source(like docker tarball in s3), you need to implement [image transport interface](https://github.com/containers/image/blob/master/types/types.go). You could take a look at [docker-archive](https://github.com/containers/image/blob/ccb87a8d0f45cf28846e307eb0ec2b9d38a458c2/docker/archive/transport.go) transport for a good start.

Any error in the custom resource provider will show up in the CloudFormation error log as `Invalid PhysicalResourceId`, because of this: [https://github.com/aws/aws-lambda-go/issues/107](https://github.com/aws/aws-lambda-go/issues/107). You need to go into the CloudWatch Log Group to find the real error.
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


class ECRDeployment(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ecr-deployment.ECRDeployment",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dest: "IImageName",
        src: "IImageName",
        image_arch: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dest: The destination of the docker image.
        :param src: The source of the docker image.
        :param image_arch: The image architecture to be copied. The 'amd64' architecture will be copied by default. Specify the architecture or architectures to copy here. It is currently not possible to copy more than one architecture at a time: the array you specify must contain exactly one string. Default: ['amd64']
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: - 512
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param vpc: The VPC network to place the deployment lambda handler in. Default: - None
        :param vpc_subnets: Where in the VPC to place the deployment lambda handler. Only used if 'vpc' is supplied. Default: - the Vpc default strategy if not specified
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d24bf38ee05e035f6d77ace8eb6a8a39c5a3ef61dbe1a8d4758949a3710c9f8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ECRDeploymentProps(
            dest=dest,
            src=src,
            image_arch=image_arch,
            memory_limit=memory_limit,
            role=role,
            security_groups=security_groups,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
    ) -> _aws_cdk_aws_iam_ceddda9d.AddToPrincipalPolicyResult:
        '''
        :param statement: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325690cb0a83adf6fab8d9967af566ee5c34ec280a23ccfb834cfb92b2023e9c)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))


@jsii.data_type(
    jsii_type="cdk-ecr-deployment.ECRDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "dest": "dest",
        "src": "src",
        "image_arch": "imageArch",
        "memory_limit": "memoryLimit",
        "role": "role",
        "security_groups": "securityGroups",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class ECRDeploymentProps:
    def __init__(
        self,
        *,
        dest: "IImageName",
        src: "IImageName",
        image_arch: typing.Optional[typing.Sequence[builtins.str]] = None,
        memory_limit: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param dest: The destination of the docker image.
        :param src: The source of the docker image.
        :param image_arch: The image architecture to be copied. The 'amd64' architecture will be copied by default. Specify the architecture or architectures to copy here. It is currently not possible to copy more than one architecture at a time: the array you specify must contain exactly one string. Default: ['amd64']
        :param memory_limit: The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket. If you are deploying large files, you will need to increase this number accordingly. Default: - 512
        :param role: Execution role associated with this function. Default: - A role is automatically created
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param vpc: The VPC network to place the deployment lambda handler in. Default: - None
        :param vpc_subnets: Where in the VPC to place the deployment lambda handler. Only used if 'vpc' is supplied. Default: - the Vpc default strategy if not specified
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36cce9ade11503a84b3a05f93d6aeb623f18eb537004fb3c37776c491a77f224)
            check_type(argname="argument dest", value=dest, expected_type=type_hints["dest"])
            check_type(argname="argument src", value=src, expected_type=type_hints["src"])
            check_type(argname="argument image_arch", value=image_arch, expected_type=type_hints["image_arch"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dest": dest,
            "src": src,
        }
        if image_arch is not None:
            self._values["image_arch"] = image_arch
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def dest(self) -> "IImageName":
        '''The destination of the docker image.'''
        result = self._values.get("dest")
        assert result is not None, "Required property 'dest' is missing"
        return typing.cast("IImageName", result)

    @builtins.property
    def src(self) -> "IImageName":
        '''The source of the docker image.'''
        result = self._values.get("src")
        assert result is not None, "Required property 'src' is missing"
        return typing.cast("IImageName", result)

    @builtins.property
    def image_arch(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The image architecture to be copied.

        The 'amd64' architecture will be copied by default. Specify the
        architecture or architectures to copy here.

        It is currently not possible to copy more than one architecture
        at a time: the array you specify must contain exactly one string.

        :default: ['amd64']
        '''
        result = self._values.get("image_arch")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory (in MiB) to allocate to the AWS Lambda function which replicates the files from the CDK bucket to the destination bucket.

        If you are deploying large files, you will need to increase this number
        accordingly.

        :default: - 512
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''Execution role associated with this function.

        :default: - A role is automatically created
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]]:
        '''The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''The VPC network to place the deployment lambda handler in.

        :default: - None
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''Where in the VPC to place the deployment lambda handler.

        Only used if 'vpc' is supplied.

        :default: - the Vpc default strategy if not specified
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECRDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-ecr-deployment.IImageName")
class IImageName(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        '''The uri of the docker image.

        The uri spec follows https://github.com/containers/skopeo
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="creds")
    def creds(self) -> typing.Optional[builtins.str]:
        '''The credentials of the docker image.

        Format ``user:password`` or ``AWS Secrets Manager secret arn`` or ``AWS Secrets Manager secret name``.

        If specifying an AWS Secrets Manager secret, the format of the secret should be either plain text (``user:password``) or
        JSON (``{"username":"<username>","password":"<password>"}``).

        For more details on JSON format, see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
        '''
        ...

    @creds.setter
    def creds(self, value: typing.Optional[builtins.str]) -> None:
        ...


class _IImageNameProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-ecr-deployment.IImageName"

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        '''The uri of the docker image.

        The uri spec follows https://github.com/containers/skopeo
        '''
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="creds")
    def creds(self) -> typing.Optional[builtins.str]:
        '''The credentials of the docker image.

        Format ``user:password`` or ``AWS Secrets Manager secret arn`` or ``AWS Secrets Manager secret name``.

        If specifying an AWS Secrets Manager secret, the format of the secret should be either plain text (``user:password``) or
        JSON (``{"username":"<username>","password":"<password>"}``).

        For more details on JSON format, see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creds"))

    @creds.setter
    def creds(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81ae2679d7471479e5816734a1164966670a97a769e663d3dba0018a25318b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creds", value) # pyright: ignore[reportArgumentType]

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IImageName).__jsii_proxy_class__ = lambda : _IImageNameProxy


@jsii.implements(IImageName)
class S3ArchiveName(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ecr-deployment.S3ArchiveName",
):
    def __init__(
        self,
        p: builtins.str,
        ref: typing.Optional[builtins.str] = None,
        creds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param p: - the S3 bucket name and path of the archive (a S3 URI without the s3://).
        :param ref: - appended to the end of the name with a ``:``, e.g. ``:latest``.
        :param creds: - The credentials of the docker image. Format ``user:password`` or ``AWS Secrets Manager secret arn`` or ``AWS Secrets Manager secret name``. If specifying an AWS Secrets Manager secret, the format of the secret should be either plain text (``user:password``) or JSON (``{"username":"<username>","password":"<password>"}``). For more details on JSON format, see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d0c83474fcf1d53ec37992ef6e48d3662feb17e26f3db1dc7656e18db0174f)
            check_type(argname="argument p", value=p, expected_type=type_hints["p"])
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
            check_type(argname="argument creds", value=creds, expected_type=type_hints["creds"])
        jsii.create(self.__class__, self, [p, ref, creds])

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        '''The uri of the docker image.

        The uri spec follows https://github.com/containers/skopeo
        '''
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="creds")
    def creds(self) -> typing.Optional[builtins.str]:
        '''- The credentials of the docker image.

        Format ``user:password`` or ``AWS Secrets Manager secret arn`` or ``AWS Secrets Manager secret name``.
        If specifying an AWS Secrets Manager secret, the format of the secret should be either plain text (``user:password``) or
        JSON (``{"username":"<username>","password":"<password>"}``).
        For more details on JSON format, see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creds"))

    @creds.setter
    def creds(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__688773b22e812b1f885bcb3c6db14df681ea8a4de7c61c9c548cc3b5251b4a09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creds", value) # pyright: ignore[reportArgumentType]


@jsii.implements(IImageName)
class DockerImageName(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-ecr-deployment.DockerImageName",
):
    def __init__(
        self,
        name: builtins.str,
        creds: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: - The name of the image, e.g. retrieved from ``DockerImageAsset.imageUri``.
        :param creds: - The credentials of the docker image. Format ``user:password`` or ``AWS Secrets Manager secret arn`` or ``AWS Secrets Manager secret name``. If specifying an AWS Secrets Manager secret, the format of the secret should be either plain text (``user:password``) or JSON (``{"username":"<username>","password":"<password>"}``). For more details on JSON format, see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb797245c2bef1d3b45b384edb79598f7dd44ad79e3cd42f8935d22e169e449)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument creds", value=creds, expected_type=type_hints["creds"])
        jsii.create(self.__class__, self, [name, creds])

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        '''The uri of the docker image.

        The uri spec follows https://github.com/containers/skopeo
        '''
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @builtins.property
    @jsii.member(jsii_name="creds")
    def creds(self) -> typing.Optional[builtins.str]:
        '''- The credentials of the docker image.

        Format ``user:password`` or ``AWS Secrets Manager secret arn`` or ``AWS Secrets Manager secret name``.
        If specifying an AWS Secrets Manager secret, the format of the secret should be either plain text (``user:password``) or
        JSON (``{"username":"<username>","password":"<password>"}``).
        For more details on JSON format, see https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "creds"))

    @creds.setter
    def creds(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72af2920d9000bc2347ecd474276dc87af6bbfa4c1a44723c544387087315a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "creds", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DockerImageName",
    "ECRDeployment",
    "ECRDeploymentProps",
    "IImageName",
    "S3ArchiveName",
]

publication.publish()

def _typecheckingstub__d24bf38ee05e035f6d77ace8eb6a8a39c5a3ef61dbe1a8d4758949a3710c9f8d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dest: IImageName,
    src: IImageName,
    image_arch: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325690cb0a83adf6fab8d9967af566ee5c34ec280a23ccfb834cfb92b2023e9c(
    statement: _aws_cdk_aws_iam_ceddda9d.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36cce9ade11503a84b3a05f93d6aeb623f18eb537004fb3c37776c491a77f224(
    *,
    dest: IImageName,
    src: IImageName,
    image_arch: typing.Optional[typing.Sequence[builtins.str]] = None,
    memory_limit: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.SecurityGroup]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81ae2679d7471479e5816734a1164966670a97a769e663d3dba0018a25318b1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d0c83474fcf1d53ec37992ef6e48d3662feb17e26f3db1dc7656e18db0174f(
    p: builtins.str,
    ref: typing.Optional[builtins.str] = None,
    creds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__688773b22e812b1f885bcb3c6db14df681ea8a4de7c61c9c548cc3b5251b4a09(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb797245c2bef1d3b45b384edb79598f7dd44ad79e3cd42f8935d22e169e449(
    name: builtins.str,
    creds: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72af2920d9000bc2347ecd474276dc87af6bbfa4c1a44723c544387087315a29(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass
