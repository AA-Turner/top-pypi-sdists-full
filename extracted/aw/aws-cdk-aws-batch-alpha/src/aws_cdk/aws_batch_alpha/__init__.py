'''
# AWS Batch Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Developer Preview](https://img.shields.io/badge/cdk--constructs-developer--preview-informational.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are in **developer preview** before they
> become stable. We will only make breaking changes to address unforeseen API issues. Therefore,
> these APIs are not subject to [Semantic Versioning](https://semver.org/), and breaking changes
> will be announced in release notes. This means that while you may use them, you may need to
> update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

AWS Batch is a batch processing tool for efficiently running hundreds of thousands computing jobs in AWS.
Batch can dynamically provision [Amazon EC2](https://aws.amazon.com/ec2/) Instances to meet the resource requirements of submitted jobs
and simplifies the planning, scheduling, and executions of your batch workloads. Batch achieves this through four different resources:

* ComputeEnvironments: Contain the resources used to execute Jobs
* JobDefinitions: Define a type of Job that can be submitted
* JobQueues: Route waiting Jobs to ComputeEnvironments
* SchedulingPolicies: Applied to Queues to control how and when Jobs exit the JobQueue and enter the ComputeEnvironment

`ComputeEnvironment`s can be managed or unmanaged. Batch will automatically provision EC2 Instances in a managed `ComputeEnvironment` and will
not provision any Instances in an unmanaged `ComputeEnvironment`. Managed `ComputeEnvironment`s can use ECS, Fargate, or EKS resources to spin up
EC2 Instances in (ensure your EKS Cluster has [been configured](https://docs.aws.amazon.com/batch/latest/userguide/getting-started-eks.html)
to support a Batch ComputeEnvironment before linking it). You can use Launch Templates and Placement Groups to configure exactly how these resources
will be provisioned.

`JobDefinition`s can use either ECS resources or EKS resources. ECS `JobDefinition`s can use multiple containers to execute distributed workloads.
EKS `JobDefinition`s can only execute a single container. Submitted Jobs use `JobDefinition`s as templates.

`JobQueue`s must link at least one `ComputeEnvironment`. Jobs exit the Queue in FIFO order unless a `SchedulingPolicy` is specified.

`SchedulingPolicy`s tell the Scheduler how to choose which Jobs should be executed next by the ComputeEnvironment.

## Use Cases & Examples

### Cost Optimization

#### Spot Instances

Spot instances are significantly discounted EC2 instances that can be reclaimed at any time by AWS.
Workloads that are fault-tolerant or stateless can take advantage of spot pricing.
To use spot spot instances, set `spot` to `true` on a managed Ec2 or Fargate Compute Environment:

```python
vpc = ec2.Vpc(self, "VPC")
batch.FargateComputeEnvironment(self, "myFargateComputeEnv",
    vpc=vpc,
    spot=True
)
```

Batch allows you to specify the percentage of the on-demand instance that the current spot price
must be to provision the instance using the `spotBidPercentage`.
This defaults to 100%, which is the recommended value.
This value cannot be specified for `FargateComputeEnvironment`s
and only applies to `ManagedEc2EcsComputeEnvironment`s.
The following code configures a Compute Environment to only use spot instances that
are at most 20% the price of the on-demand instance price:

```python
vpc = ec2.Vpc(self, "VPC")
batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    vpc=vpc,
    spot=True,
    spot_bid_percentage=20
)
```

For stateful or otherwise non-interruption-tolerant workflows, omit `spot` or set it to `false` to only provision on-demand instances.

#### Choosing Your Instance Types

Batch allows you to choose the instance types or classes that will run your workload.
This example configures your `ComputeEnvironment` to use only the `M5AD.large` instance:

```python
vpc = ec2.Vpc(self, "VPC")

batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    vpc=vpc,
    instance_types=[ec2.InstanceType.of(ec2.InstanceClass.M5AD, ec2.InstanceSize.LARGE)]
)
```

Batch allows you to specify only the instance class and to let it choose the size, which you can do like this:

```python
# compute_env: batch.IManagedEc2EcsComputeEnvironment
vpc = ec2.Vpc(self, "VPC")
compute_env.add_instance_class(ec2.InstanceClass.M5AD)
# Or, specify it on the constructor:
batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    vpc=vpc,
    instance_classes=[ec2.InstanceClass.R4]
)
```

Unless you explicitly specify `useOptimalInstanceClasses: false`, this compute environment will use `'optimal'` instances,
which tells Batch to pick an instance from the C4, M4, and R4 instance families.
*Note*: Batch does not allow specifying instance types or classes with different architectures.
For example, `InstanceClass.A1` cannot be specified alongside `'optimal'`,
because `A1` uses ARM and `'optimal'` uses x86_64.
You can specify both `'optimal'` alongside several different instance types in the same compute environment:

```python
# vpc: ec2.IVpc


compute_env = batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    instance_types=[ec2.InstanceType.of(ec2.InstanceClass.M5AD, ec2.InstanceSize.LARGE)],
    use_optimal_instance_classes=True,  # default
    vpc=vpc
)
# Note: this is equivalent to specifying
compute_env.add_instance_type(ec2.InstanceType.of(ec2.InstanceClass.M5AD, ec2.InstanceSize.LARGE))
compute_env.add_instance_class(ec2.InstanceClass.C4)
compute_env.add_instance_class(ec2.InstanceClass.M4)
compute_env.add_instance_class(ec2.InstanceClass.R4)
```

#### Allocation Strategies

| Allocation Strategy           | Optimized for              | Downsides                     |
| -----------------------       | -------------              | ----------------------------- |
| BEST_FIT                      | Cost                       | May limit throughput          |
| BEST_FIT_PROGRESSIVE          | Throughput                 | May increase cost             |
| SPOT_CAPACITY_OPTIMIZED       | Least interruption         | Only useful on Spot instances |
| SPOT_PRICE_CAPACITY_OPTIMIZED | Least interruption + Price | Only useful on Spot instances |

Batch provides different Allocation Strategies to help it choose which instances to provision.
If your workflow tolerates interruptions, you should enable `spot` on your `ComputeEnvironment`
and use `SPOT_PRICE_CAPACITY_OPTIMIZED` (this is the default if `spot` is enabled).
This will tell Batch to choose the instance types from the ones you’ve specified that have
the most spot capacity available to minimize the chance of interruption and have the lowest price.
To get the most benefit from your spot instances,
you should allow Batch to choose from as many different instance types as possible.
If you only care about minimal interruptions and not want Batch to optimize for cost, use
`SPOT_CAPACITY_OPTIMIZED`. `SPOT_PRICE_CAPACITY_OPTIMIZED` is recommended over `SPOT_CAPACITY_OPTIMIZED`
for most use cases.

If your workflow does not tolerate interruptions and you want to minimize your costs at the expense
of potentially longer waiting times, use `AllocationStrategy.BEST_FIT`.
This will choose the lowest-cost instance type that fits all the jobs in the queue.
If instances of that type are not available,
the queue will not choose a new type; instead, it will wait for the instance to become available.
This can stall your `Queue`, with your compute environment only using part of its max capacity
(or none at all) until the `BEST_FIT` instance becomes available.

If you are running a workflow that does not tolerate interruptions and you want to maximize throughput,
you can use `AllocationStrategy.BEST_FIT_PROGRESSIVE`.
This is the default Allocation Strategy if `spot` is `false` or unspecified.
This strategy will examine the Jobs in the queue and choose whichever instance type meets the requirements
of the jobs in the queue and with the lowest cost per vCPU, just as `BEST_FIT`.
However, if not all of the capacity can be filled with this instance type,
it will choose a new next-best instance type to run any jobs that couldn’t fit into the `BEST_FIT` capacity.
To make the most use of this allocation strategy,
it is recommended to use as many instance classes as is feasible for your workload.
This example shows a `ComputeEnvironment` that uses `BEST_FIT_PROGRESSIVE`
with `'optimal'` and `InstanceClass.M5` instance types:

```python
# vpc: ec2.IVpc


compute_env = batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    vpc=vpc,
    instance_classes=[ec2.InstanceClass.M5]
)
```

This example shows a `ComputeEnvironment` that uses `BEST_FIT` with `'optimal'` instances:

```python
# vpc: ec2.IVpc


compute_env = batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    vpc=vpc,
    allocation_strategy=batch.AllocationStrategy.BEST_FIT
)
```

*Note*: `allocationStrategy` cannot be specified on Fargate Compute Environments.

### Controlling vCPU allocation

You can specify the maximum and minimum vCPUs a managed `ComputeEnvironment` can have at any given time.
Batch will *always* maintain `minvCpus` worth of instances in your ComputeEnvironment, even if it is not executing any jobs,
and even if it is disabled. Batch will scale the instances up to `maxvCpus` worth of instances as
jobs exit the JobQueue and enter the ComputeEnvironment. If you use `AllocationStrategy.BEST_FIT_PROGRESSIVE`,
`AllocationStrategy.SPOT_PRICE_CAPACITY_OPTIMIZED`, or `AllocationStrategy.SPOT_CAPACITY_OPTIMIZED`,
batch may exceed `maxvCpus`; it will never exceed `maxvCpus` by more than a single instance type. This example configures a
`minvCpus` of 10 and a `maxvCpus` of 100:

```python
# vpc: ec2.IVpc


batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
    vpc=vpc,
    instance_classes=[ec2.InstanceClass.R4],
    minv_cpus=10,
    maxv_cpus=100
)
```

### Tagging Instances

You can tag any instances launched by your managed EC2 ComputeEnvironments by using the CDK `Tags` API:

```python
from aws_cdk import Tags

# vpc: ec2.IVpc


tag_cE = batch.ManagedEc2EcsComputeEnvironment(self, "CEThatMakesTaggedInstnaces",
    vpc=vpc
)

Tags.of(tag_cE).add("super", "salamander")
```

Unmanaged `ComputeEnvironment`s do not support `maxvCpus` or `minvCpus` because you must provision and manage the instances yourself;
that is, Batch will not scale them up and down as needed.

### Sharing a ComputeEnvironment between multiple JobQueues

Multiple `JobQueue`s can share the same `ComputeEnvironment`.
If multiple Queues are attempting to submit Jobs to the same `ComputeEnvironment`,
Batch will pick the Job from the Queue with the highest priority.
This example creates two `JobQueue`s that share a `ComputeEnvironment`:

```python
# vpc: ec2.IVpc

shared_compute_env = batch.FargateComputeEnvironment(self, "spotEnv",
    vpc=vpc,
    spot=True
)
low_priority_queue = batch.JobQueue(self, "JobQueue",
    priority=1
)
high_priority_queue = batch.JobQueue(self, "JobQueue",
    priority=10
)
low_priority_queue.add_compute_environment(shared_compute_env, 1)
high_priority_queue.add_compute_environment(shared_compute_env, 1)
```

### Fairshare Scheduling

Batch `JobQueue`s execute Jobs submitted to them in FIFO order unless you specify a `SchedulingPolicy`.
FIFO queuing can cause short-running jobs to be starved while long-running jobs fill the compute environment.
To solve this, Jobs can be associated with a share.

Shares consist of a `shareIdentifier` and a `weightFactor`, which is inversely correlated with the vCPU allocated to that share identifier.
When submitting a Job, you can specify its `shareIdentifier` to associate that particular job with that share.
Let's see how the scheduler uses this information to schedule jobs.

For example, if there are two shares defined as follows:

| Share Identifier | Weight Factor |
| ---------------- | ------------- |
| A                | 1             |
| B                | 1             |

The weight factors share the following relationship:

```math
A_{vCpus} / A_{Weight} = B_{vCpus} / B_{Weight}
```

where `BvCpus` is the number of vCPUs allocated to jobs with share identifier `'B'`, and `B_weight` is the weight factor of `B`.

The total number of vCpus allocated to a share is equal to the amount of jobs in that share times the number of vCpus necessary for every job.
Let's say that each A job needs 32 VCpus (`A_requirement` = 32) and each B job needs 64 vCpus (`B_requirement` = 64):

```math
A_{vCpus} = A_{Jobs} * A_{Requirement}
```

```math
B_{vCpus} = B_{Jobs} * B_{Requirement}
```

We have:

```math
A_{vCpus} / A_{Weight} = B_{vCpus} / B_{Weight}
```

```math
A_{Jobs} * A_{Requirement} / A_{Weight} = B_{Jobs} * B_{Requirement} / B_{Weight}
```

```math
A_{Jobs} * 32 / 1 = B_{Jobs} * 64 / 1
```

```math
A_{Jobs} * 32 = B_{Jobs} * 64
```

```math
A_{Jobs} = B_{Jobs} * 2
```

Thus the scheduler will schedule two `'A'` jobs for each `'B'` job.

You can control the weight factors to change these ratios, but note that
weight factors are inversely correlated with the vCpus allocated to the corresponding share.

This example would be configured like this:

```python
fairshare_policy = batch.FairshareSchedulingPolicy(self, "myFairsharePolicy")

fairshare_policy.add_share(
    share_identifier="A",
    weight_factor=1
)
fairshare_policy.add_share(
    share_identifier="B",
    weight_factor=1
)
batch.JobQueue(self, "JobQueue",
    scheduling_policy=fairshare_policy
)
```

*Note*: The scheduler will only consider the current usage of the compute environment unless you specify `shareDecay`.
For example, a `shareDecay` of 5 minutes in the above example means that at any given point in time, twice as many `'A'` jobs
will be scheduled for each `'B'` job, but only for the past 5 minutes. If `'B'` jobs run longer than 5 minutes, then
the scheduler is allowed to put more than two `'A'` jobs for each `'B'` job, because the usage of those long-running
`'B'` jobs will no longer be considered after 5 minutes. `shareDecay` linearly decreases the usage of
long running jobs for calculation purposes. For example if share decay is 60 seconds,
then jobs that run for 30 seconds have their usage considered to be only 50% of what it actually is,
but after a whole minute the scheduler pretends they don't exist for fairness calculations.

The following code specifies a `shareDecay` of 5 minutes:

```python
import aws_cdk as cdk

fairshare_policy = batch.FairshareSchedulingPolicy(self, "myFairsharePolicy",
    share_decay=cdk.Duration.minutes(5)
)
```

If you have high priority jobs that should always be executed as soon as they arrive,
you can define a `computeReservation` to specify the percentage of the
maximum vCPU capacity that should be reserved for shares that are *not in the queue*.
The actual reserved percentage is defined by Batch as:

```math
 (\frac{computeReservation}{100}) ^ {ActiveFairShares}
```

where `ActiveFairShares` is the number of shares for which there exists
at least one job in the queue with a unique share identifier.

This is best illustrated with an example.
Suppose there are three shares with share identifiers `A`, `B` and `C` respectively
and we specify the `computeReservation` to be 75%. The queue is currently empty,
and no other shares exist.

There are no active fair shares, since the queue is empty.
Thus (75/100)^0 = 1 = 100% of the maximum vCpus are reserved for all shares.

A job with identifier `A` enters the queue.

The number of active fair shares is now 1, hence
(75/100)^1 = .75 = 75% of the maximum vCpus are reserved for all shares that do not have the identifier `A`;
for this example, this is `B` and `C`,
(but if jobs are submitted with a share identifier not covered by this fairshare policy, those would be considered just as `B` and `C` are).

Now a `B` job enters the queue. The number of active fair shares is now 2,
so (75/100)^2 = .5625 = 56.25% of the maximum vCpus are reserved for all shares that do not have the identifier `A` or `B`.

Now a second `A` job enters the queue. The number of active fair shares is still 2,
so the percentage reserved is still 56.25%

Now a `C` job enters the queue. The number of active fair shares is now 3,
so (75/100)^3 = .421875 = 42.1875% of the maximum vCpus are reserved for all shares that do not have the identifier `A`, `B`, or `C`.

If there are no other shares that your jobs can specify, this means that 42.1875% of your capacity will never be used!

Now, `A`, `B`, and `C` can only consume 100% - 42.1875% = 57.8125% of the maximum vCpus.
Note that the this percentage is **not** split between `A`, `B`, and `C`.
Instead, the scheduler will use their `weightFactor`s to decide which jobs to schedule;
the only difference is that instead of competing for 100% of the max capacity, jobs compete for 57.8125% of the max capacity.

This example specifies a `computeReservation` of 75% that will behave as explained in the example above:

```python
batch.FairshareSchedulingPolicy(self, "myFairsharePolicy",
    compute_reservation=75,
    shares=[batch.Share(weight_factor=1, share_identifier="A"), batch.Share(weight_factor=0.5, share_identifier="B"), batch.Share(weight_factor=2, share_identifier="C")
    ]
)
```

You can specify a `priority` on your `JobDefinition`s to tell the scheduler to prioritize certain jobs that share the same share identifier.

### Configuring Job Retry Policies

Certain workflows may result in Jobs failing due to intermittent issues.
Jobs can specify retry policies to respond to different failures with different actions.
There are three different ways information about the way a Job exited can be conveyed;

* `exitCode`: the exit code returned from the process executed by the container. Will only match non-zero exit codes.
* `reason`: any middleware errors, like your Docker registry being down.
* `statusReason`: infrastructure errors, most commonly your spot instance being reclaimed.

For most use cases, only one of these will be associated with a particular action at a time.
To specify common `exitCode`s, `reason`s, or `statusReason`s, use the corresponding value from
the `Reason` class. This example shows some common failure reasons:

```python
import aws_cdk as cdk


job_defn = batch.EcsJobDefinition(self, "JobDefn",
    container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
        memory=cdk.Size.mebibytes(2048),
        cpu=256
    ),
    retry_attempts=5,
    retry_strategies=[
        batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER)
    ]
)
job_defn.add_retry_strategy(
    batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.SPOT_INSTANCE_RECLAIMED))
job_defn.add_retry_strategy(
    batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER))
job_defn.add_retry_strategy(
    batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.custom(
        on_exit_code="40*",
        on_reason="some reason"
    )))
```

When specifying a custom reason,
you can specify a glob string to match each of these and react to different failures accordingly.
Up to five different retry strategies can be configured for each Job,
and each strategy can match against some or all of `exitCode`, `reason`, and `statusReason`.
You can optionally configure the number of times a job will be retried,
but you cannot configure different retry counts for different strategies; they all share the same count.
If multiple conditions are specified in a given retry strategy,
they must all match for the action to be taken; the conditions are ANDed together, not ORed.

### Running single-container ECS workflows

Batch can run jobs on ECS or EKS. ECS jobs can be defined as single container or multinode.
This example creates a `JobDefinition` that runs a single container with ECS:

```python
import aws_cdk as cdk
import aws_cdk.aws_iam as iam
import aws_cdk.aws_efs as efs

# my_file_system: efs.IFileSystem
# my_job_role: iam.Role

my_file_system.grant_read(my_job_role)

job_defn = batch.EcsJobDefinition(self, "JobDefn",
    container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
        memory=cdk.Size.mebibytes(2048),
        cpu=256,
        volumes=[batch.EcsVolume.efs(
            name="myVolume",
            file_system=my_file_system,
            container_path="/Volumes/myVolume",
            use_job_role=True
        )],
        job_role=my_job_role
    )
)
```

For workflows that need persistent storage, batch supports mounting `Volume`s to the container.
You can both provision the volume and mount it to the container in a single operation:

```python
import aws_cdk.aws_efs as efs

# my_file_system: efs.IFileSystem
# job_defn: batch.EcsJobDefinition


job_defn.container.add_volume(batch.EcsVolume.efs(
    name="myVolume",
    file_system=my_file_system,
    container_path="/Volumes/myVolume"
))
```

### Secrets

You can expose SecretsManager Secret ARNs or SSM Parameters to your container as environment variables.
The following example defines the `MY_SECRET_ENV_VAR` environment variable that contains the
ARN of the Secret defined by `mySecret`:

```python
import aws_cdk as cdk

# my_secret: secretsmanager.ISecret


job_defn = batch.EcsJobDefinition(self, "JobDefn",
    container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
        memory=cdk.Size.mebibytes(2048),
        cpu=256,
        secrets={
            "MY_SECRET_ENV_VAR": batch.Secret.from_secrets_manager(my_secret)
        }
    )
)
```

### Running Kubernetes Workflows

Batch also supports running workflows on EKS. The following example creates a `JobDefinition` that runs on EKS:

```python
import aws_cdk as cdk

job_defn = batch.EksJobDefinition(self, "eksf2",
    container=batch.EksContainerDefinition(self, "container",
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        volumes=[batch.EksVolume.empty_dir(
            name="myEmptyDirVolume",
            mount_path="/mount/path",
            medium=batch.EmptyDirMediumType.MEMORY,
            readonly=True,
            size_limit=cdk.Size.mebibytes(2048)
        )]
    )
)
```

You can mount `Volume`s to these containers in a single operation:

```python
# job_defn: batch.EksJobDefinition

job_defn.container.add_volume(batch.EksVolume.empty_dir(
    name="emptyDir",
    mount_path="/Volumes/emptyDir"
))
job_defn.container.add_volume(batch.EksVolume.host_path(
    name="hostPath",
    host_path="/sys",
    mount_path="/Volumes/hostPath"
))
job_defn.container.add_volume(batch.EksVolume.secret(
    name="secret",
    optional=True,
    mount_path="/Volumes/secret",
    secret_name="mySecret"
))
```

### Running Distributed Workflows

Some workflows benefit from parallellization and are most powerful when run in a distributed environment,
such as certain numerical calculations or simulations. Batch offers `MultiNodeJobDefinition`s,
which allow a single job to run on multiple instances in parallel, for this purpose.
Message Passing Interface (MPI) is often used with these workflows.
You must configure your containers to use MPI properly,
but Batch allows different nodes running different containers to communicate easily with one another.
You must configure your containers to use certain environment variables that Batch will provide them,
which lets them know which one is the main node, among other information.
For an in-depth example on using MPI to perform numerical computations on Batch,
see this [blog post](https://aws.amazon.com/blogs/compute/building-a-tightly-coupled-molecular-dynamics-workflow-with-multi-node-parallel-jobs-in-aws-batch/)
In particular, the environment variable that tells the containers which one is the main node can be configured on your `MultiNodeJobDefinition` as follows:

```python
import aws_cdk as cdk

multi_node_job = batch.MultiNodeJobDefinition(self, "JobDefinition",
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R4, ec2.InstanceSize.LARGE),
    containers=[batch.MultiNodeContainer(
        container=batch.EcsEc2ContainerDefinition(self, "mainMPIContainer",
            image=ecs.ContainerImage.from_registry("yourregsitry.com/yourMPIImage:latest"),
            cpu=256,
            memory=cdk.Size.mebibytes(2048)
        ),
        start_node=0,
        end_node=5
    )]
)
# convenience method
multi_node_job.add_container(
    start_node=6,
    end_node=10,
    container=batch.EcsEc2ContainerDefinition(self, "multiContainer",
        image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        cpu=256,
        memory=cdk.Size.mebibytes(2048)
    )
)
```

If you need to set the control node to an index other than 0, specify it in directly:

```python
multi_node_job = batch.MultiNodeJobDefinition(self, "JobDefinition",
    main_node=5,
    instance_type=ec2.InstanceType.of(ec2.InstanceClass.R4, ec2.InstanceSize.LARGE)
)
```

### Pass Parameters to a Job

Batch allows you define parameters in your `JobDefinition`, which can be referenced in the container command. For example:

```python
import aws_cdk as cdk

batch.EcsJobDefinition(self, "JobDefn",
    parameters={"echo_param": "foobar"},
    container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
        memory=cdk.Size.mebibytes(2048),
        cpu=256,
        command=["echo", "Ref::echoParam"
        ]
    )
)
```

### Understanding Progressive Allocation Strategies

AWS Batch uses an [allocation strategy](https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html) to determine what compute resource will efficiently handle incoming job requests. By default, **BEST_FIT** will pick an available compute instance based on vCPU requirements. If none exist, the job will wait until resources become available. However, with this strategy, you may have jobs waiting in the queue unnecessarily despite having more powerful instances available. Below is an example of how that situation might look like:

```plaintext
Compute Environment:

1. m5.xlarge => 4 vCPU
2. m5.2xlarge => 8 vCPU
```

```plaintext
Job Queue:
---------
| A | B |
---------

Job Requirements:
A => 4 vCPU - ALLOCATED TO m5.xlarge
B => 2 vCPU - WAITING
```

In this situation, Batch will allocate **Job A** to compute resource #1 because it is the most cost efficient resource that matches the vCPU requirement. However, with this `BEST_FIT` strategy, **Job B** will not be allocated to our other available compute resource even though it is strong enough to handle it. Instead, it will wait until the first job is finished processing or wait a similar `m5.xlarge` resource to be provisioned.

The alternative would be to use the `BEST_FIT_PROGRESSIVE` strategy in order for the remaining job to be handled in larger containers regardless of vCPU requirement and costs.

### Permissions

You can grant any Principal the `batch:submitJob` permission on both a job definition and a job queue like this:

```python
import aws_cdk as cdk
import aws_cdk.aws_iam as iam

# vpc: ec2.IVpc


ecs_job = batch.EcsJobDefinition(self, "JobDefn",
    container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
        memory=cdk.Size.mebibytes(2048),
        cpu=256
    )
)

queue = batch.JobQueue(self, "JobQueue",
    compute_environments=[batch.OrderedComputeEnvironment(
        compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
            vpc=vpc
        ),
        order=1
    )],
    priority=10
)

user = iam.User(self, "MyUser")
ecs_job.grant_submit_job(user, queue)
```
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

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_batch as _aws_cdk_aws_batch_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_efs as _aws_cdk_aws_efs_ceddda9d
import aws_cdk.aws_eks as _aws_cdk_aws_eks_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.Action")
class Action(enum.Enum):
    '''(experimental) The Action to take when all specified conditions in a RetryStrategy are met.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        
        job_defn = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256
            ),
            retry_attempts=5,
            retry_strategies=[
                batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER)
            ]
        )
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.SPOT_INSTANCE_RECLAIMED))
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER))
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.custom(
                on_exit_code="40*",
                on_reason="some reason"
            )))
    '''

    EXIT = "EXIT"
    '''(experimental) The job will not retry.

    :stability: experimental
    '''
    RETRY = "RETRY"
    '''(experimental) The job will retry.

    It can be retried up to the number of times specified in ``retryAttempts``.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.AllocationStrategy")
class AllocationStrategy(enum.Enum):
    '''(experimental) Determines how this compute environment chooses instances to spawn.

    :see: https://aws.amazon.com/blogs/compute/optimizing-for-cost-availability-and-throughput-by-selecting-your-aws-batch-allocation-strategy/
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # vpc: ec2.IVpc
        
        
        compute_env = batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
            vpc=vpc,
            allocation_strategy=batch.AllocationStrategy.BEST_FIT
        )
    '''

    BEST_FIT = "BEST_FIT"
    '''(experimental) Batch chooses the lowest-cost instance type that fits all the jobs in the queue.

    If instances of that type are not available, the queue will not choose a new type;
    instead, it will wait for the instance to become available.
    This can stall your ``Queue``, with your compute environment only using part of its max capacity
    (or none at all) until the ``BEST_FIT`` instance becomes available.
    This allocation strategy keeps costs lower but can limit scaling.
    ``BEST_FIT`` isn't supported when updating compute environments

    :stability: experimental
    '''
    BEST_FIT_PROGRESSIVE = "BEST_FIT_PROGRESSIVE"
    '''(experimental) This is the default Allocation Strategy if ``spot`` is ``false`` or unspecified.

    This strategy will examine the Jobs in the queue and choose whichever instance type meets the requirements
    of the jobs in the queue and with the lowest cost per vCPU, just as ``BEST_FIT``.
    However, if not all of the capacity can be filled with this instance type,
    it will choose a new next-best instance type to run any jobs that couldn’t fit into the ``BEST_FIT`` capacity.
    To make the most use of this allocation strategy,
    it is recommended to use as many instance classes as is feasible for your workload.

    :stability: experimental
    '''
    SPOT_CAPACITY_OPTIMIZED = "SPOT_CAPACITY_OPTIMIZED"
    '''(experimental) If your workflow tolerates interruptions, you should enable ``spot`` on your ``ComputeEnvironment`` and use ``SPOT_CAPACITY_OPTIMIZED`` (this is the default if ``spot`` is enabled).

    This will tell Batch to choose the instance types from the ones you’ve specified that have
    the most spot capacity available to minimize the chance of interruption.
    To get the most benefit from your spot instances,
    you should allow Batch to choose from as many different instance types as possible.

    :stability: experimental
    '''
    SPOT_PRICE_CAPACITY_OPTIMIZED = "SPOT_PRICE_CAPACITY_OPTIMIZED"
    '''(experimental) The price and capacity optimized allocation strategy looks at both price and capacity to select the Spot Instance pools that are the least likely to be interrupted and have the lowest possible price.

    The Batch team recommends this over ``SPOT_CAPACITY_OPTIMIZED`` in most instances.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.ComputeEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "enabled": "enabled",
        "service_role": "serviceRole",
    },
)
class ComputeEnvironmentProps:
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Props common to all ComputeEnvironments.

        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            compute_environment_props = batch_alpha.ComputeEnvironmentProps(
                compute_environment_name="computeEnvironmentName",
                enabled=False,
                service_role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d827f561c1e2643ccfedecf52d55816f36a64383c9490ba8339fdd4f4723a97c)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ComputeEnvironment.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.CustomReason",
    jsii_struct_bases=[],
    name_mapping={
        "on_exit_code": "onExitCode",
        "on_reason": "onReason",
        "on_status_reason": "onStatusReason",
    },
)
class CustomReason:
    def __init__(
        self,
        *,
        on_exit_code: typing.Optional[builtins.str] = None,
        on_reason: typing.Optional[builtins.str] = None,
        on_status_reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) The corresponding Action will only be taken if *all* of the conditions specified here are met.

        :param on_exit_code: (experimental) A glob string that will match on the job exit code. For example, ``'40*'`` will match 400, 404, 40123456789012 Default: - will not match on the exit code
        :param on_reason: (experimental) A glob string that will match on the reason returned by the exiting job For example, ``'CannotPullContainerError*'`` indicates that container needed to start the job could not be pulled. Default: - will not match on the reason
        :param on_status_reason: (experimental) A glob string that will match on the statusReason returned by the exiting job. For example, ``'Host EC2*'`` indicates that the spot instance has been reclaimed. Default: - will not match on the status reason

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            
            job_defn = batch.EcsJobDefinition(self, "JobDefn",
                container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                    image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                    memory=cdk.Size.mebibytes(2048),
                    cpu=256
                ),
                retry_attempts=5,
                retry_strategies=[
                    batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER)
                ]
            )
            job_defn.add_retry_strategy(
                batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.SPOT_INSTANCE_RECLAIMED))
            job_defn.add_retry_strategy(
                batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER))
            job_defn.add_retry_strategy(
                batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.custom(
                    on_exit_code="40*",
                    on_reason="some reason"
                )))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34a1b2439a15559af9fb419414f098bca7f859cce42e28628fa89a3fbd48fa5b)
            check_type(argname="argument on_exit_code", value=on_exit_code, expected_type=type_hints["on_exit_code"])
            check_type(argname="argument on_reason", value=on_reason, expected_type=type_hints["on_reason"])
            check_type(argname="argument on_status_reason", value=on_status_reason, expected_type=type_hints["on_status_reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if on_exit_code is not None:
            self._values["on_exit_code"] = on_exit_code
        if on_reason is not None:
            self._values["on_reason"] = on_reason
        if on_status_reason is not None:
            self._values["on_status_reason"] = on_status_reason

    @builtins.property
    def on_exit_code(self) -> typing.Optional[builtins.str]:
        '''(experimental) A glob string that will match on the job exit code.

        For example, ``'40*'`` will match 400, 404, 40123456789012

        :default: - will not match on the exit code

        :stability: experimental
        '''
        result = self._values.get("on_exit_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_reason(self) -> typing.Optional[builtins.str]:
        '''(experimental) A glob string that will match on the reason returned by the exiting job For example, ``'CannotPullContainerError*'`` indicates that container needed to start the job could not be pulled.

        :default: - will not match on the reason

        :stability: experimental
        '''
        result = self._values.get("on_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def on_status_reason(self) -> typing.Optional[builtins.str]:
        '''(experimental) A glob string that will match on the statusReason returned by the exiting job.

        For example, ``'Host EC2*'`` indicates that the spot instance has been reclaimed.

        :default: - will not match on the status reason

        :stability: experimental
        '''
        result = self._values.get("on_status_reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomReason(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.Device",
    jsii_struct_bases=[],
    name_mapping={
        "host_path": "hostPath",
        "container_path": "containerPath",
        "permissions": "permissions",
    },
)
class Device:
    def __init__(
        self,
        *,
        host_path: builtins.str,
        container_path: typing.Optional[builtins.str] = None,
        permissions: typing.Optional[typing.Sequence["DevicePermission"]] = None,
    ) -> None:
        '''(experimental) A container instance host device.

        :param host_path: (experimental) The path for the device on the host container instance.
        :param container_path: (experimental) The path inside the container at which to expose the host device. Default: Same path as the host
        :param permissions: (experimental) The explicit permissions to provide to the container for the device. By default, the container has permissions for read, write, and mknod for the device. Default: Readonly

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            device = batch_alpha.Device(
                host_path="hostPath",
            
                # the properties below are optional
                container_path="containerPath",
                permissions=[batch_alpha.DevicePermission.READ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81e8e75a9432ab711a80858f17b1795231ea3916d8259c9a5b95d91b3411217)
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "host_path": host_path,
        }
        if container_path is not None:
            self._values["container_path"] = container_path
        if permissions is not None:
            self._values["permissions"] = permissions

    @builtins.property
    def host_path(self) -> builtins.str:
        '''(experimental) The path for the device on the host container instance.

        :stability: experimental
        '''
        result = self._values.get("host_path")
        assert result is not None, "Required property 'host_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path inside the container at which to expose the host device.

        :default: Same path as the host

        :stability: experimental
        '''
        result = self._values.get("container_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions(self) -> typing.Optional[typing.List["DevicePermission"]]:
        '''(experimental) The explicit permissions to provide to the container for the device.

        By default, the container has permissions for read, write, and mknod for the device.

        :default: Readonly

        :stability: experimental
        '''
        result = self._values.get("permissions")
        return typing.cast(typing.Optional[typing.List["DevicePermission"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Device(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.DevicePermission")
class DevicePermission(enum.Enum):
    '''(experimental) Permissions for device access.

    :stability: experimental
    '''

    READ = "READ"
    '''(experimental) Read.

    :stability: experimental
    '''
    WRITE = "WRITE"
    '''(experimental) Write.

    :stability: experimental
    '''
    MKNOD = "MKNOD"
    '''(experimental) Make a node.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.DnsPolicy")
class DnsPolicy(enum.Enum):
    '''(experimental) The DNS Policy for the pod used by the Job Definition.

    :see: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy
    :stability: experimental
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) The Pod inherits the name resolution configuration from the node that the Pods run on.

    :stability: experimental
    '''
    CLUSTER_FIRST = "CLUSTER_FIRST"
    '''(experimental) Any DNS query that does not match the configured cluster domain suffix, such as ``"www.kubernetes.io"``, is forwarded to an upstream nameserver by the DNS server. Cluster administrators may have extra stub-domain and upstream DNS servers configured.

    :stability: experimental
    '''
    CLUSTER_FIRST_WITH_HOST_NET = "CLUSTER_FIRST_WITH_HOST_NET"
    '''(experimental) For Pods running with ``hostNetwork``, you should explicitly set its DNS policy to ``CLUSTER_FIRST_WITH_HOST_NET``.

    Otherwise, Pods running with ``hostNetwork`` and ``CLUSTER_FIRST`` will fallback to the behavior of the ``DEFAULT`` policy.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EcsContainerDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "cpu": "cpu",
        "image": "image",
        "memory": "memory",
        "command": "command",
        "environment": "environment",
        "execution_role": "executionRole",
        "job_role": "jobRole",
        "linux_parameters": "linuxParameters",
        "logging": "logging",
        "readonly_root_filesystem": "readonlyRootFilesystem",
        "secrets": "secrets",
        "user": "user",
        "volumes": "volumes",
    },
)
class EcsContainerDefinitionProps:
    def __init__(
        self,
        *,
        cpu: jsii.Number,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        memory: _aws_cdk_ceddda9d.Size,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        linux_parameters: typing.Optional["LinuxParameters"] = None,
        logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, "Secret"]] = None,
        user: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence["EcsVolume"]] = None,
    ) -> None:
        '''(experimental) Props to configure an EcsContainerDefinition.

        :param cpu: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. For containers running on EC2 resources, you must specify at least one vCPU.
        :param image: (experimental) The image that this container will run.
        :param memory: (experimental) The memory hard limit present to the container. If your container attempts to exceed the memory specified, the container is terminated. You must specify at least 4 MiB of memory for a job.
        :param command: (experimental) The command that's passed to the container. Default: - no command
        :param environment: (experimental) The environment variables to pass to a container. Cannot start with ``AWS_BATCH``. We don't recommend using plaintext environment variables for sensitive information, such as credential data. Default: - no environment variables
        :param execution_role: (experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf. Default: - a Role will be created
        :param job_role: (experimental) The role that the container can assume. Default: - no job role
        :param linux_parameters: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. Default: none
        :param logging: (experimental) The loging configuration for this Job. Default: - the log configuration of the Docker daemon
        :param readonly_root_filesystem: (experimental) Gives the container readonly access to its root filesystem. Default: false
        :param secrets: (experimental) A map from environment variable names to the secrets for the container. Allows your job definitions to reference the secret by the environment variable name defined in this property. Default: - no secrets
        :param user: (experimental) The user name to use inside the container. Default: - no user
        :param volumes: (experimental) The volumes to mount to this container. Automatically added to the job definition. Default: - no volumes

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_ecs as ecs
            from aws_cdk import aws_iam as iam
            
            # container_image: ecs.ContainerImage
            # ecs_volume: batch_alpha.EcsVolume
            # linux_parameters: batch_alpha.LinuxParameters
            # log_driver: ecs.LogDriver
            # role: iam.Role
            # secret: batch_alpha.Secret
            # size: cdk.Size
            
            ecs_container_definition_props = batch_alpha.EcsContainerDefinitionProps(
                cpu=123,
                image=container_image,
                memory=size,
            
                # the properties below are optional
                command=["command"],
                environment={
                    "environment_key": "environment"
                },
                execution_role=role,
                job_role=role,
                linux_parameters=linux_parameters,
                logging=log_driver,
                readonly_root_filesystem=False,
                secrets={
                    "secrets_key": secret
                },
                user="user",
                volumes=[ecs_volume]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ce2351c7933476492b6019bf0c8b32e1ca81b2717193b3c66c4c10c9c5544e)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument job_role", value=job_role, expected_type=type_hints["job_role"])
            check_type(argname="argument linux_parameters", value=linux_parameters, expected_type=type_hints["linux_parameters"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "image": image,
            "memory": memory,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if job_role is not None:
            self._values["job_role"] = job_role
        if linux_parameters is not None:
            self._values["linux_parameters"] = linux_parameters
        if logging is not None:
            self._values["logging"] = logging
        if readonly_root_filesystem is not None:
            self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None:
            self._values["secrets"] = secrets
        if user is not None:
            self._values["user"] = user
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, result)

    @builtins.property
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Size, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :default: - no command

        :see: https://docs.docker.com/engine/reference/builder/#cmd
        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :default: - a Role will be created

        :see: https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html
        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :default: - no job role

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
        :stability: experimental
        '''
        result = self._values.get("job_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("linux_parameters")
        return typing.cast(typing.Optional["LinuxParameters"], result)

    @builtins.property
    def logging(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver]:
        '''(experimental) The loging configuration for this Job.

        :default: - the log configuration of the Docker daemon

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver], result)

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly_root_filesystem")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :default: - no secrets

        :see: https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html
        :stability: experimental
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Secret"]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :default: - no user

        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["EcsVolume"]]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :default: - no volumes

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List["EcsVolume"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsContainerDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EcsEc2ContainerDefinitionProps",
    jsii_struct_bases=[EcsContainerDefinitionProps],
    name_mapping={
        "cpu": "cpu",
        "image": "image",
        "memory": "memory",
        "command": "command",
        "environment": "environment",
        "execution_role": "executionRole",
        "job_role": "jobRole",
        "linux_parameters": "linuxParameters",
        "logging": "logging",
        "readonly_root_filesystem": "readonlyRootFilesystem",
        "secrets": "secrets",
        "user": "user",
        "volumes": "volumes",
        "gpu": "gpu",
        "privileged": "privileged",
        "ulimits": "ulimits",
    },
)
class EcsEc2ContainerDefinitionProps(EcsContainerDefinitionProps):
    def __init__(
        self,
        *,
        cpu: jsii.Number,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        memory: _aws_cdk_ceddda9d.Size,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        linux_parameters: typing.Optional["LinuxParameters"] = None,
        logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, "Secret"]] = None,
        user: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence["EcsVolume"]] = None,
        gpu: typing.Optional[jsii.Number] = None,
        privileged: typing.Optional[builtins.bool] = None,
        ulimits: typing.Optional[typing.Sequence[typing.Union["Ulimit", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Props to configure an EcsEc2ContainerDefinition.

        :param cpu: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. For containers running on EC2 resources, you must specify at least one vCPU.
        :param image: (experimental) The image that this container will run.
        :param memory: (experimental) The memory hard limit present to the container. If your container attempts to exceed the memory specified, the container is terminated. You must specify at least 4 MiB of memory for a job.
        :param command: (experimental) The command that's passed to the container. Default: - no command
        :param environment: (experimental) The environment variables to pass to a container. Cannot start with ``AWS_BATCH``. We don't recommend using plaintext environment variables for sensitive information, such as credential data. Default: - no environment variables
        :param execution_role: (experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf. Default: - a Role will be created
        :param job_role: (experimental) The role that the container can assume. Default: - no job role
        :param linux_parameters: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. Default: none
        :param logging: (experimental) The loging configuration for this Job. Default: - the log configuration of the Docker daemon
        :param readonly_root_filesystem: (experimental) Gives the container readonly access to its root filesystem. Default: false
        :param secrets: (experimental) A map from environment variable names to the secrets for the container. Allows your job definitions to reference the secret by the environment variable name defined in this property. Default: - no secrets
        :param user: (experimental) The user name to use inside the container. Default: - no user
        :param volumes: (experimental) The volumes to mount to this container. Automatically added to the job definition. Default: - no volumes
        :param gpu: (experimental) The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on. Default: - no gpus
        :param privileged: (experimental) When this parameter is true, the container is given elevated permissions on the host container instance (similar to the root user). Default: false
        :param ulimits: (experimental) Limits to set for the user this docker container will run as. Default: - no ulimits

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            import aws_cdk.aws_iam as iam
            
            # vpc: ec2.IVpc
            
            
            ecs_job = batch.EcsJobDefinition(self, "JobDefn",
                container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                    image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                    memory=cdk.Size.mebibytes(2048),
                    cpu=256
                )
            )
            
            queue = batch.JobQueue(self, "JobQueue",
                compute_environments=[batch.OrderedComputeEnvironment(
                    compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
                        vpc=vpc
                    ),
                    order=1
                )],
                priority=10
            )
            
            user = iam.User(self, "MyUser")
            ecs_job.grant_submit_job(user, queue)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69b95619d0ef073cf4a12636fc9060fc5c6b021c6fb057e989657c2fda7ec1f3)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument job_role", value=job_role, expected_type=type_hints["job_role"])
            check_type(argname="argument linux_parameters", value=linux_parameters, expected_type=type_hints["linux_parameters"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument gpu", value=gpu, expected_type=type_hints["gpu"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument ulimits", value=ulimits, expected_type=type_hints["ulimits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "image": image,
            "memory": memory,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if job_role is not None:
            self._values["job_role"] = job_role
        if linux_parameters is not None:
            self._values["linux_parameters"] = linux_parameters
        if logging is not None:
            self._values["logging"] = logging
        if readonly_root_filesystem is not None:
            self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None:
            self._values["secrets"] = secrets
        if user is not None:
            self._values["user"] = user
        if volumes is not None:
            self._values["volumes"] = volumes
        if gpu is not None:
            self._values["gpu"] = gpu
        if privileged is not None:
            self._values["privileged"] = privileged
        if ulimits is not None:
            self._values["ulimits"] = ulimits

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, result)

    @builtins.property
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Size, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :default: - no command

        :see: https://docs.docker.com/engine/reference/builder/#cmd
        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :default: - a Role will be created

        :see: https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html
        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :default: - no job role

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
        :stability: experimental
        '''
        result = self._values.get("job_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("linux_parameters")
        return typing.cast(typing.Optional["LinuxParameters"], result)

    @builtins.property
    def logging(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver]:
        '''(experimental) The loging configuration for this Job.

        :default: - the log configuration of the Docker daemon

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver], result)

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly_root_filesystem")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :default: - no secrets

        :see: https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html
        :stability: experimental
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Secret"]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :default: - no user

        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["EcsVolume"]]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :default: - no volumes

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List["EcsVolume"]], result)

    @builtins.property
    def gpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of physical GPUs to reserve for the container.

        Make sure that the number of GPUs reserved for all containers in a job doesn't exceed
        the number of available GPUs on the compute resource that the job is launched on.

        :default: - no gpus

        :stability: experimental
        '''
        result = self._values.get("gpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When this parameter is true, the container is given elevated permissions on the host container instance (similar to the root user).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ulimits(self) -> typing.Optional[typing.List["Ulimit"]]:
        '''(experimental) Limits to set for the user this docker container will run as.

        :default: - no ulimits

        :stability: experimental
        '''
        result = self._values.get("ulimits")
        return typing.cast(typing.Optional[typing.List["Ulimit"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsEc2ContainerDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EcsFargateContainerDefinitionProps",
    jsii_struct_bases=[EcsContainerDefinitionProps],
    name_mapping={
        "cpu": "cpu",
        "image": "image",
        "memory": "memory",
        "command": "command",
        "environment": "environment",
        "execution_role": "executionRole",
        "job_role": "jobRole",
        "linux_parameters": "linuxParameters",
        "logging": "logging",
        "readonly_root_filesystem": "readonlyRootFilesystem",
        "secrets": "secrets",
        "user": "user",
        "volumes": "volumes",
        "assign_public_ip": "assignPublicIp",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "fargate_platform_version": "fargatePlatformVersion",
    },
)
class EcsFargateContainerDefinitionProps(EcsContainerDefinitionProps):
    def __init__(
        self,
        *,
        cpu: jsii.Number,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        memory: _aws_cdk_ceddda9d.Size,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        linux_parameters: typing.Optional["LinuxParameters"] = None,
        logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, "Secret"]] = None,
        user: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence["EcsVolume"]] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        fargate_platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
    ) -> None:
        '''(experimental) Props to configure an EcsFargateContainerDefinition.

        :param cpu: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. For containers running on EC2 resources, you must specify at least one vCPU.
        :param image: (experimental) The image that this container will run.
        :param memory: (experimental) The memory hard limit present to the container. If your container attempts to exceed the memory specified, the container is terminated. You must specify at least 4 MiB of memory for a job.
        :param command: (experimental) The command that's passed to the container. Default: - no command
        :param environment: (experimental) The environment variables to pass to a container. Cannot start with ``AWS_BATCH``. We don't recommend using plaintext environment variables for sensitive information, such as credential data. Default: - no environment variables
        :param execution_role: (experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf. Default: - a Role will be created
        :param job_role: (experimental) The role that the container can assume. Default: - no job role
        :param linux_parameters: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. Default: none
        :param logging: (experimental) The loging configuration for this Job. Default: - the log configuration of the Docker daemon
        :param readonly_root_filesystem: (experimental) Gives the container readonly access to its root filesystem. Default: false
        :param secrets: (experimental) A map from environment variable names to the secrets for the container. Allows your job definitions to reference the secret by the environment variable name defined in this property. Default: - no secrets
        :param user: (experimental) The user name to use inside the container. Default: - no user
        :param volumes: (experimental) The volumes to mount to this container. Automatically added to the job definition. Default: - no volumes
        :param assign_public_ip: (experimental) Indicates whether the job has a public IP address. For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet. Default: false
        :param ephemeral_storage_size: (experimental) The size for ephemeral storage. Default: - 20 GiB
        :param fargate_platform_version: (experimental) Which version of Fargate to use when running this container. Default: LATEST

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_ecs as ecs
            from aws_cdk import aws_iam as iam
            
            # container_image: ecs.ContainerImage
            # ecs_volume: batch_alpha.EcsVolume
            # linux_parameters: batch_alpha.LinuxParameters
            # log_driver: ecs.LogDriver
            # role: iam.Role
            # secret: batch_alpha.Secret
            # size: cdk.Size
            
            ecs_fargate_container_definition_props = batch_alpha.EcsFargateContainerDefinitionProps(
                cpu=123,
                image=container_image,
                memory=size,
            
                # the properties below are optional
                assign_public_ip=False,
                command=["command"],
                environment={
                    "environment_key": "environment"
                },
                ephemeral_storage_size=size,
                execution_role=role,
                fargate_platform_version=ecs.FargatePlatformVersion.LATEST,
                job_role=role,
                linux_parameters=linux_parameters,
                logging=log_driver,
                readonly_root_filesystem=False,
                secrets={
                    "secrets_key": secret
                },
                user="user",
                volumes=[ecs_volume]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be426e0524ddb478956358b5434c99110733179aba3a389f8413804be7910e5f)
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument job_role", value=job_role, expected_type=type_hints["job_role"])
            check_type(argname="argument linux_parameters", value=linux_parameters, expected_type=type_hints["linux_parameters"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
            check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument fargate_platform_version", value=fargate_platform_version, expected_type=type_hints["fargate_platform_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cpu": cpu,
            "image": image,
            "memory": memory,
        }
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if job_role is not None:
            self._values["job_role"] = job_role
        if linux_parameters is not None:
            self._values["linux_parameters"] = linux_parameters
        if logging is not None:
            self._values["logging"] = logging
        if readonly_root_filesystem is not None:
            self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if secrets is not None:
            self._values["secrets"] = secrets
        if user is not None:
            self._values["user"] = user
        if volumes is not None:
            self._values["volumes"] = volumes
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if fargate_platform_version is not None:
            self._values["fargate_platform_version"] = fargate_platform_version

    @builtins.property
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        assert result is not None, "Required property 'cpu' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, result)

    @builtins.property
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        result = self._values.get("memory")
        assert result is not None, "Required property 'memory' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Size, result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :default: - no command

        :see: https://docs.docker.com/engine/reference/builder/#cmd
        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :default: - a Role will be created

        :see: https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html
        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :default: - no job role

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
        :stability: experimental
        '''
        result = self._values.get("job_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("linux_parameters")
        return typing.cast(typing.Optional["LinuxParameters"], result)

    @builtins.property
    def logging(self) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver]:
        '''(experimental) The loging configuration for this Job.

        :default: - the log configuration of the Docker daemon

        :stability: experimental
        '''
        result = self._values.get("logging")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver], result)

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly_root_filesystem")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :default: - no secrets

        :see: https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html
        :stability: experimental
        '''
        result = self._values.get("secrets")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Secret"]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :default: - no user

        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["EcsVolume"]]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :default: - no volumes

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List["EcsVolume"]], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the job has a public IP address.

        For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet
        (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet.

        :default: false

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html
        :stability: experimental
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The size for ephemeral storage.

        :default: - 20 GiB

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def fargate_platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion]:
        '''(experimental) Which version of Fargate to use when running this container.

        :default: LATEST

        :stability: experimental
        '''
        result = self._values.get("fargate_platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsFargateContainerDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EcsMachineImage",
    jsii_struct_bases=[],
    name_mapping={"image": "image", "image_type": "imageType"},
)
class EcsMachineImage:
    def __init__(
        self,
        *,
        image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        image_type: typing.Optional["EcsMachineImageType"] = None,
    ) -> None:
        '''(experimental) A Batch MachineImage that is compatible with ECS.

        :param image: (experimental) The machine image to use. Default: - chosen by batch
        :param image_type: (experimental) Tells Batch which instance type to launch this image on. Default: - 'ECS_AL2' for non-gpu instances, 'ECS_AL2_NVIDIA' for gpu instances

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # machine_image: ec2.IMachineImage
            
            ecs_machine_image = batch_alpha.EcsMachineImage(
                image=machine_image,
                image_type=batch_alpha.EcsMachineImageType.ECS_AL2
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37d05bed1d068747e454278ee23635b90274054dd119a14ca87ecd86b87fbcb7)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image is not None:
            self._values["image"] = image
        if image_type is not None:
            self._values["image_type"] = image_type

    @builtins.property
    def image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''(experimental) The machine image to use.

        :default: - chosen by batch

        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def image_type(self) -> typing.Optional["EcsMachineImageType"]:
        '''(experimental) Tells Batch which instance type to launch this image on.

        :default: - 'ECS_AL2' for non-gpu instances, 'ECS_AL2_NVIDIA' for gpu instances

        :stability: experimental
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional["EcsMachineImageType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsMachineImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.EcsMachineImageType")
class EcsMachineImageType(enum.Enum):
    '''(experimental) Maps the image to instance types.

    :stability: experimental
    '''

    ECS_AL2 = "ECS_AL2"
    '''(experimental) Tells Batch that this machine image runs on non-GPU instances.

    :stability: experimental
    '''
    ECS_AL2_NVIDIA = "ECS_AL2_NVIDIA"
    '''(experimental) Tells Batch that this machine image runs on GPU instances.

    :stability: experimental
    '''


class EcsVolume(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-batch-alpha.EcsVolume",
):
    '''(experimental) Represents a Volume that can be mounted to a container that uses ECS.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        import aws_cdk.aws_iam as iam
        import aws_cdk.aws_efs as efs
        
        # my_file_system: efs.IFileSystem
        # my_job_role: iam.Role
        
        my_file_system.grant_read(my_job_role)
        
        job_defn = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256,
                volumes=[batch.EcsVolume.efs(
                    name="myVolume",
                    file_system=my_file_system,
                    container_path="/Volumes/myVolume",
                    use_job_role=True
                )],
                job_role=my_job_role
            )
        )
    '''

    def __init__(
        self,
        *,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false

        :stability: experimental
        '''
        options = EcsVolumeOptions(
            container_path=container_path, name=name, readonly=readonly
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="efs")
    @builtins.classmethod
    def efs(
        cls,
        *,
        file_system: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
        access_point_id: typing.Optional[builtins.str] = None,
        enable_transit_encryption: typing.Optional[builtins.bool] = None,
        root_directory: typing.Optional[builtins.str] = None,
        transit_encryption_port: typing.Optional[jsii.Number] = None,
        use_job_role: typing.Optional[builtins.bool] = None,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> "EfsVolume":
        '''(experimental) Creates a Volume that uses an AWS Elastic File System (EFS);

        this volume can grow and shrink as needed

        :param file_system: (experimental) The EFS File System that supports this volume.
        :param access_point_id: (experimental) The Amazon EFS access point ID to use. If an access point is specified, ``rootDirectory`` must either be omitted or set to ``/`` which enforces the path set on the EFS access point. If an access point is used, ``enableTransitEncryption`` must be ``true``. Default: - no accessPointId
        :param enable_transit_encryption: (experimental) Enables encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server. Default: false
        :param root_directory: (experimental) The directory within the Amazon EFS file system to mount as the root directory inside the host. If this parameter is omitted, the root of the Amazon EFS volume is used instead. Specifying ``/`` has the same effect as omitting this parameter. The maximum length is 4,096 characters. Default: - root of the EFS File System
        :param transit_encryption_port: (experimental) The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server. The value must be between 0 and 65,535. Default: - chosen by the EFS Mount Helper
        :param use_job_role: (experimental) Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system. If specified, ``enableTransitEncryption`` must be ``true``. Default: false
        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html
        :stability: experimental
        '''
        options = EfsVolumeOptions(
            file_system=file_system,
            access_point_id=access_point_id,
            enable_transit_encryption=enable_transit_encryption,
            root_directory=root_directory,
            transit_encryption_port=transit_encryption_port,
            use_job_role=use_job_role,
            container_path=container_path,
            name=name,
            readonly=readonly,
        )

        return typing.cast("EfsVolume", jsii.sinvoke(cls, "efs", [options]))

    @jsii.member(jsii_name="host")
    @builtins.classmethod
    def host(
        cls,
        *,
        host_path: typing.Optional[builtins.str] = None,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> "HostVolume":
        '''(experimental) Creates a Host volume.

        This volume will persist on the host at the specified ``hostPath``.
        If the ``hostPath`` is not specified, Docker will choose the host path. In this case,
        the data may not persist after the containers that use it stop running.

        :param host_path: (experimental) The path on the host machine this container will have access to. Default: - Docker will choose the host path. The data may not persist after the containers that use it stop running.
        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false

        :stability: experimental
        '''
        options = HostVolumeOptions(
            host_path=host_path,
            container_path=container_path,
            name=name,
            readonly=readonly,
        )

        return typing.cast("HostVolume", jsii.sinvoke(cls, "host", [options]))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path on the container that this volume will be mounted to.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this volume.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="readonly")
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the container has readonly access to this volume.

        :default: false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonly"))


class _EcsVolumeProxy(EcsVolume):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, EcsVolume).__jsii_proxy_class__ = lambda : _EcsVolumeProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EcsVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={
        "container_path": "containerPath",
        "name": "name",
        "readonly": "readonly",
    },
)
class EcsVolumeOptions:
    def __init__(
        self,
        *,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options to configure an EcsVolume.

        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            ecs_volume_options = batch_alpha.EcsVolumeOptions(
                container_path="containerPath",
                name="name",
            
                # the properties below are optional
                readonly=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fd9bd77e01b20e461eaba782d1cbae004ef85d44e3c0078ed6702ded4e4da8)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_path": container_path,
            "name": name,
        }
        if readonly is not None:
            self._values["readonly"] = readonly

    @builtins.property
    def container_path(self) -> builtins.str:
        '''(experimental) the path on the container where this volume is mounted.

        :stability: experimental
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name of this volume.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if set, the container will have readonly access to the volume.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EfsVolume(
    EcsVolume,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EfsVolume",
):
    '''(experimental) A Volume that uses an AWS Elastic File System (EFS);

    this volume can grow and shrink as needed

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        from aws_cdk import aws_efs as efs
        
        # file_system: efs.FileSystem
        
        efs_volume = batch_alpha.EfsVolume(
            container_path="containerPath",
            file_system=file_system,
            name="name",
        
            # the properties below are optional
            access_point_id="accessPointId",
            enable_transit_encryption=False,
            readonly=False,
            root_directory="rootDirectory",
            transit_encryption_port=123,
            use_job_role=False
        )
    '''

    def __init__(
        self,
        *,
        file_system: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
        access_point_id: typing.Optional[builtins.str] = None,
        enable_transit_encryption: typing.Optional[builtins.bool] = None,
        root_directory: typing.Optional[builtins.str] = None,
        transit_encryption_port: typing.Optional[jsii.Number] = None,
        use_job_role: typing.Optional[builtins.bool] = None,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param file_system: (experimental) The EFS File System that supports this volume.
        :param access_point_id: (experimental) The Amazon EFS access point ID to use. If an access point is specified, ``rootDirectory`` must either be omitted or set to ``/`` which enforces the path set on the EFS access point. If an access point is used, ``enableTransitEncryption`` must be ``true``. Default: - no accessPointId
        :param enable_transit_encryption: (experimental) Enables encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server. Default: false
        :param root_directory: (experimental) The directory within the Amazon EFS file system to mount as the root directory inside the host. If this parameter is omitted, the root of the Amazon EFS volume is used instead. Specifying ``/`` has the same effect as omitting this parameter. The maximum length is 4,096 characters. Default: - root of the EFS File System
        :param transit_encryption_port: (experimental) The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server. The value must be between 0 and 65,535. Default: - chosen by the EFS Mount Helper
        :param use_job_role: (experimental) Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system. If specified, ``enableTransitEncryption`` must be ``true``. Default: false
        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false

        :stability: experimental
        '''
        options = EfsVolumeOptions(
            file_system=file_system,
            access_point_id=access_point_id,
            enable_transit_encryption=enable_transit_encryption,
            root_directory=root_directory,
            transit_encryption_port=transit_encryption_port,
            use_job_role=use_job_role,
            container_path=container_path,
            name=name,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isEfsVolume")
    @builtins.classmethod
    def is_efs_volume(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Returns true if x is an EfsVolume, false otherwise.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7c12ad3e540e49a03aad69b7d890b94cca310d933180c6f73bccbbd1509fffc)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isEfsVolume", [x]))

    @builtins.property
    @jsii.member(jsii_name="fileSystem")
    def file_system(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''(experimental) The EFS File System that supports this volume.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IFileSystem, jsii.get(self, "fileSystem"))

    @builtins.property
    @jsii.member(jsii_name="accessPointId")
    def access_point_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Amazon EFS access point ID to use.

        If an access point is specified, ``rootDirectory`` must either be omitted or set to ``/``
        which enforces the path set on the EFS access point.
        If an access point is used, ``enableTransitEncryption`` must be ``true``.

        :default: - no accessPointId

        :see: https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessPointId"))

    @builtins.property
    @jsii.member(jsii_name="enableTransitEncryption")
    def enable_transit_encryption(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server.

        :default: false

        :see: https://docs.aws.amazon.com/efs/latest/ug/encryption-in-transit.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enableTransitEncryption"))

    @builtins.property
    @jsii.member(jsii_name="rootDirectory")
    def root_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory within the Amazon EFS file system to mount as the root directory inside the host.

        If this parameter is omitted, the root of the Amazon EFS volume is used instead.
        Specifying ``/`` has the same effect as omitting this parameter.
        The maximum length is 4,096 characters.

        :default: - root of the EFS File System

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rootDirectory"))

    @builtins.property
    @jsii.member(jsii_name="transitEncryptionPort")
    def transit_encryption_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server.

        The value must be between 0 and 65,535.

        :default: - chosen by the EFS Mount Helper

        :see: https://docs.aws.amazon.com/efs/latest/ug/efs-mount-helper.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "transitEncryptionPort"))

    @builtins.property
    @jsii.member(jsii_name="useJobRole")
    def use_job_role(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system.

        If specified, ``enableTransitEncryption`` must be ``true``.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html#efs-volume-accesspoints
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useJobRole"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EfsVolumeOptions",
    jsii_struct_bases=[EcsVolumeOptions],
    name_mapping={
        "container_path": "containerPath",
        "name": "name",
        "readonly": "readonly",
        "file_system": "fileSystem",
        "access_point_id": "accessPointId",
        "enable_transit_encryption": "enableTransitEncryption",
        "root_directory": "rootDirectory",
        "transit_encryption_port": "transitEncryptionPort",
        "use_job_role": "useJobRole",
    },
)
class EfsVolumeOptions(EcsVolumeOptions):
    def __init__(
        self,
        *,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
        file_system: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
        access_point_id: typing.Optional[builtins.str] = None,
        enable_transit_encryption: typing.Optional[builtins.bool] = None,
        root_directory: typing.Optional[builtins.str] = None,
        transit_encryption_port: typing.Optional[jsii.Number] = None,
        use_job_role: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for configuring an EfsVolume.

        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false
        :param file_system: (experimental) The EFS File System that supports this volume.
        :param access_point_id: (experimental) The Amazon EFS access point ID to use. If an access point is specified, ``rootDirectory`` must either be omitted or set to ``/`` which enforces the path set on the EFS access point. If an access point is used, ``enableTransitEncryption`` must be ``true``. Default: - no accessPointId
        :param enable_transit_encryption: (experimental) Enables encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server. Default: false
        :param root_directory: (experimental) The directory within the Amazon EFS file system to mount as the root directory inside the host. If this parameter is omitted, the root of the Amazon EFS volume is used instead. Specifying ``/`` has the same effect as omitting this parameter. The maximum length is 4,096 characters. Default: - root of the EFS File System
        :param transit_encryption_port: (experimental) The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server. The value must be between 0 and 65,535. Default: - chosen by the EFS Mount Helper
        :param use_job_role: (experimental) Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system. If specified, ``enableTransitEncryption`` must be ``true``. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            import aws_cdk.aws_iam as iam
            import aws_cdk.aws_efs as efs
            
            # my_file_system: efs.IFileSystem
            # my_job_role: iam.Role
            
            my_file_system.grant_read(my_job_role)
            
            job_defn = batch.EcsJobDefinition(self, "JobDefn",
                container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                    image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                    memory=cdk.Size.mebibytes(2048),
                    cpu=256,
                    volumes=[batch.EcsVolume.efs(
                        name="myVolume",
                        file_system=my_file_system,
                        container_path="/Volumes/myVolume",
                        use_job_role=True
                    )],
                    job_role=my_job_role
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dba797b8199f276971c1302f225db8c50004625e7296aefe6f59eb993ad3784)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument file_system", value=file_system, expected_type=type_hints["file_system"])
            check_type(argname="argument access_point_id", value=access_point_id, expected_type=type_hints["access_point_id"])
            check_type(argname="argument enable_transit_encryption", value=enable_transit_encryption, expected_type=type_hints["enable_transit_encryption"])
            check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
            check_type(argname="argument transit_encryption_port", value=transit_encryption_port, expected_type=type_hints["transit_encryption_port"])
            check_type(argname="argument use_job_role", value=use_job_role, expected_type=type_hints["use_job_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_path": container_path,
            "name": name,
            "file_system": file_system,
        }
        if readonly is not None:
            self._values["readonly"] = readonly
        if access_point_id is not None:
            self._values["access_point_id"] = access_point_id
        if enable_transit_encryption is not None:
            self._values["enable_transit_encryption"] = enable_transit_encryption
        if root_directory is not None:
            self._values["root_directory"] = root_directory
        if transit_encryption_port is not None:
            self._values["transit_encryption_port"] = transit_encryption_port
        if use_job_role is not None:
            self._values["use_job_role"] = use_job_role

    @builtins.property
    def container_path(self) -> builtins.str:
        '''(experimental) the path on the container where this volume is mounted.

        :stability: experimental
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name of this volume.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if set, the container will have readonly access to the volume.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def file_system(self) -> _aws_cdk_aws_efs_ceddda9d.IFileSystem:
        '''(experimental) The EFS File System that supports this volume.

        :stability: experimental
        '''
        result = self._values.get("file_system")
        assert result is not None, "Required property 'file_system' is missing"
        return typing.cast(_aws_cdk_aws_efs_ceddda9d.IFileSystem, result)

    @builtins.property
    def access_point_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Amazon EFS access point ID to use.

        If an access point is specified, ``rootDirectory`` must either be omitted or set to ``/``
        which enforces the path set on the EFS access point.
        If an access point is used, ``enableTransitEncryption`` must be ``true``.

        :default: - no accessPointId

        :see: https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html
        :stability: experimental
        '''
        result = self._values.get("access_point_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_transit_encryption(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server.

        :default: false

        :see: https://docs.aws.amazon.com/efs/latest/ug/encryption-in-transit.html
        :stability: experimental
        '''
        result = self._values.get("enable_transit_encryption")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory within the Amazon EFS file system to mount as the root directory inside the host.

        If this parameter is omitted, the root of the Amazon EFS volume is used instead.
        Specifying ``/`` has the same effect as omitting this parameter.
        The maximum length is 4,096 characters.

        :default: - root of the EFS File System

        :stability: experimental
        '''
        result = self._values.get("root_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def transit_encryption_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server.

        The value must be between 0 and 65,535.

        :default: - chosen by the EFS Mount Helper

        :see: https://docs.aws.amazon.com/efs/latest/ug/efs-mount-helper.html
        :stability: experimental
        '''
        result = self._values.get("transit_encryption_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_job_role(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system.

        If specified, ``enableTransitEncryption`` must be ``true``.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html#efs-volume-accesspoints
        :stability: experimental
        '''
        result = self._values.get("use_job_role")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EfsVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EksContainerDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "args": "args",
        "command": "command",
        "cpu_limit": "cpuLimit",
        "cpu_reservation": "cpuReservation",
        "env": "env",
        "gpu_limit": "gpuLimit",
        "gpu_reservation": "gpuReservation",
        "image_pull_policy": "imagePullPolicy",
        "memory_limit": "memoryLimit",
        "memory_reservation": "memoryReservation",
        "name": "name",
        "privileged": "privileged",
        "readonly_root_filesystem": "readonlyRootFilesystem",
        "run_as_group": "runAsGroup",
        "run_as_root": "runAsRoot",
        "run_as_user": "runAsUser",
        "volumes": "volumes",
    },
)
class EksContainerDefinitionProps:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu_limit: typing.Optional[jsii.Number] = None,
        cpu_reservation: typing.Optional[jsii.Number] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        gpu_limit: typing.Optional[jsii.Number] = None,
        gpu_reservation: typing.Optional[jsii.Number] = None,
        image_pull_policy: typing.Optional["ImagePullPolicy"] = None,
        memory_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        memory_reservation: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        name: typing.Optional[builtins.str] = None,
        privileged: typing.Optional[builtins.bool] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        run_as_group: typing.Optional[jsii.Number] = None,
        run_as_root: typing.Optional[builtins.bool] = None,
        run_as_user: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Sequence["EksVolume"]] = None,
    ) -> None:
        '''(experimental) Props to configure an EksContainerDefinition.

        :param image: (experimental) The image that this container will run.
        :param args: (experimental) An array of arguments to the entrypoint. If this isn't specified, the CMD of the container image is used. This corresponds to the args member in the Entrypoint portion of the Pod in Kubernetes. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to "$(NAME1)" and the NAME1 environment variable doesn't exist, the command string will remain "$(NAME1)." $$ is replaced with $, and the resulting string isn't expanded. or example, $$(VAR_NAME) is passed as $(VAR_NAME) whether or not the VAR_NAME environment variable exists. Default: - no args
        :param command: (experimental) The entrypoint for the container. This isn't run within a shell. If this isn't specified, the ``ENTRYPOINT`` of the container image is used. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to ``"$(NAME1)"`` and the ``NAME1`` environment variable doesn't exist, the command string will remain ``"$(NAME1)."`` ``$$`` is replaced with ``$`` and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. The entrypoint can't be updated. Default: - no command
        :param cpu_limit: (experimental) The hard limit of CPUs to present to this container. Must be an even multiple of 0.25. If your container attempts to exceed this limit, it will be terminated. At least one of ``cpuReservation`` and ``cpuLimit`` is required. If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``. Default: - No CPU limit
        :param cpu_reservation: (experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25. The container will given at least this many CPUs, but may consume more. At least one of ``cpuReservation`` and ``cpuLimit`` is required. If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``. Default: - No CPUs reserved
        :param env: (experimental) The environment variables to pass to this container. *Note*: Environment variables cannot start with "AWS_BATCH". This naming convention is reserved for variables that AWS Batch sets. Default: - no environment variables
        :param gpu_limit: (experimental) The hard limit of GPUs to present to this container. If your container attempts to exceed this limit, it will be terminated. If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``. Default: - No GPU limit
        :param gpu_reservation: (experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25. The container will given at least this many CPUs, but may consume more. If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``. Default: - No GPUs reserved
        :param image_pull_policy: (experimental) The image pull policy for this container. Default: - ``ALWAYS`` if the ``:latest`` tag is specified, ``IF_NOT_PRESENT`` otherwise
        :param memory_limit: (experimental) The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, it will be terminated. Must be larger that 4 MiB At least one of ``memoryLimit`` and ``memoryReservation`` is required *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible for the specific instance type that you are using. Default: - No memory limit
        :param memory_reservation: (experimental) The soft limit (in MiB) of memory to reserve for the container. Your container will be given at least this much memory, but may consume more. Must be larger that 4 MiB When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of ``memoryLimit`` and ``memoryReservation`` is required. If both are specified, then ``memoryLimit`` must be equal to ``memoryReservation`` *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible for the specific instance type that you are using. Default: - No memory reserved
        :param name: (experimental) The name of this container. Default: : ``'Default'``
        :param privileged: (experimental) If specified, gives this container elevated permissions on the host container instance. The level of permissions are similar to the root user permissions. This parameter maps to ``privileged`` policy in the Privileged pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: false
        :param readonly_root_filesystem: (experimental) If specified, gives this container readonly access to its root file system. This parameter maps to ``ReadOnlyRootFilesystem`` policy in the Volumes and file systems pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: false
        :param run_as_group: (experimental) If specified, the container is run as the specified group ID (``gid``). If this parameter isn't specified, the default is the group that's specified in the image metadata. This parameter maps to ``RunAsGroup`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: none
        :param run_as_root: (experimental) If specified, the container is run as a user with a ``uid`` other than 0. Otherwise, no such rule is enforced. This parameter maps to ``RunAsUser`` and ``MustRunAsNonRoot`` policy in the Users and groups pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: - the container is *not* required to run as a non-root user
        :param run_as_user: (experimental) If specified, this container is run as the specified user ID (``uid``). This parameter maps to ``RunAsUser`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: - the user that is specified in the image metadata.
        :param volumes: (experimental) The Volumes to mount to this container. Automatically added to the Pod. Default: - no volumes

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            job_defn = batch.EksJobDefinition(self, "eksf2",
                container=batch.EksContainerDefinition(self, "container",
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    volumes=[batch.EksVolume.empty_dir(
                        name="myEmptyDirVolume",
                        mount_path="/mount/path",
                        medium=batch.EmptyDirMediumType.MEMORY,
                        readonly=True,
                        size_limit=cdk.Size.mebibytes(2048)
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53410c93d882935ca1283d4cc21ef161d31335c97183c177d91ee29a54213aa)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument cpu_limit", value=cpu_limit, expected_type=type_hints["cpu_limit"])
            check_type(argname="argument cpu_reservation", value=cpu_reservation, expected_type=type_hints["cpu_reservation"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument gpu_limit", value=gpu_limit, expected_type=type_hints["gpu_limit"])
            check_type(argname="argument gpu_reservation", value=gpu_reservation, expected_type=type_hints["gpu_reservation"])
            check_type(argname="argument image_pull_policy", value=image_pull_policy, expected_type=type_hints["image_pull_policy"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
            check_type(argname="argument memory_reservation", value=memory_reservation, expected_type=type_hints["memory_reservation"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
            check_type(argname="argument run_as_group", value=run_as_group, expected_type=type_hints["run_as_group"])
            check_type(argname="argument run_as_root", value=run_as_root, expected_type=type_hints["run_as_root"])
            check_type(argname="argument run_as_user", value=run_as_user, expected_type=type_hints["run_as_user"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if args is not None:
            self._values["args"] = args
        if command is not None:
            self._values["command"] = command
        if cpu_limit is not None:
            self._values["cpu_limit"] = cpu_limit
        if cpu_reservation is not None:
            self._values["cpu_reservation"] = cpu_reservation
        if env is not None:
            self._values["env"] = env
        if gpu_limit is not None:
            self._values["gpu_limit"] = gpu_limit
        if gpu_reservation is not None:
            self._values["gpu_reservation"] = gpu_reservation
        if image_pull_policy is not None:
            self._values["image_pull_policy"] = image_pull_policy
        if memory_limit is not None:
            self._values["memory_limit"] = memory_limit
        if memory_reservation is not None:
            self._values["memory_reservation"] = memory_reservation
        if name is not None:
            self._values["name"] = name
        if privileged is not None:
            self._values["privileged"] = privileged
        if readonly_root_filesystem is not None:
            self._values["readonly_root_filesystem"] = readonly_root_filesystem
        if run_as_group is not None:
            self._values["run_as_group"] = run_as_group
        if run_as_root is not None:
            self._values["run_as_root"] = run_as_root
        if run_as_user is not None:
            self._values["run_as_user"] = run_as_user
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, result)

    @builtins.property
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of arguments to the entrypoint.

        If this isn't specified, the CMD of the container image is used.
        This corresponds to the args member in the Entrypoint portion of the Pod in Kubernetes.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to "$(NAME1)" and the NAME1 environment variable doesn't exist,
        the command string will remain "$(NAME1)." $$ is replaced with $, and the resulting string isn't expanded.
        or example, $$(VAR_NAME) is passed as $(VAR_NAME) whether or not the VAR_NAME environment variable exists.

        :default: - no args

        :see: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/
        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The entrypoint for the container.

        This isn't run within a shell.
        If this isn't specified, the ``ENTRYPOINT`` of the container image is used.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to ``"$(NAME1)"`` and the ``NAME1`` environment variable doesn't exist,
        the command string will remain ``"$(NAME1)."`` ``$$`` is replaced with ``$`` and the resulting string isn't expanded.
        For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists.

        The entrypoint can't be updated.

        :default: - no command

        :see: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint
        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of CPUs to present to this container. Must be an even multiple of 0.25.

        If your container attempts to exceed this limit, it will be terminated.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :default: - No CPU limit

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        result = self._values.get("cpu_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def cpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :default: - No CPUs reserved

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        result = self._values.get("cpu_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to this container.

        *Note*: Environment variables cannot start with "AWS_BATCH".
        This naming convention is reserved for variables that AWS Batch sets.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def gpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of GPUs to present to this container.

        If your container attempts to exceed this limit, it will be terminated.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :default: - No GPU limit

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        result = self._values.get("gpu_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def gpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :default: - No GPUs reserved

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        result = self._values.get("gpu_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def image_pull_policy(self) -> typing.Optional["ImagePullPolicy"]:
        '''(experimental) The image pull policy for this container.

        :default: - ``ALWAYS`` if the ``:latest`` tag is specified, ``IF_NOT_PRESENT`` otherwise

        :see: https://kubernetes.io/docs/concepts/containers/images/#updating-images
        :stability: experimental
        '''
        result = self._values.get("image_pull_policy")
        return typing.cast(typing.Optional["ImagePullPolicy"], result)

    @builtins.property
    def memory_limit(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, it will be terminated.

        Must be larger that 4 MiB

        At least one of ``memoryLimit`` and ``memoryReservation`` is required

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :default: - No memory limit

        :see: https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html
        :stability: experimental
        '''
        result = self._values.get("memory_limit")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def memory_reservation(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        Your container will be given at least this much memory, but may consume more.

        Must be larger that 4 MiB

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of ``memoryLimit`` and ``memoryReservation`` is required.
        If both are specified, then ``memoryLimit`` must be equal to ``memoryReservation``

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :default: - No memory reserved

        :see: https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html
        :stability: experimental
        '''
        result = self._values.get("memory_reservation")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this container.

        :default: : ``'Default'``

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container elevated permissions on the host container instance.

        The level of permissions are similar to the root user permissions.

        This parameter maps to ``privileged`` policy in the Privileged pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: false

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#volumes-and-file-systems
        :stability: experimental
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container readonly access to its root file system.

        This parameter maps to ``ReadOnlyRootFilesystem`` policy in the Volumes and file systems pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: false

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#volumes-and-file-systems
        :stability: experimental
        '''
        result = self._values.get("readonly_root_filesystem")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def run_as_group(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, the container is run as the specified group ID (``gid``).

        If this parameter isn't specified, the default is the group that's specified in the image metadata.
        This parameter maps to ``RunAsGroup`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: none

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        result = self._values.get("run_as_group")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def run_as_root(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container is run as a user with a ``uid`` other than 0.

        Otherwise, no such rule is enforced.
        This parameter maps to ``RunAsUser`` and ``MustRunAsNonRoot`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: - the container is *not* required to run as a non-root user

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        result = self._values.get("run_as_root")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def run_as_user(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, this container is run as the specified user ID (``uid``).

        This parameter maps to ``RunAsUser`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: - the user that is specified in the image metadata.

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        result = self._values.get("run_as_user")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List["EksVolume"]]:
        '''(experimental) The Volumes to mount to this container.

        Automatically added to the Pod.

        :default: - no volumes

        :see: https://kubernetes.io/docs/concepts/storage/volumes/
        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List["EksVolume"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksContainerDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EksMachineImage",
    jsii_struct_bases=[],
    name_mapping={"image": "image", "image_type": "imageType"},
)
class EksMachineImage:
    def __init__(
        self,
        *,
        image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
        image_type: typing.Optional["EksMachineImageType"] = None,
    ) -> None:
        '''(experimental) A Batch MachineImage that is compatible with EKS.

        :param image: (experimental) The machine image to use. Default: - chosen by batch
        :param image_type: (experimental) Tells Batch which instance type to launch this image on. Default: - 'EKS_AL2' for non-gpu instances, 'EKS_AL2_NVIDIA' for gpu instances

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            from aws_cdk import aws_ec2 as ec2
            
            # machine_image: ec2.IMachineImage
            
            eks_machine_image = batch_alpha.EksMachineImage(
                image=machine_image,
                image_type=batch_alpha.EksMachineImageType.EKS_AL2
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__217985092c1dc6208d9a3e5925aa7eef933f9d780c17b631d53280fad572ecd5)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if image is not None:
            self._values["image"] = image
        if image_type is not None:
            self._values["image_type"] = image_type

    @builtins.property
    def image(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage]:
        '''(experimental) The machine image to use.

        :default: - chosen by batch

        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage], result)

    @builtins.property
    def image_type(self) -> typing.Optional["EksMachineImageType"]:
        '''(experimental) Tells Batch which instance type to launch this image on.

        :default: - 'EKS_AL2' for non-gpu instances, 'EKS_AL2_NVIDIA' for gpu instances

        :stability: experimental
        '''
        result = self._values.get("image_type")
        return typing.cast(typing.Optional["EksMachineImageType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksMachineImage(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.EksMachineImageType")
class EksMachineImageType(enum.Enum):
    '''(experimental) Maps the image to instance types.

    :stability: experimental
    '''

    EKS_AL2 = "EKS_AL2"
    '''(experimental) Tells Batch that this machine image runs on non-GPU instances.

    :stability: experimental
    '''
    EKS_AL2_NVIDIA = "EKS_AL2_NVIDIA"
    '''(experimental) Tells Batch that this machine image runs on GPU instances.

    :stability: experimental
    '''


class EksVolume(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-batch-alpha.EksVolume",
):
    '''(experimental) A Volume that can be mounted to a container supported by EKS.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        job_defn = batch.EksJobDefinition(self, "eksf2",
            container=batch.EksContainerDefinition(self, "container",
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                volumes=[batch.EksVolume.empty_dir(
                    name="myEmptyDirVolume",
                    mount_path="/mount/path",
                    medium=batch.EmptyDirMediumType.MEMORY,
                    readonly=True,
                    size_limit=cdk.Size.mebibytes(2048)
                )]
            )
        )
    '''

    def __init__(
        self,
        *,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :stability: experimental
        '''
        options = EksVolumeOptions(name=name, mount_path=mount_path, readonly=readonly)

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="emptyDir")
    @builtins.classmethod
    def empty_dir(
        cls,
        *,
        medium: typing.Optional["EmptyDirMediumType"] = None,
        size_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> "EmptyDirVolume":
        '''(experimental) Creates a Kubernetes EmptyDir volume.

        :param medium: (experimental) The storage type to use for this Volume. Default: ``EmptyDirMediumType.DISK``
        :param size_limit: (experimental) The maximum size for this Volume. Default: - no size limit
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir
        :stability: experimental
        '''
        options = EmptyDirVolumeOptions(
            medium=medium,
            size_limit=size_limit,
            name=name,
            mount_path=mount_path,
            readonly=readonly,
        )

        return typing.cast("EmptyDirVolume", jsii.sinvoke(cls, "emptyDir", [options]))

    @jsii.member(jsii_name="hostPath")
    @builtins.classmethod
    def host_path(
        cls,
        *,
        host_path: builtins.str,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> "HostPathVolume":
        '''(experimental) Creates a Kubernetes HostPath volume.

        :param host_path: (experimental) The path of the file or directory on the host to mount into containers on the pod. *Note*: HothPath Volumes present many security risks, and should be avoided when possible.
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
        :stability: experimental
        '''
        options = HostPathVolumeOptions(
            host_path=host_path, name=name, mount_path=mount_path, readonly=readonly
        )

        return typing.cast("HostPathVolume", jsii.sinvoke(cls, "hostPath", [options]))

    @jsii.member(jsii_name="secret")
    @builtins.classmethod
    def secret(
        cls,
        *,
        secret_name: builtins.str,
        optional: typing.Optional[builtins.bool] = None,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> "SecretPathVolume":
        '''(experimental) Creates a Kubernetes Secret volume.

        :param secret_name: (experimental) The name of the secret. Must be a valid DNS subdomain name.
        :param optional: (experimental) Specifies whether the secret or the secret's keys must be defined. Default: true
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#secret
        :stability: experimental
        '''
        options = SecretPathVolumeOptions(
            secret_name=secret_name,
            optional=optional,
            name=name,
            mount_path=mount_path,
            readonly=readonly,
        )

        return typing.cast("SecretPathVolume", jsii.sinvoke(cls, "secret", [options]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''(experimental) The name of this volume.

        The name must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the container where the container is mounted.

        :default: - the container is not mounted

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerPath"))

    @builtins.property
    @jsii.member(jsii_name="readonly")
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container has readonly access to the volume.

        Otherwise, the container has read/write access.

        :default: false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonly"))


class _EksVolumeProxy(EksVolume):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, EksVolume).__jsii_proxy_class__ = lambda : _EksVolumeProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EksVolumeOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "mount_path": "mountPath", "readonly": "readonly"},
)
class EksVolumeOptions:
    def __init__(
        self,
        *,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options to configure an EksVolume.

        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            eks_volume_options = batch_alpha.EksVolumeOptions(
                name="name",
            
                # the properties below are optional
                mount_path="mountPath",
                readonly=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79d1e28c8c37196461f6b4f63eef2cd8dff26b0545ab1962d0367ee18b09dd42)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if mount_path is not None:
            self._values["mount_path"] = mount_path
        if readonly is not None:
            self._values["readonly"] = readonly

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of this volume.

        The name must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the container where the volume is mounted.

        :default: - the volume is not mounted

        :stability: experimental
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container has readonly access to the volume.

        Otherwise, the container has read/write access.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.EmptyDirMediumType")
class EmptyDirMediumType(enum.Enum):
    '''(experimental) What medium the volume will live in.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        job_defn = batch.EksJobDefinition(self, "eksf2",
            container=batch.EksContainerDefinition(self, "container",
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                volumes=[batch.EksVolume.empty_dir(
                    name="myEmptyDirVolume",
                    mount_path="/mount/path",
                    medium=batch.EmptyDirMediumType.MEMORY,
                    readonly=True,
                    size_limit=cdk.Size.mebibytes(2048)
                )]
            )
        )
    '''

    DISK = "DISK"
    '''(experimental) Use the disk storage of the node.

    Items written here will survive node reboots.

    :stability: experimental
    '''
    MEMORY = "MEMORY"
    '''(experimental) Use the ``tmpfs`` volume that is backed by RAM of the node.

    Items written here will *not* survive node reboots.

    :stability: experimental
    '''


class EmptyDirVolume(
    EksVolume,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EmptyDirVolume",
):
    '''(experimental) A Kubernetes EmptyDir volume.

    :see: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        import aws_cdk as cdk
        
        # size: cdk.Size
        
        empty_dir_volume = batch_alpha.EmptyDirVolume(
            name="name",
        
            # the properties below are optional
            medium=batch_alpha.EmptyDirMediumType.DISK,
            mount_path="mountPath",
            readonly=False,
            size_limit=size
        )
    '''

    def __init__(
        self,
        *,
        medium: typing.Optional[EmptyDirMediumType] = None,
        size_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param medium: (experimental) The storage type to use for this Volume. Default: ``EmptyDirMediumType.DISK``
        :param size_limit: (experimental) The maximum size for this Volume. Default: - no size limit
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :stability: experimental
        '''
        options = EmptyDirVolumeOptions(
            medium=medium,
            size_limit=size_limit,
            name=name,
            mount_path=mount_path,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isEmptyDirVolume")
    @builtins.classmethod
    def is_empty_dir_volume(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) Returns ``true`` if ``x`` is an EmptyDirVolume, ``false`` otherwise.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61e4a4c5b13ccdd73d22eef16c5f25f0360005b334cbe7762bfae453bc1a14d5)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isEmptyDirVolume", [x]))

    @builtins.property
    @jsii.member(jsii_name="medium")
    def medium(self) -> typing.Optional[EmptyDirMediumType]:
        '''(experimental) The storage type to use for this Volume.

        :default: ``EmptyDirMediumType.DISK``

        :stability: experimental
        '''
        return typing.cast(typing.Optional[EmptyDirMediumType], jsii.get(self, "medium"))

    @builtins.property
    @jsii.member(jsii_name="sizeLimit")
    def size_limit(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The maximum size for this Volume.

        :default: - no size limit

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "sizeLimit"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EmptyDirVolumeOptions",
    jsii_struct_bases=[EksVolumeOptions],
    name_mapping={
        "name": "name",
        "mount_path": "mountPath",
        "readonly": "readonly",
        "medium": "medium",
        "size_limit": "sizeLimit",
    },
)
class EmptyDirVolumeOptions(EksVolumeOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
        medium: typing.Optional[EmptyDirMediumType] = None,
        size_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    ) -> None:
        '''(experimental) Options for a Kubernetes EmptyDir volume.

        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false
        :param medium: (experimental) The storage type to use for this Volume. Default: ``EmptyDirMediumType.DISK``
        :param size_limit: (experimental) The maximum size for this Volume. Default: - no size limit

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir
        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            job_defn = batch.EksJobDefinition(self, "eksf2",
                container=batch.EksContainerDefinition(self, "container",
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    volumes=[batch.EksVolume.empty_dir(
                        name="myEmptyDirVolume",
                        mount_path="/mount/path",
                        medium=batch.EmptyDirMediumType.MEMORY,
                        readonly=True,
                        size_limit=cdk.Size.mebibytes(2048)
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87b0da6c75ed058ff623aebcb883b8e2b3ec50d159a4b2f052c643873ed08f2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
            check_type(argname="argument size_limit", value=size_limit, expected_type=type_hints["size_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if mount_path is not None:
            self._values["mount_path"] = mount_path
        if readonly is not None:
            self._values["readonly"] = readonly
        if medium is not None:
            self._values["medium"] = medium
        if size_limit is not None:
            self._values["size_limit"] = size_limit

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of this volume.

        The name must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the container where the volume is mounted.

        :default: - the volume is not mounted

        :stability: experimental
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container has readonly access to the volume.

        Otherwise, the container has read/write access.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def medium(self) -> typing.Optional[EmptyDirMediumType]:
        '''(experimental) The storage type to use for this Volume.

        :default: ``EmptyDirMediumType.DISK``

        :stability: experimental
        '''
        result = self._values.get("medium")
        return typing.cast(typing.Optional[EmptyDirMediumType], result)

    @builtins.property
    def size_limit(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The maximum size for this Volume.

        :default: - no size limit

        :stability: experimental
        '''
        result = self._values.get("size_limit")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EmptyDirVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.FairshareSchedulingPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_reservation": "computeReservation",
        "scheduling_policy_name": "schedulingPolicyName",
        "share_decay": "shareDecay",
        "shares": "shares",
    },
)
class FairshareSchedulingPolicyProps:
    def __init__(
        self,
        *,
        compute_reservation: typing.Optional[jsii.Number] = None,
        scheduling_policy_name: typing.Optional[builtins.str] = None,
        share_decay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        shares: typing.Optional[typing.Sequence[typing.Union["Share", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Fairshare SchedulingPolicy configuration.

        :param compute_reservation: (experimental) Used to calculate the percentage of the maximum available vCPU to reserve for share identifiers not present in the Queue. The percentage reserved is defined by the Scheduler as: ``(computeReservation/100)^ActiveFairShares`` where ``ActiveFairShares`` is the number of active fair share identifiers. For example, a computeReservation value of 50 indicates that AWS Batch reserves 50% of the maximum available vCPU if there's only one fair share identifier. It reserves 25% if there are two fair share identifiers. It reserves 12.5% if there are three fair share identifiers. A computeReservation value of 25 indicates that AWS Batch should reserve 25% of the maximum available vCPU if there's only one fair share identifier, 6.25% if there are two fair share identifiers, and 1.56% if there are three fair share identifiers. Default: - no vCPU is reserved
        :param scheduling_policy_name: (experimental) The name of this SchedulingPolicy. Default: - generated by CloudFormation
        :param share_decay: (experimental) The amount of time to use to measure the usage of each job. The usage is used to calculate a fair share percentage for each fair share identifier currently in the Queue. A value of zero (0) indicates that only current usage is measured. The decay is linear and gives preference to newer jobs. The maximum supported value is 604800 seconds (1 week). Default: - 0: only the current job usage is considered
        :param shares: (experimental) The shares that this Scheduling Policy applies to. *Note*: It is possible to submit Jobs to the queue with Share Identifiers that are not recognized by the Scheduling Policy. Default: - no shares

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            fairshare_policy = batch.FairshareSchedulingPolicy(self, "myFairsharePolicy",
                share_decay=cdk.Duration.minutes(5)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ce1917e4f041cad0e9f935e693fee4450e8cf33f9a703df7ae1ed6aba5e4046)
            check_type(argname="argument compute_reservation", value=compute_reservation, expected_type=type_hints["compute_reservation"])
            check_type(argname="argument scheduling_policy_name", value=scheduling_policy_name, expected_type=type_hints["scheduling_policy_name"])
            check_type(argname="argument share_decay", value=share_decay, expected_type=type_hints["share_decay"])
            check_type(argname="argument shares", value=shares, expected_type=type_hints["shares"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_reservation is not None:
            self._values["compute_reservation"] = compute_reservation
        if scheduling_policy_name is not None:
            self._values["scheduling_policy_name"] = scheduling_policy_name
        if share_decay is not None:
            self._values["share_decay"] = share_decay
        if shares is not None:
            self._values["shares"] = shares

    @builtins.property
    def compute_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Used to calculate the percentage of the maximum available vCPU to reserve for share identifiers not present in the Queue.

        The percentage reserved is defined by the Scheduler as:
        ``(computeReservation/100)^ActiveFairShares`` where ``ActiveFairShares`` is the number of active fair share identifiers.

        For example, a computeReservation value of 50 indicates that AWS Batch reserves 50% of the
        maximum available vCPU if there's only one fair share identifier.
        It reserves 25% if there are two fair share identifiers.
        It reserves 12.5% if there are three fair share identifiers.

        A computeReservation value of 25 indicates that AWS Batch should reserve 25% of the
        maximum available vCPU if there's only one fair share identifier,
        6.25% if there are two fair share identifiers,
        and 1.56% if there are three fair share identifiers.

        :default: - no vCPU is reserved

        :stability: experimental
        '''
        result = self._values.get("compute_reservation")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheduling_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this SchedulingPolicy.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("scheduling_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def share_decay(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The amount of time to use to measure the usage of each job.

        The usage is used to calculate a fair share percentage for each fair share identifier currently in the Queue.
        A value of zero (0) indicates that only current usage is measured.
        The decay is linear and gives preference to newer jobs.

        The maximum supported value is 604800 seconds (1 week).

        :default: - 0: only the current job usage is considered

        :stability: experimental
        '''
        result = self._values.get("share_decay")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def shares(self) -> typing.Optional[typing.List["Share"]]:
        '''(experimental) The shares that this Scheduling Policy applies to.

        *Note*: It is possible to submit Jobs to the queue with Share Identifiers that
        are not recognized by the Scheduling Policy.

        :default: - no shares

        :stability: experimental
        '''
        result = self._values.get("shares")
        return typing.cast(typing.Optional[typing.List["Share"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FairshareSchedulingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostPathVolume(
    EksVolume,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.HostPathVolume",
):
    '''(experimental) A Kubernetes HostPath volume.

    :see: https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        
        host_path_volume = batch_alpha.HostPathVolume(
            host_path="hostPath",
            name="name",
        
            # the properties below are optional
            mount_path="mountPath",
            readonly=False
        )
    '''

    def __init__(
        self,
        *,
        host_path: builtins.str,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param host_path: (experimental) The path of the file or directory on the host to mount into containers on the pod. *Note*: HothPath Volumes present many security risks, and should be avoided when possible.
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :stability: experimental
        '''
        options = HostPathVolumeOptions(
            host_path=host_path, name=name, mount_path=mount_path, readonly=readonly
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isHostPathVolume")
    @builtins.classmethod
    def is_host_path_volume(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) returns ``true`` if ``x`` is a HostPathVolume, ``false`` otherwise.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0fe123d5409e9e44652333f1dca6e60d125b36cf2343f8a86721cd66de4dc2)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isHostPathVolume", [x]))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) The path of the file or directory on the host to mount into containers on the pod.

        *Note*: HothPath Volumes present many security risks, and should be avoided when possible.

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.HostPathVolumeOptions",
    jsii_struct_bases=[EksVolumeOptions],
    name_mapping={
        "name": "name",
        "mount_path": "mountPath",
        "readonly": "readonly",
        "host_path": "hostPath",
    },
)
class HostPathVolumeOptions(EksVolumeOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
        host_path: builtins.str,
    ) -> None:
        '''(experimental) Options for a kubernetes HostPath volume.

        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false
        :param host_path: (experimental) The path of the file or directory on the host to mount into containers on the pod. *Note*: HothPath Volumes present many security risks, and should be avoided when possible.

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
        :stability: experimental
        :exampleMetadata: infused

        Example::

            # job_defn: batch.EksJobDefinition
            
            job_defn.container.add_volume(batch.EksVolume.empty_dir(
                name="emptyDir",
                mount_path="/Volumes/emptyDir"
            ))
            job_defn.container.add_volume(batch.EksVolume.host_path(
                name="hostPath",
                host_path="/sys",
                mount_path="/Volumes/hostPath"
            ))
            job_defn.container.add_volume(batch.EksVolume.secret(
                name="secret",
                optional=True,
                mount_path="/Volumes/secret",
                secret_name="mySecret"
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f8d5c089c2fc4d5e83ef7c0147c81ab62b6f89571ecbdba336189a07a601b2)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "host_path": host_path,
        }
        if mount_path is not None:
            self._values["mount_path"] = mount_path
        if readonly is not None:
            self._values["readonly"] = readonly

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of this volume.

        The name must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the container where the volume is mounted.

        :default: - the volume is not mounted

        :stability: experimental
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container has readonly access to the volume.

        Otherwise, the container has read/write access.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def host_path(self) -> builtins.str:
        '''(experimental) The path of the file or directory on the host to mount into containers on the pod.

        *Note*: HothPath Volumes present many security risks, and should be avoided when possible.

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
        :stability: experimental
        '''
        result = self._values.get("host_path")
        assert result is not None, "Required property 'host_path' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostPathVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HostVolume(
    EcsVolume,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.HostVolume",
):
    '''(experimental) Creates a Host volume.

    This volume will persist on the host at the specified ``hostPath``.
    If the ``hostPath`` is not specified, Docker will choose the host path. In this case,
    the data may not persist after the containers that use it stop running.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        
        host_volume = batch_alpha.HostVolume(
            container_path="containerPath",
            name="name",
        
            # the properties below are optional
            host_path="hostPath",
            readonly=False
        )
    '''

    def __init__(
        self,
        *,
        host_path: typing.Optional[builtins.str] = None,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param host_path: (experimental) The path on the host machine this container will have access to. Default: - Docker will choose the host path. The data may not persist after the containers that use it stop running.
        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false

        :stability: experimental
        '''
        options = HostVolumeOptions(
            host_path=host_path,
            container_path=container_path,
            name=name,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isHostVolume")
    @builtins.classmethod
    def is_host_volume(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) returns ``true`` if ``x`` is a ``HostVolume``, ``false`` otherwise.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7afaf677383998a2af7586ef0bd46764cb4ab6f8eb0e0559bf181485514b63a)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isHostVolume", [x]))

    @builtins.property
    @jsii.member(jsii_name="hostPath")
    def host_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the host machine this container will have access to.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostPath"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.HostVolumeOptions",
    jsii_struct_bases=[EcsVolumeOptions],
    name_mapping={
        "container_path": "containerPath",
        "name": "name",
        "readonly": "readonly",
        "host_path": "hostPath",
    },
)
class HostVolumeOptions(EcsVolumeOptions):
    def __init__(
        self,
        *,
        container_path: builtins.str,
        name: builtins.str,
        readonly: typing.Optional[builtins.bool] = None,
        host_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for configuring an ECS HostVolume.

        :param container_path: (experimental) the path on the container where this volume is mounted.
        :param name: (experimental) the name of this volume.
        :param readonly: (experimental) if set, the container will have readonly access to the volume. Default: false
        :param host_path: (experimental) The path on the host machine this container will have access to. Default: - Docker will choose the host path. The data may not persist after the containers that use it stop running.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            host_volume_options = batch_alpha.HostVolumeOptions(
                container_path="containerPath",
                name="name",
            
                # the properties below are optional
                host_path="hostPath",
                readonly=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49269c9b7b771ac8a3b0c8c0320d0b98fd9d95fad759832648b74d993a22ecd9)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_path": container_path,
            "name": name,
        }
        if readonly is not None:
            self._values["readonly"] = readonly
        if host_path is not None:
            self._values["host_path"] = host_path

    @builtins.property
    def container_path(self) -> builtins.str:
        '''(experimental) the path on the container where this volume is mounted.

        :stability: experimental
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) the name of this volume.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if set, the container will have readonly access to the volume.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def host_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the host machine this container will have access to.

        :default:

        - Docker will choose the host path.
        The data may not persist after the containers that use it stop running.

        :stability: experimental
        '''
        result = self._values.get("host_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IComputeEnvironment")
class IComputeEnvironment(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a ComputeEnvironment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        '''(experimental) The ARN of this compute environment.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        '''(experimental) The name of the ComputeEnvironment.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        ...


class _IComputeEnvironmentProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a ComputeEnvironment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IComputeEnvironment"

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        '''(experimental) The ARN of this compute environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        '''(experimental) The name of the ComputeEnvironment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "serviceRole"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComputeEnvironment).__jsii_proxy_class__ = lambda : _IComputeEnvironmentProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IEcsContainerDefinition")
class IEcsContainerDefinition(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''(experimental) A container that can be run with ECS orchestration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :see: https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EcsVolume]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :default: - no volumes

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :see: https://docs.docker.com/engine/reference/builder/#cmd
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :default: - no environment variables

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobRole")
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :default: - no jobRole

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :default: none

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="logDriverConfig")
    def log_driver_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig]:
        '''(experimental) The configuration of the log driver.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :default: false

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :default: - no secrets

        :see: https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :default: - no user

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EcsVolume) -> None:
        '''(experimental) Add a Volume to this container.

        :param volume: -

        :stability: experimental
        '''
        ...


class _IEcsContainerDefinitionProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''(experimental) A container that can be run with ECS orchestration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IEcsContainerDefinition"

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :see: https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html
        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "executionRole"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.Size, jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EcsVolume]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :default: - no volumes

        :stability: experimental
        '''
        return typing.cast(typing.List[EcsVolume], jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :see: https://docs.docker.com/engine/reference/builder/#cmd
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :default: - no environment variables

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="jobRole")
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :default: - no jobRole

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "jobRole"))

    @builtins.property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional["LinuxParameters"]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :default: none

        :stability: experimental
        '''
        return typing.cast(typing.Optional["LinuxParameters"], jsii.get(self, "linuxParameters"))

    @builtins.property
    @jsii.member(jsii_name="logDriverConfig")
    def log_driver_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig]:
        '''(experimental) The configuration of the log driver.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig], jsii.get(self, "logDriverConfig"))

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :default: false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonlyRootFilesystem"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, "Secret"]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :default: - no secrets

        :see: https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "Secret"]], jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :default: - no user

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "user"))

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EcsVolume) -> None:
        '''(experimental) Add a Volume to this container.

        :param volume: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23d7381af0c45284e0879a7629848fc4de2d3901ba78f741661211bc62d9316c)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        return typing.cast(None, jsii.invoke(self, "addVolume", [volume]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcsContainerDefinition).__jsii_proxy_class__ = lambda : _IEcsContainerDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IEcsEc2ContainerDefinition")
class IEcsEc2ContainerDefinition(IEcsContainerDefinition, typing_extensions.Protocol):
    '''(experimental) A container orchestrated by ECS that uses EC2 resources.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List["Ulimit"]:
        '''(experimental) Limits to set for the user this docker container will run as.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="gpu")
    def gpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of physical GPUs to reserve for the container.

        Make sure that the number of GPUs reserved for all containers in a job doesn't exceed
        the number of available GPUs on the compute resource that the job is launched on.

        :default: - no gpus

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When this parameter is true, the container is given elevated permissions on the host container instance (similar to the root user).

        :default: false

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addUlimit")
    def add_ulimit(
        self,
        *,
        hard_limit: jsii.Number,
        name: "UlimitName",
        soft_limit: jsii.Number,
    ) -> None:
        '''(experimental) Add a ulimit to this container.

        :param hard_limit: (experimental) The hard limit for this resource. The container will be terminated if it exceeds this limit.
        :param name: (experimental) The resource to limit.
        :param soft_limit: (experimental) The reservation for this resource. The container will not be terminated if it exceeds this limit.

        :stability: experimental
        '''
        ...


class _IEcsEc2ContainerDefinitionProxy(
    jsii.proxy_for(IEcsContainerDefinition), # type: ignore[misc]
):
    '''(experimental) A container orchestrated by ECS that uses EC2 resources.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IEcsEc2ContainerDefinition"

    @builtins.property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List["Ulimit"]:
        '''(experimental) Limits to set for the user this docker container will run as.

        :stability: experimental
        '''
        return typing.cast(typing.List["Ulimit"], jsii.get(self, "ulimits"))

    @builtins.property
    @jsii.member(jsii_name="gpu")
    def gpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of physical GPUs to reserve for the container.

        Make sure that the number of GPUs reserved for all containers in a job doesn't exceed
        the number of available GPUs on the compute resource that the job is launched on.

        :default: - no gpus

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpu"))

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When this parameter is true, the container is given elevated permissions on the host container instance (similar to the root user).

        :default: false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "privileged"))

    @jsii.member(jsii_name="addUlimit")
    def add_ulimit(
        self,
        *,
        hard_limit: jsii.Number,
        name: "UlimitName",
        soft_limit: jsii.Number,
    ) -> None:
        '''(experimental) Add a ulimit to this container.

        :param hard_limit: (experimental) The hard limit for this resource. The container will be terminated if it exceeds this limit.
        :param name: (experimental) The resource to limit.
        :param soft_limit: (experimental) The reservation for this resource. The container will not be terminated if it exceeds this limit.

        :stability: experimental
        '''
        ulimit = Ulimit(hard_limit=hard_limit, name=name, soft_limit=soft_limit)

        return typing.cast(None, jsii.invoke(self, "addUlimit", [ulimit]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcsEc2ContainerDefinition).__jsii_proxy_class__ = lambda : _IEcsEc2ContainerDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IEcsFargateContainerDefinition")
class IEcsFargateContainerDefinition(
    IEcsContainerDefinition,
    typing_extensions.Protocol,
):
    '''(experimental) A container orchestrated by ECS that uses Fargate resources and is orchestrated by ECS.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the job has a public IP address.

        For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet
        (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet.

        :default: false

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageSize")
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The size for ephemeral storage.

        :default: - 20 GiB

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="fargatePlatformVersion")
    def fargate_platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion]:
        '''(experimental) Which version of Fargate to use when running this container.

        :default: LATEST

        :stability: experimental
        '''
        ...


class _IEcsFargateContainerDefinitionProxy(
    jsii.proxy_for(IEcsContainerDefinition), # type: ignore[misc]
):
    '''(experimental) A container orchestrated by ECS that uses Fargate resources and is orchestrated by ECS.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IEcsFargateContainerDefinition"

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the job has a public IP address.

        For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet
        (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet.

        :default: false

        :see: https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageSize")
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The size for ephemeral storage.

        :default: - 20 GiB

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "ephemeralStorageSize"))

    @builtins.property
    @jsii.member(jsii_name="fargatePlatformVersion")
    def fargate_platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion]:
        '''(experimental) Which version of Fargate to use when running this container.

        :default: LATEST

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion], jsii.get(self, "fargatePlatformVersion"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcsFargateContainerDefinition).__jsii_proxy_class__ = lambda : _IEcsFargateContainerDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IEksContainerDefinition")
class IEksContainerDefinition(
    _constructs_77d1e7e8.IConstruct,
    typing_extensions.Protocol,
):
    '''(experimental) A container that can be run with EKS orchestration on EC2 resources.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EksVolume]:
        '''(experimental) The Volumes to mount to this container.

        Automatically added to the Pod.

        :see: https://kubernetes.io/docs/concepts/storage/volumes/
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of arguments to the entrypoint.

        If this isn't specified, the CMD of the container image is used.
        This corresponds to the args member in the Entrypoint portion of the Pod in Kubernetes.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to "$(NAME1)" and the NAME1 environment variable doesn't exist,
        the command string will remain "$(NAME1)." $$ is replaced with $, and the resulting string isn't expanded.
        or example, $$(VAR_NAME) is passed as $(VAR_NAME) whether or not the VAR_NAME environment variable exists.

        :see: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The entrypoint for the container.

        This isn't run within a shell.
        If this isn't specified, the ``ENTRYPOINT`` of the container image is used.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to ``"$(NAME1)"`` and the ``NAME1`` environment variable doesn't exist,
        the command string will remain ``"$(NAME1)."`` ``$$`` is replaced with ``$`` and the resulting string isn't expanded.
        For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists.

        The entrypoint can't be updated.

        :see: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of CPUs to present to this container. Must be an even multiple of 0.25.

        If your container attempts to exceed this limit, it will be terminated.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :default: - No CPU limit

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="cpuReservation")
    def cpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :default: - No CPUs reserved

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to this container.

        *Note*: Environment variables cannot start with "AWS_BATCH".
        This naming convention is reserved for variables that AWS Batch sets.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="gpuLimit")
    def gpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of GPUs to present to this container.

        If your container attempts to exceed this limit, it will be terminated.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :default: - No GPU limit

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="gpuReservation")
    def gpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :default: - No GPUs reserved

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="imagePullPolicy")
    def image_pull_policy(self) -> typing.Optional["ImagePullPolicy"]:
        '''(experimental) The image pull policy for this container.

        :default: - ``ALWAYS`` if the ``:latest`` tag is specified, ``IF_NOT_PRESENT`` otherwise

        :see: https://kubernetes.io/docs/concepts/containers/images/#updating-images
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, it will be terminated.

        Must be larger that 4 MiB

        At least one of ``memoryLimit`` and ``memoryReservation`` is required

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :default: - No memory limit

        :see: https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        Your container will be given at least this much memory, but may consume more.

        Must be larger that 4 MiB

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of ``memoryLimit`` and ``memoryReservation`` is required.
        If both are specified, then ``memoryLimit`` must be equal to ``memoryReservation``

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :default: - No memory reserved

        :see: https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this container.

        :default: : ``'Default'``

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container elevated permissions on the host container instance.

        The level of permissions are similar to the root user permissions.

        This parameter maps to ``privileged`` policy in the Privileged pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: false

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#volumes-and-file-systems
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container readonly access to its root file system.

        This parameter maps to ``ReadOnlyRootFilesystem`` policy in the Volumes and file systems pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: false

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#volumes-and-file-systems
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="runAsGroup")
    def run_as_group(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, the container is run as the specified group ID (``gid``).

        If this parameter isn't specified, the default is the group that's specified in the image metadata.
        This parameter maps to ``RunAsGroup`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: none

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="runAsRoot")
    def run_as_root(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container is run as a user with a ``uid`` other than 0.

        Otherwise, no such rule is enforced.
        This parameter maps to ``RunAsUser`` and ``MustRunAsNonRoot`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: - the container is *not* required to run as a non-root user

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="runAsUser")
    def run_as_user(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, this container is run as the specified user ID (``uid``).

        This parameter maps to ``RunAsUser`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: - the user that is specified in the image metadata.

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EksVolume) -> None:
        '''(experimental) Mount a Volume to this container.

        Automatically added to the Pod.

        :param volume: -

        :stability: experimental
        '''
        ...


class _IEksContainerDefinitionProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
):
    '''(experimental) A container that can be run with EKS orchestration on EC2 resources.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IEksContainerDefinition"

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EksVolume]:
        '''(experimental) The Volumes to mount to this container.

        Automatically added to the Pod.

        :see: https://kubernetes.io/docs/concepts/storage/volumes/
        :stability: experimental
        '''
        return typing.cast(typing.List[EksVolume], jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of arguments to the entrypoint.

        If this isn't specified, the CMD of the container image is used.
        This corresponds to the args member in the Entrypoint portion of the Pod in Kubernetes.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to "$(NAME1)" and the NAME1 environment variable doesn't exist,
        the command string will remain "$(NAME1)." $$ is replaced with $, and the resulting string isn't expanded.
        or example, $$(VAR_NAME) is passed as $(VAR_NAME) whether or not the VAR_NAME environment variable exists.

        :see: https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "args"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The entrypoint for the container.

        This isn't run within a shell.
        If this isn't specified, the ``ENTRYPOINT`` of the container image is used.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to ``"$(NAME1)"`` and the ``NAME1`` environment variable doesn't exist,
        the command string will remain ``"$(NAME1)."`` ``$$`` is replaced with ``$`` and the resulting string isn't expanded.
        For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists.

        The entrypoint can't be updated.

        :see: https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of CPUs to present to this container. Must be an even multiple of 0.25.

        If your container attempts to exceed this limit, it will be terminated.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :default: - No CPU limit

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuLimit"))

    @builtins.property
    @jsii.member(jsii_name="cpuReservation")
    def cpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :default: - No CPUs reserved

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuReservation"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to this container.

        *Note*: Environment variables cannot start with "AWS_BATCH".
        This naming convention is reserved for variables that AWS Batch sets.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="gpuLimit")
    def gpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of GPUs to present to this container.

        If your container attempts to exceed this limit, it will be terminated.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :default: - No GPU limit

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuLimit"))

    @builtins.property
    @jsii.member(jsii_name="gpuReservation")
    def gpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :default: - No GPUs reserved

        :see: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuReservation"))

    @builtins.property
    @jsii.member(jsii_name="imagePullPolicy")
    def image_pull_policy(self) -> typing.Optional["ImagePullPolicy"]:
        '''(experimental) The image pull policy for this container.

        :default: - ``ALWAYS`` if the ``:latest`` tag is specified, ``IF_NOT_PRESENT`` otherwise

        :see: https://kubernetes.io/docs/concepts/containers/images/#updating-images
        :stability: experimental
        '''
        return typing.cast(typing.Optional["ImagePullPolicy"], jsii.get(self, "imagePullPolicy"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, it will be terminated.

        Must be larger that 4 MiB

        At least one of ``memoryLimit`` and ``memoryReservation`` is required

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :default: - No memory limit

        :see: https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "memoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        Your container will be given at least this much memory, but may consume more.

        Must be larger that 4 MiB

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of ``memoryLimit`` and ``memoryReservation`` is required.
        If both are specified, then ``memoryLimit`` must be equal to ``memoryReservation``

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :default: - No memory reserved

        :see: https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "memoryReservation"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this container.

        :default: : ``'Default'``

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container elevated permissions on the host container instance.

        The level of permissions are similar to the root user permissions.

        This parameter maps to ``privileged`` policy in the Privileged pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: false

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#volumes-and-file-systems
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "privileged"))

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container readonly access to its root file system.

        This parameter maps to ``ReadOnlyRootFilesystem`` policy in the Volumes and file systems pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: false

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#volumes-and-file-systems
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonlyRootFilesystem"))

    @builtins.property
    @jsii.member(jsii_name="runAsGroup")
    def run_as_group(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, the container is run as the specified group ID (``gid``).

        If this parameter isn't specified, the default is the group that's specified in the image metadata.
        This parameter maps to ``RunAsGroup`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: none

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runAsGroup"))

    @builtins.property
    @jsii.member(jsii_name="runAsRoot")
    def run_as_root(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container is run as a user with a ``uid`` other than 0.

        Otherwise, no such rule is enforced.
        This parameter maps to ``RunAsUser`` and ``MustRunAsNonRoot`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: - the container is *not* required to run as a non-root user

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "runAsRoot"))

    @builtins.property
    @jsii.member(jsii_name="runAsUser")
    def run_as_user(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, this container is run as the specified user ID (``uid``).

        This parameter maps to ``RunAsUser`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :default: - the user that is specified in the image metadata.

        :see: https://kubernetes.io/docs/concepts/security/pod-security-policy/#users-and-groups
        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runAsUser"))

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EksVolume) -> None:
        '''(experimental) Mount a Volume to this container.

        Automatically added to the Pod.

        :param volume: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d27eac738541f17e8629ff3d1cc312de8b73bc0f3d2f69a01613e321f0180a2)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        return typing.cast(None, jsii.invoke(self, "addVolume", [volume]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEksContainerDefinition).__jsii_proxy_class__ = lambda : _IEksContainerDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IJobDefinition")
class IJobDefinition(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a JobDefinition.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job definition.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of this job definition.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="retryStrategies")
    def retry_strategies(self) -> typing.List["RetryStrategy"]:
        '''(experimental) Defines the retry behavior for this job.

        :default: - no ``RetryStrategy``

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :default: none

        :see: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html#parameters
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="schedulingPriority")
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :default: none

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :default: - no timeout

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addRetryStrategy")
    def add_retry_strategy(self, strategy: "RetryStrategy") -> None:
        '''(experimental) Add a RetryStrategy to this JobDefinition.

        :param strategy: -

        :stability: experimental
        '''
        ...


class _IJobDefinitionProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a JobDefinition.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IJobDefinition"

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job definition.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionArn"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of this job definition.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionName"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategies")
    def retry_strategies(self) -> typing.List["RetryStrategy"]:
        '''(experimental) Defines the retry behavior for this job.

        :default: - no ``RetryStrategy``

        :stability: experimental
        '''
        return typing.cast(typing.List["RetryStrategy"], jsii.get(self, "retryStrategies"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :default: none

        :see: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html#parameters
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPriority")
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :default: none

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulingPriority"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :default: - no timeout

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))

    @jsii.member(jsii_name="addRetryStrategy")
    def add_retry_strategy(self, strategy: "RetryStrategy") -> None:
        '''(experimental) Add a RetryStrategy to this JobDefinition.

        :param strategy: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334a109994c2c6dac94c2aeaf63b80742ab7e39597ca35cd656e28c702af44c2)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        return typing.cast(None, jsii.invoke(self, "addRetryStrategy", [strategy]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobDefinition).__jsii_proxy_class__ = lambda : _IJobDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IJobQueue")
class IJobQueue(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a JobQueue.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="computeEnvironments")
    def compute_environments(self) -> typing.List["OrderedComputeEnvironment"]:
        '''(experimental) The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job.
        Compute environments must be in the VALID state before you can associate them with a job queue.
        You can associate up to three compute environments with a job queue.
        All of the compute environments must be either EC2 (EC2 or SPOT) or Fargate (FARGATE or FARGATE_SPOT);
        EC2 and Fargate compute environments can't be mixed.

        *Note*: All compute environments that are associated with a job queue must share the same architecture.
        AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job queue.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        '''(experimental) The name of the job queue.

        It can be up to 128 letters long.
        It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_)

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the job queue.

        Job queues with a higher priority are evaluated first when associated with the same compute environment.
        Priority is determined in descending order.
        For example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the job queue is enabled, it is able to accept jobs.

        Otherwise, new jobs can't be added to the queue, but jobs already in the queue can finish.

        :default: true

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicy")
    def scheduling_policy(self) -> typing.Optional["ISchedulingPolicy"]:
        '''(experimental) The SchedulingPolicy for this JobQueue.

        Instructs the Scheduler how to schedule different jobs.

        :default: - no scheduling policy

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addComputeEnvironment")
    def add_compute_environment(
        self,
        compute_environment: IComputeEnvironment,
        order: jsii.Number,
    ) -> None:
        '''(experimental) Add a ``ComputeEnvironment`` to this Queue.

        The Queue will prefer lower-order ``ComputeEnvironment``s.

        :param compute_environment: -
        :param order: -

        :stability: experimental
        '''
        ...


class _IJobQueueProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a JobQueue.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IJobQueue"

    @builtins.property
    @jsii.member(jsii_name="computeEnvironments")
    def compute_environments(self) -> typing.List["OrderedComputeEnvironment"]:
        '''(experimental) The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job.
        Compute environments must be in the VALID state before you can associate them with a job queue.
        You can associate up to three compute environments with a job queue.
        All of the compute environments must be either EC2 (EC2 or SPOT) or Fargate (FARGATE or FARGATE_SPOT);
        EC2 and Fargate compute environments can't be mixed.

        *Note*: All compute environments that are associated with a job queue must share the same architecture.
        AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :stability: experimental
        '''
        return typing.cast(typing.List["OrderedComputeEnvironment"], jsii.get(self, "computeEnvironments"))

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job queue.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueArn"))

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        '''(experimental) The name of the job queue.

        It can be up to 128 letters long.
        It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_)

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueName"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the job queue.

        Job queues with a higher priority are evaluated first when associated with the same compute environment.
        Priority is determined in descending order.
        For example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the job queue is enabled, it is able to accept jobs.

        Otherwise, new jobs can't be added to the queue, but jobs already in the queue can finish.

        :default: true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicy")
    def scheduling_policy(self) -> typing.Optional["ISchedulingPolicy"]:
        '''(experimental) The SchedulingPolicy for this JobQueue.

        Instructs the Scheduler how to schedule different jobs.

        :default: - no scheduling policy

        :stability: experimental
        '''
        return typing.cast(typing.Optional["ISchedulingPolicy"], jsii.get(self, "schedulingPolicy"))

    @jsii.member(jsii_name="addComputeEnvironment")
    def add_compute_environment(
        self,
        compute_environment: IComputeEnvironment,
        order: jsii.Number,
    ) -> None:
        '''(experimental) Add a ``ComputeEnvironment`` to this Queue.

        The Queue will prefer lower-order ``ComputeEnvironment``s.

        :param compute_environment: -
        :param order: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff1947820a24bcf175625e5097d37007f089af82dc7c2a7b5b2fb7ff68bf271)
            check_type(argname="argument compute_environment", value=compute_environment, expected_type=type_hints["compute_environment"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        return typing.cast(None, jsii.invoke(self, "addComputeEnvironment", [compute_environment, order]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobQueue).__jsii_proxy_class__ = lambda : _IJobQueueProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IManagedComputeEnvironment")
class IManagedComputeEnvironment(
    IComputeEnvironment,
    _aws_cdk_aws_ec2_ceddda9d.IConnectable,
    _aws_cdk_ceddda9d.ITaggable,
    typing_extensions.Protocol,
):
    '''(experimental) Represents a Managed ComputeEnvironment.

    Batch will provision EC2 Instances to
    meet the requirements of the jobs executing in this ComputeEnvironment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="maxvCpus")
    def maxv_cpus(self) -> jsii.Number:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :default: false

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="terminateOnUpdate")
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updateTimeout")
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :default: 30 minutes

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="updateToLatestImageVersion")
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :default: true

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="vpcSubnets")
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The VPC Subnets this Compute Environment will launch instances in.

        :stability: experimental
        '''
        ...


class _IManagedComputeEnvironmentProxy(
    jsii.proxy_for(IComputeEnvironment), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_aws_ec2_ceddda9d.IConnectable), # type: ignore[misc]
    jsii.proxy_for(_aws_cdk_ceddda9d.ITaggable), # type: ignore[misc]
):
    '''(experimental) Represents a Managed ComputeEnvironment.

    Batch will provision EC2 Instances to
    meet the requirements of the jobs executing in this ComputeEnvironment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IManagedComputeEnvironment"

    @builtins.property
    @jsii.member(jsii_name="maxvCpus")
    def maxv_cpus(self) -> jsii.Number:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "maxvCpus"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "replaceComputeEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :default: false

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "spot"))

    @builtins.property
    @jsii.member(jsii_name="terminateOnUpdate")
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "terminateOnUpdate"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeout")
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :default: 30 minutes

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "updateTimeout"))

    @builtins.property
    @jsii.member(jsii_name="updateToLatestImageVersion")
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :default: true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "updateToLatestImageVersion"))

    @builtins.property
    @jsii.member(jsii_name="vpcSubnets")
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The VPC Subnets this Compute Environment will launch instances in.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], jsii.get(self, "vpcSubnets"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedComputeEnvironment).__jsii_proxy_class__ = lambda : _IManagedComputeEnvironmentProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IManagedEc2EcsComputeEnvironment")
class IManagedEc2EcsComputeEnvironment(
    IManagedComputeEnvironment,
    typing_extensions.Protocol,
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on EC2 instances.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="instanceClasses")
    def instance_classes(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]:
        '''(experimental) The instance classes that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.
        Batch will automatically choose the size.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated.

        :default:

        - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances,
        ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.Optional[typing.List[EcsMachineImage]]:
        '''(experimental) Configure which AMIs this Compute Environment can launch.

        Leave this ``undefined`` to allow Batch to choose the latest AMIs it supports for each instance that it launches.

        :default: - ECS_AL2 compatible AMI ids for non-GPU instances, ECS_AL2_NVIDIA compatible AMI ids for GPU instances

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution Role that instances launched by this Compute Environment will use.

        :default: - a role will be created

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances.

        *Note*: if ``securityGroups`` is specified on both your
        launch template and this Compute Environment, **the
        ``securityGroup``s on the Compute Environment override the
        ones on the launch template.

        :default: no launch template

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="minvCpus")
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED.

        :default: 0

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="placementGroup")
    def placement_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup]:
        '''(experimental) The EC2 placement group to associate with your compute resources.

        If you intend to submit multi-node parallel jobs to this Compute Environment,
        you should consider creating a cluster placement group and associate it with your compute resources.
        This keeps your multi-node parallel job on a logical grouping of instances
        within a single Availability Zone with high network flow potential.

        :default: - no placement group

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="spotBidPercentage")
    def spot_bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

        For example, if your maximum percentage is 20%, the Spot price must be
        less than 20% of the current On-Demand price for that Instance.
        You always pay the lowest market price and never more than your maximum percentage.
        For most use cases, Batch recommends leaving this field empty.

        :default: - 100%

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="spotFleetRole")
    def spot_fleet_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The service-linked role that Spot Fleet needs to launch instances on your behalf.

        :default: - a new Role will be created

        :see: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="useOptimalInstanceClasses")
    def use_optimal_instance_classes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use batch's optimal instance type.

        The optimal instance type is equivalent to adding the
        C4, M4, and R4 instance classes. You can specify other instance classes
        (of the same architecture) in addition to the optimal instance classes.

        :default: true

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addInstanceClass")
    def add_instance_class(
        self,
        instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
    ) -> None:
        '''(experimental) Add an instance class to this compute environment.

        :param instance_class: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addInstanceType")
    def add_instance_type(
        self,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    ) -> None:
        '''(experimental) Add an instance type to this compute environment.

        :param instance_type: -

        :stability: experimental
        '''
        ...


class _IManagedEc2EcsComputeEnvironmentProxy(
    jsii.proxy_for(IManagedComputeEnvironment), # type: ignore[misc]
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on EC2 instances.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IManagedEc2EcsComputeEnvironment"

    @builtins.property
    @jsii.member(jsii_name="instanceClasses")
    def instance_classes(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]:
        '''(experimental) The instance classes that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.
        Batch will automatically choose the size.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass], jsii.get(self, "instanceClasses"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType], jsii.get(self, "instanceTypes"))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated.

        :default:

        - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances,
        ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AllocationStrategy], jsii.get(self, "allocationStrategy"))

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.Optional[typing.List[EcsMachineImage]]:
        '''(experimental) Configure which AMIs this Compute Environment can launch.

        Leave this ``undefined`` to allow Batch to choose the latest AMIs it supports for each instance that it launches.

        :default: - ECS_AL2 compatible AMI ids for non-GPU instances, ECS_AL2_NVIDIA compatible AMI ids for GPU instances

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[EcsMachineImage]], jsii.get(self, "images"))

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution Role that instances launched by this Compute Environment will use.

        :default: - a role will be created

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "instanceRole"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances.

        *Note*: if ``securityGroups`` is specified on both your
        launch template and this Compute Environment, **the
        ``securityGroup``s on the Compute Environment override the
        ones on the launch template.

        :default: no launch template

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate], jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="minvCpus")
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED.

        :default: 0

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minvCpus"))

    @builtins.property
    @jsii.member(jsii_name="placementGroup")
    def placement_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup]:
        '''(experimental) The EC2 placement group to associate with your compute resources.

        If you intend to submit multi-node parallel jobs to this Compute Environment,
        you should consider creating a cluster placement group and associate it with your compute resources.
        This keeps your multi-node parallel job on a logical grouping of instances
        within a single Availability Zone with high network flow potential.

        :default: - no placement group

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup], jsii.get(self, "placementGroup"))

    @builtins.property
    @jsii.member(jsii_name="spotBidPercentage")
    def spot_bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

        For example, if your maximum percentage is 20%, the Spot price must be
        less than 20% of the current On-Demand price for that Instance.
        You always pay the lowest market price and never more than your maximum percentage.
        For most use cases, Batch recommends leaving this field empty.

        :default: - 100%

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidPercentage"))

    @builtins.property
    @jsii.member(jsii_name="spotFleetRole")
    def spot_fleet_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The service-linked role that Spot Fleet needs to launch instances on your behalf.

        :default: - a new Role will be created

        :see: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "spotFleetRole"))

    @builtins.property
    @jsii.member(jsii_name="useOptimalInstanceClasses")
    def use_optimal_instance_classes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use batch's optimal instance type.

        The optimal instance type is equivalent to adding the
        C4, M4, and R4 instance classes. You can specify other instance classes
        (of the same architecture) in addition to the optimal instance classes.

        :default: true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useOptimalInstanceClasses"))

    @jsii.member(jsii_name="addInstanceClass")
    def add_instance_class(
        self,
        instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
    ) -> None:
        '''(experimental) Add an instance class to this compute environment.

        :param instance_class: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387f2e9251b506a8dfd9ff3e858b74a8cb740b78008ea64c6da21917b9d825d8)
            check_type(argname="argument instance_class", value=instance_class, expected_type=type_hints["instance_class"])
        return typing.cast(None, jsii.invoke(self, "addInstanceClass", [instance_class]))

    @jsii.member(jsii_name="addInstanceType")
    def add_instance_type(
        self,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    ) -> None:
        '''(experimental) Add an instance type to this compute environment.

        :param instance_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67a3ed0d94894cdb085f842a16aaefb3d6a0289bb3d3b50151249f5a01aa9d3e)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
        return typing.cast(None, jsii.invoke(self, "addInstanceType", [instance_type]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedEc2EcsComputeEnvironment).__jsii_proxy_class__ = lambda : _IManagedEc2EcsComputeEnvironmentProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.ISchedulingPolicy")
class ISchedulingPolicy(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(experimental) Represents a Scheduling Policy.

    Scheduling Policies tell the Batch
    Job Scheduler how to schedule incoming jobs.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyArn")
    def scheduling_policy_arn(self) -> builtins.str:
        '''(experimental) The arn of this scheduling policy.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyName")
    def scheduling_policy_name(self) -> builtins.str:
        '''(experimental) The name of this scheduling policy.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ISchedulingPolicyProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(experimental) Represents a Scheduling Policy.

    Scheduling Policies tell the Batch
    Job Scheduler how to schedule incoming jobs.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.ISchedulingPolicy"

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyArn")
    def scheduling_policy_arn(self) -> builtins.str:
        '''(experimental) The arn of this scheduling policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "schedulingPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyName")
    def scheduling_policy_name(self) -> builtins.str:
        '''(experimental) The name of this scheduling policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "schedulingPolicyName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISchedulingPolicy).__jsii_proxy_class__ = lambda : _ISchedulingPolicyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IUnmanagedComputeEnvironment")
class IUnmanagedComputeEnvironment(IComputeEnvironment, typing_extensions.Protocol):
    '''(experimental) Represents an UnmanagedComputeEnvironment.

    Batch will not provision instances on your behalf
    in this ComputeEvironment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="unmanagedvCPUs")
    def unmanagedv_cp_us(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The vCPUs this Compute Environment provides. Used only by the scheduler to schedule jobs in ``Queue``s that use ``FairshareSchedulingPolicy``s.

        **If this parameter is not provided on a fairshare queue, no capacity is reserved**;
        that is, the ``FairshareSchedulingPolicy`` is ignored.

        :stability: experimental
        '''
        ...


class _IUnmanagedComputeEnvironmentProxy(
    jsii.proxy_for(IComputeEnvironment), # type: ignore[misc]
):
    '''(experimental) Represents an UnmanagedComputeEnvironment.

    Batch will not provision instances on your behalf
    in this ComputeEvironment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IUnmanagedComputeEnvironment"

    @builtins.property
    @jsii.member(jsii_name="unmanagedvCPUs")
    def unmanagedv_cp_us(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The vCPUs this Compute Environment provides. Used only by the scheduler to schedule jobs in ``Queue``s that use ``FairshareSchedulingPolicy``s.

        **If this parameter is not provided on a fairshare queue, no capacity is reserved**;
        that is, the ``FairshareSchedulingPolicy`` is ignored.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unmanagedvCPUs"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUnmanagedComputeEnvironment).__jsii_proxy_class__ = lambda : _IUnmanagedComputeEnvironmentProxy


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.ImagePullPolicy")
class ImagePullPolicy(enum.Enum):
    '''(experimental) Determines when the image is pulled from the registry to launch a container.

    :stability: experimental
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) Every time the kubelet launches a container, the kubelet queries the container image registry to resolve the name to an image digest.

    If the kubelet has a container image with that exact digest cached locally,
    the kubelet uses its cached image; otherwise, the kubelet pulls the image with the resolved digest,
    and uses that image to launch the container.

    :see: https://docs.docker.com/engine/reference/commandline/pull/#pull-an-image-by-digest-immutable-identifier
    :stability: experimental
    '''
    IF_NOT_PRESENT = "IF_NOT_PRESENT"
    '''(experimental) The image is pulled only if it is not already present locally.

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) The kubelet does not try fetching the image.

    If the image is somehow already present locally,
    the kubelet attempts to start the container; otherwise, startup fails.
    See pre-pulled images for more details.

    :see: https://kubernetes.io/docs/concepts/containers/images/#pre-pulled-images
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.JobDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "job_definition_name": "jobDefinitionName",
        "parameters": "parameters",
        "retry_attempts": "retryAttempts",
        "retry_strategies": "retryStrategies",
        "scheduling_priority": "schedulingPriority",
        "timeout": "timeout",
    },
)
class JobDefinitionProps:
    def __init__(
        self,
        *,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence["RetryStrategy"]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''(experimental) Props common to all JobDefinitions.

        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            
            # parameters: Any
            # retry_strategy: batch_alpha.RetryStrategy
            
            job_definition_props = batch_alpha.JobDefinitionProps(
                job_definition_name="jobDefinitionName",
                parameters={
                    "parameters_key": parameters
                },
                retry_attempts=123,
                retry_strategies=[retry_strategy],
                scheduling_priority=123,
                timeout=cdk.Duration.minutes(30)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185df21ce496b49d7787089d80d45a0314ac702fd8d9d2f9ba4a623921534158)
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_strategies", value=retry_strategies, expected_type=type_hints["retry_strategies"])
            check_type(argname="argument scheduling_priority", value=scheduling_priority, expected_type=type_hints["scheduling_priority"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_strategies is not None:
            self._values["retry_strategies"] = retry_strategies
        if scheduling_priority is not None:
            self._values["scheduling_priority"] = scheduling_priority
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this job definition.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :default: none

        :see: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html#parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_strategies(self) -> typing.Optional[typing.List["RetryStrategy"]]:
        '''(experimental) Defines the retry behavior for this job.

        :default: - no ``RetryStrategy``

        :stability: experimental
        '''
        result = self._values.get("retry_strategies")
        return typing.cast(typing.Optional[typing.List["RetryStrategy"]], result)

    @builtins.property
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("scheduling_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :default: - no timeout

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IJobQueue)
class JobQueue(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.JobQueue",
):
    '''(experimental) JobQueues can receive Jobs, which are removed from the queue when sent to the linked ComputeEnvironment(s) to be executed.

    Jobs exit the queue in FIFO order unless a ``SchedulingPolicy`` is linked.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        import aws_cdk.aws_iam as iam
        
        # vpc: ec2.IVpc
        
        
        ecs_job = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256
            )
        )
        
        queue = batch.JobQueue(self, "JobQueue",
            compute_environments=[batch.OrderedComputeEnvironment(
                compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
                    vpc=vpc
                ),
                order=1
            )],
            priority=10
        )
        
        user = iam.User(self, "MyUser")
        ecs_job.grant_submit_job(user, queue)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_environments: typing.Optional[typing.Sequence[typing.Union["OrderedComputeEnvironment", typing.Dict[builtins.str, typing.Any]]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        scheduling_policy: typing.Optional[ISchedulingPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_environments: (experimental) The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 (EC2 or SPOT) or Fargate (FARGATE or FARGATE_SPOT); EC2 and Fargate compute environments can't be mixed. *Note*: All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue. Default: none
        :param enabled: (experimental) If the job queue is enabled, it is able to accept jobs. Otherwise, new jobs can't be added to the queue, but jobs already in the queue can finish. Default: true
        :param job_queue_name: (experimental) The name of the job queue. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_) Default: - no name
        :param priority: (experimental) The priority of the job queue. Job queues with a higher priority are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority of 10 is given scheduling preference over a job queue with a priority of 1. Default: 1
        :param scheduling_policy: (experimental) The SchedulingPolicy for this JobQueue. Instructs the Scheduler how to schedule different jobs. Default: - no scheduling policy

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48859d154c5df5d7c73c0dfbc7a6690f4c823f76e3ac97ea0a3302eb0eebbdcd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobQueueProps(
            compute_environments=compute_environments,
            enabled=enabled,
            job_queue_name=job_queue_name,
            priority=priority,
            scheduling_policy=scheduling_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobQueueArn")
    @builtins.classmethod
    def from_job_queue_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        job_queue_arn: builtins.str,
    ) -> IJobQueue:
        '''(experimental) refer to an existing JobQueue by its arn.

        :param scope: -
        :param id: -
        :param job_queue_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a0f379bd1cdd0d274ec73314e99f3a3964c617458143876c623482b8065bde)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_queue_arn", value=job_queue_arn, expected_type=type_hints["job_queue_arn"])
        return typing.cast(IJobQueue, jsii.sinvoke(cls, "fromJobQueueArn", [scope, id, job_queue_arn]))

    @jsii.member(jsii_name="addComputeEnvironment")
    def add_compute_environment(
        self,
        compute_environment: IComputeEnvironment,
        order: jsii.Number,
    ) -> None:
        '''(experimental) Add a ``ComputeEnvironment`` to this Queue.

        The Queue will prefer lower-order ``ComputeEnvironment``s.

        :param compute_environment: -
        :param order: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9cf974ef884ccf8550be3abbd8e5e805f821c2808c4d17b3c76d4617398d053)
            check_type(argname="argument compute_environment", value=compute_environment, expected_type=type_hints["compute_environment"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        return typing.cast(None, jsii.invoke(self, "addComputeEnvironment", [compute_environment, order]))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironments")
    def compute_environments(self) -> typing.List["OrderedComputeEnvironment"]:
        '''(experimental) The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job.
        Compute environments must be in the VALID state before you can associate them with a job queue.
        You can associate up to three compute environments with a job queue.
        All of the compute environments must be either EC2 (EC2 or SPOT) or Fargate (FARGATE or FARGATE_SPOT);
        EC2 and Fargate compute environments can't be mixed.

        *Note*: All compute environments that are associated with a job queue must share the same architecture.
        AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :stability: experimental
        '''
        return typing.cast(typing.List["OrderedComputeEnvironment"], jsii.get(self, "computeEnvironments"))

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueArn"))

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        '''(experimental) The name of the job queue.

        It can be up to 128 letters long.
        It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_)

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueName"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the job queue.

        Job queues with a higher priority are evaluated first when associated with the same compute environment.
        Priority is determined in descending order.
        For example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the job queue is enabled, it is able to accept jobs.

        Otherwise, new jobs can't be added to the queue, but jobs already in the queue can finish.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicy")
    def scheduling_policy(self) -> typing.Optional[ISchedulingPolicy]:
        '''(experimental) The SchedulingPolicy for this JobQueue.

        Instructs the Scheduler how to schedule different jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ISchedulingPolicy], jsii.get(self, "schedulingPolicy"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.JobQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environments": "computeEnvironments",
        "enabled": "enabled",
        "job_queue_name": "jobQueueName",
        "priority": "priority",
        "scheduling_policy": "schedulingPolicy",
    },
)
class JobQueueProps:
    def __init__(
        self,
        *,
        compute_environments: typing.Optional[typing.Sequence[typing.Union["OrderedComputeEnvironment", typing.Dict[builtins.str, typing.Any]]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        scheduling_policy: typing.Optional[ISchedulingPolicy] = None,
    ) -> None:
        '''(experimental) Props to configure a JobQueue.

        :param compute_environments: (experimental) The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 (EC2 or SPOT) or Fargate (FARGATE or FARGATE_SPOT); EC2 and Fargate compute environments can't be mixed. *Note*: All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue. Default: none
        :param enabled: (experimental) If the job queue is enabled, it is able to accept jobs. Otherwise, new jobs can't be added to the queue, but jobs already in the queue can finish. Default: true
        :param job_queue_name: (experimental) The name of the job queue. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_) Default: - no name
        :param priority: (experimental) The priority of the job queue. Job queues with a higher priority are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority of 10 is given scheduling preference over a job queue with a priority of 1. Default: 1
        :param scheduling_policy: (experimental) The SchedulingPolicy for this JobQueue. Instructs the Scheduler how to schedule different jobs. Default: - no scheduling policy

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            import aws_cdk.aws_iam as iam
            
            # vpc: ec2.IVpc
            
            
            ecs_job = batch.EcsJobDefinition(self, "JobDefn",
                container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                    image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                    memory=cdk.Size.mebibytes(2048),
                    cpu=256
                )
            )
            
            queue = batch.JobQueue(self, "JobQueue",
                compute_environments=[batch.OrderedComputeEnvironment(
                    compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
                        vpc=vpc
                    ),
                    order=1
                )],
                priority=10
            )
            
            user = iam.User(self, "MyUser")
            ecs_job.grant_submit_job(user, queue)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb77dbf4c08c80e90ddc79e26e0ff4218db45852e16cc5250c15de7d3041d3bf)
            check_type(argname="argument compute_environments", value=compute_environments, expected_type=type_hints["compute_environments"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument job_queue_name", value=job_queue_name, expected_type=type_hints["job_queue_name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument scheduling_policy", value=scheduling_policy, expected_type=type_hints["scheduling_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_environments is not None:
            self._values["compute_environments"] = compute_environments
        if enabled is not None:
            self._values["enabled"] = enabled
        if job_queue_name is not None:
            self._values["job_queue_name"] = job_queue_name
        if priority is not None:
            self._values["priority"] = priority
        if scheduling_policy is not None:
            self._values["scheduling_policy"] = scheduling_policy

    @builtins.property
    def compute_environments(
        self,
    ) -> typing.Optional[typing.List["OrderedComputeEnvironment"]]:
        '''(experimental) The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job.
        Compute environments must be in the VALID state before you can associate them with a job queue.
        You can associate up to three compute environments with a job queue.
        All of the compute environments must be either EC2 (EC2 or SPOT) or Fargate (FARGATE or FARGATE_SPOT);
        EC2 and Fargate compute environments can't be mixed.

        *Note*: All compute environments that are associated with a job queue must share the same architecture.
        AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("compute_environments")
        return typing.cast(typing.Optional[typing.List["OrderedComputeEnvironment"]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the job queue is enabled, it is able to accept jobs.

        Otherwise, new jobs can't be added to the queue, but jobs already in the queue can finish.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job queue.

        It can be up to 128 letters long.
        It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_)

        :default: - no name

        :stability: experimental
        '''
        result = self._values.get("job_queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of the job queue.

        Job queues with a higher priority are evaluated first when associated with the same compute environment.
        Priority is determined in descending order.
        For example, a job queue with a priority of 10 is given scheduling preference over a job queue with a priority of 1.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def scheduling_policy(self) -> typing.Optional[ISchedulingPolicy]:
        '''(experimental) The SchedulingPolicy for this JobQueue.

        Instructs the Scheduler how to schedule different jobs.

        :default: - no scheduling policy

        :stability: experimental
        '''
        result = self._values.get("scheduling_policy")
        return typing.cast(typing.Optional[ISchedulingPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxParameters(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.LinuxParameters",
):
    '''(experimental) Linux-specific options that are applied to the container.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        import aws_cdk as cdk
        
        # size: cdk.Size
        
        linux_parameters = batch_alpha.LinuxParameters(self, "MyLinuxParameters",
            init_process_enabled=False,
            max_swap=size,
            shared_memory_size=size,
            swappiness=123
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        init_process_enabled: typing.Optional[builtins.bool] = None,
        max_swap: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        shared_memory_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        swappiness: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Constructs a new instance of the LinuxParameters class.

        :param scope: -
        :param id: -
        :param init_process_enabled: (experimental) Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
        :param max_swap: (experimental) The total amount of swap memory a container can use. This parameter will be translated to the --memory-swap option to docker run. This parameter is only supported when you are using the EC2 launch type. Accepted values are positive integers. Default: No swap.
        :param shared_memory_size: (experimental) The value for the size of the /dev/shm volume. Default: No shared memory.
        :param swappiness: (experimental) This allows you to tune a container's memory swappiness behavior. This parameter maps to the --memory-swappiness option to docker run. The swappiness relates to the kernel's tendency to swap memory. A value of 0 will cause swapping to not happen unless absolutely necessary. A value of 100 will cause pages to be swapped very aggressively. This parameter is only supported when you are using the EC2 launch type. Accepted values are whole numbers between 0 and 100. If a value is not specified for maxSwap then this parameter is ignored. Default: 60

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfa1843a39cb26bea1804dabeb0330c79b6698e9cf52250cd4b3492c5b3e4dfc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LinuxParametersProps(
            init_process_enabled=init_process_enabled,
            max_swap=max_swap,
            shared_memory_size=shared_memory_size,
            swappiness=swappiness,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDevices")
    def add_devices(self, *device: Device) -> None:
        '''(experimental) Adds one or more host devices to a container.

        :param device: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c96c9da432c3bb02107313dc0610d870117421ad312e09371274d5672f2c736)
            check_type(argname="argument device", value=device, expected_type=typing.Tuple[type_hints["device"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addDevices", [*device]))

    @jsii.member(jsii_name="addTmpfs")
    def add_tmpfs(self, *tmpfs: "Tmpfs") -> None:
        '''(experimental) Specifies the container path, mount options, and size (in MiB) of the tmpfs mount for a container.

        Only works with EC2 launch type.

        :param tmpfs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6a261a81aa3b99900849aa34269258580c84910ad287d5c3f29a9d8b18b8d79)
            check_type(argname="argument tmpfs", value=tmpfs, expected_type=typing.Tuple[type_hints["tmpfs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addTmpfs", [*tmpfs]))

    @jsii.member(jsii_name="renderLinuxParameters")
    def render_linux_parameters(
        self,
    ) -> _aws_cdk_aws_batch_ceddda9d.CfnJobDefinition.LinuxParametersProperty:
        '''(experimental) Renders the Linux parameters to the Batch version of this resource, which does not have 'capabilities' and requires tmpfs.containerPath to be defined.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_batch_ceddda9d.CfnJobDefinition.LinuxParametersProperty, jsii.invoke(self, "renderLinuxParameters", []))

    @builtins.property
    @jsii.member(jsii_name="devices")
    def _devices(self) -> typing.List[Device]:
        '''(experimental) Device mounts.

        :stability: experimental
        '''
        return typing.cast(typing.List[Device], jsii.get(self, "devices"))

    @builtins.property
    @jsii.member(jsii_name="tmpfs")
    def _tmpfs(self) -> typing.List["Tmpfs"]:
        '''(experimental) TmpFs mounts.

        :stability: experimental
        '''
        return typing.cast(typing.List["Tmpfs"], jsii.get(self, "tmpfs"))

    @builtins.property
    @jsii.member(jsii_name="initProcessEnabled")
    def _init_process_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the init process is enabled.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "initProcessEnabled"))

    @builtins.property
    @jsii.member(jsii_name="maxSwap")
    def _max_swap(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The max swap memory.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "maxSwap"))

    @builtins.property
    @jsii.member(jsii_name="sharedMemorySize")
    def _shared_memory_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The shared memory size (in MiB).

        Not valid for Fargate launch type

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "sharedMemorySize"))

    @builtins.property
    @jsii.member(jsii_name="swappiness")
    def _swappiness(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The swappiness behavior.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "swappiness"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.LinuxParametersProps",
    jsii_struct_bases=[],
    name_mapping={
        "init_process_enabled": "initProcessEnabled",
        "max_swap": "maxSwap",
        "shared_memory_size": "sharedMemorySize",
        "swappiness": "swappiness",
    },
)
class LinuxParametersProps:
    def __init__(
        self,
        *,
        init_process_enabled: typing.Optional[builtins.bool] = None,
        max_swap: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        shared_memory_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        swappiness: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The properties for defining Linux-specific options that are applied to the container.

        :param init_process_enabled: (experimental) Specifies whether to run an init process inside the container that forwards signals and reaps processes. Default: false
        :param max_swap: (experimental) The total amount of swap memory a container can use. This parameter will be translated to the --memory-swap option to docker run. This parameter is only supported when you are using the EC2 launch type. Accepted values are positive integers. Default: No swap.
        :param shared_memory_size: (experimental) The value for the size of the /dev/shm volume. Default: No shared memory.
        :param swappiness: (experimental) This allows you to tune a container's memory swappiness behavior. This parameter maps to the --memory-swappiness option to docker run. The swappiness relates to the kernel's tendency to swap memory. A value of 0 will cause swapping to not happen unless absolutely necessary. A value of 100 will cause pages to be swapped very aggressively. This parameter is only supported when you are using the EC2 launch type. Accepted values are whole numbers between 0 and 100. If a value is not specified for maxSwap then this parameter is ignored. Default: 60

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            
            # size: cdk.Size
            
            linux_parameters_props = batch_alpha.LinuxParametersProps(
                init_process_enabled=False,
                max_swap=size,
                shared_memory_size=size,
                swappiness=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7520d82136e04b588afff3e9af7597b6b89fc591c1861bd204d203d4d07823f7)
            check_type(argname="argument init_process_enabled", value=init_process_enabled, expected_type=type_hints["init_process_enabled"])
            check_type(argname="argument max_swap", value=max_swap, expected_type=type_hints["max_swap"])
            check_type(argname="argument shared_memory_size", value=shared_memory_size, expected_type=type_hints["shared_memory_size"])
            check_type(argname="argument swappiness", value=swappiness, expected_type=type_hints["swappiness"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if init_process_enabled is not None:
            self._values["init_process_enabled"] = init_process_enabled
        if max_swap is not None:
            self._values["max_swap"] = max_swap
        if shared_memory_size is not None:
            self._values["shared_memory_size"] = shared_memory_size
        if swappiness is not None:
            self._values["swappiness"] = swappiness

    @builtins.property
    def init_process_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to run an init process inside the container that forwards signals and reaps processes.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("init_process_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def max_swap(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The total amount of swap memory a container can use.

        This parameter
        will be translated to the --memory-swap option to docker run.

        This parameter is only supported when you are using the EC2 launch type.
        Accepted values are positive integers.

        :default: No swap.

        :stability: experimental
        '''
        result = self._values.get("max_swap")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def shared_memory_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The value for the size of the /dev/shm volume.

        :default: No shared memory.

        :stability: experimental
        '''
        result = self._values.get("shared_memory_size")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], result)

    @builtins.property
    def swappiness(self) -> typing.Optional[jsii.Number]:
        '''(experimental) This allows you to tune a container's memory swappiness behavior.

        This parameter
        maps to the --memory-swappiness option to docker run. The swappiness relates
        to the kernel's tendency to swap memory. A value of 0 will cause swapping to
        not happen unless absolutely necessary. A value of 100 will cause pages to
        be swapped very aggressively.

        This parameter is only supported when you are using the EC2 launch type.
        Accepted values are whole numbers between 0 and 100. If a value is not
        specified for maxSwap then this parameter is ignored.

        :default: 60

        :stability: experimental
        '''
        result = self._values.get("swappiness")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxParametersProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.ManagedComputeEnvironmentProps",
    jsii_struct_bases=[ComputeEnvironmentProps],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "enabled": "enabled",
        "service_role": "serviceRole",
        "vpc": "vpc",
        "maxv_cpus": "maxvCpus",
        "replace_compute_environment": "replaceComputeEnvironment",
        "security_groups": "securityGroups",
        "spot": "spot",
        "terminate_on_update": "terminateOnUpdate",
        "update_timeout": "updateTimeout",
        "update_to_latest_image_version": "updateToLatestImageVersion",
        "vpc_subnets": "vpcSubnets",
    },
)
class ManagedComputeEnvironmentProps(ComputeEnvironmentProps):
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Props for a ManagedComputeEnvironment.

        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_ec2 as ec2
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # vpc: ec2.Vpc
            
            managed_compute_environment_props = batch_alpha.ManagedComputeEnvironmentProps(
                vpc=vpc,
            
                # the properties below are optional
                compute_environment_name="computeEnvironmentName",
                enabled=False,
                maxv_cpus=123,
                replace_compute_environment=False,
                security_groups=[security_group],
                service_role=role,
                spot=False,
                terminate_on_update=False,
                update_timeout=cdk.Duration.minutes(30),
                update_to_latest_image_version=False,
                vpc_subnets=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__185ace7c9ac3fc3c89503d419f45772a577131204fd52b9fd049cd3aff542fd8)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
            check_type(argname="argument replace_compute_environment", value=replace_compute_environment, expected_type=type_hints["replace_compute_environment"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument terminate_on_update", value=terminate_on_update, expected_type=type_hints["terminate_on_update"])
            check_type(argname="argument update_timeout", value=update_timeout, expected_type=type_hints["update_timeout"])
            check_type(argname="argument update_to_latest_image_version", value=update_to_latest_image_version, expected_type=type_hints["update_to_latest_image_version"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_role is not None:
            self._values["service_role"] = service_role
        if maxv_cpus is not None:
            self._values["maxv_cpus"] = maxv_cpus
        if replace_compute_environment is not None:
            self._values["replace_compute_environment"] = replace_compute_environment
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if terminate_on_update is not None:
            self._values["terminate_on_update"] = terminate_on_update
        if update_timeout is not None:
            self._values["update_timeout"] = update_timeout
        if update_to_latest_image_version is not None:
            self._values["update_to_latest_image_version"] = update_to_latest_image_version
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ComputeEnvironment.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC in which this Compute Environment will launch Instances.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :default: 256

        :stability: experimental
        '''
        result = self._values.get("maxv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
        :stability: experimental
        '''
        result = self._values.get("replace_compute_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :default: new security groups will be created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("terminate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :default: 30 minutes

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("update_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_to_latest_image_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The VPC Subnets this Compute Environment will launch instances in.

        :default: new subnets will be created

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IManagedEc2EcsComputeEnvironment, IManagedComputeEnvironment, IComputeEnvironment)
class ManagedEc2EcsComputeEnvironment(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.ManagedEc2EcsComputeEnvironment",
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on EC2 instances.

    :stability: experimental
    :resource: AWS::Batch::ComputeEnvironment
    :exampleMetadata: infused

    Example::

        # compute_env: batch.IManagedEc2EcsComputeEnvironment
        vpc = ec2.Vpc(self, "VPC")
        compute_env.add_instance_class(ec2.InstanceClass.M5AD)
        # Or, specify it on the constructor:
        batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
            vpc=vpc,
            instance_classes=[ec2.InstanceClass.R4]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        allocation_strategy: typing.Optional[AllocationStrategy] = None,
        images: typing.Optional[typing.Sequence[typing.Union[EcsMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
        launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
        minv_cpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
        spot_bid_percentage: typing.Optional[jsii.Number] = None,
        spot_fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param allocation_strategy: (experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated. Default: - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances, ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.
        :param images: (experimental) Configure which AMIs this Compute Environment can launch. If you specify this property with only ``image`` specified, then the ``imageType`` will default to ``ECS_AL2``. *If your image needs GPU resources, specify ``ECS_AL2_NVIDIA``; otherwise, the instances will not be able to properly join the ComputeEnvironment*. Default: - ECS_AL2 for non-GPU instances, ECS_AL2_NVIDIA for GPU instances
        :param instance_classes: (experimental) The instance classes that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Batch will automatically choose the instance size. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param instance_role: (experimental) The execution Role that instances launched by this Compute Environment will use. Default: - a role will be created
        :param instance_types: (experimental) The instance types that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param launch_template: (experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances. *Note*: if ``securityGroups`` is specified on both your launch template and this Compute Environment, **the ``securityGroup``s on the Compute Environment override the ones on the launch template. Default: no launch template
        :param minv_cpus: (experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED. Default: 0
        :param placement_group: (experimental) The EC2 placement group to associate with your compute resources. If you intend to submit multi-node parallel jobs to this Compute Environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. Default: - no placement group
        :param spot_bid_percentage: (experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Instance. You always pay the lowest market price and never more than your maximum percentage. For most use cases, Batch recommends leaving this field empty. Implies ``spot == true`` if set Default: 100%
        :param spot_fleet_role: (experimental) The service-linked role that Spot Fleet needs to launch instances on your behalf. Default: - a new role will be created
        :param use_optimal_instance_classes: (experimental) Whether or not to use batch's optimal instance type. The optimal instance type is equivalent to adding the C4, M4, and R4 instance classes. You can specify other instance classes (of the same architecture) in addition to the optimal instance classes. Default: true
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created
        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ecd7c9bbba4d9e441a13ce54d8df8673c886cac2f04a4fc28344c39c2efb9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ManagedEc2EcsComputeEnvironmentProps(
            allocation_strategy=allocation_strategy,
            images=images,
            instance_classes=instance_classes,
            instance_role=instance_role,
            instance_types=instance_types,
            launch_template=launch_template,
            minv_cpus=minv_cpus,
            placement_group=placement_group,
            spot_bid_percentage=spot_bid_percentage,
            spot_fleet_role=spot_fleet_role,
            use_optimal_instance_classes=use_optimal_instance_classes,
            vpc=vpc,
            maxv_cpus=maxv_cpus,
            replace_compute_environment=replace_compute_environment,
            security_groups=security_groups,
            spot=spot,
            terminate_on_update=terminate_on_update,
            update_timeout=update_timeout,
            update_to_latest_image_version=update_to_latest_image_version,
            vpc_subnets=vpc_subnets,
            compute_environment_name=compute_environment_name,
            enabled=enabled,
            service_role=service_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromManagedEc2EcsComputeEnvironmentArn")
    @builtins.classmethod
    def from_managed_ec2_ecs_compute_environment_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        managed_ec2_ecs_compute_environment_arn: builtins.str,
    ) -> IManagedEc2EcsComputeEnvironment:
        '''(experimental) refer to an existing ComputeEnvironment by its arn.

        :param scope: -
        :param id: -
        :param managed_ec2_ecs_compute_environment_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae86bff947bdb5fa9c0b6f95425875a909080e2645a02dbd4672a7846b669398)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_ec2_ecs_compute_environment_arn", value=managed_ec2_ecs_compute_environment_arn, expected_type=type_hints["managed_ec2_ecs_compute_environment_arn"])
        return typing.cast(IManagedEc2EcsComputeEnvironment, jsii.sinvoke(cls, "fromManagedEc2EcsComputeEnvironmentArn", [scope, id, managed_ec2_ecs_compute_environment_arn]))

    @jsii.member(jsii_name="addInstanceClass")
    def add_instance_class(
        self,
        instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
    ) -> None:
        '''(experimental) Add an instance class to this compute environment.

        :param instance_class: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4154c464d82dcda19d60e2a16fbcfc483e094fa18217992c523b2b4a4ce49bc6)
            check_type(argname="argument instance_class", value=instance_class, expected_type=type_hints["instance_class"])
        return typing.cast(None, jsii.invoke(self, "addInstanceClass", [instance_class]))

    @jsii.member(jsii_name="addInstanceType")
    def add_instance_type(
        self,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    ) -> None:
        '''(experimental) Add an instance type to this compute environment.

        :param instance_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__171399bef64d69b36e805fd95356d1f14d7d16814d59dea069290961da787252)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
        return typing.cast(None, jsii.invoke(self, "addInstanceType", [instance_type]))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        '''(experimental) The ARN of this compute environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        '''(experimental) The name of the ComputeEnvironment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="instanceClasses")
    def instance_classes(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]:
        '''(experimental) The instance classes that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.
        Batch will automatically choose the size.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass], jsii.get(self, "instanceClasses"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType], jsii.get(self, "instanceTypes"))

    @builtins.property
    @jsii.member(jsii_name="maxvCpus")
    def maxv_cpus(self) -> jsii.Number:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "maxvCpus"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''(experimental) TagManager to set, remove and format tags.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AllocationStrategy], jsii.get(self, "allocationStrategy"))

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.Optional[typing.List[EcsMachineImage]]:
        '''(experimental) Configure which AMIs this Compute Environment can launch.

        Leave this ``undefined`` to allow Batch to choose the latest AMIs it supports for each instance that it launches.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[EcsMachineImage]], jsii.get(self, "images"))

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution Role that instances launched by this Compute Environment will use.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "instanceRole"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances.

        *Note*: if ``securityGroups`` is specified on both your
        launch template and this Compute Environment, **the
        ``securityGroup``s on the Compute Environment override the
        ones on the launch template.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate], jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="minvCpus")
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minvCpus"))

    @builtins.property
    @jsii.member(jsii_name="placementGroup")
    def placement_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup]:
        '''(experimental) The EC2 placement group to associate with your compute resources.

        If you intend to submit multi-node parallel jobs to this Compute Environment,
        you should consider creating a cluster placement group and associate it with your compute resources.
        This keeps your multi-node parallel job on a logical grouping of instances
        within a single Availability Zone with high network flow potential.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup], jsii.get(self, "placementGroup"))

    @builtins.property
    @jsii.member(jsii_name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "replaceComputeEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "serviceRole"))

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "spot"))

    @builtins.property
    @jsii.member(jsii_name="spotBidPercentage")
    def spot_bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

        For example, if your maximum percentage is 20%, the Spot price must be
        less than 20% of the current On-Demand price for that Instance.
        You always pay the lowest market price and never more than your maximum percentage.
        For most use cases, Batch recommends leaving this field empty.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidPercentage"))

    @builtins.property
    @jsii.member(jsii_name="spotFleetRole")
    def spot_fleet_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The service-linked role that Spot Fleet needs to launch instances on your behalf.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "spotFleetRole"))

    @builtins.property
    @jsii.member(jsii_name="terminateOnUpdate")
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "terminateOnUpdate"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeout")
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "updateTimeout"))

    @builtins.property
    @jsii.member(jsii_name="updateToLatestImageVersion")
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "updateToLatestImageVersion"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.ManagedEc2EcsComputeEnvironmentProps",
    jsii_struct_bases=[ManagedComputeEnvironmentProps],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "enabled": "enabled",
        "service_role": "serviceRole",
        "vpc": "vpc",
        "maxv_cpus": "maxvCpus",
        "replace_compute_environment": "replaceComputeEnvironment",
        "security_groups": "securityGroups",
        "spot": "spot",
        "terminate_on_update": "terminateOnUpdate",
        "update_timeout": "updateTimeout",
        "update_to_latest_image_version": "updateToLatestImageVersion",
        "vpc_subnets": "vpcSubnets",
        "allocation_strategy": "allocationStrategy",
        "images": "images",
        "instance_classes": "instanceClasses",
        "instance_role": "instanceRole",
        "instance_types": "instanceTypes",
        "launch_template": "launchTemplate",
        "minv_cpus": "minvCpus",
        "placement_group": "placementGroup",
        "spot_bid_percentage": "spotBidPercentage",
        "spot_fleet_role": "spotFleetRole",
        "use_optimal_instance_classes": "useOptimalInstanceClasses",
    },
)
class ManagedEc2EcsComputeEnvironmentProps(ManagedComputeEnvironmentProps):
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        allocation_strategy: typing.Optional[AllocationStrategy] = None,
        images: typing.Optional[typing.Sequence[typing.Union[EcsMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
        launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
        minv_cpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
        spot_bid_percentage: typing.Optional[jsii.Number] = None,
        spot_fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Props for a ManagedEc2EcsComputeEnvironment.

        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created
        :param allocation_strategy: (experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated. Default: - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances, ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.
        :param images: (experimental) Configure which AMIs this Compute Environment can launch. If you specify this property with only ``image`` specified, then the ``imageType`` will default to ``ECS_AL2``. *If your image needs GPU resources, specify ``ECS_AL2_NVIDIA``; otherwise, the instances will not be able to properly join the ComputeEnvironment*. Default: - ECS_AL2 for non-GPU instances, ECS_AL2_NVIDIA for GPU instances
        :param instance_classes: (experimental) The instance classes that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Batch will automatically choose the instance size. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param instance_role: (experimental) The execution Role that instances launched by this Compute Environment will use. Default: - a role will be created
        :param instance_types: (experimental) The instance types that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param launch_template: (experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances. *Note*: if ``securityGroups`` is specified on both your launch template and this Compute Environment, **the ``securityGroup``s on the Compute Environment override the ones on the launch template. Default: no launch template
        :param minv_cpus: (experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED. Default: 0
        :param placement_group: (experimental) The EC2 placement group to associate with your compute resources. If you intend to submit multi-node parallel jobs to this Compute Environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. Default: - no placement group
        :param spot_bid_percentage: (experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Instance. You always pay the lowest market price and never more than your maximum percentage. For most use cases, Batch recommends leaving this field empty. Implies ``spot == true`` if set Default: 100%
        :param spot_fleet_role: (experimental) The service-linked role that Spot Fleet needs to launch instances on your behalf. Default: - a new role will be created
        :param use_optimal_instance_classes: (experimental) Whether or not to use batch's optimal instance type. The optimal instance type is equivalent to adding the C4, M4, and R4 instance classes. You can specify other instance classes (of the same architecture) in addition to the optimal instance classes. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # compute_env: batch.IManagedEc2EcsComputeEnvironment
            vpc = ec2.Vpc(self, "VPC")
            compute_env.add_instance_class(ec2.InstanceClass.M5AD)
            # Or, specify it on the constructor:
            batch.ManagedEc2EcsComputeEnvironment(self, "myEc2ComputeEnv",
                vpc=vpc,
                instance_classes=[ec2.InstanceClass.R4]
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80804fff92abbb5cf4045718bdc81911bb4157bf5a171323aa7780cf0a60ab4d)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
            check_type(argname="argument replace_compute_environment", value=replace_compute_environment, expected_type=type_hints["replace_compute_environment"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument terminate_on_update", value=terminate_on_update, expected_type=type_hints["terminate_on_update"])
            check_type(argname="argument update_timeout", value=update_timeout, expected_type=type_hints["update_timeout"])
            check_type(argname="argument update_to_latest_image_version", value=update_to_latest_image_version, expected_type=type_hints["update_to_latest_image_version"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument instance_classes", value=instance_classes, expected_type=type_hints["instance_classes"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument minv_cpus", value=minv_cpus, expected_type=type_hints["minv_cpus"])
            check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
            check_type(argname="argument spot_bid_percentage", value=spot_bid_percentage, expected_type=type_hints["spot_bid_percentage"])
            check_type(argname="argument spot_fleet_role", value=spot_fleet_role, expected_type=type_hints["spot_fleet_role"])
            check_type(argname="argument use_optimal_instance_classes", value=use_optimal_instance_classes, expected_type=type_hints["use_optimal_instance_classes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_role is not None:
            self._values["service_role"] = service_role
        if maxv_cpus is not None:
            self._values["maxv_cpus"] = maxv_cpus
        if replace_compute_environment is not None:
            self._values["replace_compute_environment"] = replace_compute_environment
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if terminate_on_update is not None:
            self._values["terminate_on_update"] = terminate_on_update
        if update_timeout is not None:
            self._values["update_timeout"] = update_timeout
        if update_to_latest_image_version is not None:
            self._values["update_to_latest_image_version"] = update_to_latest_image_version
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocation_strategy is not None:
            self._values["allocation_strategy"] = allocation_strategy
        if images is not None:
            self._values["images"] = images
        if instance_classes is not None:
            self._values["instance_classes"] = instance_classes
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if minv_cpus is not None:
            self._values["minv_cpus"] = minv_cpus
        if placement_group is not None:
            self._values["placement_group"] = placement_group
        if spot_bid_percentage is not None:
            self._values["spot_bid_percentage"] = spot_bid_percentage
        if spot_fleet_role is not None:
            self._values["spot_fleet_role"] = spot_fleet_role
        if use_optimal_instance_classes is not None:
            self._values["use_optimal_instance_classes"] = use_optimal_instance_classes

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ComputeEnvironment.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC in which this Compute Environment will launch Instances.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :default: 256

        :stability: experimental
        '''
        result = self._values.get("maxv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
        :stability: experimental
        '''
        result = self._values.get("replace_compute_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :default: new security groups will be created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("terminate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :default: 30 minutes

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("update_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_to_latest_image_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The VPC Subnets this Compute Environment will launch instances in.

        :default: new subnets will be created

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated.

        :default:

        - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances,
        ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.

        :stability: experimental
        '''
        result = self._values.get("allocation_strategy")
        return typing.cast(typing.Optional[AllocationStrategy], result)

    @builtins.property
    def images(self) -> typing.Optional[typing.List[EcsMachineImage]]:
        '''(experimental) Configure which AMIs this Compute Environment can launch.

        If you specify this property with only ``image`` specified, then the
        ``imageType`` will default to ``ECS_AL2``. *If your image needs GPU resources,
        specify ``ECS_AL2_NVIDIA``; otherwise, the instances will not be able to properly
        join the ComputeEnvironment*.

        :default: - ECS_AL2 for non-GPU instances, ECS_AL2_NVIDIA for GPU instances

        :stability: experimental
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List[EcsMachineImage]], result)

    @builtins.property
    def instance_classes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]]:
        '''(experimental) The instance classes that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.
        Batch will automatically choose the instance size.

        :default: - the instances Batch considers will be used (currently C4, M4, and R4)

        :stability: experimental
        '''
        result = self._values.get("instance_classes")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution Role that instances launched by this Compute Environment will use.

        :default: - a role will be created

        :stability: experimental
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :default: - the instances Batch considers will be used (currently C4, M4, and R4)

        :stability: experimental
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances.

        *Note*: if ``securityGroups`` is specified on both your
        launch template and this Compute Environment, **the
        ``securityGroup``s on the Compute Environment override the
        ones on the launch template.

        :default: no launch template

        :stability: experimental
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate], result)

    @builtins.property
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("minv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup]:
        '''(experimental) The EC2 placement group to associate with your compute resources.

        If you intend to submit multi-node parallel jobs to this Compute Environment,
        you should consider creating a cluster placement group and associate it with your compute resources.
        This keeps your multi-node parallel job on a logical grouping of instances
        within a single Availability Zone with high network flow potential.

        :default: - no placement group

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html
        :stability: experimental
        '''
        result = self._values.get("placement_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup], result)

    @builtins.property
    def spot_bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

        For example, if your maximum percentage is 20%, the Spot price must be
        less than 20% of the current On-Demand price for that Instance.
        You always pay the lowest market price and never more than your maximum percentage.
        For most use cases, Batch recommends leaving this field empty.

        Implies ``spot == true`` if set

        :default: 100%

        :stability: experimental
        '''
        result = self._values.get("spot_bid_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def spot_fleet_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The service-linked role that Spot Fleet needs to launch instances on your behalf.

        :default: - a new role will be created

        :see: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
        :stability: experimental
        '''
        result = self._values.get("spot_fleet_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def use_optimal_instance_classes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use batch's optimal instance type.

        The optimal instance type is equivalent to adding the
        C4, M4, and R4 instance classes. You can specify other instance classes
        (of the same architecture) in addition to the optimal instance classes.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("use_optimal_instance_classes")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedEc2EcsComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IManagedComputeEnvironment, IComputeEnvironment)
class ManagedEc2EksComputeEnvironment(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.ManagedEc2EksComputeEnvironment",
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on EC2 instances.

    :stability: experimental
    :resource: AWS::Batch::ComputeEnvironment
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_ec2 as ec2
        from aws_cdk import aws_eks as eks
        from aws_cdk import aws_iam as iam
        
        # cluster: eks.Cluster
        # instance_type: ec2.InstanceType
        # launch_template: ec2.LaunchTemplate
        # machine_image: ec2.IMachineImage
        # placement_group: ec2.PlacementGroup
        # role: iam.Role
        # security_group: ec2.SecurityGroup
        # subnet: ec2.Subnet
        # subnet_filter: ec2.SubnetFilter
        # vpc: ec2.Vpc
        
        managed_ec2_eks_compute_environment = batch_alpha.ManagedEc2EksComputeEnvironment(self, "MyManagedEc2EksComputeEnvironment",
            eks_cluster=cluster,
            kubernetes_namespace="kubernetesNamespace",
            vpc=vpc,
        
            # the properties below are optional
            allocation_strategy=batch_alpha.AllocationStrategy.BEST_FIT,
            compute_environment_name="computeEnvironmentName",
            enabled=False,
            images=[batch_alpha.EksMachineImage(
                image=machine_image,
                image_type=batch_alpha.EksMachineImageType.EKS_AL2
            )],
            instance_classes=[ec2.InstanceClass.STANDARD3],
            instance_role=role,
            instance_types=[instance_type],
            launch_template=launch_template,
            maxv_cpus=123,
            minv_cpus=123,
            placement_group=placement_group,
            replace_compute_environment=False,
            security_groups=[security_group],
            service_role=role,
            spot=False,
            spot_bid_percentage=123,
            terminate_on_update=False,
            update_timeout=cdk.Duration.minutes(30),
            update_to_latest_image_version=False,
            use_optimal_instance_classes=False,
            vpc_subnets=ec2.SubnetSelection(
                availability_zones=["availabilityZones"],
                one_per_az=False,
                subnet_filters=[subnet_filter],
                subnet_group_name="subnetGroupName",
                subnets=[subnet],
                subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        eks_cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
        kubernetes_namespace: builtins.str,
        allocation_strategy: typing.Optional[AllocationStrategy] = None,
        images: typing.Optional[typing.Sequence[typing.Union[EksMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
        launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
        minv_cpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
        spot_bid_percentage: typing.Optional[jsii.Number] = None,
        use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param eks_cluster: (experimental) The cluster that backs this Compute Environment. Required for Compute Environments running Kubernetes jobs. Please ensure that you have followed the steps at https://docs.aws.amazon.com/batch/latest/userguide/getting-started-eks.html before attempting to deploy a ``ManagedEc2EksComputeEnvironment`` that uses this cluster. If you do not follow the steps in the link, the deployment fail with a message that the compute environment did not stabilize.
        :param kubernetes_namespace: (experimental) The namespace of the Cluster.
        :param allocation_strategy: (experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated. Default: - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances, ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.
        :param images: (experimental) Configure which AMIs this Compute Environment can launch. Default: If ``imageKubernetesVersion`` is specified, - EKS_AL2 for non-GPU instances, EKS_AL2_NVIDIA for GPU instances, Otherwise, - ECS_AL2 for non-GPU instances, ECS_AL2_NVIDIA for GPU instances,
        :param instance_classes: (experimental) The instance types that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Batch will automatically choose the instance size. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param instance_role: (experimental) The execution Role that instances launched by this Compute Environment will use. Default: - a role will be created
        :param instance_types: (experimental) The instance types that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param launch_template: (experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances. *Note*: if ``securityGroups`` is specified on both your launch template and this Compute Environment, **the ``securityGroup``s on the Compute Environment override the ones on the launch template.** Default: - no launch template
        :param minv_cpus: (experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED. Default: 0
        :param placement_group: (experimental) The EC2 placement group to associate with your compute resources. If you intend to submit multi-node parallel jobs to this Compute Environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. Default: - no placement group
        :param spot_bid_percentage: (experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Instance. You always pay the lowest market price and never more than your maximum percentage. For most use cases, Batch recommends leaving this field empty. Implies ``spot == true`` if set Default: - 100%
        :param use_optimal_instance_classes: (experimental) Whether or not to use batch's optimal instance type. The optimal instance type is equivalent to adding the C4, M4, and R4 instance classes. You can specify other instance classes (of the same architecture) in addition to the optimal instance classes. Default: true
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created
        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ea4c86fae84c6f923bd126a2028d7db5eafaa0e2097047cba9c9aeb90eb98a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ManagedEc2EksComputeEnvironmentProps(
            eks_cluster=eks_cluster,
            kubernetes_namespace=kubernetes_namespace,
            allocation_strategy=allocation_strategy,
            images=images,
            instance_classes=instance_classes,
            instance_role=instance_role,
            instance_types=instance_types,
            launch_template=launch_template,
            minv_cpus=minv_cpus,
            placement_group=placement_group,
            spot_bid_percentage=spot_bid_percentage,
            use_optimal_instance_classes=use_optimal_instance_classes,
            vpc=vpc,
            maxv_cpus=maxv_cpus,
            replace_compute_environment=replace_compute_environment,
            security_groups=security_groups,
            spot=spot,
            terminate_on_update=terminate_on_update,
            update_timeout=update_timeout,
            update_to_latest_image_version=update_to_latest_image_version,
            vpc_subnets=vpc_subnets,
            compute_environment_name=compute_environment_name,
            enabled=enabled,
            service_role=service_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addInstanceClass")
    def add_instance_class(
        self,
        instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
    ) -> None:
        '''(experimental) Add an instance class to this compute environment.

        :param instance_class: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a3443238d0f0e49d52ab4a6908cebaa74e2926338df9811a0765b4c5a6d9e71)
            check_type(argname="argument instance_class", value=instance_class, expected_type=type_hints["instance_class"])
        return typing.cast(None, jsii.invoke(self, "addInstanceClass", [instance_class]))

    @jsii.member(jsii_name="addInstanceType")
    def add_instance_type(
        self,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    ) -> None:
        '''(experimental) Add an instance type to this compute environment.

        :param instance_type: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db374276009006a09b5e278249c46716cd0ad60f136c2d8935f32d132fe35747)
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
        return typing.cast(None, jsii.invoke(self, "addInstanceType", [instance_type]))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        '''(experimental) The ARN of this compute environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        '''(experimental) The name of the ComputeEnvironment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="eksCluster")
    def eks_cluster(self) -> _aws_cdk_aws_eks_ceddda9d.ICluster:
        '''(experimental) The cluster that backs this Compute Environment. Required for Compute Environments running Kubernetes jobs.

        Please ensure that you have followed the steps at

        https://docs.aws.amazon.com/batch/latest/userguide/getting-started-eks.html

        before attempting to deploy a ``ManagedEc2EksComputeEnvironment`` that uses this cluster.
        If you do not follow the steps in the link, the deployment fail with a message that the
        compute environment did not stabilize.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.ICluster, jsii.get(self, "eksCluster"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="instanceClasses")
    def instance_classes(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass], jsii.get(self, "instanceClasses"))

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType], jsii.get(self, "instanceTypes"))

    @builtins.property
    @jsii.member(jsii_name="maxvCpus")
    def maxv_cpus(self) -> jsii.Number:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "maxvCpus"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''(experimental) TagManager to set, remove and format tags.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="allocationStrategy")
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[AllocationStrategy], jsii.get(self, "allocationStrategy"))

    @builtins.property
    @jsii.member(jsii_name="images")
    def images(self) -> typing.Optional[typing.List[EksMachineImage]]:
        '''(experimental) Configure which AMIs this Compute Environment can launch.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[EksMachineImage]], jsii.get(self, "images"))

    @builtins.property
    @jsii.member(jsii_name="instanceRole")
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution Role that instances launched by this Compute Environment will use.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "instanceRole"))

    @builtins.property
    @jsii.member(jsii_name="kubernetesNamespace")
    def kubernetes_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) The namespace of the Cluster.

        Cannot be 'default', start with 'kube-', or be longer than 64 characters.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kubernetesNamespace"))

    @builtins.property
    @jsii.member(jsii_name="launchTemplate")
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances.

        *Note*: if ``securityGroups`` is specified on both your
        launch template and this Compute Environment, **the
        ``securityGroup``s on the Compute Environment override the
        ones on the launch template.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate], jsii.get(self, "launchTemplate"))

    @builtins.property
    @jsii.member(jsii_name="minvCpus")
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minvCpus"))

    @builtins.property
    @jsii.member(jsii_name="placementGroup")
    def placement_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup]:
        '''(experimental) The EC2 placement group to associate with your compute resources.

        If you intend to submit multi-node parallel jobs to this Compute Environment,
        you should consider creating a cluster placement group and associate it with your compute resources.
        This keeps your multi-node parallel job on a logical grouping of instances
        within a single Availability Zone with high network flow potential.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup], jsii.get(self, "placementGroup"))

    @builtins.property
    @jsii.member(jsii_name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "replaceComputeEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "serviceRole"))

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "spot"))

    @builtins.property
    @jsii.member(jsii_name="spotBidPercentage")
    def spot_bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

        For example, if your maximum percentage is 20%, the Spot price must be
        less than 20% of the current On-Demand price for that Instance.
        You always pay the lowest market price and never more than your maximum percentage.
        For most use cases, Batch recommends leaving this field empty.

        Implies ``spot == true`` if set

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "spotBidPercentage"))

    @builtins.property
    @jsii.member(jsii_name="terminateOnUpdate")
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "terminateOnUpdate"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeout")
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "updateTimeout"))

    @builtins.property
    @jsii.member(jsii_name="updateToLatestImageVersion")
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "updateToLatestImageVersion"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.ManagedEc2EksComputeEnvironmentProps",
    jsii_struct_bases=[ManagedComputeEnvironmentProps],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "enabled": "enabled",
        "service_role": "serviceRole",
        "vpc": "vpc",
        "maxv_cpus": "maxvCpus",
        "replace_compute_environment": "replaceComputeEnvironment",
        "security_groups": "securityGroups",
        "spot": "spot",
        "terminate_on_update": "terminateOnUpdate",
        "update_timeout": "updateTimeout",
        "update_to_latest_image_version": "updateToLatestImageVersion",
        "vpc_subnets": "vpcSubnets",
        "eks_cluster": "eksCluster",
        "kubernetes_namespace": "kubernetesNamespace",
        "allocation_strategy": "allocationStrategy",
        "images": "images",
        "instance_classes": "instanceClasses",
        "instance_role": "instanceRole",
        "instance_types": "instanceTypes",
        "launch_template": "launchTemplate",
        "minv_cpus": "minvCpus",
        "placement_group": "placementGroup",
        "spot_bid_percentage": "spotBidPercentage",
        "use_optimal_instance_classes": "useOptimalInstanceClasses",
    },
)
class ManagedEc2EksComputeEnvironmentProps(ManagedComputeEnvironmentProps):
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        eks_cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
        kubernetes_namespace: builtins.str,
        allocation_strategy: typing.Optional[AllocationStrategy] = None,
        images: typing.Optional[typing.Sequence[typing.Union[EksMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
        instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
        instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
        launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
        minv_cpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
        spot_bid_percentage: typing.Optional[jsii.Number] = None,
        use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Props for a ManagedEc2EksComputeEnvironment.

        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created
        :param eks_cluster: (experimental) The cluster that backs this Compute Environment. Required for Compute Environments running Kubernetes jobs. Please ensure that you have followed the steps at https://docs.aws.amazon.com/batch/latest/userguide/getting-started-eks.html before attempting to deploy a ``ManagedEc2EksComputeEnvironment`` that uses this cluster. If you do not follow the steps in the link, the deployment fail with a message that the compute environment did not stabilize.
        :param kubernetes_namespace: (experimental) The namespace of the Cluster.
        :param allocation_strategy: (experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated. Default: - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances, ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.
        :param images: (experimental) Configure which AMIs this Compute Environment can launch. Default: If ``imageKubernetesVersion`` is specified, - EKS_AL2 for non-GPU instances, EKS_AL2_NVIDIA for GPU instances, Otherwise, - ECS_AL2 for non-GPU instances, ECS_AL2_NVIDIA for GPU instances,
        :param instance_classes: (experimental) The instance types that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Batch will automatically choose the instance size. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param instance_role: (experimental) The execution Role that instances launched by this Compute Environment will use. Default: - a role will be created
        :param instance_types: (experimental) The instance types that this Compute Environment can launch. Which one is chosen depends on the ``AllocationStrategy`` used. Default: - the instances Batch considers will be used (currently C4, M4, and R4)
        :param launch_template: (experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances. *Note*: if ``securityGroups`` is specified on both your launch template and this Compute Environment, **the ``securityGroup``s on the Compute Environment override the ones on the launch template.** Default: - no launch template
        :param minv_cpus: (experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED. Default: 0
        :param placement_group: (experimental) The EC2 placement group to associate with your compute resources. If you intend to submit multi-node parallel jobs to this Compute Environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. Default: - no placement group
        :param spot_bid_percentage: (experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Instance. You always pay the lowest market price and never more than your maximum percentage. For most use cases, Batch recommends leaving this field empty. Implies ``spot == true`` if set Default: - 100%
        :param use_optimal_instance_classes: (experimental) Whether or not to use batch's optimal instance type. The optimal instance type is equivalent to adding the C4, M4, and R4 instance classes. You can specify other instance classes (of the same architecture) in addition to the optimal instance classes. Default: true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_ec2 as ec2
            from aws_cdk import aws_eks as eks
            from aws_cdk import aws_iam as iam
            
            # cluster: eks.Cluster
            # instance_type: ec2.InstanceType
            # launch_template: ec2.LaunchTemplate
            # machine_image: ec2.IMachineImage
            # placement_group: ec2.PlacementGroup
            # role: iam.Role
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # vpc: ec2.Vpc
            
            managed_ec2_eks_compute_environment_props = batch_alpha.ManagedEc2EksComputeEnvironmentProps(
                eks_cluster=cluster,
                kubernetes_namespace="kubernetesNamespace",
                vpc=vpc,
            
                # the properties below are optional
                allocation_strategy=batch_alpha.AllocationStrategy.BEST_FIT,
                compute_environment_name="computeEnvironmentName",
                enabled=False,
                images=[batch_alpha.EksMachineImage(
                    image=machine_image,
                    image_type=batch_alpha.EksMachineImageType.EKS_AL2
                )],
                instance_classes=[ec2.InstanceClass.STANDARD3],
                instance_role=role,
                instance_types=[instance_type],
                launch_template=launch_template,
                maxv_cpus=123,
                minv_cpus=123,
                placement_group=placement_group,
                replace_compute_environment=False,
                security_groups=[security_group],
                service_role=role,
                spot=False,
                spot_bid_percentage=123,
                terminate_on_update=False,
                update_timeout=cdk.Duration.minutes(30),
                update_to_latest_image_version=False,
                use_optimal_instance_classes=False,
                vpc_subnets=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e42d86a173146d27c5c384f1a29007831c1dca632c1e2c34c274f79f70392e)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
            check_type(argname="argument replace_compute_environment", value=replace_compute_environment, expected_type=type_hints["replace_compute_environment"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument terminate_on_update", value=terminate_on_update, expected_type=type_hints["terminate_on_update"])
            check_type(argname="argument update_timeout", value=update_timeout, expected_type=type_hints["update_timeout"])
            check_type(argname="argument update_to_latest_image_version", value=update_to_latest_image_version, expected_type=type_hints["update_to_latest_image_version"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument eks_cluster", value=eks_cluster, expected_type=type_hints["eks_cluster"])
            check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
            check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            check_type(argname="argument images", value=images, expected_type=type_hints["images"])
            check_type(argname="argument instance_classes", value=instance_classes, expected_type=type_hints["instance_classes"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument minv_cpus", value=minv_cpus, expected_type=type_hints["minv_cpus"])
            check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
            check_type(argname="argument spot_bid_percentage", value=spot_bid_percentage, expected_type=type_hints["spot_bid_percentage"])
            check_type(argname="argument use_optimal_instance_classes", value=use_optimal_instance_classes, expected_type=type_hints["use_optimal_instance_classes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
            "eks_cluster": eks_cluster,
            "kubernetes_namespace": kubernetes_namespace,
        }
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_role is not None:
            self._values["service_role"] = service_role
        if maxv_cpus is not None:
            self._values["maxv_cpus"] = maxv_cpus
        if replace_compute_environment is not None:
            self._values["replace_compute_environment"] = replace_compute_environment
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if terminate_on_update is not None:
            self._values["terminate_on_update"] = terminate_on_update
        if update_timeout is not None:
            self._values["update_timeout"] = update_timeout
        if update_to_latest_image_version is not None:
            self._values["update_to_latest_image_version"] = update_to_latest_image_version
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocation_strategy is not None:
            self._values["allocation_strategy"] = allocation_strategy
        if images is not None:
            self._values["images"] = images
        if instance_classes is not None:
            self._values["instance_classes"] = instance_classes
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if minv_cpus is not None:
            self._values["minv_cpus"] = minv_cpus
        if placement_group is not None:
            self._values["placement_group"] = placement_group
        if spot_bid_percentage is not None:
            self._values["spot_bid_percentage"] = spot_bid_percentage
        if use_optimal_instance_classes is not None:
            self._values["use_optimal_instance_classes"] = use_optimal_instance_classes

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ComputeEnvironment.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC in which this Compute Environment will launch Instances.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :default: 256

        :stability: experimental
        '''
        result = self._values.get("maxv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
        :stability: experimental
        '''
        result = self._values.get("replace_compute_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :default: new security groups will be created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("terminate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :default: 30 minutes

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("update_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_to_latest_image_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The VPC Subnets this Compute Environment will launch instances in.

        :default: new subnets will be created

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def eks_cluster(self) -> _aws_cdk_aws_eks_ceddda9d.ICluster:
        '''(experimental) The cluster that backs this Compute Environment. Required for Compute Environments running Kubernetes jobs.

        Please ensure that you have followed the steps at

        https://docs.aws.amazon.com/batch/latest/userguide/getting-started-eks.html

        before attempting to deploy a ``ManagedEc2EksComputeEnvironment`` that uses this cluster.
        If you do not follow the steps in the link, the deployment fail with a message that the
        compute environment did not stabilize.

        :stability: experimental
        '''
        result = self._values.get("eks_cluster")
        assert result is not None, "Required property 'eks_cluster' is missing"
        return typing.cast(_aws_cdk_aws_eks_ceddda9d.ICluster, result)

    @builtins.property
    def kubernetes_namespace(self) -> builtins.str:
        '''(experimental) The namespace of the Cluster.

        :stability: experimental
        '''
        result = self._values.get("kubernetes_namespace")
        assert result is not None, "Required property 'kubernetes_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use if not enough instances of the best fitting instance type can be allocated.

        :default:

        - ``BEST_FIT_PROGRESSIVE`` if not using Spot instances,
        ``SPOT_CAPACITY_OPTIMIZED`` if using Spot instances.

        :stability: experimental
        '''
        result = self._values.get("allocation_strategy")
        return typing.cast(typing.Optional[AllocationStrategy], result)

    @builtins.property
    def images(self) -> typing.Optional[typing.List[EksMachineImage]]:
        '''(experimental) Configure which AMIs this Compute Environment can launch.

        :default:

        If ``imageKubernetesVersion`` is specified,

        - EKS_AL2 for non-GPU instances, EKS_AL2_NVIDIA for GPU instances,
        Otherwise,
        - ECS_AL2 for non-GPU instances, ECS_AL2_NVIDIA for GPU instances,

        :stability: experimental
        '''
        result = self._values.get("images")
        return typing.cast(typing.Optional[typing.List[EksMachineImage]], result)

    @builtins.property
    def instance_classes(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.
        Batch will automatically choose the instance size.

        :default: - the instances Batch considers will be used (currently C4, M4, and R4)

        :stability: experimental
        '''
        result = self._values.get("instance_classes")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The execution Role that instances launched by this Compute Environment will use.

        :default: - a role will be created

        :stability: experimental
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]]:
        '''(experimental) The instance types that this Compute Environment can launch.

        Which one is chosen depends on the ``AllocationStrategy`` used.

        :default: - the instances Batch considers will be used (currently C4, M4, and R4)

        :stability: experimental
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.InstanceType]], result)

    @builtins.property
    def launch_template(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate]:
        '''(experimental) The Launch Template that this Compute Environment will use to provision EC2 Instances.

        *Note*: if ``securityGroups`` is specified on both your
        launch template and this Compute Environment, **the
        ``securityGroup``s on the Compute Environment override the
        ones on the launch template.**

        :default: - no launch template

        :stability: experimental
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate], result)

    @builtins.property
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum vCPUs that an environment should maintain, even if the compute environment is DISABLED.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("minv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_group(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup]:
        '''(experimental) The EC2 placement group to associate with your compute resources.

        If you intend to submit multi-node parallel jobs to this Compute Environment,
        you should consider creating a cluster placement group and associate it with your compute resources.
        This keeps your multi-node parallel job on a logical grouping of instances
        within a single Availability Zone with high network flow potential.

        :default: - no placement group

        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html
        :stability: experimental
        '''
        result = self._values.get("placement_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup], result)

    @builtins.property
    def spot_bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

        For example, if your maximum percentage is 20%, the Spot price must be
        less than 20% of the current On-Demand price for that Instance.
        You always pay the lowest market price and never more than your maximum percentage.
        For most use cases, Batch recommends leaving this field empty.

        Implies ``spot == true`` if set

        :default: - 100%

        :stability: experimental
        '''
        result = self._values.get("spot_bid_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_optimal_instance_classes(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use batch's optimal instance type.

        The optimal instance type is equivalent to adding the
        C4, M4, and R4 instance classes. You can specify other instance classes
        (of the same architecture) in addition to the optimal instance classes.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("use_optimal_instance_classes")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedEc2EksComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.MultiNodeContainer",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "end_node": "endNode",
        "start_node": "startNode",
    },
)
class MultiNodeContainer:
    def __init__(
        self,
        *,
        container: IEcsContainerDefinition,
        end_node: jsii.Number,
        start_node: jsii.Number,
    ) -> None:
        '''(experimental) Runs the container on nodes [startNode, endNode].

        :param container: (experimental) The container that this node range will run.
        :param end_node: (experimental) The index of the last node to run this container. The container is run on all nodes in the range [startNode, endNode] (inclusive)
        :param start_node: (experimental) The index of the first node to run this container. The container is run on all nodes in the range [startNode, endNode] (inclusive)

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            multi_node_job = batch.MultiNodeJobDefinition(self, "JobDefinition",
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.R4, ec2.InstanceSize.LARGE),
                containers=[batch.MultiNodeContainer(
                    container=batch.EcsEc2ContainerDefinition(self, "mainMPIContainer",
                        image=ecs.ContainerImage.from_registry("yourregsitry.com/yourMPIImage:latest"),
                        cpu=256,
                        memory=cdk.Size.mebibytes(2048)
                    ),
                    start_node=0,
                    end_node=5
                )]
            )
            # convenience method
            multi_node_job.add_container(
                start_node=6,
                end_node=10,
                container=batch.EcsEc2ContainerDefinition(self, "multiContainer",
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    cpu=256,
                    memory=cdk.Size.mebibytes(2048)
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c91062f1c8fc62f406ccbd11a0ac92eabc52ba7ff035a069bf920e09a854535d)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument end_node", value=end_node, expected_type=type_hints["end_node"])
            check_type(argname="argument start_node", value=start_node, expected_type=type_hints["start_node"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
            "end_node": end_node,
            "start_node": start_node,
        }

    @builtins.property
    def container(self) -> IEcsContainerDefinition:
        '''(experimental) The container that this node range will run.

        :stability: experimental
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(IEcsContainerDefinition, result)

    @builtins.property
    def end_node(self) -> jsii.Number:
        '''(experimental) The index of the last node to run this container.

        The container is run on all nodes in the range [startNode, endNode] (inclusive)

        :stability: experimental
        '''
        result = self._values.get("end_node")
        assert result is not None, "Required property 'end_node' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def start_node(self) -> jsii.Number:
        '''(experimental) The index of the first node to run this container.

        The container is run on all nodes in the range [startNode, endNode] (inclusive)

        :stability: experimental
        '''
        result = self._values.get("start_node")
        assert result is not None, "Required property 'start_node' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultiNodeContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IJobDefinition)
class MultiNodeJobDefinition(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.MultiNodeJobDefinition",
):
    '''(experimental) A JobDefinition that uses Ecs orchestration to run multiple containers.

    :stability: experimental
    :resource: AWS::Batch::JobDefinition
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        multi_node_job = batch.MultiNodeJobDefinition(self, "JobDefinition",
            instance_type=ec2.InstanceType.of(ec2.InstanceClass.R4, ec2.InstanceSize.LARGE),
            containers=[batch.MultiNodeContainer(
                container=batch.EcsEc2ContainerDefinition(self, "mainMPIContainer",
                    image=ecs.ContainerImage.from_registry("yourregsitry.com/yourMPIImage:latest"),
                    cpu=256,
                    memory=cdk.Size.mebibytes(2048)
                ),
                start_node=0,
                end_node=5
            )]
        )
        # convenience method
        multi_node_job.add_container(
            start_node=6,
            end_node=10,
            container=batch.EcsEc2ContainerDefinition(self, "multiContainer",
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                cpu=256,
                memory=cdk.Size.mebibytes(2048)
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        containers: typing.Optional[typing.Sequence[typing.Union[MultiNodeContainer, typing.Dict[builtins.str, typing.Any]]]] = None,
        main_node: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence["RetryStrategy"]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instance_type: (experimental) The instance type that this job definition will run.
        :param containers: (experimental) The containers that this multinode job will run. Default: none
        :param main_node: (experimental) The index of the main node in this job. The main node is responsible for orchestration. Default: 0
        :param propagate_tags: (experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns. Default: false
        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__139b4216a5dd7f555b1ab73bb5cea84db509a956ce81cf54bffc204e58736e03)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = MultiNodeJobDefinitionProps(
            instance_type=instance_type,
            containers=containers,
            main_node=main_node,
            propagate_tags=propagate_tags,
            job_definition_name=job_definition_name,
            parameters=parameters,
            retry_attempts=retry_attempts,
            retry_strategies=retry_strategies,
            scheduling_priority=scheduling_priority,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobDefinitionArn")
    @builtins.classmethod
    def from_job_definition_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        job_definition_arn: builtins.str,
    ) -> IJobDefinition:
        '''(experimental) refer to an existing JobDefinition by its arn.

        :param scope: -
        :param id: -
        :param job_definition_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17613a34df9a93ba88b486af78c4e07c2c4fe2f08a80569f2e45e0d4b5856d38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_definition_arn", value=job_definition_arn, expected_type=type_hints["job_definition_arn"])
        return typing.cast(IJobDefinition, jsii.sinvoke(cls, "fromJobDefinitionArn", [scope, id, job_definition_arn]))

    @jsii.member(jsii_name="addContainer")
    def add_container(
        self,
        *,
        container: IEcsContainerDefinition,
        end_node: jsii.Number,
        start_node: jsii.Number,
    ) -> None:
        '''(experimental) Add a container to this multinode job.

        :param container: (experimental) The container that this node range will run.
        :param end_node: (experimental) The index of the last node to run this container. The container is run on all nodes in the range [startNode, endNode] (inclusive)
        :param start_node: (experimental) The index of the first node to run this container. The container is run on all nodes in the range [startNode, endNode] (inclusive)

        :stability: experimental
        '''
        container_ = MultiNodeContainer(
            container=container, end_node=end_node, start_node=start_node
        )

        return typing.cast(None, jsii.invoke(self, "addContainer", [container_]))

    @jsii.member(jsii_name="addRetryStrategy")
    def add_retry_strategy(self, strategy: "RetryStrategy") -> None:
        '''(experimental) Add a RetryStrategy to this JobDefinition.

        :param strategy: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05fba5f22c63c67900e0f92f211bd72c8dab50e7dd1665f4c69ca32da27ad93a)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        return typing.cast(None, jsii.invoke(self, "addRetryStrategy", [strategy]))

    @builtins.property
    @jsii.member(jsii_name="containers")
    def containers(self) -> typing.List[MultiNodeContainer]:
        '''(experimental) The containers that this multinode job will run.

        :stability: experimental
        '''
        return typing.cast(typing.List[MultiNodeContainer], jsii.get(self, "containers"))

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''(experimental) The instance type that this job definition will run.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, jsii.get(self, "instanceType"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionArn"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of this job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionName"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategies")
    def retry_strategies(self) -> typing.List["RetryStrategy"]:
        '''(experimental) Defines the retry behavior for this job.

        :stability: experimental
        '''
        return typing.cast(typing.List["RetryStrategy"], jsii.get(self, "retryStrategies"))

    @builtins.property
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The index of the main node in this job.

        The main node is responsible for orchestration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mainNode"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "propagateTags"))

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPriority")
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulingPriority"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.MultiNodeJobDefinitionProps",
    jsii_struct_bases=[JobDefinitionProps],
    name_mapping={
        "job_definition_name": "jobDefinitionName",
        "parameters": "parameters",
        "retry_attempts": "retryAttempts",
        "retry_strategies": "retryStrategies",
        "scheduling_priority": "schedulingPriority",
        "timeout": "timeout",
        "instance_type": "instanceType",
        "containers": "containers",
        "main_node": "mainNode",
        "propagate_tags": "propagateTags",
    },
)
class MultiNodeJobDefinitionProps(JobDefinitionProps):
    def __init__(
        self,
        *,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence["RetryStrategy"]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
        containers: typing.Optional[typing.Sequence[typing.Union[MultiNodeContainer, typing.Dict[builtins.str, typing.Any]]]] = None,
        main_node: typing.Optional[jsii.Number] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Props to configure a MultiNodeJobDefinition.

        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout
        :param instance_type: (experimental) The instance type that this job definition will run.
        :param containers: (experimental) The containers that this multinode job will run. Default: none
        :param main_node: (experimental) The index of the main node in this job. The main node is responsible for orchestration. Default: 0
        :param propagate_tags: (experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            multi_node_job = batch.MultiNodeJobDefinition(self, "JobDefinition",
                instance_type=ec2.InstanceType.of(ec2.InstanceClass.R4, ec2.InstanceSize.LARGE),
                containers=[batch.MultiNodeContainer(
                    container=batch.EcsEc2ContainerDefinition(self, "mainMPIContainer",
                        image=ecs.ContainerImage.from_registry("yourregsitry.com/yourMPIImage:latest"),
                        cpu=256,
                        memory=cdk.Size.mebibytes(2048)
                    ),
                    start_node=0,
                    end_node=5
                )]
            )
            # convenience method
            multi_node_job.add_container(
                start_node=6,
                end_node=10,
                container=batch.EcsEc2ContainerDefinition(self, "multiContainer",
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    cpu=256,
                    memory=cdk.Size.mebibytes(2048)
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a47285cdbc48884b55ec85b3762923ac73e4c2727c95d4878276c2f187f22ec)
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_strategies", value=retry_strategies, expected_type=type_hints["retry_strategies"])
            check_type(argname="argument scheduling_priority", value=scheduling_priority, expected_type=type_hints["scheduling_priority"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
            check_type(argname="argument main_node", value=main_node, expected_type=type_hints["main_node"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_type": instance_type,
        }
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_strategies is not None:
            self._values["retry_strategies"] = retry_strategies
        if scheduling_priority is not None:
            self._values["scheduling_priority"] = scheduling_priority
        if timeout is not None:
            self._values["timeout"] = timeout
        if containers is not None:
            self._values["containers"] = containers
        if main_node is not None:
            self._values["main_node"] = main_node
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this job definition.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :default: none

        :see: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html#parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_strategies(self) -> typing.Optional[typing.List["RetryStrategy"]]:
        '''(experimental) Defines the retry behavior for this job.

        :default: - no ``RetryStrategy``

        :stability: experimental
        '''
        result = self._values.get("retry_strategies")
        return typing.cast(typing.Optional[typing.List["RetryStrategy"]], result)

    @builtins.property
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("scheduling_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :default: - no timeout

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def instance_type(self) -> _aws_cdk_aws_ec2_ceddda9d.InstanceType:
        '''(experimental) The instance type that this job definition will run.

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.InstanceType, result)

    @builtins.property
    def containers(self) -> typing.Optional[typing.List[MultiNodeContainer]]:
        '''(experimental) The containers that this multinode job will run.

        :default: none

        :see: https://aws.amazon.com/blogs/compute/building-a-tightly-coupled-molecular-dynamics-workflow-with-multi-node-parallel-jobs-in-aws-batch/
        :stability: experimental
        '''
        result = self._values.get("containers")
        return typing.cast(typing.Optional[typing.List[MultiNodeContainer]], result)

    @builtins.property
    def main_node(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The index of the main node in this job.

        The main node is responsible for orchestration.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("main_node")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MultiNodeJobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.OrderedComputeEnvironment",
    jsii_struct_bases=[],
    name_mapping={"compute_environment": "computeEnvironment", "order": "order"},
)
class OrderedComputeEnvironment:
    def __init__(
        self,
        *,
        compute_environment: IComputeEnvironment,
        order: jsii.Number,
    ) -> None:
        '''(experimental) Assigns an order to a ComputeEnvironment.

        The JobQueue will prioritize the lowest-order ComputeEnvironment.

        :param compute_environment: (experimental) The ComputeEnvironment to link to this JobQueue.
        :param order: (experimental) The order associated with ``computeEnvironment``.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            # compute_environment: batch_alpha.IComputeEnvironment
            
            ordered_compute_environment = batch_alpha.OrderedComputeEnvironment(
                compute_environment=compute_environment,
                order=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e89685caa52c73ced10db3d7e3342c85bc760d13702b6c1b1b6518bb92cb6da)
            check_type(argname="argument compute_environment", value=compute_environment, expected_type=type_hints["compute_environment"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_environment": compute_environment,
            "order": order,
        }

    @builtins.property
    def compute_environment(self) -> IComputeEnvironment:
        '''(experimental) The ComputeEnvironment to link to this JobQueue.

        :stability: experimental
        '''
        result = self._values.get("compute_environment")
        assert result is not None, "Required property 'compute_environment' is missing"
        return typing.cast(IComputeEnvironment, result)

    @builtins.property
    def order(self) -> jsii.Number:
        '''(experimental) The order associated with ``computeEnvironment``.

        :stability: experimental
        '''
        result = self._values.get("order")
        assert result is not None, "Required property 'order' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OrderedComputeEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Reason(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-batch-alpha.Reason"):
    '''(experimental) Common job exit reasons.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        
        job_defn = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256
            ),
            retry_attempts=5,
            retry_strategies=[
                batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER)
            ]
        )
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.SPOT_INSTANCE_RECLAIMED))
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER))
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.custom(
                on_exit_code="40*",
                on_reason="some reason"
            )))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *,
        on_exit_code: typing.Optional[builtins.str] = None,
        on_reason: typing.Optional[builtins.str] = None,
        on_status_reason: typing.Optional[builtins.str] = None,
    ) -> "Reason":
        '''(experimental) A custom Reason that can match on multiple conditions.

        Note that all specified conditions must be met for this reason to match.

        :param on_exit_code: (experimental) A glob string that will match on the job exit code. For example, ``'40*'`` will match 400, 404, 40123456789012 Default: - will not match on the exit code
        :param on_reason: (experimental) A glob string that will match on the reason returned by the exiting job For example, ``'CannotPullContainerError*'`` indicates that container needed to start the job could not be pulled. Default: - will not match on the reason
        :param on_status_reason: (experimental) A glob string that will match on the statusReason returned by the exiting job. For example, ``'Host EC2*'`` indicates that the spot instance has been reclaimed. Default: - will not match on the status reason

        :stability: experimental
        '''
        custom_reason_props = CustomReason(
            on_exit_code=on_exit_code,
            on_reason=on_reason,
            on_status_reason=on_status_reason,
        )

        return typing.cast("Reason", jsii.sinvoke(cls, "custom", [custom_reason_props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CANNOT_PULL_CONTAINER")
    def CANNOT_PULL_CONTAINER(cls) -> "Reason":
        '''(experimental) Will only match if the Docker container could not be pulled.

        :stability: experimental
        '''
        return typing.cast("Reason", jsii.sget(cls, "CANNOT_PULL_CONTAINER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NON_ZERO_EXIT_CODE")
    def NON_ZERO_EXIT_CODE(cls) -> "Reason":
        '''(experimental) Will match any non-zero exit code.

        :stability: experimental
        '''
        return typing.cast("Reason", jsii.sget(cls, "NON_ZERO_EXIT_CODE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SPOT_INSTANCE_RECLAIMED")
    def SPOT_INSTANCE_RECLAIMED(cls) -> "Reason":
        '''(experimental) Will only match if the Spot instance executing the job was reclaimed.

        :stability: experimental
        '''
        return typing.cast("Reason", jsii.sget(cls, "SPOT_INSTANCE_RECLAIMED"))


class RetryStrategy(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.RetryStrategy",
):
    '''(experimental) Define how Jobs using this JobDefinition respond to different exit conditions.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        
        job_defn = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256
            ),
            retry_attempts=5,
            retry_strategies=[
                batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER)
            ]
        )
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.SPOT_INSTANCE_RECLAIMED))
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.CANNOT_PULL_CONTAINER))
        job_defn.add_retry_strategy(
            batch.RetryStrategy.of(batch.Action.EXIT, batch.Reason.custom(
                on_exit_code="40*",
                on_reason="some reason"
            )))
    '''

    def __init__(self, action: Action, on: Reason) -> None:
        '''
        :param action: -
        :param on: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93a3cf6384cd52d885e05decbc453270afadf73350fe3fbabfe999eb000ac3af)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
        jsii.create(self.__class__, self, [action, on])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, action: Action, on: Reason) -> "RetryStrategy":
        '''(experimental) Create a new RetryStrategy.

        :param action: -
        :param on: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbd2a86a39e9602a1980340842fa5279880b52eb427c00e2482eca862804d6e1)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument on", value=on, expected_type=type_hints["on"])
        return typing.cast("RetryStrategy", jsii.sinvoke(cls, "of", [action, on]))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> Action:
        '''(experimental) The action to take when the job exits with the Reason specified.

        :stability: experimental
        '''
        return typing.cast(Action, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="on")
    def on(self) -> Reason:
        '''(experimental) If the job exits with this Reason it will trigger the specified Action.

        :stability: experimental
        '''
        return typing.cast(Reason, jsii.get(self, "on"))


class Secret(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-batch-alpha.Secret",
):
    '''(experimental) A secret environment variable.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        # my_secret: secretsmanager.ISecret
        
        
        job_defn = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256,
                secrets={
                    "MY_SECRET_ENV_VAR": batch.Secret.from_secrets_manager(my_secret)
                }
            )
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromSecretsManager")
    @builtins.classmethod
    def from_secrets_manager(
        cls,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        field: typing.Optional[builtins.str] = None,
    ) -> "Secret":
        '''(experimental) Creates a environment variable value from a secret stored in AWS Secrets Manager.

        :param secret: the secret stored in AWS Secrets Manager.
        :param field: the name of the field with the value that you want to set as the environment variable value. Only values in JSON format are supported. If you do not specify a JSON field, then the full content of the secret is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417b5bb542000b74f11d2e41b2540a20c4c11f654f8fc91dee7ffaddf9d6d998)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("Secret", jsii.sinvoke(cls, "fromSecretsManager", [secret, field]))

    @jsii.member(jsii_name="fromSecretsManagerVersion")
    @builtins.classmethod
    def from_secrets_manager_version(
        cls,
        secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        version_info: typing.Union["SecretVersionInfo", typing.Dict[builtins.str, typing.Any]],
        field: typing.Optional[builtins.str] = None,
    ) -> "Secret":
        '''(experimental) Creates a environment variable value from a secret stored in AWS Secrets Manager.

        :param secret: the secret stored in AWS Secrets Manager.
        :param version_info: the version information to reference the secret.
        :param field: the name of the field with the value that you want to set as the environment variable value. Only values in JSON format are supported. If you do not specify a JSON field, then the full content of the secret is used.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154b84f590a02078c55967f577cea92eab82265b65e02a4a494b9f1640c2c0cd)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            check_type(argname="argument version_info", value=version_info, expected_type=type_hints["version_info"])
            check_type(argname="argument field", value=field, expected_type=type_hints["field"])
        return typing.cast("Secret", jsii.sinvoke(cls, "fromSecretsManagerVersion", [secret, version_info, field]))

    @jsii.member(jsii_name="fromSsmParameter")
    @builtins.classmethod
    def from_ssm_parameter(
        cls,
        parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
    ) -> "Secret":
        '''(experimental) Creates an environment variable value from a parameter stored in AWS Systems Manager Parameter Store.

        :param parameter: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148d662618bb349676015375138c4ecfa0be439a0b516966013300b96f13b203)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("Secret", jsii.sinvoke(cls, "fromSsmParameter", [parameter]))

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants reading the secret to a principal.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="arn")
    @abc.abstractmethod
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="hasField")
    @abc.abstractmethod
    def has_field(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this secret uses a specific JSON field.

        :stability: experimental
        '''
        ...


class _SecretProxy(Secret):
    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(experimental) Grants reading the secret to a principal.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1dccacde9286de58cba92280e0cdf531ae9d73f821080448b72c71ef3e76e4b)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the secret.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="hasField")
    def has_field(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this secret uses a specific JSON field.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "hasField"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Secret).__jsii_proxy_class__ = lambda : _SecretProxy


class SecretPathVolume(
    EksVolume,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.SecretPathVolume",
):
    '''(experimental) Specifies the configuration of a Kubernetes secret volume.

    :see: https://kubernetes.io/docs/concepts/storage/volumes/#secret
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        
        secret_path_volume = batch_alpha.SecretPathVolume(
            name="name",
            secret_name="secretName",
        
            # the properties below are optional
            mount_path="mountPath",
            optional=False,
            readonly=False
        )
    '''

    def __init__(
        self,
        *,
        secret_name: builtins.str,
        optional: typing.Optional[builtins.bool] = None,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param secret_name: (experimental) The name of the secret. Must be a valid DNS subdomain name.
        :param optional: (experimental) Specifies whether the secret or the secret's keys must be defined. Default: true
        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false

        :stability: experimental
        '''
        options = SecretPathVolumeOptions(
            secret_name=secret_name,
            optional=optional,
            name=name,
            mount_path=mount_path,
            readonly=readonly,
        )

        jsii.create(self.__class__, self, [options])

    @jsii.member(jsii_name="isSecretPathVolume")
    @builtins.classmethod
    def is_secret_path_volume(cls, x: typing.Any) -> builtins.bool:
        '''(experimental) returns ``true`` if ``x`` is a ``SecretPathVolume`` and ``false`` otherwise.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3a03ecb4d2c7970b919f329ea0a70b0d6d566612846e7310ce39a70b2d28cc8)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isSecretPathVolume", [x]))

    @builtins.property
    @jsii.member(jsii_name="secretName")
    def secret_name(self) -> builtins.str:
        '''(experimental) The name of the secret.

        Must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretName"))

    @builtins.property
    @jsii.member(jsii_name="optional")
    def optional(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the secret or the secret's keys must be defined.

        :default: true

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "optional"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.SecretPathVolumeOptions",
    jsii_struct_bases=[EksVolumeOptions],
    name_mapping={
        "name": "name",
        "mount_path": "mountPath",
        "readonly": "readonly",
        "secret_name": "secretName",
        "optional": "optional",
    },
)
class SecretPathVolumeOptions(EksVolumeOptions):
    def __init__(
        self,
        *,
        name: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
        readonly: typing.Optional[builtins.bool] = None,
        secret_name: builtins.str,
        optional: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for a Kubernetes SecretPath Volume.

        :param name: (experimental) The name of this volume. The name must be a valid DNS subdomain name.
        :param mount_path: (experimental) The path on the container where the volume is mounted. Default: - the volume is not mounted
        :param readonly: (experimental) If specified, the container has readonly access to the volume. Otherwise, the container has read/write access. Default: false
        :param secret_name: (experimental) The name of the secret. Must be a valid DNS subdomain name.
        :param optional: (experimental) Specifies whether the secret or the secret's keys must be defined. Default: true

        :see: https://kubernetes.io/docs/concepts/storage/volumes/#secret
        :stability: experimental
        :exampleMetadata: infused

        Example::

            # job_defn: batch.EksJobDefinition
            
            job_defn.container.add_volume(batch.EksVolume.empty_dir(
                name="emptyDir",
                mount_path="/Volumes/emptyDir"
            ))
            job_defn.container.add_volume(batch.EksVolume.host_path(
                name="hostPath",
                host_path="/sys",
                mount_path="/Volumes/hostPath"
            ))
            job_defn.container.add_volume(batch.EksVolume.secret(
                name="secret",
                optional=True,
                mount_path="/Volumes/secret",
                secret_name="mySecret"
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6846c94bd19e040b25e2c723ce4e85c8433155366f549c39673137f848bbeabf)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
            check_type(argname="argument readonly", value=readonly, expected_type=type_hints["readonly"])
            check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
            check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "secret_name": secret_name,
        }
        if mount_path is not None:
            self._values["mount_path"] = mount_path
        if readonly is not None:
            self._values["readonly"] = readonly
        if optional is not None:
            self._values["optional"] = optional

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of this volume.

        The name must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path on the container where the volume is mounted.

        :default: - the volume is not mounted

        :stability: experimental
        '''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readonly(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container has readonly access to the volume.

        Otherwise, the container has read/write access.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("readonly")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def secret_name(self) -> builtins.str:
        '''(experimental) The name of the secret.

        Must be a valid DNS subdomain name.

        :see: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names
        :stability: experimental
        '''
        result = self._values.get("secret_name")
        assert result is not None, "Required property 'secret_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def optional(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the secret or the secret's keys must be defined.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("optional")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretPathVolumeOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.SecretVersionInfo",
    jsii_struct_bases=[],
    name_mapping={"version_id": "versionId", "version_stage": "versionStage"},
)
class SecretVersionInfo:
    def __init__(
        self,
        *,
        version_id: typing.Optional[builtins.str] = None,
        version_stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Specify the secret's version id or version stage.

        :param version_id: (experimental) version id of the secret. Default: - use default version id
        :param version_stage: (experimental) version stage of the secret. Default: - use default version stage

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            secret_version_info = batch_alpha.SecretVersionInfo(
                version_id="versionId",
                version_stage="versionStage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b741a8b4f55c3924a86f27640b2c2804411ad62a1fbd1989efe7d927f71f51e8)
            check_type(argname="argument version_id", value=version_id, expected_type=type_hints["version_id"])
            check_type(argname="argument version_stage", value=version_stage, expected_type=type_hints["version_stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if version_id is not None:
            self._values["version_id"] = version_id
        if version_stage is not None:
            self._values["version_stage"] = version_stage

    @builtins.property
    def version_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) version id of the secret.

        :default: - use default version id

        :stability: experimental
        '''
        result = self._values.get("version_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def version_stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) version stage of the secret.

        :default: - use default version stage

        :stability: experimental
        '''
        result = self._values.get("version_stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecretVersionInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.Share",
    jsii_struct_bases=[],
    name_mapping={
        "share_identifier": "shareIdentifier",
        "weight_factor": "weightFactor",
    },
)
class Share:
    def __init__(
        self,
        *,
        share_identifier: builtins.str,
        weight_factor: jsii.Number,
    ) -> None:
        '''(experimental) Represents a group of Job Definitions.

        All Job Definitions that
        declare a share identifier will be considered members of the Share
        defined by that share identifier.

        The Scheduler divides the maximum available vCPUs of the ComputeEnvironment
        among Jobs in the Queue based on their shareIdentifier and the weightFactor
        associated with that shareIdentifier.

        :param share_identifier: (experimental) The identifier of this Share. All jobs that specify this share identifier when submitted to the queue will be considered as part of this Share.
        :param weight_factor: (experimental) The weight factor given to this Share. The Scheduler decides which jobs to put in the Compute Environment such that the following ratio is equal for each job: ``sharevCpu / weightFactor``, where ``sharevCpu`` is the total amount of vCPU given to that particular share; that is, the sum of the vCPU of each job currently in the Compute Environment for that share. See the readme of this module for a detailed example that shows how these are used, how it relates to ``computeReservation``, and how ``shareDecay`` affects these calculations.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            fairshare_policy = batch.FairshareSchedulingPolicy(self, "myFairsharePolicy")
            
            fairshare_policy.add_share(
                share_identifier="A",
                weight_factor=1
            )
            fairshare_policy.add_share(
                share_identifier="B",
                weight_factor=1
            )
            batch.JobQueue(self, "JobQueue",
                scheduling_policy=fairshare_policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f49c5ab573b4bfa5d0896d9a64df348a858dcad66800c2ee4b18d7c9689127d)
            check_type(argname="argument share_identifier", value=share_identifier, expected_type=type_hints["share_identifier"])
            check_type(argname="argument weight_factor", value=weight_factor, expected_type=type_hints["weight_factor"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "share_identifier": share_identifier,
            "weight_factor": weight_factor,
        }

    @builtins.property
    def share_identifier(self) -> builtins.str:
        '''(experimental) The identifier of this Share.

        All jobs that specify this share identifier
        when submitted to the queue will be considered as part of this Share.

        :stability: experimental
        '''
        result = self._values.get("share_identifier")
        assert result is not None, "Required property 'share_identifier' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def weight_factor(self) -> jsii.Number:
        '''(experimental) The weight factor given to this Share.

        The Scheduler decides which jobs to put in the Compute Environment
        such that the following ratio is equal for each job:

        ``sharevCpu / weightFactor``,

        where ``sharevCpu`` is the total amount of vCPU given to that particular share; that is,
        the sum of the vCPU of each job currently in the Compute Environment for that share.

        See the readme of this module for a detailed example that shows how these are used,
        how it relates to ``computeReservation``, and how ``shareDecay`` affects these calculations.

        :stability: experimental
        '''
        result = self._values.get("weight_factor")
        assert result is not None, "Required property 'weight_factor' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Share(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.Tmpfs",
    jsii_struct_bases=[],
    name_mapping={
        "container_path": "containerPath",
        "size": "size",
        "mount_options": "mountOptions",
    },
)
class Tmpfs:
    def __init__(
        self,
        *,
        container_path: builtins.str,
        size: _aws_cdk_ceddda9d.Size,
        mount_options: typing.Optional[typing.Sequence["TmpfsMountOption"]] = None,
    ) -> None:
        '''(experimental) The details of a tmpfs mount for a container.

        :param container_path: (experimental) The absolute file path where the tmpfs volume is to be mounted.
        :param size: (experimental) The size (in MiB) of the tmpfs volume.
        :param mount_options: (experimental) The list of tmpfs volume mount options. For more information, see `TmpfsMountOptions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html>`_. Default: none

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            import aws_cdk as cdk
            
            # size: cdk.Size
            
            tmpfs = batch_alpha.Tmpfs(
                container_path="containerPath",
                size=size,
            
                # the properties below are optional
                mount_options=[batch_alpha.TmpfsMountOption.DEFAULTS]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae43135e0b7885bb5ad0c6b0f141663feb55023972c81196445d6320485e9b9e)
            check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
            check_type(argname="argument mount_options", value=mount_options, expected_type=type_hints["mount_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_path": container_path,
            "size": size,
        }
        if mount_options is not None:
            self._values["mount_options"] = mount_options

    @builtins.property
    def container_path(self) -> builtins.str:
        '''(experimental) The absolute file path where the tmpfs volume is to be mounted.

        :stability: experimental
        '''
        result = self._values.get("container_path")
        assert result is not None, "Required property 'container_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def size(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The size (in MiB) of the tmpfs volume.

        :stability: experimental
        '''
        result = self._values.get("size")
        assert result is not None, "Required property 'size' is missing"
        return typing.cast(_aws_cdk_ceddda9d.Size, result)

    @builtins.property
    def mount_options(self) -> typing.Optional[typing.List["TmpfsMountOption"]]:
        '''(experimental) The list of tmpfs volume mount options.

        For more information, see
        `TmpfsMountOptions <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_Tmpfs.html>`_.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("mount_options")
        return typing.cast(typing.Optional[typing.List["TmpfsMountOption"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tmpfs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.TmpfsMountOption")
class TmpfsMountOption(enum.Enum):
    '''(experimental) The supported options for a tmpfs mount for a container.

    :stability: experimental
    '''

    DEFAULTS = "DEFAULTS"
    '''
    :stability: experimental
    '''
    RO = "RO"
    '''
    :stability: experimental
    '''
    RW = "RW"
    '''
    :stability: experimental
    '''
    SUID = "SUID"
    '''
    :stability: experimental
    '''
    NOSUID = "NOSUID"
    '''
    :stability: experimental
    '''
    DEV = "DEV"
    '''
    :stability: experimental
    '''
    NODEV = "NODEV"
    '''
    :stability: experimental
    '''
    EXEC = "EXEC"
    '''
    :stability: experimental
    '''
    NOEXEC = "NOEXEC"
    '''
    :stability: experimental
    '''
    SYNC = "SYNC"
    '''
    :stability: experimental
    '''
    ASYNC = "ASYNC"
    '''
    :stability: experimental
    '''
    DIRSYNC = "DIRSYNC"
    '''
    :stability: experimental
    '''
    REMOUNT = "REMOUNT"
    '''
    :stability: experimental
    '''
    MAND = "MAND"
    '''
    :stability: experimental
    '''
    NOMAND = "NOMAND"
    '''
    :stability: experimental
    '''
    ATIME = "ATIME"
    '''
    :stability: experimental
    '''
    NOATIME = "NOATIME"
    '''
    :stability: experimental
    '''
    DIRATIME = "DIRATIME"
    '''
    :stability: experimental
    '''
    NODIRATIME = "NODIRATIME"
    '''
    :stability: experimental
    '''
    BIND = "BIND"
    '''
    :stability: experimental
    '''
    RBIND = "RBIND"
    '''
    :stability: experimental
    '''
    UNBINDABLE = "UNBINDABLE"
    '''
    :stability: experimental
    '''
    RUNBINDABLE = "RUNBINDABLE"
    '''
    :stability: experimental
    '''
    PRIVATE = "PRIVATE"
    '''
    :stability: experimental
    '''
    RPRIVATE = "RPRIVATE"
    '''
    :stability: experimental
    '''
    SHARED = "SHARED"
    '''
    :stability: experimental
    '''
    RSHARED = "RSHARED"
    '''
    :stability: experimental
    '''
    SLAVE = "SLAVE"
    '''
    :stability: experimental
    '''
    RSLAVE = "RSLAVE"
    '''
    :stability: experimental
    '''
    RELATIME = "RELATIME"
    '''
    :stability: experimental
    '''
    NORELATIME = "NORELATIME"
    '''
    :stability: experimental
    '''
    STRICTATIME = "STRICTATIME"
    '''
    :stability: experimental
    '''
    NOSTRICTATIME = "NOSTRICTATIME"
    '''
    :stability: experimental
    '''
    MODE = "MODE"
    '''
    :stability: experimental
    '''
    UID = "UID"
    '''
    :stability: experimental
    '''
    GID = "GID"
    '''
    :stability: experimental
    '''
    NR_INODES = "NR_INODES"
    '''
    :stability: experimental
    '''
    NR_BLOCKS = "NR_BLOCKS"
    '''
    :stability: experimental
    '''
    MPOL = "MPOL"
    '''
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.Ulimit",
    jsii_struct_bases=[],
    name_mapping={
        "hard_limit": "hardLimit",
        "name": "name",
        "soft_limit": "softLimit",
    },
)
class Ulimit:
    def __init__(
        self,
        *,
        hard_limit: jsii.Number,
        name: "UlimitName",
        soft_limit: jsii.Number,
    ) -> None:
        '''(experimental) Sets limits for a resource with ``ulimit`` on linux systems.

        Used by the Docker daemon.

        :param hard_limit: (experimental) The hard limit for this resource. The container will be terminated if it exceeds this limit.
        :param name: (experimental) The resource to limit.
        :param soft_limit: (experimental) The reservation for this resource. The container will not be terminated if it exceeds this limit.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            
            ulimit = batch_alpha.Ulimit(
                hard_limit=123,
                name=batch_alpha.UlimitName.CORE,
                soft_limit=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3a813e84c137117f83dbb8d34d6118680453895d16f2b159105d0d16200cf0)
            check_type(argname="argument hard_limit", value=hard_limit, expected_type=type_hints["hard_limit"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument soft_limit", value=soft_limit, expected_type=type_hints["soft_limit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "hard_limit": hard_limit,
            "name": name,
            "soft_limit": soft_limit,
        }

    @builtins.property
    def hard_limit(self) -> jsii.Number:
        '''(experimental) The hard limit for this resource.

        The container will
        be terminated if it exceeds this limit.

        :stability: experimental
        '''
        result = self._values.get("hard_limit")
        assert result is not None, "Required property 'hard_limit' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> "UlimitName":
        '''(experimental) The resource to limit.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast("UlimitName", result)

    @builtins.property
    def soft_limit(self) -> jsii.Number:
        '''(experimental) The reservation for this resource.

        The container will
        not be terminated if it exceeds this limit.

        :stability: experimental
        '''
        result = self._values.get("soft_limit")
        assert result is not None, "Required property 'soft_limit' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ulimit(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch-alpha.UlimitName")
class UlimitName(enum.Enum):
    '''(experimental) The resources to be limited.

    :stability: experimental
    '''

    CORE = "CORE"
    '''(experimental) max core dump file size.

    :stability: experimental
    '''
    CPU = "CPU"
    '''(experimental) max cpu time (seconds) for a process.

    :stability: experimental
    '''
    DATA = "DATA"
    '''(experimental) max data segment size.

    :stability: experimental
    '''
    FSIZE = "FSIZE"
    '''(experimental) max file size.

    :stability: experimental
    '''
    LOCKS = "LOCKS"
    '''(experimental) max number of file locks.

    :stability: experimental
    '''
    MEMLOCK = "MEMLOCK"
    '''(experimental) max locked memory.

    :stability: experimental
    '''
    MSGQUEUE = "MSGQUEUE"
    '''(experimental) max POSIX message queue size.

    :stability: experimental
    '''
    NICE = "NICE"
    '''(experimental) max nice value for any process this user is running.

    :stability: experimental
    '''
    NOFILE = "NOFILE"
    '''(experimental) maximum number of open file descriptors.

    :stability: experimental
    '''
    NPROC = "NPROC"
    '''(experimental) maximum number of processes.

    :stability: experimental
    '''
    RSS = "RSS"
    '''(experimental) size of the process' resident set (in pages).

    :stability: experimental
    '''
    RTPRIO = "RTPRIO"
    '''(experimental) max realtime priority.

    :stability: experimental
    '''
    RTTIME = "RTTIME"
    '''(experimental) timeout for realtime tasks.

    :stability: experimental
    '''
    SIGPENDING = "SIGPENDING"
    '''(experimental) max number of pending signals.

    :stability: experimental
    '''
    STACK = "STACK"
    '''(experimental) max stack size (in bytes).

    :stability: experimental
    '''


@jsii.implements(IUnmanagedComputeEnvironment, IComputeEnvironment)
class UnmanagedComputeEnvironment(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.UnmanagedComputeEnvironment",
):
    '''(experimental) Unmanaged ComputeEnvironments do not provision or manage EC2 instances on your behalf.

    :stability: experimental
    :resource: AWS::Batch::ComputeEnvironment
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        from aws_cdk import aws_iam as iam
        
        # role: iam.Role
        
        unmanaged_compute_environment = batch_alpha.UnmanagedComputeEnvironment(self, "MyUnmanagedComputeEnvironment",
            compute_environment_name="computeEnvironmentName",
            enabled=False,
            service_role=role,
            unmanagedv_cpus=123
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        unmanagedv_cpus: typing.Optional[jsii.Number] = None,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param unmanagedv_cpus: (experimental) The vCPUs this Compute Environment provides. Used only by the scheduler to schedule jobs in ``Queue``s that use ``FairshareSchedulingPolicy``s. **If this parameter is not provided on a fairshare queue, no capacity is reserved**; that is, the ``FairshareSchedulingPolicy`` is ignored. Default: 0
        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8ec1668bdd84e9da8d4f3138d52ee48dcc98eb518f59434abdd9d08eb77c71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UnmanagedComputeEnvironmentProps(
            unmanagedv_cpus=unmanagedv_cpus,
            compute_environment_name=compute_environment_name,
            enabled=enabled,
            service_role=service_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromUnmanagedComputeEnvironmentArn")
    @builtins.classmethod
    def from_unmanaged_compute_environment_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        unmanaged_compute_environment_arn: builtins.str,
    ) -> IUnmanagedComputeEnvironment:
        '''(experimental) Import an UnmanagedComputeEnvironment by its arn.

        :param scope: -
        :param id: -
        :param unmanaged_compute_environment_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04975c179a3ca1bd144e178327353a7b0ad4551c5fbcbec77f85adb60dd52c3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument unmanaged_compute_environment_arn", value=unmanaged_compute_environment_arn, expected_type=type_hints["unmanaged_compute_environment_arn"])
        return typing.cast(IUnmanagedComputeEnvironment, jsii.sinvoke(cls, "fromUnmanagedComputeEnvironmentArn", [scope, id, unmanaged_compute_environment_arn]))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        '''(experimental) The ARN of this compute environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        '''(experimental) The name of the ComputeEnvironment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "serviceRole"))

    @builtins.property
    @jsii.member(jsii_name="unmanagedvCPUs")
    def unmanagedv_cp_us(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The vCPUs this Compute Environment provides. Used only by the scheduler to schedule jobs in ``Queue``s that use ``FairshareSchedulingPolicy``s.

        **If this parameter is not provided on a fairshare queue, no capacity is reserved**;
        that is, the ``FairshareSchedulingPolicy`` is ignored.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unmanagedvCPUs"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.UnmanagedComputeEnvironmentProps",
    jsii_struct_bases=[ComputeEnvironmentProps],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "enabled": "enabled",
        "service_role": "serviceRole",
        "unmanagedv_cpus": "unmanagedvCpus",
    },
)
class UnmanagedComputeEnvironmentProps(ComputeEnvironmentProps):
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        unmanagedv_cpus: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Represents an UnmanagedComputeEnvironment.

        Batch will not provision instances on your behalf
        in this ComputeEvironment.

        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs
        :param unmanagedv_cpus: (experimental) The vCPUs this Compute Environment provides. Used only by the scheduler to schedule jobs in ``Queue``s that use ``FairshareSchedulingPolicy``s. **If this parameter is not provided on a fairshare queue, no capacity is reserved**; that is, the ``FairshareSchedulingPolicy`` is ignored. Default: 0

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch_alpha as batch_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            unmanaged_compute_environment_props = batch_alpha.UnmanagedComputeEnvironmentProps(
                compute_environment_name="computeEnvironmentName",
                enabled=False,
                service_role=role,
                unmanagedv_cpus=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ff6bd98bd0c62bbea69e5a54f99c879fca8729e2ba319baba6a241cfd016386)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument unmanagedv_cpus", value=unmanagedv_cpus, expected_type=type_hints["unmanagedv_cpus"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_role is not None:
            self._values["service_role"] = service_role
        if unmanagedv_cpus is not None:
            self._values["unmanagedv_cpus"] = unmanagedv_cpus

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ComputeEnvironment.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def unmanagedv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The vCPUs this Compute Environment provides. Used only by the scheduler to schedule jobs in ``Queue``s that use ``FairshareSchedulingPolicy``s.

        **If this parameter is not provided on a fairshare queue, no capacity is reserved**;
        that is, the ``FairshareSchedulingPolicy`` is ignored.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("unmanagedv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnmanagedComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IEcsEc2ContainerDefinition, IEcsContainerDefinition)
class EcsEc2ContainerDefinition(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EcsEc2ContainerDefinition",
):
    '''(experimental) A container orchestrated by ECS that uses EC2 resources.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        import aws_cdk.aws_iam as iam
        
        # vpc: ec2.IVpc
        
        
        ecs_job = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256
            )
        )
        
        queue = batch.JobQueue(self, "JobQueue",
            compute_environments=[batch.OrderedComputeEnvironment(
                compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
                    vpc=vpc
                ),
                order=1
            )],
            priority=10
        )
        
        user = iam.User(self, "MyUser")
        ecs_job.grant_submit_job(user, queue)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        gpu: typing.Optional[jsii.Number] = None,
        privileged: typing.Optional[builtins.bool] = None,
        ulimits: typing.Optional[typing.Sequence[typing.Union[Ulimit, typing.Dict[builtins.str, typing.Any]]]] = None,
        cpu: jsii.Number,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        memory: _aws_cdk_ceddda9d.Size,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        linux_parameters: typing.Optional[LinuxParameters] = None,
        logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
        user: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param gpu: (experimental) The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on. Default: - no gpus
        :param privileged: (experimental) When this parameter is true, the container is given elevated permissions on the host container instance (similar to the root user). Default: false
        :param ulimits: (experimental) Limits to set for the user this docker container will run as. Default: - no ulimits
        :param cpu: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. For containers running on EC2 resources, you must specify at least one vCPU.
        :param image: (experimental) The image that this container will run.
        :param memory: (experimental) The memory hard limit present to the container. If your container attempts to exceed the memory specified, the container is terminated. You must specify at least 4 MiB of memory for a job.
        :param command: (experimental) The command that's passed to the container. Default: - no command
        :param environment: (experimental) The environment variables to pass to a container. Cannot start with ``AWS_BATCH``. We don't recommend using plaintext environment variables for sensitive information, such as credential data. Default: - no environment variables
        :param execution_role: (experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf. Default: - a Role will be created
        :param job_role: (experimental) The role that the container can assume. Default: - no job role
        :param linux_parameters: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. Default: none
        :param logging: (experimental) The loging configuration for this Job. Default: - the log configuration of the Docker daemon
        :param readonly_root_filesystem: (experimental) Gives the container readonly access to its root filesystem. Default: false
        :param secrets: (experimental) A map from environment variable names to the secrets for the container. Allows your job definitions to reference the secret by the environment variable name defined in this property. Default: - no secrets
        :param user: (experimental) The user name to use inside the container. Default: - no user
        :param volumes: (experimental) The volumes to mount to this container. Automatically added to the job definition. Default: - no volumes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__703337fcfe6e1c52132bd99ed93a15029f92d7846e2d4ce71fd4fe473a99b3ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsEc2ContainerDefinitionProps(
            gpu=gpu,
            privileged=privileged,
            ulimits=ulimits,
            cpu=cpu,
            image=image,
            memory=memory,
            command=command,
            environment=environment,
            execution_role=execution_role,
            job_role=job_role,
            linux_parameters=linux_parameters,
            logging=logging,
            readonly_root_filesystem=readonly_root_filesystem,
            secrets=secrets,
            user=user,
            volumes=volumes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addUlimit")
    def add_ulimit(
        self,
        *,
        hard_limit: jsii.Number,
        name: UlimitName,
        soft_limit: jsii.Number,
    ) -> None:
        '''(experimental) Add a ulimit to this container.

        :param hard_limit: (experimental) The hard limit for this resource. The container will be terminated if it exceeds this limit.
        :param name: (experimental) The resource to limit.
        :param soft_limit: (experimental) The reservation for this resource. The container will not be terminated if it exceeds this limit.

        :stability: experimental
        '''
        ulimit = Ulimit(hard_limit=hard_limit, name=name, soft_limit=soft_limit)

        return typing.cast(None, jsii.invoke(self, "addUlimit", [ulimit]))

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EcsVolume) -> None:
        '''(experimental) Add a Volume to this container.

        :param volume: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee557c571178dc5154d52600836940cca88204ce5a09d4644c49746ad660498b)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        return typing.cast(None, jsii.invoke(self, "addVolume", [volume]))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "executionRole"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.Size, jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="ulimits")
    def ulimits(self) -> typing.List[Ulimit]:
        '''(experimental) Limits to set for the user this docker container will run as.

        :stability: experimental
        '''
        return typing.cast(typing.List[Ulimit], jsii.get(self, "ulimits"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EcsVolume]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :stability: experimental
        '''
        return typing.cast(typing.List[EcsVolume], jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="gpu")
    def gpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of physical GPUs to reserve for the container.

        Make sure that the number of GPUs reserved for all containers in a job doesn't exceed
        the number of available GPUs on the compute resource that the job is launched on.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpu"))

    @builtins.property
    @jsii.member(jsii_name="jobRole")
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "jobRole"))

    @builtins.property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional[LinuxParameters]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[LinuxParameters], jsii.get(self, "linuxParameters"))

    @builtins.property
    @jsii.member(jsii_name="logDriverConfig")
    def log_driver_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig]:
        '''(experimental) The configuration of the log driver.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig], jsii.get(self, "logDriverConfig"))

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When this parameter is true, the container is given elevated permissions on the host container instance (similar to the root user).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "privileged"))

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonlyRootFilesystem"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, Secret]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, Secret]], jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "user"))


@jsii.implements(IEcsFargateContainerDefinition, IEcsContainerDefinition)
class EcsFargateContainerDefinition(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EcsFargateContainerDefinition",
):
    '''(experimental) A container orchestrated by ECS that uses Fargate resources.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch_alpha as batch_alpha
        import aws_cdk as cdk
        from aws_cdk import aws_ecs as ecs
        from aws_cdk import aws_iam as iam
        
        # container_image: ecs.ContainerImage
        # ecs_volume: batch_alpha.EcsVolume
        # linux_parameters: batch_alpha.LinuxParameters
        # log_driver: ecs.LogDriver
        # role: iam.Role
        # secret: batch_alpha.Secret
        # size: cdk.Size
        
        ecs_fargate_container_definition = batch_alpha.EcsFargateContainerDefinition(self, "MyEcsFargateContainerDefinition",
            cpu=123,
            image=container_image,
            memory=size,
        
            # the properties below are optional
            assign_public_ip=False,
            command=["command"],
            environment={
                "environment_key": "environment"
            },
            ephemeral_storage_size=size,
            execution_role=role,
            fargate_platform_version=ecs.FargatePlatformVersion.LATEST,
            job_role=role,
            linux_parameters=linux_parameters,
            logging=log_driver,
            readonly_root_filesystem=False,
            secrets={
                "secrets_key": secret
            },
            user="user",
            volumes=[ecs_volume]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        fargate_platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
        cpu: jsii.Number,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        memory: _aws_cdk_ceddda9d.Size,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        linux_parameters: typing.Optional[LinuxParameters] = None,
        logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
        user: typing.Optional[builtins.str] = None,
        volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assign_public_ip: (experimental) Indicates whether the job has a public IP address. For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet. Default: false
        :param ephemeral_storage_size: (experimental) The size for ephemeral storage. Default: - 20 GiB
        :param fargate_platform_version: (experimental) Which version of Fargate to use when running this container. Default: LATEST
        :param cpu: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. For containers running on EC2 resources, you must specify at least one vCPU.
        :param image: (experimental) The image that this container will run.
        :param memory: (experimental) The memory hard limit present to the container. If your container attempts to exceed the memory specified, the container is terminated. You must specify at least 4 MiB of memory for a job.
        :param command: (experimental) The command that's passed to the container. Default: - no command
        :param environment: (experimental) The environment variables to pass to a container. Cannot start with ``AWS_BATCH``. We don't recommend using plaintext environment variables for sensitive information, such as credential data. Default: - no environment variables
        :param execution_role: (experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf. Default: - a Role will be created
        :param job_role: (experimental) The role that the container can assume. Default: - no job role
        :param linux_parameters: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. Default: none
        :param logging: (experimental) The loging configuration for this Job. Default: - the log configuration of the Docker daemon
        :param readonly_root_filesystem: (experimental) Gives the container readonly access to its root filesystem. Default: false
        :param secrets: (experimental) A map from environment variable names to the secrets for the container. Allows your job definitions to reference the secret by the environment variable name defined in this property. Default: - no secrets
        :param user: (experimental) The user name to use inside the container. Default: - no user
        :param volumes: (experimental) The volumes to mount to this container. Automatically added to the job definition. Default: - no volumes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9043358a0ec27fcc739211bbd1e2d8ba93a21bd15df808d7f8d3ccd8380718a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsFargateContainerDefinitionProps(
            assign_public_ip=assign_public_ip,
            ephemeral_storage_size=ephemeral_storage_size,
            fargate_platform_version=fargate_platform_version,
            cpu=cpu,
            image=image,
            memory=memory,
            command=command,
            environment=environment,
            execution_role=execution_role,
            job_role=job_role,
            linux_parameters=linux_parameters,
            logging=logging,
            readonly_root_filesystem=readonly_root_filesystem,
            secrets=secrets,
            user=user,
            volumes=volumes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EcsVolume) -> None:
        '''(experimental) Add a Volume to this container.

        :param volume: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5bc155ea09c4fdbae8e8ba2169b1dad78f860c6fe7189a54c9b4705abda28be)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        return typing.cast(None, jsii.invoke(self, "addVolume", [volume]))

    @builtins.property
    @jsii.member(jsii_name="cpu")
    def cpu(self) -> jsii.Number:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to 1,024 CPU shares.
        For containers running on EC2 resources, you must specify at least one vCPU.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "cpu"))

    @builtins.property
    @jsii.member(jsii_name="executionRole")
    def execution_role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(experimental) The role used by Amazon ECS container and AWS Fargate agents to make AWS API calls on your behalf.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, jsii.get(self, "executionRole"))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="memory")
    def memory(self) -> _aws_cdk_ceddda9d.Size:
        '''(experimental) The memory hard limit present to the container.

        If your container attempts to exceed the memory specified, the container is terminated.
        You must specify at least 4 MiB of memory for a job.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.Size, jsii.get(self, "memory"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EcsVolume]:
        '''(experimental) The volumes to mount to this container.

        Automatically added to the job definition.

        :stability: experimental
        '''
        return typing.cast(typing.List[EcsVolume], jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether the job has a public IP address.

        For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet
        (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "assignPublicIp"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that's passed to the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to a container.

        Cannot start with ``AWS_BATCH``.
        We don't recommend using plaintext environment variables for sensitive information, such as credential data.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "environment"))

    @builtins.property
    @jsii.member(jsii_name="ephemeralStorageSize")
    def ephemeral_storage_size(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The size for ephemeral storage.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "ephemeralStorageSize"))

    @builtins.property
    @jsii.member(jsii_name="fargatePlatformVersion")
    def fargate_platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion]:
        '''(experimental) Which version of Fargate to use when running this container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion], jsii.get(self, "fargatePlatformVersion"))

    @builtins.property
    @jsii.member(jsii_name="jobRole")
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role that the container can assume.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "jobRole"))

    @builtins.property
    @jsii.member(jsii_name="linuxParameters")
    def linux_parameters(self) -> typing.Optional[LinuxParameters]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[LinuxParameters], jsii.get(self, "linuxParameters"))

    @builtins.property
    @jsii.member(jsii_name="logDriverConfig")
    def log_driver_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig]:
        '''(experimental) The configuration of the log driver.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriverConfig], jsii.get(self, "logDriverConfig"))

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Gives the container readonly access to its root filesystem.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonlyRootFilesystem"))

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Optional[typing.Mapping[builtins.str, Secret]]:
        '''(experimental) A map from environment variable names to the secrets for the container.

        Allows your job definitions
        to reference the secret by the environment variable name defined in this property.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, Secret]], jsii.get(self, "secrets"))

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "user"))


@jsii.implements(IJobDefinition)
class EcsJobDefinition(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EcsJobDefinition",
):
    '''(experimental) A JobDefinition that uses ECS orchestration.

    :stability: experimental
    :resource: AWS::Batch::JobDefinition
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        import aws_cdk.aws_iam as iam
        
        # vpc: ec2.IVpc
        
        
        ecs_job = batch.EcsJobDefinition(self, "JobDefn",
            container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                memory=cdk.Size.mebibytes(2048),
                cpu=256
            )
        )
        
        queue = batch.JobQueue(self, "JobQueue",
            compute_environments=[batch.OrderedComputeEnvironment(
                compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
                    vpc=vpc
                ),
                order=1
            )],
            priority=10
        )
        
        user = iam.User(self, "MyUser")
        ecs_job.grant_submit_job(user, queue)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        container: IEcsContainerDefinition,
        propagate_tags: typing.Optional[builtins.bool] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param container: (experimental) The container that this job will run.
        :param propagate_tags: (experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns. Default: false
        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d22fe551a7ec9dc3ab5dca1924a9459f34e7c4a858584cd7f476997617a7257f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcsJobDefinitionProps(
            container=container,
            propagate_tags=propagate_tags,
            job_definition_name=job_definition_name,
            parameters=parameters,
            retry_attempts=retry_attempts,
            retry_strategies=retry_strategies,
            scheduling_priority=scheduling_priority,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromJobDefinitionArn")
    @builtins.classmethod
    def from_job_definition_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        job_definition_arn: builtins.str,
    ) -> IJobDefinition:
        '''(experimental) Import a JobDefinition by its arn.

        :param scope: -
        :param id: -
        :param job_definition_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab639941f3154616eec16a5022b72152eb79cf04c72b8b8e12ce55072631cf45)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_definition_arn", value=job_definition_arn, expected_type=type_hints["job_definition_arn"])
        return typing.cast(IJobDefinition, jsii.sinvoke(cls, "fromJobDefinitionArn", [scope, id, job_definition_arn]))

    @jsii.member(jsii_name="addRetryStrategy")
    def add_retry_strategy(self, strategy: RetryStrategy) -> None:
        '''(experimental) Add a RetryStrategy to this JobDefinition.

        :param strategy: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a94917adb1283e62eedbe5223f4a93a91485e876d85dcbcc25496d14009867e7)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        return typing.cast(None, jsii.invoke(self, "addRetryStrategy", [strategy]))

    @jsii.member(jsii_name="grantSubmitJob")
    def grant_submit_job(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        queue: IJobQueue,
    ) -> None:
        '''(experimental) Grants the ``batch:submitJob`` permission to the identity on both this job definition and the ``queue``.

        :param identity: -
        :param queue: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029b7552867bfe3ab6c1c2c24488738b70372469bb39e29a696bc8b1f2cc20cc)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        return typing.cast(None, jsii.invoke(self, "grantSubmitJob", [identity, queue]))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> IEcsContainerDefinition:
        '''(experimental) The container that this job will run.

        :stability: experimental
        '''
        return typing.cast(IEcsContainerDefinition, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionArn"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of this job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionName"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategies")
    def retry_strategies(self) -> typing.List[RetryStrategy]:
        '''(experimental) Defines the retry behavior for this job.

        :stability: experimental
        '''
        return typing.cast(typing.List[RetryStrategy], jsii.get(self, "retryStrategies"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "propagateTags"))

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPriority")
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulingPriority"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EcsJobDefinitionProps",
    jsii_struct_bases=[JobDefinitionProps],
    name_mapping={
        "job_definition_name": "jobDefinitionName",
        "parameters": "parameters",
        "retry_attempts": "retryAttempts",
        "retry_strategies": "retryStrategies",
        "scheduling_priority": "schedulingPriority",
        "timeout": "timeout",
        "container": "container",
        "propagate_tags": "propagateTags",
    },
)
class EcsJobDefinitionProps(JobDefinitionProps):
    def __init__(
        self,
        *,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        container: IEcsContainerDefinition,
        propagate_tags: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Props for EcsJobDefinition.

        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout
        :param container: (experimental) The container that this job will run.
        :param propagate_tags: (experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            import aws_cdk.aws_iam as iam
            
            # vpc: ec2.IVpc
            
            
            ecs_job = batch.EcsJobDefinition(self, "JobDefn",
                container=batch.EcsEc2ContainerDefinition(self, "containerDefn",
                    image=ecs.ContainerImage.from_registry("public.ecr.aws/amazonlinux/amazonlinux:latest"),
                    memory=cdk.Size.mebibytes(2048),
                    cpu=256
                )
            )
            
            queue = batch.JobQueue(self, "JobQueue",
                compute_environments=[batch.OrderedComputeEnvironment(
                    compute_environment=batch.ManagedEc2EcsComputeEnvironment(self, "managedEc2CE",
                        vpc=vpc
                    ),
                    order=1
                )],
                priority=10
            )
            
            user = iam.User(self, "MyUser")
            ecs_job.grant_submit_job(user, queue)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3422a4d894c1df05100df13e7a265d056c4ea6456cfc0b39da47fd91e557c54b)
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_strategies", value=retry_strategies, expected_type=type_hints["retry_strategies"])
            check_type(argname="argument scheduling_priority", value=scheduling_priority, expected_type=type_hints["scheduling_priority"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
        }
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_strategies is not None:
            self._values["retry_strategies"] = retry_strategies
        if scheduling_priority is not None:
            self._values["scheduling_priority"] = scheduling_priority
        if timeout is not None:
            self._values["timeout"] = timeout
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this job definition.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :default: none

        :see: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html#parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_strategies(self) -> typing.Optional[typing.List[RetryStrategy]]:
        '''(experimental) Defines the retry behavior for this job.

        :default: - no ``RetryStrategy``

        :stability: experimental
        '''
        result = self._values.get("retry_strategies")
        return typing.cast(typing.Optional[typing.List[RetryStrategy]], result)

    @builtins.property
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("scheduling_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :default: - no timeout

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def container(self) -> IEcsContainerDefinition:
        '''(experimental) The container that this job will run.

        :stability: experimental
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(IEcsContainerDefinition, result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to propogate tags from the JobDefinition to the ECS task that Batch spawns.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsJobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IEksContainerDefinition)
class EksContainerDefinition(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EksContainerDefinition",
):
    '''(experimental) A container that can be run with EKS orchestration on EC2 resources.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        job_defn = batch.EksJobDefinition(self, "eksf2",
            container=batch.EksContainerDefinition(self, "container",
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                volumes=[batch.EksVolume.empty_dir(
                    name="myEmptyDirVolume",
                    mount_path="/mount/path",
                    medium=batch.EmptyDirMediumType.MEMORY,
                    readonly=True,
                    size_limit=cdk.Size.mebibytes(2048)
                )]
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
        args: typing.Optional[typing.Sequence[builtins.str]] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        cpu_limit: typing.Optional[jsii.Number] = None,
        cpu_reservation: typing.Optional[jsii.Number] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        gpu_limit: typing.Optional[jsii.Number] = None,
        gpu_reservation: typing.Optional[jsii.Number] = None,
        image_pull_policy: typing.Optional[ImagePullPolicy] = None,
        memory_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        memory_reservation: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
        name: typing.Optional[builtins.str] = None,
        privileged: typing.Optional[builtins.bool] = None,
        readonly_root_filesystem: typing.Optional[builtins.bool] = None,
        run_as_group: typing.Optional[jsii.Number] = None,
        run_as_root: typing.Optional[builtins.bool] = None,
        run_as_user: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Sequence[EksVolume]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param image: (experimental) The image that this container will run.
        :param args: (experimental) An array of arguments to the entrypoint. If this isn't specified, the CMD of the container image is used. This corresponds to the args member in the Entrypoint portion of the Pod in Kubernetes. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to "$(NAME1)" and the NAME1 environment variable doesn't exist, the command string will remain "$(NAME1)." $$ is replaced with $, and the resulting string isn't expanded. or example, $$(VAR_NAME) is passed as $(VAR_NAME) whether or not the VAR_NAME environment variable exists. Default: - no args
        :param command: (experimental) The entrypoint for the container. This isn't run within a shell. If this isn't specified, the ``ENTRYPOINT`` of the container image is used. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to ``"$(NAME1)"`` and the ``NAME1`` environment variable doesn't exist, the command string will remain ``"$(NAME1)."`` ``$$`` is replaced with ``$`` and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. The entrypoint can't be updated. Default: - no command
        :param cpu_limit: (experimental) The hard limit of CPUs to present to this container. Must be an even multiple of 0.25. If your container attempts to exceed this limit, it will be terminated. At least one of ``cpuReservation`` and ``cpuLimit`` is required. If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``. Default: - No CPU limit
        :param cpu_reservation: (experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25. The container will given at least this many CPUs, but may consume more. At least one of ``cpuReservation`` and ``cpuLimit`` is required. If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``. Default: - No CPUs reserved
        :param env: (experimental) The environment variables to pass to this container. *Note*: Environment variables cannot start with "AWS_BATCH". This naming convention is reserved for variables that AWS Batch sets. Default: - no environment variables
        :param gpu_limit: (experimental) The hard limit of GPUs to present to this container. If your container attempts to exceed this limit, it will be terminated. If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``. Default: - No GPU limit
        :param gpu_reservation: (experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25. The container will given at least this many CPUs, but may consume more. If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``. Default: - No GPUs reserved
        :param image_pull_policy: (experimental) The image pull policy for this container. Default: - ``ALWAYS`` if the ``:latest`` tag is specified, ``IF_NOT_PRESENT`` otherwise
        :param memory_limit: (experimental) The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, it will be terminated. Must be larger that 4 MiB At least one of ``memoryLimit`` and ``memoryReservation`` is required *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible for the specific instance type that you are using. Default: - No memory limit
        :param memory_reservation: (experimental) The soft limit (in MiB) of memory to reserve for the container. Your container will be given at least this much memory, but may consume more. Must be larger that 4 MiB When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of ``memoryLimit`` and ``memoryReservation`` is required. If both are specified, then ``memoryLimit`` must be equal to ``memoryReservation`` *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible for the specific instance type that you are using. Default: - No memory reserved
        :param name: (experimental) The name of this container. Default: : ``'Default'``
        :param privileged: (experimental) If specified, gives this container elevated permissions on the host container instance. The level of permissions are similar to the root user permissions. This parameter maps to ``privileged`` policy in the Privileged pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: false
        :param readonly_root_filesystem: (experimental) If specified, gives this container readonly access to its root file system. This parameter maps to ``ReadOnlyRootFilesystem`` policy in the Volumes and file systems pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: false
        :param run_as_group: (experimental) If specified, the container is run as the specified group ID (``gid``). If this parameter isn't specified, the default is the group that's specified in the image metadata. This parameter maps to ``RunAsGroup`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: none
        :param run_as_root: (experimental) If specified, the container is run as a user with a ``uid`` other than 0. Otherwise, no such rule is enforced. This parameter maps to ``RunAsUser`` and ``MustRunAsNonRoot`` policy in the Users and groups pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: - the container is *not* required to run as a non-root user
        :param run_as_user: (experimental) If specified, this container is run as the specified user ID (``uid``). This parameter maps to ``RunAsUser`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation. *Note*: this is only compatible with Kubernetes < v1.25 Default: - the user that is specified in the image metadata.
        :param volumes: (experimental) The Volumes to mount to this container. Automatically added to the Pod. Default: - no volumes

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa55a51376bba78f2a58e4b4a9b815797d08470292f55790f7760ca8960c8117)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EksContainerDefinitionProps(
            image=image,
            args=args,
            command=command,
            cpu_limit=cpu_limit,
            cpu_reservation=cpu_reservation,
            env=env,
            gpu_limit=gpu_limit,
            gpu_reservation=gpu_reservation,
            image_pull_policy=image_pull_policy,
            memory_limit=memory_limit,
            memory_reservation=memory_reservation,
            name=name,
            privileged=privileged,
            readonly_root_filesystem=readonly_root_filesystem,
            run_as_group=run_as_group,
            run_as_root=run_as_root,
            run_as_user=run_as_user,
            volumes=volumes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addVolume")
    def add_volume(self, volume: EksVolume) -> None:
        '''(experimental) Mount a Volume to this container.

        Automatically added to the Pod.

        :param volume: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f08fa019f05afced1d0b0b9ae2f275b52da9043803f2ae598f3771a9435ad8b3)
            check_type(argname="argument volume", value=volume, expected_type=type_hints["volume"])
        return typing.cast(None, jsii.invoke(self, "addVolume", [volume]))

    @builtins.property
    @jsii.member(jsii_name="image")
    def image(self) -> _aws_cdk_aws_ecs_ceddda9d.ContainerImage:
        '''(experimental) The image that this container will run.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ContainerImage, jsii.get(self, "image"))

    @builtins.property
    @jsii.member(jsii_name="volumes")
    def volumes(self) -> typing.List[EksVolume]:
        '''(experimental) The Volumes to mount to this container.

        Automatically added to the Pod.

        :stability: experimental
        '''
        return typing.cast(typing.List[EksVolume], jsii.get(self, "volumes"))

    @builtins.property
    @jsii.member(jsii_name="args")
    def args(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) An array of arguments to the entrypoint.

        If this isn't specified, the CMD of the container image is used.
        This corresponds to the args member in the Entrypoint portion of the Pod in Kubernetes.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to "$(NAME1)" and the NAME1 environment variable doesn't exist,
        the command string will remain "$(NAME1)." $$ is replaced with $, and the resulting string isn't expanded.
        or example, $$(VAR_NAME) is passed as $(VAR_NAME) whether or not the VAR_NAME environment variable exists.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "args"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The entrypoint for the container.

        This isn't run within a shell.
        If this isn't specified, the ``ENTRYPOINT`` of the container image is used.
        Environment variable references are expanded using the container's environment.
        If the referenced environment variable doesn't exist, the reference in the command isn't changed.
        For example, if the reference is to ``"$(NAME1)"`` and the ``NAME1`` environment variable doesn't exist,
        the command string will remain ``"$(NAME1)."`` ``$$`` is replaced with ``$`` and the resulting string isn't expanded.
        For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists.

        The entrypoint can't be updated.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="cpuLimit")
    def cpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of CPUs to present to this container. Must be an even multiple of 0.25.

        If your container attempts to exceed this limit, it will be terminated.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuLimit"))

    @builtins.property
    @jsii.member(jsii_name="cpuReservation")
    def cpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        At least one of ``cpuReservation`` and ``cpuLimit`` is required.
        If both are specified, then ``cpuLimit`` must be at least as large as ``cpuReservation``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "cpuReservation"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to this container.

        *Note*: Environment variables cannot start with "AWS_BATCH".
        This naming convention is reserved for variables that AWS Batch sets.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="gpuLimit")
    def gpu_limit(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit of GPUs to present to this container.

        If your container attempts to exceed this limit, it will be terminated.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuLimit"))

    @builtins.property
    @jsii.member(jsii_name="gpuReservation")
    def gpu_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit of CPUs to reserve for the container Must be an even multiple of 0.25.

        The container will given at least this many CPUs, but may consume more.

        If both ``gpuReservation`` and ``gpuLimit`` are specified, then ``gpuLimit`` must be equal to ``gpuReservation``.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "gpuReservation"))

    @builtins.property
    @jsii.member(jsii_name="imagePullPolicy")
    def image_pull_policy(self) -> typing.Optional[ImagePullPolicy]:
        '''(experimental) The image pull policy for this container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[ImagePullPolicy], jsii.get(self, "imagePullPolicy"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def memory_limit(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, it will be terminated.

        Must be larger that 4 MiB

        At least one of ``memoryLimit`` and ``memoryReservation`` is required

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "memoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="memoryReservation")
    def memory_reservation(self) -> typing.Optional[_aws_cdk_ceddda9d.Size]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        Your container will be given at least this much memory, but may consume more.

        Must be larger that 4 MiB

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of ``memoryLimit`` and ``memoryReservation`` is required.
        If both are specified, then ``memoryLimit`` must be equal to ``memoryReservation``

        *Note*: To maximize your resource utilization, provide your jobs with as much memory as possible
        for the specific instance type that you are using.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Size], jsii.get(self, "memoryReservation"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="privileged")
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container elevated permissions on the host container instance.

        The level of permissions are similar to the root user permissions.

        This parameter maps to ``privileged`` policy in the Privileged pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "privileged"))

    @builtins.property
    @jsii.member(jsii_name="readonlyRootFilesystem")
    def readonly_root_filesystem(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, gives this container readonly access to its root file system.

        This parameter maps to ``ReadOnlyRootFilesystem`` policy in the Volumes and file systems pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "readonlyRootFilesystem"))

    @builtins.property
    @jsii.member(jsii_name="runAsGroup")
    def run_as_group(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, the container is run as the specified group ID (``gid``).

        If this parameter isn't specified, the default is the group that's specified in the image metadata.
        This parameter maps to ``RunAsGroup`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runAsGroup"))

    @builtins.property
    @jsii.member(jsii_name="runAsRoot")
    def run_as_root(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the container is run as a user with a ``uid`` other than 0.

        Otherwise, no such rule is enforced.
        This parameter maps to ``RunAsUser`` and ``MustRunAsNonRoot`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "runAsRoot"))

    @builtins.property
    @jsii.member(jsii_name="runAsUser")
    def run_as_user(self) -> typing.Optional[jsii.Number]:
        '''(experimental) If specified, this container is run as the specified user ID (``uid``).

        This parameter maps to ``RunAsUser`` and ``MustRunAs`` policy in the Users and groups pod security policies in the Kubernetes documentation.

        *Note*: this is only compatible with Kubernetes < v1.25

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "runAsUser"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.EksJobDefinitionProps",
    jsii_struct_bases=[JobDefinitionProps],
    name_mapping={
        "job_definition_name": "jobDefinitionName",
        "parameters": "parameters",
        "retry_attempts": "retryAttempts",
        "retry_strategies": "retryStrategies",
        "scheduling_priority": "schedulingPriority",
        "timeout": "timeout",
        "container": "container",
        "dns_policy": "dnsPolicy",
        "service_account": "serviceAccount",
        "use_host_network": "useHostNetwork",
    },
)
class EksJobDefinitionProps(JobDefinitionProps):
    def __init__(
        self,
        *,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        container: EksContainerDefinition,
        dns_policy: typing.Optional[DnsPolicy] = None,
        service_account: typing.Optional[builtins.str] = None,
        use_host_network: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Props for EksJobDefinition.

        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout
        :param container: (experimental) The container this Job Definition will run.
        :param dns_policy: (experimental) The DNS Policy of the pod used by this Job Definition. Default: ``DnsPolicy.CLUSTER_FIRST``
        :param service_account: (experimental) The name of the service account that's used to run the container. service accounts are Kubernetes method of identification and authentication, roughly analogous to IAM users. Default: - the default service account of the container
        :param use_host_network: (experimental) If specified, the Pod used by this Job Definition will use the host's network IP address. Otherwise, the Kubernetes pod networking model is enabled. Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk as cdk
            
            job_defn = batch.EksJobDefinition(self, "eksf2",
                container=batch.EksContainerDefinition(self, "container",
                    image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                    volumes=[batch.EksVolume.empty_dir(
                        name="myEmptyDirVolume",
                        mount_path="/mount/path",
                        medium=batch.EmptyDirMediumType.MEMORY,
                        readonly=True,
                        size_limit=cdk.Size.mebibytes(2048)
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8b77d33798657223ab8a68e0a96698e9f50b309f5eea8bc7599133c6945dc82)
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument retry_strategies", value=retry_strategies, expected_type=type_hints["retry_strategies"])
            check_type(argname="argument scheduling_priority", value=scheduling_priority, expected_type=type_hints["scheduling_priority"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument dns_policy", value=dns_policy, expected_type=type_hints["dns_policy"])
            check_type(argname="argument service_account", value=service_account, expected_type=type_hints["service_account"])
            check_type(argname="argument use_host_network", value=use_host_network, expected_type=type_hints["use_host_network"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
        }
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if parameters is not None:
            self._values["parameters"] = parameters
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if retry_strategies is not None:
            self._values["retry_strategies"] = retry_strategies
        if scheduling_priority is not None:
            self._values["scheduling_priority"] = scheduling_priority
        if timeout is not None:
            self._values["timeout"] = timeout
        if dns_policy is not None:
            self._values["dns_policy"] = dns_policy
        if service_account is not None:
            self._values["service_account"] = service_account
        if use_host_network is not None:
            self._values["use_host_network"] = use_host_network

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of this job definition.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :default: none

        :see: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html#parameters
        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retry_strategies(self) -> typing.Optional[typing.List[RetryStrategy]]:
        '''(experimental) Defines the retry behavior for this job.

        :default: - no ``RetryStrategy``

        :stability: experimental
        '''
        result = self._values.get("retry_strategies")
        return typing.cast(typing.Optional[typing.List[RetryStrategy]], result)

    @builtins.property
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("scheduling_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :default: - no timeout

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def container(self) -> EksContainerDefinition:
        '''(experimental) The container this Job Definition will run.

        :stability: experimental
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(EksContainerDefinition, result)

    @builtins.property
    def dns_policy(self) -> typing.Optional[DnsPolicy]:
        '''(experimental) The DNS Policy of the pod used by this Job Definition.

        :default: ``DnsPolicy.CLUSTER_FIRST``

        :see: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy
        :stability: experimental
        '''
        result = self._values.get("dns_policy")
        return typing.cast(typing.Optional[DnsPolicy], result)

    @builtins.property
    def service_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the service account that's used to run the container.

        service accounts are Kubernetes method of identification and authentication,
        roughly analogous to IAM users.

        :default: - the default service account of the container

        :see: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html
        :stability: experimental
        '''
        result = self._values.get("service_account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_host_network(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the Pod used by this Job Definition will use the host's network IP address.

        Otherwise, the Kubernetes pod networking model is enabled.
        Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections.

        :default: true

        :see: https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking
        :stability: experimental
        '''
        result = self._values.get("use_host_network")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksJobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch-alpha.FargateComputeEnvironmentProps",
    jsii_struct_bases=[ManagedComputeEnvironmentProps],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "enabled": "enabled",
        "service_role": "serviceRole",
        "vpc": "vpc",
        "maxv_cpus": "maxvCpus",
        "replace_compute_environment": "replaceComputeEnvironment",
        "security_groups": "securityGroups",
        "spot": "spot",
        "terminate_on_update": "terminateOnUpdate",
        "update_timeout": "updateTimeout",
        "update_to_latest_image_version": "updateToLatestImageVersion",
        "vpc_subnets": "vpcSubnets",
    },
)
class FargateComputeEnvironmentProps(ManagedComputeEnvironmentProps):
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Props for a FargateComputeEnvironment.

        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.IVpc
            
            shared_compute_env = batch.FargateComputeEnvironment(self, "spotEnv",
                vpc=vpc,
                spot=True
            )
            low_priority_queue = batch.JobQueue(self, "JobQueue",
                priority=1
            )
            high_priority_queue = batch.JobQueue(self, "JobQueue",
                priority=10
            )
            low_priority_queue.add_compute_environment(shared_compute_env, 1)
            high_priority_queue.add_compute_environment(shared_compute_env, 1)
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90829606627d5bace90cbad01656e3373471c075f52752633c48258b671deb61)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
            check_type(argname="argument replace_compute_environment", value=replace_compute_environment, expected_type=type_hints["replace_compute_environment"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot", value=spot, expected_type=type_hints["spot"])
            check_type(argname="argument terminate_on_update", value=terminate_on_update, expected_type=type_hints["terminate_on_update"])
            check_type(argname="argument update_timeout", value=update_timeout, expected_type=type_hints["update_timeout"])
            check_type(argname="argument update_to_latest_image_version", value=update_to_latest_image_version, expected_type=type_hints["update_to_latest_image_version"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if enabled is not None:
            self._values["enabled"] = enabled
        if service_role is not None:
            self._values["service_role"] = service_role
        if maxv_cpus is not None:
            self._values["maxv_cpus"] = maxv_cpus
        if replace_compute_environment is not None:
            self._values["replace_compute_environment"] = replace_compute_environment
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot is not None:
            self._values["spot"] = spot
        if terminate_on_update is not None:
            self._values["terminate_on_update"] = terminate_on_update
        if update_timeout is not None:
            self._values["update_timeout"] = update_timeout
        if update_to_latest_image_version is not None:
            self._values["update_to_latest_image_version"] = update_to_latest_image_version
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the ComputeEnvironment.

        :default: - generated by CloudFormation

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_ceddda9d.IVpc:
        '''(experimental) VPC in which this Compute Environment will launch Instances.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.IVpc, result)

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :default: 256

        :stability: experimental
        '''
        result = self._values.get("maxv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :default: false

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html
        :stability: experimental
        '''
        result = self._values.get("replace_compute_environment")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :default: new security groups will be created

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("spot")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :default: false

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("terminate_on_update")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :default: 30 minutes

        :see: https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html
        :stability: experimental
        '''
        result = self._values.get("update_timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("update_to_latest_image_version")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(experimental) The VPC Subnets this Compute Environment will launch instances in.

        :default: new subnets will be created

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IEksJobDefinition")
class IEksJobDefinition(IJobDefinition, typing_extensions.Protocol):
    '''(experimental) A JobDefinition that uses Eks orchestration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> EksContainerDefinition:
        '''(experimental) The container this Job Definition will run.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="dnsPolicy")
    def dns_policy(self) -> typing.Optional[DnsPolicy]:
        '''(experimental) The DNS Policy of the pod used by this Job Definition.

        :default: ``DnsPolicy.CLUSTER_FIRST``

        :see: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the service account that's used to run the container.

        service accounts are Kubernetes method of identification and authentication,
        roughly analogous to IAM users.

        :default: - the default service account of the container

        :see: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html
        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="useHostNetwork")
    def use_host_network(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the Pod used by this Job Definition will use the host's network IP address.

        Otherwise, the Kubernetes pod networking model is enabled.
        Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections.

        :default: true

        :see: https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking
        :stability: experimental
        '''
        ...


class _IEksJobDefinitionProxy(
    jsii.proxy_for(IJobDefinition), # type: ignore[misc]
):
    '''(experimental) A JobDefinition that uses Eks orchestration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IEksJobDefinition"

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> EksContainerDefinition:
        '''(experimental) The container this Job Definition will run.

        :stability: experimental
        '''
        return typing.cast(EksContainerDefinition, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="dnsPolicy")
    def dns_policy(self) -> typing.Optional[DnsPolicy]:
        '''(experimental) The DNS Policy of the pod used by this Job Definition.

        :default: ``DnsPolicy.CLUSTER_FIRST``

        :see: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy
        :stability: experimental
        '''
        return typing.cast(typing.Optional[DnsPolicy], jsii.get(self, "dnsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the service account that's used to run the container.

        service accounts are Kubernetes method of identification and authentication,
        roughly analogous to IAM users.

        :default: - the default service account of the container

        :see: https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="useHostNetwork")
    def use_host_network(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the Pod used by this Job Definition will use the host's network IP address.

        Otherwise, the Kubernetes pod networking model is enabled.
        Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections.

        :default: true

        :see: https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useHostNetwork"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEksJobDefinition).__jsii_proxy_class__ = lambda : _IEksJobDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IFairshareSchedulingPolicy")
class IFairshareSchedulingPolicy(ISchedulingPolicy, typing_extensions.Protocol):
    '''(experimental) Represents a Fairshare Scheduling Policy. Instructs the scheduler to allocate ComputeEnvironment vCPUs based on Job shareIdentifiers.

    The Faireshare Scheduling Policy ensures that each share gets a certain amount of vCPUs.
    It does this by deciding how many Jobs of each share to schedule *relative to how many jobs of
    each share are currently being executed by the ComputeEnvironment*. The weight factors associated with
    each share determine the ratio of vCPUs allocated; see the readme for a more in-depth discussion of
    fairshare policies.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> typing.List[Share]:
        '''(experimental) The shares that this Scheduling Policy applies to.

        *Note*: It is possible to submit Jobs to the queue with Share Identifiers that
        are not recognized by the Scheduling Policy.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="computeReservation")
    def compute_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Used to calculate the percentage of the maximum available vCPU to reserve for share identifiers not present in the Queue.

        The percentage reserved is defined by the Scheduler as:
        ``(computeReservation/100)^ActiveFairShares`` where ``ActiveFairShares`` is the number of active fair share identifiers.

        For example, a computeReservation value of 50 indicates that AWS Batch reserves 50% of the
        maximum available vCPU if there's only one fair share identifier.
        It reserves 25% if there are two fair share identifiers.
        It reserves 12.5% if there are three fair share identifiers.

        A computeReservation value of 25 indicates that AWS Batch should reserve 25% of the
        maximum available vCPU if there's only one fair share identifier,
        6.25% if there are two fair share identifiers,
        and 1.56% if there are three fair share identifiers.

        :default: - no vCPU is reserved

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="shareDecay")
    def share_decay(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The amount of time to use to measure the usage of each job.

        The usage is used to calculate a fair share percentage for each fair share identifier currently in the Queue.
        A value of zero (0) indicates that only current usage is measured.
        The decay is linear and gives preference to newer jobs.

        The maximum supported value is 604800 seconds (1 week).

        :default: - 0: only the current job usage is considered

        :stability: experimental
        '''
        ...


class _IFairshareSchedulingPolicyProxy(
    jsii.proxy_for(ISchedulingPolicy), # type: ignore[misc]
):
    '''(experimental) Represents a Fairshare Scheduling Policy. Instructs the scheduler to allocate ComputeEnvironment vCPUs based on Job shareIdentifiers.

    The Faireshare Scheduling Policy ensures that each share gets a certain amount of vCPUs.
    It does this by deciding how many Jobs of each share to schedule *relative to how many jobs of
    each share are currently being executed by the ComputeEnvironment*. The weight factors associated with
    each share determine the ratio of vCPUs allocated; see the readme for a more in-depth discussion of
    fairshare policies.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IFairshareSchedulingPolicy"

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> typing.List[Share]:
        '''(experimental) The shares that this Scheduling Policy applies to.

        *Note*: It is possible to submit Jobs to the queue with Share Identifiers that
        are not recognized by the Scheduling Policy.

        :stability: experimental
        '''
        return typing.cast(typing.List[Share], jsii.get(self, "shares"))

    @builtins.property
    @jsii.member(jsii_name="computeReservation")
    def compute_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Used to calculate the percentage of the maximum available vCPU to reserve for share identifiers not present in the Queue.

        The percentage reserved is defined by the Scheduler as:
        ``(computeReservation/100)^ActiveFairShares`` where ``ActiveFairShares`` is the number of active fair share identifiers.

        For example, a computeReservation value of 50 indicates that AWS Batch reserves 50% of the
        maximum available vCPU if there's only one fair share identifier.
        It reserves 25% if there are two fair share identifiers.
        It reserves 12.5% if there are three fair share identifiers.

        A computeReservation value of 25 indicates that AWS Batch should reserve 25% of the
        maximum available vCPU if there's only one fair share identifier,
        6.25% if there are two fair share identifiers,
        and 1.56% if there are three fair share identifiers.

        :default: - no vCPU is reserved

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeReservation"))

    @builtins.property
    @jsii.member(jsii_name="shareDecay")
    def share_decay(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The amount of time to use to measure the usage of each job.

        The usage is used to calculate a fair share percentage for each fair share identifier currently in the Queue.
        A value of zero (0) indicates that only current usage is measured.
        The decay is linear and gives preference to newer jobs.

        The maximum supported value is 604800 seconds (1 week).

        :default: - 0: only the current job usage is considered

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "shareDecay"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFairshareSchedulingPolicy).__jsii_proxy_class__ = lambda : _IFairshareSchedulingPolicyProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch-alpha.IFargateComputeEnvironment")
class IFargateComputeEnvironment(
    IManagedComputeEnvironment,
    typing_extensions.Protocol,
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on Fargate instances.

    :stability: experimental
    '''

    pass


class _IFargateComputeEnvironmentProxy(
    jsii.proxy_for(IManagedComputeEnvironment), # type: ignore[misc]
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on Fargate instances.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch-alpha.IFargateComputeEnvironment"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFargateComputeEnvironment).__jsii_proxy_class__ = lambda : _IFargateComputeEnvironmentProxy


@jsii.implements(IEksJobDefinition, IJobDefinition)
class EksJobDefinition(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.EksJobDefinition",
):
    '''(experimental) A JobDefinition that uses Eks orchestration.

    :stability: experimental
    :resource: AWS::Batch::JobDefinition
    :exampleMetadata: infused

    Example::

        import aws_cdk as cdk
        
        job_defn = batch.EksJobDefinition(self, "eksf2",
            container=batch.EksContainerDefinition(self, "container",
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
                volumes=[batch.EksVolume.empty_dir(
                    name="myEmptyDirVolume",
                    mount_path="/mount/path",
                    medium=batch.EmptyDirMediumType.MEMORY,
                    readonly=True,
                    size_limit=cdk.Size.mebibytes(2048)
                )]
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        container: EksContainerDefinition,
        dns_policy: typing.Optional[DnsPolicy] = None,
        service_account: typing.Optional[builtins.str] = None,
        use_host_network: typing.Optional[builtins.bool] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param container: (experimental) The container this Job Definition will run.
        :param dns_policy: (experimental) The DNS Policy of the pod used by this Job Definition. Default: ``DnsPolicy.CLUSTER_FIRST``
        :param service_account: (experimental) The name of the service account that's used to run the container. service accounts are Kubernetes method of identification and authentication, roughly analogous to IAM users. Default: - the default service account of the container
        :param use_host_network: (experimental) If specified, the Pod used by this Job Definition will use the host's network IP address. Otherwise, the Kubernetes pod networking model is enabled. Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections. Default: true
        :param job_definition_name: (experimental) The name of this job definition. Default: - generated by CloudFormation
        :param parameters: (experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container. Default: none
        :param retry_attempts: (experimental) The number of times to retry a job. The job is retried on failure the same number of attempts as the value. Default: 1
        :param retry_strategies: (experimental) Defines the retry behavior for this job. Default: - no ``RetryStrategy``
        :param scheduling_priority: (experimental) The priority of this Job. Only used in Fairshare Scheduling to decide which job to run first when there are multiple jobs with the same share identifier. Default: none
        :param timeout: (experimental) The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, Batch terminates your jobs if they aren't finished. Default: - no timeout

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__493040c2c7ee40246c6a072e076284b76f124d7e7aaaa01e929e603e0120ce38)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EksJobDefinitionProps(
            container=container,
            dns_policy=dns_policy,
            service_account=service_account,
            use_host_network=use_host_network,
            job_definition_name=job_definition_name,
            parameters=parameters,
            retry_attempts=retry_attempts,
            retry_strategies=retry_strategies,
            scheduling_priority=scheduling_priority,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromEksJobDefinitionArn")
    @builtins.classmethod
    def from_eks_job_definition_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        eks_job_definition_arn: builtins.str,
    ) -> IEksJobDefinition:
        '''(experimental) Import an EksJobDefinition by its arn.

        :param scope: -
        :param id: -
        :param eks_job_definition_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402960107d8c9231c93870e789ccea7b4935615a9f98366ceffb6f7117ffb401)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument eks_job_definition_arn", value=eks_job_definition_arn, expected_type=type_hints["eks_job_definition_arn"])
        return typing.cast(IEksJobDefinition, jsii.sinvoke(cls, "fromEksJobDefinitionArn", [scope, id, eks_job_definition_arn]))

    @jsii.member(jsii_name="addRetryStrategy")
    def add_retry_strategy(self, strategy: RetryStrategy) -> None:
        '''(experimental) Add a RetryStrategy to this JobDefinition.

        :param strategy: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed331e31805cc6f7683fd89242513783324ed363049fb885a482d6c6b067e61a)
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
        return typing.cast(None, jsii.invoke(self, "addRetryStrategy", [strategy]))

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> EksContainerDefinition:
        '''(experimental) The container this Job Definition will run.

        :stability: experimental
        '''
        return typing.cast(EksContainerDefinition, jsii.get(self, "container"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionArn"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of this job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionName"))

    @builtins.property
    @jsii.member(jsii_name="retryStrategies")
    def retry_strategies(self) -> typing.List[RetryStrategy]:
        '''(experimental) Defines the retry behavior for this job.

        :stability: experimental
        '''
        return typing.cast(typing.List[RetryStrategy], jsii.get(self, "retryStrategies"))

    @builtins.property
    @jsii.member(jsii_name="dnsPolicy")
    def dns_policy(self) -> typing.Optional[DnsPolicy]:
        '''(experimental) The DNS Policy of the pod used by this Job Definition.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[DnsPolicy], jsii.get(self, "dnsPolicy"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) The default parameters passed to the container These parameters can be referenced in the ``command`` that you give to the container.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="retryAttempts")
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to retry a job.

        The job is retried on failure the same number of attempts as the value.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retryAttempts"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPriority")
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of this Job.

        Only used in Fairshare Scheduling
        to decide which job to run first when there are multiple jobs
        with the same share identifier.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulingPriority"))

    @builtins.property
    @jsii.member(jsii_name="serviceAccount")
    def service_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the service account that's used to run the container.

        service accounts are Kubernetes method of identification and authentication,
        roughly analogous to IAM users.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceAccount"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes,
        Batch terminates your jobs if they aren't finished.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="useHostNetwork")
    def use_host_network(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If specified, the Pod used by this Job Definition will use the host's network IP address.

        Otherwise, the Kubernetes pod networking model is enabled.
        Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "useHostNetwork"))


@jsii.implements(IFairshareSchedulingPolicy, ISchedulingPolicy)
class FairshareSchedulingPolicy(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.FairshareSchedulingPolicy",
):
    '''(experimental) Represents a Fairshare Scheduling Policy. Instructs the scheduler to allocate ComputeEnvironment vCPUs based on Job shareIdentifiers.

    The Faireshare Scheduling Policy ensures that each share gets a certain amount of vCPUs.
    The scheduler does this by deciding how many Jobs of each share to schedule *relative to how many jobs of
    each share are currently being executed by the ComputeEnvironment*. The weight factors associated with
    each share determine the ratio of vCPUs allocated; see the readme for a more in-depth discussion of
    fairshare policies.

    :stability: experimental
    :resource: AWS::Batch::SchedulingPolicy
    :exampleMetadata: infused

    Example::

        fairshare_policy = batch.FairshareSchedulingPolicy(self, "myFairsharePolicy")
        
        fairshare_policy.add_share(
            share_identifier="A",
            weight_factor=1
        )
        fairshare_policy.add_share(
            share_identifier="B",
            weight_factor=1
        )
        batch.JobQueue(self, "JobQueue",
            scheduling_policy=fairshare_policy
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_reservation: typing.Optional[jsii.Number] = None,
        scheduling_policy_name: typing.Optional[builtins.str] = None,
        share_decay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        shares: typing.Optional[typing.Sequence[typing.Union[Share, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_reservation: (experimental) Used to calculate the percentage of the maximum available vCPU to reserve for share identifiers not present in the Queue. The percentage reserved is defined by the Scheduler as: ``(computeReservation/100)^ActiveFairShares`` where ``ActiveFairShares`` is the number of active fair share identifiers. For example, a computeReservation value of 50 indicates that AWS Batch reserves 50% of the maximum available vCPU if there's only one fair share identifier. It reserves 25% if there are two fair share identifiers. It reserves 12.5% if there are three fair share identifiers. A computeReservation value of 25 indicates that AWS Batch should reserve 25% of the maximum available vCPU if there's only one fair share identifier, 6.25% if there are two fair share identifiers, and 1.56% if there are three fair share identifiers. Default: - no vCPU is reserved
        :param scheduling_policy_name: (experimental) The name of this SchedulingPolicy. Default: - generated by CloudFormation
        :param share_decay: (experimental) The amount of time to use to measure the usage of each job. The usage is used to calculate a fair share percentage for each fair share identifier currently in the Queue. A value of zero (0) indicates that only current usage is measured. The decay is linear and gives preference to newer jobs. The maximum supported value is 604800 seconds (1 week). Default: - 0: only the current job usage is considered
        :param shares: (experimental) The shares that this Scheduling Policy applies to. *Note*: It is possible to submit Jobs to the queue with Share Identifiers that are not recognized by the Scheduling Policy. Default: - no shares

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86358ba5df7d22debd5ee041209ddc99bd9e671db20109d5f71ab65cde00dc57)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FairshareSchedulingPolicyProps(
            compute_reservation=compute_reservation,
            scheduling_policy_name=scheduling_policy_name,
            share_decay=share_decay,
            shares=shares,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFairshareSchedulingPolicyArn")
    @builtins.classmethod
    def from_fairshare_scheduling_policy_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        fairshare_scheduling_policy_arn: builtins.str,
    ) -> IFairshareSchedulingPolicy:
        '''(experimental) Reference an exisiting Scheduling Policy by its ARN.

        :param scope: -
        :param id: -
        :param fairshare_scheduling_policy_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29408cb4065574cf5a5ce4e53a16db8172d5f035cb8ab10fbd858d81ca58e86b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument fairshare_scheduling_policy_arn", value=fairshare_scheduling_policy_arn, expected_type=type_hints["fairshare_scheduling_policy_arn"])
        return typing.cast(IFairshareSchedulingPolicy, jsii.sinvoke(cls, "fromFairshareSchedulingPolicyArn", [scope, id, fairshare_scheduling_policy_arn]))

    @jsii.member(jsii_name="addShare")
    def add_share(
        self,
        *,
        share_identifier: builtins.str,
        weight_factor: jsii.Number,
    ) -> None:
        '''(experimental) Add a share this to this Fairshare SchedulingPolicy.

        :param share_identifier: (experimental) The identifier of this Share. All jobs that specify this share identifier when submitted to the queue will be considered as part of this Share.
        :param weight_factor: (experimental) The weight factor given to this Share. The Scheduler decides which jobs to put in the Compute Environment such that the following ratio is equal for each job: ``sharevCpu / weightFactor``, where ``sharevCpu`` is the total amount of vCPU given to that particular share; that is, the sum of the vCPU of each job currently in the Compute Environment for that share. See the readme of this module for a detailed example that shows how these are used, how it relates to ``computeReservation``, and how ``shareDecay`` affects these calculations.

        :stability: experimental
        '''
        share = Share(share_identifier=share_identifier, weight_factor=weight_factor)

        return typing.cast(None, jsii.invoke(self, "addShare", [share]))

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyArn")
    def scheduling_policy_arn(self) -> builtins.str:
        '''(experimental) The arn of this scheduling policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "schedulingPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyName")
    def scheduling_policy_name(self) -> builtins.str:
        '''(experimental) The name of this scheduling policy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "schedulingPolicyName"))

    @builtins.property
    @jsii.member(jsii_name="shares")
    def shares(self) -> typing.List[Share]:
        '''(experimental) The shares that this Scheduling Policy applies to.

        *Note*: It is possible to submit Jobs to the queue with Share Identifiers that
        are not recognized by the Scheduling Policy.

        :stability: experimental
        '''
        return typing.cast(typing.List[Share], jsii.get(self, "shares"))

    @builtins.property
    @jsii.member(jsii_name="computeReservation")
    def compute_reservation(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Used to calculate the percentage of the maximum available vCPU to reserve for share identifiers not present in the Queue.

        The percentage reserved is defined by the Scheduler as:
        ``(computeReservation/100)^ActiveFairShares`` where ``ActiveFairShares`` is the number of active fair share identifiers.

        For example, a computeReservation value of 50 indicates that AWS Batch reserves 50% of the
        maximum available vCPU if there's only one fair share identifier.
        It reserves 25% if there are two fair share identifiers.
        It reserves 12.5% if there are three fair share identifiers.

        A computeReservation value of 25 indicates that AWS Batch should reserve 25% of the
        maximum available vCPU if there's only one fair share identifier,
        6.25% if there are two fair share identifiers,
        and 1.56% if there are three fair share identifiers.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "computeReservation"))

    @builtins.property
    @jsii.member(jsii_name="shareDecay")
    def share_decay(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) The amount of time to use to measure the usage of each job.

        The usage is used to calculate a fair share percentage for each fair share identifier currently in the Queue.
        A value of zero (0) indicates that only current usage is measured.
        The decay is linear and gives preference to newer jobs.

        The maximum supported value is 604800 seconds (1 week).

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "shareDecay"))


@jsii.implements(IFargateComputeEnvironment, IManagedComputeEnvironment, IComputeEnvironment)
class FargateComputeEnvironment(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch-alpha.FargateComputeEnvironment",
):
    '''(experimental) A ManagedComputeEnvironment that uses ECS orchestration on Fargate instances.

    :stability: experimental
    :resource: AWS::Batch::ComputeEnvironment
    :exampleMetadata: infused

    Example::

        # vpc: ec2.IVpc
        
        shared_compute_env = batch.FargateComputeEnvironment(self, "spotEnv",
            vpc=vpc,
            spot=True
        )
        low_priority_queue = batch.JobQueue(self, "JobQueue",
            priority=1
        )
        high_priority_queue = batch.JobQueue(self, "JobQueue",
            priority=10
        )
        low_priority_queue.add_compute_environment(shared_compute_env, 1)
        high_priority_queue.add_compute_environment(shared_compute_env, 1)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        replace_compute_environment: typing.Optional[builtins.bool] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        spot: typing.Optional[builtins.bool] = None,
        terminate_on_update: typing.Optional[builtins.bool] = None,
        update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        update_to_latest_image_version: typing.Optional[builtins.bool] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        compute_environment_name: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: (experimental) VPC in which this Compute Environment will launch Instances.
        :param maxv_cpus: (experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to. Each vCPU is equivalent to 1024 CPU shares. *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances, The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes`` or ``instanceClasses``. Default: 256
        :param replace_compute_environment: (experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances. To enable more properties to be updated, set this property to ``false``. When changing the value of this property to false, do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state. You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. The properties which require a replacement of the Compute Environment are: Default: false
        :param security_groups: (experimental) The security groups this Compute Environment will launch instances in. Default: new security groups will be created
        :param spot: (experimental) Whether or not to use spot instances. Spot instances are less expensive EC2 instances that can be reclaimed by EC2 at any time; your job will be given two minutes of notice before reclamation. Default: false
        :param terminate_on_update: (experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs. If this is enabled, any terminated jobs may be retried, depending on the job's retry policy. Default: false
        :param update_timeout: (experimental) Only meaningful if ``terminateOnUpdate`` is ``false``. If so, when an infrastructure update is triggered, any running jobs will be allowed to run until ``updateTimeout`` has expired. Default: 30 minutes
        :param update_to_latest_image_version: (experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs. If you specify a specific AMI, this property will be ignored. Default: true
        :param vpc_subnets: (experimental) The VPC Subnets this Compute Environment will launch instances in. Default: new subnets will be created
        :param compute_environment_name: (experimental) The name of the ComputeEnvironment. Default: - generated by CloudFormation
        :param enabled: (experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue. Enabled ComputeEnvironments can accept jobs from a Queue and can scale instances up or down. Disabled ComputeEnvironments cannot accept jobs from a Queue or scale instances up or down. If you change a ComputeEnvironment from enabled to disabled while it is executing jobs, Jobs in the ``STARTED`` or ``RUNNING`` states will not be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``. To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``. Default: true
        :param service_role: (experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs. Default: - a serviceRole will be created for managed CEs, none for unmanaged CEs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e14c2a9aebce75c09dc576034fca5ed07c42c9827167d48f90b9dd534f102e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FargateComputeEnvironmentProps(
            vpc=vpc,
            maxv_cpus=maxv_cpus,
            replace_compute_environment=replace_compute_environment,
            security_groups=security_groups,
            spot=spot,
            terminate_on_update=terminate_on_update,
            update_timeout=update_timeout,
            update_to_latest_image_version=update_to_latest_image_version,
            vpc_subnets=vpc_subnets,
            compute_environment_name=compute_environment_name,
            enabled=enabled,
            service_role=service_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFargateComputeEnvironmentArn")
    @builtins.classmethod
    def from_fargate_compute_environment_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        fargate_compute_environment_arn: builtins.str,
    ) -> IFargateComputeEnvironment:
        '''(experimental) Reference an existing FargateComputeEnvironment by its arn.

        :param scope: -
        :param id: -
        :param fargate_compute_environment_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e1bb24b95e79c6527e243b143c630cf022d067308d7cb3418bb7dc13f26244)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument fargate_compute_environment_arn", value=fargate_compute_environment_arn, expected_type=type_hints["fargate_compute_environment_arn"])
        return typing.cast(IFargateComputeEnvironment, jsii.sinvoke(cls, "fromFargateComputeEnvironmentArn", [scope, id, fargate_compute_environment_arn]))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentArn")
    def compute_environment_arn(self) -> builtins.str:
        '''(experimental) The ARN of this compute environment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> builtins.str:
        '''(experimental) The name of the ComputeEnvironment.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _aws_cdk_aws_ec2_ceddda9d.Connections:
        '''(experimental) The network connections associated with this resource.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_aws_ec2_ceddda9d.Connections, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> builtins.bool:
        '''(experimental) Whether or not this ComputeEnvironment can accept jobs from a Queue.

        Enabled ComputeEnvironments can accept jobs from a Queue and
        can scale instances up or down.
        Disabled ComputeEnvironments cannot accept jobs from a Queue or
        scale instances up or down.

        If you change a ComputeEnvironment from enabled to disabled while it is executing jobs,
        Jobs in the ``STARTED`` or ``RUNNING`` states will not
        be interrupted. As jobs complete, the ComputeEnvironment will scale instances down to ``minvCpus``.

        To ensure you aren't billed for unused capacity, set ``minvCpus`` to ``0``.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "enabled"))

    @builtins.property
    @jsii.member(jsii_name="maxvCpus")
    def maxv_cpus(self) -> jsii.Number:
        '''(experimental) The maximum vCpus this ``ManagedComputeEnvironment`` can scale up to.

        *Note*: if this Compute Environment uses EC2 resources (not Fargate) with either ``AllocationStrategy.BEST_FIT_PROGRESSIVE`` or
        ``AllocationStrategy.SPOT_CAPACITY_OPTIMIZED``, or ``AllocationStrategy.BEST_FIT`` with Spot instances,
        The scheduler may exceed this number by at most one of the instances specified in ``instanceTypes``
        or ``instanceClasses``.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "maxvCpus"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]:
        '''(experimental) The security groups this Compute Environment will launch instances in.

        :stability: experimental
        '''
        return typing.cast(typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_ceddda9d.TagManager:
        '''(experimental) TagManager to set, remove and format tags.

        :stability: experimental
        '''
        return typing.cast(_aws_cdk_ceddda9d.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="replaceComputeEnvironment")
    def replace_compute_environment(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether this Compute Environment is replaced if an update is made that requires replacing its instances.

        To enable more properties to be updated,
        set this property to ``false``. When changing the value of this property to false,
        do not change any other properties at the same time.
        If other properties are changed at the same time,
        and the change needs to be rolled back but it can't,
        it's possible for the stack to go into the UPDATE_ROLLBACK_FAILED state.
        You can't update a stack that is in the UPDATE_ROLLBACK_FAILED state.
        However, if you can continue to roll it back,
        you can return the stack to its original settings and then try to update it again.

        The properties which require a replacement of the Compute Environment are:

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "replaceComputeEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The role Batch uses to perform actions on your behalf in your account, such as provision instances to run your jobs.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], jsii.get(self, "serviceRole"))

    @builtins.property
    @jsii.member(jsii_name="spot")
    def spot(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to use spot instances.

        Spot instances are less expensive EC2 instances that can be
        reclaimed by EC2 at any time; your job will be given two minutes
        of notice before reclamation.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "spot"))

    @builtins.property
    @jsii.member(jsii_name="terminateOnUpdate")
    def terminate_on_update(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not any running jobs will be immediately terminated when an infrastructure update occurs.

        If this is enabled, any terminated jobs may be retried, depending on the job's
        retry policy.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "terminateOnUpdate"))

    @builtins.property
    @jsii.member(jsii_name="updateTimeout")
    def update_timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(experimental) Only meaningful if ``terminateOnUpdate`` is ``false``.

        If so,
        when an infrastructure update is triggered, any running jobs
        will be allowed to run until ``updateTimeout`` has expired.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "updateTimeout"))

    @builtins.property
    @jsii.member(jsii_name="updateToLatestImageVersion")
    def update_to_latest_image_version(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not the AMI is updated to the latest one supported by Batch when an infrastructure update occurs.

        If you specify a specific AMI, this property will be ignored.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.bool], jsii.get(self, "updateToLatestImageVersion"))


__all__ = [
    "Action",
    "AllocationStrategy",
    "ComputeEnvironmentProps",
    "CustomReason",
    "Device",
    "DevicePermission",
    "DnsPolicy",
    "EcsContainerDefinitionProps",
    "EcsEc2ContainerDefinition",
    "EcsEc2ContainerDefinitionProps",
    "EcsFargateContainerDefinition",
    "EcsFargateContainerDefinitionProps",
    "EcsJobDefinition",
    "EcsJobDefinitionProps",
    "EcsMachineImage",
    "EcsMachineImageType",
    "EcsVolume",
    "EcsVolumeOptions",
    "EfsVolume",
    "EfsVolumeOptions",
    "EksContainerDefinition",
    "EksContainerDefinitionProps",
    "EksJobDefinition",
    "EksJobDefinitionProps",
    "EksMachineImage",
    "EksMachineImageType",
    "EksVolume",
    "EksVolumeOptions",
    "EmptyDirMediumType",
    "EmptyDirVolume",
    "EmptyDirVolumeOptions",
    "FairshareSchedulingPolicy",
    "FairshareSchedulingPolicyProps",
    "FargateComputeEnvironment",
    "FargateComputeEnvironmentProps",
    "HostPathVolume",
    "HostPathVolumeOptions",
    "HostVolume",
    "HostVolumeOptions",
    "IComputeEnvironment",
    "IEcsContainerDefinition",
    "IEcsEc2ContainerDefinition",
    "IEcsFargateContainerDefinition",
    "IEksContainerDefinition",
    "IEksJobDefinition",
    "IFairshareSchedulingPolicy",
    "IFargateComputeEnvironment",
    "IJobDefinition",
    "IJobQueue",
    "IManagedComputeEnvironment",
    "IManagedEc2EcsComputeEnvironment",
    "ISchedulingPolicy",
    "IUnmanagedComputeEnvironment",
    "ImagePullPolicy",
    "JobDefinitionProps",
    "JobQueue",
    "JobQueueProps",
    "LinuxParameters",
    "LinuxParametersProps",
    "ManagedComputeEnvironmentProps",
    "ManagedEc2EcsComputeEnvironment",
    "ManagedEc2EcsComputeEnvironmentProps",
    "ManagedEc2EksComputeEnvironment",
    "ManagedEc2EksComputeEnvironmentProps",
    "MultiNodeContainer",
    "MultiNodeJobDefinition",
    "MultiNodeJobDefinitionProps",
    "OrderedComputeEnvironment",
    "Reason",
    "RetryStrategy",
    "Secret",
    "SecretPathVolume",
    "SecretPathVolumeOptions",
    "SecretVersionInfo",
    "Share",
    "Tmpfs",
    "TmpfsMountOption",
    "Ulimit",
    "UlimitName",
    "UnmanagedComputeEnvironment",
    "UnmanagedComputeEnvironmentProps",
]

publication.publish()

def _typecheckingstub__d827f561c1e2643ccfedecf52d55816f36a64383c9490ba8339fdd4f4723a97c(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34a1b2439a15559af9fb419414f098bca7f859cce42e28628fa89a3fbd48fa5b(
    *,
    on_exit_code: typing.Optional[builtins.str] = None,
    on_reason: typing.Optional[builtins.str] = None,
    on_status_reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81e8e75a9432ab711a80858f17b1795231ea3916d8259c9a5b95d91b3411217(
    *,
    host_path: builtins.str,
    container_path: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Sequence[DevicePermission]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ce2351c7933476492b6019bf0c8b32e1ca81b2717193b3c66c4c10c9c5544e(
    *,
    cpu: jsii.Number,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    memory: _aws_cdk_ceddda9d.Size,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    linux_parameters: typing.Optional[LinuxParameters] = None,
    logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    user: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69b95619d0ef073cf4a12636fc9060fc5c6b021c6fb057e989657c2fda7ec1f3(
    *,
    cpu: jsii.Number,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    memory: _aws_cdk_ceddda9d.Size,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    linux_parameters: typing.Optional[LinuxParameters] = None,
    logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    user: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
    gpu: typing.Optional[jsii.Number] = None,
    privileged: typing.Optional[builtins.bool] = None,
    ulimits: typing.Optional[typing.Sequence[typing.Union[Ulimit, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be426e0524ddb478956358b5434c99110733179aba3a389f8413804be7910e5f(
    *,
    cpu: jsii.Number,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    memory: _aws_cdk_ceddda9d.Size,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    linux_parameters: typing.Optional[LinuxParameters] = None,
    logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    user: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    fargate_platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37d05bed1d068747e454278ee23635b90274054dd119a14ca87ecd86b87fbcb7(
    *,
    image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    image_type: typing.Optional[EcsMachineImageType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fd9bd77e01b20e461eaba782d1cbae004ef85d44e3c0078ed6702ded4e4da8(
    *,
    container_path: builtins.str,
    name: builtins.str,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7c12ad3e540e49a03aad69b7d890b94cca310d933180c6f73bccbbd1509fffc(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dba797b8199f276971c1302f225db8c50004625e7296aefe6f59eb993ad3784(
    *,
    container_path: builtins.str,
    name: builtins.str,
    readonly: typing.Optional[builtins.bool] = None,
    file_system: _aws_cdk_aws_efs_ceddda9d.IFileSystem,
    access_point_id: typing.Optional[builtins.str] = None,
    enable_transit_encryption: typing.Optional[builtins.bool] = None,
    root_directory: typing.Optional[builtins.str] = None,
    transit_encryption_port: typing.Optional[jsii.Number] = None,
    use_job_role: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53410c93d882935ca1283d4cc21ef161d31335c97183c177d91ee29a54213aa(
    *,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu_limit: typing.Optional[jsii.Number] = None,
    cpu_reservation: typing.Optional[jsii.Number] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    gpu_limit: typing.Optional[jsii.Number] = None,
    gpu_reservation: typing.Optional[jsii.Number] = None,
    image_pull_policy: typing.Optional[ImagePullPolicy] = None,
    memory_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    memory_reservation: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    name: typing.Optional[builtins.str] = None,
    privileged: typing.Optional[builtins.bool] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    run_as_group: typing.Optional[jsii.Number] = None,
    run_as_root: typing.Optional[builtins.bool] = None,
    run_as_user: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Sequence[EksVolume]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__217985092c1dc6208d9a3e5925aa7eef933f9d780c17b631d53280fad572ecd5(
    *,
    image: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IMachineImage] = None,
    image_type: typing.Optional[EksMachineImageType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79d1e28c8c37196461f6b4f63eef2cd8dff26b0545ab1962d0367ee18b09dd42(
    *,
    name: builtins.str,
    mount_path: typing.Optional[builtins.str] = None,
    readonly: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61e4a4c5b13ccdd73d22eef16c5f25f0360005b334cbe7762bfae453bc1a14d5(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87b0da6c75ed058ff623aebcb883b8e2b3ec50d159a4b2f052c643873ed08f2(
    *,
    name: builtins.str,
    mount_path: typing.Optional[builtins.str] = None,
    readonly: typing.Optional[builtins.bool] = None,
    medium: typing.Optional[EmptyDirMediumType] = None,
    size_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ce1917e4f041cad0e9f935e693fee4450e8cf33f9a703df7ae1ed6aba5e4046(
    *,
    compute_reservation: typing.Optional[jsii.Number] = None,
    scheduling_policy_name: typing.Optional[builtins.str] = None,
    share_decay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    shares: typing.Optional[typing.Sequence[typing.Union[Share, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0fe123d5409e9e44652333f1dca6e60d125b36cf2343f8a86721cd66de4dc2(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f8d5c089c2fc4d5e83ef7c0147c81ab62b6f89571ecbdba336189a07a601b2(
    *,
    name: builtins.str,
    mount_path: typing.Optional[builtins.str] = None,
    readonly: typing.Optional[builtins.bool] = None,
    host_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7afaf677383998a2af7586ef0bd46764cb4ab6f8eb0e0559bf181485514b63a(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49269c9b7b771ac8a3b0c8c0320d0b98fd9d95fad759832648b74d993a22ecd9(
    *,
    container_path: builtins.str,
    name: builtins.str,
    readonly: typing.Optional[builtins.bool] = None,
    host_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23d7381af0c45284e0879a7629848fc4de2d3901ba78f741661211bc62d9316c(
    volume: EcsVolume,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d27eac738541f17e8629ff3d1cc312de8b73bc0f3d2f69a01613e321f0180a2(
    volume: EksVolume,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334a109994c2c6dac94c2aeaf63b80742ab7e39597ca35cd656e28c702af44c2(
    strategy: RetryStrategy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff1947820a24bcf175625e5097d37007f089af82dc7c2a7b5b2fb7ff68bf271(
    compute_environment: IComputeEnvironment,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387f2e9251b506a8dfd9ff3e858b74a8cb740b78008ea64c6da21917b9d825d8(
    instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a3ed0d94894cdb085f842a16aaefb3d6a0289bb3d3b50151249f5a01aa9d3e(
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185df21ce496b49d7787089d80d45a0314ac702fd8d9d2f9ba4a623921534158(
    *,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48859d154c5df5d7c73c0dfbc7a6690f4c823f76e3ac97ea0a3302eb0eebbdcd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_environments: typing.Optional[typing.Sequence[typing.Union[OrderedComputeEnvironment, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    job_queue_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    scheduling_policy: typing.Optional[ISchedulingPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a0f379bd1cdd0d274ec73314e99f3a3964c617458143876c623482b8065bde(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    job_queue_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9cf974ef884ccf8550be3abbd8e5e805f821c2808c4d17b3c76d4617398d053(
    compute_environment: IComputeEnvironment,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb77dbf4c08c80e90ddc79e26e0ff4218db45852e16cc5250c15de7d3041d3bf(
    *,
    compute_environments: typing.Optional[typing.Sequence[typing.Union[OrderedComputeEnvironment, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    job_queue_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    scheduling_policy: typing.Optional[ISchedulingPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa1843a39cb26bea1804dabeb0330c79b6698e9cf52250cd4b3492c5b3e4dfc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    init_process_enabled: typing.Optional[builtins.bool] = None,
    max_swap: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    shared_memory_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    swappiness: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c96c9da432c3bb02107313dc0610d870117421ad312e09371274d5672f2c736(
    *device: Device,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6a261a81aa3b99900849aa34269258580c84910ad287d5c3f29a9d8b18b8d79(
    *tmpfs: Tmpfs,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7520d82136e04b588afff3e9af7597b6b89fc591c1861bd204d203d4d07823f7(
    *,
    init_process_enabled: typing.Optional[builtins.bool] = None,
    max_swap: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    shared_memory_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    swappiness: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__185ace7c9ac3fc3c89503d419f45772a577131204fd52b9fd049cd3aff542fd8(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ecd7c9bbba4d9e441a13ce54d8df8673c886cac2f04a4fc28344c39c2efb9d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    allocation_strategy: typing.Optional[AllocationStrategy] = None,
    images: typing.Optional[typing.Sequence[typing.Union[EcsMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
    launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
    spot_bid_percentage: typing.Optional[jsii.Number] = None,
    spot_fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae86bff947bdb5fa9c0b6f95425875a909080e2645a02dbd4672a7846b669398(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    managed_ec2_ecs_compute_environment_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4154c464d82dcda19d60e2a16fbcfc483e094fa18217992c523b2b4a4ce49bc6(
    instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__171399bef64d69b36e805fd95356d1f14d7d16814d59dea069290961da787252(
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80804fff92abbb5cf4045718bdc81911bb4157bf5a171323aa7780cf0a60ab4d(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    allocation_strategy: typing.Optional[AllocationStrategy] = None,
    images: typing.Optional[typing.Sequence[typing.Union[EcsMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
    launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
    spot_bid_percentage: typing.Optional[jsii.Number] = None,
    spot_fleet_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ea4c86fae84c6f923bd126a2028d7db5eafaa0e2097047cba9c9aeb90eb98a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    eks_cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
    kubernetes_namespace: builtins.str,
    allocation_strategy: typing.Optional[AllocationStrategy] = None,
    images: typing.Optional[typing.Sequence[typing.Union[EksMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
    launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
    spot_bid_percentage: typing.Optional[jsii.Number] = None,
    use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a3443238d0f0e49d52ab4a6908cebaa74e2926338df9811a0765b4c5a6d9e71(
    instance_class: _aws_cdk_aws_ec2_ceddda9d.InstanceClass,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db374276009006a09b5e278249c46716cd0ad60f136c2d8935f32d132fe35747(
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e42d86a173146d27c5c384f1a29007831c1dca632c1e2c34c274f79f70392e(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    eks_cluster: _aws_cdk_aws_eks_ceddda9d.ICluster,
    kubernetes_namespace: builtins.str,
    allocation_strategy: typing.Optional[AllocationStrategy] = None,
    images: typing.Optional[typing.Sequence[typing.Union[EksMachineImage, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_classes: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceClass]] = None,
    instance_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.InstanceType]] = None,
    launch_template: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.ILaunchTemplate] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[_aws_cdk_aws_ec2_ceddda9d.IPlacementGroup] = None,
    spot_bid_percentage: typing.Optional[jsii.Number] = None,
    use_optimal_instance_classes: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c91062f1c8fc62f406ccbd11a0ac92eabc52ba7ff035a069bf920e09a854535d(
    *,
    container: IEcsContainerDefinition,
    end_node: jsii.Number,
    start_node: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139b4216a5dd7f555b1ab73bb5cea84db509a956ce81cf54bffc204e58736e03(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    containers: typing.Optional[typing.Sequence[typing.Union[MultiNodeContainer, typing.Dict[builtins.str, typing.Any]]]] = None,
    main_node: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17613a34df9a93ba88b486af78c4e07c2c4fe2f08a80569f2e45e0d4b5856d38(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    job_definition_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fba5f22c63c67900e0f92f211bd72c8dab50e7dd1665f4c69ca32da27ad93a(
    strategy: RetryStrategy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a47285cdbc48884b55ec85b3762923ac73e4c2727c95d4878276c2f187f22ec(
    *,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    instance_type: _aws_cdk_aws_ec2_ceddda9d.InstanceType,
    containers: typing.Optional[typing.Sequence[typing.Union[MultiNodeContainer, typing.Dict[builtins.str, typing.Any]]]] = None,
    main_node: typing.Optional[jsii.Number] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e89685caa52c73ced10db3d7e3342c85bc760d13702b6c1b1b6518bb92cb6da(
    *,
    compute_environment: IComputeEnvironment,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93a3cf6384cd52d885e05decbc453270afadf73350fe3fbabfe999eb000ac3af(
    action: Action,
    on: Reason,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbd2a86a39e9602a1980340842fa5279880b52eb427c00e2482eca862804d6e1(
    action: Action,
    on: Reason,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417b5bb542000b74f11d2e41b2540a20c4c11f654f8fc91dee7ffaddf9d6d998(
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154b84f590a02078c55967f577cea92eab82265b65e02a4a494b9f1640c2c0cd(
    secret: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    version_info: typing.Union[SecretVersionInfo, typing.Dict[builtins.str, typing.Any]],
    field: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148d662618bb349676015375138c4ecfa0be439a0b516966013300b96f13b203(
    parameter: _aws_cdk_aws_ssm_ceddda9d.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1dccacde9286de58cba92280e0cdf531ae9d73f821080448b72c71ef3e76e4b(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3a03ecb4d2c7970b919f329ea0a70b0d6d566612846e7310ce39a70b2d28cc8(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6846c94bd19e040b25e2c723ce4e85c8433155366f549c39673137f848bbeabf(
    *,
    name: builtins.str,
    mount_path: typing.Optional[builtins.str] = None,
    readonly: typing.Optional[builtins.bool] = None,
    secret_name: builtins.str,
    optional: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b741a8b4f55c3924a86f27640b2c2804411ad62a1fbd1989efe7d927f71f51e8(
    *,
    version_id: typing.Optional[builtins.str] = None,
    version_stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f49c5ab573b4bfa5d0896d9a64df348a858dcad66800c2ee4b18d7c9689127d(
    *,
    share_identifier: builtins.str,
    weight_factor: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae43135e0b7885bb5ad0c6b0f141663feb55023972c81196445d6320485e9b9e(
    *,
    container_path: builtins.str,
    size: _aws_cdk_ceddda9d.Size,
    mount_options: typing.Optional[typing.Sequence[TmpfsMountOption]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3a813e84c137117f83dbb8d34d6118680453895d16f2b159105d0d16200cf0(
    *,
    hard_limit: jsii.Number,
    name: UlimitName,
    soft_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8ec1668bdd84e9da8d4f3138d52ee48dcc98eb518f59434abdd9d08eb77c71(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    unmanagedv_cpus: typing.Optional[jsii.Number] = None,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04975c179a3ca1bd144e178327353a7b0ad4551c5fbcbec77f85adb60dd52c3f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    unmanaged_compute_environment_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ff6bd98bd0c62bbea69e5a54f99c879fca8729e2ba319baba6a241cfd016386(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    unmanagedv_cpus: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__703337fcfe6e1c52132bd99ed93a15029f92d7846e2d4ce71fd4fe473a99b3ec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    gpu: typing.Optional[jsii.Number] = None,
    privileged: typing.Optional[builtins.bool] = None,
    ulimits: typing.Optional[typing.Sequence[typing.Union[Ulimit, typing.Dict[builtins.str, typing.Any]]]] = None,
    cpu: jsii.Number,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    memory: _aws_cdk_ceddda9d.Size,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    linux_parameters: typing.Optional[LinuxParameters] = None,
    logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    user: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee557c571178dc5154d52600836940cca88204ce5a09d4644c49746ad660498b(
    volume: EcsVolume,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9043358a0ec27fcc739211bbd1e2d8ba93a21bd15df808d7f8d3ccd8380718a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    ephemeral_storage_size: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    fargate_platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
    cpu: jsii.Number,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    memory: _aws_cdk_ceddda9d.Size,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    job_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    linux_parameters: typing.Optional[LinuxParameters] = None,
    logging: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.LogDriver] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    secrets: typing.Optional[typing.Mapping[builtins.str, Secret]] = None,
    user: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Sequence[EcsVolume]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bc155ea09c4fdbae8e8ba2169b1dad78f860c6fe7189a54c9b4705abda28be(
    volume: EcsVolume,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d22fe551a7ec9dc3ab5dca1924a9459f34e7c4a858584cd7f476997617a7257f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    container: IEcsContainerDefinition,
    propagate_tags: typing.Optional[builtins.bool] = None,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab639941f3154616eec16a5022b72152eb79cf04c72b8b8e12ce55072631cf45(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    job_definition_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a94917adb1283e62eedbe5223f4a93a91485e876d85dcbcc25496d14009867e7(
    strategy: RetryStrategy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029b7552867bfe3ab6c1c2c24488738b70372469bb39e29a696bc8b1f2cc20cc(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    queue: IJobQueue,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3422a4d894c1df05100df13e7a265d056c4ea6456cfc0b39da47fd91e557c54b(
    *,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    container: IEcsContainerDefinition,
    propagate_tags: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa55a51376bba78f2a58e4b4a9b815797d08470292f55790f7760ca8960c8117(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    image: _aws_cdk_aws_ecs_ceddda9d.ContainerImage,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    cpu_limit: typing.Optional[jsii.Number] = None,
    cpu_reservation: typing.Optional[jsii.Number] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    gpu_limit: typing.Optional[jsii.Number] = None,
    gpu_reservation: typing.Optional[jsii.Number] = None,
    image_pull_policy: typing.Optional[ImagePullPolicy] = None,
    memory_limit: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    memory_reservation: typing.Optional[_aws_cdk_ceddda9d.Size] = None,
    name: typing.Optional[builtins.str] = None,
    privileged: typing.Optional[builtins.bool] = None,
    readonly_root_filesystem: typing.Optional[builtins.bool] = None,
    run_as_group: typing.Optional[jsii.Number] = None,
    run_as_root: typing.Optional[builtins.bool] = None,
    run_as_user: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Sequence[EksVolume]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f08fa019f05afced1d0b0b9ae2f275b52da9043803f2ae598f3771a9435ad8b3(
    volume: EksVolume,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b77d33798657223ab8a68e0a96698e9f50b309f5eea8bc7599133c6945dc82(
    *,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    container: EksContainerDefinition,
    dns_policy: typing.Optional[DnsPolicy] = None,
    service_account: typing.Optional[builtins.str] = None,
    use_host_network: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90829606627d5bace90cbad01656e3373471c075f52752633c48258b671deb61(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__493040c2c7ee40246c6a072e076284b76f124d7e7aaaa01e929e603e0120ce38(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    container: EksContainerDefinition,
    dns_policy: typing.Optional[DnsPolicy] = None,
    service_account: typing.Optional[builtins.str] = None,
    use_host_network: typing.Optional[builtins.bool] = None,
    job_definition_name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    retry_strategies: typing.Optional[typing.Sequence[RetryStrategy]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402960107d8c9231c93870e789ccea7b4935615a9f98366ceffb6f7117ffb401(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    eks_job_definition_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed331e31805cc6f7683fd89242513783324ed363049fb885a482d6c6b067e61a(
    strategy: RetryStrategy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86358ba5df7d22debd5ee041209ddc99bd9e671db20109d5f71ab65cde00dc57(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_reservation: typing.Optional[jsii.Number] = None,
    scheduling_policy_name: typing.Optional[builtins.str] = None,
    share_decay: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    shares: typing.Optional[typing.Sequence[typing.Union[Share, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29408cb4065574cf5a5ce4e53a16db8172d5f035cb8ab10fbd858d81ca58e86b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    fairshare_scheduling_policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e14c2a9aebce75c09dc576034fca5ed07c42c9827167d48f90b9dd534f102e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_ceddda9d.IVpc,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    replace_compute_environment: typing.Optional[builtins.bool] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    spot: typing.Optional[builtins.bool] = None,
    terminate_on_update: typing.Optional[builtins.bool] = None,
    update_timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    update_to_latest_image_version: typing.Optional[builtins.bool] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    compute_environment_name: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e1bb24b95e79c6527e243b143c630cf022d067308d7cb3418bb7dc13f26244(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    fargate_compute_environment_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
