r'''
# AWS::ApplicationSignals Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

CloudWatch Application Signals is an auto-instrumentation solution built on OpenTelemetry that enables zero-code collection of monitoring data, such
as traces and metrics, from applications running across multiple platforms. It also supports topology auto-discovery based on collected monitoring data
and includes a new feature for managing service-level objectives (SLOs).

It supports Java, Python, .NET, and Node.js on platforms including EKS (and native Kubernetes), Lambda, ECS, and EC2. For more details, visit
[Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html) on the AWS
public website.

## Application Signals Enablement L2 Constructs

A collection of L2 constructs which leverages native L1 CFN resources, simplifying the enablement steps and the creation of Application
Signals resources.

### ApplicationSignalsIntegration

`ApplicationSignalsIntegration` aims to address key challenges in the current CDK enablement process, which requires complex manual configurations for
ECS customers. Application Signals is designed to be flexible and is supported for other platforms as well. However, the initial focus is on supporting
ECS, with plans to potentially extend support to other platforms in the future.

#### Enable Application Signals on ECS with sidecar mode

1. Configure `instrumentation` to instrument the application with the ADOT SDK Agent.
2. Specify `cloudWatchAgentSidecar` to configure the CloudWatch Agent as a sidecar container.

```python
from constructs import Construct
import aws_cdk.aws_applicationsignals_alpha as appsignals
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs

class MyStack(cdk.Stack):
    def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__()
        vpc = ec2.Vpc(self, "TestVpc")
        cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)

        fargate_task_definition = ecs.FargateTaskDefinition(self, "SampleAppTaskDefinition",
            cpu=2048,
            memory_limit_mi_b=4096
        )

        fargate_task_definition.add_container("app",
            image=ecs.ContainerImage.from_registry("test/sample-app")
        )

        appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
            task_definition=fargate_task_definition,
            instrumentation=appsignals.InstrumentationProps(
                sdk_version=appsignals.JavaInstrumentationVersion.V2_10_0
            ),
            service_name="sample-app",
            cloud_watch_agent_sidecar=appsignals.CloudWatchAgentOptions(
                container_name="cloudwatch-agent",
                enable_logging=True,
                cpu=256,
                memory_limit_mi_b=512
            )
        )

        ecs.FargateService(self, "MySampleApp",
            cluster=cluster,
            task_definition=fargate_task_definition,
            desired_count=1
        )
```

#### Enable Application Signals on ECS with daemon mode

Note: Since the daemon deployment strategy is not supported on ECS Fargate, this mode is only supported on ECS on EC2.

1. Run CloudWatch Agent as a daemon service with HOST network mode.
2. Configure `instrumentation` to instrument the application with the ADOT Python Agent.
3. Override environment variables by configuring `overrideEnvironments` to use service connect endpoints to communicate to the CloudWatch agent server

```python
from constructs import Construct
import aws_cdk.aws_applicationsignals_alpha as appsignals
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs

class MyStack(cdk.Stack):
    def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)

        vpc = ec2.Vpc(self, "TestVpc")
        cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)

        # Define Task Definition for CloudWatch agent (Daemon)
        cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
            network_mode=ecs.NetworkMode.HOST
        )

        appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
            task_definition=cw_agent_task_definition,
            container_name="ecs-cwagent",
            enable_logging=False,
            cpu=128,
            memory_limit_mi_b=64,
            port_mappings=[ecs.PortMapping(
                container_port=4316,
                host_port=4316
            ), ecs.PortMapping(
                container_port=2000,
                host_port=2000
            )
            ]
        )

        # Create the CloudWatch Agent daemon service
        ecs.Ec2Service(self, "CloudWatchAgentDaemon",
            cluster=cluster,
            task_definition=cw_agent_task_definition,
            daemon=True
        )

        # Define Task Definition for user application
        sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
            network_mode=ecs.NetworkMode.HOST
        )

        sample_app_task_definition.add_container("app",
            image=ecs.ContainerImage.from_registry("test/sample-app"),
            cpu=0,
            memory_limit_mi_b=512
        )

        # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
        appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
            task_definition=sample_app_task_definition,
            instrumentation=appsignals.InstrumentationProps(
                sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
            ),
            service_name="sample-app"
        )

        ecs.Ec2Service(self, "MySampleApp",
            cluster=cluster,
            task_definition=sample_app_task_definition,
            desired_count=1
        )
```

#### Enable Application Signals on ECS with replica mode

**Note**
*Running CloudWatch Agent service using replica mode requires specific security group configurations to enable communication with other services.
For Application Signals functionality, configure the security group with the following minimum inbound rules: Port 2000 (HTTP) and Port 4316 (HTTP).
This configuration ensures proper connectivity between the CloudWatch Agent and dependent services.*

1. Run CloudWatch Agent as a replica service with service connect.
2. Configure `instrumentation` to instrument the application with the ADOT Python Agent.
3. Override environment variables by configuring `overrideEnvironments` to use service connect endpoints to communicate to the CloudWatch agent server

```python
from constructs import Construct
import aws_cdk.aws_applicationsignals_alpha as appsignals
import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_ecs as ecs
from aws_cdk.aws_servicediscovery import PrivateDnsNamespace

class MyStack(cdk.Stack):
    def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)

        vpc = ec2.Vpc(self, "TestVpc")
        cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
        dns_namespace = PrivateDnsNamespace(self, "Namespace",
            vpc=vpc,
            name="local"
        )
        security_group = ec2.SecurityGroup(self, "ECSSG", vpc=vpc)
        security_group.add_ingress_rule(security_group, ec2.Port.tcp_range(0, 65535))

        # Define Task Definition for CloudWatch agent (Replica)
        cw_agent_task_definition = ecs.FargateTaskDefinition(self, "CloudWatchAgentTaskDefinition")

        appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
            task_definition=cw_agent_task_definition,
            container_name="ecs-cwagent",
            enable_logging=False,
            cpu=128,
            memory_limit_mi_b=64,
            port_mappings=[ecs.PortMapping(
                name="cwagent-4316",
                container_port=4316,
                host_port=4316
            ), ecs.PortMapping(
                name="cwagent-2000",
                container_port=2000,
                host_port=2000
            )
            ]
        )

        # Create the CloudWatch Agent replica service with service connect
        ecs.FargateService(self, "CloudWatchAgentService",
            cluster=cluster,
            task_definition=cw_agent_task_definition,
            security_groups=[security_group],
            service_connect_configuration=ecs.ServiceConnectProps(
                namespace=dns_namespace.namespace_arn,
                services=[ecs.ServiceConnectService(
                    port_mapping_name="cwagent-4316",
                    dns_name="cwagent-4316-http",
                    port=4316
                ), ecs.ServiceConnectService(
                    port_mapping_name="cwagent-2000",
                    dns_name="cwagent-2000-http",
                    port=2000
                )
                ]
            ),
            desired_count=1
        )

        # Define Task Definition for user application
        sample_app_task_definition = ecs.FargateTaskDefinition(self, "SampleAppTaskDefinition")

        sample_app_task_definition.add_container("app",
            image=ecs.ContainerImage.from_registry("test/sample-app"),
            cpu=0,
            memory_limit_mi_b=512
        )

        # Overwrite environment variables to connect to the CloudWatch Agent service just created
        appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
            task_definition=sample_app_task_definition,
            instrumentation=appsignals.InstrumentationProps(
                sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
            ),
            service_name="sample-app",
            override_environments=[appsignals.EnvironmentExtension(
                name=appsignals.CommonExporting.OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT,
                value="http://cwagent-4316-http:4316/v1/metrics"
            ), appsignals.EnvironmentExtension(
                name=appsignals.TraceExporting.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
                value="http://cwagent-4316-http:4316/v1/traces"
            ), appsignals.EnvironmentExtension(
                name=appsignals.TraceExporting.OTEL_TRACES_SAMPLER_ARG,
                value="endpoint=http://cwagent-2000-http:2000"
            )
            ]
        )

        # Create ECS Service with service connect configuration
        ecs.FargateService(self, "MySampleApp",
            cluster=cluster,
            task_definition=sample_app_task_definition,
            service_connect_configuration=ecs.ServiceConnectProps(
                namespace=dns_namespace.namespace_arn
            ),
            desired_count=1
        )
```
'''
from __future__ import annotations

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

from jsii._type_checking import cached_type_hints, check_type


from ._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_aws_ecs_ceddda9d = _LazyImport("aws_cdk.aws_ecs")
    _constructs_77d1e7e8 = _LazyImport("constructs")


