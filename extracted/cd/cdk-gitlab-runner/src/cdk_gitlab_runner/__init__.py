r'''
[![NPM version](https://badge.fury.io/js/cdk-gitlab-runner.svg)](https://badge.fury.io/js/cdk-gitlab-runner)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab-runner.svg)](https://badge.fury.io/py/cdk-gitlab-runner)
[![release](https://github.com/neilkuan/cdk-gitlab-runner/actions/workflows/release.yml/badge.svg)](https://github.com/neilkuan/cdk-gitlab-runner/actions/workflows/release.yml)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/cdk-gitlab-runner?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/cdk-gitlab-runner?label=pypi&color=blue)

![](https://img.shields.io/badge/iam_role_self-enable-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/vpc_self-enable-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/gitlab_url-customize-green=?style=plastic&logo=appveyor)
![](https://img.shields.io/badge/spotfleet-runner-green=?style=plastic&logo=appveyor)

# Welcome to `cdk-gitlab-runner`

Use AWS CDK to create gitlab runner, and use [gitlab runner](https://gitlab.com/gitlab-org/gitlab-runner) to help you execute your Gitlab Pipeline Job.

> GitLab Runner is the open source project that is used to run your CI/CD jobs and send the results back to GitLab. [(source repo)](https://gitlab.com/gitlab-org/gitlab-runner)

## Why

Gitlab provides [400 minutes per month for each free user](https://about.gitlab.com/pricing/), hosted Gitlab Runner to execute your gitlab pipeline job.That's pretty good and users don't need to manage gitlab runner. If it is just a simple ci job for test 400, it may be enough.
But what if you want to deploy to your AWS production environment through pipeline job?
Is there any security consideration for using the hosted gitlab runner?!

But creating Gitlab Runner is not that simple, so I created this OSS so that you can quickly create Gitlab Runner and delete your Gitlab Runner via AWS CDK.
It will be used with AWS IAM Role, so you don't need to put AKSK in Gitlab environment variables.

![](./image/cdk-gitlab-runner.png)

## Note

### Default will help you generate below services:

* VPC

  * Public Subnet (2)
* EC2 (1 T3.micro)

## Before start you need gitlab runner token in your `gitlab project` or `gitlab group`

## In Group before Gitlab 15.10

This registration process is only supported in GitLab Runner 15.10 or later
This registration process is not supported in GitLab Runner 15.9 or earlier and only available as an experimental feature in GitLab Runner 15.10 and 15.11. You should upgrade to GitLab Runner 16.0 or later to use a stable version of this registration process. [Check this issue](https://github.com/neilkuan/cdk-gitlab-runner/issues/1796)

Group > Settings > CI/CD
![group](image/group_runner_page.png)

## In Group after Gitlab 15.10

This registration process is only supported in GitLab Runner 15.10 or later
This registration process is not supported in GitLab Runner 15.9 or earlier and only available as an experimental feature in GitLab Runner 15.10 and 15.11. You should upgrade to GitLab Runner 16.0 or later to use a stable version of this registration process. [Check this issue](https://github.com/neilkuan/cdk-gitlab-runner/issues/1796)

Group > Build > Runners
![group](image/gitlab-runner-new-register.png)
![group](image/gitlab-runner-new-register-1.png)
![group](image/gitlab-runner-new-register-2.png)
![group](image/gitlab-runner-new-register-3.jpg)

### In Project before Gitlab 15.10

This registration process is only supported in GitLab Runner 15.10 or later
This registration process is not supported in GitLab Runner 15.9 or earlier and only available as an experimental feature in GitLab Runner 15.10 and 15.11. You should upgrade to GitLab Runner 16.0 or later to use a stable version of this registration process. [Check this issue](https://github.com/neilkuan/cdk-gitlab-runner/issues/1796)

Project > Settings > CI/CD > Runners
![project](image/project_runner_page.png)

### In Project after Gitlab 15.10

This registration process is only supported in GitLab Runner 15.10 or later
This registration process is not supported in GitLab Runner 15.9 or earlier and only available as an experimental feature in GitLab Runner 15.10 and 15.11. You should upgrade to GitLab Runner 16.0 or later to use a stable version of this registration process. [Check this issue](https://github.com/neilkuan/cdk-gitlab-runner/issues/1796)

Project > Settings > CI/CD > Runners
![project](image/gitlab-runner-new-register-project.png)

## Usage

Replace your gitlab runner token in `$GITLABTOKEN`

## Install

Use the npm dist tag to opt in CDKv1 or CDKv2:

```bash
// for CDKv2
npm install cdk-gitlab-runner
or
npm install cdk-gitlab-runner@latest

// for CDKv1
npm install cdk-gitlab-runner@cdkv1
```

## 💡💡💡 please click [here](https://github.com/neilkuan/cdk-gitlab-runner/tree/cdkv1#readme), if you are using aws-cdk v1.x.x version.💡💡💡

### Instance Type

```python
import { GitlabContainerRunner } from 'cdk-gitlab-runner';

// If want change instance type to t3.large .
new GitlabContainerRunner(this, 'runner-instance', { gitlabtoken: 'glrt-GITLABTOKEN', ec2type:'t3.large',gitlabRunnerVersion: '15.10' });
// OR
// Just create a gitlab runner , by default instance type is t3.micro .
import { GitlabContainerRunner } from 'cdk-gitlab-runner';

new GitlabContainerRunner(this, 'runner-instance', { gitlabtoken: 'glrt-GITLABTOKEN', gitlabRunnerVersion: '15.10' });
```

### Gitlab Server Customize Url .

If you want change what you want tag name .

```python
// If you want change  what  your self Gitlab Server Url .
import { GitlabContainerRunner } from 'cdk-gitlab-runner';

new GitlabContainerRunner(this, 'runner-instance-change-tag', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlaburl: 'https://gitlab.my.com/',
  gitlabRunnerVersion: '15.10'
});
```

### Tags

If you want change what you want tag name .
!!! Not support Gitlab Runner 15.10 and later !!!

```python
// If you want change  what  you want tag name .
import { GitlabContainerRunner } from 'cdk-gitlab-runner';

new GitlabContainerRunner(this, 'runner-instance-change-tag', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  tags: ['aa', 'bb', 'cc'],
});
```

### IAM Policy

If you want add runner other IAM Policy like s3-readonly-access.

```python
// If you want add runner other IAM Policy like s3-readonly-access.
import { GitlabContainerRunner } from 'cdk-gitlab-runner';
import { ManagedPolicy } from 'aws-cdk-lib/aws-iam';

const runner = new GitlabContainerRunner(this, 'runner-instance-add-policy', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  tags: ['aa', 'bb', 'cc'],
});
runner.runnerRole.addManagedPolicy(
  ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
);
```

### Security Group

If you want add runner other SG Ingress .

```python
// If you want add runner other SG Ingress .
import { GitlabContainerRunner } from 'cdk-gitlab-runner';
import { Port, Peer } from 'aws-cdk-lib/aws-ec2';

const runner = new GitlabContainerRunner(this, 'runner-add-SG-ingress', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  tags: ['aa', 'bb', 'cc'],
});

// you can add ingress in your runner SG .
runner.defaultRunnerSG.connections.allowFrom(
  Peer.ipv4('0.0.0.0/0'),
  Port.tcp(80),
);
```

### Use self VPC

> 2020/06/27 , you can use your self exist VPC or new VPC , but please check your `vpc public Subnet` Auto-assign public IPv4 address must be Yes ,or `vpc private Subnet` route table associated `nat gateway` .

```python
import { GitlabContainerRunner } from 'cdk-gitlab-runner';
import { Port, Peer, Vpc, SubnetType } from 'aws-cdk-lib/aws-ec2';
import { ManagedPolicy } from 'aws-cdk-lib/aws-iam';

const newvpc = new Vpc(stack, 'VPC', {
  ipAddresses: IpAddresses.cidr('10.0.0.0/16'),
  maxAzs: 2,
  subnetConfiguration: [
    {
      cidrMask: 26,
      name: 'RunnerVPC',
      subnetType: SubnetType.PUBLIC,
    },
  ],
  natGateways: 0,
});

const runner = new GitlabContainerRunner(this, 'testing', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  ec2type: 't3.small',
  selfvpc: newvpc,
});
```

### Use your self exist role

> 2020/06/27 , you can use your self exist role assign to runner

```python
import { GitlabContainerRunner } from 'cdk-gitlab-runner';
import { Port, Peer } from 'aws-cdk-lib/aws-ec2';
import { ManagedPolicy, Role, ServicePrincipal } from 'aws-cdk-lib/aws-iam';

const role = new Role(this, 'runner-role', {
  assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
  description: 'For Gitlab EC2 Runner Test Role',
  roleName: 'TestRole',
});

const runner = new GitlabContainerRunner(stack, 'testing', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  ec2iamrole: role,
});
runner.runnerRole.addManagedPolicy(
  ManagedPolicy.fromAwsManagedPolicyName('AmazonS3ReadOnlyAccess'),
);
```

### Custom Gitlab Runner EBS szie

> 2025/01/03 , you can change you want ebs size.

```python
import { GitlabContainerRunner } from 'cdk-gitlab-runner';
// on-demand instance
new GitlabContainerRunner(stack, 'testing', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  onDemandEbsConfig: BlockDeviceVolume.ebs(60),
});

// spotfleet instance
new GitlabContainerRunner(stack, 'testing', {
  gitlabtoken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  spotFleet: true,
  spotEbsConfig: {
    volumeSize: 50,
  },
});
```

### Control the number of runners with AutoScalingGroup

> 2020/11/25 , you can set the number of runners.

```python
import { GitlabRunnerAutoscaling } from 'cdk-gitlab-runner';

new GitlabRunnerAutoscaling(stack, 'testing', {
  gitlabToken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  minCapacity: 2,
  maxCapacity: 2,
});
```

### Support Spotfleet Gitlab Runner

> 2020/08/27 , you can use spotfleet instance be your gitlab runner,
> after create spotfleet instance will auto output instance id.

```python
import { GitlabContainerRunner, BlockDuration } from 'cdk-gitlab-runner';

const runner = new GitlabContainerRunner(stack, 'testing', {
  gitlabToken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  ec2type: 't3.large',
  spotFleet: true,
});
// configure the expiration after 1 hours
runner.expireAfter(Duration.hours(1));
```

> 2020/11/19, you setting job runtime bind host volumes.
> see more https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section

```python
import { GitlabContainerRunner, BlockDuration } from 'cdk-gitlab-runner';

const runner = new GitlabContainerRunner(stack, 'testing', {
  gitlabToken: 'glrt-GITLABTOKEN',
  gitlabRunnerVersion: '15.10',
  ec2type: 't3.large',
  dockerVolumes: [
    {
      hostPath: '/tmp/cache',
      containerPath: '/tmp/cache',
    },
  ],
});
```

## Wait about 6 mins , If success you will see your runner in that page .

![runner](image/group_runner2.png)

#### you can use tag `gitlab` , `runner` , `awscdk` ,

> !!!!! Not Support Gitlab Runner after 15.10 and later

## Example *`gitlab-ci.yaml`*

[gitlab docs see more ...](https://docs.gitlab.com/ee/ci/yaml/README.html)

```yaml
dockerjob:
  image: docker:18.09-dind
  variables:
  tags:
    - runner
    - awscdk
    - gitlab
  variables:
    DOCKER_TLS_CERTDIR: ""
  before_script:
    - docker info
  script:
    - docker info;
    - echo 'test 123';
    - echo 'hello world 1228'
```

### If your want to debug you can go to aws console

# `In your runner region !!!`

## AWS Systems Manager > Session Manager > Start a session

![system manager](image/session.png)

#### click your `runner` and click `start session`

#### in the brower console in put `bash`

```bash
# become to root
sudo -i

# list runner container .
root# docker ps -a

# modify gitlab-runner/config.toml

root# cd /home/ec2-user/.gitlab-runner/ && ls
config.toml
```

## :clap:  Supporters

[![Stargazers repo roster for @neilkuan/cdk-gitlab-runner](https://reporoster.com/stars/neilkuan/cdk-gitlab-runner)](https://github.com/neilkuan/cdk-gitlab-runner/stargazers)
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
import aws_cdk.aws_autoscaling as _aws_cdk_aws_autoscaling_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-gitlab-runner.DockerVolumes",
    jsii_struct_bases=[],
    name_mapping={"container_path": "containerPath", "host_path": "hostPath"},
)
class DockerVolumes:
    def __init__(
        self,
        *,
        container_path: builtins.str,
        host_path: builtins.str,
    ) -> None:
        '''(experimental) Docker Volumes interface.

        :param container_path: (experimental) Job Runtime Container Path Host Path.
        :param host_path: (experimental) EC2 Runner Host Path.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a7340e90cccad4868bbd85706a9e01f696a6d8037b67130d2ad8c0df2729c13)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_path": container_path,
            "host_path": host_path,
        }

    @builtins.property
    def container_path(self) -> builtins.str:
        '''(experimental) Job Runtime Container Path Host Path.

        :stability: experimental

        Example::

            - /tmp/cahce
            more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_path(self) -> builtins.str:
        '''(experimental) EC2 Runner Host Path.

        :stability: experimental

        Example::

            - /tmp/cahce
            more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section
        '''
        result = self._values.get("host_path")
        assert result is not None, "Required property 'host_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerVolumes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitlabContainerRunner(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab-runner.GitlabContainerRunner",
):
    '''(experimental) GitlabContainerRunner Construct for create a Gitlab Runner.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        gitlab_runner_version: builtins.str,
        gitlabtoken: builtins.str,
        concurrent_jobs: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        ec2iamrole: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        ec2type: typing.Optional[builtins.str] = None,
        enabled_imd_sv2: typing.Optional[builtins.bool] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlaburl: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"] = None,
        key_name: typing.Optional[builtins.str] = None,
        on_demand_ebs_config: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.BlockDeviceVolume] = None,
        runner_description: typing.Optional[builtins.str] = None,
        selfvpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        spot_ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_fleet: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param gitlab_runner_version: (experimental) Gitlab Runner version Please give me gitlab runner version.
        :param gitlabtoken: (experimental) Gitlab token for the Register Runner . Default: - You must to give the token !!!
        :param concurrent_jobs: (experimental) Gitlab Runner concurrent job configuration. Default: - concurrentJobs=1
        :param docker_volumes: (experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_size: (deprecated) Gitlab Runner instance EBS size .
        :param ec2iamrole: (experimental) IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param ec2type: (experimental) Runner default EC2 instance type. Default: - t3.micro
        :param enabled_imd_sv2: (experimental) Enabled IMDSv2. more detail see https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html Default: - false
        :param gitlab_runner_image: (experimental) Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:latest !!! <--- latest now > 16.0 Gitlab Runner version
        :param gitlaburl: (experimental) Gitlab Runner register url . Default: - gitlaburl='https://gitlab.com/' , please use https://yourgitlab.com/ do not use https://yourgitlab.com
        :param instance_interruption_behavior: (experimental) The behavior when a Spot Runner Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE , !!! only support spotfleet runner !!! .
        :param key_name: (experimental) SSH key name. Default: - no ssh key will be assigned , !!! only support spotfleet runner !!! .
        :param on_demand_ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - onDemandEbsConfig=BlockDeviceVolume.ebs(60)
        :param runner_description: (experimental) Gitlab Runner description. Default: - runnerDescription='Docker Runner'
        :param selfvpc: (experimental) VPC for the Gitlab Runner . Default: - new VPC will be created , 1 Vpc , 2 Public Subnet .
        :param spot_ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - spotEbsConfig={ volumeSize: 60}
        :param spot_fleet: (experimental) Gitlab Runner instance Use Spot Fleet or not ?!. Default: - spotFleet=false
        :param tags: (experimental) tags for the runner Unsupported Gitlab Runner 15.10 and later. Default: - ['runner', 'gitlab', 'awscdk']
        :param valid_until: (experimental) the time when the spot fleet allocation expires. Default: - no expiration , !!! only support spotfleet runner !!! .
        :param vpc_subnet: (experimental) VPC subnet for the spot fleet. Default: - public subnet

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3569128cd1ccb4f615528e61f1622fdbd79cb2ae3e5d8a3297d682bf482432fa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitlabContainerRunnerProps(
            gitlab_runner_version=gitlab_runner_version,
            gitlabtoken=gitlabtoken,
            concurrent_jobs=concurrent_jobs,
            docker_volumes=docker_volumes,
            ebs_size=ebs_size,
            ec2iamrole=ec2iamrole,
            ec2type=ec2type,
            enabled_imd_sv2=enabled_imd_sv2,
            gitlab_runner_image=gitlab_runner_image,
            gitlaburl=gitlaburl,
            instance_interruption_behavior=instance_interruption_behavior,
            key_name=key_name,
            on_demand_ebs_config=on_demand_ebs_config,
            runner_description=runner_description,
            selfvpc=selfvpc,
            spot_ebs_config=spot_ebs_config,
            spot_fleet=spot_fleet,
            tags=tags,
            valid_until=valid_until,
            vpc_subnet=vpc_subnet,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createUserData")
    def create_user_data(
        self,
        props: typing.Union["GitlabContainerRunnerProps", typing.Dict[builtins.str, typing.Any]],
        token_parameter_store_name: builtins.str,
    ) -> typing.List[builtins.str]:
        '''
        :param props: -
        :param token_parameter_store_name: - the tokenParameterStoreName to put gitlab runner token.

        :return: Array.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bd058a7173e616aea7ec4839df2470f6ebe0b7b19ab8e14adc26a124919f645)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument token_parameter_store_name", value=token_parameter_store_name, expected_type=type_hints["token_parameter_store_name"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "createUserData", [props, token_parameter_store_name]))

    @jsii.member(jsii_name="expireAfter")
    def expire_after(self, duration: _aws_cdk_ceddda9d.Duration) -> None:
        '''(experimental) Add expire time function for spotfleet runner !!! .

        :param duration: - Block duration.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573d5bebeef3dab5acf1ce20fe1bec4b423b45aa004fd1962be44c7be581f4d9)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast(None, jsii.invoke(self, "expireAfter", [duration]))

    @builtins.property
    @jsii.member(jsii_name="defaultRunnerSG")
    def default_runner_sg(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''(experimental) The EC2 runner's default SecurityGroup.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "defaultRunnerSG"))

    @builtins.property
    @jsii.member(jsii_name="runnerEc2")
    def runner_ec2(self) -> _aws_cdk_aws_ec2_ceddda9d.IInstance:
        '''(experimental) This represents a Runner EC2 instance , !!! only support On-demand runner instance !!!

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IInstance, jsii.get(self, "runnerEc2"))

    @builtins.property
    @jsii.member(jsii_name="runnerRole")
    def runner_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role assumed by the Runner instance .

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "runnerRole"))

    @builtins.property
    @jsii.member(jsii_name="spotFleetInstanceId")
    def spot_fleet_instance_id(self) -> builtins.str:
        '''(experimental) the first instance id in this fleet , !!! only support spotfleet runner !!!

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "spotFleetInstanceId"))

    @builtins.property
    @jsii.member(jsii_name="spotFleetRequestId")
    def spot_fleet_request_id(self) -> builtins.str:
        '''(experimental) SpotFleetRequestId for this spot fleet , !!! only support spotfleet runner !!!

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "spotFleetRequestId"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The EC2 runner's vpc.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-gitlab-runner.GitlabContainerRunnerProps",
    jsii_struct_bases=[],
    name_mapping={
        "gitlab_runner_version": "gitlabRunnerVersion",
        "gitlabtoken": "gitlabtoken",
        "concurrent_jobs": "concurrentJobs",
        "docker_volumes": "dockerVolumes",
        "ebs_size": "ebsSize",
        "ec2iamrole": "ec2iamrole",
        "ec2type": "ec2type",
        "enabled_imd_sv2": "enabledIMDSv2",
        "gitlab_runner_image": "gitlabRunnerImage",
        "gitlaburl": "gitlaburl",
        "instance_interruption_behavior": "instanceInterruptionBehavior",
        "key_name": "keyName",
        "on_demand_ebs_config": "onDemandEbsConfig",
        "runner_description": "runnerDescription",
        "selfvpc": "selfvpc",
        "spot_ebs_config": "spotEbsConfig",
        "spot_fleet": "spotFleet",
        "tags": "tags",
        "valid_until": "validUntil",
        "vpc_subnet": "vpcSubnet",
    },
)
class GitlabContainerRunnerProps:
    def __init__(
        self,
        *,
        gitlab_runner_version: builtins.str,
        gitlabtoken: builtins.str,
        concurrent_jobs: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        ec2iamrole: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        ec2type: typing.Optional[builtins.str] = None,
        enabled_imd_sv2: typing.Optional[builtins.bool] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlaburl: typing.Optional[builtins.str] = None,
        instance_interruption_behavior: typing.Optional["InstanceInterruptionBehavior"] = None,
        key_name: typing.Optional[builtins.str] = None,
        on_demand_ebs_config: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.BlockDeviceVolume] = None,
        runner_description: typing.Optional[builtins.str] = None,
        selfvpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        spot_ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        spot_fleet: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        valid_until: typing.Optional[builtins.str] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) GitlabContainerRunner Props.

        :param gitlab_runner_version: (experimental) Gitlab Runner version Please give me gitlab runner version.
        :param gitlabtoken: (experimental) Gitlab token for the Register Runner . Default: - You must to give the token !!!
        :param concurrent_jobs: (experimental) Gitlab Runner concurrent job configuration. Default: - concurrentJobs=1
        :param docker_volumes: (experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_size: (deprecated) Gitlab Runner instance EBS size .
        :param ec2iamrole: (experimental) IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param ec2type: (experimental) Runner default EC2 instance type. Default: - t3.micro
        :param enabled_imd_sv2: (experimental) Enabled IMDSv2. more detail see https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html Default: - false
        :param gitlab_runner_image: (experimental) Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:latest !!! <--- latest now > 16.0 Gitlab Runner version
        :param gitlaburl: (experimental) Gitlab Runner register url . Default: - gitlaburl='https://gitlab.com/' , please use https://yourgitlab.com/ do not use https://yourgitlab.com
        :param instance_interruption_behavior: (experimental) The behavior when a Spot Runner Instance is interrupted. Default: - InstanceInterruptionBehavior.TERMINATE , !!! only support spotfleet runner !!! .
        :param key_name: (experimental) SSH key name. Default: - no ssh key will be assigned , !!! only support spotfleet runner !!! .
        :param on_demand_ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - onDemandEbsConfig=BlockDeviceVolume.ebs(60)
        :param runner_description: (experimental) Gitlab Runner description. Default: - runnerDescription='Docker Runner'
        :param selfvpc: (experimental) VPC for the Gitlab Runner . Default: - new VPC will be created , 1 Vpc , 2 Public Subnet .
        :param spot_ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - spotEbsConfig={ volumeSize: 60}
        :param spot_fleet: (experimental) Gitlab Runner instance Use Spot Fleet or not ?!. Default: - spotFleet=false
        :param tags: (experimental) tags for the runner Unsupported Gitlab Runner 15.10 and later. Default: - ['runner', 'gitlab', 'awscdk']
        :param valid_until: (experimental) the time when the spot fleet allocation expires. Default: - no expiration , !!! only support spotfleet runner !!! .
        :param vpc_subnet: (experimental) VPC subnet for the spot fleet. Default: - public subnet

        :stability: experimental
        '''
        if isinstance(spot_ebs_config, dict):
            spot_ebs_config = _aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty(**spot_ebs_config)
        if isinstance(vpc_subnet, dict):
            vpc_subnet = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnet)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0026c0e7fdafbb0c3cfac95f254acf8fbd8eb0fb39b8b1e9cd3089655e745dbe)
            check_type(argname="argument gitlab_runner_version", value=gitlab_runner_version, expected_type=type_hints["gitlab_runner_version"])
            check_type(argname="argument gitlabtoken", value=gitlabtoken, expected_type=type_hints["gitlabtoken"])
            check_type(argname="argument concurrent_jobs", value=concurrent_jobs, expected_type=type_hints["concurrent_jobs"])
            check_type(argname="argument docker_volumes", value=docker_volumes, expected_type=type_hints["docker_volumes"])
            check_type(argname="argument ebs_size", value=ebs_size, expected_type=type_hints["ebs_size"])
            check_type(argname="argument ec2iamrole", value=ec2iamrole, expected_type=type_hints["ec2iamrole"])
            check_type(argname="argument ec2type", value=ec2type, expected_type=type_hints["ec2type"])
            check_type(argname="argument enabled_imd_sv2", value=enabled_imd_sv2, expected_type=type_hints["enabled_imd_sv2"])
            check_type(argname="argument gitlab_runner_image", value=gitlab_runner_image, expected_type=type_hints["gitlab_runner_image"])
            check_type(argname="argument gitlaburl", value=gitlaburl, expected_type=type_hints["gitlaburl"])
            check_type(argname="argument instance_interruption_behavior", value=instance_interruption_behavior, expected_type=type_hints["instance_interruption_behavior"])
            check_type(argname="argument key_name", value=key_name, expected_type=type_hints["key_name"])
            check_type(argname="argument on_demand_ebs_config", value=on_demand_ebs_config, expected_type=type_hints["on_demand_ebs_config"])
            check_type(argname="argument runner_description", value=runner_description, expected_type=type_hints["runner_description"])
            check_type(argname="argument selfvpc", value=selfvpc, expected_type=type_hints["selfvpc"])
            check_type(argname="argument spot_ebs_config", value=spot_ebs_config, expected_type=type_hints["spot_ebs_config"])
            check_type(argname="argument spot_fleet", value=spot_fleet, expected_type=type_hints["spot_fleet"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument valid_until", value=valid_until, expected_type=type_hints["valid_until"])
            check_type(argname="argument vpc_subnet", value=vpc_subnet, expected_type=type_hints["vpc_subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gitlab_runner_version": gitlab_runner_version,
            "gitlabtoken": gitlabtoken,
        }
        if concurrent_jobs is not None:
            self._values["concurrent_jobs"] = concurrent_jobs
        if docker_volumes is not None:
            self._values["docker_volumes"] = docker_volumes
        if ebs_size is not None:
            self._values["ebs_size"] = ebs_size
        if ec2iamrole is not None:
            self._values["ec2iamrole"] = ec2iamrole
        if ec2type is not None:
            self._values["ec2type"] = ec2type
        if enabled_imd_sv2 is not None:
            self._values["enabled_imd_sv2"] = enabled_imd_sv2
        if gitlab_runner_image is not None:
            self._values["gitlab_runner_image"] = gitlab_runner_image
        if gitlaburl is not None:
            self._values["gitlaburl"] = gitlaburl
        if instance_interruption_behavior is not None:
            self._values["instance_interruption_behavior"] = instance_interruption_behavior
        if key_name is not None:
            self._values["key_name"] = key_name
        if on_demand_ebs_config is not None:
            self._values["on_demand_ebs_config"] = on_demand_ebs_config
        if runner_description is not None:
            self._values["runner_description"] = runner_description
        if selfvpc is not None:
            self._values["selfvpc"] = selfvpc
        if spot_ebs_config is not None:
            self._values["spot_ebs_config"] = spot_ebs_config
        if spot_fleet is not None:
            self._values["spot_fleet"] = spot_fleet
        if tags is not None:
            self._values["tags"] = tags
        if valid_until is not None:
            self._values["valid_until"] = valid_until
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet

    @builtins.property
    def gitlab_runner_version(self) -> builtins.str:
        '''(experimental) Gitlab Runner version Please give me gitlab runner version.

        :stability: experimental
        '''
        result = self._values.get("gitlab_runner_version")
        assert result is not None, "Required property 'gitlab_runner_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gitlabtoken(self) -> builtins.str:
        '''(experimental) Gitlab token for the Register Runner .

        :default: - You must to give the token !!!

        :stability: experimental

        Example::

            new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN' });
        '''
        result = self._values.get("gitlabtoken")
        assert result is not None, "Required property 'gitlabtoken' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def concurrent_jobs(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Gitlab Runner concurrent job configuration.

        :default: - concurrentJobs=1

        :stability: experimental

        Example::

            const runner = new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN',concurrentJobs: 3});
        '''
        result = self._values.get("concurrent_jobs")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_volumes(self) -> typing.Optional[typing.List[DockerVolumes]]:
        '''(experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime.

        more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section

        :default: - already mount "/var/run/docker.sock:/var/run/docker.sock"

        :stability: experimental

        Example::

            dockerVolumes: [
              {
                hostPath: '/tmp/cache',
                containerPath: '/tmp/cache',
              },
            ],
        '''
        result = self._values.get("docker_volumes")
        return typing.cast(typing.Optional[typing.List[DockerVolumes]], result)

    @builtins.property
    def ebs_size(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Gitlab Runner instance EBS size .

        :deprecated: , use ebsConfig

        :stability: deprecated
        '''
        result = self._values.get("ebs_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ec2iamrole(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) IAM role for the Gitlab Runner Instance .

        :default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .

        :stability: experimental

        Example::

            const role = new Role(stack, 'runner-role', {
              assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
              description: 'For Gitlab EC2 Runner Test Role',
              roleName: 'Myself-Runner-Role',
            });
            
            new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN', ec2iamrole: role });
        '''
        result = self._values.get("ec2iamrole")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def ec2type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Runner default EC2 instance type.

        :default: - t3.micro

        :stability: experimental

        Example::

            new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN', ec2type: 't3.small' });
        '''
        result = self._values.get("ec2type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled_imd_sv2(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enabled IMDSv2.

        more detail see https://docs.aws.amazon.com/zh_tw/AWSEC2/latest/UserGuide/configuring-instance-metadata-service.html

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enabled_imd_sv2")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def gitlab_runner_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Image URL of Gitlab Runner.

        :default: public.ecr.aws/gitlab/gitlab-runner:latest !!! <--- latest now > 16.0 Gitlab Runner version

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', gitlabRunnerImage: 'gitlab/gitlab-runner:alpine' });
        '''
        result = self._values.get("gitlab_runner_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gitlaburl(self) -> typing.Optional[builtins.str]:
        '''(experimental) Gitlab Runner register url .

        :default: - gitlaburl='https://gitlab.com/' , please use https://yourgitlab.com/ do not use https://yourgitlab.com

        :stability: experimental

        Example::

            const runner = new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN',gitlaburl: 'https://gitlab.com/'});
        '''
        result = self._values.get("gitlaburl")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_interruption_behavior(
        self,
    ) -> typing.Optional["InstanceInterruptionBehavior"]:
        '''(experimental) The behavior when a Spot Runner Instance is interrupted.

        :default: - InstanceInterruptionBehavior.TERMINATE , !!! only support spotfleet runner !!! .

        :stability: experimental
        '''
        result = self._values.get("instance_interruption_behavior")
        return typing.cast(typing.Optional["InstanceInterruptionBehavior"], result)

    @builtins.property
    def key_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) SSH key name.

        :default: - no ssh key will be assigned , !!! only support spotfleet runner !!! .

        :stability: experimental
        '''
        result = self._values.get("key_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_demand_ebs_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.BlockDeviceVolume]:
        '''(experimental) Gitlab Runner instance EBS config.

        :default: - onDemandEbsConfig=BlockDeviceVolume.ebs(60)

        :stability: experimental

        Example::

            const runner = new GitlabContainerRunner(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', onDemandEbsConfig: BlockDeviceVolume.ebs(60)});
        '''
        result = self._values.get("on_demand_ebs_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.BlockDeviceVolume], result)

    @builtins.property
    def runner_description(self) -> typing.Optional[builtins.str]:
        '''(experimental) Gitlab Runner description.

        :default: - runnerDescription='Docker Runner'

        :stability: experimental

        Example::

            const runner = new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN',runnerDescription: 'Simple GitLab Runner'});
        '''
        result = self._values.get("runner_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def selfvpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC for the Gitlab Runner .

        :default: - new VPC will be created , 1 Vpc , 2 Public Subnet .

        :stability: experimental

        Example::

            const newvpc = new Vpc(stack, 'NEWVPC', {
              ipAddresses: IpAddresses.cidr('10.0.0.0/16'),
              maxAzs: 2,
              subnetConfiguration: [{
                cidrMask: 26,
                name: 'RunnerVPC',
                subnetType: SubnetType.PUBLIC,
              }],
              natGateways: 0,
            });
            
            new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN', selfvpc: newvpc });
        '''
        result = self._values.get("selfvpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def spot_ebs_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty]:
        '''(experimental) Gitlab Runner instance EBS config.

        :default: - spotEbsConfig={ volumeSize: 60}

        :stability: experimental

        Example::

            const runner = new GitlabContainerRunner(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', ebsConfig: { volumeSize: 60}});
        '''
        result = self._values.get("spot_ebs_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty], result)

    @builtins.property
    def spot_fleet(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gitlab Runner instance Use Spot Fleet or not ?!.

        :default: - spotFleet=false

        :stability: experimental

        Example::

            const runner = new GitlabContainerRunner(stack, 'runner', { gitlabtoken: 'GITLAB_TOKEN',spotFleet: true});
        '''
        result = self._values.get("spot_fleet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) tags for the runner Unsupported Gitlab Runner 15.10 and later.

        :default: - ['runner', 'gitlab', 'awscdk']

        :see: - https://docs.gitlab.com/ee/ci/runners/new_creation_workflow.html
        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def valid_until(self) -> typing.Optional[builtins.str]:
        '''(experimental) the time when the spot fleet allocation expires.

        :default: - no expiration , !!! only support spotfleet runner !!! .

        :stability: experimental
        '''
        result = self._values.get("valid_until")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) VPC subnet for the spot fleet.

        :default: - public subnet

        :stability: experimental

        Example::

            const vpc = new Vpc(stack, 'nat', {
            natGateways: 1,
            maxAzs: 2,
            });
            const runner = new GitlabContainerRunner(stack, 'testing', {
              gitlabtoken: 'GITLAB_TOKEN',
              ec2type: 't3.large',
              ec2iamrole: role,
              selfvpc: vpc,
              vpcSubnet: {
                subnetType: SubnetType.PUBLIC,
              },
            });
        '''
        result = self._values.get("vpc_subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitlabContainerRunnerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitlabRunnerAutoscaling(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab-runner.GitlabRunnerAutoscaling",
):
    '''(experimental) GitlabRunnerAutoscaling Construct for create Autoscaling Gitlab Runner.

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        gitlab_runner_version: builtins.str,
        gitlab_token: builtins.str,
        alarms: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_type: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        spot_instance: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param gitlab_runner_version: (experimental) Gitlab Runner version Please give me gitlab runner version.
        :param gitlab_token: (experimental) Gitlab token.
        :param alarms: (experimental) Parameters of put_metric_alarm function. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm Default: - [{ AlarmName: 'GitlabRunnerDiskUsage', MetricName: 'disk_used_percent', }]
        :param desired_capacity: (experimental) Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: (experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - ebsConfig={ volumeSize: 60}
        :param ebs_size: (deprecated) Gitlab Runner instance EBS size .
        :param gitlab_runner_image: (experimental) Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:latest
        :param gitlab_url: (experimental) Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param instance_role: (experimental) IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param instance_type: (experimental) Runner default EC2 instance type. Default: - t3.micro
        :param max_capacity: (experimental) Maximum capacity limit for autoscaling group. Default: - desiredCapacity
        :param min_capacity: (experimental) Minimum capacity limit for autoscaling group. Default: - minCapacity: 1
        :param spot_instance: (experimental) Run worker nodes as EC2 Spot. Default: - false
        :param tags: (experimental) tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        :param vpc: (experimental) VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param vpc_subnet: (experimental) VPC subnet. Default: - SubnetType.PRIVATE subnet

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1346a7c57bd8e3d5b6fd96e74f7310063137cbf2338091d3cb96f36a1921a41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitlabRunnerAutoscalingProps(
            gitlab_runner_version=gitlab_runner_version,
            gitlab_token=gitlab_token,
            alarms=alarms,
            desired_capacity=desired_capacity,
            docker_volumes=docker_volumes,
            ebs_config=ebs_config,
            ebs_size=ebs_size,
            gitlab_runner_image=gitlab_runner_image,
            gitlab_url=gitlab_url,
            instance_role=instance_role,
            instance_type=instance_type,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            spot_instance=spot_instance,
            tags=tags,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="createUserData")
    def create_user_data(
        self,
        *,
        gitlab_runner_version: builtins.str,
        gitlab_token: builtins.str,
        alarms: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_type: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        spot_instance: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> typing.List[builtins.str]:
        '''
        :param gitlab_runner_version: (experimental) Gitlab Runner version Please give me gitlab runner version.
        :param gitlab_token: (experimental) Gitlab token.
        :param alarms: (experimental) Parameters of put_metric_alarm function. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm Default: - [{ AlarmName: 'GitlabRunnerDiskUsage', MetricName: 'disk_used_percent', }]
        :param desired_capacity: (experimental) Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: (experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - ebsConfig={ volumeSize: 60}
        :param ebs_size: (deprecated) Gitlab Runner instance EBS size .
        :param gitlab_runner_image: (experimental) Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:latest
        :param gitlab_url: (experimental) Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param instance_role: (experimental) IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param instance_type: (experimental) Runner default EC2 instance type. Default: - t3.micro
        :param max_capacity: (experimental) Maximum capacity limit for autoscaling group. Default: - desiredCapacity
        :param min_capacity: (experimental) Minimum capacity limit for autoscaling group. Default: - minCapacity: 1
        :param spot_instance: (experimental) Run worker nodes as EC2 Spot. Default: - false
        :param tags: (experimental) tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        :param vpc: (experimental) VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param vpc_subnet: (experimental) VPC subnet. Default: - SubnetType.PRIVATE subnet

        :return: Array.

        :stability: experimental
        '''
        props = GitlabRunnerAutoscalingProps(
            gitlab_runner_version=gitlab_runner_version,
            gitlab_token=gitlab_token,
            alarms=alarms,
            desired_capacity=desired_capacity,
            docker_volumes=docker_volumes,
            ebs_config=ebs_config,
            ebs_size=ebs_size,
            gitlab_runner_image=gitlab_runner_image,
            gitlab_url=gitlab_url,
            instance_role=instance_role,
            instance_type=instance_type,
            max_capacity=max_capacity,
            min_capacity=min_capacity,
            spot_instance=spot_instance,
            tags=tags,
            vpc=vpc,
            vpc_subnet=vpc_subnet,
        )

        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "createUserData", [props]))

    @builtins.property
    @jsii.member(jsii_name="autoscalingGroup")
    def autoscaling_group(self) -> _aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup:
        '''(experimental) This represents a Runner Auto Scaling Group.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_autoscaling_ceddda9d.AutoScalingGroup, jsii.get(self, "autoscalingGroup"))

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The IAM role assumed by the Runner instance.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "instanceRole"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''(experimental) The EC2 runner's default SecurityGroup.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="topicAlarm")
    def topic_alarm(self) -> _aws_cdk_aws_sns_ceddda9d.ITopic:
        '''(experimental) The SNS topic to suscribe alarms for EC2 runner's metrics.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_sns_ceddda9d.ITopic, jsii.get(self, "topicAlarm"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) The EC2 runner's VPC.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))


@jsii.data_type(
    jsii_type="cdk-gitlab-runner.GitlabRunnerAutoscalingProps",
    jsii_struct_bases=[],
    name_mapping={
        "gitlab_runner_version": "gitlabRunnerVersion",
        "gitlab_token": "gitlabToken",
        "alarms": "alarms",
        "desired_capacity": "desiredCapacity",
        "docker_volumes": "dockerVolumes",
        "ebs_config": "ebsConfig",
        "ebs_size": "ebsSize",
        "gitlab_runner_image": "gitlabRunnerImage",
        "gitlab_url": "gitlabUrl",
        "instance_role": "instanceRole",
        "instance_type": "instanceType",
        "max_capacity": "maxCapacity",
        "min_capacity": "minCapacity",
        "spot_instance": "spotInstance",
        "tags": "tags",
        "vpc": "vpc",
        "vpc_subnet": "vpcSubnet",
    },
)
class GitlabRunnerAutoscalingProps:
    def __init__(
        self,
        *,
        gitlab_runner_version: builtins.str,
        gitlab_token: builtins.str,
        alarms: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
        ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        ebs_size: typing.Optional[jsii.Number] = None,
        gitlab_runner_image: typing.Optional[builtins.str] = None,
        gitlab_url: typing.Optional[builtins.str] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_type: typing.Optional[builtins.str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        spot_instance: typing.Optional[builtins.bool] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) GitlabRunnerAutoscaling Props.

        :param gitlab_runner_version: (experimental) Gitlab Runner version Please give me gitlab runner version.
        :param gitlab_token: (experimental) Gitlab token.
        :param alarms: (experimental) Parameters of put_metric_alarm function. https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm Default: - [{ AlarmName: 'GitlabRunnerDiskUsage', MetricName: 'disk_used_percent', }]
        :param desired_capacity: (experimental) Desired capacity limit for autoscaling group. Default: - minCapacity, and leave unchanged during deployment
        :param docker_volumes: (experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime. more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section Default: - already mount "/var/run/docker.sock:/var/run/docker.sock"
        :param ebs_config: (experimental) Gitlab Runner instance EBS config. Default: - ebsConfig={ volumeSize: 60}
        :param ebs_size: (deprecated) Gitlab Runner instance EBS size .
        :param gitlab_runner_image: (experimental) Image URL of Gitlab Runner. Default: public.ecr.aws/gitlab/gitlab-runner:latest
        :param gitlab_url: (experimental) Gitlab Runner register url . Default: - https://gitlab.com/ , The trailing slash is mandatory.
        :param instance_role: (experimental) IAM role for the Gitlab Runner Instance . Default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .
        :param instance_type: (experimental) Runner default EC2 instance type. Default: - t3.micro
        :param max_capacity: (experimental) Maximum capacity limit for autoscaling group. Default: - desiredCapacity
        :param min_capacity: (experimental) Minimum capacity limit for autoscaling group. Default: - minCapacity: 1
        :param spot_instance: (experimental) Run worker nodes as EC2 Spot. Default: - false
        :param tags: (experimental) tags for the runner. Default: - ['runner', 'gitlab', 'awscdk']
        :param vpc: (experimental) VPC for the Gitlab Runner . Default: - A new VPC will be created.
        :param vpc_subnet: (experimental) VPC subnet. Default: - SubnetType.PRIVATE subnet

        :stability: experimental
        '''
        if isinstance(ebs_config, dict):
            ebs_config = _aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty(**ebs_config)
        if isinstance(vpc_subnet, dict):
            vpc_subnet = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnet)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__456bc54665e983cecf5d286556d3b391003886fdd1d6f537def2467508670cc9)
            check_type(argname="argument gitlab_runner_version", value=gitlab_runner_version, expected_type=type_hints["gitlab_runner_version"])
            check_type(argname="argument gitlab_token", value=gitlab_token, expected_type=type_hints["gitlab_token"])
            check_type(argname="argument alarms", value=alarms, expected_type=type_hints["alarms"])
            check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            check_type(argname="argument docker_volumes", value=docker_volumes, expected_type=type_hints["docker_volumes"])
            check_type(argname="argument ebs_config", value=ebs_config, expected_type=type_hints["ebs_config"])
            check_type(argname="argument ebs_size", value=ebs_size, expected_type=type_hints["ebs_size"])
            check_type(argname="argument gitlab_runner_image", value=gitlab_runner_image, expected_type=type_hints["gitlab_runner_image"])
            check_type(argname="argument gitlab_url", value=gitlab_url, expected_type=type_hints["gitlab_url"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument max_capacity", value=max_capacity, expected_type=type_hints["max_capacity"])
            check_type(argname="argument min_capacity", value=min_capacity, expected_type=type_hints["min_capacity"])
            check_type(argname="argument spot_instance", value=spot_instance, expected_type=type_hints["spot_instance"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnet", value=vpc_subnet, expected_type=type_hints["vpc_subnet"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "gitlab_runner_version": gitlab_runner_version,
            "gitlab_token": gitlab_token,
        }
        if alarms is not None:
            self._values["alarms"] = alarms
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if docker_volumes is not None:
            self._values["docker_volumes"] = docker_volumes
        if ebs_config is not None:
            self._values["ebs_config"] = ebs_config
        if ebs_size is not None:
            self._values["ebs_size"] = ebs_size
        if gitlab_runner_image is not None:
            self._values["gitlab_runner_image"] = gitlab_runner_image
        if gitlab_url is not None:
            self._values["gitlab_url"] = gitlab_url
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if spot_instance is not None:
            self._values["spot_instance"] = spot_instance
        if tags is not None:
            self._values["tags"] = tags
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnet is not None:
            self._values["vpc_subnet"] = vpc_subnet

    @builtins.property
    def gitlab_runner_version(self) -> builtins.str:
        '''(experimental) Gitlab Runner version Please give me gitlab runner version.

        :stability: experimental
        '''
        result = self._values.get("gitlab_runner_version")
        assert result is not None, "Required property 'gitlab_runner_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def gitlab_token(self) -> builtins.str:
        '''(experimental) Gitlab token.

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN' });
        '''
        result = self._values.get("gitlab_token")
        assert result is not None, "Required property 'gitlab_token' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarms(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]]:
        '''(experimental) Parameters of put_metric_alarm function.

        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm

        :default:

        - [{
        AlarmName: 'GitlabRunnerDiskUsage',
        MetricName: 'disk_used_percent',
        }]

        :stability: experimental
        '''
        result = self._values.get("alarms")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[typing.Any, typing.Any]]], result)

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Desired capacity limit for autoscaling group.

        :default: - minCapacity, and leave unchanged during deployment

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', desiredCapacity: 2 });
        '''
        result = self._values.get("desired_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def docker_volumes(self) -> typing.Optional[typing.List[DockerVolumes]]:
        '''(experimental) add another Gitlab Container Runner Docker Volumes Path at job runner runtime.

        more detail see https://docs.gitlab.com/runner/configuration/advanced-configuration.html#the-runnersdocker-section

        :default: - already mount "/var/run/docker.sock:/var/run/docker.sock"

        :stability: experimental

        Example::

            dockerVolumes: [
              {
                hostPath: '/tmp/cache',
                containerPath: '/tmp/cache',
              },
            ],
        '''
        result = self._values.get("docker_volumes")
        return typing.cast(typing.Optional[typing.List[DockerVolumes]], result)

    @builtins.property
    def ebs_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty]:
        '''(experimental) Gitlab Runner instance EBS config.

        :default: - ebsConfig={ volumeSize: 60}

        :stability: experimental

        Example::

            const runner = new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', ebsConfig: { volumeSize: 60}});
        '''
        result = self._values.get("ebs_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty], result)

    @builtins.property
    def ebs_size(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Gitlab Runner instance EBS size .

        :deprecated: , use ebsConfig

        :stability: deprecated
        '''
        result = self._values.get("ebs_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gitlab_runner_image(self) -> typing.Optional[builtins.str]:
        '''(experimental) Image URL of Gitlab Runner.

        :default: public.ecr.aws/gitlab/gitlab-runner:latest

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', gitlabRunnerImage: 'gitlab/gitlab-runner:alpine' });
        '''
        result = self._values.get("gitlab_runner_image")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def gitlab_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) Gitlab Runner register url .

        :default: - https://gitlab.com/ , The trailing slash is mandatory.

        :stability: experimental

        Example::

            const runner = new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN',gitlabUrl: 'https://gitlab.com/'});
        '''
        result = self._values.get("gitlab_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) IAM role for the Gitlab Runner Instance .

        :default: - new Role for Gitlab Runner Instance , attach AmazonSSMManagedInstanceCore Policy .

        :stability: experimental

        Example::

            const role = new Role(stack, 'runner-role', {
              assumedBy: new ServicePrincipal('ec2.amazonaws.com'),
              description: 'For Gitlab Runner Test Role',
              roleName: 'Runner-Role',
            });
            
            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', instanceRole: role });
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) Runner default EC2 instance type.

        :default: - t3.micro

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', instanceType: 't3.small' });
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Maximum capacity limit for autoscaling group.

        :default: - desiredCapacity

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', maxCapacity: 4 });
        '''
        result = self._values.get("max_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Minimum capacity limit for autoscaling group.

        :default: - minCapacity: 1

        :stability: experimental

        Example::

            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', minCapacity: 2 });
        '''
        result = self._values.get("min_capacity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spot_instance(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run worker nodes as EC2 Spot.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("spot_instance")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) tags for the runner.

        :default: - ['runner', 'gitlab', 'awscdk']

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''(experimental) VPC for the Gitlab Runner .

        :default: - A new VPC will be created.

        :stability: experimental

        Example::

            const newVpc = new Vpc(stack, 'NewVPC', {
              ipAddresses: IpAddresses.cidr('10.0.0.0/16'),
              maxAzs: 2,
              subnetConfiguration: [{
                cidrMask: 26,
                name: 'RunnerVPC',
                subnetType: SubnetType.PUBLIC,
              }],
              natGateways: 0,
            });
            
            new GitlabRunnerAutoscaling(stack, 'runner', { gitlabToken: 'GITLAB_TOKEN', vpc: newVpc });
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnet(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) VPC subnet.

        :default: - SubnetType.PRIVATE subnet

        :stability: experimental

        Example::

            const vpc = new Vpc(stack, 'nat', {
            natGateways: 1,
            maxAzs: 2,
            });
            const runner = new GitlabRunnerAutoscaling(stack, 'testing', {
              gitlabToken: 'GITLAB_TOKEN',
              instanceType: 't3.large',
              instanceRole: role,
              vpc: vpc,
              vpcSubnet: {
                subnetType: SubnetType.PUBLIC,
              },
            });
        '''
        result = self._values.get("vpc_subnet")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitlabRunnerAutoscalingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-gitlab-runner.InstanceInterruptionBehavior")
class InstanceInterruptionBehavior(enum.Enum):
    '''(experimental) InstanceInterruptionBehavior enum.

    :stability: experimental
    '''

    HIBERNATE = "HIBERNATE"
    '''(experimental) hibernate.

    :stability: experimental
    '''
    STOP = "STOP"
    '''(experimental) stop.

    :stability: experimental
    '''
    TERMINATE = "TERMINATE"
    '''(experimental) terminate.

    :stability: experimental
    '''


__all__ = [
    "DockerVolumes",
    "GitlabContainerRunner",
    "GitlabContainerRunnerProps",
    "GitlabRunnerAutoscaling",
    "GitlabRunnerAutoscalingProps",
    "InstanceInterruptionBehavior",
]

publication.publish()

def _typecheckingstub__6a7340e90cccad4868bbd85706a9e01f696a6d8037b67130d2ad8c0df2729c13(
    *,
    container_path: builtins.str,
    host_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3569128cd1ccb4f615528e61f1622fdbd79cb2ae3e5d8a3297d682bf482432fa(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gitlab_runner_version: builtins.str,
    gitlabtoken: builtins.str,
    concurrent_jobs: typing.Optional[jsii.Number] = None,
    docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    ebs_size: typing.Optional[jsii.Number] = None,
    ec2iamrole: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ec2type: typing.Optional[builtins.str] = None,
    enabled_imd_sv2: typing.Optional[builtins.bool] = None,
    gitlab_runner_image: typing.Optional[builtins.str] = None,
    gitlaburl: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    key_name: typing.Optional[builtins.str] = None,
    on_demand_ebs_config: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.BlockDeviceVolume] = None,
    runner_description: typing.Optional[builtins.str] = None,
    selfvpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    spot_ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_fleet: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    valid_until: typing.Optional[builtins.str] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bd058a7173e616aea7ec4839df2470f6ebe0b7b19ab8e14adc26a124919f645(
    props: typing.Union[GitlabContainerRunnerProps, typing.Dict[builtins.str, typing.Any]],
    token_parameter_store_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573d5bebeef3dab5acf1ce20fe1bec4b423b45aa004fd1962be44c7be581f4d9(
    duration: _aws_cdk_ceddda9d.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0026c0e7fdafbb0c3cfac95f254acf8fbd8eb0fb39b8b1e9cd3089655e745dbe(
    *,
    gitlab_runner_version: builtins.str,
    gitlabtoken: builtins.str,
    concurrent_jobs: typing.Optional[jsii.Number] = None,
    docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    ebs_size: typing.Optional[jsii.Number] = None,
    ec2iamrole: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ec2type: typing.Optional[builtins.str] = None,
    enabled_imd_sv2: typing.Optional[builtins.bool] = None,
    gitlab_runner_image: typing.Optional[builtins.str] = None,
    gitlaburl: typing.Optional[builtins.str] = None,
    instance_interruption_behavior: typing.Optional[InstanceInterruptionBehavior] = None,
    key_name: typing.Optional[builtins.str] = None,
    on_demand_ebs_config: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.BlockDeviceVolume] = None,
    runner_description: typing.Optional[builtins.str] = None,
    selfvpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    spot_ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    spot_fleet: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    valid_until: typing.Optional[builtins.str] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1346a7c57bd8e3d5b6fd96e74f7310063137cbf2338091d3cb96f36a1921a41(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gitlab_runner_version: builtins.str,
    gitlab_token: builtins.str,
    alarms: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_size: typing.Optional[jsii.Number] = None,
    gitlab_runner_image: typing.Optional[builtins.str] = None,
    gitlab_url: typing.Optional[builtins.str] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instance_type: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    spot_instance: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__456bc54665e983cecf5d286556d3b391003886fdd1d6f537def2467508670cc9(
    *,
    gitlab_runner_version: builtins.str,
    gitlab_token: builtins.str,
    alarms: typing.Optional[typing.Sequence[typing.Mapping[typing.Any, typing.Any]]] = None,
    desired_capacity: typing.Optional[jsii.Number] = None,
    docker_volumes: typing.Optional[typing.Sequence[typing.Union[DockerVolumes, typing.Dict[builtins.str, typing.Any]]]] = None,
    ebs_config: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.CfnLaunchTemplate.EbsProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ebs_size: typing.Optional[jsii.Number] = None,
    gitlab_runner_image: typing.Optional[builtins.str] = None,
    gitlab_url: typing.Optional[builtins.str] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instance_type: typing.Optional[builtins.str] = None,
    max_capacity: typing.Optional[jsii.Number] = None,
    min_capacity: typing.Optional[jsii.Number] = None,
    spot_instance: typing.Optional[builtins.bool] = None,
    tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnet: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
