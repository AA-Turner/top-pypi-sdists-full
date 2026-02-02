r'''
# AWS Cloud9 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

AWS Cloud9 is a cloud-based integrated development environment (IDE) that lets you write, run, and debug your code with just a
browser. It includes a code editor, debugger, and terminal. Cloud9 comes prepackaged with essential tools for popular
programming languages, including JavaScript, Python, PHP, and more, so you don’t need to install files or configure your
development machine to start new projects. Since your Cloud9 IDE is cloud-based, you can work on your projects from your
office, home, or anywhere using an internet-connected machine. Cloud9 also provides a seamless experience for developing
serverless applications enabling you to easily define resources, debug, and switch between local and remote execution of
serverless applications. With Cloud9, you can quickly share your development environment with your team, enabling you to pair
program and track each other's inputs in real time.

## Creating EC2 Environment

EC2 Environments are defined with `Ec2Environment`. To create an EC2 environment in the private subnet, specify
`subnetSelection` with private `subnetType`.

```python
# create a cloud9 ec2 environment in a new VPC
vpc = ec2.Vpc(self, "VPC", max_azs=3)
cloud9.Ec2Environment(self, "Cloud9Env", vpc=vpc, image_id=cloud9.ImageId.AMAZON_LINUX_2)

# or create the cloud9 environment in the default VPC with specific instanceType
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    instance_type=ec2.InstanceType("t3.large"),
    image_id=cloud9.ImageId.AMAZON_LINUX_2
)

# or specify in a different subnetSelection
c9env = cloud9.Ec2Environment(self, "Cloud9Env3",
    vpc=vpc,
    subnet_selection=ec2.SubnetSelection(
        subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS
    ),
    image_id=cloud9.ImageId.AMAZON_LINUX_2
)

# print the Cloud9 IDE URL in the output
CfnOutput(self, "URL", value=c9env.ide_url)
```

## Specifying EC2 AMI

Use `imageId` to specify the EC2 AMI image to be used:

```python
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    instance_type=ec2.InstanceType("t3.large"),
    image_id=cloud9.ImageId.UBUNTU_18_04
)
```

## Cloning Repositories

Use `clonedRepositories` to clone one or multiple AWS Codecommit repositories into the environment:

```python
import aws_cdk.aws_codecommit as codecommit

# create a new Cloud9 environment and clone the two repositories
# vpc: ec2.Vpc


# create a codecommit repository to clone into the cloud9 environment
repo_new = codecommit.Repository(self, "RepoNew",
    repository_name="new-repo"
)

# import an existing codecommit repository to clone into the cloud9 environment
repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
cloud9.Ec2Environment(self, "C9Env",
    vpc=vpc,
    cloned_repositories=[
        cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
        cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
    ],
    image_id=cloud9.ImageId.AMAZON_LINUX_2
)
```

## Specifying Owners

Every Cloud9 Environment has an **owner**. An owner has full control over the environment, and can invite additional members to the environment for collaboration purposes. For more information, see [Working with shared environments in AWS Cloud9](https://docs.aws.amazon.com/cloud9/latest/user-guide/share-environment.html)).

By default, the owner will be the identity that creates the Environment, which is most likely your CloudFormation Execution Role when the Environment is created using CloudFormation. Provider a value for the `owner` property to assign a different owner, either a specific IAM User or the AWS Account Root User.

`Owner` is an IAM entity that owns a Cloud9 environment. `Owner` has their own access permissions, and resources. You can specify an `Owner`in an EC2 environment which could be of the following types:

1. Account Root
2. IAM User
3. IAM Federated User
4. IAM Assumed Role

The ARN of the owner must satisfy the following regular expression: `^arn:(aws|aws-cn|aws-us-gov|aws-iso|aws-iso-b):(iam|sts)::\d+:(root|(user\/[\w+=/:,.@-]{1,64}|federated-user\/[\w+=/:,.@-]{2,32}|assumed-role\/[\w+=:,.@-]{1,64}\/[\w+=,.@-]{1,64}))$`

Note: Using the account root user is not recommended, see [environment sharing best practices](https://docs.aws.amazon.com/cloud9/latest/user-guide/share-environment.html#share-environment-best-practices).

To specify the AWS Account Root User as the environment owner, use `Owner.accountRoot()`

```python
# vpc: ec2.Vpc

cloud9.Ec2Environment(self, "C9Env",
    vpc=vpc,
    image_id=cloud9.ImageId.AMAZON_LINUX_2,
    owner=cloud9.Owner.account_root("111111111")
)
```

To specify a specific IAM User as the environment owner, use `Owner.user()`. The user should have the `AWSCloud9Administrator` managed policy

The user should have the `AWSCloud9User` (preferred) or `AWSCloud9Administrator` managed policy attached.

```python
import aws_cdk.aws_iam as iam
# vpc: ec2.Vpc


user = iam.User(self, "user")
user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9Administrator"))
cloud9.Ec2Environment(self, "C9Env",
    vpc=vpc,
    image_id=cloud9.ImageId.AMAZON_LINUX_2,

    owner=cloud9.Owner.user(user)
)
```

To specify a specific IAM Federated User as the environment owner, use `Owner.federatedUser(accountId, userName)`.

The user should have the `AWSCloud9User` (preferred) or `AWSCloud9Administrator` managed policy attached.

```python
import aws_cdk.aws_iam as iam

# vpc: ec2.Vpc

cloud9.Ec2Environment(self, "C9Env",
    vpc=vpc,
    image_id=cloud9.ImageId.AMAZON_LINUX_2,
    owner=cloud9.Owner.federated_user(Stack.of(self).account, "Admin/johndoe")
)
```

To specify an IAM Assumed Role as the environment owner, use `Owner.assumedRole(accountId: string, roleName: string)`.

The role should have the `AWSCloud9User` (preferred) or `AWSCloud9Administrator` managed policy attached.

```python
import aws_cdk.aws_iam as iam

# vpc: ec2.Vpc

cloud9.Ec2Environment(self, "C9Env",
    vpc=vpc,
    image_id=cloud9.ImageId.AMAZON_LINUX_2,
    owner=cloud9.Owner.assumed_role(Stack.of(self).account, "Admin/johndoe-role")
)
```

## Auto-Hibernation

A Cloud9 environment can automatically start and stop the associated EC2 instance to reduce costs.

Use `automaticStop` to specify the number of minutes until the running instance is shut down after the environment was last used.

```python
default_vpc = ec2.Vpc.from_lookup(self, "DefaultVPC", is_default=True)
cloud9.Ec2Environment(self, "Cloud9Env2",
    vpc=default_vpc,
    image_id=cloud9.ImageId.AMAZON_LINUX_2,
    automatic_stop=Duration.minutes(30)
)
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
import aws_cdk.aws_codecommit as _aws_cdk_aws_codecommit_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


class CloneRepository(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9-alpha.CloneRepository",
):
    '''(experimental) The class for different repository providers.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codecommit as codecommit
        
        # create a new Cloud9 environment and clone the two repositories
        # vpc: ec2.Vpc
        
        
        # create a codecommit repository to clone into the cloud9 environment
        repo_new = codecommit.Repository(self, "RepoNew",
            repository_name="new-repo"
        )
        
        # import an existing codecommit repository to clone into the cloud9 environment
        repo_existing = codecommit.Repository.from_repository_name(self, "RepoExisting", "existing-repo")
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            cloned_repositories=[
                cloud9.CloneRepository.from_code_commit(repo_new, "/src/new-repo"),
                cloud9.CloneRepository.from_code_commit(repo_existing, "/src/existing-repo")
            ],
            image_id=cloud9.ImageId.AMAZON_LINUX_2
        )
    '''

    @jsii.member(jsii_name="fromCodeCommit")
    @builtins.classmethod
    def from_code_commit(
        cls,
        repository: "_aws_cdk_aws_codecommit_ceddda9d.IRepository",
        path: builtins.str,
    ) -> "CloneRepository":
        '''(experimental) import repository to cloud9 environment from AWS CodeCommit.

        :param repository: the codecommit repository to clone from.
        :param path: the target path in cloud9 environment.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5715f24eed483fb786c815cf1538129556b87955db8377dbc98f7d312db74b8e)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("CloneRepository", jsii.sinvoke(cls, "fromCodeCommit", [repository, path]))

    @builtins.property
    @jsii.member(jsii_name="pathComponent")
    def path_component(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "pathComponent"))

    @builtins.property
    @jsii.member(jsii_name="repositoryUrl")
    def repository_url(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "repositoryUrl"))