class ApplicationSignalsIntegration(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.ApplicationSignalsIntegration",
):
    '''(experimental) Class for integrating Application Signals into an ECS task definition.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
        
                # Define Task Definition for CloudWatch agent (Daemon)
                cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                    task_definition=cw_agent_task_definition,
                    container_name="ecs-cwagent",
                    enable_logging=False,
                    cpu=128,
                    memory_limit_mi_b=64,
                    port_mappings=[ecs.PortMapping(
                        container_port=4316,
                        host_port=4316
                    ), ecs.PortMapping(
                        container_port=2000,
                        host_port=2000
                    )
                    ]
                )
        
                # Create the CloudWatch Agent daemon service
                ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                    cluster=cluster,
                    task_definition=cw_agent_task_definition,
                    daemon=True
                )
        
                # Define Task Definition for user application
                sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                sample_app_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app"),
                    cpu=0,
                    memory_limit_mi_b=512
                )
        
                # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=sample_app_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                    ),
                    service_name="sample-app"
                )
        
                ecs.Ec2Service(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=sample_app_task_definition,
                    desired_count=1
                )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        instrumentation: typing.Union["InstrumentationProps", typing.Dict[builtins.str, typing.Any]],
        task_definition: "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition",
        cloud_watch_agent_sidecar: typing.Optional[typing.Union["CloudWatchAgentOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param instrumentation: (experimental) The instrumentation properties.
        :param task_definition: (experimental) The task definition to integrate Application Signals into. [disable-awslint:ref-via-interface]
        :param cloud_watch_agent_sidecar: (experimental) The CloudWatch Agent properties. Default: - a basic agent sidecar container with latest public image
        :param override_environments: (experimental) The environment variables to override. Default: - no environment variables to override.
        :param service_name: (experimental) The name of the service. Default: - task definition family name

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__45fc22f9560022d5f606a9a371c1833f463aa1c7bdb573a765baafe38bfb4040)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ApplicationSignalsIntegrationProps(
            instrumentation=instrumentation,
            task_definition=task_definition,
            cloud_watch_agent_sidecar=cloud_watch_agent_sidecar,
            override_environments=override_environments,
            service_name=service_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.ApplicationSignalsIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "instrumentation": "instrumentation",
        "task_definition": "taskDefinition",
        "cloud_watch_agent_sidecar": "cloudWatchAgentSidecar",
        "override_environments": "overrideEnvironments",
        "service_name": "serviceName",
    },
)
class ApplicationSignalsIntegrationProps:
    def __init__(
        self,
        *,
        instrumentation: typing.Union["InstrumentationProps", typing.Dict[builtins.str, typing.Any]],
        task_definition: "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition",
        cloud_watch_agent_sidecar: typing.Optional[typing.Union["CloudWatchAgentOptions", typing.Dict[builtins.str, typing.Any]]] = None,
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Interface for Application Signals properties.

        :param instrumentation: (experimental) The instrumentation properties.
        :param task_definition: (experimental) The task definition to integrate Application Signals into. [disable-awslint:ref-via-interface]
        :param cloud_watch_agent_sidecar: (experimental) The CloudWatch Agent properties. Default: - a basic agent sidecar container with latest public image
        :param override_environments: (experimental) The environment variables to override. Default: - no environment variables to override.
        :param service_name: (experimental) The name of the service. Default: - task definition family name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from constructs import Construct
            import aws_cdk.aws_applicationsignals_alpha as appsignals
            import aws_cdk as cdk
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            
            class MyStack(cdk.Stack):
                def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                    super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
            
                    vpc = ec2.Vpc(self, "TestVpc")
                    cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
            
                    # Define Task Definition for CloudWatch agent (Daemon)
                    cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                        network_mode=ecs.NetworkMode.HOST
                    )
            
                    appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                        task_definition=cw_agent_task_definition,
                        container_name="ecs-cwagent",
                        enable_logging=False,
                        cpu=128,
                        memory_limit_mi_b=64,
                        port_mappings=[ecs.PortMapping(
                            container_port=4316,
                            host_port=4316
                        ), ecs.PortMapping(
                            container_port=2000,
                            host_port=2000
                        )
                        ]
                    )
            
                    # Create the CloudWatch Agent daemon service
                    ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                        cluster=cluster,
                        task_definition=cw_agent_task_definition,
                        daemon=True
                    )
            
                    # Define Task Definition for user application
                    sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                        network_mode=ecs.NetworkMode.HOST
                    )
            
                    sample_app_task_definition.add_container("app",
                        image=ecs.ContainerImage.from_registry("test/sample-app"),
                        cpu=0,
                        memory_limit_mi_b=512
                    )
            
                    # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                    appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                        task_definition=sample_app_task_definition,
                        instrumentation=appsignals.InstrumentationProps(
                            sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                        ),
                        service_name="sample-app"
                    )
            
                    ecs.Ec2Service(self, "MySampleApp",
                        cluster=cluster,
                        task_definition=sample_app_task_definition,
                        desired_count=1
                    )
        '''
        if isinstance(instrumentation, dict):
            instrumentation = InstrumentationProps(**instrumentation)
        if isinstance(cloud_watch_agent_sidecar, dict):
            cloud_watch_agent_sidecar = CloudWatchAgentOptions(**cloud_watch_agent_sidecar)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cd6fa50a03d0911abf781dabe7f10143f0811de27611dfdaf9ceeefc5b82a804)
            check_type(argname="argument instrumentation", value=instrumentation, expected_type=type_hints["instrumentation"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument cloud_watch_agent_sidecar", value=cloud_watch_agent_sidecar, expected_type=type_hints["cloud_watch_agent_sidecar"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instrumentation": instrumentation,
            "task_definition": task_definition,
        }
        if cloud_watch_agent_sidecar is not None:
            self._values["cloud_watch_agent_sidecar"] = cloud_watch_agent_sidecar
        if override_environments is not None:
            self._values["override_environments"] = override_environments
        if service_name is not None:
            self._values["service_name"] = service_name

    @builtins.property
    def instrumentation(self) -> "InstrumentationProps":
        '''(experimental) The instrumentation properties.

        :stability: experimental
        '''
        result = self._values.get("instrumentation")
        assert result is not None, "Required property 'instrumentation' is missing"
        return typing.cast("InstrumentationProps", result)

    @builtins.property
    def task_definition(self) -> "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition":
        '''(experimental) The task definition to integrate Application Signals into.

        [disable-awslint:ref-via-interface]

        :stability: experimental
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.TaskDefinition", result)

    @builtins.property
    def cloud_watch_agent_sidecar(self) -> typing.Optional["CloudWatchAgentOptions"]:
        '''(experimental) The CloudWatch Agent properties.

        :default: - a basic agent sidecar container with latest public image

        :stability: experimental
        '''
        result = self._values.get("cloud_watch_agent_sidecar")
        return typing.cast(typing.Optional["CloudWatchAgentOptions"], result)

    @builtins.property
    def override_environments(
        self,
    ) -> typing.Optional[typing.List["EnvironmentExtension"]]:
        '''(experimental) The environment variables to override.

        :default: - no environment variables to override.

        :stability: experimental
        '''
        result = self._values.get("override_environments")
        return typing.cast(typing.Optional[typing.List["EnvironmentExtension"]], result)

    @builtins.property
    def service_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the service.

        :default: - task definition family name

        :stability: experimental
        '''
        result = self._values.get("service_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApplicationSignalsIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWatchAgentIntegration(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.CloudWatchAgentIntegration",
):
    '''(experimental) A construct that adds CloudWatch Agent as a container to an ECS task definition.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
        
                # Define Task Definition for CloudWatch agent (Daemon)
                cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                    task_definition=cw_agent_task_definition,
                    container_name="ecs-cwagent",
                    enable_logging=False,
                    cpu=128,
                    memory_limit_mi_b=64,
                    port_mappings=[ecs.PortMapping(
                        container_port=4316,
                        host_port=4316
                    ), ecs.PortMapping(
                        container_port=2000,
                        host_port=2000
                    )
                    ]
                )
        
                # Create the CloudWatch Agent daemon service
                ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                    cluster=cluster,
                    task_definition=cw_agent_task_definition,
                    daemon=True
                )
        
                # Define Task Definition for user application
                sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                sample_app_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app"),
                    cpu=0,
                    memory_limit_mi_b=512
                )
        
                # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=sample_app_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                    ),
                    service_name="sample-app"
                )
        
                ecs.Ec2Service(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=sample_app_task_definition,
                    desired_count=1
                )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        task_definition: "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition",
        container_name: builtins.str,
        agent_config: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        essential: typing.Optional[builtins.bool] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        operating_system_family: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"] = None,
        port_mappings: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_aws_ecs_ceddda9d.PortMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Creates a new CloudWatch Agent integration.

        :param scope: - The construct scope.
        :param id: - The construct ID.
        :param task_definition: (experimental) The task definition to integrate CloudWatch agent into. [disable-awslint:ref-via-interface]
        :param container_name: (experimental) Name of the CloudWatch Agent container.
        :param agent_config: (experimental) Custom agent configuration in JSON format. Default: - Uses default configuration for Application Signals
        :param cpu: (experimental) The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param enable_logging: (experimental) Whether to enable logging for the CloudWatch Agent. Default: - false
        :param essential: (experimental) Start as an essential container. Default: - true
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory to present to the container. Default: - No memory limit.
        :param memory_reservation_mib: (experimental) The soft limit (in MiB) of memory to reserve for the container. Default: - No memory reserved.
        :param operating_system_family: (experimental) Operating system family for the CloudWatch Agent. Default: - Linux
        :param port_mappings: (experimental) The port mappings to add to the container definition. Default: - No ports are mapped.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d88d8cd0ef22ce2257442d2a60f0e38524aa23226623a1e7f58323196bdebaf8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CloudWatchAgentIntegrationProps(
            task_definition=task_definition,
            container_name=container_name,
            agent_config=agent_config,
            cpu=cpu,
            enable_logging=enable_logging,
            essential=essential,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            operating_system_family=operating_system_family,
            port_mappings=port_mappings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="agentContainer")
    def agent_container(self) -> "_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition":
        '''(experimental) The CloudWatch Agent container definition.

        :stability: experimental
        '''
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition", jsii.get(self, "agentContainer"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.CloudWatchAgentOptions",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "agent_config": "agentConfig",
        "cpu": "cpu",
        "enable_logging": "enableLogging",
        "essential": "essential",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "operating_system_family": "operatingSystemFamily",
        "port_mappings": "portMappings",
    },
)
class CloudWatchAgentOptions:
    def __init__(
        self,
        *,
        container_name: builtins.str,
        agent_config: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        essential: typing.Optional[builtins.bool] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        operating_system_family: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"] = None,
        port_mappings: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_aws_ecs_ceddda9d.PortMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Configuration options for the CloudWatch Agent container.

        :param container_name: (experimental) Name of the CloudWatch Agent container.
        :param agent_config: (experimental) Custom agent configuration in JSON format. Default: - Uses default configuration for Application Signals
        :param cpu: (experimental) The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param enable_logging: (experimental) Whether to enable logging for the CloudWatch Agent. Default: - false
        :param essential: (experimental) Start as an essential container. Default: - true
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory to present to the container. Default: - No memory limit.
        :param memory_reservation_mib: (experimental) The soft limit (in MiB) of memory to reserve for the container. Default: - No memory reserved.
        :param operating_system_family: (experimental) Operating system family for the CloudWatch Agent. Default: - Linux
        :param port_mappings: (experimental) The port mappings to add to the container definition. Default: - No ports are mapped.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from constructs import Construct
            import aws_cdk.aws_applicationsignals_alpha as appsignals
            import aws_cdk as cdk
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            
            class MyStack(cdk.Stack):
                def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                    super().__init__()
                    vpc = ec2.Vpc(self, "TestVpc")
                    cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
            
                    fargate_task_definition = ecs.FargateTaskDefinition(self, "SampleAppTaskDefinition",
                        cpu=2048,
                        memory_limit_mi_b=4096
                    )
            
                    fargate_task_definition.add_container("app",
                        image=ecs.ContainerImage.from_registry("test/sample-app")
                    )
            
                    appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                        task_definition=fargate_task_definition,
                        instrumentation=appsignals.InstrumentationProps(
                            sdk_version=appsignals.JavaInstrumentationVersion.V2_10_0
                        ),
                        service_name="sample-app",
                        cloud_watch_agent_sidecar=appsignals.CloudWatchAgentOptions(
                            container_name="cloudwatch-agent",
                            enable_logging=True,
                            cpu=256,
                            memory_limit_mi_b=512
                        )
                    )
            
                    ecs.FargateService(self, "MySampleApp",
                        cluster=cluster,
                        task_definition=fargate_task_definition,
                        desired_count=1
                    )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8a45015e4a6a56c1499f4458a2b77c626b987c6f596c335f08463327164cd54b)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument agent_config", value=agent_config, expected_type=type_hints["agent_config"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument operating_system_family", value=operating_system_family, expected_type=type_hints["operating_system_family"])
            check_type(argname="argument port_mappings", value=port_mappings, expected_type=type_hints["port_mappings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_name": container_name,
        }
        if agent_config is not None:
            self._values["agent_config"] = agent_config
        if cpu is not None:
            self._values["cpu"] = cpu
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if essential is not None:
            self._values["essential"] = essential
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if operating_system_family is not None:
            self._values["operating_system_family"] = operating_system_family
        if port_mappings is not None:
            self._values["port_mappings"] = port_mappings

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) Name of the CloudWatch Agent container.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_config(self) -> typing.Optional[builtins.str]:
        '''(experimental) Custom agent configuration in JSON format.

        :default: - Uses default configuration for Application Signals

        :stability: experimental
        '''
        result = self._values.get("agent_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum number of CPU units to reserve for the container.

        :default: - No minimum CPU units reserved.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable logging for the CloudWatch Agent.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def essential(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Start as an essential container.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("essential")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in MiB) of memory to present to the container.

        :default: - No memory limit.

        :stability: experimental
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        :default: - No memory reserved.

        :stability: experimental
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operating_system_family(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"]:
        '''(experimental) Operating system family for the CloudWatch Agent.

        :default: - Linux

        :stability: experimental
        '''
        result = self._values.get("operating_system_family")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"], result)

    @builtins.property
    def port_mappings(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PortMapping"]]:
        '''(experimental) The port mappings to add to the container definition.

        :default: - No ports are mapped.

        :stability: experimental
        '''
        result = self._values.get("port_mappings")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PortMapping"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchAgentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CloudWatchAgentVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.CloudWatchAgentVersion",
):
    '''(experimental) Provides version information and image selection for CloudWatch Agent.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        cloud_watch_agent_version = applicationsignals_alpha.CloudWatchAgentVersion()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="getCloudWatchAgentImage")
    @builtins.classmethod
    def get_cloud_watch_agent_image(
        cls,
        operating_system_family: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"] = None,
    ) -> builtins.str:
        '''(experimental) Gets the appropriate CloudWatch Agent image based on the operating system.

        :param operating_system_family: - The ECS operating system family.

        :return: The CloudWatch Agent image URI

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__132fb1893dfd6cb3bd0e34ef1067e39cb5c6bcf814379ce6e7a8315999d8dbfd)
            check_type(argname="argument operating_system_family", value=operating_system_family, expected_type=type_hints["operating_system_family"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "getCloudWatchAgentImage", [operating_system_family]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDWATCH_AGENT_IMAGE")
    def CLOUDWATCH_AGENT_IMAGE(cls) -> builtins.str:
        '''(experimental) Default CloudWatch Agent image for Linux.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CLOUDWATCH_AGENT_IMAGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDWATCH_AGENT_IMAGE_WIN2019")
    def CLOUDWATCH_AGENT_IMAGE_WIN2019(cls) -> builtins.str:
        '''(experimental) CloudWatch Agent image for Windows Server 2019.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CLOUDWATCH_AGENT_IMAGE_WIN2019"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLOUDWATCH_AGENT_IMAGE_WIN2022")
    def CLOUDWATCH_AGENT_IMAGE_WIN2022(cls) -> builtins.str:
        '''(experimental) CloudWatch Agent image for Windows Server 2022.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CLOUDWATCH_AGENT_IMAGE_WIN2022"))


