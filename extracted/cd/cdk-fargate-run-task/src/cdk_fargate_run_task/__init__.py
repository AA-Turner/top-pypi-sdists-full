'''
[![NPM version](https://badge.fury.io/js/cdk-fargate-run-task.svg)](https://badge.fury.io/js/cdk-fargate-run-task)
[![PyPI version](https://badge.fury.io/py/cdk-fargate-run-task.svg)](https://badge.fury.io/py/cdk-fargate-run-task)
[![build](https://github.com/pahud/cdk-fargate-run-task/actions/workflows/build.yml/badge.svg)](https://github.com/pahud/cdk-fargate-run-task/actions/workflows/build.yml)

# cdk-fargate-run-task

Define and run container tasks on AWS Fargate at once or by schedule.

# sample

```python
const app = new cdk.App();

const env = {
  account: process.env.CDK_DEFAULT_ACCOUNT,
  region: process.env.CDK_DEFAULT_REGION,
};

const stack = new cdk.Stack(app, 'run-task-demo-stack', { env });

// define your task
const task = new ecs.FargateTaskDefinition(stack, 'Task', { cpu: 256, memoryLimitMiB: 512 });

// add contianer into the task
task.addContainer('Ping', {
  image: ecs.ContainerImage.fromRegistry('busybox'),
  command: [
    'sh', '-c',
    'ping -c 3 google.com',
  ],
  logging: new ecs.AwsLogDriver({
    streamPrefix: 'Ping',
    logGroup: new LogGroup(stack, 'LogGroup', {
      logGroupName: `${stack.stackName}LogGroup`,
      retention: RetentionDays.ONE_DAY,
    }),
  }),
});

// deploy and run this task once
const runTaskAtOnce = new RunTask(stack, 'RunDemoTaskOnce', { task });

// or run it with schedule(every hour 0min)
new RunTask(stack, 'RunDemoTaskEveryHour', {
  task,
  cluster: runTaskAtOnce.cluster,
  runOnce: false,
  schedule: Schedule.cron({ minute: '0' }),
});
```

## Public Subnets only VPC

To run task in public subnets only VPC:

```python
new RunTask(stack, 'RunTask', {
  task,
  vpcSubnets: {
    subnetType: ec2.SubnetType.PUBLIC,
  },
```

# ECS Anywhere

[Amazon ECS Anywhere](https://aws.amazon.com/ecs/anywhere/) allows you to run ECS tasks on external instances. To run external task once or on schedule:

```python
const externalTask = new ecs.TaskDefinition(stack, 'ExternalTask', {
  cpu: '256',
  memoryMiB: '512',
  compatibility: ecs.Compatibility.EXTERNAL,
});

externalTask.addContainer('ExternalPing', {
  image: ecs.ContainerImage.fromRegistry('busybox'),
  command: [
    'sh', '-c',
    'ping -c 3 google.com',
  ],
  logging: new ecs.AwsLogDriver({
    streamPrefix: 'Ping',
    logGroup: new LogGroup(stack, 'ExternalLogGroup', {
      retention: RetentionDays.ONE_DAY,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    }),
  }),
});

// run it once on external instance
new RunTask(stack, 'RunDemoTaskFromExternal', {
  task: externalTask,
  cluster: existingCluster,
  launchType: LaunchType.EXTERNAL,
});

// run it by schedule  on external instance
new RunTask(stack, 'RunDemoTaskFromExternalSchedule', {
  task: externalTask,
  cluster: existingCluster,
  launchType: LaunchType.EXTERNAL,
  runAtOnce: false,
  schedule: Schedule.cron({ minute: '0' }),
});
```

Please note when you run task in `EXTERNAL` launch type, no fargate tasks will be scheduled. You will be responsible to register the external instances to your ECS cluster. See [Registering an external instance to a cluster](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-anywhere-registration.html) for more details.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.custom_resources as _aws_cdk_custom_resources_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="cdk-fargate-run-task.LaunchType")
class LaunchType(enum.Enum):
    FARGATE = "FARGATE"
    EXTERNAL = "EXTERNAL"


@jsii.enum(jsii_type="cdk-fargate-run-task.PlatformVersion")
class PlatformVersion(enum.Enum):
    '''Fargate platform version.'''

    V1_3_0 = "V1_3_0"
    V1_4_0 = "V1_4_0"
    LATEST = "LATEST"


@jsii.implements(_aws_cdk_aws_ec2_ceddda9d.IConnectable)
class RunTask(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-fargate-run-task.RunTask",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        task: _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
        fargate_platform_version: typing.Optional[PlatformVersion] = None,
        launch_type: typing.Optional[LaunchType] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        run_at_once: typing.Optional[builtins.bool] = None,
        run_on_resource_update: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param task: The Amazon ECS Task definition for AWS Fargate.
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: false
        :param capacity_provider_strategy: The capacity provider strategy to run the fargate task; Default: - No capacity provider strategy defined. Use LaunchType instead.
        :param cluster: The Amazon ECS Cluster. Default: - create a new cluster
        :param fargate_platform_version: Fargate platform version. Default: LATEST
        :param launch_type: Luanch Type of the task. Default is ``FARGATE``, however, if you choose ``EXTERNAL``, you are allowed to run external tasks on external instances. The ``capacityProviderStrategy`` will be ingored if you specify this property. Please note this is the feature from ECS Anywhere. The external task will be scheduled on the registered external instance(s). No fargate task will be scheduled in the ``EXTERNAL`` launch type. Default: FARGATE
        :param log_retention: Log retention days. Default: - one week
        :param run_at_once: run it at once(immediately after deployment). Default: true
        :param run_on_resource_update: run the task again on the custom resource update. Default: false
        :param schedule: run the task with defined schedule. Default: - no shedule
        :param security_group: fargate security group. Default: - create a default security group
        :param vpc: The VPC for the Amazon ECS task. Default: - create a new VPC or use existing one
        :param vpc_subnets: The subnets to run the task. Default: - { ec2.SubnetType.PRIVATE_WITH_NAT }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8933709ce6be0978c83e2e4bf58faa0e03d7928c43f79f05efa54d3bce34fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RunTaskProps(
            task=task,
            assign_public_ip=assign_public_ip,
            capacity_provider_strategy=capacity_provider_strategy,
            cluster=cluster,
            fargate_platform_version=fargate_platform_version,
            launch_type=launch_type,
            log_retention=log_retention,
            run_at_once=run_at_once,
            run_on_resource_update=run_on_resource_update,
            schedule=schedule,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.ICluster:
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''makes RunTask "connectable".'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="securityGroup")
    def security_group(self) -> _aws_cdk_aws_ec2_ceddda9d.ISecurityGroup:
        '''fargate task security group.'''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup, jsii.get(self, "securityGroup"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, jsii.get(self, "vpc"))

    @builtins.property
    @jsii.member(jsii_name="runOnceResource")
    def run_once_resource(
        self,
    ) -> typing.Optional[_aws_cdk_custom_resources_ceddda9d.AwsCustomResource]:
        '''The custom resource of the runOnce execution.'''
        return typing.cast(typing.Optional[_aws_cdk_custom_resources_ceddda9d.AwsCustomResource], jsii.get(self, "runOnceResource"))


@jsii.data_type(
    jsii_type="cdk-fargate-run-task.RunTaskProps",
    jsii_struct_bases=[],
    name_mapping={
        "task": "task",
        "assign_public_ip": "assignPublicIp",
        "capacity_provider_strategy": "capacityProviderStrategy",
        "cluster": "cluster",
        "fargate_platform_version": "fargatePlatformVersion",
        "launch_type": "launchType",
        "log_retention": "logRetention",
        "run_at_once": "runAtOnce",
        "run_on_resource_update": "runOnResourceUpdate",
        "schedule": "schedule",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class RunTaskProps:
    def __init__(
        self,
        *,
        task: _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
        fargate_platform_version: typing.Optional[PlatformVersion] = None,
        launch_type: typing.Optional[LaunchType] = None,
        log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
        run_at_once: typing.Optional[builtins.bool] = None,
        run_on_resource_update: typing.Optional[builtins.bool] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
        security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
        vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param task: The Amazon ECS Task definition for AWS Fargate.
        :param assign_public_ip: Specifies whether the task's elastic network interface receives a public IP address. If true, each task will receive a public IP address. Default: false
        :param capacity_provider_strategy: The capacity provider strategy to run the fargate task; Default: - No capacity provider strategy defined. Use LaunchType instead.
        :param cluster: The Amazon ECS Cluster. Default: - create a new cluster
        :param fargate_platform_version: Fargate platform version. Default: LATEST
        :param launch_type: Luanch Type of the task. Default is ``FARGATE``, however, if you choose ``EXTERNAL``, you are allowed to run external tasks on external instances. The ``capacityProviderStrategy`` will be ingored if you specify this property. Please note this is the feature from ECS Anywhere. The external task will be scheduled on the registered external instance(s). No fargate task will be scheduled in the ``EXTERNAL`` launch type. Default: FARGATE
        :param log_retention: Log retention days. Default: - one week
        :param run_at_once: run it at once(immediately after deployment). Default: true
        :param run_on_resource_update: run the task again on the custom resource update. Default: false
        :param schedule: run the task with defined schedule. Default: - no shedule
        :param security_group: fargate security group. Default: - create a default security group
        :param vpc: The VPC for the Amazon ECS task. Default: - create a new VPC or use existing one
        :param vpc_subnets: The subnets to run the task. Default: - { ec2.SubnetType.PRIVATE_WITH_NAT }
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c14a221ca288d188334ee55b30a1dfebf2bf1cd1ed8804f74f16ff7972eca92)
            check_type(argname="argument task", value=task, expected_type=type_hints["task"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument capacity_provider_strategy", value=capacity_provider_strategy, expected_type=type_hints["capacity_provider_strategy"])
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
            check_type(argname="argument fargate_platform_version", value=fargate_platform_version, expected_type=type_hints["fargate_platform_version"])
            check_type(argname="argument launch_type", value=launch_type, expected_type=type_hints["launch_type"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument run_at_once", value=run_at_once, expected_type=type_hints["run_at_once"])
            check_type(argname="argument run_on_resource_update", value=run_on_resource_update, expected_type=type_hints["run_on_resource_update"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task": task,
        }
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if capacity_provider_strategy is not None:
            self._values["capacity_provider_strategy"] = capacity_provider_strategy
        if cluster is not None:
            self._values["cluster"] = cluster
        if fargate_platform_version is not None:
            self._values["fargate_platform_version"] = fargate_platform_version
        if launch_type is not None:
            self._values["launch_type"] = launch_type
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if run_at_once is not None:
            self._values["run_at_once"] = run_at_once
        if run_on_resource_update is not None:
            self._values["run_on_resource_update"] = run_on_resource_update
        if schedule is not None:
            self._values["schedule"] = schedule
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def task(self) -> _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition:
        '''The Amazon ECS Task definition for AWS Fargate.'''
        result = self._values.get("task")
        assert result is not None, "Required property 'task' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition, result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''Specifies whether the task's elastic network interface receives a public IP address.

        If true, each task will receive a public IP address.

        :default: false
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def capacity_provider_strategy(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]]:
        '''The capacity provider strategy to run the fargate task;

        :default: - No capacity provider strategy defined. Use LaunchType instead.
        '''
        result = self._values.get("capacity_provider_strategy")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]], result)

    @builtins.property
    def cluster(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster]:
        '''The Amazon ECS Cluster.

        :default: - create a new cluster
        '''
        result = self._values.get("cluster")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster], result)

    @builtins.property
    def fargate_platform_version(self) -> typing.Optional[PlatformVersion]:
        '''Fargate platform version.

        :default: LATEST
        '''
        result = self._values.get("fargate_platform_version")
        return typing.cast(typing.Optional[PlatformVersion], result)

    @builtins.property
    def launch_type(self) -> typing.Optional[LaunchType]:
        '''Luanch Type of the task.

        Default is ``FARGATE``, however, if you choose ``EXTERNAL``, you are allowed to
        run external tasks on external instances. The ``capacityProviderStrategy`` will be ingored if you specify
        this property. Please note this is the feature from ECS Anywhere. The external task will be scheduled on the
        registered external instance(s). No fargate task will be scheduled in the ``EXTERNAL`` launch type.

        :default: FARGATE
        '''
        result = self._values.get("launch_type")
        return typing.cast(typing.Optional[LaunchType], result)

    @builtins.property
    def log_retention(
        self,
    ) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays]:
        '''Log retention days.

        :default: - one week
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays], result)

    @builtins.property
    def run_at_once(self) -> typing.Optional[builtins.bool]:
        '''run it at once(immediately after deployment).

        :default: true
        '''
        result = self._values.get("run_at_once")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def run_on_resource_update(self) -> typing.Optional[builtins.bool]:
        '''run the task again on the custom resource update.

        :default: false
        '''
        result = self._values.get("run_on_resource_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schedule(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule]:
        '''run the task with defined schedule.

        :default: - no shedule
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule], result)

    @builtins.property
    def security_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''fargate security group.

        :default: - create a default security group
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc]:
        '''The VPC for the Amazon ECS task.

        :default: - create a new VPC or use existing one
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''The subnets to run the task.

        :default: - { ec2.SubnetType.PRIVATE_WITH_NAT }
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "LaunchType",
    "PlatformVersion",
    "RunTask",
    "RunTaskProps",
]

publication.publish()

def _typecheckingstub__4a8933709ce6be0978c83e2e4bf58faa0e03d7928c43f79f05efa54d3bce34fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    task: _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
    fargate_platform_version: typing.Optional[PlatformVersion] = None,
    launch_type: typing.Optional[LaunchType] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    run_at_once: typing.Optional[builtins.bool] = None,
    run_on_resource_update: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c14a221ca288d188334ee55b30a1dfebf2bf1cd1ed8804f74f16ff7972eca92(
    *,
    task: _aws_cdk_aws_ecs_ceddda9d.FargateTaskDefinition,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    capacity_provider_strategy: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    cluster: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.ICluster] = None,
    fargate_platform_version: typing.Optional[PlatformVersion] = None,
    launch_type: typing.Optional[LaunchType] = None,
    log_retention: typing.Optional[_aws_cdk_aws_logs_ceddda9d.RetentionDays] = None,
    run_at_once: typing.Optional[builtins.bool] = None,
    run_on_resource_update: typing.Optional[builtins.bool] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_ceddda9d.Schedule] = None,
    security_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup] = None,
    vpc: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IVpc] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass
