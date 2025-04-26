'''
# AWS Batch Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

AWS Batch is a batch processing tool for efficiently running hundreds of thousands computing jobs in AWS. Batch can dynamically provision different types of compute resources based on the resource requirements of submitted jobs.

AWS Batch simplifies the planning, scheduling, and executions of your batch workloads across a full range of compute services like [Amazon EC2](https://aws.amazon.com/ec2/) and [Spot Resources](https://aws.amazon.com/ec2/spot/).

Batch achieves this by utilizing queue processing of batch job requests. To successfully submit a job for execution, you need the following resources:

1. [Job Definition](#job-definition) - *Group various job properties (container image, resource requirements, env variables...) into a single definition. These definitions are used at job submission time.*
2. [Compute Environment](#compute-environment) - *the execution runtime of submitted batch jobs*
3. [Job Queue](#job-queue) - *the queue where batch jobs can be submitted to via AWS SDK/CLI*

For more information on **AWS Batch** visit the [AWS Docs for Batch](https://docs.aws.amazon.com/batch/index.html).

## Compute Environment

At the core of AWS Batch is the compute environment. All batch jobs are processed within a compute environment, which uses resource like OnDemand/Spot EC2 instances or Fargate.

In **MANAGED** mode, AWS will handle the provisioning of compute resources to accommodate the demand. Otherwise, in **UNMANAGED** mode, you will need to manage the provisioning of those resources.

Below is an example of each available type of compute environment:

```python
# vpc: ec2.Vpc


# default is managed
aws_managed_environment = batch.ComputeEnvironment(self, "AWS-Managed-Compute-Env",
    compute_resources=batch.ComputeResources(
        vpc=vpc
    )
)

customer_managed_environment = batch.ComputeEnvironment(self, "Customer-Managed-Compute-Env",
    managed=False
)
```

### Spot-Based Compute Environment

It is possible to have AWS Batch submit spotfleet requests for obtaining compute resources. Below is an example of how this can be done:

```python
vpc = ec2.Vpc(self, "VPC")

spot_environment = batch.ComputeEnvironment(self, "MySpotEnvironment",
    compute_resources=batch.ComputeResources(
        type=batch.ComputeResourceType.SPOT,
        bid_percentage=75,  # Bids for resources at 75% of the on-demand price
        vpc=vpc
    )
)
```

### Fargate Compute Environment

It is possible to have AWS Batch submit jobs to be run on Fargate compute resources. Below is an example of how this can be done:

```python
vpc = ec2.Vpc(self, "VPC")

fargate_spot_environment = batch.ComputeEnvironment(self, "MyFargateEnvironment",
    compute_resources=batch.ComputeResources(
        type=batch.ComputeResourceType.FARGATE_SPOT,
        vpc=vpc
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

### Launch template support

Simply define your Launch Template:

```text
// This example is only available in TypeScript
const myLaunchTemplate = new ec2.CfnLaunchTemplate(this, 'LaunchTemplate', {
  launchTemplateName: 'extra-storage-template',
  launchTemplateData: {
    blockDeviceMappings: [
      {
        deviceName: '/dev/xvdcz',
        ebs: {
          encrypted: true,
          volumeSize: 100,
          volumeType: 'gp2',
        },
      },
    ],
  },
});
```

and use it:

```python
# vpc: ec2.Vpc
# my_launch_template: ec2.CfnLaunchTemplate


my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources=batch.ComputeResources(
        launch_template=batch.LaunchTemplateSpecification(
            launch_template_name=my_launch_template.launch_template_name
        ),
        vpc=vpc
    ),
    compute_environment_name="MyStorageCapableComputeEnvironment"
)
```

### Importing an existing Compute Environment

To import an existing batch compute environment, call `ComputeEnvironment.fromComputeEnvironmentArn()`.

Below is an example:

```python
compute_env = batch.ComputeEnvironment.from_compute_environment_arn(self, "imported-compute-env", "arn:aws:batch:us-east-1:555555555555:compute-environment/My-Compute-Env")
```

### Change the baseline AMI of the compute resources

Occasionally, you will need to deviate from the default processing AMI.

ECS Optimized Amazon Linux 2 example:

```python
# vpc: ec2.Vpc

my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources=batch.ComputeResources(
        image=ecs.EcsOptimizedAmi(
            generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
        ),
        vpc=vpc
    )
)
```

Custom based AMI example:

```python
# vpc: ec2.Vpc

my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
    compute_resources=batch.ComputeResources(
        image=ec2.MachineImage.generic_linux({
            "[aws-region]": "[ami-ID]"
        }),
        vpc=vpc
    )
)
```

## Job Queue

Jobs are always submitted to a specific queue. This means that you have to create a queue before you can start submitting jobs. Each queue is mapped to at least one (and no more than three) compute environment. When the job is scheduled for execution, AWS Batch will select the compute environment based on ordinal priority and available capacity in each environment.

```python
# compute_environment: batch.ComputeEnvironment

job_queue = batch.JobQueue(self, "JobQueue",
    compute_environments=[batch.JobQueueComputeEnvironment(
        # Defines a collection of compute resources to handle assigned batch jobs
        compute_environment=compute_environment,
        # Order determines the allocation order for jobs (i.e. Lower means higher preference for job assignment)
        order=1
    )
    ]
)
```

### Priorty-Based Queue Example

Sometimes you might have jobs that are more important than others, and when submitted, should take precedence over the existing jobs. To achieve this, you can create a priority based execution strategy, by assigning each queue its own priority:

```python
# shared_compute_envs: batch.ComputeEnvironment

high_prio_queue = batch.JobQueue(self, "JobQueue",
    compute_environments=[batch.JobQueueComputeEnvironment(
        compute_environment=shared_compute_envs,
        order=1
    )],
    priority=2
)

low_prio_queue = batch.JobQueue(self, "JobQueue",
    compute_environments=[batch.JobQueueComputeEnvironment(
        compute_environment=shared_compute_envs,
        order=1
    )],
    priority=1
)
```

By making sure to use the same compute environments between both job queues, we will give precedence to the `highPrioQueue` for the assigning of jobs to available compute environments.

### Importing an existing Job Queue

To import an existing batch job queue, call `JobQueue.fromJobQueueArn()`.

Below is an example:

```python
job_queue = batch.JobQueue.from_job_queue_arn(self, "imported-job-queue", "arn:aws:batch:us-east-1:555555555555:job-queue/High-Prio-Queue")
```

## Job Definition

A Batch Job definition helps AWS Batch understand important details about how to run your application in the scope of a Batch Job. This involves key information like resource requirements, what containers to run, how the compute environment should be prepared, and more. Below is a simple example of how to create a job definition:

```python
import aws_cdk.aws_ecr as ecr


repo = ecr.Repository.from_repository_name(self, "batch-job-repo", "todo-list")

batch.JobDefinition(self, "batch-job-def-from-ecr",
    container=batch.JobDefinitionContainer(
        image=ecs.EcrImage(repo, "latest")
    )
)
```

### Using a local Docker project

Below is an example of how you can create a Batch Job Definition from a local Docker application.

```python
batch.JobDefinition(self, "batch-job-def-from-local",
    container=batch.JobDefinitionContainer(
        # todo-list is a directory containing a Dockerfile to build the application
        image=ecs.ContainerImage.from_asset("../todo-list")
    )
)
```

### Providing custom log configuration

You can provide custom log driver and its configuration for the container.

```python
import aws_cdk.aws_ssm as ssm


batch.JobDefinition(self, "job-def",
    container=batch.JobDefinitionContainer(
        image=ecs.EcrImage.from_registry("docker/whalesay"),
        log_configuration=batch.LogConfiguration(
            log_driver=batch.LogDriver.AWSLOGS,
            options={"awslogs-region": "us-east-1"},
            secret_options=[
                batch.ExposedSecret.from_parameters_store("xyz", ssm.StringParameter.from_string_parameter_name(self, "parameter", "xyz"))
            ]
        )
    )
)
```

### Importing an existing Job Definition

#### From ARN

To import an existing batch job definition from its ARN, call `JobDefinition.fromJobDefinitionArn()`.

Below is an example:

```python
job = batch.JobDefinition.from_job_definition_arn(self, "imported-job-definition", "arn:aws:batch:us-east-1:555555555555:job-definition/my-job-definition")
```

#### From Name

To import an existing batch job definition from its name, call `JobDefinition.fromJobDefinitionName()`.
If name is specified without a revision then the latest active revision is used.

Below is an example:

```python
# Without revision
job1 = batch.JobDefinition.from_job_definition_name(self, "imported-job-definition", "my-job-definition")

# With revision
job2 = batch.JobDefinition.from_job_definition_name(self, "imported-job-definition", "my-job-definition:3")
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

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_7896c08f
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_72af8d6f
import aws_cdk.aws_ssm as _aws_cdk_aws_ssm_1e9d799e
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.enum(jsii_type="@aws-cdk/aws-batch.AllocationStrategy")
class AllocationStrategy(enum.Enum):
    '''(experimental) Properties for how to prepare compute resources that are provisioned for a compute environment.

    :stability: experimental
    '''

    BEST_FIT = "BEST_FIT"
    '''(experimental) Batch will use the best fitting instance type will be used when assigning a batch job in this compute environment.

    :stability: experimental
    '''
    BEST_FIT_PROGRESSIVE = "BEST_FIT_PROGRESSIVE"
    '''(experimental) Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU.

    :stability: experimental
    '''
    SPOT_CAPACITY_OPTIMIZED = "SPOT_CAPACITY_OPTIMIZED"
    '''(experimental) This is only available for Spot Instance compute resources and will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted.

    :stability: experimental
    '''


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnComputeEnvironment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment",
):
    '''A CloudFormation ``AWS::Batch::ComputeEnvironment``.

    The ``AWS::Batch::ComputeEnvironment`` resource defines your AWS Batch compute environment. You can define ``MANAGED`` or ``UNMANAGED`` compute environments. ``MANAGED`` compute environments can use Amazon EC2 or AWS Fargate resources. ``UNMANAGED`` compute environments can only use EC2 resources. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .

    In a managed compute environment, AWS Batch manages the capacity and instance types of the compute resources within the environment. This is based on the compute resource specification that you define or the `launch template <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html>`_ that you specify when you create the compute environment. You can choose either to use EC2 On-Demand Instances and EC2 Spot Instances, or to use Fargate and Fargate Spot capacity in your managed compute environment. You can optionally set a maximum price so that Spot Instances only launch when the Spot Instance price is below a specified percentage of the On-Demand price.
    .. epigraph::

       Multi-node parallel jobs are not supported on Spot Instances.

    In an unmanaged compute environment, you can manage your own EC2 compute resources and have a lot of flexibility with how you configure your compute resources. For example, you can use custom AMI. However, you need to verify that your AMI meets the Amazon ECS container instance AMI specification. For more information, see `container instance AMIs <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container_instance_AMIs.html>`_ in the *Amazon Elastic Container Service Developer Guide* . After you have created your unmanaged compute environment, you can use the `DescribeComputeEnvironments <https://docs.aws.amazon.com/batch/latest/APIReference/API_DescribeComputeEnvironments.html>`_ operation to find the Amazon ECS cluster that is associated with it. Then, manually launch your container instances into that Amazon ECS cluster. For more information, see `Launching an Amazon ECS container instance <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/launch_container_instance.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
    .. epigraph::

       To create a compute environment that uses EKS resources, the caller must have permissions to call ``eks:DescribeCluster`` . > AWS Batch doesn't upgrade the AMIs in a compute environment after it's created except under specific conditions. For example, it doesn't automatically update the AMIs when a newer version of the Amazon ECS optimized AMI is available. Therefore, you're responsible for the management of the guest operating system (including updates and security patches) and any additional application software or utilities that you install on the compute resources. There are two ways to use a new AMI for your AWS Batch jobs. The original method is to complete these steps:

       - Create a new compute environment with the new AMI.
       - Add the compute environment to an existing job queue.
       - Remove the earlier compute environment from your job queue.
       - Delete the earlier compute environment.

       In April 2022, AWS Batch added enhanced support for updating compute environments. For example, the ``UpdateComputeEnvironent`` API lets you use the ``ReplaceComputeEnvironment`` property to dynamically update compute environment parameters such as the launch template or instance type without replacement. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

       To use the enhanced updating of compute environments to update AMIs, follow these rules:

       - Either do not set the `ServiceRole <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole>`_ property or set it to the *AWSServiceRoleForBatch* service-linked role.
       - Set the `AllocationStrategy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ property to ``BEST_FIT_PROGRESSIVE`` or ``SPOT_CAPACITY_OPTIMIZED`` .
       - Set the `ReplaceComputeEnvironment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-replacecomputeenvironment>`_ property to ``false`` .

       .. epigraph::

          Set the ``ReplaceComputeEnvironment`` property to ``false`` if the compute environment uses the ``BEST_FIT`` allocation strategy. > If the ``ReplaceComputeEnvironment`` property is set to ``false`` , you might receive an error message when you update the CFN template for a compute environment. This issue occurs if the updated ``desiredvcpus`` value is less than the current ``desiredvcpus`` value. As a workaround, delete the ``desiredvcpus`` value from the updated template or use the ``minvcpus`` property to manage the number of vCPUs. For information, see `Error message when you update the ``DesiredvCpus`` setting <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#error-desired-vcpus-update>`_ .

       - Set the `UpdateToLatestImageVersion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ property to ``true`` . This property is used when you update a compute environment. The `UpdateToLatestImageVersion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ property is ignored when you create a compute environment.
       - Either do not specify an image ID in `ImageId <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ or `ImageIdOverride <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imageidoverride>`_ properties, or in the launch template identified by the `Launch Template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ property. In that case AWS Batch will select the latest Amazon ECS optimized AMI supported by AWS Batch at the time the infrastructure update is initiated. Alternatively you can specify the AMI ID in the ``ImageId`` or ``ImageIdOverride`` properties, or the launch template identified by the ``LaunchTemplate`` properties. Changing any of these properties will trigger an infrastructure update.

       If these rules are followed, any update that triggers an infrastructure update will cause the AMI ID to be re-selected. If the `Version <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-version>`_ property of the `LaunchTemplateSpecification <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html>`_ is set to ``$Latest`` or ``$Default`` , the latest or default version of the launch template will be evaluated up at the time of the infrastructure update, even if the ``LaunchTemplateSpecification`` was not updated.

    :cloudformationResource: AWS::Batch::ComputeEnvironment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch as batch
        
        cfn_compute_environment = batch.CfnComputeEnvironment(self, "MyCfnComputeEnvironment",
            type="type",
        
            # the properties below are optional
            compute_environment_name="computeEnvironmentName",
            compute_resources=batch.CfnComputeEnvironment.ComputeResourcesProperty(
                maxv_cpus=123,
                subnets=["subnets"],
                type="type",
        
                # the properties below are optional
                allocation_strategy="allocationStrategy",
                bid_percentage=123,
                desiredv_cpus=123,
                ec2_configuration=[batch.CfnComputeEnvironment.Ec2ConfigurationObjectProperty(
                    image_type="imageType",
        
                    # the properties below are optional
                    image_id_override="imageIdOverride",
                    image_kubernetes_version="imageKubernetesVersion"
                )],
                ec2_key_pair="ec2KeyPair",
                image_id="imageId",
                instance_role="instanceRole",
                instance_types=["instanceTypes"],
                launch_template=batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    version="version"
                ),
                minv_cpus=123,
                placement_group="placementGroup",
                security_group_ids=["securityGroupIds"],
                spot_iam_fleet_role="spotIamFleetRole",
                tags={
                    "tags_key": "tags"
                },
                update_to_latest_image_version=False
            ),
            eks_configuration=batch.CfnComputeEnvironment.EksConfigurationProperty(
                eks_cluster_arn="eksClusterArn",
                kubernetes_namespace="kubernetesNamespace"
            ),
            replace_compute_environment=False,
            service_role="serviceRole",
            state="state",
            tags={
                "tags_key": "tags"
            },
            unmanagedv_cpus=123,
            update_policy=batch.CfnComputeEnvironment.UpdatePolicyProperty(
                job_execution_timeout_minutes=123,
                terminate_jobs_on_update=False
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        type: builtins.str,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union[typing.Union["CfnComputeEnvironment.ComputeResourcesProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        eks_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComputeEnvironment.EksConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        replace_compute_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        service_role: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        unmanagedv_cpus: typing.Optional[jsii.Number] = None,
        update_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComputeEnvironment.UpdatePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Batch::ComputeEnvironment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: The type of the compute environment: ``MANAGED`` or ``UNMANAGED`` . For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .
        :param compute_environment_name: The name for your compute environment. It can be up to 128 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param compute_resources: The ComputeResources property type specifies details of the compute resources managed by the compute environment. This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .
        :param eks_configuration: The details for the Amazon EKS cluster that supports the compute environment.
        :param replace_compute_environment: Specifies whether the compute environment is replaced if an update is made that requires replacing the instances in the compute environment. The default value is ``true`` . To enable more properties to be updated, set this property to ``false`` . When changing the value of this property to ``false`` , do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the ``UPDATE_ROLLBACK_FAILED`` state. You can't update a stack that is in the ``UPDATE_ROLLBACK_FAILED`` state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. For more information, see `Continue rolling back an update <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html>`_ in the *AWS CloudFormation User Guide* . The properties that can't be changed without replacing the compute environment are in the ```ComputeResources`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html>`_ property type: ```AllocationStrategy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ , ```BidPercentage`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage>`_ , ```Ec2Configuration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```ImageId`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ , ```InstanceRole`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole>`_ , ```InstanceTypes`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes>`_ , ```LaunchTemplate`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ , ```MaxvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus>`_ , ```MinvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus>`_ , ```PlacementGroup`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup>`_ , ```SecurityGroupIds`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids>`_ , ```Subnets`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets>`_ , `Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags>`_ , ```Type`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type>`_ , and ```UpdateToLatestImageVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ .
        :param service_role: The full Amazon Resource Name (ARN) of the IAM role that allows AWS Batch to make calls to other AWS services on your behalf. For more information, see `AWS Batch service IAM role <https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html>`_ in the *AWS Batch User Guide* . .. epigraph:: If your account already created the AWS Batch service-linked role, that role is used by default for your compute environment unless you specify a different role here. If the AWS Batch service-linked role doesn't exist in your account, and no role is specified here, the service attempts to create the AWS Batch service-linked role in your account. If your specified role has a path other than ``/`` , then you must specify either the full role ARN (recommended) or prefix the role name with the path. For example, if a role with the name ``bar`` has a path of ``/foo/`` , specify ``/foo/bar`` as the role name. For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* . .. epigraph:: Depending on how you created your AWS Batch service role, its ARN might contain the ``service-role`` path prefix. When you only specify the name of the service role, AWS Batch assumes that your ARN doesn't use the ``service-role`` path prefix. Because of this, we recommend that you specify the full ARN of your service role when you create compute environments.
        :param state: The state of the compute environment. If the state is ``ENABLED`` , then the compute environment accepts jobs from a queue and can scale out automatically based on queues. If the state is ``ENABLED`` , then the AWS Batch scheduler can attempt to place jobs from an associated job queue on the compute resources within the environment. If the compute environment is managed, then it can scale its instances out or in automatically, based on the job queue demand. If the state is ``DISABLED`` , then the AWS Batch scheduler doesn't attempt to place jobs within the environment. Jobs in a ``STARTING`` or ``RUNNING`` state continue to progress normally. Managed compute environments in the ``DISABLED`` state don't scale out. .. epigraph:: Compute environments in a ``DISABLED`` state may continue to incur billing charges. To prevent additional charges, turn off and then delete the compute environment. For more information, see `State <https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html#compute_environment_state>`_ in the *AWS Batch User Guide* . When an instance is idle, the instance scales down to the ``minvCpus`` value. However, the instance size doesn't change. For example, consider a ``c5.8xlarge`` instance with a ``minvCpus`` value of ``4`` and a ``desiredvCpus`` value of ``36`` . This instance doesn't scale down to a ``c5.large`` instance.
        :param tags: The tags applied to the compute environment.
        :param unmanagedv_cpus: The maximum number of vCPUs for an unmanaged compute environment. This parameter is only used for fair share scheduling to reserve vCPU capacity for new share identifiers. If this parameter isn't provided for a fair share job queue, no vCPU capacity is reserved. .. epigraph:: This parameter is only supported when the ``type`` parameter is set to ``UNMANAGED`` .
        :param update_policy: Specifies the infrastructure update policy for the compute environment. For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2cbf692bbd14fb1bd48d457b8474146c99da23d24f5a1cc3dac848f9787b8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnComputeEnvironmentProps(
            type=type,
            compute_environment_name=compute_environment_name,
            compute_resources=compute_resources,
            eks_configuration=eks_configuration,
            replace_compute_environment=replace_compute_environment,
            service_role=service_role,
            state=state,
            tags=tags,
            unmanagedv_cpus=unmanagedv_cpus,
            update_policy=update_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd974725cb49c9198b63049aeb87de5804a7ab99d9894cf93d84ad1c0767238)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d2e0b0511cbf14c7e45ca90e00b700eb3bd8367007555ed2b4545bac6315ccd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrComputeEnvironmentArn")
    def attr_compute_environment_arn(self) -> builtins.str:
        '''Returns the compute environment ARN, such as ``batch: *us-east-1* : *111122223333* :compute-environment/ *ComputeEnvironmentName*`` .

        :cloudformationAttribute: ComputeEnvironmentArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrComputeEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags applied to the compute environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the compute environment: ``MANAGED`` or ``UNMANAGED`` .

        For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b60d178d17433dacbd973f4a52d87d5b724639882d584c63260fe7cd2a1c1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentName")
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''The name for your compute environment.

        It can be up to 128 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computeEnvironmentName"))

    @compute_environment_name.setter
    def compute_environment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b59c000947b3ca506f2753af800b18959bdd14f83cd8ec8fe42a5c2b68fee9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentName", value)

    @builtins.property
    @jsii.member(jsii_name="computeResources")
    def compute_resources(
        self,
    ) -> typing.Optional[typing.Union["CfnComputeEnvironment.ComputeResourcesProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The ComputeResources property type specifies details of the compute resources managed by the compute environment.

        This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        '''
        return typing.cast(typing.Optional[typing.Union["CfnComputeEnvironment.ComputeResourcesProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "computeResources"))

    @compute_resources.setter
    def compute_resources(
        self,
        value: typing.Optional[typing.Union["CfnComputeEnvironment.ComputeResourcesProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8168068cfbbef0a4b43390a3a6e230b3cbea310ee59afb681e4465aed9eabea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeResources", value)

    @builtins.property
    @jsii.member(jsii_name="eksConfiguration")
    def eks_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.EksConfigurationProperty"]]:
        '''The details for the Amazon EKS cluster that supports the compute environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-eksconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.EksConfigurationProperty"]], jsii.get(self, "eksConfiguration"))

    @eks_configuration.setter
    def eks_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.EksConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b8a811119a9bc2a47bb57e7b87f12807667d14844ddcbaa64b977914a8b2ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="replaceComputeEnvironment")
    def replace_compute_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the compute environment is replaced if an update is made that requires replacing the instances in the compute environment.

        The default value is ``true`` . To enable more properties to be updated, set this property to ``false`` . When changing the value of this property to ``false`` , do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the ``UPDATE_ROLLBACK_FAILED`` state. You can't update a stack that is in the ``UPDATE_ROLLBACK_FAILED`` state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. For more information, see `Continue rolling back an update <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html>`_ in the *AWS CloudFormation User Guide* .

        The properties that can't be changed without replacing the compute environment are in the ```ComputeResources`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html>`_ property type: ```AllocationStrategy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ , ```BidPercentage`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage>`_ , ```Ec2Configuration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```ImageId`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ , ```InstanceRole`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole>`_ , ```InstanceTypes`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes>`_ , ```LaunchTemplate`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ , ```MaxvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus>`_ , ```MinvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus>`_ , ```PlacementGroup`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup>`_ , ```SecurityGroupIds`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids>`_ , ```Subnets`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets>`_ , `Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags>`_ , ```Type`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type>`_ , and ```UpdateToLatestImageVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-replacecomputeenvironment
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "replaceComputeEnvironment"))

    @replace_compute_environment.setter
    def replace_compute_environment(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19948d8357991cc3039673852ff520831c4a6b397cbee41699d9ffba81463151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replaceComputeEnvironment", value)

    @builtins.property
    @jsii.member(jsii_name="serviceRole")
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The full Amazon Resource Name (ARN) of the IAM role that allows AWS Batch to make calls to other AWS services on your behalf.

        For more information, see `AWS Batch service IAM role <https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html>`_ in the *AWS Batch User Guide* .
        .. epigraph::

           If your account already created the AWS Batch service-linked role, that role is used by default for your compute environment unless you specify a different role here. If the AWS Batch service-linked role doesn't exist in your account, and no role is specified here, the service attempts to create the AWS Batch service-linked role in your account.

        If your specified role has a path other than ``/`` , then you must specify either the full role ARN (recommended) or prefix the role name with the path. For example, if a role with the name ``bar`` has a path of ``/foo/`` , specify ``/foo/bar`` as the role name. For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* .
        .. epigraph::

           Depending on how you created your AWS Batch service role, its ARN might contain the ``service-role`` path prefix. When you only specify the name of the service role, AWS Batch assumes that your ARN doesn't use the ``service-role`` path prefix. Because of this, we recommend that you specify the full ARN of your service role when you create compute environments.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRole"))

    @service_role.setter
    def service_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2b2600d383f72b2ef58c9f3a532a74d0fde77403f873923cb9ddbd4b3b217c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRole", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the compute environment.

        If the state is ``ENABLED`` , then the compute environment accepts jobs from a queue and can scale out automatically based on queues.

        If the state is ``ENABLED`` , then the AWS Batch scheduler can attempt to place jobs from an associated job queue on the compute resources within the environment. If the compute environment is managed, then it can scale its instances out or in automatically, based on the job queue demand.

        If the state is ``DISABLED`` , then the AWS Batch scheduler doesn't attempt to place jobs within the environment. Jobs in a ``STARTING`` or ``RUNNING`` state continue to progress normally. Managed compute environments in the ``DISABLED`` state don't scale out.
        .. epigraph::

           Compute environments in a ``DISABLED`` state may continue to incur billing charges. To prevent additional charges, turn off and then delete the compute environment. For more information, see `State <https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html#compute_environment_state>`_ in the *AWS Batch User Guide* .

        When an instance is idle, the instance scales down to the ``minvCpus`` value. However, the instance size doesn't change. For example, consider a ``c5.8xlarge`` instance with a ``minvCpus`` value of ``4`` and a ``desiredvCpus`` value of ``36`` . This instance doesn't scale down to a ``c5.large`` instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e41aa9107af2cab70ae1955cb7f76fc2c055e39c29573e227b21359c63a5f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @builtins.property
    @jsii.member(jsii_name="unmanagedvCpus")
    def unmanagedv_cpus(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of vCPUs for an unmanaged compute environment.

        This parameter is only used for fair share scheduling to reserve vCPU capacity for new share identifiers. If this parameter isn't provided for a fair share job queue, no vCPU capacity is reserved.
        .. epigraph::

           This parameter is only supported when the ``type`` parameter is set to ``UNMANAGED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-unmanagedvcpus
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "unmanagedvCpus"))

    @unmanagedv_cpus.setter
    def unmanagedv_cpus(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811decbaf1eb9a8f02657685e6247a7f53a70c8379d47ecbdc670a1fc577b347)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unmanagedvCpus", value)

    @builtins.property
    @jsii.member(jsii_name="updatePolicy")
    def update_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.UpdatePolicyProperty"]]:
        '''Specifies the infrastructure update policy for the compute environment.

        For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-updatepolicy
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.UpdatePolicyProperty"]], jsii.get(self, "updatePolicy"))

    @update_policy.setter
    def update_policy(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.UpdatePolicyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4782916fb7fd0274a3412ccf21812e95b96a5ebc03d67359ef15eb3d86690480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "updatePolicy", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.ComputeResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "maxv_cpus": "maxvCpus",
            "subnets": "subnets",
            "type": "type",
            "allocation_strategy": "allocationStrategy",
            "bid_percentage": "bidPercentage",
            "desiredv_cpus": "desiredvCpus",
            "ec2_configuration": "ec2Configuration",
            "ec2_key_pair": "ec2KeyPair",
            "image_id": "imageId",
            "instance_role": "instanceRole",
            "instance_types": "instanceTypes",
            "launch_template": "launchTemplate",
            "minv_cpus": "minvCpus",
            "placement_group": "placementGroup",
            "security_group_ids": "securityGroupIds",
            "spot_iam_fleet_role": "spotIamFleetRole",
            "tags": "tags",
            "update_to_latest_image_version": "updateToLatestImageVersion",
        },
    )
    class ComputeResourcesProperty:
        def __init__(
            self,
            *,
            maxv_cpus: jsii.Number,
            subnets: typing.Sequence[builtins.str],
            type: builtins.str,
            allocation_strategy: typing.Optional[builtins.str] = None,
            bid_percentage: typing.Optional[jsii.Number] = None,
            desiredv_cpus: typing.Optional[jsii.Number] = None,
            ec2_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComputeEnvironment.Ec2ConfigurationObjectProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ec2_key_pair: typing.Optional[builtins.str] = None,
            image_id: typing.Optional[builtins.str] = None,
            instance_role: typing.Optional[builtins.str] = None,
            instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            launch_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnComputeEnvironment.LaunchTemplateSpecificationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            minv_cpus: typing.Optional[jsii.Number] = None,
            placement_group: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            spot_iam_fleet_role: typing.Optional[builtins.str] = None,
            tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            update_to_latest_image_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Details about the compute resources managed by the compute environment.

            This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

            :param maxv_cpus: The maximum number of Amazon EC2 vCPUs that an environment can reach. .. epigraph:: With both ``BEST_FIT_PROGRESSIVE`` and ``SPOT_CAPACITY_OPTIMIZED`` allocation strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to exceed ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance. That is, no more than a single instance from among those specified in your compute environment.
            :param subnets: The VPC subnets where the compute resources are launched. Fargate compute resources can contain up to 16 subnets. For Fargate compute resources, providing an empty list will be handled as if this parameter wasn't specified and no change is made. For EC2 compute resources, providing an empty list removes the VPC subnets from the compute resource. For more information, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* . When updating a compute environment, changing the VPC subnets requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: AWS Batch on Amazon EC2 and AWS Batch on Amazon EKS support Local Zones. For more information, see `Local Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones>`_ in the *Amazon EC2 User Guide for Linux Instances* , `Amazon EKS and AWS Local Zones <https://docs.aws.amazon.com/eks/latest/userguide/local-zones.html>`_ in the *Amazon EKS User Guide* and `Amazon ECS clusters in Local Zones, Wavelength Zones, and AWS Outposts <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-regions-zones.html#clusters-local-zones>`_ in the *Amazon ECS Developer Guide* . AWS Batch on Fargate doesn't currently support Local Zones.
            :param type: The type of compute environment: ``EC2`` , ``SPOT`` , ``FARGATE`` , or ``FARGATE_SPOT`` . For more information, see `Compute environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* . If you choose ``SPOT`` , you must also specify an Amazon EC2 Spot Fleet role with the ``spotIamFleetRole`` parameter. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* . When updating compute environment, changing the type of a compute environment requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . When updating the type of a compute environment, changing between ``EC2`` and ``SPOT`` or between ``FARGATE`` and ``FARGATE_SPOT`` will initiate an infrastructure update, but if you switch between ``EC2`` and ``FARGATE`` , AWS CloudFormation will create a new compute environment.
            :param allocation_strategy: The allocation strategy to use for the compute resource if not enough instances of the best fitting instance type can be allocated. This might be because of availability of the instance type in the Region or `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ . For more information, see `Allocation strategies <https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html>`_ in the *AWS Batch User Guide* . When updating a compute environment, changing the allocation strategy requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . ``BEST_FIT`` is not supported when updating a compute environment. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources, and shouldn't be specified. - **BEST_FIT (default)** - AWS Batch selects an instance type that best fits the needs of the jobs with a preference for the lowest-cost instance type. If additional instances of the selected instance type aren't available, AWS Batch waits for the additional instances to be available. If there aren't enough instances available, or if the user is reaching `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ then additional jobs aren't run until the currently running jobs have completed. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with ``BEST_FIT`` then the Spot Fleet IAM role must be specified. - **BEST_FIT_PROGRESSIVE** - AWS Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU. If additional instances of the previously selected instance types aren't available, AWS Batch will select new instance types. - **SPOT_CAPACITY_OPTIMIZED** - AWS Batch will select one or more instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted. This allocation strategy is only available for Spot Instance compute resources. With both ``BEST_FIT_PROGRESSIVE`` and ``SPOT_CAPACITY_OPTIMIZED`` allocation strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to go above ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance.
            :param bid_percentage: The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Amazon EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. For most use cases, we recommend leaving this field empty. When updating a compute environment, changing the bid percentage requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param desiredv_cpus: The desired number of vCPUS in the compute environment. AWS Batch modifies this value between the minimum and maximum values based on job queue demand. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > AWS Batch doesn't support changing the desired number of vCPUs of an existing compute environment. Don't specify this parameter for compute environments using Amazon EKS clusters. > When you update the ``desiredvCpus`` setting, the value must be between the ``minvCpus`` and ``maxvCpus`` values. Additionally, the updated ``desiredvCpus`` value must be greater than or equal to the current ``desiredvCpus`` value. For more information, see `Troubleshooting AWS Batch <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#error-desired-vcpus-update>`_ in the *AWS Batch User Guide* .
            :param ec2_configuration: Provides information used to select Amazon Machine Images (AMIs) for EC2 instances in the compute environment. If ``Ec2Configuration`` isn't specified, the default is ``ECS_AL2`` . When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . To remove the EC2 configuration and any custom AMI ID specified in ``imageIdOverride`` , set this value to an empty string. One or two values can be provided. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param ec2_key_pair: The Amazon EC2 key pair that's used for instances launched in the compute environment. You can use this key pair to log in to your instances with SSH. To remove the Amazon EC2 key pair, set this value to an empty string. When updating a compute environment, changing the EC2 key pair requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param image_id: The Amazon Machine Image (AMI) ID used for instances launched in the compute environment. This parameter is overridden by the ``imageIdOverride`` member of the ``Ec2Configuration`` structure. To remove the custom AMI ID and use the default AMI ID, set this value to an empty string. When updating a compute environment, changing the AMI ID requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param instance_role: The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment. You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ``*ecsInstanceRole*`` or ``arn:aws:iam:: *<aws_account_id>* :instance-profile/ *ecsInstanceRole*`` . For more information, see `Amazon ECS instance role <https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html>`_ in the *AWS Batch User Guide* . When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param instance_types: The instances types that can be launched. You can specify instance families to launch any instance type within those families (for example, ``c5`` or ``p3`` ), or you can specify specific sizes within a family (such as ``c5.8xlarge`` ). You can also choose ``optimal`` to select instance types (from the C4, M4, and R4 instance families) that match the demand of your job queues. When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > When you create a compute environment, the instance types that you select for the compute environment must share the same architecture. For example, you can't mix x86 and ARM instances in the same compute environment. > Currently, ``optimal`` uses instance types from the C4, M4, and R4 instance families. In Regions that don't have instance types from those instance families, instance types from the C5, M5, and R5 instance families are used.
            :param launch_template: The launch template to use for your compute resources. Any other compute resource parameters that you specify in a `CreateComputeEnvironment <https://docs.aws.amazon.com/batch/latest/APIReference/API_CreateComputeEnvironment.html>`_ API operation override the same parameters in the launch template. You must specify either the launch template ID or launch template name in the request, but not both. For more information, see `Launch Template Support <https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html>`_ in the ** . Removing the launch template from a compute environment will not remove the AMI specified in the launch template. In order to update the AMI specified in a launch template, the ``updateToLatestImageVersion`` parameter must be set to ``true`` . When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the ** . .. epigraph:: This parameter isn't applicable to jobs running on Fargate resources, and shouldn't be specified.
            :param minv_cpus: The minimum number of vCPUs that an environment should maintain (even if the compute environment is ``DISABLED`` ). .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param placement_group: The Amazon EC2 placement group to associate with your compute resources. If you intend to submit multi-node parallel jobs to your compute environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. For more information, see `Placement groups <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html>`_ in the *Amazon EC2 User Guide for Linux Instances* . When updating a compute environment, changing the placement group requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param security_group_ids: The Amazon EC2 security groups that are associated with instances launched in the compute environment. This parameter is required for Fargate compute resources, where it can contain up to 5 security groups. For Fargate compute resources, providing an empty list is handled as if this parameter wasn't specified and no change is made. For EC2 compute resources, providing an empty list removes the security groups from the compute resource. When updating a compute environment, changing the EC2 security groups requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            :param spot_iam_fleet_role: The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a ``SPOT`` compute environment. This role is required if the allocation strategy set to ``BEST_FIT`` or if the allocation strategy isn't specified. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > To tag your Spot Instances on creation, the Spot Fleet IAM role specified here must use the newer *AmazonEC2SpotFleetTaggingRole* managed policy. The previously recommended *AmazonEC2SpotFleetRole* managed policy doesn't have the required permissions to tag Spot Instances. For more information, see `Spot instances not tagged on creation <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#spot-instance-no-tag>`_ in the *AWS Batch User Guide* .
            :param tags: Key-value pair tags to be applied to EC2 resources that are launched in the compute environment. For AWS Batch , these take the form of ``"String1": "String2"`` , where ``String1`` is the tag key and ``String2`` is the tag value-for example, ``{ "Name": "Batch Instance - C4OnDemand" }`` . This is helpful for recognizing your AWS Batch instances in the Amazon EC2 console. These tags aren't seen when using the AWS Batch ``ListTagsForResource`` API operation. When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.
            :param update_to_latest_image_version: Specifies whether the AMI ID is updated to the latest one that's supported by AWS Batch when the compute environment has an infrastructure update. The default value is ``false`` . .. epigraph:: An AMI ID can either be specified in the ``imageId`` or ``imageIdOverride`` parameters or be determined by the launch template that's specified in the ``launchTemplate`` parameter. If an AMI ID is specified any of these ways, this parameter is ignored. For more information about to update AMI IDs during an infrastructure update, see `Updating the AMI ID <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html#updating-compute-environments-ami>`_ in the *AWS Batch User Guide* . When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                compute_resources_property = batch.CfnComputeEnvironment.ComputeResourcesProperty(
                    maxv_cpus=123,
                    subnets=["subnets"],
                    type="type",
                
                    # the properties below are optional
                    allocation_strategy="allocationStrategy",
                    bid_percentage=123,
                    desiredv_cpus=123,
                    ec2_configuration=[batch.CfnComputeEnvironment.Ec2ConfigurationObjectProperty(
                        image_type="imageType",
                
                        # the properties below are optional
                        image_id_override="imageIdOverride",
                        image_kubernetes_version="imageKubernetesVersion"
                    )],
                    ec2_key_pair="ec2KeyPair",
                    image_id="imageId",
                    instance_role="instanceRole",
                    instance_types=["instanceTypes"],
                    launch_template=batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        version="version"
                    ),
                    minv_cpus=123,
                    placement_group="placementGroup",
                    security_group_ids=["securityGroupIds"],
                    spot_iam_fleet_role="spotIamFleetRole",
                    tags={
                        "tags_key": "tags"
                    },
                    update_to_latest_image_version=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d52ba8fff15f28c08cee5d63b61572d65e0cbe72d0cf24f85e4e50d2a2547910)
                check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
                check_type(argname="argument subnets", value=subnets, expected_type=type_hints["subnets"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
                check_type(argname="argument bid_percentage", value=bid_percentage, expected_type=type_hints["bid_percentage"])
                check_type(argname="argument desiredv_cpus", value=desiredv_cpus, expected_type=type_hints["desiredv_cpus"])
                check_type(argname="argument ec2_configuration", value=ec2_configuration, expected_type=type_hints["ec2_configuration"])
                check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
                check_type(argname="argument image_id", value=image_id, expected_type=type_hints["image_id"])
                check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
                check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
                check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
                check_type(argname="argument minv_cpus", value=minv_cpus, expected_type=type_hints["minv_cpus"])
                check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument spot_iam_fleet_role", value=spot_iam_fleet_role, expected_type=type_hints["spot_iam_fleet_role"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
                check_type(argname="argument update_to_latest_image_version", value=update_to_latest_image_version, expected_type=type_hints["update_to_latest_image_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "maxv_cpus": maxv_cpus,
                "subnets": subnets,
                "type": type,
            }
            if allocation_strategy is not None:
                self._values["allocation_strategy"] = allocation_strategy
            if bid_percentage is not None:
                self._values["bid_percentage"] = bid_percentage
            if desiredv_cpus is not None:
                self._values["desiredv_cpus"] = desiredv_cpus
            if ec2_configuration is not None:
                self._values["ec2_configuration"] = ec2_configuration
            if ec2_key_pair is not None:
                self._values["ec2_key_pair"] = ec2_key_pair
            if image_id is not None:
                self._values["image_id"] = image_id
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
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if spot_iam_fleet_role is not None:
                self._values["spot_iam_fleet_role"] = spot_iam_fleet_role
            if tags is not None:
                self._values["tags"] = tags
            if update_to_latest_image_version is not None:
                self._values["update_to_latest_image_version"] = update_to_latest_image_version

        @builtins.property
        def maxv_cpus(self) -> jsii.Number:
            '''The maximum number of Amazon EC2 vCPUs that an environment can reach.

            .. epigraph::

               With both ``BEST_FIT_PROGRESSIVE`` and ``SPOT_CAPACITY_OPTIMIZED`` allocation strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to exceed ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance. That is, no more than a single instance from among those specified in your compute environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus
            '''
            result = self._values.get("maxv_cpus")
            assert result is not None, "Required property 'maxv_cpus' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def subnets(self) -> typing.List[builtins.str]:
            '''The VPC subnets where the compute resources are launched.

            Fargate compute resources can contain up to 16 subnets. For Fargate compute resources, providing an empty list will be handled as if this parameter wasn't specified and no change is made. For EC2 compute resources, providing an empty list removes the VPC subnets from the compute resource. For more information, see `VPCs and subnets <https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Subnets.html>`_ in the *Amazon VPC User Guide* .

            When updating a compute environment, changing the VPC subnets requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               AWS Batch on Amazon EC2 and AWS Batch on Amazon EKS support Local Zones. For more information, see `Local Zones <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html#concepts-local-zones>`_ in the *Amazon EC2 User Guide for Linux Instances* , `Amazon EKS and AWS Local Zones <https://docs.aws.amazon.com/eks/latest/userguide/local-zones.html>`_ in the *Amazon EKS User Guide* and `Amazon ECS clusters in Local Zones, Wavelength Zones, and AWS Outposts <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-regions-zones.html#clusters-local-zones>`_ in the *Amazon ECS Developer Guide* .

               AWS Batch on Fargate doesn't currently support Local Zones.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets
            '''
            result = self._values.get("subnets")
            assert result is not None, "Required property 'subnets' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of compute environment: ``EC2`` , ``SPOT`` , ``FARGATE`` , or ``FARGATE_SPOT`` .

            For more information, see `Compute environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

            If you choose ``SPOT`` , you must also specify an Amazon EC2 Spot Fleet role with the ``spotIamFleetRole`` parameter. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* .

            When updating compute environment, changing the type of a compute environment requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            When updating the type of a compute environment, changing between ``EC2`` and ``SPOT`` or between ``FARGATE`` and ``FARGATE_SPOT`` will initiate an infrastructure update, but if you switch between ``EC2`` and ``FARGATE`` , AWS CloudFormation will create a new compute environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def allocation_strategy(self) -> typing.Optional[builtins.str]:
            '''The allocation strategy to use for the compute resource if not enough instances of the best fitting instance type can be allocated.

            This might be because of availability of the instance type in the Region or `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ . For more information, see `Allocation strategies <https://docs.aws.amazon.com/batch/latest/userguide/allocation-strategies.html>`_ in the *AWS Batch User Guide* .

            When updating a compute environment, changing the allocation strategy requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . ``BEST_FIT`` is not supported when updating a compute environment.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources, and shouldn't be specified.

            - **BEST_FIT (default)** - AWS Batch selects an instance type that best fits the needs of the jobs with a preference for the lowest-cost instance type. If additional instances of the selected instance type aren't available, AWS Batch waits for the additional instances to be available. If there aren't enough instances available, or if the user is reaching `Amazon EC2 service limits <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-resource-limits.html>`_ then additional jobs aren't run until the currently running jobs have completed. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with ``BEST_FIT`` then the Spot Fleet IAM role must be specified.
            - **BEST_FIT_PROGRESSIVE** - AWS Batch will select additional instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types with a lower cost per unit vCPU. If additional instances of the previously selected instance types aren't available, AWS Batch will select new instance types.
            - **SPOT_CAPACITY_OPTIMIZED** - AWS Batch will select one or more instance types that are large enough to meet the requirements of the jobs in the queue, with a preference for instance types that are less likely to be interrupted. This allocation strategy is only available for Spot Instance compute resources.

            With both ``BEST_FIT_PROGRESSIVE`` and ``SPOT_CAPACITY_OPTIMIZED`` allocation strategies using On-Demand or Spot Instances, and the ``BEST_FIT`` strategy using Spot Instances, AWS Batch might need to go above ``maxvCpus`` to meet your capacity requirements. In this event, AWS Batch never exceeds ``maxvCpus`` by more than a single instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy
            '''
            result = self._values.get("allocation_strategy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def bid_percentage(self) -> typing.Optional[jsii.Number]:
            '''The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched.

            For example, if your maximum percentage is 20%, the Spot price must be less than 20% of the current On-Demand price for that Amazon EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. For most use cases, we recommend leaving this field empty.

            When updating a compute environment, changing the bid percentage requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage
            '''
            result = self._values.get("bid_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
            '''The desired number of vCPUS in the compute environment.

            AWS Batch modifies this value between the minimum and maximum values based on job queue demand.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > AWS Batch doesn't support changing the desired number of vCPUs of an existing compute environment. Don't specify this parameter for compute environments using Amazon EKS clusters. > When you update the ``desiredvCpus`` setting, the value must be between the ``minvCpus`` and ``maxvCpus`` values.

               Additionally, the updated ``desiredvCpus`` value must be greater than or equal to the current ``desiredvCpus`` value. For more information, see `Troubleshooting AWS Batch <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#error-desired-vcpus-update>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-desiredvcpus
            '''
            result = self._values.get("desiredv_cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def ec2_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.Ec2ConfigurationObjectProperty"]]]]:
            '''Provides information used to select Amazon Machine Images (AMIs) for EC2 instances in the compute environment.

            If ``Ec2Configuration`` isn't specified, the default is ``ECS_AL2`` .

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . To remove the EC2 configuration and any custom AMI ID specified in ``imageIdOverride`` , set this value to an empty string.

            One or two values can be provided.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration
            '''
            result = self._values.get("ec2_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.Ec2ConfigurationObjectProperty"]]]], result)

        @builtins.property
        def ec2_key_pair(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 key pair that's used for instances launched in the compute environment.

            You can use this key pair to log in to your instances with SSH. To remove the Amazon EC2 key pair, set this value to an empty string.

            When updating a compute environment, changing the EC2 key pair requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair
            '''
            result = self._values.get("ec2_key_pair")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon Machine Image (AMI) ID used for instances launched in the compute environment.

            This parameter is overridden by the ``imageIdOverride`` member of the ``Ec2Configuration`` structure. To remove the custom AMI ID and use the default AMI ID, set this value to an empty string.

            When updating a compute environment, changing the AMI ID requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid
            '''
            result = self._values.get("image_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_role(self) -> typing.Optional[builtins.str]:
            '''The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment.

            You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ``*ecsInstanceRole*`` or ``arn:aws:iam:: *<aws_account_id>* :instance-profile/ *ecsInstanceRole*`` . For more information, see `Amazon ECS instance role <https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html>`_ in the *AWS Batch User Guide* .

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole
            '''
            result = self._values.get("instance_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def instance_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The instances types that can be launched.

            You can specify instance families to launch any instance type within those families (for example, ``c5`` or ``p3`` ), or you can specify specific sizes within a family (such as ``c5.8xlarge`` ). You can also choose ``optimal`` to select instance types (from the C4, M4, and R4 instance families) that match the demand of your job queues.

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > When you create a compute environment, the instance types that you select for the compute environment must share the same architecture. For example, you can't mix x86 and ARM instances in the same compute environment. > Currently, ``optimal`` uses instance types from the C4, M4, and R4 instance families. In Regions that don't have instance types from those instance families, instance types from the C5, M5, and R5 instance families are used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes
            '''
            result = self._values.get("instance_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def launch_template(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]]:
            '''The launch template to use for your compute resources.

            Any other compute resource parameters that you specify in a `CreateComputeEnvironment <https://docs.aws.amazon.com/batch/latest/APIReference/API_CreateComputeEnvironment.html>`_ API operation override the same parameters in the launch template. You must specify either the launch template ID or launch template name in the request, but not both. For more information, see `Launch Template Support <https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html>`_ in the ** . Removing the launch template from a compute environment will not remove the AMI specified in the launch template. In order to update the AMI specified in a launch template, the ``updateToLatestImageVersion`` parameter must be set to ``true`` .

            When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the ** .
            .. epigraph::

               This parameter isn't applicable to jobs running on Fargate resources, and shouldn't be specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate
            '''
            result = self._values.get("launch_template")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnComputeEnvironment.LaunchTemplateSpecificationProperty"]], result)

        @builtins.property
        def minv_cpus(self) -> typing.Optional[jsii.Number]:
            '''The minimum number of vCPUs that an environment should maintain (even if the compute environment is ``DISABLED`` ).

            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus
            '''
            result = self._values.get("minv_cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def placement_group(self) -> typing.Optional[builtins.str]:
            '''The Amazon EC2 placement group to associate with your compute resources.

            If you intend to submit multi-node parallel jobs to your compute environment, you should consider creating a cluster placement group and associate it with your compute resources. This keeps your multi-node parallel job on a logical grouping of instances within a single Availability Zone with high network flow potential. For more information, see `Placement groups <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html>`_ in the *Amazon EC2 User Guide for Linux Instances* .

            When updating a compute environment, changing the placement group requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup
            '''
            result = self._values.get("placement_group")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon EC2 security groups that are associated with instances launched in the compute environment.

            This parameter is required for Fargate compute resources, where it can contain up to 5 security groups. For Fargate compute resources, providing an empty list is handled as if this parameter wasn't specified and no change is made. For EC2 compute resources, providing an empty list removes the security groups from the compute resource.

            When updating a compute environment, changing the EC2 security groups requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def spot_iam_fleet_role(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a ``SPOT`` compute environment.

            This role is required if the allocation strategy set to ``BEST_FIT`` or if the allocation strategy isn't specified. For more information, see `Amazon EC2 spot fleet role <https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it. > To tag your Spot Instances on creation, the Spot Fleet IAM role specified here must use the newer *AmazonEC2SpotFleetTaggingRole* managed policy. The previously recommended *AmazonEC2SpotFleetRole* managed policy doesn't have the required permissions to tag Spot Instances. For more information, see `Spot instances not tagged on creation <https://docs.aws.amazon.com/batch/latest/userguide/troubleshooting.html#spot-instance-no-tag>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-spotiamfleetrole
            '''
            result = self._values.get("spot_iam_fleet_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
            '''Key-value pair tags to be applied to EC2 resources that are launched in the compute environment.

            For AWS Batch , these take the form of ``"String1": "String2"`` , where ``String1`` is the tag key and ``String2`` is the tag value-for example, ``{ "Name": "Batch Instance - C4OnDemand" }`` . This is helpful for recognizing your AWS Batch instances in the Amazon EC2 console. These tags aren't seen when using the AWS Batch ``ListTagsForResource`` API operation.

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't specify it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

        @builtins.property
        def update_to_latest_image_version(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether the AMI ID is updated to the latest one that's supported by AWS Batch when the compute environment has an infrastructure update.

            The default value is ``false`` .
            .. epigraph::

               An AMI ID can either be specified in the ``imageId`` or ``imageIdOverride`` parameters or be determined by the launch template that's specified in the ``launchTemplate`` parameter. If an AMI ID is specified any of these ways, this parameter is ignored. For more information about to update AMI IDs during an infrastructure update, see `Updating the AMI ID <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html#updating-compute-environments-ami>`_ in the *AWS Batch User Guide* .

            When updating a compute environment, changing this setting requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion
            '''
            result = self._values.get("update_to_latest_image_version")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.Ec2ConfigurationObjectProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image_type": "imageType",
            "image_id_override": "imageIdOverride",
            "image_kubernetes_version": "imageKubernetesVersion",
        },
    )
    class Ec2ConfigurationObjectProperty:
        def __init__(
            self,
            *,
            image_type: builtins.str,
            image_id_override: typing.Optional[builtins.str] = None,
            image_kubernetes_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information used to select Amazon Machine Images (AMIs) for instances in the compute environment.

            If ``Ec2Configuration`` isn't specified, the default is ``ECS_AL2`` ( `Amazon Linux 2 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ ).
            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param image_type: The image type to match with the instance type to select an AMI. The supported values are different for ``ECS`` and ``EKS`` resources. - **ECS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ ( ``ECS_AL2`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon ECS optimized AMI for that image type that's supported by AWS Batch is used. - **ECS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ : Default for all non-GPU instance families. - **ECS_AL2_NVIDIA** - `Amazon Linux 2 (GPU) <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#gpuami>`_ : Default for all GPU instance families (for example ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types. - **ECS_AL1** - `Amazon Linux <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#alami>`_ . Amazon Linux has reached the end-of-life of standard support. For more information, see `Amazon Linux AMI <https://docs.aws.amazon.com/amazon-linux-ami/>`_ . - **EKS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon EKS-optimized Amazon Linux AMI <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ ( ``EKS_AL2`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon EKS optimized AMI for that image type that AWS Batch supports is used. - **EKS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for all non-GPU instance families. - **EKS_AL2_NVIDIA** - `Amazon Linux 2 (accelerated) <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for all GPU instance families (for example, ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types.
            :param image_id_override: The AMI ID used for instances launched in the compute environment that match the image type. This setting overrides the ``imageId`` set in the ``computeResource`` object. .. epigraph:: The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param image_kubernetes_version: The Kubernetes version for the compute environment. If you don't specify a value, the latest version that AWS Batch supports is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                ec2_configuration_object_property = batch.CfnComputeEnvironment.Ec2ConfigurationObjectProperty(
                    image_type="imageType",
                
                    # the properties below are optional
                    image_id_override="imageIdOverride",
                    image_kubernetes_version="imageKubernetesVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6335daee74ef7fe5510815efefc031b5dce197755b59328823d11a4c255d1fcc)
                check_type(argname="argument image_type", value=image_type, expected_type=type_hints["image_type"])
                check_type(argname="argument image_id_override", value=image_id_override, expected_type=type_hints["image_id_override"])
                check_type(argname="argument image_kubernetes_version", value=image_kubernetes_version, expected_type=type_hints["image_kubernetes_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "image_type": image_type,
            }
            if image_id_override is not None:
                self._values["image_id_override"] = image_id_override
            if image_kubernetes_version is not None:
                self._values["image_kubernetes_version"] = image_kubernetes_version

        @builtins.property
        def image_type(self) -> builtins.str:
            '''The image type to match with the instance type to select an AMI.

            The supported values are different for ``ECS`` and ``EKS`` resources.

            - **ECS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ ( ``ECS_AL2`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon ECS optimized AMI for that image type that's supported by AWS Batch is used.
            - **ECS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#al2ami>`_ : Default for all non-GPU instance families.
            - **ECS_AL2_NVIDIA** - `Amazon Linux 2 (GPU) <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#gpuami>`_ : Default for all GPU instance families (for example ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types.
            - **ECS_AL1** - `Amazon Linux <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#alami>`_ . Amazon Linux has reached the end-of-life of standard support. For more information, see `Amazon Linux AMI <https://docs.aws.amazon.com/amazon-linux-ami/>`_ .
            - **EKS** - If the ``imageIdOverride`` parameter isn't specified, then a recent `Amazon EKS-optimized Amazon Linux AMI <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ ( ``EKS_AL2`` ) is used. If a new image type is specified in an update, but neither an ``imageId`` nor a ``imageIdOverride`` parameter is specified, then the latest Amazon EKS optimized AMI for that image type that AWS Batch supports is used.
            - **EKS_AL2** - `Amazon Linux 2 <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for all non-GPU instance families.
            - **EKS_AL2_NVIDIA** - `Amazon Linux 2 (accelerated) <https://docs.aws.amazon.com/eks/latest/userguide/eks-optimized-ami.html>`_ : Default for all GPU instance families (for example, ``P4`` and ``G4`` ) and can be used for all non AWS Graviton-based instance types.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imagetype
            '''
            result = self._values.get("image_type")
            assert result is not None, "Required property 'image_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def image_id_override(self) -> typing.Optional[builtins.str]:
            '''The AMI ID used for instances launched in the compute environment that match the image type.

            This setting overrides the ``imageId`` set in the ``computeResource`` object.
            .. epigraph::

               The AMI that you choose for a compute environment must match the architecture of the instance types that you intend to use for that compute environment. For example, if your compute environment uses A1 instance types, the compute resource AMI that you choose must support ARM instances. Amazon ECS vends both x86 and ARM versions of the Amazon ECS-optimized Amazon Linux 2 AMI. For more information, see `Amazon ECS-optimized Amazon Linux 2 AMI <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html#ecs-optimized-ami-linux-variants.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imageidoverride
            '''
            result = self._values.get("image_id_override")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def image_kubernetes_version(self) -> typing.Optional[builtins.str]:
            '''The Kubernetes version for the compute environment.

            If you don't specify a value, the latest version that AWS Batch supports is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-ec2configurationobject.html#cfn-batch-computeenvironment-ec2configurationobject-imagekubernetesversion
            '''
            result = self._values.get("image_kubernetes_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "Ec2ConfigurationObjectProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.EksConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "eks_cluster_arn": "eksClusterArn",
            "kubernetes_namespace": "kubernetesNamespace",
        },
    )
    class EksConfigurationProperty:
        def __init__(
            self,
            *,
            eks_cluster_arn: builtins.str,
            kubernetes_namespace: builtins.str,
        ) -> None:
            '''Configuration for the Amazon EKS cluster that supports the AWS Batch compute environment.

            The cluster must exist before the compute environment can be created.

            :param eks_cluster_arn: The Amazon Resource Name (ARN) of the Amazon EKS cluster. An example is ``arn: *aws* :eks: *us-east-1* : *123456789012* :cluster/ *ClusterForBatch*`` .
            :param kubernetes_namespace: The namespace of the Amazon EKS cluster. AWS Batch manages pods in this namespace. The value can't left empty or null. It must be fewer than 64 characters long, can't be set to ``default`` , can't start with " ``kube-`` ," and must match this regular expression: ``^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`` . For more information, see `Namespaces <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_ in the Kubernetes documentation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-eksconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                eks_configuration_property = batch.CfnComputeEnvironment.EksConfigurationProperty(
                    eks_cluster_arn="eksClusterArn",
                    kubernetes_namespace="kubernetesNamespace"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75c6c485947f145511982cdf4fbb8da610e181cc7ef984298d438a09c767d796)
                check_type(argname="argument eks_cluster_arn", value=eks_cluster_arn, expected_type=type_hints["eks_cluster_arn"])
                check_type(argname="argument kubernetes_namespace", value=kubernetes_namespace, expected_type=type_hints["kubernetes_namespace"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "eks_cluster_arn": eks_cluster_arn,
                "kubernetes_namespace": kubernetes_namespace,
            }

        @builtins.property
        def eks_cluster_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Amazon EKS cluster.

            An example is ``arn: *aws* :eks: *us-east-1* : *123456789012* :cluster/ *ClusterForBatch*`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-eksconfiguration.html#cfn-batch-computeenvironment-eksconfiguration-eksclusterarn
            '''
            result = self._values.get("eks_cluster_arn")
            assert result is not None, "Required property 'eks_cluster_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kubernetes_namespace(self) -> builtins.str:
            '''The namespace of the Amazon EKS cluster.

            AWS Batch manages pods in this namespace. The value can't left empty or null. It must be fewer than 64 characters long, can't be set to ``default`` , can't start with " ``kube-`` ," and must match this regular expression: ``^[a-z0-9]([-a-z0-9]*[a-z0-9])?$`` . For more information, see `Namespaces <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/>`_ in the Kubernetes documentation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-eksconfiguration.html#cfn-batch-computeenvironment-eksconfiguration-kubernetesnamespace
            '''
            result = self._values.get("kubernetes_namespace")
            assert result is not None, "Required property 'kubernetes_namespace' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_template_id": "launchTemplateId",
            "launch_template_name": "launchTemplateName",
            "version": "version",
        },
    )
    class LaunchTemplateSpecificationProperty:
        def __init__(
            self,
            *,
            launch_template_id: typing.Optional[builtins.str] = None,
            launch_template_name: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An object that represents a launch template that's associated with a compute resource.

            You must specify either the launch template ID or launch template name in the request, but not both.

            If security groups are specified using both the ``securityGroupIds`` parameter of ``CreateComputeEnvironment`` and the launch template, the values in the ``securityGroupIds`` parameter of ``CreateComputeEnvironment`` will be used.
            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param launch_template_id: The ID of the launch template.
            :param launch_template_name: The name of the launch template.
            :param version: The version number of the launch template, ``$Latest`` , or ``$Default`` . If the value is ``$Latest`` , the latest version of the launch template is used. If the value is ``$Default`` , the default version of the launch template is used. .. epigraph:: If the AMI ID that's used in a compute environment is from the launch template, the AMI isn't changed when the compute environment is updated. It's only changed if the ``updateToLatestImageVersion`` parameter for the compute environment is set to ``true`` . During an infrastructure update, if either ``$Latest`` or ``$Default`` is specified, AWS Batch re-evaluates the launch template version, and it might use a different version of the launch template. This is the case even if the launch template isn't specified in the update. When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* . Default: ``$Default`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                launch_template_specification_property = batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty(
                    launch_template_id="launchTemplateId",
                    launch_template_name="launchTemplateName",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6d04f3237de0943c7f0f5becf9745ad232016e6c97fce1ca392b6c908b52d81)
                check_type(argname="argument launch_template_id", value=launch_template_id, expected_type=type_hints["launch_template_id"])
                check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_template_id is not None:
                self._values["launch_template_id"] = launch_template_id
            if launch_template_name is not None:
                self._values["launch_template_name"] = launch_template_name
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def launch_template_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the launch template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplateid
            '''
            result = self._values.get("launch_template_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def launch_template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the launch template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-launchtemplatename
            '''
            result = self._values.get("launch_template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version number of the launch template, ``$Latest`` , or ``$Default`` .

            If the value is ``$Latest`` , the latest version of the launch template is used. If the value is ``$Default`` , the default version of the launch template is used.
            .. epigraph::

               If the AMI ID that's used in a compute environment is from the launch template, the AMI isn't changed when the compute environment is updated. It's only changed if the ``updateToLatestImageVersion`` parameter for the compute environment is set to ``true`` . During an infrastructure update, if either ``$Latest`` or ``$Default`` is specified, AWS Batch re-evaluates the launch template version, and it might use a different version of the launch template. This is the case even if the launch template isn't specified in the update. When updating a compute environment, changing the launch template requires an infrastructure update of the compute environment. For more information, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            Default: ``$Default`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-launchtemplatespecification.html#cfn-batch-computeenvironment-launchtemplatespecification-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LaunchTemplateSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironment.UpdatePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "job_execution_timeout_minutes": "jobExecutionTimeoutMinutes",
            "terminate_jobs_on_update": "terminateJobsOnUpdate",
        },
    )
    class UpdatePolicyProperty:
        def __init__(
            self,
            *,
            job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
            terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Specifies the infrastructure update policy for the compute environment.

            For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

            :param job_execution_timeout_minutes: Specifies the job timeout (in minutes) when the compute environment infrastructure is updated. The default value is 30.
            :param terminate_jobs_on_update: Specifies whether jobs are automatically terminated when the computer environment infrastructure is updated. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-updatepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                update_policy_property = batch.CfnComputeEnvironment.UpdatePolicyProperty(
                    job_execution_timeout_minutes=123,
                    terminate_jobs_on_update=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75d7bc40febb29f50ea904aa6b5893aab138ad295bdc26efc9d8ab839650779c)
                check_type(argname="argument job_execution_timeout_minutes", value=job_execution_timeout_minutes, expected_type=type_hints["job_execution_timeout_minutes"])
                check_type(argname="argument terminate_jobs_on_update", value=terminate_jobs_on_update, expected_type=type_hints["terminate_jobs_on_update"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if job_execution_timeout_minutes is not None:
                self._values["job_execution_timeout_minutes"] = job_execution_timeout_minutes
            if terminate_jobs_on_update is not None:
                self._values["terminate_jobs_on_update"] = terminate_jobs_on_update

        @builtins.property
        def job_execution_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''Specifies the job timeout (in minutes) when the compute environment infrastructure is updated.

            The default value is 30.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-updatepolicy.html#cfn-batch-computeenvironment-updatepolicy-jobexecutiontimeoutminutes
            '''
            result = self._values.get("job_execution_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def terminate_jobs_on_update(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specifies whether jobs are automatically terminated when the computer environment infrastructure is updated.

            The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-updatepolicy.html#cfn-batch-computeenvironment-updatepolicy-terminatejobsonupdate
            '''
            result = self._values.get("terminate_jobs_on_update")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UpdatePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnComputeEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "compute_environment_name": "computeEnvironmentName",
        "compute_resources": "computeResources",
        "eks_configuration": "eksConfiguration",
        "replace_compute_environment": "replaceComputeEnvironment",
        "service_role": "serviceRole",
        "state": "state",
        "tags": "tags",
        "unmanagedv_cpus": "unmanagedvCpus",
        "update_policy": "updatePolicy",
    },
)
class CfnComputeEnvironmentProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union[typing.Union[CfnComputeEnvironment.ComputeResourcesProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        eks_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.EksConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        replace_compute_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        service_role: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        unmanagedv_cpus: typing.Optional[jsii.Number] = None,
        update_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.UpdatePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnComputeEnvironment``.

        :param type: The type of the compute environment: ``MANAGED`` or ``UNMANAGED`` . For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .
        :param compute_environment_name: The name for your compute environment. It can be up to 128 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param compute_resources: The ComputeResources property type specifies details of the compute resources managed by the compute environment. This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .
        :param eks_configuration: The details for the Amazon EKS cluster that supports the compute environment.
        :param replace_compute_environment: Specifies whether the compute environment is replaced if an update is made that requires replacing the instances in the compute environment. The default value is ``true`` . To enable more properties to be updated, set this property to ``false`` . When changing the value of this property to ``false`` , do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the ``UPDATE_ROLLBACK_FAILED`` state. You can't update a stack that is in the ``UPDATE_ROLLBACK_FAILED`` state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. For more information, see `Continue rolling back an update <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html>`_ in the *AWS CloudFormation User Guide* . The properties that can't be changed without replacing the compute environment are in the ```ComputeResources`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html>`_ property type: ```AllocationStrategy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ , ```BidPercentage`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage>`_ , ```Ec2Configuration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```ImageId`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ , ```InstanceRole`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole>`_ , ```InstanceTypes`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes>`_ , ```LaunchTemplate`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ , ```MaxvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus>`_ , ```MinvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus>`_ , ```PlacementGroup`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup>`_ , ```SecurityGroupIds`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids>`_ , ```Subnets`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets>`_ , `Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags>`_ , ```Type`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type>`_ , and ```UpdateToLatestImageVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ .
        :param service_role: The full Amazon Resource Name (ARN) of the IAM role that allows AWS Batch to make calls to other AWS services on your behalf. For more information, see `AWS Batch service IAM role <https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html>`_ in the *AWS Batch User Guide* . .. epigraph:: If your account already created the AWS Batch service-linked role, that role is used by default for your compute environment unless you specify a different role here. If the AWS Batch service-linked role doesn't exist in your account, and no role is specified here, the service attempts to create the AWS Batch service-linked role in your account. If your specified role has a path other than ``/`` , then you must specify either the full role ARN (recommended) or prefix the role name with the path. For example, if a role with the name ``bar`` has a path of ``/foo/`` , specify ``/foo/bar`` as the role name. For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* . .. epigraph:: Depending on how you created your AWS Batch service role, its ARN might contain the ``service-role`` path prefix. When you only specify the name of the service role, AWS Batch assumes that your ARN doesn't use the ``service-role`` path prefix. Because of this, we recommend that you specify the full ARN of your service role when you create compute environments.
        :param state: The state of the compute environment. If the state is ``ENABLED`` , then the compute environment accepts jobs from a queue and can scale out automatically based on queues. If the state is ``ENABLED`` , then the AWS Batch scheduler can attempt to place jobs from an associated job queue on the compute resources within the environment. If the compute environment is managed, then it can scale its instances out or in automatically, based on the job queue demand. If the state is ``DISABLED`` , then the AWS Batch scheduler doesn't attempt to place jobs within the environment. Jobs in a ``STARTING`` or ``RUNNING`` state continue to progress normally. Managed compute environments in the ``DISABLED`` state don't scale out. .. epigraph:: Compute environments in a ``DISABLED`` state may continue to incur billing charges. To prevent additional charges, turn off and then delete the compute environment. For more information, see `State <https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html#compute_environment_state>`_ in the *AWS Batch User Guide* . When an instance is idle, the instance scales down to the ``minvCpus`` value. However, the instance size doesn't change. For example, consider a ``c5.8xlarge`` instance with a ``minvCpus`` value of ``4`` and a ``desiredvCpus`` value of ``36`` . This instance doesn't scale down to a ``c5.large`` instance.
        :param tags: The tags applied to the compute environment.
        :param unmanagedv_cpus: The maximum number of vCPUs for an unmanaged compute environment. This parameter is only used for fair share scheduling to reserve vCPU capacity for new share identifiers. If this parameter isn't provided for a fair share job queue, no vCPU capacity is reserved. .. epigraph:: This parameter is only supported when the ``type`` parameter is set to ``UNMANAGED`` .
        :param update_policy: Specifies the infrastructure update policy for the compute environment. For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch as batch
            
            cfn_compute_environment_props = batch.CfnComputeEnvironmentProps(
                type="type",
            
                # the properties below are optional
                compute_environment_name="computeEnvironmentName",
                compute_resources=batch.CfnComputeEnvironment.ComputeResourcesProperty(
                    maxv_cpus=123,
                    subnets=["subnets"],
                    type="type",
            
                    # the properties below are optional
                    allocation_strategy="allocationStrategy",
                    bid_percentage=123,
                    desiredv_cpus=123,
                    ec2_configuration=[batch.CfnComputeEnvironment.Ec2ConfigurationObjectProperty(
                        image_type="imageType",
            
                        # the properties below are optional
                        image_id_override="imageIdOverride",
                        image_kubernetes_version="imageKubernetesVersion"
                    )],
                    ec2_key_pair="ec2KeyPair",
                    image_id="imageId",
                    instance_role="instanceRole",
                    instance_types=["instanceTypes"],
                    launch_template=batch.CfnComputeEnvironment.LaunchTemplateSpecificationProperty(
                        launch_template_id="launchTemplateId",
                        launch_template_name="launchTemplateName",
                        version="version"
                    ),
                    minv_cpus=123,
                    placement_group="placementGroup",
                    security_group_ids=["securityGroupIds"],
                    spot_iam_fleet_role="spotIamFleetRole",
                    tags={
                        "tags_key": "tags"
                    },
                    update_to_latest_image_version=False
                ),
                eks_configuration=batch.CfnComputeEnvironment.EksConfigurationProperty(
                    eks_cluster_arn="eksClusterArn",
                    kubernetes_namespace="kubernetesNamespace"
                ),
                replace_compute_environment=False,
                service_role="serviceRole",
                state="state",
                tags={
                    "tags_key": "tags"
                },
                unmanagedv_cpus=123,
                update_policy=batch.CfnComputeEnvironment.UpdatePolicyProperty(
                    job_execution_timeout_minutes=123,
                    terminate_jobs_on_update=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44457c64a729c5ff982fbfb1f21de15729c324ca632e1f48a3a7933efb884449)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument compute_resources", value=compute_resources, expected_type=type_hints["compute_resources"])
            check_type(argname="argument eks_configuration", value=eks_configuration, expected_type=type_hints["eks_configuration"])
            check_type(argname="argument replace_compute_environment", value=replace_compute_environment, expected_type=type_hints["replace_compute_environment"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument unmanagedv_cpus", value=unmanagedv_cpus, expected_type=type_hints["unmanagedv_cpus"])
            check_type(argname="argument update_policy", value=update_policy, expected_type=type_hints["update_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None:
            self._values["compute_resources"] = compute_resources
        if eks_configuration is not None:
            self._values["eks_configuration"] = eks_configuration
        if replace_compute_environment is not None:
            self._values["replace_compute_environment"] = replace_compute_environment
        if service_role is not None:
            self._values["service_role"] = service_role
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags
        if unmanagedv_cpus is not None:
            self._values["unmanagedv_cpus"] = unmanagedv_cpus
        if update_policy is not None:
            self._values["update_policy"] = update_policy

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the compute environment: ``MANAGED`` or ``UNMANAGED`` .

        For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''The name for your compute environment.

        It can be up to 128 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeenvironmentname
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_resources(
        self,
    ) -> typing.Optional[typing.Union[CfnComputeEnvironment.ComputeResourcesProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The ComputeResources property type specifies details of the compute resources managed by the compute environment.

        This parameter is required for managed compute environments. For more information, see `Compute Environments <https://docs.aws.amazon.com/batch/latest/userguide/compute_environments.html>`_ in the ** .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-computeresources
        '''
        result = self._values.get("compute_resources")
        return typing.cast(typing.Optional[typing.Union[CfnComputeEnvironment.ComputeResourcesProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def eks_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComputeEnvironment.EksConfigurationProperty]]:
        '''The details for the Amazon EKS cluster that supports the compute environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-eksconfiguration
        '''
        result = self._values.get("eks_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComputeEnvironment.EksConfigurationProperty]], result)

    @builtins.property
    def replace_compute_environment(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the compute environment is replaced if an update is made that requires replacing the instances in the compute environment.

        The default value is ``true`` . To enable more properties to be updated, set this property to ``false`` . When changing the value of this property to ``false`` , do not change any other properties at the same time. If other properties are changed at the same time, and the change needs to be rolled back but it can't, it's possible for the stack to go into the ``UPDATE_ROLLBACK_FAILED`` state. You can't update a stack that is in the ``UPDATE_ROLLBACK_FAILED`` state. However, if you can continue to roll it back, you can return the stack to its original settings and then try to update it again. For more information, see `Continue rolling back an update <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-continueupdaterollback.html>`_ in the *AWS CloudFormation User Guide* .

        The properties that can't be changed without replacing the compute environment are in the ```ComputeResources`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html>`_ property type: ```AllocationStrategy`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-allocationstrategy>`_ , ```BidPercentage`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-bidpercentage>`_ , ```Ec2Configuration`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2configuration>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```Ec2KeyPair`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-ec2keypair>`_ , ```ImageId`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-imageid>`_ , ```InstanceRole`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancerole>`_ , ```InstanceTypes`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-instancetypes>`_ , ```LaunchTemplate`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-launchtemplate>`_ , ```MaxvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-maxvcpus>`_ , ```MinvCpus`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-minvcpus>`_ , ```PlacementGroup`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-placementgroup>`_ , ```SecurityGroupIds`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-securitygroupids>`_ , ```Subnets`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-subnets>`_ , `Tags <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-tags>`_ , ```Type`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-type>`_ , and ```UpdateToLatestImageVersion`` <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html#cfn-batch-computeenvironment-computeresources-updatetolatestimageversion>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-replacecomputeenvironment
        '''
        result = self._values.get("replace_compute_environment")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def service_role(self) -> typing.Optional[builtins.str]:
        '''The full Amazon Resource Name (ARN) of the IAM role that allows AWS Batch to make calls to other AWS services on your behalf.

        For more information, see `AWS Batch service IAM role <https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html>`_ in the *AWS Batch User Guide* .
        .. epigraph::

           If your account already created the AWS Batch service-linked role, that role is used by default for your compute environment unless you specify a different role here. If the AWS Batch service-linked role doesn't exist in your account, and no role is specified here, the service attempts to create the AWS Batch service-linked role in your account.

        If your specified role has a path other than ``/`` , then you must specify either the full role ARN (recommended) or prefix the role name with the path. For example, if a role with the name ``bar`` has a path of ``/foo/`` , specify ``/foo/bar`` as the role name. For more information, see `Friendly names and paths <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names>`_ in the *IAM User Guide* .
        .. epigraph::

           Depending on how you created your AWS Batch service role, its ARN might contain the ``service-role`` path prefix. When you only specify the name of the service role, AWS Batch assumes that your ARN doesn't use the ``service-role`` path prefix. Because of this, we recommend that you specify the full ARN of your service role when you create compute environments.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-servicerole
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the compute environment.

        If the state is ``ENABLED`` , then the compute environment accepts jobs from a queue and can scale out automatically based on queues.

        If the state is ``ENABLED`` , then the AWS Batch scheduler can attempt to place jobs from an associated job queue on the compute resources within the environment. If the compute environment is managed, then it can scale its instances out or in automatically, based on the job queue demand.

        If the state is ``DISABLED`` , then the AWS Batch scheduler doesn't attempt to place jobs within the environment. Jobs in a ``STARTING`` or ``RUNNING`` state continue to progress normally. Managed compute environments in the ``DISABLED`` state don't scale out.
        .. epigraph::

           Compute environments in a ``DISABLED`` state may continue to incur billing charges. To prevent additional charges, turn off and then delete the compute environment. For more information, see `State <https://docs.aws.amazon.com/batch/latest/userguide/compute_environment_parameters.html#compute_environment_state>`_ in the *AWS Batch User Guide* .

        When an instance is idle, the instance scales down to the ``minvCpus`` value. However, the instance size doesn't change. For example, consider a ``c5.8xlarge`` instance with a ``minvCpus`` value of ``4`` and a ``desiredvCpus`` value of ``36`` . This instance doesn't scale down to a ``c5.large`` instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags applied to the compute environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def unmanagedv_cpus(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of vCPUs for an unmanaged compute environment.

        This parameter is only used for fair share scheduling to reserve vCPU capacity for new share identifiers. If this parameter isn't provided for a fair share job queue, no vCPU capacity is reserved.
        .. epigraph::

           This parameter is only supported when the ``type`` parameter is set to ``UNMANAGED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-unmanagedvcpus
        '''
        result = self._values.get("unmanagedv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def update_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComputeEnvironment.UpdatePolicyProperty]]:
        '''Specifies the infrastructure update policy for the compute environment.

        For more information about infrastructure updates, see `Updating compute environments <https://docs.aws.amazon.com/batch/latest/userguide/updating-compute-environments.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-computeenvironment.html#cfn-batch-computeenvironment-updatepolicy
        '''
        result = self._values.get("update_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComputeEnvironment.UpdatePolicyProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnJobDefinition(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnJobDefinition",
):
    '''A CloudFormation ``AWS::Batch::JobDefinition``.

    The ``AWS::Batch::JobDefinition`` resource specifies the parameters for an AWS Batch job definition. For more information, see `Job Definitions <https://docs.aws.amazon.com/batch/latest/userguide/job_definitions.html>`_ in the ** .

    :cloudformationResource: AWS::Batch::JobDefinition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch as batch
        
        # labels: Any
        # limits: Any
        # options: Any
        # parameters: Any
        # requests: Any
        # tags: Any
        
        cfn_job_definition = batch.CfnJobDefinition(self, "MyCfnJobDefinition",
            type="type",
        
            # the properties below are optional
            container_properties=batch.CfnJobDefinition.ContainerPropertiesProperty(
                image="image",
        
                # the properties below are optional
                command=["command"],
                environment=[batch.CfnJobDefinition.EnvironmentProperty(
                    name="name",
                    value="value"
                )],
                ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                    size_in_gi_b=123
                ),
                execution_role_arn="executionRoleArn",
                fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                    platform_version="platformVersion"
                ),
                instance_type="instanceType",
                job_role_arn="jobRoleArn",
                linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                    devices=[batch.CfnJobDefinition.DeviceProperty(
                        container_path="containerPath",
                        host_path="hostPath",
                        permissions=["permissions"]
                    )],
                    init_process_enabled=False,
                    max_swap=123,
                    shared_memory_size=123,
                    swappiness=123,
                    tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                        container_path="containerPath",
                        size=123,
        
                        # the properties below are optional
                        mount_options=["mountOptions"]
                    )]
                ),
                log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                    log_driver="logDriver",
        
                    # the properties below are optional
                    options=options,
                    secret_options=[batch.CfnJobDefinition.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )]
                ),
                memory=123,
                mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                    container_path="containerPath",
                    read_only=False,
                    source_volume="sourceVolume"
                )],
                network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                    assign_public_ip="assignPublicIp"
                ),
                privileged=False,
                readonly_root_filesystem=False,
                resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                    type="type",
                    value="value"
                )],
                secrets=[batch.CfnJobDefinition.SecretProperty(
                    name="name",
                    value_from="valueFrom"
                )],
                ulimits=[batch.CfnJobDefinition.UlimitProperty(
                    hard_limit=123,
                    name="name",
                    soft_limit=123
                )],
                user="user",
                vcpus=123,
                volumes=[batch.CfnJobDefinition.VolumesProperty(
                    efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                        file_system_id="fileSystemId",
        
                        # the properties below are optional
                        authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                            access_point_id="accessPointId",
                            iam="iam"
                        ),
                        root_directory="rootDirectory",
                        transit_encryption="transitEncryption",
                        transit_encryption_port=123
                    ),
                    host=batch.CfnJobDefinition.VolumesHostProperty(
                        source_path="sourcePath"
                    ),
                    name="name"
                )]
            ),
            eks_properties=batch.CfnJobDefinition.EksPropertiesProperty(
                pod_properties=batch.CfnJobDefinition.PodPropertiesProperty(
                    containers=[batch.CfnJobDefinition.EksContainerProperty(
                        image="image",
        
                        # the properties below are optional
                        args=["args"],
                        command=["command"],
                        env=[batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty(
                            name="name",
        
                            # the properties below are optional
                            value="value"
                        )],
                        image_pull_policy="imagePullPolicy",
                        name="name",
                        resources=batch.CfnJobDefinition.ResourcesProperty(
                            limits=limits,
                            requests=requests
                        ),
                        security_context=batch.CfnJobDefinition.SecurityContextProperty(
                            privileged=False,
                            read_only_root_filesystem=False,
                            run_as_group=123,
                            run_as_non_root=False,
                            run_as_user=123
                        ),
                        volume_mounts=[batch.CfnJobDefinition.EksContainerVolumeMountProperty(
                            mount_path="mountPath",
                            name="name",
                            read_only=False
                        )]
                    )],
                    dns_policy="dnsPolicy",
                    host_network=False,
                    metadata=batch.CfnJobDefinition.MetadataProperty(
                        labels=labels
                    ),
                    service_account_name="serviceAccountName",
                    volumes=[batch.CfnJobDefinition.EksVolumeProperty(
                        name="name",
        
                        # the properties below are optional
                        empty_dir=batch.CfnJobDefinition.EmptyDirProperty(
                            medium="medium",
                            size_limit="sizeLimit"
                        ),
                        host_path=batch.CfnJobDefinition.HostPathProperty(
                            path="path"
                        ),
                        secret=batch.CfnJobDefinition.EksSecretProperty(
                            secret_name="secretName",
        
                            # the properties below are optional
                            optional=False
                        )
                    )]
                )
            ),
            job_definition_name="jobDefinitionName",
            node_properties=batch.CfnJobDefinition.NodePropertiesProperty(
                main_node=123,
                node_range_properties=[batch.CfnJobDefinition.NodeRangePropertyProperty(
                    target_nodes="targetNodes",
        
                    # the properties below are optional
                    container=batch.CfnJobDefinition.ContainerPropertiesProperty(
                        image="image",
        
                        # the properties below are optional
                        command=["command"],
                        environment=[batch.CfnJobDefinition.EnvironmentProperty(
                            name="name",
                            value="value"
                        )],
                        ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                            size_in_gi_b=123
                        ),
                        execution_role_arn="executionRoleArn",
                        fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                            platform_version="platformVersion"
                        ),
                        instance_type="instanceType",
                        job_role_arn="jobRoleArn",
                        linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                            devices=[batch.CfnJobDefinition.DeviceProperty(
                                container_path="containerPath",
                                host_path="hostPath",
                                permissions=["permissions"]
                            )],
                            init_process_enabled=False,
                            max_swap=123,
                            shared_memory_size=123,
                            swappiness=123,
                            tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                                container_path="containerPath",
                                size=123,
        
                                # the properties below are optional
                                mount_options=["mountOptions"]
                            )]
                        ),
                        log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                            log_driver="logDriver",
        
                            # the properties below are optional
                            options=options,
                            secret_options=[batch.CfnJobDefinition.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )]
                        ),
                        memory=123,
                        mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                            container_path="containerPath",
                            read_only=False,
                            source_volume="sourceVolume"
                        )],
                        network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                            assign_public_ip="assignPublicIp"
                        ),
                        privileged=False,
                        readonly_root_filesystem=False,
                        resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                            type="type",
                            value="value"
                        )],
                        secrets=[batch.CfnJobDefinition.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )],
                        ulimits=[batch.CfnJobDefinition.UlimitProperty(
                            hard_limit=123,
                            name="name",
                            soft_limit=123
                        )],
                        user="user",
                        vcpus=123,
                        volumes=[batch.CfnJobDefinition.VolumesProperty(
                            efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                                file_system_id="fileSystemId",
        
                                # the properties below are optional
                                authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                                    access_point_id="accessPointId",
                                    iam="iam"
                                ),
                                root_directory="rootDirectory",
                                transit_encryption="transitEncryption",
                                transit_encryption_port=123
                            ),
                            host=batch.CfnJobDefinition.VolumesHostProperty(
                                source_path="sourcePath"
                            ),
                            name="name"
                        )]
                    )
                )],
                num_nodes=123
            ),
            parameters=parameters,
            platform_capabilities=["platformCapabilities"],
            propagate_tags=False,
            retry_strategy=batch.CfnJobDefinition.RetryStrategyProperty(
                attempts=123,
                evaluate_on_exit=[batch.CfnJobDefinition.EvaluateOnExitProperty(
                    action="action",
        
                    # the properties below are optional
                    on_exit_code="onExitCode",
                    on_reason="onReason",
                    on_status_reason="onStatusReason"
                )]
            ),
            scheduling_priority=123,
            tags=tags,
            timeout=batch.CfnJobDefinition.TimeoutProperty(
                attempt_duration_seconds=123
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        type: builtins.str,
        container_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.ContainerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        eks_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EksPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        node_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.NodePropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Any = None,
        platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        propagate_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        retry_strategy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.RetryStrategyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.TimeoutProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Batch::JobDefinition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: The type of job definition. For more information about multi-node parallel jobs, see `Creating a multi-node parallel job definition <https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html>`_ in the *AWS Batch User Guide* . .. epigraph:: If the job is run on Fargate resources, then ``multinode`` isn't supported.
        :param container_properties: An object with various properties specific to Amazon ECS based jobs. Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.
        :param eks_properties: An object with various properties that are specific to Amazon EKS based jobs. Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.
        :param job_definition_name: The name of the job definition.
        :param node_properties: An object with various properties that are specific to multi-node parallel jobs. Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified. .. epigraph:: If the job runs on Fargate resources, don't specify ``nodeProperties`` . Use ``containerProperties`` instead.
        :param parameters: Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a ``SubmitJob`` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see `Job definition parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html>`_ in the *AWS Batch User Guide* .
        :param platform_capabilities: The platform capabilities required by the job definition. If no value is specified, it defaults to ``EC2`` . Jobs run on Fargate resources specify ``FARGATE`` .
        :param propagate_tags: Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the ``FAILED`` state.
        :param retry_strategy: The retry strategy to use for failed jobs that are submitted with this job definition.
        :param scheduling_priority: The scheduling priority of the job definition. This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        :param tags: The tags that are applied to the job definition.
        :param timeout: The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09ec8de6705a545cf0dec395d0428610a6f30e1c3153ac78de0972e161cff8c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnJobDefinitionProps(
            type=type,
            container_properties=container_properties,
            eks_properties=eks_properties,
            job_definition_name=job_definition_name,
            node_properties=node_properties,
            parameters=parameters,
            platform_capabilities=platform_capabilities,
            propagate_tags=propagate_tags,
            retry_strategy=retry_strategy,
            scheduling_priority=scheduling_priority,
            tags=tags,
            timeout=timeout,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffdf3b83891dcd061b21f73c6403b713c55d8cb2ce0db150ac5fa995ce05670)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f1ea088ac0f6d10a55174546a8eb88016b0fff39aeccac98484a09241ff046)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags that are applied to the job definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        '''Default parameters or parameter substitution placeholders that are set in the job definition.

        Parameters are specified as a key-value pair mapping. Parameters in a ``SubmitJob`` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see `Job definition parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        '''
        return typing.cast(typing.Any, jsii.get(self, "parameters"))

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19e9fa72412a02a0d36931c48e44d3a4c64e4fa474774278451f6060c3b9381)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameters", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of job definition.

        For more information about multi-node parallel jobs, see `Creating a multi-node parallel job definition <https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html>`_ in the *AWS Batch User Guide* .
        .. epigraph::

           If the job is run on Fargate resources, then ``multinode`` isn't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865988743dae3f2c3b28bfc650692f8ddaf678f4a06c29ee10d04665c39d86ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="containerProperties")
    def container_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]]:
        '''An object with various properties specific to Amazon ECS based jobs.

        Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]], jsii.get(self, "containerProperties"))

    @container_properties.setter
    def container_properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa8a665ac0fc4175e4adeca0bd949ee7ece31bcc1e1d67f54315ea25959f0fc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerProperties", value)

    @builtins.property
    @jsii.member(jsii_name="eksProperties")
    def eks_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksPropertiesProperty"]]:
        '''An object with various properties that are specific to Amazon EKS based jobs.

        Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-eksproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksPropertiesProperty"]], jsii.get(self, "eksProperties"))

    @eks_properties.setter
    def eks_properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksPropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97f6e506a82a2e83baefa91b15a94232c42c77f069f25c68a722bc1ed1a10538)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eksProperties", value)

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobDefinitionName"))

    @job_definition_name.setter
    def job_definition_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a19ff7605217bedc6be9604fa338eb995376f0ee7155377d9595d6108ba3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobDefinitionName", value)

    @builtins.property
    @jsii.member(jsii_name="nodeProperties")
    def node_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NodePropertiesProperty"]]:
        '''An object with various properties that are specific to multi-node parallel jobs.

        Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.
        .. epigraph::

           If the job runs on Fargate resources, don't specify ``nodeProperties`` . Use ``containerProperties`` instead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NodePropertiesProperty"]], jsii.get(self, "nodeProperties"))

    @node_properties.setter
    def node_properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NodePropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b569e80dc519f1dac44b9d64419f86adc8ee9c828c95bf9aa7fffe90581323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeProperties", value)

    @builtins.property
    @jsii.member(jsii_name="platformCapabilities")
    def platform_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The platform capabilities required by the job definition.

        If no value is specified, it defaults to ``EC2`` . Jobs run on Fargate resources specify ``FARGATE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-platformcapabilities
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "platformCapabilities"))

    @platform_capabilities.setter
    def platform_capabilities(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a28268df731ecd0c6d2cba57b1762312c312552ae37915fbb6bf8a9202cfcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformCapabilities", value)

    @builtins.property
    @jsii.member(jsii_name="propagateTags")
    def propagate_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task.

        If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the ``FAILED`` state.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-propagatetags
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "propagateTags"))

    @propagate_tags.setter
    def propagate_tags(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6d8a7f5d85c48fd8a8369e01a8119bf08c42762b1156908d486b6cdfaeb517)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "propagateTags", value)

    @builtins.property
    @jsii.member(jsii_name="retryStrategy")
    def retry_strategy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.RetryStrategyProperty"]]:
        '''The retry strategy to use for failed jobs that are submitted with this job definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.RetryStrategyProperty"]], jsii.get(self, "retryStrategy"))

    @retry_strategy.setter
    def retry_strategy(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.RetryStrategyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82ccabeb4142f8f6d7aaedcee1a0c7e28e55c32f9b5f1b5478ec0e65fedb00f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retryStrategy", value)

    @builtins.property
    @jsii.member(jsii_name="schedulingPriority")
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''The scheduling priority of the job definition.

        This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-schedulingpriority
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "schedulingPriority"))

    @scheduling_priority.setter
    def scheduling_priority(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad2894dcbaf9ddb7e0e81e5e04176379ff49c8ab7a9fa7b0c1b8a2886454383b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulingPriority", value)

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.TimeoutProperty"]]:
        '''The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.TimeoutProperty"]], jsii.get(self, "timeout"))

    @timeout.setter
    def timeout(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.TimeoutProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a6af6e67e7a9f429c0ea70b5d8f10e14b564dff12df6c8f8fb22167ab82b1e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeout", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.AuthorizationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"access_point_id": "accessPointId", "iam": "iam"},
    )
    class AuthorizationConfigProperty:
        def __init__(
            self,
            *,
            access_point_id: typing.Optional[builtins.str] = None,
            iam: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The authorization configuration details for the Amazon EFS file system.

            :param access_point_id: The Amazon EFS access point ID to use. If an access point is specified, the root directory value specified in the ``EFSVolumeConfiguration`` must either be omitted or set to ``/`` which enforces the path set on the EFS access point. If an access point is used, transit encryption must be enabled in the ``EFSVolumeConfiguration`` . For more information, see `Working with Amazon EFS access points <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_ in the *Amazon Elastic File System User Guide* .
            :param iam: Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system. If enabled, transit encryption must be enabled in the ``EFSVolumeConfiguration`` . If this parameter is omitted, the default value of ``DISABLED`` is used. For more information, see `Using Amazon EFS access points <https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html#efs-volume-accesspoints>`_ in the *AWS Batch User Guide* . EFS IAM authorization requires that ``TransitEncryption`` be ``ENABLED`` and that a ``JobRoleArn`` is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-authorizationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                authorization_config_property = batch.CfnJobDefinition.AuthorizationConfigProperty(
                    access_point_id="accessPointId",
                    iam="iam"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b6dd1959b1c99e09ca004083b9c3b4a1da0f9c22ce44fde15de0a86bd4c8d570)
                check_type(argname="argument access_point_id", value=access_point_id, expected_type=type_hints["access_point_id"])
                check_type(argname="argument iam", value=iam, expected_type=type_hints["iam"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if access_point_id is not None:
                self._values["access_point_id"] = access_point_id
            if iam is not None:
                self._values["iam"] = iam

        @builtins.property
        def access_point_id(self) -> typing.Optional[builtins.str]:
            '''The Amazon EFS access point ID to use.

            If an access point is specified, the root directory value specified in the ``EFSVolumeConfiguration`` must either be omitted or set to ``/`` which enforces the path set on the EFS access point. If an access point is used, transit encryption must be enabled in the ``EFSVolumeConfiguration`` . For more information, see `Working with Amazon EFS access points <https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html>`_ in the *Amazon Elastic File System User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-authorizationconfig.html#cfn-batch-jobdefinition-authorizationconfig-accesspointid
            '''
            result = self._values.get("access_point_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def iam(self) -> typing.Optional[builtins.str]:
            '''Whether or not to use the AWS Batch job IAM role defined in a job definition when mounting the Amazon EFS file system.

            If enabled, transit encryption must be enabled in the ``EFSVolumeConfiguration`` . If this parameter is omitted, the default value of ``DISABLED`` is used. For more information, see `Using Amazon EFS access points <https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html#efs-volume-accesspoints>`_ in the *AWS Batch User Guide* . EFS IAM authorization requires that ``TransitEncryption`` be ``ENABLED`` and that a ``JobRoleArn`` is specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-authorizationconfig.html#cfn-batch-jobdefinition-authorizationconfig-iam
            '''
            result = self._values.get("iam")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthorizationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ContainerPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image": "image",
            "command": "command",
            "environment": "environment",
            "ephemeral_storage": "ephemeralStorage",
            "execution_role_arn": "executionRoleArn",
            "fargate_platform_configuration": "fargatePlatformConfiguration",
            "instance_type": "instanceType",
            "job_role_arn": "jobRoleArn",
            "linux_parameters": "linuxParameters",
            "log_configuration": "logConfiguration",
            "memory": "memory",
            "mount_points": "mountPoints",
            "network_configuration": "networkConfiguration",
            "privileged": "privileged",
            "readonly_root_filesystem": "readonlyRootFilesystem",
            "resource_requirements": "resourceRequirements",
            "secrets": "secrets",
            "ulimits": "ulimits",
            "user": "user",
            "vcpus": "vcpus",
            "volumes": "volumes",
        },
    )
    class ContainerPropertiesProperty:
        def __init__(
            self,
            *,
            image: builtins.str,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EnvironmentProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EphemeralStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            execution_role_arn: typing.Optional[builtins.str] = None,
            fargate_platform_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.FargatePlatformConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            instance_type: typing.Optional[builtins.str] = None,
            job_role_arn: typing.Optional[builtins.str] = None,
            linux_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.LinuxParametersProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            log_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.LogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            memory: typing.Optional[jsii.Number] = None,
            mount_points: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.MountPointsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            resource_requirements: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.ResourceRequirementProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            secrets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.SecretProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            ulimits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.UlimitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            user: typing.Optional[builtins.str] = None,
            vcpus: typing.Optional[jsii.Number] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.VolumesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Container properties are used for Amazon ECS based job definitions.

            These properties to describe the container that's launched as part of a job.

            :param image: The image used to start a container. This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with ``*repository-url* / *image* : *tag*`` . It can be 255 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), underscores (_), colons (:), periods (.), forward slashes (/), and number signs (#). This parameter maps to ``Image`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``IMAGE`` parameter of `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: Docker image architecture must match the processor architecture of the compute resources that they're scheduled on. For example, ARM-based Docker images can only run on ARM-based compute resources. - Images in Amazon ECR Public repositories use the full ``registry/repository[:tag]`` or ``registry/repository[@digest]`` naming conventions. For example, ``public.ecr.aws/ *registry_alias* / *my-web-app* : *latest*`` . - Images in Amazon ECR repositories use the full registry and repository URI (for example, ``123456789012.dkr.ecr.<region-name>.amazonaws.com/<repository-name>`` ). - Images in official repositories on Docker Hub use a single name (for example, ``ubuntu`` or ``mongo`` ). - Images in other repositories on Docker Hub are qualified with an organization name (for example, ``amazon/amazon-ecs-agent`` ). - Images in other online repositories are qualified further by a domain name (for example, ``quay.io/assemblyline/ubuntu`` ).
            :param command: The command that's passed to the container. This parameter maps to ``Cmd`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``COMMAND`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . For more information, see `https://docs.docker.com/engine/reference/builder/#cmd <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ .
            :param environment: The environment variables to pass to a container. This parameter maps to ``Env`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--env`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: We don't recommend using plaintext environment variables for sensitive information, such as credential data. > Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.
            :param ephemeral_storage: ``CfnJobDefinition.ContainerPropertiesProperty.EphemeralStorage``.
            :param execution_role_arn: The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume. For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .
            :param fargate_platform_configuration: The platform configuration for jobs that are running on Fargate resources. Jobs that are running on EC2 resources must not specify this parameter.
            :param instance_type: The instance type to use for a multi-node parallel job. All node groups in a multi-node parallel job must use the same instance type. .. epigraph:: This parameter isn't applicable to single-node container jobs or jobs that run on Fargate resources, and shouldn't be provided.
            :param job_role_arn: The Amazon Resource Name (ARN) of the IAM role that the container can assume for AWS permissions. For more information, see `IAM roles for tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param linux_parameters: Linux-specific modifications that are applied to the container, such as details for device mappings.
            :param log_configuration: The log configuration specification for the container. This parameter maps to ``LogConfig`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--log-driver`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . By default, containers use the same logging driver that the Docker daemon uses. However the container might use a different logging driver than the Docker daemon by specifying a log driver with this parameter in the container definition. To use a different logging driver for a container, the log system must be configured properly on the container instance (or on a different log server for remote logging options). For more information on the options for different supported log drivers, see `Configure logging drivers <https://docs.aws.amazon.com/https://docs.docker.com/engine/admin/logging/overview/>`_ in the Docker documentation. .. epigraph:: AWS Batch currently supports a subset of the logging drivers available to the Docker daemon (shown in the ``LogConfiguration`` data type). This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"`` .. epigraph:: The Amazon ECS container agent running on a container instance must register the logging drivers available on that instance with the ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before containers placed on that instance can use these log configuration options. For more information, see `Amazon ECS container agent configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`_ in the *Amazon Elastic Container Service Developer Guide* .
            :param memory: This parameter is deprecated, use ``resourceRequirements`` to specify the memory requirements for the job definition. It's not supported for jobs running on Fargate resources. For jobs that run on EC2 resources, it specifies the memory hard limit (in MiB) for a container. If your container attempts to exceed the specified number, it's terminated. You must specify at least 4 MiB of memory for a job using this parameter. The memory hard limit can be specified in several places. It must be specified for each node at least once.
            :param mount_points: The mount points for data volumes in your container. This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--volume`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            :param network_configuration: The network configuration for jobs that are running on Fargate resources. Jobs that are running on EC2 resources must not specify this parameter.
            :param privileged: When this parameter is true, the container is given elevated permissions on the host container instance (similar to the ``root`` user). This parameter maps to ``Privileged`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--privileged`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The default value is false. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided, or specified as false.
            :param readonly_root_filesystem: When this parameter is true, the container is given read-only access to its root file system. This parameter maps to ``ReadonlyRootfs`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--read-only`` option to ``docker run`` .
            :param resource_requirements: The type and amount of resources to assign to a container. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .
            :param secrets: The secrets for the container. For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .
            :param ulimits: A list of ``ulimits`` to set in the container. This parameter maps to ``Ulimits`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--ulimit`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.
            :param user: The user name to use inside the container. This parameter maps to ``User`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--user`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            :param vcpus: This parameter is deprecated, use ``resourceRequirements`` to specify the vCPU requirements for the job definition. It's not supported for jobs running on Fargate resources. For jobs running on EC2 resources, it specifies the number of vCPUs reserved for the job. Each vCPU is equivalent to 1,024 CPU shares. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The number of vCPUs must be specified but can be specified in several places. You must specify it at least once for each node.
            :param volumes: A list of data volumes used in a job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # options: Any
                
                container_properties_property = batch.CfnJobDefinition.ContainerPropertiesProperty(
                    image="image",
                
                    # the properties below are optional
                    command=["command"],
                    environment=[batch.CfnJobDefinition.EnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                        size_in_gi_b=123
                    ),
                    execution_role_arn="executionRoleArn",
                    fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                        platform_version="platformVersion"
                    ),
                    instance_type="instanceType",
                    job_role_arn="jobRoleArn",
                    linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                        devices=[batch.CfnJobDefinition.DeviceProperty(
                            container_path="containerPath",
                            host_path="hostPath",
                            permissions=["permissions"]
                        )],
                        init_process_enabled=False,
                        max_swap=123,
                        shared_memory_size=123,
                        swappiness=123,
                        tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                            container_path="containerPath",
                            size=123,
                
                            # the properties below are optional
                            mount_options=["mountOptions"]
                        )]
                    ),
                    log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                        log_driver="logDriver",
                
                        # the properties below are optional
                        options=options,
                        secret_options=[batch.CfnJobDefinition.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )]
                    ),
                    memory=123,
                    mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                        container_path="containerPath",
                        read_only=False,
                        source_volume="sourceVolume"
                    )],
                    network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                        assign_public_ip="assignPublicIp"
                    ),
                    privileged=False,
                    readonly_root_filesystem=False,
                    resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                        type="type",
                        value="value"
                    )],
                    secrets=[batch.CfnJobDefinition.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )],
                    ulimits=[batch.CfnJobDefinition.UlimitProperty(
                        hard_limit=123,
                        name="name",
                        soft_limit=123
                    )],
                    user="user",
                    vcpus=123,
                    volumes=[batch.CfnJobDefinition.VolumesProperty(
                        efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                            file_system_id="fileSystemId",
                
                            # the properties below are optional
                            authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                                access_point_id="accessPointId",
                                iam="iam"
                            ),
                            root_directory="rootDirectory",
                            transit_encryption="transitEncryption",
                            transit_encryption_port=123
                        ),
                        host=batch.CfnJobDefinition.VolumesHostProperty(
                            source_path="sourcePath"
                        ),
                        name="name"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c36bec7bbd2f351d26a8cf8b78efbd8f28320eb8ab212dfbc506e1eaeeb3f271)
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
                check_type(argname="argument ephemeral_storage", value=ephemeral_storage, expected_type=type_hints["ephemeral_storage"])
                check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
                check_type(argname="argument fargate_platform_configuration", value=fargate_platform_configuration, expected_type=type_hints["fargate_platform_configuration"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
                check_type(argname="argument job_role_arn", value=job_role_arn, expected_type=type_hints["job_role_arn"])
                check_type(argname="argument linux_parameters", value=linux_parameters, expected_type=type_hints["linux_parameters"])
                check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument mount_points", value=mount_points, expected_type=type_hints["mount_points"])
                check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
                check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
                check_type(argname="argument readonly_root_filesystem", value=readonly_root_filesystem, expected_type=type_hints["readonly_root_filesystem"])
                check_type(argname="argument resource_requirements", value=resource_requirements, expected_type=type_hints["resource_requirements"])
                check_type(argname="argument secrets", value=secrets, expected_type=type_hints["secrets"])
                check_type(argname="argument ulimits", value=ulimits, expected_type=type_hints["ulimits"])
                check_type(argname="argument user", value=user, expected_type=type_hints["user"])
                check_type(argname="argument vcpus", value=vcpus, expected_type=type_hints["vcpus"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "image": image,
            }
            if command is not None:
                self._values["command"] = command
            if environment is not None:
                self._values["environment"] = environment
            if ephemeral_storage is not None:
                self._values["ephemeral_storage"] = ephemeral_storage
            if execution_role_arn is not None:
                self._values["execution_role_arn"] = execution_role_arn
            if fargate_platform_configuration is not None:
                self._values["fargate_platform_configuration"] = fargate_platform_configuration
            if instance_type is not None:
                self._values["instance_type"] = instance_type
            if job_role_arn is not None:
                self._values["job_role_arn"] = job_role_arn
            if linux_parameters is not None:
                self._values["linux_parameters"] = linux_parameters
            if log_configuration is not None:
                self._values["log_configuration"] = log_configuration
            if memory is not None:
                self._values["memory"] = memory
            if mount_points is not None:
                self._values["mount_points"] = mount_points
            if network_configuration is not None:
                self._values["network_configuration"] = network_configuration
            if privileged is not None:
                self._values["privileged"] = privileged
            if readonly_root_filesystem is not None:
                self._values["readonly_root_filesystem"] = readonly_root_filesystem
            if resource_requirements is not None:
                self._values["resource_requirements"] = resource_requirements
            if secrets is not None:
                self._values["secrets"] = secrets
            if ulimits is not None:
                self._values["ulimits"] = ulimits
            if user is not None:
                self._values["user"] = user
            if vcpus is not None:
                self._values["vcpus"] = vcpus
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def image(self) -> builtins.str:
            '''The image used to start a container.

            This string is passed directly to the Docker daemon. Images in the Docker Hub registry are available by default. Other repositories are specified with ``*repository-url* / *image* : *tag*`` . It can be 255 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), underscores (_), colons (:), periods (.), forward slashes (/), and number signs (#). This parameter maps to ``Image`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``IMAGE`` parameter of `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               Docker image architecture must match the processor architecture of the compute resources that they're scheduled on. For example, ARM-based Docker images can only run on ARM-based compute resources.

            - Images in Amazon ECR Public repositories use the full ``registry/repository[:tag]`` or ``registry/repository[@digest]`` naming conventions. For example, ``public.ecr.aws/ *registry_alias* / *my-web-app* : *latest*`` .
            - Images in Amazon ECR repositories use the full registry and repository URI (for example, ``123456789012.dkr.ecr.<region-name>.amazonaws.com/<repository-name>`` ).
            - Images in official repositories on Docker Hub use a single name (for example, ``ubuntu`` or ``mongo`` ).
            - Images in other repositories on Docker Hub are qualified with an organization name (for example, ``amazon/amazon-ecs-agent`` ).
            - Images in other online repositories are qualified further by a domain name (for example, ``quay.io/assemblyline/ubuntu`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-image
            '''
            result = self._values.get("image")
            assert result is not None, "Required property 'image' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The command that's passed to the container.

            This parameter maps to ``Cmd`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``COMMAND`` parameter to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . For more information, see `https://docs.docker.com/engine/reference/builder/#cmd <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def environment(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EnvironmentProperty"]]]]:
            '''The environment variables to pass to a container.

            This parameter maps to ``Env`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--env`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               We don't recommend using plaintext environment variables for sensitive information, such as credential data. > Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-environment
            '''
            result = self._values.get("environment")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EnvironmentProperty"]]]], result)

        @builtins.property
        def ephemeral_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EphemeralStorageProperty"]]:
            '''``CfnJobDefinition.ContainerPropertiesProperty.EphemeralStorage``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-ephemeralstorage
            '''
            result = self._values.get("ephemeral_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EphemeralStorageProperty"]], result)

        @builtins.property
        def execution_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the execution role that AWS Batch can assume.

            For jobs that run on Fargate resources, you must provide an execution role. For more information, see `AWS Batch execution IAM role <https://docs.aws.amazon.com/batch/latest/userguide/execution-IAM-role.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-executionrolearn
            '''
            result = self._values.get("execution_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def fargate_platform_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.FargatePlatformConfigurationProperty"]]:
            '''The platform configuration for jobs that are running on Fargate resources.

            Jobs that are running on EC2 resources must not specify this parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-fargateplatformconfiguration
            '''
            result = self._values.get("fargate_platform_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.FargatePlatformConfigurationProperty"]], result)

        @builtins.property
        def instance_type(self) -> typing.Optional[builtins.str]:
            '''The instance type to use for a multi-node parallel job.

            All node groups in a multi-node parallel job must use the same instance type.
            .. epigraph::

               This parameter isn't applicable to single-node container jobs or jobs that run on Fargate resources, and shouldn't be provided.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-instancetype
            '''
            result = self._values.get("instance_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def job_role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role that the container can assume for AWS permissions.

            For more information, see `IAM roles for tasks <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-jobrolearn
            '''
            result = self._values.get("job_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.LinuxParametersProperty"]]:
            '''Linux-specific modifications that are applied to the container, such as details for device mappings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-linuxparameters
            '''
            result = self._values.get("linux_parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.LinuxParametersProperty"]], result)

        @builtins.property
        def log_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.LogConfigurationProperty"]]:
            '''The log configuration specification for the container.

            This parameter maps to ``LogConfig`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--log-driver`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . By default, containers use the same logging driver that the Docker daemon uses. However the container might use a different logging driver than the Docker daemon by specifying a log driver with this parameter in the container definition. To use a different logging driver for a container, the log system must be configured properly on the container instance (or on a different log server for remote logging options). For more information on the options for different supported log drivers, see `Configure logging drivers <https://docs.aws.amazon.com/https://docs.docker.com/engine/admin/logging/overview/>`_ in the Docker documentation.
            .. epigraph::

               AWS Batch currently supports a subset of the logging drivers available to the Docker daemon (shown in the ``LogConfiguration`` data type).

            This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            .. epigraph::

               The Amazon ECS container agent running on a container instance must register the logging drivers available on that instance with the ``ECS_AVAILABLE_LOGGING_DRIVERS`` environment variable before containers placed on that instance can use these log configuration options. For more information, see `Amazon ECS container agent configuration <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-logconfiguration
            '''
            result = self._values.get("log_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.LogConfigurationProperty"]], result)

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            '''This parameter is deprecated, use ``resourceRequirements`` to specify the memory requirements for the job definition.

            It's not supported for jobs running on Fargate resources. For jobs that run on EC2 resources, it specifies the memory hard limit (in MiB) for a container. If your container attempts to exceed the specified number, it's terminated. You must specify at least 4 MiB of memory for a job using this parameter. The memory hard limit can be specified in several places. It must be specified for each node at least once.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mount_points(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.MountPointsProperty"]]]]:
            '''The mount points for data volumes in your container.

            This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--volume`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-mountpoints
            '''
            result = self._values.get("mount_points")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.MountPointsProperty"]]]], result)

        @builtins.property
        def network_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NetworkConfigurationProperty"]]:
            '''The network configuration for jobs that are running on Fargate resources.

            Jobs that are running on EC2 resources must not specify this parameter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-networkconfiguration
            '''
            result = self._values.get("network_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NetworkConfigurationProperty"]], result)

        @builtins.property
        def privileged(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''When this parameter is true, the container is given elevated permissions on the host container instance (similar to the ``root`` user).

            This parameter maps to ``Privileged`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--privileged`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The default value is false.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided, or specified as false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-privileged
            '''
            result = self._values.get("privileged")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def readonly_root_filesystem(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''When this parameter is true, the container is given read-only access to its root file system.

            This parameter maps to ``ReadonlyRootfs`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--read-only`` option to ``docker run`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-readonlyrootfilesystem
            '''
            result = self._values.get("readonly_root_filesystem")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def resource_requirements(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ResourceRequirementProperty"]]]]:
            '''The type and amount of resources to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-resourcerequirements
            '''
            result = self._values.get("resource_requirements")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ResourceRequirementProperty"]]]], result)

        @builtins.property
        def secrets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.SecretProperty"]]]]:
            '''The secrets for the container.

            For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-secrets
            '''
            result = self._values.get("secrets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.SecretProperty"]]]], result)

        @builtins.property
        def ulimits(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.UlimitProperty"]]]]:
            '''A list of ``ulimits`` to set in the container.

            This parameter maps to ``Ulimits`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--ulimit`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-ulimits
            '''
            result = self._values.get("ulimits")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.UlimitProperty"]]]], result)

        @builtins.property
        def user(self) -> typing.Optional[builtins.str]:
            '''The user name to use inside the container.

            This parameter maps to ``User`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--user`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-user
            '''
            result = self._values.get("user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vcpus(self) -> typing.Optional[jsii.Number]:
            '''This parameter is deprecated, use ``resourceRequirements`` to specify the vCPU requirements for the job definition.

            It's not supported for jobs running on Fargate resources. For jobs running on EC2 resources, it specifies the number of vCPUs reserved for the job.

            Each vCPU is equivalent to 1,024 CPU shares. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . The number of vCPUs must be specified but can be specified in several places. You must specify it at least once for each node.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-vcpus
            '''
            result = self._values.get("vcpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.VolumesProperty"]]]]:
            '''A list of data volumes used in a job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties.html#cfn-batch-jobdefinition-containerproperties-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.VolumesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ContainerPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.DeviceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "host_path": "hostPath",
            "permissions": "permissions",
        },
    )
    class DeviceProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            host_path: typing.Optional[builtins.str] = None,
            permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that represents a container instance host device.

            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.

            :param container_path: The path inside the container that's used to expose the host device. By default, the ``hostPath`` value is used.
            :param host_path: The path for the device on the host container instance.
            :param permissions: The explicit permissions to provide to the container for the device. By default, the container has permissions for ``read`` , ``write`` , and ``mknod`` for the device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                device_property = batch.CfnJobDefinition.DeviceProperty(
                    container_path="containerPath",
                    host_path="hostPath",
                    permissions=["permissions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__35fe4ef9664bfaf270ea5abc9abf4321ad3f4a2efd4baa5b171bad4edefb04e0)
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
                check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if host_path is not None:
                self._values["host_path"] = host_path
            if permissions is not None:
                self._values["permissions"] = permissions

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''The path inside the container that's used to expose the host device.

            By default, the ``hostPath`` value is used.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_path(self) -> typing.Optional[builtins.str]:
            '''The path for the device on the host container instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-hostpath
            '''
            result = self._values.get("host_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def permissions(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The explicit permissions to provide to the container for the device.

            By default, the container has permissions for ``read`` , ``write`` , and ``mknod`` for the device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-device.html#cfn-batch-jobdefinition-device-permissions
            '''
            result = self._values.get("permissions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeviceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EfsVolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "file_system_id": "fileSystemId",
            "authorization_config": "authorizationConfig",
            "root_directory": "rootDirectory",
            "transit_encryption": "transitEncryption",
            "transit_encryption_port": "transitEncryptionPort",
        },
    )
    class EfsVolumeConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_id: builtins.str,
            authorization_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.AuthorizationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            root_directory: typing.Optional[builtins.str] = None,
            transit_encryption: typing.Optional[builtins.str] = None,
            transit_encryption_port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''This is used when you're using an Amazon Elastic File System file system for job storage.

            For more information, see `Amazon EFS Volumes <https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html>`_ in the *AWS Batch User Guide* .

            :param file_system_id: The Amazon EFS file system ID to use.
            :param authorization_config: The authorization configuration details for the Amazon EFS file system.
            :param root_directory: The directory within the Amazon EFS file system to mount as the root directory inside the host. If this parameter is omitted, the root of the Amazon EFS volume is used instead. Specifying ``/`` has the same effect as omitting this parameter. The maximum length is 4,096 characters. .. epigraph:: If an EFS access point is specified in the ``authorizationConfig`` , the root directory parameter must either be omitted or set to ``/`` , which enforces the path set on the Amazon EFS access point.
            :param transit_encryption: Determines whether to enable encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server. Transit encryption must be enabled if Amazon EFS IAM authorization is used. If this parameter is omitted, the default value of ``DISABLED`` is used. For more information, see `Encrypting data in transit <https://docs.aws.amazon.com/efs/latest/ug/encryption-in-transit.html>`_ in the *Amazon Elastic File System User Guide* .
            :param transit_encryption_port: The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server. If you don't specify a transit encryption port, it uses the port selection strategy that the Amazon EFS mount helper uses. The value must be between 0 and 65,535. For more information, see `EFS mount helper <https://docs.aws.amazon.com/efs/latest/ug/efs-mount-helper.html>`_ in the *Amazon Elastic File System User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                efs_volume_configuration_property = batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                    file_system_id="fileSystemId",
                
                    # the properties below are optional
                    authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                        access_point_id="accessPointId",
                        iam="iam"
                    ),
                    root_directory="rootDirectory",
                    transit_encryption="transitEncryption",
                    transit_encryption_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dcfbc9b547d661e2143ab9658d20564fb7843f0e04ae5735703f79fa3b0163a4)
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument authorization_config", value=authorization_config, expected_type=type_hints["authorization_config"])
                check_type(argname="argument root_directory", value=root_directory, expected_type=type_hints["root_directory"])
                check_type(argname="argument transit_encryption", value=transit_encryption, expected_type=type_hints["transit_encryption"])
                check_type(argname="argument transit_encryption_port", value=transit_encryption_port, expected_type=type_hints["transit_encryption_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "file_system_id": file_system_id,
            }
            if authorization_config is not None:
                self._values["authorization_config"] = authorization_config
            if root_directory is not None:
                self._values["root_directory"] = root_directory
            if transit_encryption is not None:
                self._values["transit_encryption"] = transit_encryption
            if transit_encryption_port is not None:
                self._values["transit_encryption_port"] = transit_encryption_port

        @builtins.property
        def file_system_id(self) -> builtins.str:
            '''The Amazon EFS file system ID to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            assert result is not None, "Required property 'file_system_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def authorization_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.AuthorizationConfigProperty"]]:
            '''The authorization configuration details for the Amazon EFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-authorizationconfig
            '''
            result = self._values.get("authorization_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.AuthorizationConfigProperty"]], result)

        @builtins.property
        def root_directory(self) -> typing.Optional[builtins.str]:
            '''The directory within the Amazon EFS file system to mount as the root directory inside the host.

            If this parameter is omitted, the root of the Amazon EFS volume is used instead. Specifying ``/`` has the same effect as omitting this parameter. The maximum length is 4,096 characters.
            .. epigraph::

               If an EFS access point is specified in the ``authorizationConfig`` , the root directory parameter must either be omitted or set to ``/`` , which enforces the path set on the Amazon EFS access point.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-rootdirectory
            '''
            result = self._values.get("root_directory")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transit_encryption(self) -> typing.Optional[builtins.str]:
            '''Determines whether to enable encryption for Amazon EFS data in transit between the Amazon ECS host and the Amazon EFS server.

            Transit encryption must be enabled if Amazon EFS IAM authorization is used. If this parameter is omitted, the default value of ``DISABLED`` is used. For more information, see `Encrypting data in transit <https://docs.aws.amazon.com/efs/latest/ug/encryption-in-transit.html>`_ in the *Amazon Elastic File System User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-transitencryption
            '''
            result = self._values.get("transit_encryption")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def transit_encryption_port(self) -> typing.Optional[jsii.Number]:
            '''The port to use when sending encrypted data between the Amazon ECS host and the Amazon EFS server.

            If you don't specify a transit encryption port, it uses the port selection strategy that the Amazon EFS mount helper uses. The value must be between 0 and 65,535. For more information, see `EFS mount helper <https://docs.aws.amazon.com/efs/latest/ug/efs-mount-helper.html>`_ in the *Amazon Elastic File System User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-efsvolumeconfiguration.html#cfn-batch-jobdefinition-efsvolumeconfiguration-transitencryptionport
            '''
            result = self._values.get("transit_encryption_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EfsVolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EksContainerEnvironmentVariableProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An environment variable.

            :param name: The name of the environment variable.
            :param value: The value of the environment variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerenvironmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                eks_container_environment_variable_property = batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty(
                    name="name",
                
                    # the properties below are optional
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5102752e15e97c347ddb868c096e52cbf237ad566b130f28bb70cdf3332131b7)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the environment variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerenvironmentvariable.html#cfn-batch-jobdefinition-ekscontainerenvironmentvariable-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerenvironmentvariable.html#cfn-batch-jobdefinition-ekscontainerenvironmentvariable-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksContainerEnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EksContainerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "image": "image",
            "args": "args",
            "command": "command",
            "env": "env",
            "image_pull_policy": "imagePullPolicy",
            "name": "name",
            "resources": "resources",
            "security_context": "securityContext",
            "volume_mounts": "volumeMounts",
        },
    )
    class EksContainerProperty:
        def __init__(
            self,
            *,
            image: builtins.str,
            args: typing.Optional[typing.Sequence[builtins.str]] = None,
            command: typing.Optional[typing.Sequence[builtins.str]] = None,
            env: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EksContainerEnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            image_pull_policy: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            resources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.ResourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_context: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.SecurityContextProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_mounts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EksContainerVolumeMountProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''EKS container properties are used in job definitions for Amazon EKS based job definitions to describe the properties for a container node in the pod that's launched as part of a job.

            This can't be specified for Amazon ECS based job definitions.

            :param image: The Docker image used to start the container.
            :param args: An array of arguments to the entrypoint. If this isn't specified, the ``CMD`` of the container image is used. This corresponds to the ``args`` member in the `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ portion of the `Pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/>`_ in Kubernetes. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` , and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` is passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. For more information, see `CMD <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ in the *Dockerfile reference* and `Define a command and arguments for a pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ in the *Kubernetes documentation* .
            :param command: The entrypoint for the container. This isn't run within a shell. If this isn't specified, the ``ENTRYPOINT`` of the container image is used. Environment variable references are expanded using the container's environment. If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. The entrypoint can't be updated. For more information, see `ENTRYPOINT <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#entrypoint>`_ in the *Dockerfile reference* and `Define a command and arguments for a container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ and `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ in the *Kubernetes documentation* .
            :param env: The environment variables to pass to a container. .. epigraph:: Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.
            :param image_pull_policy: The image pull policy for the container. Supported values are ``Always`` , ``IfNotPresent`` , and ``Never`` . This parameter defaults to ``IfNotPresent`` . However, if the ``:latest`` tag is specified, it defaults to ``Always`` . For more information, see `Updating images <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/containers/images/#updating-images>`_ in the *Kubernetes documentation* .
            :param name: The name of the container. If the name isn't specified, the default name " ``Default`` " is used. Each container in a pod must have a unique name.
            :param resources: The type and amount of resources to assign to a container. The supported resources include ``memory`` , ``cpu`` , and ``nvidia.com/gpu`` . For more information, see `Resource management for pods and containers <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>`_ in the *Kubernetes documentation* .
            :param security_context: The security context for a job. For more information, see `Configure a security context for a pod or container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>`_ in the *Kubernetes documentation* .
            :param volume_mounts: The volume mounts for the container. AWS Batch supports ``emptyDir`` , ``hostPath`` , and ``secret`` volume types. For more information about volumes and volume mounts in Kubernetes, see `Volumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # limits: Any
                # requests: Any
                
                eks_container_property = batch.CfnJobDefinition.EksContainerProperty(
                    image="image",
                
                    # the properties below are optional
                    args=["args"],
                    command=["command"],
                    env=[batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty(
                        name="name",
                
                        # the properties below are optional
                        value="value"
                    )],
                    image_pull_policy="imagePullPolicy",
                    name="name",
                    resources=batch.CfnJobDefinition.ResourcesProperty(
                        limits=limits,
                        requests=requests
                    ),
                    security_context=batch.CfnJobDefinition.SecurityContextProperty(
                        privileged=False,
                        read_only_root_filesystem=False,
                        run_as_group=123,
                        run_as_non_root=False,
                        run_as_user=123
                    ),
                    volume_mounts=[batch.CfnJobDefinition.EksContainerVolumeMountProperty(
                        mount_path="mountPath",
                        name="name",
                        read_only=False
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__07330371bcb1f8637f0ce902c267671a26ddf915f0287a6c9ff05e28baa8ff7b)
                check_type(argname="argument image", value=image, expected_type=type_hints["image"])
                check_type(argname="argument args", value=args, expected_type=type_hints["args"])
                check_type(argname="argument command", value=command, expected_type=type_hints["command"])
                check_type(argname="argument env", value=env, expected_type=type_hints["env"])
                check_type(argname="argument image_pull_policy", value=image_pull_policy, expected_type=type_hints["image_pull_policy"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
                check_type(argname="argument security_context", value=security_context, expected_type=type_hints["security_context"])
                check_type(argname="argument volume_mounts", value=volume_mounts, expected_type=type_hints["volume_mounts"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "image": image,
            }
            if args is not None:
                self._values["args"] = args
            if command is not None:
                self._values["command"] = command
            if env is not None:
                self._values["env"] = env
            if image_pull_policy is not None:
                self._values["image_pull_policy"] = image_pull_policy
            if name is not None:
                self._values["name"] = name
            if resources is not None:
                self._values["resources"] = resources
            if security_context is not None:
                self._values["security_context"] = security_context
            if volume_mounts is not None:
                self._values["volume_mounts"] = volume_mounts

        @builtins.property
        def image(self) -> builtins.str:
            '''The Docker image used to start the container.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-image
            '''
            result = self._values.get("image")
            assert result is not None, "Required property 'image' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of arguments to the entrypoint.

            If this isn't specified, the ``CMD`` of the container image is used. This corresponds to the ``args`` member in the `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ portion of the `Pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/>`_ in Kubernetes. Environment variable references are expanded using the container's environment.

            If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` , and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` is passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. For more information, see `CMD <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#cmd>`_ in the *Dockerfile reference* and `Define a command and arguments for a pod <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-args
            '''
            result = self._values.get("args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def command(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The entrypoint for the container.

            This isn't run within a shell. If this isn't specified, the ``ENTRYPOINT`` of the container image is used. Environment variable references are expanded using the container's environment.

            If the referenced environment variable doesn't exist, the reference in the command isn't changed. For example, if the reference is to " ``$(NAME1)`` " and the ``NAME1`` environment variable doesn't exist, the command string will remain " ``$(NAME1)`` ." ``$$`` is replaced with ``$`` and the resulting string isn't expanded. For example, ``$$(VAR_NAME)`` will be passed as ``$(VAR_NAME)`` whether or not the ``VAR_NAME`` environment variable exists. The entrypoint can't be updated. For more information, see `ENTRYPOINT <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/builder/#entrypoint>`_ in the *Dockerfile reference* and `Define a command and arguments for a container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_ and `Entrypoint <https://docs.aws.amazon.com/https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#entrypoint>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-command
            '''
            result = self._values.get("command")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def env(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksContainerEnvironmentVariableProperty"]]]]:
            '''The environment variables to pass to a container.

            .. epigraph::

               Environment variables cannot start with " ``AWS_BATCH`` ". This naming convention is reserved for variables that AWS Batch sets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-env
            '''
            result = self._values.get("env")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksContainerEnvironmentVariableProperty"]]]], result)

        @builtins.property
        def image_pull_policy(self) -> typing.Optional[builtins.str]:
            '''The image pull policy for the container.

            Supported values are ``Always`` , ``IfNotPresent`` , and ``Never`` . This parameter defaults to ``IfNotPresent`` . However, if the ``:latest`` tag is specified, it defaults to ``Always`` . For more information, see `Updating images <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/containers/images/#updating-images>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-imagepullpolicy
            '''
            result = self._values.get("image_pull_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the container.

            If the name isn't specified, the default name " ``Default`` " is used. Each container in a pod must have a unique name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ResourcesProperty"]]:
            '''The type and amount of resources to assign to a container.

            The supported resources include ``memory`` , ``cpu`` , and ``nvidia.com/gpu`` . For more information, see `Resource management for pods and containers <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-resources
            '''
            result = self._values.get("resources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ResourcesProperty"]], result)

        @builtins.property
        def security_context(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.SecurityContextProperty"]]:
            '''The security context for a job.

            For more information, see `Configure a security context for a pod or container <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-securitycontext
            '''
            result = self._values.get("security_context")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.SecurityContextProperty"]], result)

        @builtins.property
        def volume_mounts(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksContainerVolumeMountProperty"]]]]:
            '''The volume mounts for the container.

            AWS Batch supports ``emptyDir`` , ``hostPath`` , and ``secret`` volume types. For more information about volumes and volume mounts in Kubernetes, see `Volumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainer.html#cfn-batch-jobdefinition-ekscontainer-volumemounts
            '''
            result = self._values.get("volume_mounts")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksContainerVolumeMountProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksContainerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EksContainerVolumeMountProperty",
        jsii_struct_bases=[],
        name_mapping={
            "mount_path": "mountPath",
            "name": "name",
            "read_only": "readOnly",
        },
    )
    class EksContainerVolumeMountProperty:
        def __init__(
            self,
            *,
            mount_path: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''The volume mounts for a container for an Amazon EKS job.

            For more information about volumes and volume mounts in Kubernetes, see `Volumes <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/>`_ in the *Kubernetes documentation* .

            :param mount_path: The path on the container where the volume is mounted.
            :param name: The name the volume mount. This must match the name of one of the volumes in the pod.
            :param read_only: If this value is ``true`` , the container has read-only access to the volume. Otherwise, the container can write to the volume. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                eks_container_volume_mount_property = batch.CfnJobDefinition.EksContainerVolumeMountProperty(
                    mount_path="mountPath",
                    name="name",
                    read_only=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__62a561e3828d7cfb4c75e48064ea5d673ac3360be196c55629ccb243d5c9977b)
                check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if mount_path is not None:
                self._values["mount_path"] = mount_path
            if name is not None:
                self._values["name"] = name
            if read_only is not None:
                self._values["read_only"] = read_only

        @builtins.property
        def mount_path(self) -> typing.Optional[builtins.str]:
            '''The path on the container where the volume is mounted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-mountpath
            '''
            result = self._values.get("mount_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name the volume mount.

            This must match the name of one of the volumes in the pod.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If this value is ``true`` , the container has read-only access to the volume.

            Otherwise, the container can write to the volume. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainervolumemount.html#cfn-batch-jobdefinition-ekscontainervolumemount-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksContainerVolumeMountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EksPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"pod_properties": "podProperties"},
    )
    class EksPropertiesProperty:
        def __init__(
            self,
            *,
            pod_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.PodPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that contains the properties for the Kubernetes resources of a job.

            :param pod_properties: The properties for the Kubernetes pod resources of a job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # labels: Any
                # limits: Any
                # requests: Any
                
                eks_properties_property = batch.CfnJobDefinition.EksPropertiesProperty(
                    pod_properties=batch.CfnJobDefinition.PodPropertiesProperty(
                        containers=[batch.CfnJobDefinition.EksContainerProperty(
                            image="image",
                
                            # the properties below are optional
                            args=["args"],
                            command=["command"],
                            env=[batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty(
                                name="name",
                
                                # the properties below are optional
                                value="value"
                            )],
                            image_pull_policy="imagePullPolicy",
                            name="name",
                            resources=batch.CfnJobDefinition.ResourcesProperty(
                                limits=limits,
                                requests=requests
                            ),
                            security_context=batch.CfnJobDefinition.SecurityContextProperty(
                                privileged=False,
                                read_only_root_filesystem=False,
                                run_as_group=123,
                                run_as_non_root=False,
                                run_as_user=123
                            ),
                            volume_mounts=[batch.CfnJobDefinition.EksContainerVolumeMountProperty(
                                mount_path="mountPath",
                                name="name",
                                read_only=False
                            )]
                        )],
                        dns_policy="dnsPolicy",
                        host_network=False,
                        metadata=batch.CfnJobDefinition.MetadataProperty(
                            labels=labels
                        ),
                        service_account_name="serviceAccountName",
                        volumes=[batch.CfnJobDefinition.EksVolumeProperty(
                            name="name",
                
                            # the properties below are optional
                            empty_dir=batch.CfnJobDefinition.EmptyDirProperty(
                                medium="medium",
                                size_limit="sizeLimit"
                            ),
                            host_path=batch.CfnJobDefinition.HostPathProperty(
                                path="path"
                            ),
                            secret=batch.CfnJobDefinition.EksSecretProperty(
                                secret_name="secretName",
                
                                # the properties below are optional
                                optional=False
                            )
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5f6833a85c1a2916f4d0d61c549a2b582b50946cf34bb122cde97a47f3f3630d)
                check_type(argname="argument pod_properties", value=pod_properties, expected_type=type_hints["pod_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if pod_properties is not None:
                self._values["pod_properties"] = pod_properties

        @builtins.property
        def pod_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.PodPropertiesProperty"]]:
            '''The properties for the Kubernetes pod resources of a job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksproperties.html#cfn-batch-jobdefinition-eksproperties-podproperties
            '''
            result = self._values.get("pod_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.PodPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EksSecretProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_name": "secretName", "optional": "optional"},
    )
    class EksSecretProperty:
        def __init__(
            self,
            *,
            secret_name: builtins.str,
            optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''
            :param secret_name: ``CfnJobDefinition.EksSecretProperty.SecretName``.
            :param optional: ``CfnJobDefinition.EksSecretProperty.Optional``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekssecret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                eks_secret_property = batch.CfnJobDefinition.EksSecretProperty(
                    secret_name="secretName",
                
                    # the properties below are optional
                    optional=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4237d0f232d47de96690769028656e53b44f46fd8b8c5b7fa035950da743f230)
                check_type(argname="argument secret_name", value=secret_name, expected_type=type_hints["secret_name"])
                check_type(argname="argument optional", value=optional, expected_type=type_hints["optional"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_name": secret_name,
            }
            if optional is not None:
                self._values["optional"] = optional

        @builtins.property
        def secret_name(self) -> builtins.str:
            '''``CfnJobDefinition.EksSecretProperty.SecretName``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekssecret.html#cfn-batch-jobdefinition-ekssecret-secretname
            '''
            result = self._values.get("secret_name")
            assert result is not None, "Required property 'secret_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def optional(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnJobDefinition.EksSecretProperty.Optional``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekssecret.html#cfn-batch-jobdefinition-ekssecret-optional
            '''
            result = self._values.get("optional")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksSecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EksVolumeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "empty_dir": "emptyDir",
            "host_path": "hostPath",
            "secret": "secret",
        },
    )
    class EksVolumeProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            empty_dir: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EmptyDirProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            host_path: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.HostPathProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            secret: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EksSecretProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Specifies an Amazon EKS volume for a job definition.

            :param name: The name of the volume. The name must be allowed as a DNS subdomain name. For more information, see `DNS subdomain names <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names>`_ in the *Kubernetes documentation* .
            :param empty_dir: Specifies the configuration of a Kubernetes ``emptyDir`` volume. For more information, see `emptyDir <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#emptydir>`_ in the *Kubernetes documentation* .
            :param host_path: Specifies the configuration of a Kubernetes ``hostPath`` volume. For more information, see `hostPath <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#hostpath>`_ in the *Kubernetes documentation* .
            :param secret: Specifies the configuration of a Kubernetes ``secret`` volume. For more information, see `secret <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#secret>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                eks_volume_property = batch.CfnJobDefinition.EksVolumeProperty(
                    name="name",
                
                    # the properties below are optional
                    empty_dir=batch.CfnJobDefinition.EmptyDirProperty(
                        medium="medium",
                        size_limit="sizeLimit"
                    ),
                    host_path=batch.CfnJobDefinition.HostPathProperty(
                        path="path"
                    ),
                    secret=batch.CfnJobDefinition.EksSecretProperty(
                        secret_name="secretName",
                
                        # the properties below are optional
                        optional=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eae87049527466b1696763e1e45d7ec09d103e7024a3169413fb2ae04dd416f7)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument empty_dir", value=empty_dir, expected_type=type_hints["empty_dir"])
                check_type(argname="argument host_path", value=host_path, expected_type=type_hints["host_path"])
                check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if empty_dir is not None:
                self._values["empty_dir"] = empty_dir
            if host_path is not None:
                self._values["host_path"] = host_path
            if secret is not None:
                self._values["secret"] = secret

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the volume.

            The name must be allowed as a DNS subdomain name. For more information, see `DNS subdomain names <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-subdomain-names>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def empty_dir(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EmptyDirProperty"]]:
            '''Specifies the configuration of a Kubernetes ``emptyDir`` volume.

            For more information, see `emptyDir <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#emptydir>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-emptydir
            '''
            result = self._values.get("empty_dir")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EmptyDirProperty"]], result)

        @builtins.property
        def host_path(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.HostPathProperty"]]:
            '''Specifies the configuration of a Kubernetes ``hostPath`` volume.

            For more information, see `hostPath <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#hostpath>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-hostpath
            '''
            result = self._values.get("host_path")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.HostPathProperty"]], result)

        @builtins.property
        def secret(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksSecretProperty"]]:
            '''Specifies the configuration of a Kubernetes ``secret`` volume.

            For more information, see `secret <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/storage/volumes/#secret>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksvolume.html#cfn-batch-jobdefinition-eksvolume-secret
            '''
            result = self._values.get("secret")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksSecretProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EksVolumeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EmptyDirProperty",
        jsii_struct_bases=[],
        name_mapping={"medium": "medium", "size_limit": "sizeLimit"},
    )
    class EmptyDirProperty:
        def __init__(
            self,
            *,
            medium: typing.Optional[builtins.str] = None,
            size_limit: typing.Optional[builtins.str] = None,
        ) -> None:
            '''
            :param medium: ``CfnJobDefinition.EmptyDirProperty.Medium``.
            :param size_limit: ``CfnJobDefinition.EmptyDirProperty.SizeLimit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksemptydir.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                empty_dir_property = batch.CfnJobDefinition.EmptyDirProperty(
                    medium="medium",
                    size_limit="sizeLimit"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c8a07cc209d3d279842fe570b9d019970da5ec93fccc438f8af3d2f7cbb879f)
                check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
                check_type(argname="argument size_limit", value=size_limit, expected_type=type_hints["size_limit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if medium is not None:
                self._values["medium"] = medium
            if size_limit is not None:
                self._values["size_limit"] = size_limit

        @builtins.property
        def medium(self) -> typing.Optional[builtins.str]:
            '''``CfnJobDefinition.EmptyDirProperty.Medium``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksemptydir.html#cfn-batch-jobdefinition-eksemptydir-medium
            '''
            result = self._values.get("medium")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def size_limit(self) -> typing.Optional[builtins.str]:
            '''``CfnJobDefinition.EmptyDirProperty.SizeLimit``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-eksemptydir.html#cfn-batch-jobdefinition-eksemptydir-sizelimit
            '''
            result = self._values.get("size_limit")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EmptyDirProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EnvironmentProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The Environment property type specifies environment variables to use in a job definition.

            :param name: The name of the environment variable.
            :param value: The value of the environment variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                environment_property = batch.CfnJobDefinition.EnvironmentProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b35292326ef6167cd330db6c2deab88c160e3b1819b5bb6f6701ea805fb6478f)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the environment variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value of the environment variable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-environment.html#cfn-batch-jobdefinition-environment-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EphemeralStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"size_in_gib": "sizeInGiB"},
    )
    class EphemeralStorageProperty:
        def __init__(self, *, size_in_gib: jsii.Number) -> None:
            '''
            :param size_in_gib: ``CfnJobDefinition.EphemeralStorageProperty.SizeInGiB``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-ephemeralstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                ephemeral_storage_property = batch.CfnJobDefinition.EphemeralStorageProperty(
                    size_in_gi_b=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__971954cc156e97f6afe9dc7b1bb2f996b4209307a00baf0f98e9dbc4c48825c6)
                check_type(argname="argument size_in_gib", value=size_in_gib, expected_type=type_hints["size_in_gib"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "size_in_gib": size_in_gib,
            }

        @builtins.property
        def size_in_gib(self) -> jsii.Number:
            '''``CfnJobDefinition.EphemeralStorageProperty.SizeInGiB``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-ephemeralstorage.html#cfn-batch-jobdefinition-containerproperties-ephemeralstorage-sizeingib
            '''
            result = self._values.get("size_in_gib")
            assert result is not None, "Required property 'size_in_gib' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EphemeralStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.EvaluateOnExitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "on_exit_code": "onExitCode",
            "on_reason": "onReason",
            "on_status_reason": "onStatusReason",
        },
    )
    class EvaluateOnExitProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            on_exit_code: typing.Optional[builtins.str] = None,
            on_reason: typing.Optional[builtins.str] = None,
            on_status_reason: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an array of up to 5 conditions to be met, and an action to take ( ``RETRY`` or ``EXIT`` ) if all conditions are met.

            If none of the ``EvaluateOnExit`` conditions in a ``RetryStrategy`` match, then the job is retried.

            :param action: Specifies the action to take if all of the specified conditions ( ``onStatusReason`` , ``onReason`` , and ``onExitCode`` ) are met. The values aren't case sensitive.
            :param on_exit_code: Contains a glob pattern to match against the decimal representation of the ``ExitCode`` returned for a job. The pattern can be up to 512 characters long. It can contain only numbers, and can end with an asterisk (*) so that only the start of the string needs to be an exact match. The string can contain up to 512 characters.
            :param on_reason: Contains a glob pattern to match against the ``Reason`` returned for a job. The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white space (including spaces and tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.
            :param on_status_reason: Contains a glob pattern to match against the ``StatusReason`` returned for a job. The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white spaces (including spaces or tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                evaluate_on_exit_property = batch.CfnJobDefinition.EvaluateOnExitProperty(
                    action="action",
                
                    # the properties below are optional
                    on_exit_code="onExitCode",
                    on_reason="onReason",
                    on_status_reason="onStatusReason"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7e8e95b83645d5ca87bdedddfcb79d63524285a5b71dc7be8c3882493a745153)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument on_exit_code", value=on_exit_code, expected_type=type_hints["on_exit_code"])
                check_type(argname="argument on_reason", value=on_reason, expected_type=type_hints["on_reason"])
                check_type(argname="argument on_status_reason", value=on_status_reason, expected_type=type_hints["on_status_reason"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
            }
            if on_exit_code is not None:
                self._values["on_exit_code"] = on_exit_code
            if on_reason is not None:
                self._values["on_reason"] = on_reason
            if on_status_reason is not None:
                self._values["on_status_reason"] = on_status_reason

        @builtins.property
        def action(self) -> builtins.str:
            '''Specifies the action to take if all of the specified conditions ( ``onStatusReason`` , ``onReason`` , and ``onExitCode`` ) are met.

            The values aren't case sensitive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def on_exit_code(self) -> typing.Optional[builtins.str]:
            '''Contains a glob pattern to match against the decimal representation of the ``ExitCode`` returned for a job.

            The pattern can be up to 512 characters long. It can contain only numbers, and can end with an asterisk (*) so that only the start of the string needs to be an exact match.

            The string can contain up to 512 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onexitcode
            '''
            result = self._values.get("on_exit_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_reason(self) -> typing.Optional[builtins.str]:
            '''Contains a glob pattern to match against the ``Reason`` returned for a job.

            The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white space (including spaces and tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onreason
            '''
            result = self._values.get("on_reason")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def on_status_reason(self) -> typing.Optional[builtins.str]:
            '''Contains a glob pattern to match against the ``StatusReason`` returned for a job.

            The pattern can contain up to 512 characters. It can contain letters, numbers, periods (.), colons (:), and white spaces (including spaces or tabs). It can optionally end with an asterisk (*) so that only the start of the string needs to be an exact match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-evaluateonexit.html#cfn-batch-jobdefinition-evaluateonexit-onstatusreason
            '''
            result = self._values.get("on_status_reason")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EvaluateOnExitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.FargatePlatformConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"platform_version": "platformVersion"},
    )
    class FargatePlatformConfigurationProperty:
        def __init__(
            self,
            *,
            platform_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The platform configuration for jobs that are running on Fargate resources.

            Jobs that run on EC2 resources must not specify this parameter.

            :param platform_version: The AWS Fargate platform version where the jobs are running. A platform version is specified only for jobs that are running on Fargate resources. If one isn't specified, the ``LATEST`` platform version is used by default. This uses a recent, approved version of the AWS Fargate platform for compute resources. For more information, see `AWS Fargate platform versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-fargateplatformconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                fargate_platform_configuration_property = batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                    platform_version="platformVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79cf55719603ebb0ac170c1a33148643ba787476040be52aea0bce84c013d05f)
                check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if platform_version is not None:
                self._values["platform_version"] = platform_version

        @builtins.property
        def platform_version(self) -> typing.Optional[builtins.str]:
            '''The AWS Fargate platform version where the jobs are running.

            A platform version is specified only for jobs that are running on Fargate resources. If one isn't specified, the ``LATEST`` platform version is used by default. This uses a recent, approved version of the AWS Fargate platform for compute resources. For more information, see `AWS Fargate platform versions <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/platform_versions.html>`_ in the *Amazon Elastic Container Service Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-fargateplatformconfiguration.html#cfn-batch-jobdefinition-containerproperties-fargateplatformconfiguration-platformversion
            '''
            result = self._values.get("platform_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FargatePlatformConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.HostPathProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path"},
    )
    class HostPathProperty:
        def __init__(self, *, path: typing.Optional[builtins.str] = None) -> None:
            '''
            :param path: ``CfnJobDefinition.HostPathProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekshostpath.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                host_path_property = batch.CfnJobDefinition.HostPathProperty(
                    path="path"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0d46aaf98c27d80f22140cee98dfbee6e1fb9bd31f85be5de4ebd19cce173eb6)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if path is not None:
                self._values["path"] = path

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''``CfnJobDefinition.HostPathProperty.Path``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekshostpath.html#cfn-batch-jobdefinition-ekshostpath-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HostPathProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.LinuxParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "devices": "devices",
            "init_process_enabled": "initProcessEnabled",
            "max_swap": "maxSwap",
            "shared_memory_size": "sharedMemorySize",
            "swappiness": "swappiness",
            "tmpfs": "tmpfs",
        },
    )
    class LinuxParametersProperty:
        def __init__(
            self,
            *,
            devices: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.DeviceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            init_process_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            max_swap: typing.Optional[jsii.Number] = None,
            shared_memory_size: typing.Optional[jsii.Number] = None,
            swappiness: typing.Optional[jsii.Number] = None,
            tmpfs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.TmpfsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Linux-specific modifications that are applied to the container, such as details for device mappings.

            :param devices: Any of the host devices to expose to the container. This parameter maps to ``Devices`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--device`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param init_process_enabled: If true, run an ``init`` process inside the container that forwards signals and reaps processes. This parameter maps to the ``--init`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . This parameter requires version 1.25 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            :param max_swap: The total amount of swap memory (in MiB) a container can use. This parameter is translated to the ``--memory-swap`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ where the value is the sum of the container memory plus the ``maxSwap`` value. For more information, see ```--memory-swap`` details <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/resource_constraints/#--memory-swap-details>`_ in the Docker documentation. If a ``maxSwap`` value of ``0`` is specified, the container doesn't use swap. Accepted values are ``0`` or any positive integer. If the ``maxSwap`` parameter is omitted, the container doesn't use the swap configuration for the container instance that it's running on. A ``maxSwap`` value must be set for the ``swappiness`` parameter to be used. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param shared_memory_size: The value for the size (in MiB) of the ``/dev/shm`` volume. This parameter maps to the ``--shm-size`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param swappiness: You can use this parameter to tune a container's memory swappiness behavior. A ``swappiness`` value of ``0`` causes swapping to not occur unless absolutely necessary. A ``swappiness`` value of ``100`` causes pages to be swapped aggressively. Valid values are whole numbers between ``0`` and ``100`` . If the ``swappiness`` parameter isn't specified, a default value of ``60`` is used. If a value isn't specified for ``maxSwap`` , then this parameter is ignored. If ``maxSwap`` is set to 0, the container doesn't use swap. This parameter maps to the ``--memory-swappiness`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Consider the following when you use a per-container swap configuration. - Swap space must be enabled and allocated on the container instance for the containers to use. .. epigraph:: By default, the Amazon ECS optimized AMIs don't have swap enabled. You must enable swap on the instance to use this feature. For more information, see `Instance store swap volumes <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* or `How do I allocate memory to work as swap space in an Amazon EC2 instance by using a swap file? <https://docs.aws.amazon.com/premiumsupport/knowledge-center/ec2-memory-swap-file/>`_ - The swap space parameters are only supported for job definitions using EC2 resources. - If the ``maxSwap`` and ``swappiness`` parameters are omitted from a job definition, each container has a default ``swappiness`` value of 60. Moreover, the total swap usage is limited to two times the memory reservation of the container. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.
            :param tmpfs: The container path, mount options, and size (in MiB) of the ``tmpfs`` mount. This parameter maps to the ``--tmpfs`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide this parameter for this resource type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                linux_parameters_property = batch.CfnJobDefinition.LinuxParametersProperty(
                    devices=[batch.CfnJobDefinition.DeviceProperty(
                        container_path="containerPath",
                        host_path="hostPath",
                        permissions=["permissions"]
                    )],
                    init_process_enabled=False,
                    max_swap=123,
                    shared_memory_size=123,
                    swappiness=123,
                    tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                        container_path="containerPath",
                        size=123,
                
                        # the properties below are optional
                        mount_options=["mountOptions"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6518edf5760938a62889b149467428ec12ba500342066833b437008ff0b6db06)
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
                check_type(argname="argument init_process_enabled", value=init_process_enabled, expected_type=type_hints["init_process_enabled"])
                check_type(argname="argument max_swap", value=max_swap, expected_type=type_hints["max_swap"])
                check_type(argname="argument shared_memory_size", value=shared_memory_size, expected_type=type_hints["shared_memory_size"])
                check_type(argname="argument swappiness", value=swappiness, expected_type=type_hints["swappiness"])
                check_type(argname="argument tmpfs", value=tmpfs, expected_type=type_hints["tmpfs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if devices is not None:
                self._values["devices"] = devices
            if init_process_enabled is not None:
                self._values["init_process_enabled"] = init_process_enabled
            if max_swap is not None:
                self._values["max_swap"] = max_swap
            if shared_memory_size is not None:
                self._values["shared_memory_size"] = shared_memory_size
            if swappiness is not None:
                self._values["swappiness"] = swappiness
            if tmpfs is not None:
                self._values["tmpfs"] = tmpfs

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.DeviceProperty"]]]]:
            '''Any of the host devices to expose to the container.

            This parameter maps to ``Devices`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--device`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-devices
            '''
            result = self._values.get("devices")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.DeviceProperty"]]]], result)

        @builtins.property
        def init_process_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If true, run an ``init`` process inside the container that forwards signals and reaps processes.

            This parameter maps to the ``--init`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . This parameter requires version 1.25 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-initprocessenabled
            '''
            result = self._values.get("init_process_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def max_swap(self) -> typing.Optional[jsii.Number]:
            '''The total amount of swap memory (in MiB) a container can use.

            This parameter is translated to the ``--memory-swap`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ where the value is the sum of the container memory plus the ``maxSwap`` value. For more information, see ```--memory-swap`` details <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/resource_constraints/#--memory-swap-details>`_ in the Docker documentation.

            If a ``maxSwap`` value of ``0`` is specified, the container doesn't use swap. Accepted values are ``0`` or any positive integer. If the ``maxSwap`` parameter is omitted, the container doesn't use the swap configuration for the container instance that it's running on. A ``maxSwap`` value must be set for the ``swappiness`` parameter to be used.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-maxswap
            '''
            result = self._values.get("max_swap")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def shared_memory_size(self) -> typing.Optional[jsii.Number]:
            '''The value for the size (in MiB) of the ``/dev/shm`` volume.

            This parameter maps to the ``--shm-size`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-sharedmemorysize
            '''
            result = self._values.get("shared_memory_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def swappiness(self) -> typing.Optional[jsii.Number]:
            '''You can use this parameter to tune a container's memory swappiness behavior.

            A ``swappiness`` value of ``0`` causes swapping to not occur unless absolutely necessary. A ``swappiness`` value of ``100`` causes pages to be swapped aggressively. Valid values are whole numbers between ``0`` and ``100`` . If the ``swappiness`` parameter isn't specified, a default value of ``60`` is used. If a value isn't specified for ``maxSwap`` , then this parameter is ignored. If ``maxSwap`` is set to 0, the container doesn't use swap. This parameter maps to the ``--memory-swappiness`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            Consider the following when you use a per-container swap configuration.

            - Swap space must be enabled and allocated on the container instance for the containers to use.

            .. epigraph::

               By default, the Amazon ECS optimized AMIs don't have swap enabled. You must enable swap on the instance to use this feature. For more information, see `Instance store swap volumes <https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-store-swap-volumes.html>`_ in the *Amazon EC2 User Guide for Linux Instances* or `How do I allocate memory to work as swap space in an Amazon EC2 instance by using a swap file? <https://docs.aws.amazon.com/premiumsupport/knowledge-center/ec2-memory-swap-file/>`_

            - The swap space parameters are only supported for job definitions using EC2 resources.
            - If the ``maxSwap`` and ``swappiness`` parameters are omitted from a job definition, each container has a default ``swappiness`` value of 60. Moreover, the total swap usage is limited to two times the memory reservation of the container.

            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide it for these jobs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-swappiness
            '''
            result = self._values.get("swappiness")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def tmpfs(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.TmpfsProperty"]]]]:
            '''The container path, mount options, and size (in MiB) of the ``tmpfs`` mount.

            This parameter maps to the ``--tmpfs`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources. Don't provide this parameter for this resource type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-linuxparameters.html#cfn-batch-jobdefinition-containerproperties-linuxparameters-tmpfs
            '''
            result = self._values.get("tmpfs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.TmpfsProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LinuxParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.LogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_driver": "logDriver",
            "options": "options",
            "secret_options": "secretOptions",
        },
    )
    class LogConfigurationProperty:
        def __init__(
            self,
            *,
            log_driver: builtins.str,
            options: typing.Any = None,
            secret_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.SecretProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Log configuration options to send to a custom log driver for the container.

            :param log_driver: The log driver to use for the container. The valid values that are listed for this parameter are log drivers that the Amazon ECS container agent can communicate with by default. The supported log drivers are ``awslogs`` , ``fluentd`` , ``gelf`` , ``json-file`` , ``journald`` , ``logentries`` , ``syslog`` , and ``splunk`` . .. epigraph:: Jobs that are running on Fargate resources are restricted to the ``awslogs`` and ``splunk`` log drivers. - **awslogs** - Specifies the Amazon CloudWatch Logs logging driver. For more information, see `Using the awslogs log driver <https://docs.aws.amazon.com/batch/latest/userguide/using_awslogs.html>`_ in the *AWS Batch User Guide* and `Amazon CloudWatch Logs logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/awslogs/>`_ in the Docker documentation. - **fluentd** - Specifies the Fluentd logging driver. For more information including usage and options, see `Fluentd logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/fluentd/>`_ in the *Docker documentation* . - **gelf** - Specifies the Graylog Extended Format (GELF) logging driver. For more information including usage and options, see `Graylog Extended Format logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/gelf/>`_ in the *Docker documentation* . - **journald** - Specifies the journald logging driver. For more information including usage and options, see `Journald logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/journald/>`_ in the *Docker documentation* . - **json-file** - Specifies the JSON file logging driver. For more information including usage and options, see `JSON File logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/json-file/>`_ in the *Docker documentation* . - **splunk** - Specifies the Splunk logging driver. For more information including usage and options, see `Splunk logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/splunk/>`_ in the *Docker documentation* . - **syslog** - Specifies the syslog logging driver. For more information including usage and options, see `Syslog logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/syslog/>`_ in the *Docker documentation* . .. epigraph:: If you have a custom driver that's not listed earlier that you want to work with the Amazon ECS container agent, you can fork the Amazon ECS container agent project that's `available on GitHub <https://docs.aws.amazon.com/https://github.com/aws/amazon-ecs-agent>`_ and customize it to work with that driver. We encourage you to submit pull requests for changes that you want to have included. However, Amazon Web Services doesn't currently support running modified copies of this software. This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            :param options: The configuration options to send to the log driver. This parameter requires version 1.19 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``
            :param secret_options: The secrets to pass to the log configuration. For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # options: Any
                
                log_configuration_property = batch.CfnJobDefinition.LogConfigurationProperty(
                    log_driver="logDriver",
                
                    # the properties below are optional
                    options=options,
                    secret_options=[batch.CfnJobDefinition.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d14a86920d47896d42fc0ded7f8a8908d69ffbbbeff807e371d96f6dd4425a8c)
                check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
                check_type(argname="argument options", value=options, expected_type=type_hints["options"])
                check_type(argname="argument secret_options", value=secret_options, expected_type=type_hints["secret_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_driver": log_driver,
            }
            if options is not None:
                self._values["options"] = options
            if secret_options is not None:
                self._values["secret_options"] = secret_options

        @builtins.property
        def log_driver(self) -> builtins.str:
            '''The log driver to use for the container.

            The valid values that are listed for this parameter are log drivers that the Amazon ECS container agent can communicate with by default.

            The supported log drivers are ``awslogs`` , ``fluentd`` , ``gelf`` , ``json-file`` , ``journald`` , ``logentries`` , ``syslog`` , and ``splunk`` .
            .. epigraph::

               Jobs that are running on Fargate resources are restricted to the ``awslogs`` and ``splunk`` log drivers.

            - **awslogs** - Specifies the Amazon CloudWatch Logs logging driver. For more information, see `Using the awslogs log driver <https://docs.aws.amazon.com/batch/latest/userguide/using_awslogs.html>`_ in the *AWS Batch User Guide* and `Amazon CloudWatch Logs logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/awslogs/>`_ in the Docker documentation.
            - **fluentd** - Specifies the Fluentd logging driver. For more information including usage and options, see `Fluentd logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/fluentd/>`_ in the *Docker documentation* .
            - **gelf** - Specifies the Graylog Extended Format (GELF) logging driver. For more information including usage and options, see `Graylog Extended Format logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/gelf/>`_ in the *Docker documentation* .
            - **journald** - Specifies the journald logging driver. For more information including usage and options, see `Journald logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/journald/>`_ in the *Docker documentation* .
            - **json-file** - Specifies the JSON file logging driver. For more information including usage and options, see `JSON File logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/json-file/>`_ in the *Docker documentation* .
            - **splunk** - Specifies the Splunk logging driver. For more information including usage and options, see `Splunk logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/splunk/>`_ in the *Docker documentation* .
            - **syslog** - Specifies the syslog logging driver. For more information including usage and options, see `Syslog logging driver <https://docs.aws.amazon.com/https://docs.docker.com/config/containers/logging/syslog/>`_ in the *Docker documentation* .

            .. epigraph::

               If you have a custom driver that's not listed earlier that you want to work with the Amazon ECS container agent, you can fork the Amazon ECS container agent project that's `available on GitHub <https://docs.aws.amazon.com/https://github.com/aws/amazon-ecs-agent>`_ and customize it to work with that driver. We encourage you to submit pull requests for changes that you want to have included. However, Amazon Web Services doesn't currently support running modified copies of this software.

            This parameter requires version 1.18 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html#cfn-batch-jobdefinition-containerproperties-logconfiguration-logdriver
            '''
            result = self._values.get("log_driver")
            assert result is not None, "Required property 'log_driver' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def options(self) -> typing.Any:
            '''The configuration options to send to the log driver.

            This parameter requires version 1.19 of the Docker Remote API or greater on your container instance. To check the Docker Remote API version on your container instance, log in to your container instance and run the following command: ``sudo docker version | grep "Server API version"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html#cfn-batch-jobdefinition-containerproperties-logconfiguration-options
            '''
            result = self._values.get("options")
            return typing.cast(typing.Any, result)

        @builtins.property
        def secret_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.SecretProperty"]]]]:
            '''The secrets to pass to the log configuration.

            For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-logconfiguration.html#cfn-batch-jobdefinition-containerproperties-logconfiguration-secretoptions
            '''
            result = self._values.get("secret_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.SecretProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.MetadataProperty",
        jsii_struct_bases=[],
        name_mapping={"labels": "labels"},
    )
    class MetadataProperty:
        def __init__(self, *, labels: typing.Any = None) -> None:
            '''
            :param labels: ``CfnJobDefinition.MetadataProperty.Labels``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties-metadata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # labels: Any
                
                metadata_property = batch.CfnJobDefinition.MetadataProperty(
                    labels=labels
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__31621d3ff7016700af15f9c5ff125711ef60901884dc470945d8f4f839861aff)
                check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if labels is not None:
                self._values["labels"] = labels

        @builtins.property
        def labels(self) -> typing.Any:
            '''``CfnJobDefinition.MetadataProperty.Labels``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties-metadata.html#cfn-batch-jobdefinition-podproperties-metadata-labels
            '''
            result = self._values.get("labels")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MetadataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.MountPointsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "read_only": "readOnly",
            "source_volume": "sourceVolume",
        },
    )
    class MountPointsProperty:
        def __init__(
            self,
            *,
            container_path: typing.Optional[builtins.str] = None,
            read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            source_volume: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Details for a Docker volume mount point that's used in a job's container properties.

            This parameter maps to ``Volumes`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/api/docker_remote_api_v1.19/#create-a-container>`_ section of the *Docker Remote API* and the ``--volume`` option to docker run.

            :param container_path: The path on the container where the host volume is mounted.
            :param read_only: If this value is ``true`` , the container has read-only access to the volume. Otherwise, the container can write to the volume. The default value is ``false`` .
            :param source_volume: The name of the volume to mount.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                mount_points_property = batch.CfnJobDefinition.MountPointsProperty(
                    container_path="containerPath",
                    read_only=False,
                    source_volume="sourceVolume"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4c079302185b99b4fa3cd459368854d06d0d90ee703847212f02b6b7733b03c4)
                check_type(argname="argument container_path", value=container_path, expected_type=type_hints["container_path"])
                check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
                check_type(argname="argument source_volume", value=source_volume, expected_type=type_hints["source_volume"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_path is not None:
                self._values["container_path"] = container_path
            if read_only is not None:
                self._values["read_only"] = read_only
            if source_volume is not None:
                self._values["source_volume"] = source_volume

        @builtins.property
        def container_path(self) -> typing.Optional[builtins.str]:
            '''The path on the container where the host volume is mounted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-containerpath
            '''
            result = self._values.get("container_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def read_only(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If this value is ``true`` , the container has read-only access to the volume.

            Otherwise, the container can write to the volume. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-readonly
            '''
            result = self._values.get("read_only")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def source_volume(self) -> typing.Optional[builtins.str]:
            '''The name of the volume to mount.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-mountpoints.html#cfn-batch-jobdefinition-mountpoints-sourcevolume
            '''
            result = self._values.get("source_volume")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MountPointsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"assign_public_ip": "assignPublicIp"},
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            assign_public_ip: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The network configuration for jobs that are running on Fargate resources.

            Jobs that are running on EC2 resources must not specify this parameter.

            :param assign_public_ip: Indicates whether the job has a public IP address. For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet. For more information, see `Amazon ECS task networking <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html>`_ in the *Amazon Elastic Container Service Developer Guide* . The default value is " ``DISABLED`` ".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                network_configuration_property = batch.CfnJobDefinition.NetworkConfigurationProperty(
                    assign_public_ip="assignPublicIp"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__157c880493ccc742e54423b3430b89dd94c48c69fa5e070b6a961bf0342da08c)
                check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assign_public_ip is not None:
                self._values["assign_public_ip"] = assign_public_ip

        @builtins.property
        def assign_public_ip(self) -> typing.Optional[builtins.str]:
            '''Indicates whether the job has a public IP address.

            For a job that's running on Fargate resources in a private subnet to send outbound traffic to the internet (for example, to pull container images), the private subnet requires a NAT gateway be attached to route requests to the internet. For more information, see `Amazon ECS task networking <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-networking.html>`_ in the *Amazon Elastic Container Service Developer Guide* . The default value is " ``DISABLED`` ".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-containerproperties-networkconfiguration.html#cfn-batch-jobdefinition-containerproperties-networkconfiguration-assignpublicip
            '''
            result = self._values.get("assign_public_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodePropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "main_node": "mainNode",
            "node_range_properties": "nodeRangeProperties",
            "num_nodes": "numNodes",
        },
    )
    class NodePropertiesProperty:
        def __init__(
            self,
            *,
            main_node: jsii.Number,
            node_range_properties: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.NodeRangePropertyProperty", typing.Dict[builtins.str, typing.Any]]]]],
            num_nodes: jsii.Number,
        ) -> None:
            '''An object that represents the node properties of a multi-node parallel job.

            .. epigraph::

               Node properties can't be specified for Amazon EKS based job definitions.

            :param main_node: Specifies the node index for the main node of a multi-node parallel job. This node index value must be fewer than the number of nodes.
            :param node_range_properties: A list of node ranges and their properties that are associated with a multi-node parallel job.
            :param num_nodes: The number of nodes that are associated with a multi-node parallel job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # options: Any
                
                node_properties_property = batch.CfnJobDefinition.NodePropertiesProperty(
                    main_node=123,
                    node_range_properties=[batch.CfnJobDefinition.NodeRangePropertyProperty(
                        target_nodes="targetNodes",
                
                        # the properties below are optional
                        container=batch.CfnJobDefinition.ContainerPropertiesProperty(
                            image="image",
                
                            # the properties below are optional
                            command=["command"],
                            environment=[batch.CfnJobDefinition.EnvironmentProperty(
                                name="name",
                                value="value"
                            )],
                            ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                                size_in_gi_b=123
                            ),
                            execution_role_arn="executionRoleArn",
                            fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                                platform_version="platformVersion"
                            ),
                            instance_type="instanceType",
                            job_role_arn="jobRoleArn",
                            linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                                devices=[batch.CfnJobDefinition.DeviceProperty(
                                    container_path="containerPath",
                                    host_path="hostPath",
                                    permissions=["permissions"]
                                )],
                                init_process_enabled=False,
                                max_swap=123,
                                shared_memory_size=123,
                                swappiness=123,
                                tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                                    container_path="containerPath",
                                    size=123,
                
                                    # the properties below are optional
                                    mount_options=["mountOptions"]
                                )]
                            ),
                            log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                                log_driver="logDriver",
                
                                # the properties below are optional
                                options=options,
                                secret_options=[batch.CfnJobDefinition.SecretProperty(
                                    name="name",
                                    value_from="valueFrom"
                                )]
                            ),
                            memory=123,
                            mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                                container_path="containerPath",
                                read_only=False,
                                source_volume="sourceVolume"
                            )],
                            network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                                assign_public_ip="assignPublicIp"
                            ),
                            privileged=False,
                            readonly_root_filesystem=False,
                            resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                                type="type",
                                value="value"
                            )],
                            secrets=[batch.CfnJobDefinition.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )],
                            ulimits=[batch.CfnJobDefinition.UlimitProperty(
                                hard_limit=123,
                                name="name",
                                soft_limit=123
                            )],
                            user="user",
                            vcpus=123,
                            volumes=[batch.CfnJobDefinition.VolumesProperty(
                                efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                                    file_system_id="fileSystemId",
                
                                    # the properties below are optional
                                    authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                                        access_point_id="accessPointId",
                                        iam="iam"
                                    ),
                                    root_directory="rootDirectory",
                                    transit_encryption="transitEncryption",
                                    transit_encryption_port=123
                                ),
                                host=batch.CfnJobDefinition.VolumesHostProperty(
                                    source_path="sourcePath"
                                ),
                                name="name"
                            )]
                        )
                    )],
                    num_nodes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__afd3eb2cc497ae286475a2cb668997daea0e7618383362d61443f39093012a55)
                check_type(argname="argument main_node", value=main_node, expected_type=type_hints["main_node"])
                check_type(argname="argument node_range_properties", value=node_range_properties, expected_type=type_hints["node_range_properties"])
                check_type(argname="argument num_nodes", value=num_nodes, expected_type=type_hints["num_nodes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "main_node": main_node,
                "node_range_properties": node_range_properties,
                "num_nodes": num_nodes,
            }

        @builtins.property
        def main_node(self) -> jsii.Number:
            '''Specifies the node index for the main node of a multi-node parallel job.

            This node index value must be fewer than the number of nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-mainnode
            '''
            result = self._values.get("main_node")
            assert result is not None, "Required property 'main_node' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def node_range_properties(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NodeRangePropertyProperty"]]]:
            '''A list of node ranges and their properties that are associated with a multi-node parallel job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-noderangeproperties
            '''
            result = self._values.get("node_range_properties")
            assert result is not None, "Required property 'node_range_properties' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.NodeRangePropertyProperty"]]], result)

        @builtins.property
        def num_nodes(self) -> jsii.Number:
            '''The number of nodes that are associated with a multi-node parallel job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-nodeproperties.html#cfn-batch-jobdefinition-nodeproperties-numnodes
            '''
            result = self._values.get("num_nodes")
            assert result is not None, "Required property 'num_nodes' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodePropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.NodeRangePropertyProperty",
        jsii_struct_bases=[],
        name_mapping={"target_nodes": "targetNodes", "container": "container"},
    )
    class NodeRangePropertyProperty:
        def __init__(
            self,
            *,
            target_nodes: builtins.str,
            container: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.ContainerPropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An object that represents the properties of the node range for a multi-node parallel job.

            :param target_nodes: The range of nodes, using node index values. A range of ``0:3`` indicates nodes with index values of ``0`` through ``3`` . If the starting range value is omitted ( ``:n`` ), then ``0`` is used to start the range. If the ending range value is omitted ( ``n:`` ), then the highest possible node index is used to end the range. Your accumulative node ranges must account for all nodes ( ``0:n`` ). You can nest node ranges (for example, ``0:10`` and ``4:5`` ). In this case, the ``4:5`` range properties override the ``0:10`` properties.
            :param container: The container details for the node range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # options: Any
                
                node_range_property_property = batch.CfnJobDefinition.NodeRangePropertyProperty(
                    target_nodes="targetNodes",
                
                    # the properties below are optional
                    container=batch.CfnJobDefinition.ContainerPropertiesProperty(
                        image="image",
                
                        # the properties below are optional
                        command=["command"],
                        environment=[batch.CfnJobDefinition.EnvironmentProperty(
                            name="name",
                            value="value"
                        )],
                        ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                            size_in_gi_b=123
                        ),
                        execution_role_arn="executionRoleArn",
                        fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                            platform_version="platformVersion"
                        ),
                        instance_type="instanceType",
                        job_role_arn="jobRoleArn",
                        linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                            devices=[batch.CfnJobDefinition.DeviceProperty(
                                container_path="containerPath",
                                host_path="hostPath",
                                permissions=["permissions"]
                            )],
                            init_process_enabled=False,
                            max_swap=123,
                            shared_memory_size=123,
                            swappiness=123,
                            tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                                container_path="containerPath",
                                size=123,
                
                                # the properties below are optional
                                mount_options=["mountOptions"]
                            )]
                        ),
                        log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                            log_driver="logDriver",
                
                            # the properties below are optional
                            options=options,
                            secret_options=[batch.CfnJobDefinition.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )]
                        ),
                        memory=123,
                        mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                            container_path="containerPath",
                            read_only=False,
                            source_volume="sourceVolume"
                        )],
                        network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                            assign_public_ip="assignPublicIp"
                        ),
                        privileged=False,
                        readonly_root_filesystem=False,
                        resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                            type="type",
                            value="value"
                        )],
                        secrets=[batch.CfnJobDefinition.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )],
                        ulimits=[batch.CfnJobDefinition.UlimitProperty(
                            hard_limit=123,
                            name="name",
                            soft_limit=123
                        )],
                        user="user",
                        vcpus=123,
                        volumes=[batch.CfnJobDefinition.VolumesProperty(
                            efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                                file_system_id="fileSystemId",
                
                                # the properties below are optional
                                authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                                    access_point_id="accessPointId",
                                    iam="iam"
                                ),
                                root_directory="rootDirectory",
                                transit_encryption="transitEncryption",
                                transit_encryption_port=123
                            ),
                            host=batch.CfnJobDefinition.VolumesHostProperty(
                                source_path="sourcePath"
                            ),
                            name="name"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c3d1407f741b2c7cb684b73fd954f9df2434b5c6382c0dc6a1939f4ff3bbe6d)
                check_type(argname="argument target_nodes", value=target_nodes, expected_type=type_hints["target_nodes"])
                check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_nodes": target_nodes,
            }
            if container is not None:
                self._values["container"] = container

        @builtins.property
        def target_nodes(self) -> builtins.str:
            '''The range of nodes, using node index values.

            A range of ``0:3`` indicates nodes with index values of ``0`` through ``3`` . If the starting range value is omitted ( ``:n`` ), then ``0`` is used to start the range. If the ending range value is omitted ( ``n:`` ), then the highest possible node index is used to end the range. Your accumulative node ranges must account for all nodes ( ``0:n`` ). You can nest node ranges (for example, ``0:10`` and ``4:5`` ). In this case, the ``4:5`` range properties override the ``0:10`` properties.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-targetnodes
            '''
            result = self._values.get("target_nodes")
            assert result is not None, "Required property 'target_nodes' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def container(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]]:
            '''The container details for the node range.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-noderangeproperty.html#cfn-batch-jobdefinition-noderangeproperty-container
            '''
            result = self._values.get("container")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.ContainerPropertiesProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeRangePropertyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.PodPropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "containers": "containers",
            "dns_policy": "dnsPolicy",
            "host_network": "hostNetwork",
            "metadata": "metadata",
            "service_account_name": "serviceAccountName",
            "volumes": "volumes",
        },
    )
    class PodPropertiesProperty:
        def __init__(
            self,
            *,
            containers: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EksContainerProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            dns_policy: typing.Optional[builtins.str] = None,
            host_network: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.MetadataProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            service_account_name: typing.Optional[builtins.str] = None,
            volumes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EksVolumeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The properties for the pod.

            :param containers: The properties of the container that's used on the Amazon EKS pod.
            :param dns_policy: The DNS policy for the pod. The default value is ``ClusterFirst`` . If the ``hostNetwork`` parameter is not specified, the default is ``ClusterFirstWithHostNet`` . ``ClusterFirst`` indicates that any DNS query that does not match the configured cluster domain suffix is forwarded to the upstream nameserver inherited from the node. If no value was specified for ``dnsPolicy`` in the `RegisterJobDefinition <https://docs.aws.amazon.com/batch/latest/APIReference/API_RegisterJobDefinition.html>`_ API operation, then no value will be returned for ``dnsPolicy`` by either of `DescribeJobDefinitions <https://docs.aws.amazon.com/batch/latest/APIReference/API_DescribeJobDefinitions.html>`_ or `DescribeJobs <https://docs.aws.amazon.com/batch/latest/APIReference/API_DescribeJobs.html>`_ API operations. The pod spec setting will contain either ``ClusterFirst`` or ``ClusterFirstWithHostNet`` , depending on the value of the ``hostNetwork`` parameter. For more information, see `Pod's DNS policy <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy>`_ in the *Kubernetes documentation* . Valid values: ``Default`` | ``ClusterFirst`` | ``ClusterFirstWithHostNet``
            :param host_network: Indicates if the pod uses the hosts' network IP address. The default value is ``true`` . Setting this to ``false`` enables the Kubernetes pod networking model. Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections. For more information, see `Host namespaces <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/security/pod-security-policy/#host-namespaces>`_ and `Pod networking <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking>`_ in the *Kubernetes documentation* .
            :param metadata: ``CfnJobDefinition.PodPropertiesProperty.Metadata``.
            :param service_account_name: The name of the service account that's used to run the pod. For more information, see `Kubernetes service accounts <https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html>`_ and `Configure a Kubernetes service account to assume an IAM role <https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html>`_ in the *Amazon EKS User Guide* and `Configure service accounts for pods <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/>`_ in the *Kubernetes documentation* .
            :param volumes: Specifies the volumes for a job definition that uses Amazon EKS resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # labels: Any
                # limits: Any
                # requests: Any
                
                pod_properties_property = batch.CfnJobDefinition.PodPropertiesProperty(
                    containers=[batch.CfnJobDefinition.EksContainerProperty(
                        image="image",
                
                        # the properties below are optional
                        args=["args"],
                        command=["command"],
                        env=[batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty(
                            name="name",
                
                            # the properties below are optional
                            value="value"
                        )],
                        image_pull_policy="imagePullPolicy",
                        name="name",
                        resources=batch.CfnJobDefinition.ResourcesProperty(
                            limits=limits,
                            requests=requests
                        ),
                        security_context=batch.CfnJobDefinition.SecurityContextProperty(
                            privileged=False,
                            read_only_root_filesystem=False,
                            run_as_group=123,
                            run_as_non_root=False,
                            run_as_user=123
                        ),
                        volume_mounts=[batch.CfnJobDefinition.EksContainerVolumeMountProperty(
                            mount_path="mountPath",
                            name="name",
                            read_only=False
                        )]
                    )],
                    dns_policy="dnsPolicy",
                    host_network=False,
                    metadata=batch.CfnJobDefinition.MetadataProperty(
                        labels=labels
                    ),
                    service_account_name="serviceAccountName",
                    volumes=[batch.CfnJobDefinition.EksVolumeProperty(
                        name="name",
                
                        # the properties below are optional
                        empty_dir=batch.CfnJobDefinition.EmptyDirProperty(
                            medium="medium",
                            size_limit="sizeLimit"
                        ),
                        host_path=batch.CfnJobDefinition.HostPathProperty(
                            path="path"
                        ),
                        secret=batch.CfnJobDefinition.EksSecretProperty(
                            secret_name="secretName",
                
                            # the properties below are optional
                            optional=False
                        )
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfc82a59dd1f31175037081efef47fcd96e8a6831b408bdc5dbbff446e85c77a)
                check_type(argname="argument containers", value=containers, expected_type=type_hints["containers"])
                check_type(argname="argument dns_policy", value=dns_policy, expected_type=type_hints["dns_policy"])
                check_type(argname="argument host_network", value=host_network, expected_type=type_hints["host_network"])
                check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
                check_type(argname="argument service_account_name", value=service_account_name, expected_type=type_hints["service_account_name"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if containers is not None:
                self._values["containers"] = containers
            if dns_policy is not None:
                self._values["dns_policy"] = dns_policy
            if host_network is not None:
                self._values["host_network"] = host_network
            if metadata is not None:
                self._values["metadata"] = metadata
            if service_account_name is not None:
                self._values["service_account_name"] = service_account_name
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def containers(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksContainerProperty"]]]]:
            '''The properties of the container that's used on the Amazon EKS pod.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-containers
            '''
            result = self._values.get("containers")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksContainerProperty"]]]], result)

        @builtins.property
        def dns_policy(self) -> typing.Optional[builtins.str]:
            '''The DNS policy for the pod.

            The default value is ``ClusterFirst`` . If the ``hostNetwork`` parameter is not specified, the default is ``ClusterFirstWithHostNet`` . ``ClusterFirst`` indicates that any DNS query that does not match the configured cluster domain suffix is forwarded to the upstream nameserver inherited from the node. If no value was specified for ``dnsPolicy`` in the `RegisterJobDefinition <https://docs.aws.amazon.com/batch/latest/APIReference/API_RegisterJobDefinition.html>`_ API operation, then no value will be returned for ``dnsPolicy`` by either of `DescribeJobDefinitions <https://docs.aws.amazon.com/batch/latest/APIReference/API_DescribeJobDefinitions.html>`_ or `DescribeJobs <https://docs.aws.amazon.com/batch/latest/APIReference/API_DescribeJobs.html>`_ API operations. The pod spec setting will contain either ``ClusterFirst`` or ``ClusterFirstWithHostNet`` , depending on the value of the ``hostNetwork`` parameter. For more information, see `Pod's DNS policy <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/#pod-s-dns-policy>`_ in the *Kubernetes documentation* .

            Valid values: ``Default`` | ``ClusterFirst`` | ``ClusterFirstWithHostNet``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-dnspolicy
            '''
            result = self._values.get("dns_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def host_network(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates if the pod uses the hosts' network IP address.

            The default value is ``true`` . Setting this to ``false`` enables the Kubernetes pod networking model. Most AWS Batch workloads are egress-only and don't require the overhead of IP allocation for each pod for incoming connections. For more information, see `Host namespaces <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/security/pod-security-policy/#host-namespaces>`_ and `Pod networking <https://docs.aws.amazon.com/https://kubernetes.io/docs/concepts/workloads/pods/#pod-networking>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-hostnetwork
            '''
            result = self._values.get("host_network")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def metadata(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.MetadataProperty"]]:
            '''``CfnJobDefinition.PodPropertiesProperty.Metadata``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-metadata
            '''
            result = self._values.get("metadata")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.MetadataProperty"]], result)

        @builtins.property
        def service_account_name(self) -> typing.Optional[builtins.str]:
            '''The name of the service account that's used to run the pod.

            For more information, see `Kubernetes service accounts <https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html>`_ and `Configure a Kubernetes service account to assume an IAM role <https://docs.aws.amazon.com/eks/latest/userguide/associate-service-account-role.html>`_ in the *Amazon EKS User Guide* and `Configure service accounts for pods <https://docs.aws.amazon.com/https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/>`_ in the *Kubernetes documentation* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-serviceaccountname
            '''
            result = self._values.get("service_account_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksVolumeProperty"]]]]:
            '''Specifies the volumes for a job definition that uses Amazon EKS resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-podproperties.html#cfn-batch-jobdefinition-podproperties-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EksVolumeProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PodPropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ResourceRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={"type": "type", "value": "value"},
    )
    class ResourceRequirementProperty:
        def __init__(
            self,
            *,
            type: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The type and amount of a resource to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :param type: The type of resource to assign to a container. The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .
            :param value: The quantity of the specified resource to reserve for the container. The values vary based on the ``type`` specified. - **type="GPU"** - The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on. .. epigraph:: GPUs aren't available for jobs that are running on Fargate resources. - **type="MEMORY"** - The memory hard limit (in MiB) present to the container. This parameter is supported for jobs that are running on EC2 resources. If your container attempts to exceed the memory specified, the container is terminated. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . You must specify at least 4 MiB of memory for a job. This is required but can be specified in several places for multi-node parallel (MNP) jobs. It must be specified for each node at least once. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . .. epigraph:: If you're trying to maximize your resource utilization by providing your jobs as much memory as possible for a particular instance type, see `Memory management <https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html>`_ in the *AWS Batch User Guide* . For jobs that are running on Fargate resources, then ``value`` is the hard limit (in MiB), and must match one of the supported values and the ``VCPU`` values must be one of the values supported for that memory value. - **value = 512** - ``VCPU`` = 0.25 - **value = 1024** - ``VCPU`` = 0.25 or 0.5 - **value = 2048** - ``VCPU`` = 0.25, 0.5, or 1 - **value = 3072** - ``VCPU`` = 0.5, or 1 - **value = 4096** - ``VCPU`` = 0.5, 1, or 2 - **value = 5120, 6144, or 7168** - ``VCPU`` = 1 or 2 - **value = 8192** - ``VCPU`` = 1, 2, or 4 - **value = 9216, 10240, 11264, 12288, 13312, 14336, or 15360** - ``VCPU`` = 2 or 4 - **value = 16384** - ``VCPU`` = 2, 4, or 8 - **value = 17408, 18432, 19456, 21504, 22528, 23552, 25600, 26624, 27648, 29696, or 30720** - ``VCPU`` = 4 - **value = 20480, 24576, or 28672** - ``VCPU`` = 4 or 8 - **value = 36864, 45056, 53248, or 61440** - ``VCPU`` = 8 - **value = 32768, 40960, 49152, or 57344** - ``VCPU`` = 8 or 16 - **value = 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880** - ``VCPU`` = 16 - **type="VCPU"** - The number of vCPUs reserved for the container. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Each vCPU is equivalent to 1,024 CPU shares. For EC2 resources, you must specify at least one vCPU. This is required but can be specified in several places; it must be specified for each node at least once. The default for the Fargate On-Demand vCPU resource count quota is 6 vCPUs. For more information about Fargate quotas, see `AWS Fargate quotas <https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#service-quotas-fargate>`_ in the *AWS General Reference* . For jobs that are running on Fargate resources, then ``value`` must match one of the supported values and the ``MEMORY`` values must be one of the values supported for that ``VCPU`` value. The supported values are 0.25, 0.5, 1, 2, 4, 8, and 16 - **value = 0.25** - ``MEMORY`` = 512, 1024, or 2048 - **value = 0.5** - ``MEMORY`` = 1024, 2048, 3072, or 4096 - **value = 1** - ``MEMORY`` = 2048, 3072, 4096, 5120, 6144, 7168, or 8192 - **value = 2** - ``MEMORY`` = 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, or 16384 - **value = 4** - ``MEMORY`` = 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, or 30720 - **value = 8** - ``MEMORY`` = 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, or 61440 - **value = 16** - ``MEMORY`` = 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                resource_requirement_property = batch.CfnJobDefinition.ResourceRequirementProperty(
                    type="type",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e1631be66b62756fc44ffe485df78aa9ef2d0179130d5762da3d7c8fedbb1d3c)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if type is not None:
                self._values["type"] = type
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of resource to assign to a container.

            The supported resources include ``GPU`` , ``MEMORY`` , and ``VCPU`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The quantity of the specified resource to reserve for the container. The values vary based on the ``type`` specified.

            - **type="GPU"** - The number of physical GPUs to reserve for the container. Make sure that the number of GPUs reserved for all containers in a job doesn't exceed the number of available GPUs on the compute resource that the job is launched on.

            .. epigraph::

               GPUs aren't available for jobs that are running on Fargate resources.

            - **type="MEMORY"** - The memory hard limit (in MiB) present to the container. This parameter is supported for jobs that are running on EC2 resources. If your container attempts to exceed the memory specified, the container is terminated. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . You must specify at least 4 MiB of memory for a job. This is required but can be specified in several places for multi-node parallel (MNP) jobs. It must be specified for each node at least once. This parameter maps to ``Memory`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--memory`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ .

            .. epigraph::

               If you're trying to maximize your resource utilization by providing your jobs as much memory as possible for a particular instance type, see `Memory management <https://docs.aws.amazon.com/batch/latest/userguide/memory-management.html>`_ in the *AWS Batch User Guide* .

            For jobs that are running on Fargate resources, then ``value`` is the hard limit (in MiB), and must match one of the supported values and the ``VCPU`` values must be one of the values supported for that memory value.

            - **value = 512** - ``VCPU`` = 0.25
            - **value = 1024** - ``VCPU`` = 0.25 or 0.5
            - **value = 2048** - ``VCPU`` = 0.25, 0.5, or 1
            - **value = 3072** - ``VCPU`` = 0.5, or 1
            - **value = 4096** - ``VCPU`` = 0.5, 1, or 2
            - **value = 5120, 6144, or 7168** - ``VCPU`` = 1 or 2
            - **value = 8192** - ``VCPU`` = 1, 2, or 4
            - **value = 9216, 10240, 11264, 12288, 13312, 14336, or 15360** - ``VCPU`` = 2 or 4
            - **value = 16384** - ``VCPU`` = 2, 4, or 8
            - **value = 17408, 18432, 19456, 21504, 22528, 23552, 25600, 26624, 27648, 29696, or 30720** - ``VCPU`` = 4
            - **value = 20480, 24576, or 28672** - ``VCPU`` = 4 or 8
            - **value = 36864, 45056, 53248, or 61440** - ``VCPU`` = 8
            - **value = 32768, 40960, 49152, or 57344** - ``VCPU`` = 8 or 16
            - **value = 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880** - ``VCPU`` = 16
            - **type="VCPU"** - The number of vCPUs reserved for the container. This parameter maps to ``CpuShares`` in the `Create a container <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/#create-a-container>`_ section of the `Docker Remote API <https://docs.aws.amazon.com/https://docs.docker.com/engine/api/v1.23/>`_ and the ``--cpu-shares`` option to `docker run <https://docs.aws.amazon.com/https://docs.docker.com/engine/reference/run/>`_ . Each vCPU is equivalent to 1,024 CPU shares. For EC2 resources, you must specify at least one vCPU. This is required but can be specified in several places; it must be specified for each node at least once.

            The default for the Fargate On-Demand vCPU resource count quota is 6 vCPUs. For more information about Fargate quotas, see `AWS Fargate quotas <https://docs.aws.amazon.com/general/latest/gr/ecs-service.html#service-quotas-fargate>`_ in the *AWS General Reference* .

            For jobs that are running on Fargate resources, then ``value`` must match one of the supported values and the ``MEMORY`` values must be one of the values supported for that ``VCPU`` value. The supported values are 0.25, 0.5, 1, 2, 4, 8, and 16

            - **value = 0.25** - ``MEMORY`` = 512, 1024, or 2048
            - **value = 0.5** - ``MEMORY`` = 1024, 2048, 3072, or 4096
            - **value = 1** - ``MEMORY`` = 2048, 3072, 4096, 5120, 6144, 7168, or 8192
            - **value = 2** - ``MEMORY`` = 4096, 5120, 6144, 7168, 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, or 16384
            - **value = 4** - ``MEMORY`` = 8192, 9216, 10240, 11264, 12288, 13312, 14336, 15360, 16384, 17408, 18432, 19456, 20480, 21504, 22528, 23552, 24576, 25600, 26624, 27648, 28672, 29696, or 30720
            - **value = 8** - ``MEMORY`` = 16384, 20480, 24576, 28672, 32768, 36864, 40960, 45056, 49152, 53248, 57344, or 61440
            - **value = 16** - ``MEMORY`` = 32768, 40960, 49152, 57344, 65536, 73728, 81920, 90112, 98304, 106496, 114688, or 122880

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-resourcerequirement.html#cfn-batch-jobdefinition-resourcerequirement-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.ResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={"limits": "limits", "requests": "requests"},
    )
    class ResourcesProperty:
        def __init__(
            self,
            *,
            limits: typing.Any = None,
            requests: typing.Any = None,
        ) -> None:
            '''
            :param limits: ``CfnJobDefinition.ResourcesProperty.Limits``.
            :param requests: ``CfnJobDefinition.ResourcesProperty.Requests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerresourcerequirements.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                # limits: Any
                # requests: Any
                
                resources_property = batch.CfnJobDefinition.ResourcesProperty(
                    limits=limits,
                    requests=requests
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d8d14a2294314d52d1f5f9ed29100fe3b4d05b9507e48a8a9d76c8968ebaa70c)
                check_type(argname="argument limits", value=limits, expected_type=type_hints["limits"])
                check_type(argname="argument requests", value=requests, expected_type=type_hints["requests"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if limits is not None:
                self._values["limits"] = limits
            if requests is not None:
                self._values["requests"] = requests

        @builtins.property
        def limits(self) -> typing.Any:
            '''``CfnJobDefinition.ResourcesProperty.Limits``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerresourcerequirements.html#cfn-batch-jobdefinition-ekscontainerresourcerequirements-limits
            '''
            result = self._values.get("limits")
            return typing.cast(typing.Any, result)

        @builtins.property
        def requests(self) -> typing.Any:
            '''``CfnJobDefinition.ResourcesProperty.Requests``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainerresourcerequirements.html#cfn-batch-jobdefinition-ekscontainerresourcerequirements-requests
            '''
            result = self._values.get("requests")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.RetryStrategyProperty",
        jsii_struct_bases=[],
        name_mapping={"attempts": "attempts", "evaluate_on_exit": "evaluateOnExit"},
    )
    class RetryStrategyProperty:
        def __init__(
            self,
            *,
            attempts: typing.Optional[jsii.Number] = None,
            evaluate_on_exit: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EvaluateOnExitProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The retry strategy that's associated with a job.

            For more information, see `Automated job retries <https://docs.aws.amazon.com/batch/latest/userguide/job_retries.html>`_ in the *AWS Batch User Guide* .

            :param attempts: The number of times to move a job to the ``RUNNABLE`` status. You can specify between 1 and 10 attempts. If the value of ``attempts`` is greater than one, the job is retried on failure the same number of attempts as the value.
            :param evaluate_on_exit: Array of up to 5 objects that specify the conditions where jobs are retried or failed. If this parameter is specified, then the ``attempts`` parameter must also be specified. If none of the listed conditions match, then the job is retried.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                retry_strategy_property = batch.CfnJobDefinition.RetryStrategyProperty(
                    attempts=123,
                    evaluate_on_exit=[batch.CfnJobDefinition.EvaluateOnExitProperty(
                        action="action",
                
                        # the properties below are optional
                        on_exit_code="onExitCode",
                        on_reason="onReason",
                        on_status_reason="onStatusReason"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fbb92016638159461ddf9048da4302f986b31747904432195638b08c9068871)
                check_type(argname="argument attempts", value=attempts, expected_type=type_hints["attempts"])
                check_type(argname="argument evaluate_on_exit", value=evaluate_on_exit, expected_type=type_hints["evaluate_on_exit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempts is not None:
                self._values["attempts"] = attempts
            if evaluate_on_exit is not None:
                self._values["evaluate_on_exit"] = evaluate_on_exit

        @builtins.property
        def attempts(self) -> typing.Optional[jsii.Number]:
            '''The number of times to move a job to the ``RUNNABLE`` status.

            You can specify between 1 and 10 attempts. If the value of ``attempts`` is greater than one, the job is retried on failure the same number of attempts as the value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-attempts
            '''
            result = self._values.get("attempts")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def evaluate_on_exit(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EvaluateOnExitProperty"]]]]:
            '''Array of up to 5 objects that specify the conditions where jobs are retried or failed.

            If this parameter is specified, then the ``attempts`` parameter must also be specified. If none of the listed conditions match, then the job is retried.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-retrystrategy.html#cfn-batch-jobdefinition-retrystrategy-evaluateonexit
            '''
            result = self._values.get("evaluate_on_exit")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EvaluateOnExitProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RetryStrategyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.SecretProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value_from": "valueFrom"},
    )
    class SecretProperty:
        def __init__(self, *, name: builtins.str, value_from: builtins.str) -> None:
            '''An object that represents the secret to expose to your container.

            Secrets can be exposed to a container in the following ways:

            - To inject sensitive data into your containers as environment variables, use the ``secrets`` container definition parameter.
            - To reference sensitive information in the log configuration of a container, use the ``secretOptions`` container definition parameter.

            For more information, see `Specifying sensitive data <https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data.html>`_ in the *AWS Batch User Guide* .

            :param name: The name of the secret.
            :param value_from: The secret to expose to the container. The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store. .. epigraph:: If the AWS Systems Manager Parameter Store parameter exists in the same Region as the job you're launching, then you can use either the full Amazon Resource Name (ARN) or name of the parameter. If the parameter exists in a different Region, then the full ARN must be specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                secret_property = batch.CfnJobDefinition.SecretProperty(
                    name="name",
                    value_from="valueFrom"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8457bb10d6230cf7d2376b857c7da531278ec4e55263cdf7d00ab731033b6b8)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value_from", value=value_from, expected_type=type_hints["value_from"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value_from": value_from,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the secret.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html#cfn-batch-jobdefinition-secret-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value_from(self) -> builtins.str:
            '''The secret to expose to the container.

            The supported values are either the full Amazon Resource Name (ARN) of the AWS Secrets Manager secret or the full ARN of the parameter in the AWS Systems Manager Parameter Store.
            .. epigraph::

               If the AWS Systems Manager Parameter Store parameter exists in the same Region as the job you're launching, then you can use either the full Amazon Resource Name (ARN) or name of the parameter. If the parameter exists in a different Region, then the full ARN must be specified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-secret.html#cfn-batch-jobdefinition-secret-valuefrom
            '''
            result = self._values.get("value_from")
            assert result is not None, "Required property 'value_from' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.SecurityContextProperty",
        jsii_struct_bases=[],
        name_mapping={
            "privileged": "privileged",
            "read_only_root_filesystem": "readOnlyRootFilesystem",
            "run_as_group": "runAsGroup",
            "run_as_non_root": "runAsNonRoot",
            "run_as_user": "runAsUser",
        },
    )
    class SecurityContextProperty:
        def __init__(
            self,
            *,
            privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            run_as_group: typing.Optional[jsii.Number] = None,
            run_as_non_root: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            run_as_user: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''
            :param privileged: ``CfnJobDefinition.SecurityContextProperty.Privileged``.
            :param read_only_root_filesystem: ``CfnJobDefinition.SecurityContextProperty.ReadOnlyRootFilesystem``.
            :param run_as_group: ``CfnJobDefinition.SecurityContextProperty.RunAsGroup``.
            :param run_as_non_root: ``CfnJobDefinition.SecurityContextProperty.RunAsNonRoot``.
            :param run_as_user: ``CfnJobDefinition.SecurityContextProperty.RunAsUser``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainersecuritycontext.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                security_context_property = batch.CfnJobDefinition.SecurityContextProperty(
                    privileged=False,
                    read_only_root_filesystem=False,
                    run_as_group=123,
                    run_as_non_root=False,
                    run_as_user=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2e712a516a1e7049d6a49a6b9958b7620d24b559ea9cc41246c57c36c6e065f)
                check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
                check_type(argname="argument read_only_root_filesystem", value=read_only_root_filesystem, expected_type=type_hints["read_only_root_filesystem"])
                check_type(argname="argument run_as_group", value=run_as_group, expected_type=type_hints["run_as_group"])
                check_type(argname="argument run_as_non_root", value=run_as_non_root, expected_type=type_hints["run_as_non_root"])
                check_type(argname="argument run_as_user", value=run_as_user, expected_type=type_hints["run_as_user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if privileged is not None:
                self._values["privileged"] = privileged
            if read_only_root_filesystem is not None:
                self._values["read_only_root_filesystem"] = read_only_root_filesystem
            if run_as_group is not None:
                self._values["run_as_group"] = run_as_group
            if run_as_non_root is not None:
                self._values["run_as_non_root"] = run_as_non_root
            if run_as_user is not None:
                self._values["run_as_user"] = run_as_user

        @builtins.property
        def privileged(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnJobDefinition.SecurityContextProperty.Privileged``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainersecuritycontext.html#cfn-batch-jobdefinition-ekscontainersecuritycontext-privileged
            '''
            result = self._values.get("privileged")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def read_only_root_filesystem(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnJobDefinition.SecurityContextProperty.ReadOnlyRootFilesystem``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainersecuritycontext.html#cfn-batch-jobdefinition-ekscontainersecuritycontext-readonlyrootfilesystem
            '''
            result = self._values.get("read_only_root_filesystem")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def run_as_group(self) -> typing.Optional[jsii.Number]:
            '''``CfnJobDefinition.SecurityContextProperty.RunAsGroup``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainersecuritycontext.html#cfn-batch-jobdefinition-ekscontainersecuritycontext-runasgroup
            '''
            result = self._values.get("run_as_group")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def run_as_non_root(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''``CfnJobDefinition.SecurityContextProperty.RunAsNonRoot``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainersecuritycontext.html#cfn-batch-jobdefinition-ekscontainersecuritycontext-runasnonroot
            '''
            result = self._values.get("run_as_non_root")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def run_as_user(self) -> typing.Optional[jsii.Number]:
            '''``CfnJobDefinition.SecurityContextProperty.RunAsUser``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ekscontainersecuritycontext.html#cfn-batch-jobdefinition-ekscontainersecuritycontext-runasuser
            '''
            result = self._values.get("run_as_user")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityContextProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.TimeoutProperty",
        jsii_struct_bases=[],
        name_mapping={"attempt_duration_seconds": "attemptDurationSeconds"},
    )
    class TimeoutProperty:
        def __init__(
            self,
            *,
            attempt_duration_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''An object that represents a job timeout configuration.

            :param attempt_duration_seconds: The job timeout time (in seconds) that's measured from the job attempt's ``startedAt`` timestamp. After this time passes, AWS Batch terminates your jobs if they aren't finished. The minimum value for the timeout is 60 seconds. For array jobs, the timeout applies to the child jobs, not to the parent array job. For multi-node parallel (MNP) jobs, the timeout applies to the whole job, not to the individual nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                timeout_property = batch.CfnJobDefinition.TimeoutProperty(
                    attempt_duration_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e723710dab64b31b8950c8bd8f23b73b01d993c8b6b612ea68c13df98c7c35dd)
                check_type(argname="argument attempt_duration_seconds", value=attempt_duration_seconds, expected_type=type_hints["attempt_duration_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attempt_duration_seconds is not None:
                self._values["attempt_duration_seconds"] = attempt_duration_seconds

        @builtins.property
        def attempt_duration_seconds(self) -> typing.Optional[jsii.Number]:
            '''The job timeout time (in seconds) that's measured from the job attempt's ``startedAt`` timestamp.

            After this time passes, AWS Batch terminates your jobs if they aren't finished. The minimum value for the timeout is 60 seconds.

            For array jobs, the timeout applies to the child jobs, not to the parent array job.

            For multi-node parallel (MNP) jobs, the timeout applies to the whole job, not to the individual nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-timeout.html#cfn-batch-jobdefinition-timeout-attemptdurationseconds
            '''
            result = self._values.get("attempt_duration_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TimeoutProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.TmpfsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_path": "containerPath",
            "size": "size",
            "mount_options": "mountOptions",
        },
    )
    class TmpfsProperty:
        def __init__(
            self,
            *,
            container_path: builtins.str,
            size: jsii.Number,
            mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The container path, mount options, and size of the ``tmpfs`` mount.

            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param container_path: The absolute file path in the container where the ``tmpfs`` volume is mounted.
            :param size: The size (in MiB) of the ``tmpfs`` volume.
            :param mount_options: The list of ``tmpfs`` volume mount options. Valid values: " ``defaults`` " | " ``ro`` " | " ``rw`` " | " ``suid`` " | " ``nosuid`` " | " ``dev`` " | " ``nodev`` " | " ``exec`` " | " ``noexec`` " | " ``sync`` " | " ``async`` " | " ``dirsync`` " | " ``remount`` " | " ``mand`` " | " ``nomand`` " | " ``atime`` " | " ``noatime`` " | " ``diratime`` " | " ``nodiratime`` " | " ``bind`` " | " ``rbind" | "unbindable" | "runbindable" | "private" | "rprivate" | "shared" | "rshared" | "slave" | "rslave" | "relatime`` " | " ``norelatime`` " | " ``strictatime`` " | " ``nostrictatime`` " | " ``mode`` " | " ``uid`` " | " ``gid`` " | " ``nr_inodes`` " | " ``nr_blocks`` " | " ``mpol`` "

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                tmpfs_property = batch.CfnJobDefinition.TmpfsProperty(
                    container_path="containerPath",
                    size=123,
                
                    # the properties below are optional
                    mount_options=["mountOptions"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a1e5e98ab831889be5a29592909c964829742037779ae89ca57cd54289531bcf)
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
            '''The absolute file path in the container where the ``tmpfs`` volume is mounted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-containerpath
            '''
            result = self._values.get("container_path")
            assert result is not None, "Required property 'container_path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def size(self) -> jsii.Number:
            '''The size (in MiB) of the ``tmpfs`` volume.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-size
            '''
            result = self._values.get("size")
            assert result is not None, "Required property 'size' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def mount_options(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of ``tmpfs`` volume mount options.

            Valid values: " ``defaults`` " | " ``ro`` " | " ``rw`` " | " ``suid`` " | " ``nosuid`` " | " ``dev`` " | " ``nodev`` " | " ``exec`` " | " ``noexec`` " | " ``sync`` " | " ``async`` " | " ``dirsync`` " | " ``remount`` " | " ``mand`` " | " ``nomand`` " | " ``atime`` " | " ``noatime`` " | " ``diratime`` " | " ``nodiratime`` " | " ``bind`` " | " ``rbind" | "unbindable" | "runbindable" | "private" | "rprivate" | "shared" | "rshared" | "slave" | "rslave" | "relatime`` " | " ``norelatime`` " | " ``strictatime`` " | " ``nostrictatime`` " | " ``mode`` " | " ``uid`` " | " ``gid`` " | " ``nr_inodes`` " | " ``nr_blocks`` " | " ``mpol`` "

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-tmpfs.html#cfn-batch-jobdefinition-tmpfs-mountoptions
            '''
            result = self._values.get("mount_options")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TmpfsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.UlimitProperty",
        jsii_struct_bases=[],
        name_mapping={
            "hard_limit": "hardLimit",
            "name": "name",
            "soft_limit": "softLimit",
        },
    )
    class UlimitProperty:
        def __init__(
            self,
            *,
            hard_limit: jsii.Number,
            name: builtins.str,
            soft_limit: jsii.Number,
        ) -> None:
            '''The ``ulimit`` settings to pass to the container.

            .. epigraph::

               This object isn't applicable to jobs that are running on Fargate resources.

            :param hard_limit: The hard limit for the ``ulimit`` type.
            :param name: The ``type`` of the ``ulimit`` .
            :param soft_limit: The soft limit for the ``ulimit`` type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                ulimit_property = batch.CfnJobDefinition.UlimitProperty(
                    hard_limit=123,
                    name="name",
                    soft_limit=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4577baeb748f86c40692f2fcbbc6aa23be44c64f98c4cf01489c80e9c919d43d)
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
            '''The hard limit for the ``ulimit`` type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-hardlimit
            '''
            result = self._values.get("hard_limit")
            assert result is not None, "Required property 'hard_limit' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The ``type`` of the ``ulimit`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def soft_limit(self) -> jsii.Number:
            '''The soft limit for the ``ulimit`` type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-ulimit.html#cfn-batch-jobdefinition-ulimit-softlimit
            '''
            result = self._values.get("soft_limit")
            assert result is not None, "Required property 'soft_limit' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UlimitProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesHostProperty",
        jsii_struct_bases=[],
        name_mapping={"source_path": "sourcePath"},
    )
    class VolumesHostProperty:
        def __init__(
            self,
            *,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Determine whether your data volume persists on the host container instance and where it's stored.

            If this parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data isn't guaranteed to persist after the containers that are associated with it stop running.

            :param source_path: The path on the host container instance that's presented to the container. If this parameter is empty, then the Docker daemon has assigned a host path for you. If this parameter contains a file location, then the data volume persists at the specified location on the host container instance until you delete it manually. If the source path location doesn't exist on the host container instance, the Docker daemon creates it. If the location does exist, the contents of the source path folder are exported. .. epigraph:: This parameter isn't applicable to jobs that run on Fargate resources. Don't provide this for these jobs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                volumes_host_property = batch.CfnJobDefinition.VolumesHostProperty(
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a948f23849eafddf36c96cb6c33217b6c1e2bb2f0ce8459301b1f27e5e5ffe30)
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The path on the host container instance that's presented to the container.

            If this parameter is empty, then the Docker daemon has assigned a host path for you. If this parameter contains a file location, then the data volume persists at the specified location on the host container instance until you delete it manually. If the source path location doesn't exist on the host container instance, the Docker daemon creates it. If the location does exist, the contents of the source path folder are exported.
            .. epigraph::

               This parameter isn't applicable to jobs that run on Fargate resources. Don't provide this for these jobs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumeshost.html#cfn-batch-jobdefinition-volumeshost-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumesHostProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobDefinition.VolumesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "efs_volume_configuration": "efsVolumeConfiguration",
            "host": "host",
            "name": "name",
        },
    )
    class VolumesProperty:
        def __init__(
            self,
            *,
            efs_volume_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.EfsVolumeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            host: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobDefinition.VolumesHostProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A list of volumes that are associated with the job.

            :param efs_volume_configuration: This is used when you're using an Amazon Elastic File System file system for job storage. For more information, see `Amazon EFS Volumes <https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html>`_ in the *AWS Batch User Guide* .
            :param host: The contents of the ``host`` parameter determine whether your data volume persists on the host container instance and where it's stored. If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data isn't guaranteed to persist after the containers that are associated with it stop running. .. epigraph:: This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.
            :param name: The name of the volume. It can be up to 255 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_). This name is referenced in the ``sourceVolume`` parameter of container definition ``mountPoints`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                volumes_property = batch.CfnJobDefinition.VolumesProperty(
                    efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                        file_system_id="fileSystemId",
                
                        # the properties below are optional
                        authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                            access_point_id="accessPointId",
                            iam="iam"
                        ),
                        root_directory="rootDirectory",
                        transit_encryption="transitEncryption",
                        transit_encryption_port=123
                    ),
                    host=batch.CfnJobDefinition.VolumesHostProperty(
                        source_path="sourcePath"
                    ),
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b5087ce87b378614336ecbae50a75fa807f069b9632cac9e6035b8d18b75562b)
                check_type(argname="argument efs_volume_configuration", value=efs_volume_configuration, expected_type=type_hints["efs_volume_configuration"])
                check_type(argname="argument host", value=host, expected_type=type_hints["host"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if efs_volume_configuration is not None:
                self._values["efs_volume_configuration"] = efs_volume_configuration
            if host is not None:
                self._values["host"] = host
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def efs_volume_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EfsVolumeConfigurationProperty"]]:
            '''This is used when you're using an Amazon Elastic File System file system for job storage.

            For more information, see `Amazon EFS Volumes <https://docs.aws.amazon.com/batch/latest/userguide/efs-volumes.html>`_ in the *AWS Batch User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-efsvolumeconfiguration
            '''
            result = self._values.get("efs_volume_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.EfsVolumeConfigurationProperty"]], result)

        @builtins.property
        def host(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.VolumesHostProperty"]]:
            '''The contents of the ``host`` parameter determine whether your data volume persists on the host container instance and where it's stored.

            If the host parameter is empty, then the Docker daemon assigns a host path for your data volume. However, the data isn't guaranteed to persist after the containers that are associated with it stop running.
            .. epigraph::

               This parameter isn't applicable to jobs that are running on Fargate resources and shouldn't be provided.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-host
            '''
            result = self._values.get("host")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobDefinition.VolumesHostProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the volume.

            It can be up to 255 characters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_). This name is referenced in the ``sourceVolume`` parameter of container definition ``mountPoints`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobdefinition-volumes.html#cfn-batch-jobdefinition-volumes-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnJobDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "container_properties": "containerProperties",
        "eks_properties": "eksProperties",
        "job_definition_name": "jobDefinitionName",
        "node_properties": "nodeProperties",
        "parameters": "parameters",
        "platform_capabilities": "platformCapabilities",
        "propagate_tags": "propagateTags",
        "retry_strategy": "retryStrategy",
        "scheduling_priority": "schedulingPriority",
        "tags": "tags",
        "timeout": "timeout",
    },
)
class CfnJobDefinitionProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        container_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.ContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        eks_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        job_definition_name: typing.Optional[builtins.str] = None,
        node_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.NodePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        parameters: typing.Any = None,
        platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
        propagate_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        retry_strategy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.RetryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        scheduling_priority: typing.Optional[jsii.Number] = None,
        tags: typing.Any = None,
        timeout: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.TimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnJobDefinition``.

        :param type: The type of job definition. For more information about multi-node parallel jobs, see `Creating a multi-node parallel job definition <https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html>`_ in the *AWS Batch User Guide* . .. epigraph:: If the job is run on Fargate resources, then ``multinode`` isn't supported.
        :param container_properties: An object with various properties specific to Amazon ECS based jobs. Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.
        :param eks_properties: An object with various properties that are specific to Amazon EKS based jobs. Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.
        :param job_definition_name: The name of the job definition.
        :param node_properties: An object with various properties that are specific to multi-node parallel jobs. Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified. .. epigraph:: If the job runs on Fargate resources, don't specify ``nodeProperties`` . Use ``containerProperties`` instead.
        :param parameters: Default parameters or parameter substitution placeholders that are set in the job definition. Parameters are specified as a key-value pair mapping. Parameters in a ``SubmitJob`` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see `Job definition parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html>`_ in the *AWS Batch User Guide* .
        :param platform_capabilities: The platform capabilities required by the job definition. If no value is specified, it defaults to ``EC2`` . Jobs run on Fargate resources specify ``FARGATE`` .
        :param propagate_tags: Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task. If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the ``FAILED`` state.
        :param retry_strategy: The retry strategy to use for failed jobs that are submitted with this job definition.
        :param scheduling_priority: The scheduling priority of the job definition. This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.
        :param tags: The tags that are applied to the job definition.
        :param timeout: The timeout time for jobs that are submitted with this job definition. After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch as batch
            
            # labels: Any
            # limits: Any
            # options: Any
            # parameters: Any
            # requests: Any
            # tags: Any
            
            cfn_job_definition_props = batch.CfnJobDefinitionProps(
                type="type",
            
                # the properties below are optional
                container_properties=batch.CfnJobDefinition.ContainerPropertiesProperty(
                    image="image",
            
                    # the properties below are optional
                    command=["command"],
                    environment=[batch.CfnJobDefinition.EnvironmentProperty(
                        name="name",
                        value="value"
                    )],
                    ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                        size_in_gi_b=123
                    ),
                    execution_role_arn="executionRoleArn",
                    fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                        platform_version="platformVersion"
                    ),
                    instance_type="instanceType",
                    job_role_arn="jobRoleArn",
                    linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                        devices=[batch.CfnJobDefinition.DeviceProperty(
                            container_path="containerPath",
                            host_path="hostPath",
                            permissions=["permissions"]
                        )],
                        init_process_enabled=False,
                        max_swap=123,
                        shared_memory_size=123,
                        swappiness=123,
                        tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                            container_path="containerPath",
                            size=123,
            
                            # the properties below are optional
                            mount_options=["mountOptions"]
                        )]
                    ),
                    log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                        log_driver="logDriver",
            
                        # the properties below are optional
                        options=options,
                        secret_options=[batch.CfnJobDefinition.SecretProperty(
                            name="name",
                            value_from="valueFrom"
                        )]
                    ),
                    memory=123,
                    mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                        container_path="containerPath",
                        read_only=False,
                        source_volume="sourceVolume"
                    )],
                    network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                        assign_public_ip="assignPublicIp"
                    ),
                    privileged=False,
                    readonly_root_filesystem=False,
                    resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                        type="type",
                        value="value"
                    )],
                    secrets=[batch.CfnJobDefinition.SecretProperty(
                        name="name",
                        value_from="valueFrom"
                    )],
                    ulimits=[batch.CfnJobDefinition.UlimitProperty(
                        hard_limit=123,
                        name="name",
                        soft_limit=123
                    )],
                    user="user",
                    vcpus=123,
                    volumes=[batch.CfnJobDefinition.VolumesProperty(
                        efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                            file_system_id="fileSystemId",
            
                            # the properties below are optional
                            authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                                access_point_id="accessPointId",
                                iam="iam"
                            ),
                            root_directory="rootDirectory",
                            transit_encryption="transitEncryption",
                            transit_encryption_port=123
                        ),
                        host=batch.CfnJobDefinition.VolumesHostProperty(
                            source_path="sourcePath"
                        ),
                        name="name"
                    )]
                ),
                eks_properties=batch.CfnJobDefinition.EksPropertiesProperty(
                    pod_properties=batch.CfnJobDefinition.PodPropertiesProperty(
                        containers=[batch.CfnJobDefinition.EksContainerProperty(
                            image="image",
            
                            # the properties below are optional
                            args=["args"],
                            command=["command"],
                            env=[batch.CfnJobDefinition.EksContainerEnvironmentVariableProperty(
                                name="name",
            
                                # the properties below are optional
                                value="value"
                            )],
                            image_pull_policy="imagePullPolicy",
                            name="name",
                            resources=batch.CfnJobDefinition.ResourcesProperty(
                                limits=limits,
                                requests=requests
                            ),
                            security_context=batch.CfnJobDefinition.SecurityContextProperty(
                                privileged=False,
                                read_only_root_filesystem=False,
                                run_as_group=123,
                                run_as_non_root=False,
                                run_as_user=123
                            ),
                            volume_mounts=[batch.CfnJobDefinition.EksContainerVolumeMountProperty(
                                mount_path="mountPath",
                                name="name",
                                read_only=False
                            )]
                        )],
                        dns_policy="dnsPolicy",
                        host_network=False,
                        metadata=batch.CfnJobDefinition.MetadataProperty(
                            labels=labels
                        ),
                        service_account_name="serviceAccountName",
                        volumes=[batch.CfnJobDefinition.EksVolumeProperty(
                            name="name",
            
                            # the properties below are optional
                            empty_dir=batch.CfnJobDefinition.EmptyDirProperty(
                                medium="medium",
                                size_limit="sizeLimit"
                            ),
                            host_path=batch.CfnJobDefinition.HostPathProperty(
                                path="path"
                            ),
                            secret=batch.CfnJobDefinition.EksSecretProperty(
                                secret_name="secretName",
            
                                # the properties below are optional
                                optional=False
                            )
                        )]
                    )
                ),
                job_definition_name="jobDefinitionName",
                node_properties=batch.CfnJobDefinition.NodePropertiesProperty(
                    main_node=123,
                    node_range_properties=[batch.CfnJobDefinition.NodeRangePropertyProperty(
                        target_nodes="targetNodes",
            
                        # the properties below are optional
                        container=batch.CfnJobDefinition.ContainerPropertiesProperty(
                            image="image",
            
                            # the properties below are optional
                            command=["command"],
                            environment=[batch.CfnJobDefinition.EnvironmentProperty(
                                name="name",
                                value="value"
                            )],
                            ephemeral_storage=batch.CfnJobDefinition.EphemeralStorageProperty(
                                size_in_gi_b=123
                            ),
                            execution_role_arn="executionRoleArn",
                            fargate_platform_configuration=batch.CfnJobDefinition.FargatePlatformConfigurationProperty(
                                platform_version="platformVersion"
                            ),
                            instance_type="instanceType",
                            job_role_arn="jobRoleArn",
                            linux_parameters=batch.CfnJobDefinition.LinuxParametersProperty(
                                devices=[batch.CfnJobDefinition.DeviceProperty(
                                    container_path="containerPath",
                                    host_path="hostPath",
                                    permissions=["permissions"]
                                )],
                                init_process_enabled=False,
                                max_swap=123,
                                shared_memory_size=123,
                                swappiness=123,
                                tmpfs=[batch.CfnJobDefinition.TmpfsProperty(
                                    container_path="containerPath",
                                    size=123,
            
                                    # the properties below are optional
                                    mount_options=["mountOptions"]
                                )]
                            ),
                            log_configuration=batch.CfnJobDefinition.LogConfigurationProperty(
                                log_driver="logDriver",
            
                                # the properties below are optional
                                options=options,
                                secret_options=[batch.CfnJobDefinition.SecretProperty(
                                    name="name",
                                    value_from="valueFrom"
                                )]
                            ),
                            memory=123,
                            mount_points=[batch.CfnJobDefinition.MountPointsProperty(
                                container_path="containerPath",
                                read_only=False,
                                source_volume="sourceVolume"
                            )],
                            network_configuration=batch.CfnJobDefinition.NetworkConfigurationProperty(
                                assign_public_ip="assignPublicIp"
                            ),
                            privileged=False,
                            readonly_root_filesystem=False,
                            resource_requirements=[batch.CfnJobDefinition.ResourceRequirementProperty(
                                type="type",
                                value="value"
                            )],
                            secrets=[batch.CfnJobDefinition.SecretProperty(
                                name="name",
                                value_from="valueFrom"
                            )],
                            ulimits=[batch.CfnJobDefinition.UlimitProperty(
                                hard_limit=123,
                                name="name",
                                soft_limit=123
                            )],
                            user="user",
                            vcpus=123,
                            volumes=[batch.CfnJobDefinition.VolumesProperty(
                                efs_volume_configuration=batch.CfnJobDefinition.EfsVolumeConfigurationProperty(
                                    file_system_id="fileSystemId",
            
                                    # the properties below are optional
                                    authorization_config=batch.CfnJobDefinition.AuthorizationConfigProperty(
                                        access_point_id="accessPointId",
                                        iam="iam"
                                    ),
                                    root_directory="rootDirectory",
                                    transit_encryption="transitEncryption",
                                    transit_encryption_port=123
                                ),
                                host=batch.CfnJobDefinition.VolumesHostProperty(
                                    source_path="sourcePath"
                                ),
                                name="name"
                            )]
                        )
                    )],
                    num_nodes=123
                ),
                parameters=parameters,
                platform_capabilities=["platformCapabilities"],
                propagate_tags=False,
                retry_strategy=batch.CfnJobDefinition.RetryStrategyProperty(
                    attempts=123,
                    evaluate_on_exit=[batch.CfnJobDefinition.EvaluateOnExitProperty(
                        action="action",
            
                        # the properties below are optional
                        on_exit_code="onExitCode",
                        on_reason="onReason",
                        on_status_reason="onStatusReason"
                    )]
                ),
                scheduling_priority=123,
                tags=tags,
                timeout=batch.CfnJobDefinition.TimeoutProperty(
                    attempt_duration_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2fb593465fb397a49eb9e021db7bb3c04e885d5f6d7e1af323262458c238c9)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument container_properties", value=container_properties, expected_type=type_hints["container_properties"])
            check_type(argname="argument eks_properties", value=eks_properties, expected_type=type_hints["eks_properties"])
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument node_properties", value=node_properties, expected_type=type_hints["node_properties"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument platform_capabilities", value=platform_capabilities, expected_type=type_hints["platform_capabilities"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument retry_strategy", value=retry_strategy, expected_type=type_hints["retry_strategy"])
            check_type(argname="argument scheduling_priority", value=scheduling_priority, expected_type=type_hints["scheduling_priority"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if container_properties is not None:
            self._values["container_properties"] = container_properties
        if eks_properties is not None:
            self._values["eks_properties"] = eks_properties
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if node_properties is not None:
            self._values["node_properties"] = node_properties
        if parameters is not None:
            self._values["parameters"] = parameters
        if platform_capabilities is not None:
            self._values["platform_capabilities"] = platform_capabilities
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if retry_strategy is not None:
            self._values["retry_strategy"] = retry_strategy
        if scheduling_priority is not None:
            self._values["scheduling_priority"] = scheduling_priority
        if tags is not None:
            self._values["tags"] = tags
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of job definition.

        For more information about multi-node parallel jobs, see `Creating a multi-node parallel job definition <https://docs.aws.amazon.com/batch/latest/userguide/multi-node-job-def.html>`_ in the *AWS Batch User Guide* .
        .. epigraph::

           If the job is run on Fargate resources, then ``multinode`` isn't supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def container_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.ContainerPropertiesProperty]]:
        '''An object with various properties specific to Amazon ECS based jobs.

        Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-containerproperties
        '''
        result = self._values.get("container_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.ContainerPropertiesProperty]], result)

    @builtins.property
    def eks_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.EksPropertiesProperty]]:
        '''An object with various properties that are specific to Amazon EKS based jobs.

        Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-eksproperties
        '''
        result = self._values.get("eks_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.EksPropertiesProperty]], result)

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-jobdefinitionname
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.NodePropertiesProperty]]:
        '''An object with various properties that are specific to multi-node parallel jobs.

        Valid values are ``containerProperties`` , ``eksProperties`` , and ``nodeProperties`` . Only one can be specified.
        .. epigraph::

           If the job runs on Fargate resources, don't specify ``nodeProperties`` . Use ``containerProperties`` instead.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-nodeproperties
        '''
        result = self._values.get("node_properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.NodePropertiesProperty]], result)

    @builtins.property
    def parameters(self) -> typing.Any:
        '''Default parameters or parameter substitution placeholders that are set in the job definition.

        Parameters are specified as a key-value pair mapping. Parameters in a ``SubmitJob`` request override any corresponding parameter defaults from the job definition. For more information about specifying parameters, see `Job definition parameters <https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html>`_ in the *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-parameters
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Any, result)

    @builtins.property
    def platform_capabilities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The platform capabilities required by the job definition.

        If no value is specified, it defaults to ``EC2`` . Jobs run on Fargate resources specify ``FARGATE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-platformcapabilities
        '''
        result = self._values.get("platform_capabilities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def propagate_tags(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether to propagate the tags from the job or job definition to the corresponding Amazon ECS task.

        If no value is specified, the tags aren't propagated. Tags can only be propagated to the tasks when the tasks are created. For tags with the same name, job tags are given priority over job definitions tags. If the total number of combined tags from the job and job definition is over 50, the job is moved to the ``FAILED`` state.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-propagatetags
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def retry_strategy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.RetryStrategyProperty]]:
        '''The retry strategy to use for failed jobs that are submitted with this job definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-retrystrategy
        '''
        result = self._values.get("retry_strategy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.RetryStrategyProperty]], result)

    @builtins.property
    def scheduling_priority(self) -> typing.Optional[jsii.Number]:
        '''The scheduling priority of the job definition.

        This only affects jobs in job queues with a fair share policy. Jobs with a higher scheduling priority are scheduled before jobs with a lower scheduling priority.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-schedulingpriority
        '''
        result = self._values.get("scheduling_priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Any:
        '''The tags that are applied to the job definition.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Any, result)

    @builtins.property
    def timeout(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.TimeoutProperty]]:
        '''The timeout time for jobs that are submitted with this job definition.

        After the amount of time you specify passes, AWS Batch terminates your jobs if they aren't finished.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobdefinition.html#cfn-batch-jobdefinition-timeout
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.TimeoutProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobDefinitionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnJobQueue(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnJobQueue",
):
    '''A CloudFormation ``AWS::Batch::JobQueue``.

    The ``AWS::Batch::JobQueue`` resource specifies the parameters for an AWS Batch job queue definition. For more information, see `Job Queues <https://docs.aws.amazon.com/batch/latest/userguide/job_queues.html>`_ in the ** .

    :cloudformationResource: AWS::Batch::JobQueue
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch as batch
        
        cfn_job_queue = batch.CfnJobQueue(self, "MyCfnJobQueue",
            compute_environment_order=[batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                compute_environment="computeEnvironment",
                order=123
            )],
            priority=123,
        
            # the properties below are optional
            job_queue_name="jobQueueName",
            scheduling_policy_arn="schedulingPolicyArn",
            state="state",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        compute_environment_order: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnJobQueue.ComputeEnvironmentOrderProperty", typing.Dict[builtins.str, typing.Any]]]]],
        priority: jsii.Number,
        job_queue_name: typing.Optional[builtins.str] = None,
        scheduling_policy_arn: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Batch::JobQueue``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param compute_environment_order: The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed. .. epigraph:: All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.
        :param priority: The priority of the job queue. Job queues with a higher priority (or a higher integer value for the ``priority`` parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority value of ``10`` is given scheduling preference over a job queue with a priority value of ``1`` . All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
        :param job_queue_name: The name of the job queue. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param scheduling_policy_arn: The Amazon Resource Name (ARN) of the scheduling policy. The format is ``aws: *Partition* :batch: *Region* : *Account* :scheduling-policy/ *Name*`` . For example, ``aws:aws:batch:us-west-2:123456789012:scheduling-policy/MySchedulingPolicy`` .
        :param state: The state of the job queue. If the job queue state is ``ENABLED`` , it is able to accept jobs. If the job queue state is ``DISABLED`` , new jobs can't be added to the queue, but jobs already in the queue can finish.
        :param tags: The tags that are applied to the job queue. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ in *AWS Batch User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d45ceb8834180bf5b87da79a018b9248e1475232962a3bab5fc8e9874e9fc7f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnJobQueueProps(
            compute_environment_order=compute_environment_order,
            priority=priority,
            job_queue_name=job_queue_name,
            scheduling_policy_arn=scheduling_policy_arn,
            state=state,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b40845028a0f4f7eaad64ef2519b142a4c3847fdd17579a79dff446cb1223bbb)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bba213fbb76e04ee2b0ea1ca549bb1356bc2f700259e377f297466a196e5019c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrJobQueueArn")
    def attr_job_queue_arn(self) -> builtins.str:
        '''Returns the job queue ARN, such as ``batch: *us-east-1* : *111122223333* :job-queue/ *JobQueueName*`` .

        :cloudformationAttribute: JobQueueArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrJobQueueArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags that are applied to the job queue.

        For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ in *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="computeEnvironmentOrder")
    def compute_environment_order(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobQueue.ComputeEnvironmentOrderProperty"]]]:
        '''The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
        .. epigraph::

           All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobQueue.ComputeEnvironmentOrderProperty"]]], jsii.get(self, "computeEnvironmentOrder"))

    @compute_environment_order.setter
    def compute_environment_order(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnJobQueue.ComputeEnvironmentOrderProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f46e6804b033d8f6c463e15ff250bd04172d1d6f9a81fadbe808c4c7e59ae4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computeEnvironmentOrder", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''The priority of the job queue.

        Job queues with a higher priority (or a higher integer value for the ``priority`` parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority value of ``10`` is given scheduling preference over a job queue with a priority value of ``1`` . All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1078e6a6700fd0cdcbf286e07d93323c4bbbaf73b0b7dfbe7aad318300b4efca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job queue.

        It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "jobQueueName"))

    @job_queue_name.setter
    def job_queue_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1749dbd3563f50046f0c775d69fbe792a8e925d8a408b163bc5c048fd0cad86a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jobQueueName", value)

    @builtins.property
    @jsii.member(jsii_name="schedulingPolicyArn")
    def scheduling_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the scheduling policy.

        The format is ``aws: *Partition* :batch: *Region* : *Account* :scheduling-policy/ *Name*`` . For example, ``aws:aws:batch:us-west-2:123456789012:scheduling-policy/MySchedulingPolicy`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-schedulingpolicyarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "schedulingPolicyArn"))

    @scheduling_policy_arn.setter
    def scheduling_policy_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39329cd2acd43021d3942bdea6716312480fe2a28ba4e71868404948115d44ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "schedulingPolicyArn", value)

    @builtins.property
    @jsii.member(jsii_name="state")
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the job queue.

        If the job queue state is ``ENABLED`` , it is able to accept jobs. If the job queue state is ``DISABLED`` , new jobs can't be added to the queue, but jobs already in the queue can finish.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "state"))

    @state.setter
    def state(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea43c391bbfb1443f4c91e0c8b6716bda8e2a17836bd269e26b2a99fd91c3668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "state", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnJobQueue.ComputeEnvironmentOrderProperty",
        jsii_struct_bases=[],
        name_mapping={"compute_environment": "computeEnvironment", "order": "order"},
    )
    class ComputeEnvironmentOrderProperty:
        def __init__(
            self,
            *,
            compute_environment: builtins.str,
            order: jsii.Number,
        ) -> None:
            '''The order that compute environments are tried in for job placement within a queue.

            Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower order integer value is tried for job placement first. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
            .. epigraph::

               All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

            :param compute_environment: The Amazon Resource Name (ARN) of the compute environment.
            :param order: The order of the compute environment. Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower ``order`` integer value is tried for job placement first.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                compute_environment_order_property = batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment="computeEnvironment",
                    order=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d652f3a45d29f5f6e825062154191183ef2be818632dd8c3bb528bab72ff8734)
                check_type(argname="argument compute_environment", value=compute_environment, expected_type=type_hints["compute_environment"])
                check_type(argname="argument order", value=order, expected_type=type_hints["order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "compute_environment": compute_environment,
                "order": order,
            }

        @builtins.property
        def compute_environment(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the compute environment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-computeenvironment
            '''
            result = self._values.get("compute_environment")
            assert result is not None, "Required property 'compute_environment' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def order(self) -> jsii.Number:
            '''The order of the compute environment.

            Compute environments are tried in ascending order. For example, if two compute environments are associated with a job queue, the compute environment with a lower ``order`` integer value is tried for job placement first.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-jobqueue-computeenvironmentorder.html#cfn-batch-jobqueue-computeenvironmentorder-order
            '''
            result = self._values.get("order")
            assert result is not None, "Required property 'order' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeEnvironmentOrderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnJobQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_order": "computeEnvironmentOrder",
        "priority": "priority",
        "job_queue_name": "jobQueueName",
        "scheduling_policy_arn": "schedulingPolicyArn",
        "state": "state",
        "tags": "tags",
    },
)
class CfnJobQueueProps:
    def __init__(
        self,
        *,
        compute_environment_order: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobQueue.ComputeEnvironmentOrderProperty, typing.Dict[builtins.str, typing.Any]]]]],
        priority: jsii.Number,
        job_queue_name: typing.Optional[builtins.str] = None,
        scheduling_policy_arn: typing.Optional[builtins.str] = None,
        state: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnJobQueue``.

        :param compute_environment_order: The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed. .. epigraph:: All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.
        :param priority: The priority of the job queue. Job queues with a higher priority (or a higher integer value for the ``priority`` parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority value of ``10`` is given scheduling preference over a job queue with a priority value of ``1`` . All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
        :param job_queue_name: The name of the job queue. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param scheduling_policy_arn: The Amazon Resource Name (ARN) of the scheduling policy. The format is ``aws: *Partition* :batch: *Region* : *Account* :scheduling-policy/ *Name*`` . For example, ``aws:aws:batch:us-west-2:123456789012:scheduling-policy/MySchedulingPolicy`` .
        :param state: The state of the job queue. If the job queue state is ``ENABLED`` , it is able to accept jobs. If the job queue state is ``DISABLED`` , new jobs can't be added to the queue, but jobs already in the queue can finish.
        :param tags: The tags that are applied to the job queue. For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ in *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch as batch
            
            cfn_job_queue_props = batch.CfnJobQueueProps(
                compute_environment_order=[batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment="computeEnvironment",
                    order=123
                )],
                priority=123,
            
                # the properties below are optional
                job_queue_name="jobQueueName",
                scheduling_policy_arn="schedulingPolicyArn",
                state="state",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb68f68eff8e0e521b37bbd631d3341564b3f6e589db1d5e23de934507b9c2ed)
            check_type(argname="argument compute_environment_order", value=compute_environment_order, expected_type=type_hints["compute_environment_order"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument job_queue_name", value=job_queue_name, expected_type=type_hints["job_queue_name"])
            check_type(argname="argument scheduling_policy_arn", value=scheduling_policy_arn, expected_type=type_hints["scheduling_policy_arn"])
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_environment_order": compute_environment_order,
            "priority": priority,
        }
        if job_queue_name is not None:
            self._values["job_queue_name"] = job_queue_name
        if scheduling_policy_arn is not None:
            self._values["scheduling_policy_arn"] = scheduling_policy_arn
        if state is not None:
            self._values["state"] = state
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def compute_environment_order(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobQueue.ComputeEnvironmentOrderProperty]]]:
        '''The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to determine which compute environment runs a specific job. Compute environments must be in the ``VALID`` state before you can associate them with a job queue. You can associate up to three compute environments with a job queue. All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.
        .. epigraph::

           All compute environments that are associated with a job queue must share the same architecture. AWS Batch doesn't support mixing compute environment architecture types in a single job queue.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-computeenvironmentorder
        '''
        result = self._values.get("compute_environment_order")
        assert result is not None, "Required property 'compute_environment_order' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobQueue.ComputeEnvironmentOrderProperty]]], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''The priority of the job queue.

        Job queues with a higher priority (or a higher integer value for the ``priority`` parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order. For example, a job queue with a priority value of ``10`` is given scheduling preference over a job queue with a priority value of ``1`` . All of the compute environments must be either EC2 ( ``EC2`` or ``SPOT`` ) or Fargate ( ``FARGATE`` or ``FARGATE_SPOT`` ); EC2 and Fargate compute environments can't be mixed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        '''The name of the job queue.

        It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-jobqueuename
        '''
        result = self._values.get("job_queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scheduling_policy_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the scheduling policy.

        The format is ``aws: *Partition* :batch: *Region* : *Account* :scheduling-policy/ *Name*`` . For example, ``aws:aws:batch:us-west-2:123456789012:scheduling-policy/MySchedulingPolicy`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-schedulingpolicyarn
        '''
        result = self._values.get("scheduling_policy_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def state(self) -> typing.Optional[builtins.str]:
        '''The state of the job queue.

        If the job queue state is ``ENABLED`` , it is able to accept jobs. If the job queue state is ``DISABLED`` , new jobs can't be added to the queue, but jobs already in the queue can finish.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-state
        '''
        result = self._values.get("state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags that are applied to the job queue.

        For more information, see `Tagging your AWS Batch resources <https://docs.aws.amazon.com/batch/latest/userguide/using-tags.html>`_ in *AWS Batch User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-jobqueue.html#cfn-batch-jobqueue-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnJobQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnSchedulingPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.CfnSchedulingPolicy",
):
    '''A CloudFormation ``AWS::Batch::SchedulingPolicy``.

    The ``AWS::Batch::SchedulingPolicy`` resource specifies the parameters for an AWS Batch scheduling policy. For more information, see `Scheduling Policies <https://docs.aws.amazon.com/batch/latest/userguide/scheduling_policies.html>`_ in the ** .

    :cloudformationResource: AWS::Batch::SchedulingPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_batch as batch
        
        cfn_scheduling_policy = batch.CfnSchedulingPolicy(self, "MyCfnSchedulingPolicy",
            fairshare_policy=batch.CfnSchedulingPolicy.FairsharePolicyProperty(
                compute_reservation=123,
                share_decay_seconds=123,
                share_distribution=[batch.CfnSchedulingPolicy.ShareAttributesProperty(
                    share_identifier="shareIdentifier",
                    weight_factor=123
                )]
            ),
            name="name",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        fairshare_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSchedulingPolicy.FairsharePolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::Batch::SchedulingPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param fairshare_policy: The fair share policy of the scheduling policy.
        :param name: The name of the scheduling policy. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param tags: The tags that you apply to the scheduling policy to help you categorize and organize your resources. Each tag consists of a key and an optional value. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in *AWS General Reference* . These tags can be updated or removed using the `TagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_TagResource.html>`_ and `UntagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_UntagResource.html>`_ API operations.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e3f5b12574d09b9b554d3949c3a208090b28bfd8e56c76a1acb4a1b9dbf9dfb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSchedulingPolicyProps(
            fairshare_policy=fairshare_policy, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c74595793997bab76778b08d2b955353f9f489c52c12224700fcd3e48a29078a)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea1c11da28bfd24b8bce94afa234114cf35f7ab9217c678155d3852bd2d19418)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''Returns the scheduling policy ARN, such as ``batch: *us-east-1* : *111122223333* :scheduling-policy/ *HighPriority*`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags that you apply to the scheduling policy to help you categorize and organize your resources.

        Each tag consists of a key and an optional value. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in *AWS General Reference* .

        These tags can be updated or removed using the `TagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_TagResource.html>`_ and `UntagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_UntagResource.html>`_ API operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="fairsharePolicy")
    def fairshare_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSchedulingPolicy.FairsharePolicyProperty"]]:
        '''The fair share policy of the scheduling policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSchedulingPolicy.FairsharePolicyProperty"]], jsii.get(self, "fairsharePolicy"))

    @fairshare_policy.setter
    def fairshare_policy(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSchedulingPolicy.FairsharePolicyProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e7e12ec1e5407c9625e59828a1ee16a4660abc2e95da6f63b9bdad7ef167184)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fairsharePolicy", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the scheduling policy.

        It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849ed0269d02025a08e0e0cf84b06eb3051a4493243cbf19b2f4ba4aaa3d9d0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnSchedulingPolicy.FairsharePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "compute_reservation": "computeReservation",
            "share_decay_seconds": "shareDecaySeconds",
            "share_distribution": "shareDistribution",
        },
    )
    class FairsharePolicyProperty:
        def __init__(
            self,
            *,
            compute_reservation: typing.Optional[jsii.Number] = None,
            share_decay_seconds: typing.Optional[jsii.Number] = None,
            share_distribution: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnSchedulingPolicy.ShareAttributesProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The fair share policy for a scheduling policy.

            :param compute_reservation: A value used to reserve some of the available maximum vCPU for fair share identifiers that aren't already used. The reserved ratio is ``( *computeReservation* /100)^ *ActiveFairShares*`` where ``*ActiveFairShares*`` is the number of active fair share identifiers. For example, a ``computeReservation`` value of 50 indicates that AWS Batch reserves 50% of the maximum available vCPU if there's only one fair share identifier. It reserves 25% if there are two fair share identifiers. It reserves 12.5% if there are three fair share identifiers. A ``computeReservation`` value of 25 indicates that AWS Batch should reserve 25% of the maximum available vCPU if there's only one fair share identifier, 6.25% if there are two fair share identifiers, and 1.56% if there are three fair share identifiers. The minimum value is 0 and the maximum value is 99.
            :param share_decay_seconds: The amount of time (in seconds) to use to calculate a fair share percentage for each fair share identifier in use. A value of zero (0) indicates that only current usage is measured. The decay allows for more recently run jobs to have more weight than jobs that ran earlier. The maximum supported value is 604800 (1 week).
            :param share_distribution: An array of ``SharedIdentifier`` objects that contain the weights for the fair share identifiers for the fair share policy. Fair share identifiers that aren't included have a default weight of ``1.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                fairshare_policy_property = batch.CfnSchedulingPolicy.FairsharePolicyProperty(
                    compute_reservation=123,
                    share_decay_seconds=123,
                    share_distribution=[batch.CfnSchedulingPolicy.ShareAttributesProperty(
                        share_identifier="shareIdentifier",
                        weight_factor=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a8d2dd48acf8140bc8e582e663930a1cf7feb0f972af9196223d5f169ef40f82)
                check_type(argname="argument compute_reservation", value=compute_reservation, expected_type=type_hints["compute_reservation"])
                check_type(argname="argument share_decay_seconds", value=share_decay_seconds, expected_type=type_hints["share_decay_seconds"])
                check_type(argname="argument share_distribution", value=share_distribution, expected_type=type_hints["share_distribution"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if compute_reservation is not None:
                self._values["compute_reservation"] = compute_reservation
            if share_decay_seconds is not None:
                self._values["share_decay_seconds"] = share_decay_seconds
            if share_distribution is not None:
                self._values["share_distribution"] = share_distribution

        @builtins.property
        def compute_reservation(self) -> typing.Optional[jsii.Number]:
            '''A value used to reserve some of the available maximum vCPU for fair share identifiers that aren't already used.

            The reserved ratio is ``( *computeReservation* /100)^ *ActiveFairShares*`` where ``*ActiveFairShares*`` is the number of active fair share identifiers.

            For example, a ``computeReservation`` value of 50 indicates that AWS Batch reserves 50% of the maximum available vCPU if there's only one fair share identifier. It reserves 25% if there are two fair share identifiers. It reserves 12.5% if there are three fair share identifiers. A ``computeReservation`` value of 25 indicates that AWS Batch should reserve 25% of the maximum available vCPU if there's only one fair share identifier, 6.25% if there are two fair share identifiers, and 1.56% if there are three fair share identifiers.

            The minimum value is 0 and the maximum value is 99.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy-computereservation
            '''
            result = self._values.get("compute_reservation")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def share_decay_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time (in seconds) to use to calculate a fair share percentage for each fair share identifier in use.

            A value of zero (0) indicates that only current usage is measured. The decay allows for more recently run jobs to have more weight than jobs that ran earlier. The maximum supported value is 604800 (1 week).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy-sharedecayseconds
            '''
            result = self._values.get("share_decay_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def share_distribution(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSchedulingPolicy.ShareAttributesProperty"]]]]:
            '''An array of ``SharedIdentifier`` objects that contain the weights for the fair share identifiers for the fair share policy.

            Fair share identifiers that aren't included have a default weight of ``1.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-fairsharepolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy-sharedistribution
            '''
            result = self._values.get("share_distribution")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnSchedulingPolicy.ShareAttributesProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FairsharePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-batch.CfnSchedulingPolicy.ShareAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "share_identifier": "shareIdentifier",
            "weight_factor": "weightFactor",
        },
    )
    class ShareAttributesProperty:
        def __init__(
            self,
            *,
            share_identifier: typing.Optional[builtins.str] = None,
            weight_factor: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Specifies the weights for the fair share identifiers for the fair share policy.

            Fair share identifiers that aren't included have a default weight of ``1.0`` .

            :param share_identifier: A fair share identifier or fair share identifier prefix. If the string ends with an asterisk (*), this entry specifies the weight factor to use for fair share identifiers that start with that prefix. The list of fair share identifiers in a fair share policy can't overlap. For example, you can't have one that specifies a ``shareIdentifier`` of ``UserA*`` and another that specifies a ``shareIdentifier`` of ``UserA-1`` . There can be no more than 500 fair share identifiers active in a job queue. The string is limited to 255 alphanumeric characters, and can be followed by an asterisk (*).
            :param weight_factor: The weight factor for the fair share identifier. The default value is 1.0. A lower value has a higher priority for compute resources. For example, jobs that use a share identifier with a weight factor of 0.125 (1/8) get 8 times the compute resources of jobs that use a share identifier with a weight factor of 1. The smallest supported value is 0.0001, and the largest supported value is 999.9999.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-shareattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_batch as batch
                
                share_attributes_property = batch.CfnSchedulingPolicy.ShareAttributesProperty(
                    share_identifier="shareIdentifier",
                    weight_factor=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1bac75ae975eec2e972fd2432eaac0f39e1f2b6e2328652659783cbb0f71bce7)
                check_type(argname="argument share_identifier", value=share_identifier, expected_type=type_hints["share_identifier"])
                check_type(argname="argument weight_factor", value=weight_factor, expected_type=type_hints["weight_factor"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if share_identifier is not None:
                self._values["share_identifier"] = share_identifier
            if weight_factor is not None:
                self._values["weight_factor"] = weight_factor

        @builtins.property
        def share_identifier(self) -> typing.Optional[builtins.str]:
            '''A fair share identifier or fair share identifier prefix.

            If the string ends with an asterisk (*), this entry specifies the weight factor to use for fair share identifiers that start with that prefix. The list of fair share identifiers in a fair share policy can't overlap. For example, you can't have one that specifies a ``shareIdentifier`` of ``UserA*`` and another that specifies a ``shareIdentifier`` of ``UserA-1`` .

            There can be no more than 500 fair share identifiers active in a job queue.

            The string is limited to 255 alphanumeric characters, and can be followed by an asterisk (*).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-shareattributes.html#cfn-batch-schedulingpolicy-shareattributes-shareidentifier
            '''
            result = self._values.get("share_identifier")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def weight_factor(self) -> typing.Optional[jsii.Number]:
            '''The weight factor for the fair share identifier.

            The default value is 1.0. A lower value has a higher priority for compute resources. For example, jobs that use a share identifier with a weight factor of 0.125 (1/8) get 8 times the compute resources of jobs that use a share identifier with a weight factor of 1.

            The smallest supported value is 0.0001, and the largest supported value is 999.9999.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-schedulingpolicy-shareattributes.html#cfn-batch-schedulingpolicy-shareattributes-weightfactor
            '''
            result = self._values.get("weight_factor")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ShareAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.CfnSchedulingPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "fairshare_policy": "fairsharePolicy",
        "name": "name",
        "tags": "tags",
    },
)
class CfnSchedulingPolicyProps:
    def __init__(
        self,
        *,
        fairshare_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSchedulingPolicy.FairsharePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSchedulingPolicy``.

        :param fairshare_policy: The fair share policy of the scheduling policy.
        :param name: The name of the scheduling policy. It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).
        :param tags: The tags that you apply to the scheduling policy to help you categorize and organize your resources. Each tag consists of a key and an optional value. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in *AWS General Reference* . These tags can be updated or removed using the `TagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_TagResource.html>`_ and `UntagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_UntagResource.html>`_ API operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch as batch
            
            cfn_scheduling_policy_props = batch.CfnSchedulingPolicyProps(
                fairshare_policy=batch.CfnSchedulingPolicy.FairsharePolicyProperty(
                    compute_reservation=123,
                    share_decay_seconds=123,
                    share_distribution=[batch.CfnSchedulingPolicy.ShareAttributesProperty(
                        share_identifier="shareIdentifier",
                        weight_factor=123
                    )]
                ),
                name="name",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2762a742e69dc2048aa582997e3913536cecc5018d19c3d94bdea6d66e74b8)
            check_type(argname="argument fairshare_policy", value=fairshare_policy, expected_type=type_hints["fairshare_policy"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if fairshare_policy is not None:
            self._values["fairshare_policy"] = fairshare_policy
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def fairshare_policy(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSchedulingPolicy.FairsharePolicyProperty]]:
        '''The fair share policy of the scheduling policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-fairsharepolicy
        '''
        result = self._values.get("fairshare_policy")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSchedulingPolicy.FairsharePolicyProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the scheduling policy.

        It can be up to 128 letters long. It can contain uppercase and lowercase letters, numbers, hyphens (-), and underscores (_).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''The tags that you apply to the scheduling policy to help you categorize and organize your resources.

        Each tag consists of a key and an optional value. For more information, see `Tagging AWS Resources <https://docs.aws.amazon.com/general/latest/gr/aws_tagging.html>`_ in *AWS General Reference* .

        These tags can be updated or removed using the `TagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_TagResource.html>`_ and `UntagResource <https://docs.aws.amazon.com/batch/latest/APIReference/API_UntagResource.html>`_ API operations.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-batch-schedulingpolicy.html#cfn-batch-schedulingpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSchedulingPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.ComputeEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environment_name": "computeEnvironmentName",
        "compute_resources": "computeResources",
        "enabled": "enabled",
        "managed": "managed",
        "service_role": "serviceRole",
    },
)
class ComputeEnvironmentProps:
    def __init__(
        self,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union["ComputeResources", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        managed: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Compute Environment.

        :param compute_environment_name: (experimental) A name for the compute environment. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - CloudFormation-generated name
        :param compute_resources: (experimental) The details of the required compute resources for the managed compute environment. If specified, and this is an unmanaged compute environment, will throw an error. By default, AWS Batch managed compute environments use a recent, approved version of the Amazon ECS-optimized AMI for compute resources. Default: - CloudFormation defaults
        :param enabled: (experimental) The state of the compute environment. If the state is set to true, then the compute environment accepts jobs from a queue and can scale out automatically based on queues. Default: true
        :param managed: (experimental) Determines if AWS should manage the allocation of compute resources for processing jobs. If set to false, then you are in charge of providing the compute resource details. Default: true
        :param service_role: (experimental) The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service. By default, this role is created for you using the AWS managed service policy for Batch. Default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
                compute_resources=batch.ComputeResources(
                    image=ecs.EcsOptimizedAmi(
                        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                    ),
                    vpc=vpc
                )
            )
        '''
        if isinstance(compute_resources, dict):
            compute_resources = ComputeResources(**compute_resources)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21ace0cdfc3f35b35e17654517fe1dbc2099cd3b46cec312cf8dce94ded0d75)
            check_type(argname="argument compute_environment_name", value=compute_environment_name, expected_type=type_hints["compute_environment_name"])
            check_type(argname="argument compute_resources", value=compute_resources, expected_type=type_hints["compute_resources"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument managed", value=managed, expected_type=type_hints["managed"])
            check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_environment_name is not None:
            self._values["compute_environment_name"] = compute_environment_name
        if compute_resources is not None:
            self._values["compute_resources"] = compute_resources
        if enabled is not None:
            self._values["enabled"] = enabled
        if managed is not None:
            self._values["managed"] = managed
        if service_role is not None:
            self._values["service_role"] = service_role

    @builtins.property
    def compute_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the compute environment.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :default: - CloudFormation-generated name

        :stability: experimental
        '''
        result = self._values.get("compute_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def compute_resources(self) -> typing.Optional["ComputeResources"]:
        '''(experimental) The details of the required compute resources for the managed compute environment.

        If specified, and this is an unmanaged compute environment, will throw an error.

        By default, AWS Batch managed compute environments use a recent, approved version of the
        Amazon ECS-optimized AMI for compute resources.

        :default: - CloudFormation defaults

        :stability: experimental
        :link: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-batch-computeenvironment-computeresources.html
        '''
        result = self._values.get("compute_resources")
        return typing.cast(typing.Optional["ComputeResources"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The state of the compute environment.

        If the state is set to true, then the compute
        environment accepts jobs from a queue and can scale out automatically based on queues.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def managed(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Determines if AWS should manage the allocation of compute resources for processing jobs.

        If set to false, then you are in charge of providing the compute resource details.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("managed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def service_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service.

        By default, this role is created for you using
        the AWS managed service policy for Batch.

        :default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/service_IAM_role.html
        '''
        result = self._values.get("service_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch.ComputeResourceType")
class ComputeResourceType(enum.Enum):
    '''(experimental) Property to specify if the compute environment uses On-Demand, SpotFleet, Fargate, or Fargate Spot compute resources.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        vpc = ec2.Vpc(self, "VPC")
        
        spot_environment = batch.ComputeEnvironment(self, "MySpotEnvironment",
            compute_resources=batch.ComputeResources(
                type=batch.ComputeResourceType.SPOT,
                bid_percentage=75,  # Bids for resources at 75% of the on-demand price
                vpc=vpc
            )
        )
    '''

    ON_DEMAND = "ON_DEMAND"
    '''(experimental) Resources will be EC2 On-Demand resources.

    :stability: experimental
    '''
    SPOT = "SPOT"
    '''(experimental) Resources will be EC2 SpotFleet resources.

    :stability: experimental
    '''
    FARGATE = "FARGATE"
    '''(experimental) Resources will be Fargate resources.

    :stability: experimental
    '''
    FARGATE_SPOT = "FARGATE_SPOT"
    '''(experimental) Resources will be Fargate Spot resources.

    Fargate Spot uses spare capacity in the AWS cloud to run your fault-tolerant,
    time-flexible jobs at up to a 70% discount. If AWS needs the resources back,
    jobs running on Fargate Spot will be interrupted with two minutes of notification.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.ComputeResources",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "allocation_strategy": "allocationStrategy",
        "bid_percentage": "bidPercentage",
        "compute_resources_tags": "computeResourcesTags",
        "desiredv_cpus": "desiredvCpus",
        "ec2_key_pair": "ec2KeyPair",
        "image": "image",
        "instance_role": "instanceRole",
        "instance_types": "instanceTypes",
        "launch_template": "launchTemplate",
        "maxv_cpus": "maxvCpus",
        "minv_cpus": "minvCpus",
        "placement_group": "placementGroup",
        "security_groups": "securityGroups",
        "spot_fleet_role": "spotFleetRole",
        "type": "type",
        "vpc_subnets": "vpcSubnets",
    },
)
class ComputeResources:
    def __init__(
        self,
        *,
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
        allocation_strategy: typing.Optional[AllocationStrategy] = None,
        bid_percentage: typing.Optional[jsii.Number] = None,
        compute_resources_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        desiredv_cpus: typing.Optional[jsii.Number] = None,
        ec2_key_pair: typing.Optional[builtins.str] = None,
        image: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IMachineImage] = None,
        instance_role: typing.Optional[builtins.str] = None,
        instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.InstanceType]] = None,
        launch_template: typing.Optional[typing.Union["LaunchTemplateSpecification", typing.Dict[builtins.str, typing.Any]]] = None,
        maxv_cpus: typing.Optional[jsii.Number] = None,
        minv_cpus: typing.Optional[jsii.Number] = None,
        placement_group: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
        spot_fleet_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        type: typing.Optional[ComputeResourceType] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for defining the structure of the batch compute cluster.

        :param vpc: (experimental) The VPC network that all compute resources will be connected to.
        :param allocation_strategy: (experimental) The allocation strategy to use for the compute resource in case not enough instances of the best fitting instance type can be allocated. This could be due to availability of the instance type in the region or Amazon EC2 service limits. If this is not specified, the default for the EC2 ComputeResourceType is BEST_FIT, which will use only the best fitting instance type, waiting for additional capacity if it's not available. This allocation strategy keeps costs lower but can limit scaling. If you are using Spot Fleets with BEST_FIT then the Spot Fleet IAM Role must be specified. BEST_FIT_PROGRESSIVE will select an additional instance type that is large enough to meet the requirements of the jobs in the queue, with a preference for an instance type with a lower cost. The default value for the SPOT instance type is SPOT_CAPACITY_OPTIMIZED, which is only available for for this type of compute resources and will select an additional instance type that is large enough to meet the requirements of the jobs in the queue, with a preference for an instance type that is less likely to be interrupted. Default: AllocationStrategy.BEST_FIT
        :param bid_percentage: (experimental) This property will be ignored if you set the environment type to ON_DEMAND. The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for that instance type before instances are launched. For example, if your maximum percentage is 20%, then the Spot price must be below 20% of the current On-Demand price for that EC2 instance. You always pay the lowest (market) price and never more than your maximum percentage. If you leave this field empty, the default value is 100% of the On-Demand price. Default: 100
        :param compute_resources_tags: (experimental) Key-value pair tags to be applied to resources that are launched in the compute environment. For AWS Batch, these take the form of "String1": "String2", where String1 is the tag key and String2 is the tag value—for example, { "Name": "AWS Batch Instance - C4OnDemand" }. Default: - no tags will be assigned on compute resources.
        :param desiredv_cpus: (experimental) The desired number of EC2 vCPUS in the compute environment. Default: - no desired vcpu value will be used.
        :param ec2_key_pair: (experimental) The EC2 key pair that is used for instances launched in the compute environment. If no key is defined, then SSH access is not allowed to provisioned compute resources. Default: - no SSH access will be possible.
        :param image: (experimental) The Amazon Machine Image (AMI) ID used for instances launched in the compute environment. Default: - no image will be used.
        :param instance_role: (experimental) The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment. You can specify the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ecsInstanceRole or arn:aws:iam::<aws_account_id>:instance-profile/ecsInstanceRole . For more information, see Amazon ECS Instance Role in the AWS Batch User Guide. Default: - a new role will be created.
        :param instance_types: (experimental) The types of EC2 instances that may be launched in the compute environment. You can specify instance families to launch any instance type within those families (for example, c4 or p3), or you can specify specific sizes within a family (such as c4.8xlarge). You can also choose optimal to pick instance types (from the C, M, and R instance families) on the fly that match the demand of your job queues. Default: optimal
        :param launch_template: (experimental) An optional launch template to associate with your compute resources. For more information, see README file. Default: - no custom launch template will be used
        :param maxv_cpus: (experimental) The maximum number of EC2 vCPUs that an environment can reach. Each vCPU is equivalent to 1,024 CPU shares. You must specify at least one vCPU. Default: 256
        :param minv_cpus: (experimental) The minimum number of EC2 vCPUs that an environment should maintain (even if the compute environment state is DISABLED). Each vCPU is equivalent to 1,024 CPU shares. By keeping this set to 0 you will not have instance time wasted when there is no work to be run. If you set this above zero you will maintain that number of vCPUs at all times. Default: 0
        :param placement_group: (experimental) The Amazon EC2 placement group to associate with your compute resources. Default: - No placement group will be used.
        :param security_groups: (experimental) The EC2 security group(s) associated with instances launched in the compute environment. Default: - AWS default security group.
        :param spot_fleet_role: (experimental) This property will be ignored if you set the environment type to ON_DEMAND. The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a SPOT compute environment. For more information, see Amazon EC2 Spot Fleet Role in the AWS Batch User Guide. Default: - no fleet role will be used.
        :param type: (experimental) The type of compute environment: ON_DEMAND, SPOT, FARGATE, or FARGATE_SPOT. Default: ON_DEMAND
        :param vpc_subnets: (experimental) The VPC subnets into which the compute resources are launched. Default: - private subnets of the supplied VPC.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            
            my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
                compute_resources=batch.ComputeResources(
                    image=ecs.EcsOptimizedAmi(
                        generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                    ),
                    vpc=vpc
                )
            )
        '''
        if isinstance(launch_template, dict):
            launch_template = LaunchTemplateSpecification(**launch_template)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_67de8e8d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65d1d6f59471e724a007d30eb7dfaa63f8276fadedd726498ca966a8516f58a5)
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument allocation_strategy", value=allocation_strategy, expected_type=type_hints["allocation_strategy"])
            check_type(argname="argument bid_percentage", value=bid_percentage, expected_type=type_hints["bid_percentage"])
            check_type(argname="argument compute_resources_tags", value=compute_resources_tags, expected_type=type_hints["compute_resources_tags"])
            check_type(argname="argument desiredv_cpus", value=desiredv_cpus, expected_type=type_hints["desiredv_cpus"])
            check_type(argname="argument ec2_key_pair", value=ec2_key_pair, expected_type=type_hints["ec2_key_pair"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument instance_role", value=instance_role, expected_type=type_hints["instance_role"])
            check_type(argname="argument instance_types", value=instance_types, expected_type=type_hints["instance_types"])
            check_type(argname="argument launch_template", value=launch_template, expected_type=type_hints["launch_template"])
            check_type(argname="argument maxv_cpus", value=maxv_cpus, expected_type=type_hints["maxv_cpus"])
            check_type(argname="argument minv_cpus", value=minv_cpus, expected_type=type_hints["minv_cpus"])
            check_type(argname="argument placement_group", value=placement_group, expected_type=type_hints["placement_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument spot_fleet_role", value=spot_fleet_role, expected_type=type_hints["spot_fleet_role"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "vpc": vpc,
        }
        if allocation_strategy is not None:
            self._values["allocation_strategy"] = allocation_strategy
        if bid_percentage is not None:
            self._values["bid_percentage"] = bid_percentage
        if compute_resources_tags is not None:
            self._values["compute_resources_tags"] = compute_resources_tags
        if desiredv_cpus is not None:
            self._values["desiredv_cpus"] = desiredv_cpus
        if ec2_key_pair is not None:
            self._values["ec2_key_pair"] = ec2_key_pair
        if image is not None:
            self._values["image"] = image
        if instance_role is not None:
            self._values["instance_role"] = instance_role
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if launch_template is not None:
            self._values["launch_template"] = launch_template
        if maxv_cpus is not None:
            self._values["maxv_cpus"] = maxv_cpus
        if minv_cpus is not None:
            self._values["minv_cpus"] = minv_cpus
        if placement_group is not None:
            self._values["placement_group"] = placement_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if spot_fleet_role is not None:
            self._values["spot_fleet_role"] = spot_fleet_role
        if type is not None:
            self._values["type"] = type
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''(experimental) The VPC network that all compute resources will be connected to.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, result)

    @builtins.property
    def allocation_strategy(self) -> typing.Optional[AllocationStrategy]:
        '''(experimental) The allocation strategy to use for the compute resource in case not enough instances of the best fitting instance type can be allocated.

        This could be due to availability of the instance type in
        the region or Amazon EC2 service limits. If this is not specified, the default for the EC2
        ComputeResourceType is BEST_FIT, which will use only the best fitting instance type, waiting for
        additional capacity if it's not available. This allocation strategy keeps costs lower but can limit
        scaling. If you are using Spot Fleets with BEST_FIT then the Spot Fleet IAM Role must be specified.
        BEST_FIT_PROGRESSIVE will select an additional instance type that is large enough to meet the
        requirements of the jobs in the queue, with a preference for an instance type with a lower cost.
        The default value for the SPOT instance type is SPOT_CAPACITY_OPTIMIZED, which is only available for
        for this type of compute resources and will select an additional instance type that is large enough
        to meet the requirements of the jobs in the queue, with a preference for an instance type that is
        less likely to be interrupted.

        :default: AllocationStrategy.BEST_FIT

        :stability: experimental
        '''
        result = self._values.get("allocation_strategy")
        return typing.cast(typing.Optional[AllocationStrategy], result)

    @builtins.property
    def bid_percentage(self) -> typing.Optional[jsii.Number]:
        '''(experimental) This property will be ignored if you set the environment type to ON_DEMAND.

        The maximum percentage that a Spot Instance price can be when compared with the On-Demand price for
        that instance type before instances are launched. For example, if your maximum percentage is 20%,
        then the Spot price must be below 20% of the current On-Demand price for that EC2 instance. You always
        pay the lowest (market) price and never more than your maximum percentage. If you leave this field empty,
        the default value is 100% of the On-Demand price.

        :default: 100

        :stability: experimental
        '''
        result = self._values.get("bid_percentage")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def compute_resources_tags(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-value pair tags to be applied to resources that are launched in the compute environment.

        For AWS Batch, these take the form of "String1": "String2", where String1 is the tag key and
        String2 is the tag value—for example, { "Name": "AWS Batch Instance - C4OnDemand" }.

        :default: - no tags will be assigned on compute resources.

        :stability: experimental
        '''
        result = self._values.get("compute_resources_tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def desiredv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The desired number of EC2 vCPUS in the compute environment.

        :default: - no desired vcpu value will be used.

        :stability: experimental
        '''
        result = self._values.get("desiredv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ec2_key_pair(self) -> typing.Optional[builtins.str]:
        '''(experimental) The EC2 key pair that is used for instances launched in the compute environment.

        If no key is defined, then SSH access is not allowed to provisioned compute resources.

        :default: - no SSH access will be possible.

        :stability: experimental
        '''
        result = self._values.get("ec2_key_pair")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IMachineImage]:
        '''(experimental) The Amazon Machine Image (AMI) ID used for instances launched in the compute environment.

        :default: - no image will be used.

        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IMachineImage], result)

    @builtins.property
    def instance_role(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Amazon ECS instance profile applied to Amazon EC2 instances in a compute environment.

        You can specify
        the short name or full Amazon Resource Name (ARN) of an instance profile. For example, ecsInstanceRole or
        arn:aws:iam::<aws_account_id>:instance-profile/ecsInstanceRole . For more information, see Amazon ECS
        Instance Role in the AWS Batch User Guide.

        :default: - a new role will be created.

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/instance_IAM_role.html
        '''
        result = self._values.get("instance_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_types(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.InstanceType]]:
        '''(experimental) The types of EC2 instances that may be launched in the compute environment.

        You can specify instance
        families to launch any instance type within those families (for example, c4 or p3), or you can specify
        specific sizes within a family (such as c4.8xlarge). You can also choose optimal to pick instance types
        (from the C, M, and R instance families) on the fly that match the demand of your job queues.

        :default: optimal

        :stability: experimental
        '''
        result = self._values.get("instance_types")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.InstanceType]], result)

    @builtins.property
    def launch_template(self) -> typing.Optional["LaunchTemplateSpecification"]:
        '''(experimental) An optional launch template to associate with your compute resources.

        For more information, see README file.

        :default: - no custom launch template will be used

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/launch-templates.html
        '''
        result = self._values.get("launch_template")
        return typing.cast(typing.Optional["LaunchTemplateSpecification"], result)

    @builtins.property
    def maxv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of EC2 vCPUs that an environment can reach.

        Each vCPU is equivalent to
        1,024 CPU shares. You must specify at least one vCPU.

        :default: 256

        :stability: experimental
        '''
        result = self._values.get("maxv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minv_cpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum number of EC2 vCPUs that an environment should maintain (even if the compute environment state is DISABLED).

        Each vCPU is equivalent to 1,024 CPU shares. By keeping this set to 0 you will not have instance time wasted when
        there is no work to be run. If you set this above zero you will maintain that number of vCPUs at all times.

        :default: 0

        :stability: experimental
        '''
        result = self._values.get("minv_cpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def placement_group(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Amazon EC2 placement group to associate with your compute resources.

        :default: - No placement group will be used.

        :stability: experimental
        '''
        result = self._values.get("placement_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]]:
        '''(experimental) The EC2 security group(s) associated with instances launched in the compute environment.

        :default: - AWS default security group.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]], result)

    @builtins.property
    def spot_fleet_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) This property will be ignored if you set the environment type to ON_DEMAND.

        The Amazon Resource Name (ARN) of the Amazon EC2 Spot Fleet IAM role applied to a SPOT compute environment.
        For more information, see Amazon EC2 Spot Fleet Role in the AWS Batch User Guide.

        :default: - no fleet role will be used.

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/spot_fleet_IAM_role.html
        '''
        result = self._values.get("spot_fleet_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def type(self) -> typing.Optional[ComputeResourceType]:
        '''(experimental) The type of compute environment: ON_DEMAND, SPOT, FARGATE, or FARGATE_SPOT.

        :default: ON_DEMAND

        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[ComputeResourceType], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection]:
        '''(experimental) The VPC subnets into which the compute resources are launched.

        :default: - private subnets of the supplied VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComputeResources(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ExposedSecret(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.ExposedSecret",
):
    '''(experimental) Exposed secret for log configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ssm as ssm
        
        
        batch.JobDefinition(self, "job-def",
            container=batch.JobDefinitionContainer(
                image=ecs.EcrImage.from_registry("docker/whalesay"),
                log_configuration=batch.LogConfiguration(
                    log_driver=batch.LogDriver.AWSLOGS,
                    options={"awslogs-region": "us-east-1"},
                    secret_options=[
                        batch.ExposedSecret.from_parameters_store("xyz", ssm.StringParameter.from_string_parameter_name(self, "parameter", "xyz"))
                    ]
                )
            )
        )
    '''

    def __init__(self, option_name: builtins.str, secret_arn: builtins.str) -> None:
        '''
        :param option_name: -
        :param secret_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf444b6830a3c37bd1ea3f56c2f74ef441ed72e6b04d13891ef0df1e5bb0df0)
            check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
            check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
        jsii.create(self.__class__, self, [option_name, secret_arn])

    @jsii.member(jsii_name="fromParametersStore")
    @builtins.classmethod
    def from_parameters_store(
        cls,
        option_name: builtins.str,
        parameter: _aws_cdk_aws_ssm_1e9d799e.IParameter,
    ) -> "ExposedSecret":
        '''(experimental) User Parameters Store Parameter.

        :param option_name: - The name of the option.
        :param parameter: - A parameter from parameters store.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0acfdd28c190f00699a1359a250ee574c4fda31db85590a1908235d79926de9)
            check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        return typing.cast("ExposedSecret", jsii.sinvoke(cls, "fromParametersStore", [option_name, parameter]))

    @jsii.member(jsii_name="fromSecretsManager")
    @builtins.classmethod
    def from_secrets_manager(
        cls,
        option_name: builtins.str,
        secret: _aws_cdk_aws_secretsmanager_72af8d6f.ISecret,
    ) -> "ExposedSecret":
        '''(experimental) Use Secrets Manager Secret.

        :param option_name: - The name of the option.
        :param secret: - A secret from secrets manager.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7478244b9551787bd9b2436bea927603c98c0f3355a06230f5d2b2170e6862a9)
            check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        return typing.cast("ExposedSecret", jsii.sinvoke(cls, "fromSecretsManager", [option_name, secret]))

    @builtins.property
    @jsii.member(jsii_name="optionName")
    def option_name(self) -> builtins.str:
        '''(experimental) Name of the option.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "optionName"))

    @option_name.setter
    def option_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__079a44ba31d8a59ec41ad37e7e48f98bfb8a167d93d4367ee91512bc5787ed0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionName", value)

    @builtins.property
    @jsii.member(jsii_name="secretArn")
    def secret_arn(self) -> builtins.str:
        '''(experimental) ARN of the secret option.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "secretArn"))

    @secret_arn.setter
    def secret_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ad90a34744d2ab8f28910b6970f3e27c10876a0d3f586d8b752e85cd708dbfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "secretArn", value)


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IComputeEnvironment")
class IComputeEnvironment(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Properties of a compute environment.

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
        '''(experimental) The name of this compute environment.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IComputeEnvironmentProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Properties of a compute environment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IComputeEnvironment"

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
        '''(experimental) The name of this compute environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComputeEnvironment).__jsii_proxy_class__ = lambda : _IComputeEnvironmentProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IJobDefinition")
class IJobDefinition(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) An interface representing a job definition - either a new one, created with the CDK, *using the {@link JobDefinition} class, or existing ones, referenced using the {@link JobDefinition.fromJobDefinitionArn} method.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this batch job definition.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of the batch job definition.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IJobDefinitionProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) An interface representing a job definition - either a new one, created with the CDK, *using the {@link JobDefinition} class, or existing ones, referenced using the {@link JobDefinition.fromJobDefinitionArn} method.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IJobDefinition"

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this batch job definition.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionArn"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of the batch job definition.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobDefinition).__jsii_proxy_class__ = lambda : _IJobDefinitionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IJobQueue")
class IJobQueue(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Properties of a Job Queue.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this batch job queue.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        '''(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IJobQueueProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Properties of a Job Queue.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IJobQueue"

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this batch job queue.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueArn"))

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        '''(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IJobQueue).__jsii_proxy_class__ = lambda : _IJobQueueProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch.IMultiNodeProps")
class IMultiNodeProps(typing_extensions.Protocol):
    '''(experimental) Properties for specifying multi-node properties for compute resources.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        '''(experimental) The number of nodes associated with a multi-node parallel job.

        :stability: experimental
        '''
        ...

    @count.setter
    def count(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> jsii.Number:
        '''(experimental) Specifies the node index for the main node of a multi-node parallel job.

        This node index value must be fewer than the number of nodes.

        :stability: experimental
        '''
        ...

    @main_node.setter
    def main_node(self, value: jsii.Number) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="rangeProps")
    def range_props(self) -> typing.List["INodeRangeProps"]:
        '''(experimental) A list of node ranges and their properties associated with a multi-node parallel job.

        :stability: experimental
        '''
        ...

    @range_props.setter
    def range_props(self, value: typing.List["INodeRangeProps"]) -> None:
        ...


class _IMultiNodePropsProxy:
    '''(experimental) Properties for specifying multi-node properties for compute resources.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.IMultiNodeProps"

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> jsii.Number:
        '''(experimental) The number of nodes associated with a multi-node parallel job.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "count"))

    @count.setter
    def count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e5f97d09d498f1af7abc7fc9d1227db1dae50d19ec241bcf77b7e88328b6e92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="mainNode")
    def main_node(self) -> jsii.Number:
        '''(experimental) Specifies the node index for the main node of a multi-node parallel job.

        This node index value must be fewer than the number of nodes.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "mainNode"))

    @main_node.setter
    def main_node(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961416f58d1245c43f294c9adb44ad149127f6ea251e2af151b913926bae938c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mainNode", value)

    @builtins.property
    @jsii.member(jsii_name="rangeProps")
    def range_props(self) -> typing.List["INodeRangeProps"]:
        '''(experimental) A list of node ranges and their properties associated with a multi-node parallel job.

        :stability: experimental
        '''
        return typing.cast(typing.List["INodeRangeProps"], jsii.get(self, "rangeProps"))

    @range_props.setter
    def range_props(self, value: typing.List["INodeRangeProps"]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d63b7cdb37883f54096481a8db3fc4c27c224b08ca2ea11cb66c17092eb17e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rangeProps", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMultiNodeProps).__jsii_proxy_class__ = lambda : _IMultiNodePropsProxy


@jsii.interface(jsii_type="@aws-cdk/aws-batch.INodeRangeProps")
class INodeRangeProps(typing_extensions.Protocol):
    '''(experimental) Properties for a multi-node batch job.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> "JobDefinitionContainer":
        '''(experimental) The container details for the node range.

        :stability: experimental
        '''
        ...

    @container.setter
    def container(self, value: "JobDefinitionContainer") -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="fromNodeIndex")
    def from_node_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum node index value to apply this container definition against.

        You may nest node ranges, for example 0:10 and 4:5, in which case the 4:5 range properties override the 0:10 properties.

        :default: 0

        :stability: experimental
        '''
        ...

    @from_node_index.setter
    def from_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="toNodeIndex")
    def to_node_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum node index value to apply this container definition against. If omitted, the highest value is used relative.

        to the number of nodes associated with the job. You may nest node ranges, for example 0:10 and 4:5,
        in which case the 4:5 range properties override the 0:10 properties.

        :default: {@link IMultiNodeprops.count}

        :stability: experimental
        '''
        ...

    @to_node_index.setter
    def to_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        ...


class _INodeRangePropsProxy:
    '''(experimental) Properties for a multi-node batch job.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-batch.INodeRangeProps"

    @builtins.property
    @jsii.member(jsii_name="container")
    def container(self) -> "JobDefinitionContainer":
        '''(experimental) The container details for the node range.

        :stability: experimental
        '''
        return typing.cast("JobDefinitionContainer", jsii.get(self, "container"))

    @container.setter
    def container(self, value: "JobDefinitionContainer") -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef07a3cc73397dc52c31d5246652bdbff89e2ecfbd56777725fc0d4cc15df906)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "container", value)

    @builtins.property
    @jsii.member(jsii_name="fromNodeIndex")
    def from_node_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum node index value to apply this container definition against.

        You may nest node ranges, for example 0:10 and 4:5, in which case the 4:5 range properties override the 0:10 properties.

        :default: 0

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fromNodeIndex"))

    @from_node_index.setter
    def from_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c009fac035be99494cc36b3483ba8f78a585f4c8a85e576bad9cd4bce30588cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromNodeIndex", value)

    @builtins.property
    @jsii.member(jsii_name="toNodeIndex")
    def to_node_index(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum node index value to apply this container definition against. If omitted, the highest value is used relative.

        to the number of nodes associated with the job. You may nest node ranges, for example 0:10 and 4:5,
        in which case the 4:5 range properties override the 0:10 properties.

        :default: {@link IMultiNodeprops.count}

        :stability: experimental
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "toNodeIndex"))

    @to_node_index.setter
    def to_node_index(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03171da246a8befa529a66a7c73d299e5e1b2535eb131dcb23f43c0f42774464)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toNodeIndex", value)

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INodeRangeProps).__jsii_proxy_class__ = lambda : _INodeRangePropsProxy


@jsii.implements(IJobDefinition)
class JobDefinition(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.JobDefinition",
):
    '''(experimental) Batch Job Definition.

    Defines a batch job definition to execute a specific batch job.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ecr as ecr
        
        
        repo = ecr.Repository.from_repository_name(self, "batch-job-repo", "todo-list")
        
        batch.JobDefinition(self, "batch-job-def-from-ecr",
            container=batch.JobDefinitionContainer(
                image=ecs.EcrImage(repo, "latest")
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        container: typing.Union["JobDefinitionContainer", typing.Dict[builtins.str, typing.Any]],
        job_definition_name: typing.Optional[builtins.str] = None,
        node_props: typing.Optional[IMultiNodeProps] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform_capabilities: typing.Optional[typing.Sequence["PlatformCapabilities"]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param container: (experimental) An object with various properties specific to container-based jobs.
        :param job_definition_name: (experimental) The name of the job definition. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: Cloudformation-generated name
        :param node_props: (experimental) An object with various properties specific to multi-node parallel jobs. Default: - undefined
        :param parameters: (experimental) When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters. Parameters in job submission requests take precedence over the defaults in a job definition. This allows you to use the same job definition for multiple jobs that use the same format, and programmatically change values in the command at submission time. Default: - undefined
        :param platform_capabilities: (experimental) The platform capabilities required by the job definition. Default: - EC2
        :param retry_attempts: (experimental) The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param timeout: (experimental) The timeout configuration for jobs that are submitted with this job definition. You can specify a timeout duration after which AWS Batch terminates your jobs if they have not finished. Default: - undefined

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6db60780f36109c6c0914155c556375ad097f407c82cbcadadf25694a369f10)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobDefinitionProps(
            container=container,
            job_definition_name=job_definition_name,
            node_props=node_props,
            parameters=parameters,
            platform_capabilities=platform_capabilities,
            retry_attempts=retry_attempts,
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
        '''(experimental) Imports an existing batch job definition by its amazon resource name.

        :param scope: -
        :param id: -
        :param job_definition_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b41850089fd68272b72c3ac134ab5c9cee8169f9fa7dc046e2f4e0ca2f738ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_definition_arn", value=job_definition_arn, expected_type=type_hints["job_definition_arn"])
        return typing.cast(IJobDefinition, jsii.sinvoke(cls, "fromJobDefinitionArn", [scope, id, job_definition_arn]))

    @jsii.member(jsii_name="fromJobDefinitionName")
    @builtins.classmethod
    def from_job_definition_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        job_definition_name: builtins.str,
    ) -> IJobDefinition:
        '''(experimental) Imports an existing batch job definition by its name.

        If name is specified without a revision then the latest active revision is used.

        :param scope: -
        :param id: -
        :param job_definition_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2be081cb800d733e9351d4b28aa9719554b5f5a90043aa0dd11b6ad9e3376c7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
        return typing.cast(IJobDefinition, jsii.sinvoke(cls, "fromJobDefinitionName", [scope, id, job_definition_name]))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionArn")
    def job_definition_arn(self) -> builtins.str:
        '''(experimental) The ARN of this batch job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionArn"))

    @builtins.property
    @jsii.member(jsii_name="jobDefinitionName")
    def job_definition_name(self) -> builtins.str:
        '''(experimental) The name of the batch job definition.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobDefinitionName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobDefinitionContainer",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "assign_public_ip": "assignPublicIp",
        "command": "command",
        "environment": "environment",
        "execution_role": "executionRole",
        "gpu_count": "gpuCount",
        "instance_type": "instanceType",
        "job_role": "jobRole",
        "linux_params": "linuxParams",
        "log_configuration": "logConfiguration",
        "memory_limit_mib": "memoryLimitMiB",
        "mount_points": "mountPoints",
        "platform_version": "platformVersion",
        "privileged": "privileged",
        "read_only": "readOnly",
        "ulimits": "ulimits",
        "user": "user",
        "vcpus": "vcpus",
        "volumes": "volumes",
    },
)
class JobDefinitionContainer:
    def __init__(
        self,
        *,
        image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        command: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        gpu_count: typing.Optional[jsii.Number] = None,
        instance_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType] = None,
        job_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
        linux_params: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LinuxParameters] = None,
        log_configuration: typing.Optional[typing.Union["LogConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        mount_points: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.MountPoint, typing.Dict[builtins.str, typing.Any]]]] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
        privileged: typing.Optional[builtins.bool] = None,
        read_only: typing.Optional[builtins.bool] = None,
        ulimits: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.Ulimit, typing.Dict[builtins.str, typing.Any]]]] = None,
        user: typing.Optional[builtins.str] = None,
        vcpus: typing.Optional[jsii.Number] = None,
        volumes: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.Volume, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties of a job definition container.

        :param image: (experimental) The image used to start a container.
        :param assign_public_ip: (experimental) Whether or not to assign a public IP to the job. Default: - false
        :param command: (experimental) The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: (experimental) The environment variables to pass to the container. Default: none
        :param execution_role: (experimental) The IAM role that AWS Batch can assume. Required when using Fargate. Default: - None
        :param gpu_count: (experimental) The number of physical GPUs to reserve for the container. The number of GPUs reserved for all containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on. Default: - No GPU reservation.
        :param instance_type: (experimental) The instance type to use for a multi-node parallel job. Currently all node groups in a multi-node parallel job must use the same instance type. This parameter is not valid for single-node container jobs. Default: - None
        :param job_role: (experimental) The IAM role that the container can assume for AWS permissions. Default: - An IAM role will created.
        :param linux_params: (experimental) Linux-specific modifications that are applied to the container, such as details for device mappings. For now, only the ``devices`` property is supported. Default: - None will be used.
        :param log_configuration: (experimental) The log configuration specification for the container. Default: - containers use the same logging driver that the Docker daemon uses
        :param memory_limit_mib: (experimental) The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the memory specified here, the container is killed. You must specify at least 4 MiB of memory for EC2 and 512 MiB for Fargate. Default: - 4 for EC2, 512 for Fargate
        :param mount_points: (experimental) The mount points for data volumes in your container. Default: - No mount points will be used.
        :param platform_version: (experimental) Fargate platform version. Default: - LATEST platform version will be used
        :param privileged: (experimental) When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user). Default: false
        :param read_only: (experimental) When this parameter is true, the container is given read-only access to its root file system. Default: false
        :param ulimits: (experimental) A list of ulimits to set in the container. Default: - No limits.
        :param user: (experimental) The user name to use inside the container. Default: - None will be used.
        :param vcpus: (experimental) The number of vCPUs reserved for the container. Each vCPU is equivalent to 1,024 CPU shares. You must specify at least one vCPU for EC2 and 0.25 for Fargate. Default: - 1 for EC2, 0.25 for Fargate
        :param volumes: (experimental) A list of data volumes used in a job. Default: - No data volumes will be used.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ssm as ssm
            
            
            batch.JobDefinition(self, "job-def",
                container=batch.JobDefinitionContainer(
                    image=ecs.EcrImage.from_registry("docker/whalesay"),
                    log_configuration=batch.LogConfiguration(
                        log_driver=batch.LogDriver.AWSLOGS,
                        options={"awslogs-region": "us-east-1"},
                        secret_options=[
                            batch.ExposedSecret.from_parameters_store("xyz", ssm.StringParameter.from_string_parameter_name(self, "parameter", "xyz"))
                        ]
                    )
                )
            )
        '''
        if isinstance(log_configuration, dict):
            log_configuration = LogConfiguration(**log_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a7fb86fc0d39f59a00e5f1e1e0834ede0353f6c657b5ee7432a25ab66135ab)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument command", value=command, expected_type=type_hints["command"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument execution_role", value=execution_role, expected_type=type_hints["execution_role"])
            check_type(argname="argument gpu_count", value=gpu_count, expected_type=type_hints["gpu_count"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument job_role", value=job_role, expected_type=type_hints["job_role"])
            check_type(argname="argument linux_params", value=linux_params, expected_type=type_hints["linux_params"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument mount_points", value=mount_points, expected_type=type_hints["mount_points"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument read_only", value=read_only, expected_type=type_hints["read_only"])
            check_type(argname="argument ulimits", value=ulimits, expected_type=type_hints["ulimits"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument vcpus", value=vcpus, expected_type=type_hints["vcpus"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image": image,
        }
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if command is not None:
            self._values["command"] = command
        if environment is not None:
            self._values["environment"] = environment
        if execution_role is not None:
            self._values["execution_role"] = execution_role
        if gpu_count is not None:
            self._values["gpu_count"] = gpu_count
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if job_role is not None:
            self._values["job_role"] = job_role
        if linux_params is not None:
            self._values["linux_params"] = linux_params
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if mount_points is not None:
            self._values["mount_points"] = mount_points
        if platform_version is not None:
            self._values["platform_version"] = platform_version
        if privileged is not None:
            self._values["privileged"] = privileged
        if read_only is not None:
            self._values["read_only"] = read_only
        if ulimits is not None:
            self._values["ulimits"] = ulimits
        if user is not None:
            self._values["user"] = user
        if vcpus is not None:
            self._values["vcpus"] = vcpus
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> _aws_cdk_aws_ecs_7896c08f.ContainerImage:
        '''(experimental) The image used to start a container.

        :stability: experimental
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(_aws_cdk_aws_ecs_7896c08f.ContainerImage, result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to assign a public IP to the job.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def command(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        :default: - CMD value built into container image.

        :stability: experimental
        '''
        result = self._values.get("command")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The environment variables to pass to the container.

        :default: none

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def execution_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role that AWS Batch can assume.

        Required when using Fargate.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("execution_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def gpu_count(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of physical GPUs to reserve for the container.

        The number of GPUs reserved for all
        containers in a job should not exceed the number of available GPUs on the compute resource that the job is launched on.

        :default: - No GPU reservation.

        :stability: experimental
        '''
        result = self._values.get("gpu_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def instance_type(self) -> typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType]:
        '''(experimental) The instance type to use for a multi-node parallel job.

        Currently all node groups in a
        multi-node parallel job must use the same instance type. This parameter is not valid
        for single-node container jobs.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("instance_type")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType], result)

    @builtins.property
    def job_role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(experimental) The IAM role that the container can assume for AWS permissions.

        :default: - An IAM role will created.

        :stability: experimental
        '''
        result = self._values.get("job_role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    @builtins.property
    def linux_params(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.LinuxParameters]:
        '''(experimental) Linux-specific modifications that are applied to the container, such as details for device mappings.

        For now, only the ``devices`` property is supported.

        :default: - None will be used.

        :stability: experimental
        '''
        result = self._values.get("linux_params")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.LinuxParameters], result)

    @builtins.property
    def log_configuration(self) -> typing.Optional["LogConfiguration"]:
        '''(experimental) The log configuration specification for the container.

        :default: - containers use the same logging driver that the Docker daemon uses

        :stability: experimental
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional["LogConfiguration"], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed
        the memory specified here, the container is killed. You must specify at least 4 MiB of memory for EC2 and 512 MiB for Fargate.

        :default: - 4 for EC2, 512 for Fargate

        :stability: experimental
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def mount_points(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.MountPoint]]:
        '''(experimental) The mount points for data volumes in your container.

        :default: - No mount points will be used.

        :stability: experimental
        '''
        result = self._values.get("mount_points")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.MountPoint]], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion]:
        '''(experimental) Fargate platform version.

        :default: - LATEST platform version will be used

        :stability: experimental
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion], result)

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When this parameter is true, the container is given elevated privileges on the host container instance (similar to the root user).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def read_only(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When this parameter is true, the container is given read-only access to its root file system.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("read_only")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ulimits(self) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.Ulimit]]:
        '''(experimental) A list of ulimits to set in the container.

        :default: - No limits.

        :stability: experimental
        '''
        result = self._values.get("ulimits")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.Ulimit]], result)

    @builtins.property
    def user(self) -> typing.Optional[builtins.str]:
        '''(experimental) The user name to use inside the container.

        :default: - None will be used.

        :stability: experimental
        '''
        result = self._values.get("user")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vcpus(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of vCPUs reserved for the container.

        Each vCPU is equivalent to
        1,024 CPU shares. You must specify at least one vCPU for EC2 and 0.25 for Fargate.

        :default: - 1 for EC2, 0.25 for Fargate

        :stability: experimental
        '''
        result = self._values.get("vcpus")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.Volume]]:
        '''(experimental) A list of data volumes used in a job.

        :default: - No data volumes will be used.

        :stability: experimental
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_7896c08f.Volume]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefinitionContainer(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobDefinitionProps",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "job_definition_name": "jobDefinitionName",
        "node_props": "nodeProps",
        "parameters": "parameters",
        "platform_capabilities": "platformCapabilities",
        "retry_attempts": "retryAttempts",
        "timeout": "timeout",
    },
)
class JobDefinitionProps:
    def __init__(
        self,
        *,
        container: typing.Union[JobDefinitionContainer, typing.Dict[builtins.str, typing.Any]],
        job_definition_name: typing.Optional[builtins.str] = None,
        node_props: typing.Optional[IMultiNodeProps] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        platform_capabilities: typing.Optional[typing.Sequence["PlatformCapabilities"]] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> None:
        '''(experimental) Construction properties of the {@link JobDefinition} construct.

        :param container: (experimental) An object with various properties specific to container-based jobs.
        :param job_definition_name: (experimental) The name of the job definition. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: Cloudformation-generated name
        :param node_props: (experimental) An object with various properties specific to multi-node parallel jobs. Default: - undefined
        :param parameters: (experimental) When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters. Parameters in job submission requests take precedence over the defaults in a job definition. This allows you to use the same job definition for multiple jobs that use the same format, and programmatically change values in the command at submission time. Default: - undefined
        :param platform_capabilities: (experimental) The platform capabilities required by the job definition. Default: - EC2
        :param retry_attempts: (experimental) The number of times to move a job to the RUNNABLE status. You may specify between 1 and 10 attempts. If the value of attempts is greater than one, the job is retried on failure the same number of attempts as the value. Default: 1
        :param timeout: (experimental) The timeout configuration for jobs that are submitted with this job definition. You can specify a timeout duration after which AWS Batch terminates your jobs if they have not finished. Default: - undefined

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ssm as ssm
            
            
            batch.JobDefinition(self, "job-def",
                container=batch.JobDefinitionContainer(
                    image=ecs.EcrImage.from_registry("docker/whalesay"),
                    log_configuration=batch.LogConfiguration(
                        log_driver=batch.LogDriver.AWSLOGS,
                        options={"awslogs-region": "us-east-1"},
                        secret_options=[
                            batch.ExposedSecret.from_parameters_store("xyz", ssm.StringParameter.from_string_parameter_name(self, "parameter", "xyz"))
                        ]
                    )
                )
            )
        '''
        if isinstance(container, dict):
            container = JobDefinitionContainer(**container)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fa972272cb531d13e06acde1da4d0a48676283a04d603a5ebf86c369f0cb141)
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument job_definition_name", value=job_definition_name, expected_type=type_hints["job_definition_name"])
            check_type(argname="argument node_props", value=node_props, expected_type=type_hints["node_props"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument platform_capabilities", value=platform_capabilities, expected_type=type_hints["platform_capabilities"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container": container,
        }
        if job_definition_name is not None:
            self._values["job_definition_name"] = job_definition_name
        if node_props is not None:
            self._values["node_props"] = node_props
        if parameters is not None:
            self._values["parameters"] = parameters
        if platform_capabilities is not None:
            self._values["platform_capabilities"] = platform_capabilities
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def container(self) -> JobDefinitionContainer:
        '''(experimental) An object with various properties specific to container-based jobs.

        :stability: experimental
        '''
        result = self._values.get("container")
        assert result is not None, "Required property 'container' is missing"
        return typing.cast(JobDefinitionContainer, result)

    @builtins.property
    def job_definition_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the job definition.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :default: Cloudformation-generated name

        :stability: experimental
        '''
        result = self._values.get("job_definition_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_props(self) -> typing.Optional[IMultiNodeProps]:
        '''(experimental) An object with various properties specific to multi-node parallel jobs.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("node_props")
        return typing.cast(typing.Optional[IMultiNodeProps], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) When you submit a job, you can specify parameters that should replace the placeholders or override the default job definition parameters.

        Parameters
        in job submission requests take precedence over the defaults in a job definition.
        This allows you to use the same job definition for multiple jobs that use the same
        format, and programmatically change values in the command at submission time.

        :default: - undefined

        :stability: experimental
        :link: https://docs.aws.amazon.com/batch/latest/userguide/job_definition_parameters.html
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def platform_capabilities(
        self,
    ) -> typing.Optional[typing.List["PlatformCapabilities"]]:
        '''(experimental) The platform capabilities required by the job definition.

        :default: - EC2

        :stability: experimental
        '''
        result = self._values.get("platform_capabilities")
        return typing.cast(typing.Optional[typing.List["PlatformCapabilities"]], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The number of times to move a job to the RUNNABLE status.

        You may specify between 1 and
        10 attempts. If the value of attempts is greater than one, the job is retried on failure
        the same number of attempts as the value.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) The timeout configuration for jobs that are submitted with this job definition.

        You can specify
        a timeout duration after which AWS Batch terminates your jobs if they have not finished.

        :default: - undefined

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

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
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.JobQueue",
):
    '''(experimental) Batch Job Queue.

    Defines a batch job queue to define how submitted batch jobs
    should be ran based on specified batch compute environments.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # shared_compute_envs: batch.ComputeEnvironment
        
        high_prio_queue = batch.JobQueue(self, "JobQueue",
            compute_environments=[batch.JobQueueComputeEnvironment(
                compute_environment=shared_compute_envs,
                order=1
            )],
            priority=2
        )
        
        low_prio_queue = batch.JobQueue(self, "JobQueue",
            compute_environments=[batch.JobQueueComputeEnvironment(
                compute_environment=shared_compute_envs,
                order=1
            )],
            priority=1
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_environments: typing.Sequence[typing.Union["JobQueueComputeEnvironment", typing.Dict[builtins.str, typing.Any]]],
        enabled: typing.Optional[builtins.bool] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_environments: (experimental) The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
        :param enabled: (experimental) The state of the job queue. If set to true, it is able to accept jobs. Default: true
        :param job_queue_name: (experimental) A name for the job queue. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - Cloudformation-generated name
        :param priority: (experimental) The priority of the job queue. Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1. Default: 1

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfd49c95e3f6aad58cb8cbecd81984130f9fccc646ce1b993e6d691fa77e6434)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JobQueueProps(
            compute_environments=compute_environments,
            enabled=enabled,
            job_queue_name=job_queue_name,
            priority=priority,
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
        '''(experimental) Fetches an existing batch job queue by its amazon resource name.

        :param scope: -
        :param id: -
        :param job_queue_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1351d7084272383ee85ae7b25f9bcf1a4f812160acc1b98a5f3c0acec7369276)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument job_queue_arn", value=job_queue_arn, expected_type=type_hints["job_queue_arn"])
        return typing.cast(IJobQueue, jsii.sinvoke(cls, "fromJobQueueArn", [scope, id, job_queue_arn]))

    @builtins.property
    @jsii.member(jsii_name="jobQueueArn")
    def job_queue_arn(self) -> builtins.str:
        '''(experimental) The ARN of this batch job queue.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueArn"))

    @builtins.property
    @jsii.member(jsii_name="jobQueueName")
    def job_queue_name(self) -> builtins.str:
        '''(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "jobQueueName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobQueueComputeEnvironment",
    jsii_struct_bases=[],
    name_mapping={"compute_environment": "computeEnvironment", "order": "order"},
)
class JobQueueComputeEnvironment:
    def __init__(
        self,
        *,
        compute_environment: IComputeEnvironment,
        order: jsii.Number,
    ) -> None:
        '''(experimental) Properties for mapping a compute environment to a job queue.

        :param compute_environment: (experimental) The batch compute environment to use for processing submitted jobs to this queue.
        :param order: (experimental) The order in which this compute environment will be selected for dynamic allocation of resources to process submitted jobs.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_batch as batch
            
            # compute_environment: batch.ComputeEnvironment
            
            job_queue_compute_environment = batch.JobQueueComputeEnvironment(
                compute_environment=compute_environment,
                order=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1049c098b4510fd4f91b4a80fd0ee0db14d9de161e6d8fa24e1a29a9d5c21bd9)
            check_type(argname="argument compute_environment", value=compute_environment, expected_type=type_hints["compute_environment"])
            check_type(argname="argument order", value=order, expected_type=type_hints["order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_environment": compute_environment,
            "order": order,
        }

    @builtins.property
    def compute_environment(self) -> IComputeEnvironment:
        '''(experimental) The batch compute environment to use for processing submitted jobs to this queue.

        :stability: experimental
        '''
        result = self._values.get("compute_environment")
        assert result is not None, "Required property 'compute_environment' is missing"
        return typing.cast(IComputeEnvironment, result)

    @builtins.property
    def order(self) -> jsii.Number:
        '''(experimental) The order in which this compute environment will be selected for dynamic allocation of resources to process submitted jobs.

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
        return "JobQueueComputeEnvironment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.JobQueueProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_environments": "computeEnvironments",
        "enabled": "enabled",
        "job_queue_name": "jobQueueName",
        "priority": "priority",
    },
)
class JobQueueProps:
    def __init__(
        self,
        *,
        compute_environments: typing.Sequence[typing.Union[JobQueueComputeEnvironment, typing.Dict[builtins.str, typing.Any]]],
        enabled: typing.Optional[builtins.bool] = None,
        job_queue_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Properties of a batch job queue.

        :param compute_environments: (experimental) The set of compute environments mapped to a job queue and their order relative to each other. The job scheduler uses this parameter to determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them with a job queue. You can associate up to three compute environments with a job queue.
        :param enabled: (experimental) The state of the job queue. If set to true, it is able to accept jobs. Default: true
        :param job_queue_name: (experimental) A name for the job queue. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - Cloudformation-generated name
        :param priority: (experimental) The priority of the job queue. Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value of 10 is given scheduling preference over a job queue with a priority value of 1. Default: 1

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # shared_compute_envs: batch.ComputeEnvironment
            
            high_prio_queue = batch.JobQueue(self, "JobQueue",
                compute_environments=[batch.JobQueueComputeEnvironment(
                    compute_environment=shared_compute_envs,
                    order=1
                )],
                priority=2
            )
            
            low_prio_queue = batch.JobQueue(self, "JobQueue",
                compute_environments=[batch.JobQueueComputeEnvironment(
                    compute_environment=shared_compute_envs,
                    order=1
                )],
                priority=1
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08940a1fda209fa6d0a451eff3fd33e053ae672e99e3cb8f73e51e8877dfb76a)
            check_type(argname="argument compute_environments", value=compute_environments, expected_type=type_hints["compute_environments"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument job_queue_name", value=job_queue_name, expected_type=type_hints["job_queue_name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "compute_environments": compute_environments,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if job_queue_name is not None:
            self._values["job_queue_name"] = job_queue_name
        if priority is not None:
            self._values["priority"] = priority

    @builtins.property
    def compute_environments(self) -> typing.List[JobQueueComputeEnvironment]:
        '''(experimental) The set of compute environments mapped to a job queue and their order relative to each other.

        The job scheduler uses this parameter to
        determine which compute environment should execute a given job. Compute environments must be in the VALID state before you can associate them
        with a job queue. You can associate up to three compute environments with a job queue.

        :stability: experimental
        '''
        result = self._values.get("compute_environments")
        assert result is not None, "Required property 'compute_environments' is missing"
        return typing.cast(typing.List[JobQueueComputeEnvironment], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) The state of the job queue.

        If set to true, it is able to accept jobs.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def job_queue_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the job queue.

        Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed.

        :default: - Cloudformation-generated name

        :stability: experimental
        '''
        result = self._values.get("job_queue_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The priority of the job queue.

        Job queues with a higher priority (or a higher integer value for the priority parameter) are evaluated first
        when associated with the same compute environment. Priority is determined in descending order, for example, a job queue with a priority value
        of 10 is given scheduling preference over a job queue with a priority value of 1.

        :default: 1

        :stability: experimental
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobQueueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.LaunchTemplateSpecification",
    jsii_struct_bases=[],
    name_mapping={"launch_template_name": "launchTemplateName", "version": "version"},
)
class LaunchTemplateSpecification:
    def __init__(
        self,
        *,
        launch_template_name: builtins.str,
        version: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Launch template property specification.

        :param launch_template_name: (experimental) The Launch template name.
        :param version: (experimental) The launch template version to be used (optional). Default: - the default version of the launch template

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            # my_launch_template: ec2.CfnLaunchTemplate
            
            
            my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
                compute_resources=batch.ComputeResources(
                    launch_template=batch.LaunchTemplateSpecification(
                        launch_template_name=my_launch_template.launch_template_name
                    ),
                    vpc=vpc
                ),
                compute_environment_name="MyStorageCapableComputeEnvironment"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40b697492dedf22ff3d1629d0837d575b0bdb27e02bdf4387dcdad8b0da2e896)
            check_type(argname="argument launch_template_name", value=launch_template_name, expected_type=type_hints["launch_template_name"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "launch_template_name": launch_template_name,
        }
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def launch_template_name(self) -> builtins.str:
        '''(experimental) The Launch template name.

        :stability: experimental
        '''
        result = self._values.get("launch_template_name")
        assert result is not None, "Required property 'launch_template_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The launch template version to be used (optional).

        :default: - the default version of the launch template

        :stability: experimental
        '''
        result = self._values.get("version")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LaunchTemplateSpecification(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-batch.LogConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "log_driver": "logDriver",
        "options": "options",
        "secret_options": "secretOptions",
    },
)
class LogConfiguration:
    def __init__(
        self,
        *,
        log_driver: "LogDriver",
        options: typing.Any = None,
        secret_options: typing.Optional[typing.Sequence[ExposedSecret]] = None,
    ) -> None:
        '''(experimental) Log configuration options to send to a custom log driver for the container.

        :param log_driver: (experimental) The log driver to use for the container.
        :param options: (experimental) The configuration options to send to the log driver. Default: - No configuration options are sent
        :param secret_options: (experimental) The secrets to pass to the log configuration as options. For more information, see https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data-secrets.html#secrets-logconfig Default: - No secrets are passed

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ssm as ssm
            
            
            batch.JobDefinition(self, "job-def",
                container=batch.JobDefinitionContainer(
                    image=ecs.EcrImage.from_registry("docker/whalesay"),
                    log_configuration=batch.LogConfiguration(
                        log_driver=batch.LogDriver.AWSLOGS,
                        options={"awslogs-region": "us-east-1"},
                        secret_options=[
                            batch.ExposedSecret.from_parameters_store("xyz", ssm.StringParameter.from_string_parameter_name(self, "parameter", "xyz"))
                        ]
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7959a77ca17c46379418110fc7173feb55c9a61f7cd7c806f8964b8f520d9dc8)
            check_type(argname="argument log_driver", value=log_driver, expected_type=type_hints["log_driver"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument secret_options", value=secret_options, expected_type=type_hints["secret_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log_driver": log_driver,
        }
        if options is not None:
            self._values["options"] = options
        if secret_options is not None:
            self._values["secret_options"] = secret_options

    @builtins.property
    def log_driver(self) -> "LogDriver":
        '''(experimental) The log driver to use for the container.

        :stability: experimental
        '''
        result = self._values.get("log_driver")
        assert result is not None, "Required property 'log_driver' is missing"
        return typing.cast("LogDriver", result)

    @builtins.property
    def options(self) -> typing.Any:
        '''(experimental) The configuration options to send to the log driver.

        :default: - No configuration options are sent

        :stability: experimental
        '''
        result = self._values.get("options")
        return typing.cast(typing.Any, result)

    @builtins.property
    def secret_options(self) -> typing.Optional[typing.List[ExposedSecret]]:
        '''(experimental) The secrets to pass to the log configuration as options.

        For more information, see https://docs.aws.amazon.com/batch/latest/userguide/specifying-sensitive-data-secrets.html#secrets-logconfig

        :default: - No secrets are passed

        :stability: experimental
        '''
        result = self._values.get("secret_options")
        return typing.cast(typing.Optional[typing.List[ExposedSecret]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LogConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-batch.LogDriver")
class LogDriver(enum.Enum):
    '''(experimental) The log driver to use for the container.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ssm as ssm
        
        
        batch.JobDefinition(self, "job-def",
            container=batch.JobDefinitionContainer(
                image=ecs.EcrImage.from_registry("docker/whalesay"),
                log_configuration=batch.LogConfiguration(
                    log_driver=batch.LogDriver.AWSLOGS,
                    options={"awslogs-region": "us-east-1"},
                    secret_options=[
                        batch.ExposedSecret.from_parameters_store("xyz", ssm.StringParameter.from_string_parameter_name(self, "parameter", "xyz"))
                    ]
                )
            )
        )
    '''

    AWSLOGS = "AWSLOGS"
    '''(experimental) Specifies the Amazon CloudWatch Logs logging driver.

    :stability: experimental
    '''
    FLUENTD = "FLUENTD"
    '''(experimental) Specifies the Fluentd logging driver.

    :stability: experimental
    '''
    GELF = "GELF"
    '''(experimental) Specifies the Graylog Extended Format (GELF) logging driver.

    :stability: experimental
    '''
    JOURNALD = "JOURNALD"
    '''(experimental) Specifies the journald logging driver.

    :stability: experimental
    '''
    LOGENTRIES = "LOGENTRIES"
    '''(experimental) Specifies the logentries logging driver.

    :stability: experimental
    '''
    JSON_FILE = "JSON_FILE"
    '''(experimental) Specifies the JSON file logging driver.

    :stability: experimental
    '''
    SPLUNK = "SPLUNK"
    '''(experimental) Specifies the Splunk logging driver.

    :stability: experimental
    '''
    SYSLOG = "SYSLOG"
    '''(experimental) Specifies the syslog logging driver.

    :stability: experimental
    '''


@jsii.enum(jsii_type="@aws-cdk/aws-batch.PlatformCapabilities")
class PlatformCapabilities(enum.Enum):
    '''(experimental) Platform capabilities.

    :stability: experimental
    '''

    EC2 = "EC2"
    '''(experimental) Specifies EC2 environment.

    :stability: experimental
    '''
    FARGATE = "FARGATE"
    '''(experimental) Specifies Fargate environment.

    :stability: experimental
    '''


@jsii.implements(IComputeEnvironment)
class ComputeEnvironment(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-batch.ComputeEnvironment",
):
    '''(experimental) Batch Compute Environment.

    Defines a batch compute environment to run batch jobs on.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # vpc: ec2.Vpc
        
        my_compute_env = batch.ComputeEnvironment(self, "ComputeEnv",
            compute_resources=batch.ComputeResources(
                image=ecs.EcsOptimizedAmi(
                    generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2
                ),
                vpc=vpc
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_environment_name: typing.Optional[builtins.str] = None,
        compute_resources: typing.Optional[typing.Union[ComputeResources, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        managed: typing.Optional[builtins.bool] = None,
        service_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_environment_name: (experimental) A name for the compute environment. Up to 128 letters (uppercase and lowercase), numbers, hyphens, and underscores are allowed. Default: - CloudFormation-generated name
        :param compute_resources: (experimental) The details of the required compute resources for the managed compute environment. If specified, and this is an unmanaged compute environment, will throw an error. By default, AWS Batch managed compute environments use a recent, approved version of the Amazon ECS-optimized AMI for compute resources. Default: - CloudFormation defaults
        :param enabled: (experimental) The state of the compute environment. If the state is set to true, then the compute environment accepts jobs from a queue and can scale out automatically based on queues. Default: true
        :param managed: (experimental) Determines if AWS should manage the allocation of compute resources for processing jobs. If set to false, then you are in charge of providing the compute resource details. Default: true
        :param service_role: (experimental) The IAM role used by Batch to make calls to other AWS services on your behalf for managing the resources that you use with the service. By default, this role is created for you using the AWS managed service policy for Batch. Default: - Role using the 'service-role/AWSBatchServiceRole' policy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__585b81e40fcc982c3c9cbb15cd4d566a5c43af3b6df9e20f412d5c7e000ba012)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ComputeEnvironmentProps(
            compute_environment_name=compute_environment_name,
            compute_resources=compute_resources,
            enabled=enabled,
            managed=managed,
            service_role=service_role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromComputeEnvironmentArn")
    @builtins.classmethod
    def from_compute_environment_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        compute_environment_arn: builtins.str,
    ) -> IComputeEnvironment:
        '''(experimental) Fetches an existing batch compute environment by its amazon resource name.

        :param scope: -
        :param id: -
        :param compute_environment_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70162245124335067837158534d16fcc55b46ea780fb49a4fa7db3117ac4f6c2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument compute_environment_arn", value=compute_environment_arn, expected_type=type_hints["compute_environment_arn"])
        return typing.cast(IComputeEnvironment, jsii.sinvoke(cls, "fromComputeEnvironmentArn", [scope, id, compute_environment_arn]))

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
        '''(experimental) The name of this compute environment.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "computeEnvironmentName"))


__all__ = [
    "AllocationStrategy",
    "CfnComputeEnvironment",
    "CfnComputeEnvironmentProps",
    "CfnJobDefinition",
    "CfnJobDefinitionProps",
    "CfnJobQueue",
    "CfnJobQueueProps",
    "CfnSchedulingPolicy",
    "CfnSchedulingPolicyProps",
    "ComputeEnvironment",
    "ComputeEnvironmentProps",
    "ComputeResourceType",
    "ComputeResources",
    "ExposedSecret",
    "IComputeEnvironment",
    "IJobDefinition",
    "IJobQueue",
    "IMultiNodeProps",
    "INodeRangeProps",
    "JobDefinition",
    "JobDefinitionContainer",
    "JobDefinitionProps",
    "JobQueue",
    "JobQueueComputeEnvironment",
    "JobQueueProps",
    "LaunchTemplateSpecification",
    "LogConfiguration",
    "LogDriver",
    "PlatformCapabilities",
]

publication.publish()

def _typecheckingstub__1f2cbf692bbd14fb1bd48d457b8474146c99da23d24f5a1cc3dac848f9787b8e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    type: builtins.str,
    compute_environment_name: typing.Optional[builtins.str] = None,
    compute_resources: typing.Optional[typing.Union[typing.Union[CfnComputeEnvironment.ComputeResourcesProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    eks_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.EksConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replace_compute_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    service_role: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    unmanagedv_cpus: typing.Optional[jsii.Number] = None,
    update_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.UpdatePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd974725cb49c9198b63049aeb87de5804a7ab99d9894cf93d84ad1c0767238(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2e0b0511cbf14c7e45ca90e00b700eb3bd8367007555ed2b4545bac6315ccd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b60d178d17433dacbd973f4a52d87d5b724639882d584c63260fe7cd2a1c1cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b59c000947b3ca506f2753af800b18959bdd14f83cd8ec8fe42a5c2b68fee9b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8168068cfbbef0a4b43390a3a6e230b3cbea310ee59afb681e4465aed9eabea(
    value: typing.Optional[typing.Union[CfnComputeEnvironment.ComputeResourcesProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b8a811119a9bc2a47bb57e7b87f12807667d14844ddcbaa64b977914a8b2ddf(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComputeEnvironment.EksConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19948d8357991cc3039673852ff520831c4a6b397cbee41699d9ffba81463151(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2b2600d383f72b2ef58c9f3a532a74d0fde77403f873923cb9ddbd4b3b217c2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e41aa9107af2cab70ae1955cb7f76fc2c055e39c29573e227b21359c63a5f1f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811decbaf1eb9a8f02657685e6247a7f53a70c8379d47ecbdc670a1fc577b347(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4782916fb7fd0274a3412ccf21812e95b96a5ebc03d67359ef15eb3d86690480(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnComputeEnvironment.UpdatePolicyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52ba8fff15f28c08cee5d63b61572d65e0cbe72d0cf24f85e4e50d2a2547910(
    *,
    maxv_cpus: jsii.Number,
    subnets: typing.Sequence[builtins.str],
    type: builtins.str,
    allocation_strategy: typing.Optional[builtins.str] = None,
    bid_percentage: typing.Optional[jsii.Number] = None,
    desiredv_cpus: typing.Optional[jsii.Number] = None,
    ec2_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.Ec2ConfigurationObjectProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ec2_key_pair: typing.Optional[builtins.str] = None,
    image_id: typing.Optional[builtins.str] = None,
    instance_role: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    launch_template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.LaunchTemplateSpecificationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    spot_iam_fleet_role: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    update_to_latest_image_version: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6335daee74ef7fe5510815efefc031b5dce197755b59328823d11a4c255d1fcc(
    *,
    image_type: builtins.str,
    image_id_override: typing.Optional[builtins.str] = None,
    image_kubernetes_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c6c485947f145511982cdf4fbb8da610e181cc7ef984298d438a09c767d796(
    *,
    eks_cluster_arn: builtins.str,
    kubernetes_namespace: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d04f3237de0943c7f0f5becf9745ad232016e6c97fce1ca392b6c908b52d81(
    *,
    launch_template_id: typing.Optional[builtins.str] = None,
    launch_template_name: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75d7bc40febb29f50ea904aa6b5893aab138ad295bdc26efc9d8ab839650779c(
    *,
    job_execution_timeout_minutes: typing.Optional[jsii.Number] = None,
    terminate_jobs_on_update: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44457c64a729c5ff982fbfb1f21de15729c324ca632e1f48a3a7933efb884449(
    *,
    type: builtins.str,
    compute_environment_name: typing.Optional[builtins.str] = None,
    compute_resources: typing.Optional[typing.Union[typing.Union[CfnComputeEnvironment.ComputeResourcesProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    eks_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.EksConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    replace_compute_environment: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    service_role: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    unmanagedv_cpus: typing.Optional[jsii.Number] = None,
    update_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnComputeEnvironment.UpdatePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09ec8de6705a545cf0dec395d0428610a6f30e1c3153ac78de0972e161cff8c0(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    type: builtins.str,
    container_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.ContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    eks_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_definition_name: typing.Optional[builtins.str] = None,
    node_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.NodePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Any = None,
    platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    propagate_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    retry_strategy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.RetryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.TimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffdf3b83891dcd061b21f73c6403b713c55d8cb2ce0db150ac5fa995ce05670(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f1ea088ac0f6d10a55174546a8eb88016b0fff39aeccac98484a09241ff046(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19e9fa72412a02a0d36931c48e44d3a4c64e4fa474774278451f6060c3b9381(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865988743dae3f2c3b28bfc650692f8ddaf678f4a06c29ee10d04665c39d86ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa8a665ac0fc4175e4adeca0bd949ee7ece31bcc1e1d67f54315ea25959f0fc8(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.ContainerPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97f6e506a82a2e83baefa91b15a94232c42c77f069f25c68a722bc1ed1a10538(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.EksPropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a19ff7605217bedc6be9604fa338eb995376f0ee7155377d9595d6108ba3a5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b569e80dc519f1dac44b9d64419f86adc8ee9c828c95bf9aa7fffe90581323(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.NodePropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a28268df731ecd0c6d2cba57b1762312c312552ae37915fbb6bf8a9202cfcf(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6d8a7f5d85c48fd8a8369e01a8119bf08c42762b1156908d486b6cdfaeb517(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82ccabeb4142f8f6d7aaedcee1a0c7e28e55c32f9b5f1b5478ec0e65fedb00f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.RetryStrategyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad2894dcbaf9ddb7e0e81e5e04176379ff49c8ab7a9fa7b0c1b8a2886454383b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a6af6e67e7a9f429c0ea70b5d8f10e14b564dff12df6c8f8fb22167ab82b1e2(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobDefinition.TimeoutProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6dd1959b1c99e09ca004083b9c3b4a1da0f9c22ce44fde15de0a86bd4c8d570(
    *,
    access_point_id: typing.Optional[builtins.str] = None,
    iam: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c36bec7bbd2f351d26a8cf8b78efbd8f28320eb8ab212dfbc506e1eaeeb3f271(
    *,
    image: builtins.str,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EnvironmentProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ephemeral_storage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EphemeralStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    fargate_platform_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.FargatePlatformConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    instance_type: typing.Optional[builtins.str] = None,
    job_role_arn: typing.Optional[builtins.str] = None,
    linux_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.LinuxParametersProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.LogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    memory: typing.Optional[jsii.Number] = None,
    mount_points: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.MountPointsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    readonly_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    resource_requirements: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.ResourceRequirementProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    secrets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.SecretProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ulimits: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.UlimitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    user: typing.Optional[builtins.str] = None,
    vcpus: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.VolumesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35fe4ef9664bfaf270ea5abc9abf4321ad3f4a2efd4baa5b171bad4edefb04e0(
    *,
    container_path: typing.Optional[builtins.str] = None,
    host_path: typing.Optional[builtins.str] = None,
    permissions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfbc9b547d661e2143ab9658d20564fb7843f0e04ae5735703f79fa3b0163a4(
    *,
    file_system_id: builtins.str,
    authorization_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.AuthorizationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    root_directory: typing.Optional[builtins.str] = None,
    transit_encryption: typing.Optional[builtins.str] = None,
    transit_encryption_port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5102752e15e97c347ddb868c096e52cbf237ad566b130f28bb70cdf3332131b7(
    *,
    name: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07330371bcb1f8637f0ce902c267671a26ddf915f0287a6c9ff05e28baa8ff7b(
    *,
    image: builtins.str,
    args: typing.Optional[typing.Sequence[builtins.str]] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    env: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksContainerEnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    image_pull_policy: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.ResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_context: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.SecurityContextProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_mounts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksContainerVolumeMountProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a561e3828d7cfb4c75e48064ea5d673ac3360be196c55629ccb243d5c9977b(
    *,
    mount_path: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f6833a85c1a2916f4d0d61c549a2b582b50946cf34bb122cde97a47f3f3630d(
    *,
    pod_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.PodPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4237d0f232d47de96690769028656e53b44f46fd8b8c5b7fa035950da743f230(
    *,
    secret_name: builtins.str,
    optional: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eae87049527466b1696763e1e45d7ec09d103e7024a3169413fb2ae04dd416f7(
    *,
    name: builtins.str,
    empty_dir: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EmptyDirProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    host_path: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.HostPathProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    secret: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksSecretProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c8a07cc209d3d279842fe570b9d019970da5ec93fccc438f8af3d2f7cbb879f(
    *,
    medium: typing.Optional[builtins.str] = None,
    size_limit: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35292326ef6167cd330db6c2deab88c160e3b1819b5bb6f6701ea805fb6478f(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__971954cc156e97f6afe9dc7b1bb2f996b4209307a00baf0f98e9dbc4c48825c6(
    *,
    size_in_gib: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e8e95b83645d5ca87bdedddfcb79d63524285a5b71dc7be8c3882493a745153(
    *,
    action: builtins.str,
    on_exit_code: typing.Optional[builtins.str] = None,
    on_reason: typing.Optional[builtins.str] = None,
    on_status_reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cf55719603ebb0ac170c1a33148643ba787476040be52aea0bce84c013d05f(
    *,
    platform_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d46aaf98c27d80f22140cee98dfbee6e1fb9bd31f85be5de4ebd19cce173eb6(
    *,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6518edf5760938a62889b149467428ec12ba500342066833b437008ff0b6db06(
    *,
    devices: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.DeviceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    init_process_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    max_swap: typing.Optional[jsii.Number] = None,
    shared_memory_size: typing.Optional[jsii.Number] = None,
    swappiness: typing.Optional[jsii.Number] = None,
    tmpfs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.TmpfsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d14a86920d47896d42fc0ded7f8a8908d69ffbbbeff807e371d96f6dd4425a8c(
    *,
    log_driver: builtins.str,
    options: typing.Any = None,
    secret_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.SecretProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31621d3ff7016700af15f9c5ff125711ef60901884dc470945d8f4f839861aff(
    *,
    labels: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c079302185b99b4fa3cd459368854d06d0d90ee703847212f02b6b7733b03c4(
    *,
    container_path: typing.Optional[builtins.str] = None,
    read_only: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    source_volume: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157c880493ccc742e54423b3430b89dd94c48c69fa5e070b6a961bf0342da08c(
    *,
    assign_public_ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd3eb2cc497ae286475a2cb668997daea0e7618383362d61443f39093012a55(
    *,
    main_node: jsii.Number,
    node_range_properties: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.NodeRangePropertyProperty, typing.Dict[builtins.str, typing.Any]]]]],
    num_nodes: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3d1407f741b2c7cb684b73fd954f9df2434b5c6382c0dc6a1939f4ff3bbe6d(
    *,
    target_nodes: builtins.str,
    container: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.ContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc82a59dd1f31175037081efef47fcd96e8a6831b408bdc5dbbff446e85c77a(
    *,
    containers: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksContainerProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    dns_policy: typing.Optional[builtins.str] = None,
    host_network: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    metadata: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.MetadataProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_account_name: typing.Optional[builtins.str] = None,
    volumes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksVolumeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1631be66b62756fc44ffe485df78aa9ef2d0179130d5762da3d7c8fedbb1d3c(
    *,
    type: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8d14a2294314d52d1f5f9ed29100fe3b4d05b9507e48a8a9d76c8968ebaa70c(
    *,
    limits: typing.Any = None,
    requests: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fbb92016638159461ddf9048da4302f986b31747904432195638b08c9068871(
    *,
    attempts: typing.Optional[jsii.Number] = None,
    evaluate_on_exit: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EvaluateOnExitProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8457bb10d6230cf7d2376b857c7da531278ec4e55263cdf7d00ab731033b6b8(
    *,
    name: builtins.str,
    value_from: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e712a516a1e7049d6a49a6b9958b7620d24b559ea9cc41246c57c36c6e065f(
    *,
    privileged: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    read_only_root_filesystem: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    run_as_group: typing.Optional[jsii.Number] = None,
    run_as_non_root: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    run_as_user: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e723710dab64b31b8950c8bd8f23b73b01d993c8b6b612ea68c13df98c7c35dd(
    *,
    attempt_duration_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e5e98ab831889be5a29592909c964829742037779ae89ca57cd54289531bcf(
    *,
    container_path: builtins.str,
    size: jsii.Number,
    mount_options: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4577baeb748f86c40692f2fcbbc6aa23be44c64f98c4cf01489c80e9c919d43d(
    *,
    hard_limit: jsii.Number,
    name: builtins.str,
    soft_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a948f23849eafddf36c96cb6c33217b6c1e2bb2f0ce8459301b1f27e5e5ffe30(
    *,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5087ce87b378614336ecbae50a75fa807f069b9632cac9e6035b8d18b75562b(
    *,
    efs_volume_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EfsVolumeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    host: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.VolumesHostProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2fb593465fb397a49eb9e021db7bb3c04e885d5f6d7e1af323262458c238c9(
    *,
    type: builtins.str,
    container_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.ContainerPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    eks_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.EksPropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    job_definition_name: typing.Optional[builtins.str] = None,
    node_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.NodePropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    parameters: typing.Any = None,
    platform_capabilities: typing.Optional[typing.Sequence[builtins.str]] = None,
    propagate_tags: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    retry_strategy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.RetryStrategyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    scheduling_priority: typing.Optional[jsii.Number] = None,
    tags: typing.Any = None,
    timeout: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobDefinition.TimeoutProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d45ceb8834180bf5b87da79a018b9248e1475232962a3bab5fc8e9874e9fc7f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    compute_environment_order: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobQueue.ComputeEnvironmentOrderProperty, typing.Dict[builtins.str, typing.Any]]]]],
    priority: jsii.Number,
    job_queue_name: typing.Optional[builtins.str] = None,
    scheduling_policy_arn: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b40845028a0f4f7eaad64ef2519b142a4c3847fdd17579a79dff446cb1223bbb(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bba213fbb76e04ee2b0ea1ca549bb1356bc2f700259e377f297466a196e5019c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f46e6804b033d8f6c463e15ff250bd04172d1d6f9a81fadbe808c4c7e59ae4d(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnJobQueue.ComputeEnvironmentOrderProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1078e6a6700fd0cdcbf286e07d93323c4bbbaf73b0b7dfbe7aad318300b4efca(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1749dbd3563f50046f0c775d69fbe792a8e925d8a408b163bc5c048fd0cad86a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39329cd2acd43021d3942bdea6716312480fe2a28ba4e71868404948115d44ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea43c391bbfb1443f4c91e0c8b6716bda8e2a17836bd269e26b2a99fd91c3668(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d652f3a45d29f5f6e825062154191183ef2be818632dd8c3bb528bab72ff8734(
    *,
    compute_environment: builtins.str,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb68f68eff8e0e521b37bbd631d3341564b3f6e589db1d5e23de934507b9c2ed(
    *,
    compute_environment_order: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnJobQueue.ComputeEnvironmentOrderProperty, typing.Dict[builtins.str, typing.Any]]]]],
    priority: jsii.Number,
    job_queue_name: typing.Optional[builtins.str] = None,
    scheduling_policy_arn: typing.Optional[builtins.str] = None,
    state: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e3f5b12574d09b9b554d3949c3a208090b28bfd8e56c76a1acb4a1b9dbf9dfb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    fairshare_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSchedulingPolicy.FairsharePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74595793997bab76778b08d2b955353f9f489c52c12224700fcd3e48a29078a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea1c11da28bfd24b8bce94afa234114cf35f7ab9217c678155d3852bd2d19418(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e7e12ec1e5407c9625e59828a1ee16a4660abc2e95da6f63b9bdad7ef167184(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnSchedulingPolicy.FairsharePolicyProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849ed0269d02025a08e0e0cf84b06eb3051a4493243cbf19b2f4ba4aaa3d9d0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d2dd48acf8140bc8e582e663930a1cf7feb0f972af9196223d5f169ef40f82(
    *,
    compute_reservation: typing.Optional[jsii.Number] = None,
    share_decay_seconds: typing.Optional[jsii.Number] = None,
    share_distribution: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSchedulingPolicy.ShareAttributesProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bac75ae975eec2e972fd2432eaac0f39e1f2b6e2328652659783cbb0f71bce7(
    *,
    share_identifier: typing.Optional[builtins.str] = None,
    weight_factor: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2762a742e69dc2048aa582997e3913536cecc5018d19c3d94bdea6d66e74b8(
    *,
    fairshare_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnSchedulingPolicy.FairsharePolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21ace0cdfc3f35b35e17654517fe1dbc2099cd3b46cec312cf8dce94ded0d75(
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    compute_resources: typing.Optional[typing.Union[ComputeResources, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    managed: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d1d6f59471e724a007d30eb7dfaa63f8276fadedd726498ca966a8516f58a5(
    *,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    allocation_strategy: typing.Optional[AllocationStrategy] = None,
    bid_percentage: typing.Optional[jsii.Number] = None,
    compute_resources_tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    desiredv_cpus: typing.Optional[jsii.Number] = None,
    ec2_key_pair: typing.Optional[builtins.str] = None,
    image: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.IMachineImage] = None,
    instance_role: typing.Optional[builtins.str] = None,
    instance_types: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.InstanceType]] = None,
    launch_template: typing.Optional[typing.Union[LaunchTemplateSpecification, typing.Dict[builtins.str, typing.Any]]] = None,
    maxv_cpus: typing.Optional[jsii.Number] = None,
    minv_cpus: typing.Optional[jsii.Number] = None,
    placement_group: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_67de8e8d.ISecurityGroup]] = None,
    spot_fleet_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    type: typing.Optional[ComputeResourceType] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_67de8e8d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf444b6830a3c37bd1ea3f56c2f74ef441ed72e6b04d13891ef0df1e5bb0df0(
    option_name: builtins.str,
    secret_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0acfdd28c190f00699a1359a250ee574c4fda31db85590a1908235d79926de9(
    option_name: builtins.str,
    parameter: _aws_cdk_aws_ssm_1e9d799e.IParameter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7478244b9551787bd9b2436bea927603c98c0f3355a06230f5d2b2170e6862a9(
    option_name: builtins.str,
    secret: _aws_cdk_aws_secretsmanager_72af8d6f.ISecret,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__079a44ba31d8a59ec41ad37e7e48f98bfb8a167d93d4367ee91512bc5787ed0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ad90a34744d2ab8f28910b6970f3e27c10876a0d3f586d8b752e85cd708dbfa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e5f97d09d498f1af7abc7fc9d1227db1dae50d19ec241bcf77b7e88328b6e92(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__961416f58d1245c43f294c9adb44ad149127f6ea251e2af151b913926bae938c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d63b7cdb37883f54096481a8db3fc4c27c224b08ca2ea11cb66c17092eb17e9(
    value: typing.List[INodeRangeProps],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef07a3cc73397dc52c31d5246652bdbff89e2ecfbd56777725fc0d4cc15df906(
    value: JobDefinitionContainer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c009fac035be99494cc36b3483ba8f78a585f4c8a85e576bad9cd4bce30588cd(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03171da246a8befa529a66a7c73d299e5e1b2535eb131dcb23f43c0f42774464(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6db60780f36109c6c0914155c556375ad097f407c82cbcadadf25694a369f10(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    container: typing.Union[JobDefinitionContainer, typing.Dict[builtins.str, typing.Any]],
    job_definition_name: typing.Optional[builtins.str] = None,
    node_props: typing.Optional[IMultiNodeProps] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform_capabilities: typing.Optional[typing.Sequence[PlatformCapabilities]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b41850089fd68272b72c3ac134ab5c9cee8169f9fa7dc046e2f4e0ca2f738ec(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    job_definition_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2be081cb800d733e9351d4b28aa9719554b5f5a90043aa0dd11b6ad9e3376c7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    job_definition_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a7fb86fc0d39f59a00e5f1e1e0834ede0353f6c657b5ee7432a25ab66135ab(
    *,
    image: _aws_cdk_aws_ecs_7896c08f.ContainerImage,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    command: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    execution_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    gpu_count: typing.Optional[jsii.Number] = None,
    instance_type: typing.Optional[_aws_cdk_aws_ec2_67de8e8d.InstanceType] = None,
    job_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    linux_params: typing.Optional[_aws_cdk_aws_ecs_7896c08f.LinuxParameters] = None,
    log_configuration: typing.Optional[typing.Union[LogConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    mount_points: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.MountPoint, typing.Dict[builtins.str, typing.Any]]]] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_7896c08f.FargatePlatformVersion] = None,
    privileged: typing.Optional[builtins.bool] = None,
    read_only: typing.Optional[builtins.bool] = None,
    ulimits: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.Ulimit, typing.Dict[builtins.str, typing.Any]]]] = None,
    user: typing.Optional[builtins.str] = None,
    vcpus: typing.Optional[jsii.Number] = None,
    volumes: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_7896c08f.Volume, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fa972272cb531d13e06acde1da4d0a48676283a04d603a5ebf86c369f0cb141(
    *,
    container: typing.Union[JobDefinitionContainer, typing.Dict[builtins.str, typing.Any]],
    job_definition_name: typing.Optional[builtins.str] = None,
    node_props: typing.Optional[IMultiNodeProps] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    platform_capabilities: typing.Optional[typing.Sequence[PlatformCapabilities]] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    timeout: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfd49c95e3f6aad58cb8cbecd81984130f9fccc646ce1b993e6d691fa77e6434(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_environments: typing.Sequence[typing.Union[JobQueueComputeEnvironment, typing.Dict[builtins.str, typing.Any]]],
    enabled: typing.Optional[builtins.bool] = None,
    job_queue_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1351d7084272383ee85ae7b25f9bcf1a4f812160acc1b98a5f3c0acec7369276(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    job_queue_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1049c098b4510fd4f91b4a80fd0ee0db14d9de161e6d8fa24e1a29a9d5c21bd9(
    *,
    compute_environment: IComputeEnvironment,
    order: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08940a1fda209fa6d0a451eff3fd33e053ae672e99e3cb8f73e51e8877dfb76a(
    *,
    compute_environments: typing.Sequence[typing.Union[JobQueueComputeEnvironment, typing.Dict[builtins.str, typing.Any]]],
    enabled: typing.Optional[builtins.bool] = None,
    job_queue_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40b697492dedf22ff3d1629d0837d575b0bdb27e02bdf4387dcdad8b0da2e896(
    *,
    launch_template_name: builtins.str,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7959a77ca17c46379418110fc7173feb55c9a61f7cd7c806f8964b8f520d9dc8(
    *,
    log_driver: LogDriver,
    options: typing.Any = None,
    secret_options: typing.Optional[typing.Sequence[ExposedSecret]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__585b81e40fcc982c3c9cbb15cd4d566a5c43af3b6df9e20f412d5c7e000ba012(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_environment_name: typing.Optional[builtins.str] = None,
    compute_resources: typing.Optional[typing.Union[ComputeResources, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    managed: typing.Optional[builtins.bool] = None,
    service_role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70162245124335067837158534d16fcc55b46ea780fb49a4fa7db3117ac4f6c2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    compute_environment_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