class CommonExporting(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.CommonExporting",
):
    '''(experimental) Common OpenTelemetry exporter configurations and AWS Application Signals settings.

    Contains constants for OTLP protocol, resource attributes, and Application Signals enablement.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        from aws_cdk.aws_servicediscovery import PrivateDnsNamespace
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
                dns_namespace = PrivateDnsNamespace(self, "Namespace",
                    vpc=vpc,
                    name="local"
                )
                security_group = ec2.SecurityGroup(self, "ECSSG", vpc=vpc)
                security_group.add_ingress_rule(security_group, ec2.Port.tcp_range(0, 65535))
        
                # Define Task Definition for CloudWatch agent (Replica)
                cw_agent_task_definition = ecs.FargateTaskDefinition(self, "CloudWatchAgentTaskDefinition")
        
                appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                    task_definition=cw_agent_task_definition,
                    container_name="ecs-cwagent",
                    enable_logging=False,
                    cpu=128,
                    memory_limit_mi_b=64,
                    port_mappings=[ecs.PortMapping(
                        name="cwagent-4316",
                        container_port=4316,
                        host_port=4316
                    ), ecs.PortMapping(
                        name="cwagent-2000",
                        container_port=2000,
                        host_port=2000
                    )
                    ]
                )
        
                # Create the CloudWatch Agent replica service with service connect
                ecs.FargateService(self, "CloudWatchAgentService",
                    cluster=cluster,
                    task_definition=cw_agent_task_definition,
                    security_groups=[security_group],
                    service_connect_configuration=ecs.ServiceConnectProps(
                        namespace=dns_namespace.namespace_arn,
                        services=[ecs.ServiceConnectService(
                            port_mapping_name="cwagent-4316",
                            dns_name="cwagent-4316-http",
                            port=4316
                        ), ecs.ServiceConnectService(
                            port_mapping_name="cwagent-2000",
                            dns_name="cwagent-2000-http",
                            port=2000
                        )
                        ]
                    ),
                    desired_count=1
                )
        
                # Define Task Definition for user application
                sample_app_task_definition = ecs.FargateTaskDefinition(self, "SampleAppTaskDefinition")
        
                sample_app_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app"),
                    cpu=0,
                    memory_limit_mi_b=512
                )
        
                # Overwrite environment variables to connect to the CloudWatch Agent service just created
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=sample_app_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                    ),
                    service_name="sample-app",
                    override_environments=[appsignals.EnvironmentExtension(
                        name=appsignals.CommonExporting.OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT,
                        value="http://cwagent-4316-http:4316/v1/metrics"
                    ), appsignals.EnvironmentExtension(
                        name=appsignals.TraceExporting.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
                        value="http://cwagent-4316-http:4316/v1/traces"
                    ), appsignals.EnvironmentExtension(
                        name=appsignals.TraceExporting.OTEL_TRACES_SAMPLER_ARG,
                        value="endpoint=http://cwagent-2000-http:2000"
                    )
                    ]
                )
        
                # Create ECS Service with service connect configuration
                ecs.FargateService(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=sample_app_task_definition,
                    service_connect_configuration=ecs.ServiceConnectProps(
                        namespace=dns_namespace.namespace_arn
                    ),
                    desired_count=1
                )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS")
    def OTEL_AWS_APPLICATION_SIGNALS(cls) -> builtins.str:
        '''(experimental) Flag to enable/disable AWS Application Signals.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_DISABLED")
    def OTEL_AWS_APPLICATION_SIGNALS_DISABLED(cls) -> builtins.str:
        '''(experimental) Value to disable AWS Application Signals.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_DISABLED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_ENABLED")
    def OTEL_AWS_APPLICATION_SIGNALS_ENABLED(cls) -> builtins.str:
        '''(experimental) Value to enable AWS Application Signals.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_ENABLED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT")
    def OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT(cls) -> builtins.str:
        '''(experimental) Endpoint configuration for AWS Application Signals exporter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT_LOCAL_CWA")
    def OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT_LOCAL_CWA(cls) -> builtins.str:
        '''(experimental) Local CloudWatch Agent endpoint for metrics.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT_LOCAL_CWA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_RUNTIME")
    def OTEL_AWS_APPLICATION_SIGNALS_RUNTIME(cls) -> builtins.str:
        '''(experimental) Runtime configuration for AWS Application Signals.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_RUNTIME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_RUNTIME_DISABLED")
    def OTEL_AWS_APPLICATION_SIGNALS_RUNTIME_DISABLED(cls) -> builtins.str:
        '''(experimental) Value to disable AWS Application Signals runtime.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_RUNTIME_DISABLED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_AWS_APPLICATION_SIGNALS_RUNTIME_ENABLED")
    def OTEL_AWS_APPLICATION_SIGNALS_RUNTIME_ENABLED(cls) -> builtins.str:
        '''(experimental) Value to enable AWS Application Signals runtime.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_AWS_APPLICATION_SIGNALS_RUNTIME_ENABLED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_EXPORTER_OTLP_PROTOCOL")
    def OTEL_EXPORTER_OTLP_PROTOCOL(cls) -> builtins.str:
        '''(experimental) Protocol configuration for OpenTelemetry OTLP exporter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_EXPORTER_OTLP_PROTOCOL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_EXPORTER_OTLP_PROTOCOL_HTTP_PROTOBUF")
    def OTEL_EXPORTER_OTLP_PROTOCOL_HTTP_PROTOBUF(cls) -> builtins.str:
        '''(experimental) HTTP/Protobuf protocol setting for OTLP exporter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_EXPORTER_OTLP_PROTOCOL_HTTP_PROTOBUF"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_RESOURCE_ATTRIBUTES")
    def OTEL_RESOURCE_ATTRIBUTES(cls) -> builtins.str:
        '''(experimental) Resource attributes configuration for OpenTelemetry.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_RESOURCE_ATTRIBUTES"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_SERVICE_NAME")
    def OTEL_SERVICE_NAME(cls) -> builtins.str:
        '''(experimental) Resource attribute configuration for service.name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_SERVICE_NAME"))


class DotnetInstrumentation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.DotnetInstrumentation",
):
    '''(experimental) .NET-specific OpenTelemetry instrumentation configurations. Contains constants for .NET runtime settings, profiler configurations, and paths for both Linux and Windows environments.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        dotnet_instrumentation = applicationsignals_alpha.DotnetInstrumentation()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORECLR_ENABLE_PROFILING")
    def CORECLR_ENABLE_PROFILING(cls) -> builtins.str:
        '''(experimental) CoreCLR profiling enable flag.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CORECLR_ENABLE_PROFILING"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORECLR_ENABLE_PROFILING_DISABLED")
    def CORECLR_ENABLE_PROFILING_DISABLED(cls) -> builtins.str:
        '''(experimental) Disable CoreCLR profiling.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CORECLR_ENABLE_PROFILING_DISABLED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORECLR_ENABLE_PROFILING_ENABLED")
    def CORECLR_ENABLE_PROFILING_ENABLED(cls) -> builtins.str:
        '''(experimental) Enable CoreCLR profiling.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CORECLR_ENABLE_PROFILING_ENABLED"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORECLR_PROFILER")
    def CORECLR_PROFILER(cls) -> builtins.str:
        '''(experimental) CoreCLR profiler GUID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CORECLR_PROFILER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORECLR_PROFILER_OTEL")
    def CORECLR_PROFILER_OTEL(cls) -> builtins.str:
        '''(experimental) OpenTelemetry CoreCLR profiler ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CORECLR_PROFILER_OTEL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CORECLR_PROFILER_PATH")
    def CORECLR_PROFILER_PATH(cls) -> builtins.str:
        '''(experimental) Path to CoreCLR profiler.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "CORECLR_PROFILER_PATH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_ADDITIONAL_DEPS")
    def DOTNET_ADDITIONAL_DEPS(cls) -> builtins.str:
        '''(experimental) Additional .NET dependencies configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOTNET_ADDITIONAL_DEPS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_SHARED_STORE")
    def DOTNET_SHARED_STORE(cls) -> builtins.str:
        '''(experimental) .NET shared store configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOTNET_SHARED_STORE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_STARTUP_HOOKS")
    def DOTNET_STARTUP_HOOKS(cls) -> builtins.str:
        '''(experimental) .NET startup hooks configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "DOTNET_STARTUP_HOOKS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_AUTO_HOME")
    def OTEL_DOTNET_AUTO_HOME(cls) -> builtins.str:
        '''(experimental) .NET auto-instrumentation home directory.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_AUTO_HOME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_AUTO_PLUGINS")
    def OTEL_DOTNET_AUTO_PLUGINS(cls) -> builtins.str:
        '''(experimental) .NET auto-instrumentation plugins configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_AUTO_PLUGINS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_AUTO_PLUGINS_ADOT")
    def OTEL_DOTNET_AUTO_PLUGINS_ADOT(cls) -> builtins.str:
        '''(experimental) ADOT auto-instrumentation plugin for .NET.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_AUTO_PLUGINS_ADOT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_CONFIGURATOR")
    def OTEL_DOTNET_CONFIGURATOR(cls) -> builtins.str:
        '''(experimental) .NET OpenTelemetry configurator setting.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_CONFIGURATOR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_CONFIGURATOR_AWS_CONFIGURATOR")
    def OTEL_DOTNET_CONFIGURATOR_AWS_CONFIGURATOR(cls) -> builtins.str:
        '''(experimental) AWS configurator for .NET OpenTelemetry.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_CONFIGURATOR_AWS_CONFIGURATOR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_DISTRO")
    def OTEL_DOTNET_DISTRO(cls) -> builtins.str:
        '''(experimental) .NET OpenTelemetry distribution configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_DISTRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_DOTNET_DISTRO_AWS_DISTRO")
    def OTEL_DOTNET_DISTRO_AWS_DISTRO(cls) -> builtins.str:
        '''(experimental) AWS distribution for .NET OpenTelemetry.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_DOTNET_DISTRO_AWS_DISTRO"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.EnvironmentExtension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class EnvironmentExtension:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(experimental) Interface for environment extensions.

        :param name: (experimental) The name of the environment variable.
        :param value: (experimental) The value of the environment variable.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
            
            environment_extension = applicationsignals_alpha.EnvironmentExtension(
                name="name",
                value="value"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a4aa9680fa88bf414827c37a058f36194f57ec8c1b651cc1f9f15e5668086e76)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(experimental) The name of the environment variable.

        :stability: experimental
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The value of the environment variable.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EnvironmentExtension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Injector(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.Injector",
):
    '''(experimental) Injector is a base class for all SDK injects to mutate the task definition to inject the ADOT init container and configure the application container with the necessary environment variables.

    :stability: experimental
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a176319238cff5f99f06e8c96073bb71ca67bb9ad00460eb480526249a85e43a)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, override_environments])

    @jsii.member(jsii_name="injectAdditionalEnvironments")
    @abc.abstractmethod
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="injectInitContainer")
    def inject_init_container(
        self,
        task_definition: "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition",
    ) -> "_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition":
        '''(experimental) Inject ADOT SDK agent init container.

        :param task_definition: The TaskDefinition to render.

        :return: The created ContainerDefinition

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__37fe739a9bf12b91df80438a88b17ef898d49a2a7aa5ec7b48e173667c91ce05)
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.ContainerDefinition", jsii.invoke(self, "injectInitContainer", [task_definition]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    @abc.abstractmethod
    def _override_additional_environments(
        self,
        envs_to_override: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param envs_to_override: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="renderDefaultContainer")
    def render_default_container(
        self,
        task_definition: "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition",
    ) -> None:
        '''(experimental) Render the application container for SDK instrumentation.

        :param task_definition: The TaskDefinition to render.

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9146ad7105b1491db117463af1f3697bb71ccb6cdf38f24a1f7377ac94cce5e7)
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        return typing.cast(None, jsii.invoke(self, "renderDefaultContainer", [task_definition]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_ENVS")
    def DEFAULT_ENVS(cls) -> typing.List["EnvironmentExtension"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["EnvironmentExtension"], jsii.sget(cls, "DEFAULT_ENVS"))

    @builtins.property
    @jsii.member(jsii_name="command")
    @abc.abstractmethod
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    @abc.abstractmethod
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="instrumentationVersion")
    def _instrumentation_version(self) -> "InstrumentationVersion":
        '''
        :stability: experimental
        '''
        return typing.cast("InstrumentationVersion", jsii.get(self, "instrumentationVersion"))

    @_instrumentation_version.setter
    def _instrumentation_version(self, value: "InstrumentationVersion") -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__94fc97bfd0d5618005048c5433172a3b7faa7b8c480e7f893f3bd76411bf09f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instrumentationVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedVolumeName")
    def _shared_volume_name(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "sharedVolumeName"))

    @_shared_volume_name.setter
    def _shared_volume_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__acf91c135de73ebc450bad91aabf833d9815551c82d4173b7cb9645c03d4325b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedVolumeName", value) # pyright: ignore[reportArgumentType]


class _InjectorProxy(Injector):
    @jsii.member(jsii_name="injectAdditionalEnvironments")
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7d6de8aad617ac6df0bd7cf9bf4320f144dcbd0e4fb0d873ae4256c10c800908)
            check_type(argname="argument envs_to_inject", value=envs_to_inject, expected_type=type_hints["envs_to_inject"])
            check_type(argname="argument envs_from_task_def", value=envs_from_task_def, expected_type=type_hints["envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "injectAdditionalEnvironments", [envs_to_inject, envs_from_task_def]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    def _override_additional_environments(
        self,
        envs_to_override: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param envs_to_override: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__77e2d3e425835d619b9fe3e1de373e527efc11eec32cd8260ccb59910b02dc4c)
            check_type(argname="argument envs_to_override", value=envs_to_override, expected_type=type_hints["envs_to_override"])
            check_type(argname="argument envs_from_task_def", value=envs_from_task_def, expected_type=type_hints["envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "overrideAdditionalEnvironments", [envs_to_override, envs_from_task_def]))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Injector).__jsii_proxy_class__ = lambda : _InjectorProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.InstrumentationProps",
    jsii_struct_bases=[],
    name_mapping={"sdk_version": "sdkVersion", "runtime_platform": "runtimePlatform"},
)
class InstrumentationProps:
    def __init__(
        self,
        *,
        sdk_version: "InstrumentationVersion",
        runtime_platform: typing.Optional[typing.Union["_aws_cdk_aws_ecs_ceddda9d.RuntimePlatform", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Interface for instrumentation properties.

        :param sdk_version: (experimental) The version of the instrumentation.
        :param runtime_platform: (experimental) The runtime platform of the instrumentation. Default: - the runtime platform specified through the input TaskDefinition.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from constructs import Construct
            import aws_cdk.aws_applicationsignals_alpha as appsignals
            import aws_cdk as cdk
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            
            class MyStack(cdk.Stack):
                def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                    super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
            
                    vpc = ec2.Vpc(self, "TestVpc")
                    cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
            
                    # Define Task Definition for CloudWatch agent (Daemon)
                    cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                        network_mode=ecs.NetworkMode.HOST
                    )
            
                    appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                        task_definition=cw_agent_task_definition,
                        container_name="ecs-cwagent",
                        enable_logging=False,
                        cpu=128,
                        memory_limit_mi_b=64,
                        port_mappings=[ecs.PortMapping(
                            container_port=4316,
                            host_port=4316
                        ), ecs.PortMapping(
                            container_port=2000,
                            host_port=2000
                        )
                        ]
                    )
            
                    # Create the CloudWatch Agent daemon service
                    ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                        cluster=cluster,
                        task_definition=cw_agent_task_definition,
                        daemon=True
                    )
            
                    # Define Task Definition for user application
                    sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                        network_mode=ecs.NetworkMode.HOST
                    )
            
                    sample_app_task_definition.add_container("app",
                        image=ecs.ContainerImage.from_registry("test/sample-app"),
                        cpu=0,
                        memory_limit_mi_b=512
                    )
            
                    # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                    appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                        task_definition=sample_app_task_definition,
                        instrumentation=appsignals.InstrumentationProps(
                            sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                        ),
                        service_name="sample-app"
                    )
            
                    ecs.Ec2Service(self, "MySampleApp",
                        cluster=cluster,
                        task_definition=sample_app_task_definition,
                        desired_count=1
                    )
        '''
        if isinstance(runtime_platform, dict):
            runtime_platform = _aws_cdk_aws_ecs_ceddda9d.RuntimePlatform(**runtime_platform)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__30f3a873cce9bc04d8a5cbdf66e4dfc92f40184f5b6790e7dda9be8c7c75fe68)
            check_type(argname="argument sdk_version", value=sdk_version, expected_type=type_hints["sdk_version"])
            check_type(argname="argument runtime_platform", value=runtime_platform, expected_type=type_hints["runtime_platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sdk_version": sdk_version,
        }
        if runtime_platform is not None:
            self._values["runtime_platform"] = runtime_platform

    @builtins.property
    def sdk_version(self) -> "InstrumentationVersion":
        '''(experimental) The version of the instrumentation.

        :stability: experimental
        '''
        result = self._values.get("sdk_version")
        assert result is not None, "Required property 'sdk_version' is missing"
        return typing.cast("InstrumentationVersion", result)

    @builtins.property
    def runtime_platform(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ecs_ceddda9d.RuntimePlatform"]:
        '''(experimental) The runtime platform of the instrumentation.

        :default: - the runtime platform specified through the input TaskDefinition.

        :stability: experimental
        '''
        result = self._values.get("runtime_platform")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecs_ceddda9d.RuntimePlatform"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstrumentationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InstrumentationVersion(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.InstrumentationVersion",
):
    '''(experimental) Base class for instrumentation versions.

    Provides functionality to generate image URIs for different instrumentation types.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
        
                # Define Task Definition for CloudWatch agent (Daemon)
                cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                    task_definition=cw_agent_task_definition,
                    container_name="ecs-cwagent",
                    enable_logging=False,
                    cpu=128,
                    memory_limit_mi_b=64,
                    port_mappings=[ecs.PortMapping(
                        container_port=4316,
                        host_port=4316
                    ), ecs.PortMapping(
                        container_port=2000,
                        host_port=2000
                    )
                    ]
                )
        
                # Create the CloudWatch Agent daemon service
                ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                    cluster=cluster,
                    task_definition=cw_agent_task_definition,
                    daemon=True
                )
        
                # Define Task Definition for user application
                sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                sample_app_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app"),
                    cpu=0,
                    memory_limit_mi_b=512
                )
        
                # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=sample_app_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                    ),
                    service_name="sample-app"
                )
        
                ecs.Ec2Service(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=sample_app_task_definition,
                    desired_count=1
                )
    '''

    def __init__(
        self,
        image_repo: builtins.str,
        version: builtins.str,
        memory_limit: jsii.Number,
    ) -> None:
        '''
        :param image_repo: -
        :param version: -
        :param memory_limit: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__989198f6fafd3ca55c39b81f4dc4b469ca56d458b4311d247f0fe18895701e58)
            check_type(argname="argument image_repo", value=image_repo, expected_type=type_hints["image_repo"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        jsii.create(self.__class__, self, [image_repo, version, memory_limit])

    @jsii.member(jsii_name="imageURI")
    def image_uri(self) -> builtins.str:
        '''(experimental) Get the image URI for the instrumentation version.

        :return: The image URI.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "imageURI", []))

    @jsii.member(jsii_name="memoryLimitMiB")
    def memory_limit_mib(self) -> jsii.Number:
        '''(experimental) Get the memory limit in MiB for the instrumentation version.

        :return: The memory limit

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.invoke(self, "memoryLimitMiB", []))

    @builtins.property
    @jsii.member(jsii_name="imageRepo")
    def _image_repo(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "imageRepo"))

    @builtins.property
    @jsii.member(jsii_name="memoryLimit")
    def _memory_limit(self) -> jsii.Number:
        '''
        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "memoryLimit"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def _version(self) -> builtins.str:
        '''
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))


class _InstrumentationVersionProxy(InstrumentationVersion):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InstrumentationVersion).__jsii_proxy_class__ = lambda : _InstrumentationVersionProxy


class JavaInjector(
    Injector,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.JavaInjector",
):
    '''(experimental) Java-specific implementation of the SDK injector.

    Handles Java agent configuration and environment setup.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        # instrumentation_version: applicationsignals_alpha.InstrumentationVersion
        
        java_injector = applicationsignals_alpha.JavaInjector("sharedVolumeName", instrumentation_version, [
            name="name",
            value="value"
        ])
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7403c797b04ab9a0cbda947dff697fba5302781a4e42f2ffbd2d0ec4b4d766ca)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, override_environments])

    @jsii.member(jsii_name="injectAdditionalEnvironments")
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param _envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f09a1c5208eb108a63693921a7b494fabb652de3a8eeaf16dff057c6a0bd3b8a)
            check_type(argname="argument envs_to_inject", value=envs_to_inject, expected_type=type_hints["envs_to_inject"])
            check_type(argname="argument _envs_from_task_def", value=_envs_from_task_def, expected_type=type_hints["_envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "injectAdditionalEnvironments", [envs_to_inject, _envs_from_task_def]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    def _override_additional_environments(
        self,
        _envs_to_override: typing.Mapping[builtins.str, builtins.str],
        _override_environments: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param _envs_to_override: -
        :param _override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b90b697fdf33f347fe1633b1bf76c6bbedfa2b9b62115e409872a3c9fdfb9f41)
            check_type(argname="argument _envs_to_override", value=_envs_to_override, expected_type=type_hints["_envs_to_override"])
            check_type(argname="argument _override_environments", value=_override_environments, expected_type=type_hints["_override_environments"])
        return typing.cast(None, jsii.invoke(self, "overrideAdditionalEnvironments", [_envs_to_override, _override_environments]))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))