@jsii.enum(jsii_type="@aws-cdk/aws-cloud9-alpha.ConnectionType")
class ConnectionType(enum.Enum):
    '''(experimental) The connection type used for connecting to an Amazon EC2 environment.

    :stability: experimental
    '''

    CONNECT_SSH = "CONNECT_SSH"
    '''(experimental) Connect through SSH.

    :stability: experimental
    '''
    CONNECT_SSM = "CONNECT_SSM"
    '''(experimental) Connect through AWS Systems Manager When using SSM, service role and instance profile aren't automatically created.

    See https://docs.aws.amazon.com/cloud9/latest/user-guide/ec2-ssm.html#service-role-ssm

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-cloud9-alpha.Ec2EnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "image_id": "imageId",
        "vpc": "vpc",
        "automatic_stop": "automaticStop",
        "cloned_repositories": "clonedRepositories",
        "connection_type": "connectionType",
        "description": "description",
        "ec2_environment_name": "ec2EnvironmentName",
        "instance_type": "instanceType",
        "owner": "owner",
        "subnet_selection": "subnetSelection",
    },
)
class Ec2EnvironmentProps:
    def __init__(
        self,
        *,
        image_id: "ImageId",
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        automatic_stop: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        cloned_repositories: typing.Optional[typing.Sequence["CloneRepository"]] = None,
        connection_type: typing.Optional["ConnectionType"] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_environment_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        owner: typing.Optional["Owner"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for Ec2Environment.

        :param image_id: (experimental) The image ID used for creating an Amazon EC2 environment.
        :param vpc: (experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param automatic_stop: (experimental) The number of minutes until the running instance is shut down after the environment was last used. Setting a value of 0 means the instance will never be automatically shut down." Default: - The instance will not be shut down automatically.
        :param cloned_repositories: (experimental) The AWS CodeCommit repository to be cloned. Default: - do not clone any repository
        :param connection_type: (experimental) The connection type used for connecting to an Amazon EC2 environment. Valid values are: CONNECT_SSH (default) and CONNECT_SSM (connected through AWS Systems Manager) Default: - CONNECT_SSH
        :param description: (experimental) Description of the environment. Default: - no description
        :param ec2_environment_name: (experimental) Name of the environment. Default: - automatically generated name
        :param instance_type: (experimental) The type of instance to connect to the environment. Default: - t2.micro
        :param owner: (experimental) Owner of the environment. The owner has full control of the environment and can invite additional members. Default: - The identity that CloudFormation executes under will be the owner
        :param subnet_selection: (experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance. Default: - all public subnets of the VPC are selected.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iam as iam
            # vpc: ec2.Vpc
            
            
            user = iam.User(self, "user")
            user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9Administrator"))
            cloud9.Ec2Environment(self, "C9Env",
                vpc=vpc,
                image_id=cloud9.ImageId.AMAZON_LINUX_2,
            
                owner=cloud9.Owner.user(user)
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b532dbafc2fd7c4838c0d7dd941df44770ef42cfe6c754418d3d7fb3a4f9c36)
            check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument automatic_stop", value=automatic_stop, expected_type=type_hints["automatic_stop"])
            check_type(argname="argument cloned_repositories", value=cloned_repositories, expected_type=type_hints["cloned_repositories"])
            check_type(argname="argument connection_type", value=connection_type, expected_type=type_hints["connection_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_environment_name", value=ec2_environment_name, expected_type=type_hints["ec2_environment_name"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_id": image_id,
            "vpc": vpc,
        }
        if automatic_stop is not None:
            self._values["automatic_stop"] = automatic_stop
        if cloned_repositories is not None:
            self._values["cloned_repositories"] = cloned_repositories
        if connection_type is not None:
            self._values["connection_type"] = connection_type
        if description is not None:
            self._values["description"] = description
        if ec2_environment_name is not None:
            self._values["ec2_environment_name"] = ec2_environment_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if owner is not None:
            self._values["owner"] = owner
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection

    @builtins.property
    def image_id(self) -> "ImageId":
        '''(experimental) The image ID used for creating an Amazon EC2 environment.

        :stability: experimental
        '''
        result = self._values.get("image_id")
        assert result is not None, "Required property 'image_id' is missing"
        return typing.cast("ImageId", result)

    @builtins.property
    def vpc(self) -> "_aws_cdk_aws_ec2_ceddda9d.IVpc":
        '''(experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IVpc", result)

    @builtins.property
    def automatic_stop(self) -> typing.Optional["_aws_cdk_ceddda9d.Duration"]:
        '''(experimental) The number of minutes until the running instance is shut down after the environment was last used.

        Setting a value of 0 means the instance will never be automatically shut down."

        :default: - The instance will not be shut down automatically.

        :stability: experimental
        '''
        result = self._values.get("automatic_stop")
        return typing.cast(typing.Optional["_aws_cdk_ceddda9d.Duration"], result)

    @builtins.property
    def cloned_repositories(self) -> typing.Optional[typing.List["CloneRepository"]]:
        '''(experimental) The AWS CodeCommit repository to be cloned.

        :default: - do not clone any repository

        :stability: experimental
        '''
        result = self._values.get("cloned_repositories")
        return typing.cast(typing.Optional[typing.List["CloneRepository"]], result)

    @builtins.property
    def connection_type(self) -> typing.Optional["ConnectionType"]:
        '''(experimental) The connection type used for connecting to an Amazon EC2 environment.

        Valid values are: CONNECT_SSH (default) and CONNECT_SSM (connected through AWS Systems Manager)

        :default: - CONNECT_SSH

        :stability: experimental
        '''
        result = self._values.get("connection_type")
        return typing.cast(typing.Optional["ConnectionType"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Description of the environment.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the environment.

        :default: - automatically generated name

        :stability: experimental
        '''
        result = self._values.get("ec2_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_type(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"]:
        '''(experimental) The type of instance to connect to the environment.

        :default: - t2.micro

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"], result)

    @builtins.property
    def owner(self) -> typing.Optional["Owner"]:
        '''(experimental) Owner of the environment.

        The owner has full control of the environment and can invite additional members.

        :default: - The identity that CloudFormation executes under will be the owner

        :stability: experimental
        '''
        result = self._values.get("owner")
        return typing.cast(typing.Optional["Owner"], result)

    @builtins.property
    def subnet_selection(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"]:
        '''(experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance.

        :default: - all public subnets of the VPC are selected.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2EnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-cloud9-alpha.IEc2Environment")
class IEc2Environment(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) A Cloud9 Environment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentArn")
    def ec2_environment_arn(self) -> builtins.str:
        '''(experimental) The arn of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentE2Arn
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentName")
    def ec2_environment_name(self) -> builtins.str:
        '''(experimental) The name of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentEc2Name
        '''
        ...


class _IEc2EnvironmentProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) A Cloud9 Environment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-cloud9-alpha.IEc2Environment"

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentArn")
    def ec2_environment_arn(self) -> builtins.str:
        '''(experimental) The arn of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentE2Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentName")
    def ec2_environment_name(self) -> builtins.str:
        '''(experimental) The name of the EnvironmentEc2.

        :stability: experimental
        :attribute: environmentEc2Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEc2Environment).__jsii_proxy_class__ = lambda : _IEc2EnvironmentProxy


@jsii.enum(jsii_type="@aws-cdk/aws-cloud9-alpha.ImageId")
class ImageId(enum.Enum):
    '''(experimental) The image ID used for creating an Amazon EC2 environment.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iam as iam
        # vpc: ec2.Vpc
        
        
        user = iam.User(self, "user")
        user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9Administrator"))
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            image_id=cloud9.ImageId.AMAZON_LINUX_2,
        
            owner=cloud9.Owner.user(user)
        )
    '''

    AMAZON_LINUX_2 = "AMAZON_LINUX_2"
    '''(experimental) Create using Amazon Linux 2.

    :stability: experimental
    '''
    AMAZON_LINUX_2023 = "AMAZON_LINUX_2023"
    '''(experimental) Create using Amazon Linux 2023.

    :stability: experimental
    '''
    UBUNTU_18_04 = "UBUNTU_18_04"
    '''(deprecated) Create using Ubuntu 18.04.

    :deprecated: Since Ubuntu 18.04 has ended standard support as of May 31, 2023, we recommend you choose Ubuntu 22.04.

    :stability: deprecated
    '''
    UBUNTU_22_04 = "UBUNTU_22_04"
    '''(experimental) Create using Ubuntu 22.04.

    :stability: experimental
    '''


class Owner(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloud9-alpha.Owner"):
    '''(experimental) An environment owner.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iam as iam
        
        # vpc: ec2.Vpc
        
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            image_id=cloud9.ImageId.AMAZON_LINUX_2,
            owner=cloud9.Owner.federated_user(Stack.of(self).account, "Admin/johndoe")
        )
    '''

    @jsii.member(jsii_name="accountRoot")
    @builtins.classmethod
    def account_root(cls, account_id: builtins.str) -> "Owner":
        '''(experimental) Make the Account Root User the environment owner (not recommended).

        :param account_id: the AccountId to use as the environment owner.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d1eab4a881f1a2118cf896be3c95fb9c110cb70d2d65dd7d8d1a5f1dcdf9b5)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast("Owner", jsii.sinvoke(cls, "accountRoot", [account_id]))

    @jsii.member(jsii_name="assumedRole")
    @builtins.classmethod
    def assumed_role(cls, account_id: builtins.str, role_name: builtins.str) -> "Owner":
        '''(experimental) Make an IAM assumed role the environment owner.

        :param account_id: The account id of the target account.
        :param role_name: The name of the assumed role.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__665b285f64bc14dedbde9ef49982b5abb375c42bac120eb1663db792a3d4085d)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        return typing.cast("Owner", jsii.sinvoke(cls, "assumedRole", [account_id, role_name]))

    @jsii.member(jsii_name="federatedUser")
    @builtins.classmethod
    def federated_user(
        cls,
        account_id: builtins.str,
        user_name: builtins.str,
    ) -> "Owner":
        '''(experimental) Make an IAM federated user the environment owner.

        :param account_id: The AccountId of the target account.
        :param user_name: The name of the federated user.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08a6a8c14e203af7186d0bc0315a85714c6e312b13d78a96605f8735c1264bb0)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        return typing.cast("Owner", jsii.sinvoke(cls, "federatedUser", [account_id, user_name]))

    @jsii.member(jsii_name="user")
    @builtins.classmethod
    def user(cls, user: "_aws_cdk_aws_iam_ceddda9d.IUser") -> "Owner":
        '''(experimental) Make an IAM user the environment owner.

        User need to have AWSCloud9Administrator permissions

        :param user: the User object to use as the environment owner.

        :see: https://docs.aws.amazon.com/cloud9/latest/user-guide/share-environment.html#share-environment-about
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf11b6609024597957d1a625237cdf5b0c0dba8d7e8e633393926e6dcdaed63d)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast("Owner", jsii.sinvoke(cls, "user", [user]))

    @builtins.property
    @jsii.member(jsii_name="ownerArn")
    def owner_arn(self) -> builtins.str:
        '''(experimental) of environment owner.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ownerArn"))


@jsii.implements(IEc2Environment)
class Ec2Environment(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-cloud9-alpha.Ec2Environment",
):
    '''(experimental) A Cloud9 Environment with Amazon EC2.

    :stability: experimental
    :resource: AWS::Cloud9::EnvironmentEC2
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iam as iam
        # vpc: ec2.Vpc
        
        
        user = iam.User(self, "user")
        user.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AWSCloud9Administrator"))
        cloud9.Ec2Environment(self, "C9Env",
            vpc=vpc,
            image_id=cloud9.ImageId.AMAZON_LINUX_2,
        
            owner=cloud9.Owner.user(user)
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        image_id: "ImageId",
        vpc: "_aws_cdk_aws_ec2_ceddda9d.IVpc",
        automatic_stop: typing.Optional["_aws_cdk_ceddda9d.Duration"] = None,
        cloned_repositories: typing.Optional[typing.Sequence["CloneRepository"]] = None,
        connection_type: typing.Optional["ConnectionType"] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_environment_name: typing.Optional[builtins.str] = None,
        instance_type: typing.Optional["_aws_cdk_aws_ec2_ceddda9d.InstanceType"] = None,
        owner: typing.Optional["Owner"] = None,
        subnet_selection: typing.Optional[typing.Union["_aws_cdk_aws_ec2_ceddda9d.SubnetSelection", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image_id: (experimental) The image ID used for creating an Amazon EC2 environment.
        :param vpc: (experimental) The VPC that AWS Cloud9 will use to communicate with the Amazon Elastic Compute Cloud (Amazon EC2) instance.
        :param automatic_stop: (experimental) The number of minutes until the running instance is shut down after the environment was last used. Setting a value of 0 means the instance will never be automatically shut down." Default: - The instance will not be shut down automatically.
        :param cloned_repositories: (experimental) The AWS CodeCommit repository to be cloned. Default: - do not clone any repository
        :param connection_type: (experimental) The connection type used for connecting to an Amazon EC2 environment. Valid values are: CONNECT_SSH (default) and CONNECT_SSM (connected through AWS Systems Manager) Default: - CONNECT_SSH
        :param description: (experimental) Description of the environment. Default: - no description
        :param ec2_environment_name: (experimental) Name of the environment. Default: - automatically generated name
        :param instance_type: (experimental) The type of instance to connect to the environment. Default: - t2.micro
        :param owner: (experimental) Owner of the environment. The owner has full control of the environment and can invite additional members. Default: - The identity that CloudFormation executes under will be the owner
        :param subnet_selection: (experimental) The subnetSelection of the VPC that AWS Cloud9 will use to communicate with the Amazon EC2 instance. Default: - all public subnets of the VPC are selected.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccb4415ff26f23d4bbd47eed0eaf906e2fa0f0c270d17e7a8ba45aac4875bc3a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = Ec2EnvironmentProps(
            image_id=image_id,
            vpc=vpc,
            automatic_stop=automatic_stop,
            cloned_repositories=cloned_repositories,
            connection_type=connection_type,
            description=description,
            ec2_environment_name=ec2_environment_name,
            instance_type=instance_type,
            owner=owner,
            subnet_selection=subnet_selection,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEc2EnvironmentName")
    @builtins.classmethod
    def from_ec2_environment_name(
        cls,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        ec2_environment_name: builtins.str,
    ) -> "IEc2Environment":
        '''(experimental) import from EnvironmentEc2Name.

        :param scope: -
        :param id: -
        :param ec2_environment_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d751637c6d8a0fabae0fc9fff5d25771870587a93f9436dae131c0b5f45da4a5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ec2_environment_name", value=ec2_environment_name, expected_type=type_hints["ec2_environment_name"])
        return typing.cast("IEc2Environment", jsii.sinvoke(cls, "fromEc2EnvironmentName", [scope, id, ec2_environment_name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PROPERTY_INJECTION_ID")
    def PROPERTY_INJECTION_ID(cls) -> builtins.str:
        '''(experimental) Uniquely identifies this class.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PROPERTY_INJECTION_ID"))

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentArn")
    def ec2_environment_arn(self) -> builtins.str:
        '''(experimental) The environment ARN of this Cloud9 environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="ec2EnvironmentName")
    def ec2_environment_name(self) -> builtins.str:
        '''(experimental) The environment name of this Cloud9 environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2EnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''(experimental) The environment ID of this Cloud9 environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @builtins.property
    @jsii.member(jsii_name="ideUrl")
    def ide_url(self) -> builtins.str:
        '''(experimental) The complete IDE URL of this Cloud9 environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "ideUrl"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> "_aws_cdk_aws_ec2_ceddda9d.IVpc":
        '''(experimental) VPC ID.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ec2_ceddda9d.IVpc", jsii.get(self, "vpc"))


__all__ = [
    "CloneRepository",
    "ConnectionType",
    "Ec2Environment",
    "Ec2EnvironmentProps",
    "IEc2Environment",
    "ImageId",
    "Owner",
]

publication.publish()

def _typecheckingstub__5715f24eed483fb786c815cf1538129556b87955db8377dbc98f7d312db74b8e(
    repository: _aws_cdk_aws_codecommit_ceddda9d.IRepository,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b532dbafc2fd7c4838c0d7dd941df44770ef42cfe6c754418d3d7fb3a4f9c36(
    *,
    image_id: ImageId,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    automatic_stop: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
    connection_type: typing.Optional[ConnectionType] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_environment_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    owner: typing.Optional[Owner] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d1eab4a881f1a2118cf896be3c95fb9c110cb70d2d65dd7d8d1a5f1dcdf9b5(
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__665b285f64bc14dedbde9ef49982b5abb375c42bac120eb1663db792a3d4085d(
    account_id: builtins.str,
    role_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08a6a8c14e203af7186d0bc0315a85714c6e312b13d78a96605f8735c1264bb0(
    account_id: builtins.str,
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf11b6609024597957d1a625237cdf5b0c0dba8d7e8e633393926e6dcdaed63d(
    user: _aws_cdk_aws_iam_ceddda9d.IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccb4415ff26f23d4bbd47eed0eaf906e2fa0f0c270d17e7a8ba45aac4875bc3a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image_id: ImageId,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    automatic_stop: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    cloned_repositories: typing.Optional[typing.Sequence[CloneRepository]] = None,
    connection_type: typing.Optional[ConnectionType] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_environment_name: typing.Optional[builtins.str] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.InstanceType] = None,
    owner: typing.Optional[Owner] = None,
    subnet_selection: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d751637c6d8a0fabae0fc9fff5d25771870587a93f9436dae131c0b5f45da4a5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    ec2_environment_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IEc2Environment]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