class JavaInstrumentation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.JavaInstrumentation",
):
    '''(experimental) Java-specific OpenTelemetry instrumentation configurations.

    Contains constants for Java agent setup and tool options.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        java_instrumentation = applicationsignals_alpha.JavaInstrumentation()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="JAVA_TOOL_OPTIONS")
    def JAVA_TOOL_OPTIONS(cls) -> builtins.str:
        '''(experimental) Java tool options environment variable.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "JAVA_TOOL_OPTIONS"))


class JavaInstrumentationVersion(
    InstrumentationVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.JavaInstrumentationVersion",
):
    '''(experimental) Available versions for Java instrumentation.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__()
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
        
                fargate_task_definition = ecs.FargateTaskDefinition(self, "SampleAppTaskDefinition",
                    cpu=2048,
                    memory_limit_mi_b=4096
                )
        
                fargate_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app")
                )
        
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=fargate_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.JavaInstrumentationVersion.V2_10_0
                    ),
                    service_name="sample-app",
                    cloud_watch_agent_sidecar=appsignals.CloudWatchAgentOptions(
                        container_name="cloudwatch-agent",
                        enable_logging=True,
                        cpu=256,
                        memory_limit_mi_b=512
                    )
                )
        
                ecs.FargateService(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=fargate_task_definition,
                    desired_count=1
                )
    '''

    def __init__(
        self,
        image_repo: builtins.str,
        version: builtins.str,
        memory_limit: jsii.Number,
    ) -> None:
        '''
        :param image_repo: -
        :param version: -
        :param memory_limit: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6d004882f88e1f1b003370930d225c933dce58799455a6072a30c3e3f247cc0a)
            check_type(argname="argument image_repo", value=image_repo, expected_type=type_hints["image_repo"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        jsii.create(self.__class__, self, [image_repo, version, memory_limit])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_MEMORY_LIMIT_MIB")
    def DEFAULT_MEMORY_LIMIT_MIB(cls) -> jsii.Number:
        '''(experimental) The default memory limit of the Java instrumentation.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_MEMORY_LIMIT_MIB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IMAGE_REPO")
    def IMAGE_REPO(cls) -> builtins.str:
        '''(experimental) The image repository for Java instrumentation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IMAGE_REPO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_32_6")
    def V1_32_6(cls) -> "JavaInstrumentationVersion":
        '''(experimental) ADOT Java Instrumentation version 1.32.6.

        :stability: experimental
        '''
        return typing.cast("JavaInstrumentationVersion", jsii.sget(cls, "V1_32_6"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_33_0")
    def V1_33_0(cls) -> "JavaInstrumentationVersion":
        '''(experimental) ADOT Java Instrumentation version 1.33.0.

        :stability: experimental
        '''
        return typing.cast("JavaInstrumentationVersion", jsii.sget(cls, "V1_33_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V2_10_0")
    def V2_10_0(cls) -> "JavaInstrumentationVersion":
        '''(experimental) ADOT Java Instrumentation version 2.10.0.

        :stability: experimental
        '''
        return typing.cast("JavaInstrumentationVersion", jsii.sget(cls, "V2_10_0"))


class LogsExporting(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.LogsExporting",
):
    '''(experimental) OpenTelemetry logs exporter configurations.

    Contains constants for configuring log export behavior.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        logs_exporting = applicationsignals_alpha.LogsExporting()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_LOGS_EXPORTER")
    def OTEL_LOGS_EXPORTER(cls) -> builtins.str:
        '''(experimental) Configuration for OpenTelemetry logs exporter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_LOGS_EXPORTER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_LOGS_EXPORTER_NONE")
    def OTEL_LOGS_EXPORTER_NONE(cls) -> builtins.str:
        '''(experimental) Disable logs export.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_LOGS_EXPORTER_NONE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_LOGS_EXPORTER_OTLP")
    def OTEL_LOGS_EXPORTER_OTLP(cls) -> builtins.str:
        '''(experimental) Enable OTLP logs export.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_LOGS_EXPORTER_OTLP"))


class MetricsExporting(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.MetricsExporting",
):
    '''(experimental) OpenTelemetry metrics exporter configurations.

    Contains constants for configuring metrics export behavior.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        metrics_exporting = applicationsignals_alpha.MetricsExporting()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_METRICS_EXPORTER")
    def OTEL_METRICS_EXPORTER(cls) -> builtins.str:
        '''(experimental) Configuration for OpenTelemetry metrics exporter.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_METRICS_EXPORTER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_METRICS_EXPORTER_NONE")
    def OTEL_METRICS_EXPORTER_NONE(cls) -> builtins.str:
        '''(experimental) Disable metrics export.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_METRICS_EXPORTER_NONE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_METRICS_EXPORTER_OTLP")
    def OTEL_METRICS_EXPORTER_OTLP(cls) -> builtins.str:
        '''(experimental) Enable OTLP metrics export.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_METRICS_EXPORTER_OTLP"))


class NodeInjector(
    Injector,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.NodeInjector",
):
    '''(experimental) Node.js-specific implementation of the SDK injector. Handles Node.js auto-instrumentation setup and NODE_OPTIONS configuration.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        # instrumentation_version: applicationsignals_alpha.InstrumentationVersion
        
        node_injector = applicationsignals_alpha.NodeInjector("sharedVolumeName", instrumentation_version, [
            name="name",
            value="value"
        ])
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__87c93d0c5a8652675cf804e04ef3d62c6e7ad6e1d3296c9ad58f63fb625f55af)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, override_environments])

    @jsii.member(jsii_name="injectAdditionalEnvironments")
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param _envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__39127a0a5ae88f9a1b0c80264ce2db9f9784b67f046d3ed2be5d2d20a7dfe19e)
            check_type(argname="argument envs_to_inject", value=envs_to_inject, expected_type=type_hints["envs_to_inject"])
            check_type(argname="argument _envs_from_task_def", value=_envs_from_task_def, expected_type=type_hints["_envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "injectAdditionalEnvironments", [envs_to_inject, _envs_from_task_def]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    def _override_additional_environments(
        self,
        envs_to_override: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param envs_to_override: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cadfce433e7a0ec76c4a4565867dc755986ea91aa0566d22ac44926040145425)
            check_type(argname="argument envs_to_override", value=envs_to_override, expected_type=type_hints["envs_to_override"])
            check_type(argname="argument envs_from_task_def", value=envs_from_task_def, expected_type=type_hints["envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "overrideAdditionalEnvironments", [envs_to_override, envs_from_task_def]))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))


class NodeInstrumentation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.NodeInstrumentation",
):
    '''(experimental) Node-specific OpenTelemetry instrumentation configurations.

    Contains constants for Node.js runtime settings and options.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        node_instrumentation = applicationsignals_alpha.NodeInstrumentation()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODE_OPTIONS")
    def NODE_OPTIONS(cls) -> builtins.str:
        '''(experimental) Node.js options environment variable.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "NODE_OPTIONS"))


class NodeInstrumentationVersion(
    InstrumentationVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.NodeInstrumentationVersion",
):
    '''(experimental) Available versions for Node.js instrumentation.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        node_instrumentation_version = applicationsignals_alpha.NodeInstrumentationVersion("imageRepo", "version", 123)
    '''

    def __init__(
        self,
        image_repo: builtins.str,
        version: builtins.str,
        memory_limit: jsii.Number,
    ) -> None:
        '''
        :param image_repo: -
        :param version: -
        :param memory_limit: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3510d8584f0983d1afd873d320da180001785a54ca6bc7700291583211963529)
            check_type(argname="argument image_repo", value=image_repo, expected_type=type_hints["image_repo"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        jsii.create(self.__class__, self, [image_repo, version, memory_limit])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_MEMORY_LIMIT_MIB")
    def DEFAULT_MEMORY_LIMIT_MIB(cls) -> jsii.Number:
        '''(experimental) The default memory limit of the Node.js instrumentation.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_MEMORY_LIMIT_MIB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IMAGE_REPO")
    def IMAGE_REPO(cls) -> builtins.str:
        '''(experimental) The image repository for Node.js instrumentation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IMAGE_REPO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V0_5_0")
    def V0_5_0(cls) -> "NodeInstrumentationVersion":
        '''(experimental) ADOT Node.js Instrumentation version 0.5.0.

        :stability: experimental
        '''
        return typing.cast("NodeInstrumentationVersion", jsii.sget(cls, "V0_5_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V0_6_0")
    def V0_6_0(cls) -> "NodeInstrumentationVersion":
        '''(experimental) ADOT Node.js Instrumentation version 0.6.0.

        :stability: experimental
        '''
        return typing.cast("NodeInstrumentationVersion", jsii.sget(cls, "V0_6_0"))


class PythonInjector(
    Injector,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.PythonInjector",
):
    '''(experimental) Python-specific implementation of the SDK injector.

    Handles Python auto-instrumentation setup and PYTHONPATH configuration.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        # instrumentation_version: applicationsignals_alpha.InstrumentationVersion
        
        python_injector = applicationsignals_alpha.PythonInjector("sharedVolumeName", instrumentation_version, [
            name="name",
            value="value"
        ])
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__755df21cd88a372ea7ecfa20c4f5f44a6e5339e04d041c32c0c91670abc94d4e)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, override_environments])

    @jsii.member(jsii_name="injectAdditionalEnvironments")
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param _envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1e118e5b7ed3aedbfefc719f804a8b80c450909dd106d79abaaf85cacbb9f60c)
            check_type(argname="argument envs_to_inject", value=envs_to_inject, expected_type=type_hints["envs_to_inject"])
            check_type(argname="argument _envs_from_task_def", value=_envs_from_task_def, expected_type=type_hints["_envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "injectAdditionalEnvironments", [envs_to_inject, _envs_from_task_def]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    def _override_additional_environments(
        self,
        envs_to_override: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param envs_to_override: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f97d48c6a23d98c5c4c2dcde6c8129adab13c99e79e680796863795a9196864c)
            check_type(argname="argument envs_to_override", value=envs_to_override, expected_type=type_hints["envs_to_override"])
            check_type(argname="argument envs_from_task_def", value=envs_from_task_def, expected_type=type_hints["envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "overrideAdditionalEnvironments", [envs_to_override, envs_from_task_def]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHON_ENVS")
    def PYTHON_ENVS(cls) -> typing.List["EnvironmentExtension"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["EnvironmentExtension"], jsii.sget(cls, "PYTHON_ENVS"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))


class PythonInstrumentation(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.PythonInstrumentation",
):
    '''(experimental) Python-specific OpenTelemetry instrumentation configurations.

    Contains constants for Python distribution, configurator, and path settings.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        python_instrumentation = applicationsignals_alpha.PythonInstrumentation()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_PYTHON_CONFIGURATOR")
    def OTEL_PYTHON_CONFIGURATOR(cls) -> builtins.str:
        '''(experimental) Python OpenTelemetry configurator setting.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_PYTHON_CONFIGURATOR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_PYTHON_CONFIGURATOR_AWS_CONFIGURATOR")
    def OTEL_PYTHON_CONFIGURATOR_AWS_CONFIGURATOR(cls) -> builtins.str:
        '''(experimental) AWS configurator for Python OpenTelemetry.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_PYTHON_CONFIGURATOR_AWS_CONFIGURATOR"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_PYTHON_DISTRO")
    def OTEL_PYTHON_DISTRO(cls) -> builtins.str:
        '''(experimental) Python OpenTelemetry distribution configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_PYTHON_DISTRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_PYTHON_DISTRO_AWS_DISTRO")
    def OTEL_PYTHON_DISTRO_AWS_DISTRO(cls) -> builtins.str:
        '''(experimental) AWS distribution for Python OpenTelemetry.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_PYTHON_DISTRO_AWS_DISTRO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PYTHONPATH")
    def PYTHONPATH(cls) -> builtins.str:
        '''(experimental) Python path environment variable.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "PYTHONPATH"))


class PythonInstrumentationVersion(
    InstrumentationVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.PythonInstrumentationVersion",
):
    '''(experimental) Available versions for Python instrumentation.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
        
                # Define Task Definition for CloudWatch agent (Daemon)
                cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                    task_definition=cw_agent_task_definition,
                    container_name="ecs-cwagent",
                    enable_logging=False,
                    cpu=128,
                    memory_limit_mi_b=64,
                    port_mappings=[ecs.PortMapping(
                        container_port=4316,
                        host_port=4316
                    ), ecs.PortMapping(
                        container_port=2000,
                        host_port=2000
                    )
                    ]
                )
        
                # Create the CloudWatch Agent daemon service
                ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                    cluster=cluster,
                    task_definition=cw_agent_task_definition,
                    daemon=True
                )
        
                # Define Task Definition for user application
                sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                    network_mode=ecs.NetworkMode.HOST
                )
        
                sample_app_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app"),
                    cpu=0,
                    memory_limit_mi_b=512
                )
        
                # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=sample_app_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                    ),
                    service_name="sample-app"
                )
        
                ecs.Ec2Service(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=sample_app_task_definition,
                    desired_count=1
                )
    '''

    def __init__(
        self,
        image_repo: builtins.str,
        version: builtins.str,
        memory_limit: jsii.Number,
    ) -> None:
        '''
        :param image_repo: -
        :param version: -
        :param memory_limit: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d0bd4a76db437dac5011c5e2a64453ff52ded12780b4f71ddfdfe1a2144089cf)
            check_type(argname="argument image_repo", value=image_repo, expected_type=type_hints["image_repo"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        jsii.create(self.__class__, self, [image_repo, version, memory_limit])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_MEMORY_LIMIT_MIB")
    def DEFAULT_MEMORY_LIMIT_MIB(cls) -> jsii.Number:
        '''(experimental) The default memory limit of the Python instrumentation.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_MEMORY_LIMIT_MIB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IMAGE_REPO")
    def IMAGE_REPO(cls) -> builtins.str:
        '''(experimental) The image repository for Python instrumentation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IMAGE_REPO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V0_8_0")
    def V0_8_0(cls) -> "PythonInstrumentationVersion":
        '''(experimental) ADOT Python Instrumentation version 0.8.0.

        :stability: experimental
        '''
        return typing.cast("PythonInstrumentationVersion", jsii.sget(cls, "V0_8_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V0_9_0")
    def V0_9_0(cls) -> "PythonInstrumentationVersion":
        '''(experimental) ADOT Python Instrumentation version 0.8.0.

        :stability: experimental
        '''
        return typing.cast("PythonInstrumentationVersion", jsii.sget(cls, "V0_9_0"))


class TraceExporting(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.TraceExporting",
):
    '''(experimental) OpenTelemetry trace exporter and sampling configurations.

    Contains constants for trace endpoints, sampling strategies, and propagation formats.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from constructs import Construct
        import aws_cdk.aws_applicationsignals_alpha as appsignals
        import aws_cdk as cdk
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_ecs as ecs
        from aws_cdk.aws_servicediscovery import PrivateDnsNamespace
        
        class MyStack(cdk.Stack):
            def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
        
                vpc = ec2.Vpc(self, "TestVpc")
                cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
                dns_namespace = PrivateDnsNamespace(self, "Namespace",
                    vpc=vpc,
                    name="local"
                )
                security_group = ec2.SecurityGroup(self, "ECSSG", vpc=vpc)
                security_group.add_ingress_rule(security_group, ec2.Port.tcp_range(0, 65535))
        
                # Define Task Definition for CloudWatch agent (Replica)
                cw_agent_task_definition = ecs.FargateTaskDefinition(self, "CloudWatchAgentTaskDefinition")
        
                appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                    task_definition=cw_agent_task_definition,
                    container_name="ecs-cwagent",
                    enable_logging=False,
                    cpu=128,
                    memory_limit_mi_b=64,
                    port_mappings=[ecs.PortMapping(
                        name="cwagent-4316",
                        container_port=4316,
                        host_port=4316
                    ), ecs.PortMapping(
                        name="cwagent-2000",
                        container_port=2000,
                        host_port=2000
                    )
                    ]
                )
        
                # Create the CloudWatch Agent replica service with service connect
                ecs.FargateService(self, "CloudWatchAgentService",
                    cluster=cluster,
                    task_definition=cw_agent_task_definition,
                    security_groups=[security_group],
                    service_connect_configuration=ecs.ServiceConnectProps(
                        namespace=dns_namespace.namespace_arn,
                        services=[ecs.ServiceConnectService(
                            port_mapping_name="cwagent-4316",
                            dns_name="cwagent-4316-http",
                            port=4316
                        ), ecs.ServiceConnectService(
                            port_mapping_name="cwagent-2000",
                            dns_name="cwagent-2000-http",
                            port=2000
                        )
                        ]
                    ),
                    desired_count=1
                )
        
                # Define Task Definition for user application
                sample_app_task_definition = ecs.FargateTaskDefinition(self, "SampleAppTaskDefinition")
        
                sample_app_task_definition.add_container("app",
                    image=ecs.ContainerImage.from_registry("test/sample-app"),
                    cpu=0,
                    memory_limit_mi_b=512
                )
        
                # Overwrite environment variables to connect to the CloudWatch Agent service just created
                appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                    task_definition=sample_app_task_definition,
                    instrumentation=appsignals.InstrumentationProps(
                        sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                    ),
                    service_name="sample-app",
                    override_environments=[appsignals.EnvironmentExtension(
                        name=appsignals.CommonExporting.OTEL_AWS_APPLICATION_SIGNALS_EXPORTER_ENDPOINT,
                        value="http://cwagent-4316-http:4316/v1/metrics"
                    ), appsignals.EnvironmentExtension(
                        name=appsignals.TraceExporting.OTEL_EXPORTER_OTLP_TRACES_ENDPOINT,
                        value="http://cwagent-4316-http:4316/v1/traces"
                    ), appsignals.EnvironmentExtension(
                        name=appsignals.TraceExporting.OTEL_TRACES_SAMPLER_ARG,
                        value="endpoint=http://cwagent-2000-http:2000"
                    )
                    ]
                )
        
                # Create ECS Service with service connect configuration
                ecs.FargateService(self, "MySampleApp",
                    cluster=cluster,
                    task_definition=sample_app_task_definition,
                    service_connect_configuration=ecs.ServiceConnectProps(
                        namespace=dns_namespace.namespace_arn
                    ),
                    desired_count=1
                )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    def OTEL_EXPORTER_OTLP_TRACES_ENDPOINT(cls) -> builtins.str:
        '''(experimental) Endpoint configuration for OTLP traces.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_LOCAL_CWA")
    def OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_LOCAL_CWA(cls) -> builtins.str:
        '''(experimental) Local CloudWatch Agent endpoint for traces.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_EXPORTER_OTLP_TRACES_ENDPOINT_LOCAL_CWA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_PROPAGATORS")
    def OTEL_PROPAGATORS(cls) -> builtins.str:
        '''(experimental) Configuration for trace context propagation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_PROPAGATORS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_PROPAGATORS_APPLICATION_SIGNALS")
    def OTEL_PROPAGATORS_APPLICATION_SIGNALS(cls) -> builtins.str:
        '''(experimental) Supported propagation formats for Application Signals.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_PROPAGATORS_APPLICATION_SIGNALS"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER")
    def OTEL_TRACES_SAMPLER(cls) -> builtins.str:
        '''(experimental) Sampling configuration for traces.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_ALWAYS_OFF")
    def OTEL_TRACES_SAMPLER_ALWAYS_OFF(cls) -> builtins.str:
        '''(experimental) Sample no traces.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_ALWAYS_OFF"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_ALWAYS_ON")
    def OTEL_TRACES_SAMPLER_ALWAYS_ON(cls) -> builtins.str:
        '''(experimental) Sample all traces.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_ALWAYS_ON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_ARG")
    def OTEL_TRACES_SAMPLER_ARG(cls) -> builtins.str:
        '''(experimental) Arguments for trace sampler configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_ARG"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_ARG_LOCAL_CWA")
    def OTEL_TRACES_SAMPLER_ARG_LOCAL_CWA(cls) -> builtins.str:
        '''(experimental) Local CloudWatch Agent endpoint for sampler.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_ARG_LOCAL_CWA"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_PARENT_BASED_ALWAYS_OFF")
    def OTEL_TRACES_SAMPLER_PARENT_BASED_ALWAYS_OFF(cls) -> builtins.str:
        '''(experimental) Parent-based always off sampling.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_PARENT_BASED_ALWAYS_OFF"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_PARENT_BASED_ALWAYS_ON")
    def OTEL_TRACES_SAMPLER_PARENT_BASED_ALWAYS_ON(cls) -> builtins.str:
        '''(experimental) Parent-based always on sampling.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_PARENT_BASED_ALWAYS_ON"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_PARENT_BASED_TRACEID_RATIO")
    def OTEL_TRACES_SAMPLER_PARENT_BASED_TRACEID_RATIO(cls) -> builtins.str:
        '''(experimental) Parent-based trace ID ratio sampling.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_PARENT_BASED_TRACEID_RATIO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_TRACEID_RATIO")
    def OTEL_TRACES_SAMPLER_TRACEID_RATIO(cls) -> builtins.str:
        '''(experimental) Trace ID ratio based sampling.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_TRACEID_RATIO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="OTEL_TRACES_SAMPLER_XRAY")
    def OTEL_TRACES_SAMPLER_XRAY(cls) -> builtins.str:
        '''(experimental) X-Ray sampling strategy.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "OTEL_TRACES_SAMPLER_XRAY"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.CloudWatchAgentIntegrationProps",
    jsii_struct_bases=[CloudWatchAgentOptions],
    name_mapping={
        "container_name": "containerName",
        "agent_config": "agentConfig",
        "cpu": "cpu",
        "enable_logging": "enableLogging",
        "essential": "essential",
        "memory_limit_mib": "memoryLimitMiB",
        "memory_reservation_mib": "memoryReservationMiB",
        "operating_system_family": "operatingSystemFamily",
        "port_mappings": "portMappings",
        "task_definition": "taskDefinition",
    },
)
class CloudWatchAgentIntegrationProps(CloudWatchAgentOptions):
    def __init__(
        self,
        *,
        container_name: builtins.str,
        agent_config: typing.Optional[builtins.str] = None,
        cpu: typing.Optional[jsii.Number] = None,
        enable_logging: typing.Optional[builtins.bool] = None,
        essential: typing.Optional[builtins.bool] = None,
        memory_limit_mib: typing.Optional[jsii.Number] = None,
        memory_reservation_mib: typing.Optional[jsii.Number] = None,
        operating_system_family: typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"] = None,
        port_mappings: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_aws_ecs_ceddda9d.PortMapping", typing.Dict[builtins.str, typing.Any]]]] = None,
        task_definition: "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition",
    ) -> None:
        '''(experimental) Properties for integrating CloudWatch Agent into an ECS task definition.

        :param container_name: (experimental) Name of the CloudWatch Agent container.
        :param agent_config: (experimental) Custom agent configuration in JSON format. Default: - Uses default configuration for Application Signals
        :param cpu: (experimental) The minimum number of CPU units to reserve for the container. Default: - No minimum CPU units reserved.
        :param enable_logging: (experimental) Whether to enable logging for the CloudWatch Agent. Default: - false
        :param essential: (experimental) Start as an essential container. Default: - true
        :param memory_limit_mib: (experimental) The amount (in MiB) of memory to present to the container. Default: - No memory limit.
        :param memory_reservation_mib: (experimental) The soft limit (in MiB) of memory to reserve for the container. Default: - No memory reserved.
        :param operating_system_family: (experimental) Operating system family for the CloudWatch Agent. Default: - Linux
        :param port_mappings: (experimental) The port mappings to add to the container definition. Default: - No ports are mapped.
        :param task_definition: (experimental) The task definition to integrate CloudWatch agent into. [disable-awslint:ref-via-interface]

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from constructs import Construct
            import aws_cdk.aws_applicationsignals_alpha as appsignals
            import aws_cdk as cdk
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_ecs as ecs
            
            class MyStack(cdk.Stack):
                def __init__(self, scope=None, id=None, *, description=None, env=None, stackName=None, tags=None, notificationArns=None, synthesizer=None, terminationProtection=None, analyticsReporting=None, crossRegionReferences=None, permissionsBoundary=None, suppressTemplateIndentation=None, propertyInjectors=None):
                    super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, notificationArns=notificationArns, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting, crossRegionReferences=crossRegionReferences, permissionsBoundary=permissionsBoundary, suppressTemplateIndentation=suppressTemplateIndentation, propertyInjectors=propertyInjectors)
            
                    vpc = ec2.Vpc(self, "TestVpc")
                    cluster = ecs.Cluster(self, "TestCluster", vpc=vpc)
            
                    # Define Task Definition for CloudWatch agent (Daemon)
                    cw_agent_task_definition = ecs.Ec2TaskDefinition(self, "CloudWatchAgentTaskDefinition",
                        network_mode=ecs.NetworkMode.HOST
                    )
            
                    appsignals.CloudWatchAgentIntegration(self, "CloudWatchAgentIntegration",
                        task_definition=cw_agent_task_definition,
                        container_name="ecs-cwagent",
                        enable_logging=False,
                        cpu=128,
                        memory_limit_mi_b=64,
                        port_mappings=[ecs.PortMapping(
                            container_port=4316,
                            host_port=4316
                        ), ecs.PortMapping(
                            container_port=2000,
                            host_port=2000
                        )
                        ]
                    )
            
                    # Create the CloudWatch Agent daemon service
                    ecs.Ec2Service(self, "CloudWatchAgentDaemon",
                        cluster=cluster,
                        task_definition=cw_agent_task_definition,
                        daemon=True
                    )
            
                    # Define Task Definition for user application
                    sample_app_task_definition = ecs.Ec2TaskDefinition(self, "SampleAppTaskDefinition",
                        network_mode=ecs.NetworkMode.HOST
                    )
            
                    sample_app_task_definition.add_container("app",
                        image=ecs.ContainerImage.from_registry("test/sample-app"),
                        cpu=0,
                        memory_limit_mi_b=512
                    )
            
                    # No CloudWatch Agent side car is needed as application container communicates to CloudWatch Agent daemon through host network
                    appsignals.ApplicationSignalsIntegration(self, "ApplicationSignalsIntegration",
                        task_definition=sample_app_task_definition,
                        instrumentation=appsignals.InstrumentationProps(
                            sdk_version=appsignals.PythonInstrumentationVersion.V0_8_0
                        ),
                        service_name="sample-app"
                    )
            
                    ecs.Ec2Service(self, "MySampleApp",
                        cluster=cluster,
                        task_definition=sample_app_task_definition,
                        desired_count=1
                    )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__20255def7d9260c1403c6d5cae3fee890c97955fd3b8ba64a894f3c361ed250f)
            check_type(argname="argument container_name", value=container_name, expected_type=type_hints["container_name"])
            check_type(argname="argument agent_config", value=agent_config, expected_type=type_hints["agent_config"])
            check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
            check_type(argname="argument enable_logging", value=enable_logging, expected_type=type_hints["enable_logging"])
            check_type(argname="argument essential", value=essential, expected_type=type_hints["essential"])
            check_type(argname="argument memory_limit_mib", value=memory_limit_mib, expected_type=type_hints["memory_limit_mib"])
            check_type(argname="argument memory_reservation_mib", value=memory_reservation_mib, expected_type=type_hints["memory_reservation_mib"])
            check_type(argname="argument operating_system_family", value=operating_system_family, expected_type=type_hints["operating_system_family"])
            check_type(argname="argument port_mappings", value=port_mappings, expected_type=type_hints["port_mappings"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "container_name": container_name,
            "task_definition": task_definition,
        }
        if agent_config is not None:
            self._values["agent_config"] = agent_config
        if cpu is not None:
            self._values["cpu"] = cpu
        if enable_logging is not None:
            self._values["enable_logging"] = enable_logging
        if essential is not None:
            self._values["essential"] = essential
        if memory_limit_mib is not None:
            self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None:
            self._values["memory_reservation_mib"] = memory_reservation_mib
        if operating_system_family is not None:
            self._values["operating_system_family"] = operating_system_family
        if port_mappings is not None:
            self._values["port_mappings"] = port_mappings

    @builtins.property
    def container_name(self) -> builtins.str:
        '''(experimental) Name of the CloudWatch Agent container.

        :stability: experimental
        '''
        result = self._values.get("container_name")
        assert result is not None, "Required property 'container_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_config(self) -> typing.Optional[builtins.str]:
        '''(experimental) Custom agent configuration in JSON format.

        :default: - Uses default configuration for Application Signals

        :stability: experimental
        '''
        result = self._values.get("agent_config")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The minimum number of CPU units to reserve for the container.

        :default: - No minimum CPU units reserved.

        :stability: experimental
        '''
        result = self._values.get("cpu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enable_logging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable logging for the CloudWatch Agent.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("enable_logging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def essential(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Start as an essential container.

        :default: - true

        :stability: experimental
        '''
        result = self._values.get("essential")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount (in MiB) of memory to present to the container.

        :default: - No memory limit.

        :stability: experimental
        '''
        result = self._values.get("memory_limit_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The soft limit (in MiB) of memory to reserve for the container.

        :default: - No memory reserved.

        :stability: experimental
        '''
        result = self._values.get("memory_reservation_mib")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operating_system_family(
        self,
    ) -> typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"]:
        '''(experimental) Operating system family for the CloudWatch Agent.

        :default: - Linux

        :stability: experimental
        '''
        result = self._values.get("operating_system_family")
        return typing.cast(typing.Optional["_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily"], result)

    @builtins.property
    def port_mappings(
        self,
    ) -> typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PortMapping"]]:
        '''(experimental) The port mappings to add to the container definition.

        :default: - No ports are mapped.

        :stability: experimental
        '''
        result = self._values.get("port_mappings")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_aws_ecs_ceddda9d.PortMapping"]], result)

    @builtins.property
    def task_definition(self) -> "_aws_cdk_aws_ecs_ceddda9d.TaskDefinition":
        '''(experimental) The task definition to integrate CloudWatch agent into.

        [disable-awslint:ref-via-interface]

        :stability: experimental
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast("_aws_cdk_aws_ecs_ceddda9d.TaskDefinition", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchAgentIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DotNetInjector(
    Injector,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.DotNetInjector",
):
    '''(experimental) Base class for .NET SDK injectors. Contains common .NET configuration settings used by both Windows and Linux implementations.

    :stability: experimental
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__723605dd5f104304bdbe241b72d5f9f481421abbb5da18950597510f7cab0cf9)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, override_environments])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_COMMON_ENVS")
    def DOTNET_COMMON_ENVS(cls) -> typing.List["EnvironmentExtension"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["EnvironmentExtension"], jsii.sget(cls, "DOTNET_COMMON_ENVS"))


class _DotNetInjectorProxy(
    DotNetInjector,
    jsii.proxy_for(Injector), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DotNetInjector).__jsii_proxy_class__ = lambda : _DotNetInjectorProxy


class DotNetLinuxInjector(
    DotNetInjector,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.DotNetLinuxInjector",
):
    '''(experimental) Linux-specific implementation of the .NET SDK injector. Handles CoreCLR profiler setup and paths for Linux environments.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        from aws_cdk import aws_ecs as ecs
        
        # cpu_architecture: ecs.CpuArchitecture
        # instrumentation_version: applicationsignals_alpha.InstrumentationVersion
        
        dot_net_linux_injector = applicationsignals_alpha.DotNetLinuxInjector("sharedVolumeName", instrumentation_version, cpu_architecture, [
            name="name",
            value="value"
        ])
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        cpu_arch: "_aws_cdk_aws_ecs_ceddda9d.CpuArchitecture",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param cpu_arch: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a7e340fe7ecae13da5eca5e4210c20ff95c3ef75e79741676628934b99bc8a9c)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument cpu_arch", value=cpu_arch, expected_type=type_hints["cpu_arch"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, cpu_arch, override_environments])

    @jsii.member(jsii_name="injectAdditionalEnvironments")
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cebec5b075b3e64d0fa79958aae7117913be02a4bcbb7b53aa43752401b51fd7)
            check_type(argname="argument envs_to_inject", value=envs_to_inject, expected_type=type_hints["envs_to_inject"])
            check_type(argname="argument envs_from_task_def", value=envs_from_task_def, expected_type=type_hints["envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "injectAdditionalEnvironments", [envs_to_inject, envs_from_task_def]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    def _override_additional_environments(
        self,
        _envs_to_override: typing.Mapping[builtins.str, builtins.str],
        _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param _envs_to_override: -
        :param _envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__559711f48581411c9f0428f479b70f4b7d8af1a2ddb50938de0460af401d8271)
            check_type(argname="argument _envs_to_override", value=_envs_to_override, expected_type=type_hints["_envs_to_override"])
            check_type(argname="argument _envs_from_task_def", value=_envs_from_task_def, expected_type=type_hints["_envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "overrideAdditionalEnvironments", [_envs_to_override, _envs_from_task_def]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_LINUX_ENVS")
    def DOTNET_LINUX_ENVS(cls) -> typing.List["EnvironmentExtension"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["EnvironmentExtension"], jsii.sget(cls, "DOTNET_LINUX_ENVS"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))


class DotNetWindowsInjector(
    DotNetInjector,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.DotNetWindowsInjector",
):
    '''(experimental) Windows-specific implementation of the .NET SDK injector. Handles CoreCLR profiler setup and paths for Windows environments.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        # instrumentation_version: applicationsignals_alpha.InstrumentationVersion
        
        dot_net_windows_injector = applicationsignals_alpha.DotNetWindowsInjector("sharedVolumeName", instrumentation_version, [
            name="name",
            value="value"
        ])
    '''

    def __init__(
        self,
        shared_volume_name: builtins.str,
        instrumentation_version: "InstrumentationVersion",
        override_environments: typing.Optional[typing.Sequence[typing.Union["EnvironmentExtension", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param shared_volume_name: -
        :param instrumentation_version: -
        :param override_environments: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__65dc12e91b7cc122b9c3aa988c239864364839add6877b765e3d6733066ed3ad)
            check_type(argname="argument shared_volume_name", value=shared_volume_name, expected_type=type_hints["shared_volume_name"])
            check_type(argname="argument instrumentation_version", value=instrumentation_version, expected_type=type_hints["instrumentation_version"])
            check_type(argname="argument override_environments", value=override_environments, expected_type=type_hints["override_environments"])
        jsii.create(self.__class__, self, [shared_volume_name, instrumentation_version, override_environments])

    @jsii.member(jsii_name="injectAdditionalEnvironments")
    def _inject_additional_environments(
        self,
        envs_to_inject: typing.Mapping[builtins.str, builtins.str],
        envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Inject additional environment variables to the application container other than the DEFAULT_ENVS.

        :param envs_to_inject: -
        :param envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__b382d5ca42a376d5d27040c3e93f7f77483a90058963945ff046fa8734de7d37)
            check_type(argname="argument envs_to_inject", value=envs_to_inject, expected_type=type_hints["envs_to_inject"])
            check_type(argname="argument envs_from_task_def", value=envs_from_task_def, expected_type=type_hints["envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "injectAdditionalEnvironments", [envs_to_inject, envs_from_task_def]))

    @jsii.member(jsii_name="overrideAdditionalEnvironments")
    def _override_additional_environments(
        self,
        _envs_to_override: typing.Mapping[builtins.str, builtins.str],
        _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Override environment variables in the application container.

        :param _envs_to_override: -
        :param _envs_from_task_def: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7aa5580cbd9d022e77cbd96d2286f17946d76e0cce5d3b107477d0a748d4b220)
            check_type(argname="argument _envs_to_override", value=_envs_to_override, expected_type=type_hints["_envs_to_override"])
            check_type(argname="argument _envs_from_task_def", value=_envs_from_task_def, expected_type=type_hints["_envs_from_task_def"])
        return typing.cast(None, jsii.invoke(self, "overrideAdditionalEnvironments", [_envs_to_override, _envs_from_task_def]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOTNET_WINDOWS_ENVS")
    def DOTNET_WINDOWS_ENVS(cls) -> typing.List["EnvironmentExtension"]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.List["EnvironmentExtension"], jsii.sget(cls, "DOTNET_WINDOWS_ENVS"))

    @builtins.property
    @jsii.member(jsii_name="command")
    def command(self) -> typing.List[builtins.str]:
        '''(experimental) The command to run the init container.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "command"))

    @builtins.property
    @jsii.member(jsii_name="containerPath")
    def container_path(self) -> builtins.str:
        '''(experimental) The path to ADOT SDK agent in the init container.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "containerPath"))


class DotnetInstrumentationVersion(
    InstrumentationVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-applicationsignals-alpha.DotnetInstrumentationVersion",
):
    '''(experimental) Available versions for .NET instrumentation.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_applicationsignals_alpha as applicationsignals_alpha
        
        dotnet_instrumentation_version = applicationsignals_alpha.DotnetInstrumentationVersion("imageRepo", "version", 123)
    '''

    def __init__(
        self,
        image_repo: builtins.str,
        version: builtins.str,
        memory_limit: jsii.Number,
    ) -> None:
        '''
        :param image_repo: -
        :param version: -
        :param memory_limit: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__227947dd2c75fe7ff50646f28e69d9bb5e58d3ad37ebf9315976351904dd8371)
            check_type(argname="argument image_repo", value=image_repo, expected_type=type_hints["image_repo"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument memory_limit", value=memory_limit, expected_type=type_hints["memory_limit"])
        jsii.create(self.__class__, self, [image_repo, version, memory_limit])

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_MEMORY_LIMIT_MIB")
    def DEFAULT_MEMORY_LIMIT_MIB(cls) -> jsii.Number:
        '''(experimental) The default memory limit of the .NET instrumentation.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.sget(cls, "DEFAULT_MEMORY_LIMIT_MIB"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="IMAGE_REPO")
    def IMAGE_REPO(cls) -> builtins.str:
        '''(experimental) The image repository for .NET instrumentation.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "IMAGE_REPO"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_6_0")
    def V1_6_0(cls) -> "DotnetInstrumentationVersion":
        '''(experimental) ADOT .NET Instrumentation version 1.6.0.

        :stability: experimental
        '''
        return typing.cast("DotnetInstrumentationVersion", jsii.sget(cls, "V1_6_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_6_0_WINDOWS2019")
    def V1_6_0_WINDOWS2019(cls) -> "DotnetInstrumentationVersion":
        '''(experimental) ADOT .NET Instrumentation version 1.6.0 for Windows 2019.

        :stability: experimental
        '''
        return typing.cast("DotnetInstrumentationVersion", jsii.sget(cls, "V1_6_0_WINDOWS2019"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_6_0_WINDOWS2022")
    def V1_6_0_WINDOWS2022(cls) -> "DotnetInstrumentationVersion":
        '''(experimental) ADOT .NET Instrumentation version 1.6.0 for Windows 2022.

        :stability: experimental
        '''
        return typing.cast("DotnetInstrumentationVersion", jsii.sget(cls, "V1_6_0_WINDOWS2022"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_0")
    def V1_7_0(cls) -> "DotnetInstrumentationVersion":
        '''(experimental) ADOT .NET Instrumentation version 1.7.0.

        :stability: experimental
        '''
        return typing.cast("DotnetInstrumentationVersion", jsii.sget(cls, "V1_7_0"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_0_WINDOWS2019")
    def V1_7_0_WINDOWS2019(cls) -> "DotnetInstrumentationVersion":
        '''(experimental) ADOT .NET Instrumentation version 1.7.0 for Windows 2019.

        :stability: experimental
        '''
        return typing.cast("DotnetInstrumentationVersion", jsii.sget(cls, "V1_7_0_WINDOWS2019"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_7_0_WINDOWS2022")
    def V1_7_0_WINDOWS2022(cls) -> "DotnetInstrumentationVersion":
        '''(experimental) ADOT .NET Instrumentation version 1.7.0 for Windows 2022.

        :stability: experimental
        '''
        return typing.cast("DotnetInstrumentationVersion", jsii.sget(cls, "V1_7_0_WINDOWS2022"))


__all__ = [
    "ApplicationSignalsIntegration",
    "ApplicationSignalsIntegrationProps",
    "CloudWatchAgentIntegration",
    "CloudWatchAgentIntegrationProps",
    "CloudWatchAgentOptions",
    "CloudWatchAgentVersion",
    "CommonExporting",
    "DotNetInjector",
    "DotNetLinuxInjector",
    "DotNetWindowsInjector",
    "DotnetInstrumentation",
    "DotnetInstrumentationVersion",
    "EnvironmentExtension",
    "Injector",
    "InstrumentationProps",
    "InstrumentationVersion",
    "JavaInjector",
    "JavaInstrumentation",
    "JavaInstrumentationVersion",
    "LogsExporting",
    "MetricsExporting",
    "NodeInjector",
    "NodeInstrumentation",
    "NodeInstrumentationVersion",
    "PythonInjector",
    "PythonInstrumentation",
    "PythonInstrumentationVersion",
    "TraceExporting",
]

publication.publish()

def _typecheckingstub__45fc22f9560022d5f606a9a371c1833f463aa1c7bdb573a765baafe38bfb4040(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    instrumentation: typing.Union[InstrumentationProps, typing.Dict[builtins.str, typing.Any]],
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    cloud_watch_agent_sidecar: typing.Optional[typing.Union[CloudWatchAgentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd6fa50a03d0911abf781dabe7f10143f0811de27611dfdaf9ceeefc5b82a804(
    *,
    instrumentation: typing.Union[InstrumentationProps, typing.Dict[builtins.str, typing.Any]],
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    cloud_watch_agent_sidecar: typing.Optional[typing.Union[CloudWatchAgentOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d88d8cd0ef22ce2257442d2a60f0e38524aa23226623a1e7f58323196bdebaf8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    container_name: builtins.str,
    agent_config: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    essential: typing.Optional[builtins.bool] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    operating_system_family: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily] = None,
    port_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.PortMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a45015e4a6a56c1499f4458a2b77c626b987c6f596c335f08463327164cd54b(
    *,
    container_name: builtins.str,
    agent_config: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    essential: typing.Optional[builtins.bool] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    operating_system_family: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily] = None,
    port_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.PortMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__132fb1893dfd6cb3bd0e34ef1067e39cb5c6bcf814379ce6e7a8315999d8dbfd(
    operating_system_family: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4aa9680fa88bf414827c37a058f36194f57ec8c1b651cc1f9f15e5668086e76(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a176319238cff5f99f06e8c96073bb71ca67bb9ad00460eb480526249a85e43a(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fe739a9bf12b91df80438a88b17ef898d49a2a7aa5ec7b48e173667c91ce05(
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9146ad7105b1491db117463af1f3697bb71ccb6cdf38f24a1f7377ac94cce5e7(
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94fc97bfd0d5618005048c5433172a3b7faa7b8c480e7f893f3bd76411bf09f0(
    value: InstrumentationVersion,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf91c135de73ebc450bad91aabf833d9815551c82d4173b7cb9645c03d4325b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d6de8aad617ac6df0bd7cf9bf4320f144dcbd0e4fb0d873ae4256c10c800908(
    envs_to_inject: typing.Mapping[builtins.str, builtins.str],
    envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77e2d3e425835d619b9fe3e1de373e527efc11eec32cd8260ccb59910b02dc4c(
    envs_to_override: typing.Mapping[builtins.str, builtins.str],
    envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f3a873cce9bc04d8a5cbdf66e4dfc92f40184f5b6790e7dda9be8c7c75fe68(
    *,
    sdk_version: InstrumentationVersion,
    runtime_platform: typing.Optional[typing.Union[_aws_cdk_aws_ecs_ceddda9d.RuntimePlatform, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989198f6fafd3ca55c39b81f4dc4b469ca56d458b4311d247f0fe18895701e58(
    image_repo: builtins.str,
    version: builtins.str,
    memory_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7403c797b04ab9a0cbda947dff697fba5302781a4e42f2ffbd2d0ec4b4d766ca(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09a1c5208eb108a63693921a7b494fabb652de3a8eeaf16dff057c6a0bd3b8a(
    envs_to_inject: typing.Mapping[builtins.str, builtins.str],
    _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90b697fdf33f347fe1633b1bf76c6bbedfa2b9b62115e409872a3c9fdfb9f41(
    _envs_to_override: typing.Mapping[builtins.str, builtins.str],
    _override_environments: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d004882f88e1f1b003370930d225c933dce58799455a6072a30c3e3f247cc0a(
    image_repo: builtins.str,
    version: builtins.str,
    memory_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c93d0c5a8652675cf804e04ef3d62c6e7ad6e1d3296c9ad58f63fb625f55af(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39127a0a5ae88f9a1b0c80264ce2db9f9784b67f046d3ed2be5d2d20a7dfe19e(
    envs_to_inject: typing.Mapping[builtins.str, builtins.str],
    _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadfce433e7a0ec76c4a4565867dc755986ea91aa0566d22ac44926040145425(
    envs_to_override: typing.Mapping[builtins.str, builtins.str],
    envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3510d8584f0983d1afd873d320da180001785a54ca6bc7700291583211963529(
    image_repo: builtins.str,
    version: builtins.str,
    memory_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755df21cd88a372ea7ecfa20c4f5f44a6e5339e04d041c32c0c91670abc94d4e(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e118e5b7ed3aedbfefc719f804a8b80c450909dd106d79abaaf85cacbb9f60c(
    envs_to_inject: typing.Mapping[builtins.str, builtins.str],
    _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f97d48c6a23d98c5c4c2dcde6c8129adab13c99e79e680796863795a9196864c(
    envs_to_override: typing.Mapping[builtins.str, builtins.str],
    envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0bd4a76db437dac5011c5e2a64453ff52ded12780b4f71ddfdfe1a2144089cf(
    image_repo: builtins.str,
    version: builtins.str,
    memory_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20255def7d9260c1403c6d5cae3fee890c97955fd3b8ba64a894f3c361ed250f(
    *,
    container_name: builtins.str,
    agent_config: typing.Optional[builtins.str] = None,
    cpu: typing.Optional[jsii.Number] = None,
    enable_logging: typing.Optional[builtins.bool] = None,
    essential: typing.Optional[builtins.bool] = None,
    memory_limit_mib: typing.Optional[jsii.Number] = None,
    memory_reservation_mib: typing.Optional[jsii.Number] = None,
    operating_system_family: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.OperatingSystemFamily] = None,
    port_mappings: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.PortMapping, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723605dd5f104304bdbe241b72d5f9f481421abbb5da18950597510f7cab0cf9(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e340fe7ecae13da5eca5e4210c20ff95c3ef75e79741676628934b99bc8a9c(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    cpu_arch: _aws_cdk_aws_ecs_ceddda9d.CpuArchitecture,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebec5b075b3e64d0fa79958aae7117913be02a4bcbb7b53aa43752401b51fd7(
    envs_to_inject: typing.Mapping[builtins.str, builtins.str],
    envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559711f48581411c9f0428f479b70f4b7d8af1a2ddb50938de0460af401d8271(
    _envs_to_override: typing.Mapping[builtins.str, builtins.str],
    _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65dc12e91b7cc122b9c3aa988c239864364839add6877b765e3d6733066ed3ad(
    shared_volume_name: builtins.str,
    instrumentation_version: InstrumentationVersion,
    override_environments: typing.Optional[typing.Sequence[typing.Union[EnvironmentExtension, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b382d5ca42a376d5d27040c3e93f7f77483a90058963945ff046fa8734de7d37(
    envs_to_inject: typing.Mapping[builtins.str, builtins.str],
    envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aa5580cbd9d022e77cbd96d2286f17946d76e0cce5d3b107477d0a748d4b220(
    _envs_to_override: typing.Mapping[builtins.str, builtins.str],
    _envs_from_task_def: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__227947dd2c75fe7ff50646f28e69d9bb5e58d3ad37ebf9315976351904dd8371(
    image_repo: builtins.str,
    version: builtins.str,
    memory_limit: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass
