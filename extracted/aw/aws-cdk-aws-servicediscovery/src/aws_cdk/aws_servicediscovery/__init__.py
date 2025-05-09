'''
# Amazon ECS Service Discovery Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

This package contains constructs for working with **AWS Cloud Map**

AWS Cloud Map is a fully managed service that you can use to create and
maintain a map of the backend services and resources that your applications
depend on.

For further information on AWS Cloud Map,
see the [AWS Cloud Map documentation](https://docs.aws.amazon.com/cloud-map)

## HTTP Namespace Example

The following example creates an AWS Cloud Map namespace that
supports API calls, creates a service in that namespace, and
registers an instance to it:

```python
import aws_cdk.core as cdk
import aws_cdk.aws_servicediscovery as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
    name="covfefe"
)

service1 = namespace.create_service("NonIpService",
    description="service registering non-ip instances"
)

service1.register_non_ip_instance("NonIpInstance",
    custom_attributes={"arn": "arn:aws:s3:::mybucket"}
)

service2 = namespace.create_service("IpService",
    description="service registering ip instances",
    health_check=servicediscovery.HealthCheckConfig(
        type=servicediscovery.HealthCheckType.HTTP,
        resource_path="/check"
    )
)

service2.register_ip_instance("IpInstance",
    ipv4="54.239.25.192"
)

app.synth()
```

## Private DNS Namespace Example

The following example creates an AWS Cloud Map namespace that
supports both API calls and DNS queries within a vpc, creates a
service in that namespace, and registers a loadbalancer as an
instance:

```python
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elbv2
import aws_cdk.core as cdk
import aws_cdk.aws_servicediscovery as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

vpc = ec2.Vpc(stack, "Vpc", max_azs=2)

namespace = servicediscovery.PrivateDnsNamespace(stack, "Namespace",
    name="boobar.com",
    vpc=vpc
)

service = namespace.create_service("Service",
    dns_record_type=servicediscovery.DnsRecordType.A_AAAA,
    dns_ttl=cdk.Duration.seconds(30),
    load_balancer=True
)

loadbalancer = elbv2.ApplicationLoadBalancer(stack, "LB", vpc=vpc, internet_facing=True)

service.register_load_balancer("Loadbalancer", loadbalancer)

app.synth()
```

## Public DNS Namespace Example

The following example creates an AWS Cloud Map namespace that
supports both API calls and public DNS queries, creates a service in
that namespace, and registers an IP instance:

```python
import aws_cdk.core as cdk
import aws_cdk.aws_servicediscovery as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
    name="foobar.com"
)

service = namespace.create_service("Service",
    name="foo",
    dns_record_type=servicediscovery.DnsRecordType.A,
    dns_ttl=cdk.Duration.seconds(30),
    health_check=servicediscovery.HealthCheckConfig(
        type=servicediscovery.HealthCheckType.HTTPS,
        resource_path="/healthcheck",
        failure_threshold=2
    )
)

service.register_ip_instance("IpInstance",
    ipv4="54.239.25.192",
    port=443
)

app.synth()
```

For DNS namespaces, you can also register instances to services with CNAME records:

```python
import aws_cdk.core as cdk
import aws_cdk.aws_servicediscovery as servicediscovery

app = cdk.App()
stack = cdk.Stack(app, "aws-servicediscovery-integ")

namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
    name="foobar.com"
)

service = namespace.create_service("Service",
    name="foo",
    dns_record_type=servicediscovery.DnsRecordType.CNAME,
    dns_ttl=cdk.Duration.seconds(30)
)

service.register_cname_instance("CnameInstance",
    instance_cname="service.pizza"
)

app.synth()
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
import aws_cdk.aws_elasticloadbalancingv2 as _aws_cdk_aws_elasticloadbalancingv2_e93c784f
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.BaseInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
    },
)
class BaseInstanceProps:
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Used when the resource that's associated with the service instance is accessible using values other than an IP address or a domain name (CNAME), i.e. for non-ip-instances.

        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            base_instance_props = servicediscovery.BaseInstanceProps(
                custom_attributes={
                    "custom_attributes_key": "customAttributes"
                },
                instance_id="instanceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a583c7464f8c139d8dceb66f956e5eebba623400a7680b46c6ccf75f0444249e)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.BaseNamespaceProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description"},
)
class BaseNamespaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            base_namespace_props = servicediscovery.BaseNamespaceProps(
                name="name",
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ee522871d4628f82b79f6e596467b8d6ae558a0c0e319cdec7ee0b649b0dd18)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Namespace.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.BaseServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "custom_health_check": "customHealthCheck",
        "description": "description",
        "health_check": "healthCheck",
        "name": "name",
    },
)
class BaseServiceProps:
    def __init__(
        self,
        *,
        custom_health_check: typing.Optional[typing.Union["HealthCheckCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union["HealthCheckConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Basic props needed to create a service in a given namespace.

        Used by HttpNamespace.createService

        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name

        :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
                name="covfefe"
            )
            
            service1 = namespace.create_service("NonIpService",
                description="service registering non-ip instances"
            )
            
            service1.register_non_ip_instance("NonIpInstance",
                custom_attributes={"arn": "arn:aws:s3:::mybucket"}
            )
            
            service2 = namespace.create_service("IpService",
                description="service registering ip instances",
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTP,
                    resource_path="/check"
                )
            )
            
            service2.register_ip_instance("IpInstance",
                ipv4="54.239.25.192"
            )
            
            app.synth()
        '''
        if isinstance(custom_health_check, dict):
            custom_health_check = HealthCheckCustomConfig(**custom_health_check)
        if isinstance(health_check, dict):
            health_check = HealthCheckConfig(**health_check)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3234580726ea7c1baa9bfb41a16e5e12552a916340e9671bfe9898cdfd467c2f)
            check_type(argname="argument custom_health_check", value=custom_health_check, expected_type=type_hints["custom_health_check"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_health_check is not None:
            self._values["custom_health_check"] = custom_health_check
        if description is not None:
            self._values["description"] = description
        if health_check is not None:
            self._values["health_check"] = health_check
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def custom_health_check(self) -> typing.Optional["HealthCheckCustomConfig"]:
        '''Structure containing failure threshold for a custom health checker.

        Only one of healthCheckConfig or healthCheckCustomConfig can be specified.
        See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html

        :default: none
        '''
        result = self._values.get("custom_health_check")
        return typing.cast(typing.Optional["HealthCheckCustomConfig"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheckConfig"]:
        '''Settings for an optional health check.

        If you specify health check settings, AWS Cloud Map associates the health
        check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can
        be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to
        this service.

        :default: none
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheckConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the Service.

        :default: CloudFormation-generated name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnHttpNamespace(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.CfnHttpNamespace",
):
    '''A CloudFormation ``AWS::ServiceDiscovery::HttpNamespace``.

    The ``HttpNamespace`` resource is an AWS Cloud Map resource type that contains information about an HTTP namespace. Service instances that you register using an HTTP namespace can be discovered using a ``DiscoverInstances`` request but can't be discovered using DNS.

    For the current quota on the number of namespaces that you can create using the same AWS account, see `AWS Cloud Map quotas <https://docs.aws.amazon.com/cloud-map/latest/dg/cloud-map-limits.html>`_ in the ** .

    :cloudformationResource: AWS::ServiceDiscovery::HttpNamespace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        cfn_http_namespace = servicediscovery.CfnHttpNamespace(self, "MyCfnHttpNamespace",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceDiscovery::HttpNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name that you want to assign to this namespace.
        :param description: A description for the namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2911f77aa685ed17d42b798cae8b06b1d85a964a2a3b9704aa149b4e01483fd1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHttpNamespaceProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610af52d6f2eaf2034ee4c2227daafd04fb1be9474dc54562126efad6fbdab28)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0056dcf9bfeb6b3fe02b1ef2c996c450056757b4d7455f5b464adfcd162622c)
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
        '''The Amazon Resource Name (ARN) of the namespace, such as ``arn:aws:service-discovery:us-east-1:123456789012:http-namespace/http-namespace-a1bzhi`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the namespace.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name that you want to assign to this namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d124a27920c5dab8d282baf3e08d222ea680b984dd2bdf123a1321b90595b65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f910bd79b25571798e6e3fef6b16493f0dc0a0f0153417a120adf22b1211e363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CfnHttpNamespaceProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnHttpNamespaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnHttpNamespace``.

        :param name: The name that you want to assign to this namespace.
        :param description: A description for the namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            cfn_http_namespace_props = servicediscovery.CfnHttpNamespaceProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1a661f1544296619903f44581126a75cda827e9c5cc8b5eb5cb7aab3b9e691)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name that you want to assign to this namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-httpnamespace.html#cfn-servicediscovery-httpnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHttpNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnInstance(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.CfnInstance",
):
    '''A CloudFormation ``AWS::ServiceDiscovery::Instance``.

    A complex type that contains information about an instance that AWS Cloud Map creates when you submit a ``RegisterInstance`` request.

    :cloudformationResource: AWS::ServiceDiscovery::Instance
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        # instance_attributes: Any
        
        cfn_instance = servicediscovery.CfnInstance(self, "MyCfnInstance",
            instance_attributes=instance_attributes,
            service_id="serviceId",
        
            # the properties below are optional
            instance_id="instanceId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        instance_attributes: typing.Any,
        service_id: builtins.str,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceDiscovery::Instance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param instance_attributes: A string map that contains the following information for the service that you specify in ``ServiceId`` :. - The attributes that apply to the records that are defined in the service. - For each attribute, the applicable value. Supported attribute keys include the following: - **AWS_ALIAS_DNS_NAME** - If you want AWS Cloud Map to create a Route 53 alias record that routes traffic to an Elastic Load Balancing load balancer, specify the DNS name that is associated with the load balancer. For information about how to get the DNS name, see `AliasTarget->DNSName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-DNSName>`_ in the *Route 53 API Reference* . Note the following: - The configuration for the service that is specified by ``ServiceId`` must include settings for an ``A`` record, an ``AAAA`` record, or both. - In the service that is specified by ``ServiceId`` , the value of ``RoutingPolicy`` must be ``WEIGHTED`` . - If the service that is specified by ``ServiceId`` includes ``HealthCheckConfig`` settings, AWS Cloud Map will create the health check, but it won't associate the health check with the alias record. - Auto naming currently doesn't support creating alias records that route traffic to AWS resources other than ELB load balancers. - If you specify a value for ``AWS_ALIAS_DNS_NAME`` , don't specify values for any of the ``AWS_INSTANCE`` attributes. - **AWS_EC2_INSTANCE_ID** - *HTTP namespaces only.* The Amazon EC2 instance ID for the instance. The ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. When creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ , if the ``AWS_EC2_INSTANCE_ID`` attribute is specified, the only other attribute that can be specified is ``AWS_INIT_HEALTH_STATUS`` . After the resource has been created, the ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. - **AWS_INIT_HEALTH_STATUS** - If the service configuration includes ``HealthCheckCustomConfig`` , when creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ you can optionally use ``AWS_INIT_HEALTH_STATUS`` to specify the initial status of the custom health check, ``HEALTHY`` or ``UNHEALTHY`` . If you don't specify a value for ``AWS_INIT_HEALTH_STATUS`` , the initial status is ``HEALTHY`` . This attribute can only be used when creating resources and will not be seen on existing resources. - **AWS_INSTANCE_CNAME** - If the service configuration includes a ``CNAME`` record, the domain name that you want Route 53 to return in response to DNS queries, for example, ``example.com`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``CNAME`` record. - **AWS_INSTANCE_IPV4** - If the service configuration includes an ``A`` record, the IPv4 address that you want Route 53 to return in response to DNS queries, for example, ``192.0.2.44`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``A`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both. - **AWS_INSTANCE_IPV6** - If the service configuration includes an ``AAAA`` record, the IPv6 address that you want Route 53 to return in response to DNS queries, for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``AAAA`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both. - **AWS_INSTANCE_PORT** - If the service includes an ``SRV`` record, the value that you want Route 53 to return for the port. If the service includes ``HealthCheckConfig`` , the port on the endpoint that you want Route 53 to send requests to. This value is required if you specified settings for an ``SRV`` record or a Route 53 health check when you created the service.
        :param service_id: The ID of the service that you want to use for settings for the instance.
        :param instance_id: An identifier that you want to associate with the instance. Note the following:. - If the service that's specified by ``ServiceId`` includes settings for an ``SRV`` record, the value of ``InstanceId`` is automatically included as part of the value for the ``SRV`` record. For more information, see `DnsRecord > Type <https://docs.aws.amazon.com/cloud-map/latest/api/API_DnsRecord.html#cloudmap-Type-DnsRecord-Type>`_ . - You can use this value to update an existing instance. - To register a new instance, you must specify a value that's unique among instances that you register by using the same service. - If you specify an existing ``InstanceId`` and ``ServiceId`` , AWS Cloud Map updates the existing DNS records, if any. If there's also an existing health check, AWS Cloud Map deletes the old health check and creates a new one. .. epigraph:: The health check isn't deleted immediately, so it will still appear for a while if you submit a ``ListHealthChecks`` request, for example. .. epigraph:: Do not include sensitive information in ``InstanceId`` if the namespace is discoverable by public DNS queries and any ``Type`` member of ``DnsRecord`` for the service contains ``SRV`` because the ``InstanceId`` is discoverable by public DNS queries.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc2dd80dc637822332f087219a98eaeba9a57c808c6087345bd115908f85f852)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceProps(
            instance_attributes=instance_attributes,
            service_id=service_id,
            instance_id=instance_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5f5529a591cdc85f4fe487954fc2490c9c49a6874b81c08e6ed85c2675bae5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6ec7f237c5a4deb84df6ec3057ad52dcd2c3db48ee9753218e82e74eb75a3aff)
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
    @jsii.member(jsii_name="instanceAttributes")
    def instance_attributes(self) -> typing.Any:
        '''A string map that contains the following information for the service that you specify in ``ServiceId`` :.

        - The attributes that apply to the records that are defined in the service.
        - For each attribute, the applicable value.

        Supported attribute keys include the following:

        - **AWS_ALIAS_DNS_NAME** - If you want AWS Cloud Map to create a Route 53 alias record that routes traffic to an Elastic Load Balancing load balancer, specify the DNS name that is associated with the load balancer. For information about how to get the DNS name, see `AliasTarget->DNSName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-DNSName>`_ in the *Route 53 API Reference* .

        Note the following:

        - The configuration for the service that is specified by ``ServiceId`` must include settings for an ``A`` record, an ``AAAA`` record, or both.
        - In the service that is specified by ``ServiceId`` , the value of ``RoutingPolicy`` must be ``WEIGHTED`` .
        - If the service that is specified by ``ServiceId`` includes ``HealthCheckConfig`` settings, AWS Cloud Map will create the health check, but it won't associate the health check with the alias record.
        - Auto naming currently doesn't support creating alias records that route traffic to AWS resources other than ELB load balancers.
        - If you specify a value for ``AWS_ALIAS_DNS_NAME`` , don't specify values for any of the ``AWS_INSTANCE`` attributes.
        - **AWS_EC2_INSTANCE_ID** - *HTTP namespaces only.* The Amazon EC2 instance ID for the instance. The ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. When creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ , if the ``AWS_EC2_INSTANCE_ID`` attribute is specified, the only other attribute that can be specified is ``AWS_INIT_HEALTH_STATUS`` . After the resource has been created, the ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address.
        - **AWS_INIT_HEALTH_STATUS** - If the service configuration includes ``HealthCheckCustomConfig`` , when creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ you can optionally use ``AWS_INIT_HEALTH_STATUS`` to specify the initial status of the custom health check, ``HEALTHY`` or ``UNHEALTHY`` . If you don't specify a value for ``AWS_INIT_HEALTH_STATUS`` , the initial status is ``HEALTHY`` . This attribute can only be used when creating resources and will not be seen on existing resources.
        - **AWS_INSTANCE_CNAME** - If the service configuration includes a ``CNAME`` record, the domain name that you want Route 53 to return in response to DNS queries, for example, ``example.com`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``CNAME`` record.

        - **AWS_INSTANCE_IPV4** - If the service configuration includes an ``A`` record, the IPv4 address that you want Route 53 to return in response to DNS queries, for example, ``192.0.2.44`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``A`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both.

        - **AWS_INSTANCE_IPV6** - If the service configuration includes an ``AAAA`` record, the IPv6 address that you want Route 53 to return in response to DNS queries, for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``AAAA`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both.

        - **AWS_INSTANCE_PORT** - If the service includes an ``SRV`` record, the value that you want Route 53 to return for the port.

        If the service includes ``HealthCheckConfig`` , the port on the endpoint that you want Route 53 to send requests to.

        This value is required if you specified settings for an ``SRV`` record or a Route 53 health check when you created the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceattributes
        '''
        return typing.cast(typing.Any, jsii.get(self, "instanceAttributes"))

    @instance_attributes.setter
    def instance_attributes(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2597aea5bf8a8df900153f5d55b760439e30ecc44bf1d802f19796b2ee1ea610)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''The ID of the service that you want to use for settings for the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-serviceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @service_id.setter
    def service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48280bf88ef8c77a1406aeb5ff45c0133556134c24fd6ac63c035ab03c6dabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceId", value)

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''An identifier that you want to associate with the instance. Note the following:.

        - If the service that's specified by ``ServiceId`` includes settings for an ``SRV`` record, the value of ``InstanceId`` is automatically included as part of the value for the ``SRV`` record. For more information, see `DnsRecord > Type <https://docs.aws.amazon.com/cloud-map/latest/api/API_DnsRecord.html#cloudmap-Type-DnsRecord-Type>`_ .
        - You can use this value to update an existing instance.
        - To register a new instance, you must specify a value that's unique among instances that you register by using the same service.
        - If you specify an existing ``InstanceId`` and ``ServiceId`` , AWS Cloud Map updates the existing DNS records, if any. If there's also an existing health check, AWS Cloud Map deletes the old health check and creates a new one.

        .. epigraph::

           The health check isn't deleted immediately, so it will still appear for a while if you submit a ``ListHealthChecks`` request, for example.
        .. epigraph::

           Do not include sensitive information in ``InstanceId`` if the namespace is discoverable by public DNS queries and any ``Type`` member of ``DnsRecord`` for the service contains ``SRV`` because the ``InstanceId`` is discoverable by public DNS queries.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceId"))

    @instance_id.setter
    def instance_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20980649ae5374738eeee56d611f3e1b528a15011a1ac7ed7998acedd1098c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CfnInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "instance_attributes": "instanceAttributes",
        "service_id": "serviceId",
        "instance_id": "instanceId",
    },
)
class CfnInstanceProps:
    def __init__(
        self,
        *,
        instance_attributes: typing.Any,
        service_id: builtins.str,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstance``.

        :param instance_attributes: A string map that contains the following information for the service that you specify in ``ServiceId`` :. - The attributes that apply to the records that are defined in the service. - For each attribute, the applicable value. Supported attribute keys include the following: - **AWS_ALIAS_DNS_NAME** - If you want AWS Cloud Map to create a Route 53 alias record that routes traffic to an Elastic Load Balancing load balancer, specify the DNS name that is associated with the load balancer. For information about how to get the DNS name, see `AliasTarget->DNSName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-DNSName>`_ in the *Route 53 API Reference* . Note the following: - The configuration for the service that is specified by ``ServiceId`` must include settings for an ``A`` record, an ``AAAA`` record, or both. - In the service that is specified by ``ServiceId`` , the value of ``RoutingPolicy`` must be ``WEIGHTED`` . - If the service that is specified by ``ServiceId`` includes ``HealthCheckConfig`` settings, AWS Cloud Map will create the health check, but it won't associate the health check with the alias record. - Auto naming currently doesn't support creating alias records that route traffic to AWS resources other than ELB load balancers. - If you specify a value for ``AWS_ALIAS_DNS_NAME`` , don't specify values for any of the ``AWS_INSTANCE`` attributes. - **AWS_EC2_INSTANCE_ID** - *HTTP namespaces only.* The Amazon EC2 instance ID for the instance. The ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. When creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ , if the ``AWS_EC2_INSTANCE_ID`` attribute is specified, the only other attribute that can be specified is ``AWS_INIT_HEALTH_STATUS`` . After the resource has been created, the ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. - **AWS_INIT_HEALTH_STATUS** - If the service configuration includes ``HealthCheckCustomConfig`` , when creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ you can optionally use ``AWS_INIT_HEALTH_STATUS`` to specify the initial status of the custom health check, ``HEALTHY`` or ``UNHEALTHY`` . If you don't specify a value for ``AWS_INIT_HEALTH_STATUS`` , the initial status is ``HEALTHY`` . This attribute can only be used when creating resources and will not be seen on existing resources. - **AWS_INSTANCE_CNAME** - If the service configuration includes a ``CNAME`` record, the domain name that you want Route 53 to return in response to DNS queries, for example, ``example.com`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``CNAME`` record. - **AWS_INSTANCE_IPV4** - If the service configuration includes an ``A`` record, the IPv4 address that you want Route 53 to return in response to DNS queries, for example, ``192.0.2.44`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``A`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both. - **AWS_INSTANCE_IPV6** - If the service configuration includes an ``AAAA`` record, the IPv6 address that you want Route 53 to return in response to DNS queries, for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` . This value is required if the service specified by ``ServiceId`` includes settings for an ``AAAA`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both. - **AWS_INSTANCE_PORT** - If the service includes an ``SRV`` record, the value that you want Route 53 to return for the port. If the service includes ``HealthCheckConfig`` , the port on the endpoint that you want Route 53 to send requests to. This value is required if you specified settings for an ``SRV`` record or a Route 53 health check when you created the service.
        :param service_id: The ID of the service that you want to use for settings for the instance.
        :param instance_id: An identifier that you want to associate with the instance. Note the following:. - If the service that's specified by ``ServiceId`` includes settings for an ``SRV`` record, the value of ``InstanceId`` is automatically included as part of the value for the ``SRV`` record. For more information, see `DnsRecord > Type <https://docs.aws.amazon.com/cloud-map/latest/api/API_DnsRecord.html#cloudmap-Type-DnsRecord-Type>`_ . - You can use this value to update an existing instance. - To register a new instance, you must specify a value that's unique among instances that you register by using the same service. - If you specify an existing ``InstanceId`` and ``ServiceId`` , AWS Cloud Map updates the existing DNS records, if any. If there's also an existing health check, AWS Cloud Map deletes the old health check and creates a new one. .. epigraph:: The health check isn't deleted immediately, so it will still appear for a while if you submit a ``ListHealthChecks`` request, for example. .. epigraph:: Do not include sensitive information in ``InstanceId`` if the namespace is discoverable by public DNS queries and any ``Type`` member of ``DnsRecord`` for the service contains ``SRV`` because the ``InstanceId`` is discoverable by public DNS queries.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            # instance_attributes: Any
            
            cfn_instance_props = servicediscovery.CfnInstanceProps(
                instance_attributes=instance_attributes,
                service_id="serviceId",
            
                # the properties below are optional
                instance_id="instanceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f66bd527852b58bfda784fbbd343d14bf76e664a0fa0232c509deb73c8ff469a)
            check_type(argname="argument instance_attributes", value=instance_attributes, expected_type=type_hints["instance_attributes"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_attributes": instance_attributes,
            "service_id": service_id,
        }
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def instance_attributes(self) -> typing.Any:
        '''A string map that contains the following information for the service that you specify in ``ServiceId`` :.

        - The attributes that apply to the records that are defined in the service.
        - For each attribute, the applicable value.

        Supported attribute keys include the following:

        - **AWS_ALIAS_DNS_NAME** - If you want AWS Cloud Map to create a Route 53 alias record that routes traffic to an Elastic Load Balancing load balancer, specify the DNS name that is associated with the load balancer. For information about how to get the DNS name, see `AliasTarget->DNSName <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-DNSName>`_ in the *Route 53 API Reference* .

        Note the following:

        - The configuration for the service that is specified by ``ServiceId`` must include settings for an ``A`` record, an ``AAAA`` record, or both.
        - In the service that is specified by ``ServiceId`` , the value of ``RoutingPolicy`` must be ``WEIGHTED`` .
        - If the service that is specified by ``ServiceId`` includes ``HealthCheckConfig`` settings, AWS Cloud Map will create the health check, but it won't associate the health check with the alias record.
        - Auto naming currently doesn't support creating alias records that route traffic to AWS resources other than ELB load balancers.
        - If you specify a value for ``AWS_ALIAS_DNS_NAME`` , don't specify values for any of the ``AWS_INSTANCE`` attributes.
        - **AWS_EC2_INSTANCE_ID** - *HTTP namespaces only.* The Amazon EC2 instance ID for the instance. The ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address. When creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ , if the ``AWS_EC2_INSTANCE_ID`` attribute is specified, the only other attribute that can be specified is ``AWS_INIT_HEALTH_STATUS`` . After the resource has been created, the ``AWS_INSTANCE_IPV4`` attribute contains the primary private IPv4 address.
        - **AWS_INIT_HEALTH_STATUS** - If the service configuration includes ``HealthCheckCustomConfig`` , when creating resources with a type of `AWS::ServiceDiscovery::Instance <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html>`_ you can optionally use ``AWS_INIT_HEALTH_STATUS`` to specify the initial status of the custom health check, ``HEALTHY`` or ``UNHEALTHY`` . If you don't specify a value for ``AWS_INIT_HEALTH_STATUS`` , the initial status is ``HEALTHY`` . This attribute can only be used when creating resources and will not be seen on existing resources.
        - **AWS_INSTANCE_CNAME** - If the service configuration includes a ``CNAME`` record, the domain name that you want Route 53 to return in response to DNS queries, for example, ``example.com`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``CNAME`` record.

        - **AWS_INSTANCE_IPV4** - If the service configuration includes an ``A`` record, the IPv4 address that you want Route 53 to return in response to DNS queries, for example, ``192.0.2.44`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``A`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both.

        - **AWS_INSTANCE_IPV6** - If the service configuration includes an ``AAAA`` record, the IPv6 address that you want Route 53 to return in response to DNS queries, for example, ``2001:0db8:85a3:0000:0000:abcd:0001:2345`` .

        This value is required if the service specified by ``ServiceId`` includes settings for an ``AAAA`` record. If the service includes settings for an ``SRV`` record, you must specify a value for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both.

        - **AWS_INSTANCE_PORT** - If the service includes an ``SRV`` record, the value that you want Route 53 to return for the port.

        If the service includes ``HealthCheckConfig`` , the port on the endpoint that you want Route 53 to send requests to.

        This value is required if you specified settings for an ``SRV`` record or a Route 53 health check when you created the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceattributes
        '''
        result = self._values.get("instance_attributes")
        assert result is not None, "Required property 'instance_attributes' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        '''The ID of the service that you want to use for settings for the instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-serviceid
        '''
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''An identifier that you want to associate with the instance. Note the following:.

        - If the service that's specified by ``ServiceId`` includes settings for an ``SRV`` record, the value of ``InstanceId`` is automatically included as part of the value for the ``SRV`` record. For more information, see `DnsRecord > Type <https://docs.aws.amazon.com/cloud-map/latest/api/API_DnsRecord.html#cloudmap-Type-DnsRecord-Type>`_ .
        - You can use this value to update an existing instance.
        - To register a new instance, you must specify a value that's unique among instances that you register by using the same service.
        - If you specify an existing ``InstanceId`` and ``ServiceId`` , AWS Cloud Map updates the existing DNS records, if any. If there's also an existing health check, AWS Cloud Map deletes the old health check and creates a new one.

        .. epigraph::

           The health check isn't deleted immediately, so it will still appear for a while if you submit a ``ListHealthChecks`` request, for example.
        .. epigraph::

           Do not include sensitive information in ``InstanceId`` if the namespace is discoverable by public DNS queries and any ``Type`` member of ``DnsRecord`` for the service contains ``SRV`` because the ``InstanceId`` is discoverable by public DNS queries.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-instance.html#cfn-servicediscovery-instance-instanceid
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPrivateDnsNamespace(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespace",
):
    '''A CloudFormation ``AWS::ServiceDiscovery::PrivateDnsNamespace``.

    Creates a private namespace based on DNS, which is visible only inside a specified Amazon VPC. The namespace defines your service naming scheme. For example, if you name your namespace ``example.com`` and name your service ``backend`` , the resulting DNS name for the service is ``backend.example.com`` . Service instances that are registered using a private DNS namespace can be discovered using either a ``DiscoverInstances`` request or using DNS. For the current quota on the number of namespaces that you can create using the same AWS account , see `AWS Cloud Map quotas <https://docs.aws.amazon.com/cloud-map/latest/dg/cloud-map-limits.html>`_ in the *AWS Cloud Map Developer Guide* .

    :cloudformationResource: AWS::ServiceDiscovery::PrivateDnsNamespace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        cfn_private_dns_namespace = servicediscovery.CfnPrivateDnsNamespace(self, "MyCfnPrivateDnsNamespace",
            name="name",
            vpc="vpc",
        
            # the properties below are optional
            description="description",
            properties=servicediscovery.CfnPrivateDnsNamespace.PropertiesProperty(
                dns_properties=servicediscovery.CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty(
                    soa=servicediscovery.CfnPrivateDnsNamespace.SOAProperty(
                        ttl=123
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        vpc: builtins.str,
        description: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPrivateDnsNamespace.PropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceDiscovery::PrivateDnsNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name that you want to assign to this namespace. When you create a private DNS namespace, AWS Cloud Map automatically creates an Amazon Route 53 private hosted zone that has the same name as the namespace.
        :param vpc: The ID of the Amazon VPC that you want to associate the namespace with.
        :param description: A description for the namespace.
        :param properties: Properties for the private DNS namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1794382d187fc6030f15b6d87ce7e723479c15363167b200cfa2b0813a9b242e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPrivateDnsNamespaceProps(
            name=name,
            vpc=vpc,
            description=description,
            properties=properties,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06b3a5d1e7e28add33a9c5c817b80bdbcde5add53db88fd6562ce0158e26088)
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
            type_hints = typing.get_type_hints(_typecheckingstub__87c02d4c20283defa1567deaec184b7134d524aa0b192dee99ad16c23af25b5f)
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
        '''The Amazon Resource Name (ARN) of the private namespace.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrHostedZoneId")
    def attr_hosted_zone_id(self) -> builtins.str:
        '''The ID for the Route 53 hosted zone that AWS Cloud Map creates when you create a namespace.

        :cloudformationAttribute: HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the private namespace.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name that you want to assign to this namespace.

        When you create a private DNS namespace, AWS Cloud Map automatically creates an Amazon Route 53 private hosted zone that has the same name as the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c69cb8c4613b4475ff6774ca21118a415444422e0220369b0140e46635cb3b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> builtins.str:
        '''The ID of the Amazon VPC that you want to associate the namespace with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-vpc
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpc"))

    @vpc.setter
    def vpc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25ec3073d6251823d7958711c3fd808c6c90a3e905985ac21679c1f551ab9d63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpc", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38dc8138d7f4d3bbdf045a806a9d0009983b71b2f86a377e71842e210745091b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.PropertiesProperty"]]:
        '''Properties for the private DNS namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-properties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.PropertiesProperty"]], jsii.get(self, "properties"))

    @properties.setter
    def properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.PropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb06930f8a3d10b38e2259b72cf5a901cb5820c36444c752f76d39275e9135d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty",
        jsii_struct_bases=[],
        name_mapping={"soa": "soa"},
    )
    class PrivateDnsPropertiesMutableProperty:
        def __init__(
            self,
            *,
            soa: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPrivateDnsNamespace.SOAProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''DNS properties for the private DNS namespace.

            :param soa: Fields for the Start of Authority (SOA) record for the hosted zone for the private DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-privatednspropertiesmutable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                private_dns_properties_mutable_property = servicediscovery.CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty(
                    soa=servicediscovery.CfnPrivateDnsNamespace.SOAProperty(
                        ttl=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7d9656d93cd4eb5626700402532389d894f3b9f3600d3f6726a17097f802929)
                check_type(argname="argument soa", value=soa, expected_type=type_hints["soa"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if soa is not None:
                self._values["soa"] = soa

        @builtins.property
        def soa(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.SOAProperty"]]:
            '''Fields for the Start of Authority (SOA) record for the hosted zone for the private DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-privatednspropertiesmutable.html#cfn-servicediscovery-privatednsnamespace-privatednspropertiesmutable-soa
            '''
            result = self._values.get("soa")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.SOAProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PrivateDnsPropertiesMutableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespace.PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"dns_properties": "dnsProperties"},
    )
    class PropertiesProperty:
        def __init__(
            self,
            *,
            dns_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Properties for the private DNS namespace.

            :param dns_properties: DNS properties for the private DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                properties_property = servicediscovery.CfnPrivateDnsNamespace.PropertiesProperty(
                    dns_properties=servicediscovery.CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty(
                        soa=servicediscovery.CfnPrivateDnsNamespace.SOAProperty(
                            ttl=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__22c92d0f581d14b979a9eba84f458e99b8f7d047b3b0cf9e62ce1528c7973a0f)
                check_type(argname="argument dns_properties", value=dns_properties, expected_type=type_hints["dns_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_properties is not None:
                self._values["dns_properties"] = dns_properties

        @builtins.property
        def dns_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty"]]:
            '''DNS properties for the private DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-properties.html#cfn-servicediscovery-privatednsnamespace-properties-dnsproperties
            '''
            result = self._values.get("dns_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespace.SOAProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl"},
    )
    class SOAProperty:
        def __init__(self, *, ttl: typing.Optional[jsii.Number] = None) -> None:
            '''Start of Authority (SOA) properties for a public or private DNS namespace.

            :param ttl: The time to live (TTL) for purposes of negative caching.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-soa.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                s_oAProperty = servicediscovery.CfnPrivateDnsNamespace.SOAProperty(
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2424720246f242b6ebc693ab54e03c6869388ea9b7a560bdb3a8ac5480976ee)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The time to live (TTL) for purposes of negative caching.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-privatednsnamespace-soa.html#cfn-servicediscovery-privatednsnamespace-soa-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SOAProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CfnPrivateDnsNamespaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "vpc": "vpc",
        "description": "description",
        "properties": "properties",
        "tags": "tags",
    },
)
class CfnPrivateDnsNamespaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        vpc: builtins.str,
        description: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPrivateDnsNamespace.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPrivateDnsNamespace``.

        :param name: The name that you want to assign to this namespace. When you create a private DNS namespace, AWS Cloud Map automatically creates an Amazon Route 53 private hosted zone that has the same name as the namespace.
        :param vpc: The ID of the Amazon VPC that you want to associate the namespace with.
        :param description: A description for the namespace.
        :param properties: Properties for the private DNS namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            cfn_private_dns_namespace_props = servicediscovery.CfnPrivateDnsNamespaceProps(
                name="name",
                vpc="vpc",
            
                # the properties below are optional
                description="description",
                properties=servicediscovery.CfnPrivateDnsNamespace.PropertiesProperty(
                    dns_properties=servicediscovery.CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty(
                        soa=servicediscovery.CfnPrivateDnsNamespace.SOAProperty(
                            ttl=123
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b539a93a0f92851fc3dc947e81944261d1176424ddca25083d29c1385381d4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vpc": vpc,
        }
        if description is not None:
            self._values["description"] = description
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name that you want to assign to this namespace.

        When you create a private DNS namespace, AWS Cloud Map automatically creates an Amazon Route 53 private hosted zone that has the same name as the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc(self) -> builtins.str:
        '''The ID of the Amazon VPC that you want to associate the namespace with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-vpc
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPrivateDnsNamespace.PropertiesProperty]]:
        '''Properties for the private DNS namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPrivateDnsNamespace.PropertiesProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-privatednsnamespace.html#cfn-servicediscovery-privatednsnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPrivateDnsNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPublicDnsNamespace(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespace",
):
    '''A CloudFormation ``AWS::ServiceDiscovery::PublicDnsNamespace``.

    Creates a public namespace based on DNS, which is visible on the internet. The namespace defines your service naming scheme. For example, if you name your namespace ``example.com`` and name your service ``backend`` , the resulting DNS name for the service is ``backend.example.com`` . You can discover instances that were registered with a public DNS namespace by using either a ``DiscoverInstances`` request or using DNS. For the current quota on the number of namespaces that you can create using the same AWS account , see `AWS Cloud Map quotas <https://docs.aws.amazon.com/cloud-map/latest/dg/cloud-map-limits.html>`_ in the *AWS Cloud Map Developer Guide* .
    .. epigraph::

       The ``CreatePublicDnsNamespace`` API operation is not supported in the AWS GovCloud (US) Regions.

    :cloudformationResource: AWS::ServiceDiscovery::PublicDnsNamespace
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        cfn_public_dns_namespace = servicediscovery.CfnPublicDnsNamespace(self, "MyCfnPublicDnsNamespace",
            name="name",
        
            # the properties below are optional
            description="description",
            properties=servicediscovery.CfnPublicDnsNamespace.PropertiesProperty(
                dns_properties=servicediscovery.CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty(
                    soa=servicediscovery.CfnPublicDnsNamespace.SOAProperty(
                        ttl=123
                    )
                )
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPublicDnsNamespace.PropertiesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceDiscovery::PublicDnsNamespace``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name that you want to assign to this namespace. .. epigraph:: Do not include sensitive information in the name. The name is publicly available using DNS queries.
        :param description: A description for the namespace.
        :param properties: Properties for the public DNS namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2343ad30b0962c71e204183b106a7663df321812f54e73f6173c3d14cf29ab4e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPublicDnsNamespaceProps(
            name=name, description=description, properties=properties, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dc84819f5515601e96cb9e7575ee9135fc704506f23eeb67af484f0d953c8d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd09b4983469e0bdcd04e47f63e2beacbfe81efadc47514cf8c179a8ce64bf1c)
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
        '''The Amazon Resource Name (ARN) of the public namespace.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrHostedZoneId")
    def attr_hosted_zone_id(self) -> builtins.str:
        '''The ID for the Route 53 hosted zone that AWS Cloud Map creates when you create a namespace.

        :cloudformationAttribute: HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the public namespace.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name that you want to assign to this namespace.

        .. epigraph::

           Do not include sensitive information in the name. The name is publicly available using DNS queries.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba834a9219d132cfbc9fb02c446a8faab31df58be2b088d1626957058fa3cca6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0672e6797c215b8bfca48131cf43eba5427bdb4700e96c22da7ee25d3de8d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="properties")
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.PropertiesProperty"]]:
        '''Properties for the public DNS namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-properties
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.PropertiesProperty"]], jsii.get(self, "properties"))

    @properties.setter
    def properties(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.PropertiesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f361c2dac1ca7d13c6852778184b6b4a1f1939293b89c32ac3a20462c480da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "properties", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespace.PropertiesProperty",
        jsii_struct_bases=[],
        name_mapping={"dns_properties": "dnsProperties"},
    )
    class PropertiesProperty:
        def __init__(
            self,
            *,
            dns_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Properties for the public DNS namespace.

            :param dns_properties: DNS properties for the public DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-properties.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                properties_property = servicediscovery.CfnPublicDnsNamespace.PropertiesProperty(
                    dns_properties=servicediscovery.CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty(
                        soa=servicediscovery.CfnPublicDnsNamespace.SOAProperty(
                            ttl=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11c5d7144b029acde30dcd0c119e536322e1a812164b9b5c1ff6ddfcab19107b)
                check_type(argname="argument dns_properties", value=dns_properties, expected_type=type_hints["dns_properties"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dns_properties is not None:
                self._values["dns_properties"] = dns_properties

        @builtins.property
        def dns_properties(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty"]]:
            '''DNS properties for the public DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-properties.html#cfn-servicediscovery-publicdnsnamespace-properties-dnsproperties
            '''
            result = self._values.get("dns_properties")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PropertiesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty",
        jsii_struct_bases=[],
        name_mapping={"soa": "soa"},
    )
    class PublicDnsPropertiesMutableProperty:
        def __init__(
            self,
            *,
            soa: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPublicDnsNamespace.SOAProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''DNS properties for the public DNS namespace.

            :param soa: Start of Authority (SOA) record for the hosted zone for the public DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-publicdnspropertiesmutable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                public_dns_properties_mutable_property = servicediscovery.CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty(
                    soa=servicediscovery.CfnPublicDnsNamespace.SOAProperty(
                        ttl=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3a32b20b6499fe7aa98b60def15629e0fbc0a1192890c1c9f9c6b26b1e106a88)
                check_type(argname="argument soa", value=soa, expected_type=type_hints["soa"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if soa is not None:
                self._values["soa"] = soa

        @builtins.property
        def soa(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.SOAProperty"]]:
            '''Start of Authority (SOA) record for the hosted zone for the public DNS namespace.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-publicdnspropertiesmutable.html#cfn-servicediscovery-publicdnsnamespace-publicdnspropertiesmutable-soa
            '''
            result = self._values.get("soa")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPublicDnsNamespace.SOAProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublicDnsPropertiesMutableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespace.SOAProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl"},
    )
    class SOAProperty:
        def __init__(self, *, ttl: typing.Optional[jsii.Number] = None) -> None:
            '''Start of Authority (SOA) properties for a public or private DNS namespace.

            :param ttl: The time to live (TTL) for purposes of negative caching.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-soa.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                s_oAProperty = servicediscovery.CfnPublicDnsNamespace.SOAProperty(
                    ttl=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__21f895639c4c1a78d206dfe04b5d8570fda7e7638dc180a39aad413173b005c8)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ttl is not None:
                self._values["ttl"] = ttl

        @builtins.property
        def ttl(self) -> typing.Optional[jsii.Number]:
            '''The time to live (TTL) for purposes of negative caching.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-publicdnsnamespace-soa.html#cfn-servicediscovery-publicdnsnamespace-soa-ttl
            '''
            result = self._values.get("ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SOAProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CfnPublicDnsNamespaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "description": "description",
        "properties": "properties",
        "tags": "tags",
    },
)
class CfnPublicDnsNamespaceProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPublicDnsNamespace.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPublicDnsNamespace``.

        :param name: The name that you want to assign to this namespace. .. epigraph:: Do not include sensitive information in the name. The name is publicly available using DNS queries.
        :param description: A description for the namespace.
        :param properties: Properties for the public DNS namespace.
        :param tags: The tags for the namespace. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            cfn_public_dns_namespace_props = servicediscovery.CfnPublicDnsNamespaceProps(
                name="name",
            
                # the properties below are optional
                description="description",
                properties=servicediscovery.CfnPublicDnsNamespace.PropertiesProperty(
                    dns_properties=servicediscovery.CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty(
                        soa=servicediscovery.CfnPublicDnsNamespace.SOAProperty(
                            ttl=123
                        )
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__642a04150e405d0273f65a0aae73705b0e8fff3061867b01bc4b665b8672bdb8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if properties is not None:
            self._values["properties"] = properties
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name that you want to assign to this namespace.

        .. epigraph::

           Do not include sensitive information in the name. The name is publicly available using DNS queries.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPublicDnsNamespace.PropertiesProperty]]:
        '''Properties for the public DNS namespace.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-properties
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPublicDnsNamespace.PropertiesProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the namespace.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-publicdnsnamespace.html#cfn-servicediscovery-publicdnsnamespace-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPublicDnsNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnService(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.CfnService",
):
    '''A CloudFormation ``AWS::ServiceDiscovery::Service``.

    A complex type that contains information about a service, which defines the configuration of the following entities:

    - For public and private DNS namespaces, one of the following combinations of DNS records in Amazon Route 53:
    - A
    - AAAA
    - A and AAAA
    - SRV
    - CNAME
    - Optionally, a health check

    :cloudformationResource: AWS::ServiceDiscovery::Service
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        cfn_service = servicediscovery.CfnService(self, "MyCfnService",
            description="description",
            dns_config=servicediscovery.CfnService.DnsConfigProperty(
                dns_records=[servicediscovery.CfnService.DnsRecordProperty(
                    ttl=123,
                    type="type"
                )],
        
                # the properties below are optional
                namespace_id="namespaceId",
                routing_policy="routingPolicy"
            ),
            health_check_config=servicediscovery.CfnService.HealthCheckConfigProperty(
                type="type",
        
                # the properties below are optional
                failure_threshold=123,
                resource_path="resourcePath"
            ),
            health_check_custom_config=servicediscovery.CfnService.HealthCheckCustomConfigProperty(
                failure_threshold=123
            ),
            name="name",
            namespace_id="namespaceId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.DnsConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_custom_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.HealthCheckCustomConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ServiceDiscovery::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: The description of the service.
        :param dns_config: A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance. .. epigraph:: The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .
        :param health_check_config: *Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` . For information about the charges for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .
        :param health_check_custom_config: A complex type that contains information about an optional custom health check. .. epigraph:: If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.
        :param name: The name of the service.
        :param namespace_id: The ID of the namespace that was used to create the service. .. epigraph:: You must specify a value for ``NamespaceId`` either for the service properties or for `DnsConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html>`_ . Don't specify a value in both places.
        :param tags: The tags for the service. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param type: If present, specifies that the service instances are only discoverable using the ``DiscoverInstances`` API operation. No DNS records is registered for the service instances. The only valid value is ``HTTP`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db652afe83160664aba67161cefe1937d1f0688e65436994223c61ee5cf6600b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceProps(
            description=description,
            dns_config=dns_config,
            health_check_config=health_check_config,
            health_check_custom_config=health_check_custom_config,
            name=name,
            namespace_id=namespace_id,
            tags=tags,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbed11ee98645877be78be36680db1292df4aa7de386942f466c61affc413d8e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30578c47261b37f8529be14614a05b7155b0bf5a533b6abf117a3140fe414c39)
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
        '''The Amazon Resource Name (ARN) of the service.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the service.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name that you assigned to the service.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the service.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f7a430fb8cfb8860ec3a1700d83427b670914d8f3f61d52a86fd75f4fa53a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="dnsConfig")
    def dns_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsConfigProperty"]]:
        '''A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

        .. epigraph::

           The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-dnsconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsConfigProperty"]], jsii.get(self, "dnsConfig"))

    @dns_config.setter
    def dns_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d8aaa5b9c56a45c8da24bb9bc8e0fc27dbb158b9c58428edb645221e5ae3bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsConfig", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckConfig")
    def health_check_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckConfigProperty"]]:
        '''*Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` .

        For information about the charges for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckConfigProperty"]], jsii.get(self, "healthCheckConfig"))

    @health_check_config.setter
    def health_check_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__908c71ea29ec1d8d74a898e932507b91f38c04d0373e1069d485541a626c39ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckConfig", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckCustomConfig")
    def health_check_custom_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckCustomConfigProperty"]]:
        '''A complex type that contains information about an optional custom health check.

        .. epigraph::

           If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckcustomconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckCustomConfigProperty"]], jsii.get(self, "healthCheckCustomConfig"))

    @health_check_custom_config.setter
    def health_check_custom_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.HealthCheckCustomConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0507e4b3b026b952ba34fe6f767d6886b85297e1fdb4ef2e16a03b0ca04161bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckCustomConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e6f59696f7c161ca2aba72658ac73d1e276d8d69a0d19edf2916a915e0795bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the namespace that was used to create the service.

        .. epigraph::

           You must specify a value for ``NamespaceId`` either for the service properties or for `DnsConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html>`_ . Don't specify a value in both places.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-namespaceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceId"))

    @namespace_id.setter
    def namespace_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8ac8383f66ffda9394b914e35b199e14c87758c42838304dc2a0523976d0f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''If present, specifies that the service instances are only discoverable using the ``DiscoverInstances`` API operation.

        No DNS records is registered for the service instances. The only valid value is ``HTTP`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__675d00478c3ea444c1241d56f1a1aff667e5e8bcf41ea08a73c95cbdfa2ed1b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnService.DnsConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dns_records": "dnsRecords",
            "namespace_id": "namespaceId",
            "routing_policy": "routingPolicy",
        },
    )
    class DnsConfigProperty:
        def __init__(
            self,
            *,
            dns_records: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.DnsRecordProperty", typing.Dict[builtins.str, typing.Any]]]]],
            namespace_id: typing.Optional[builtins.str] = None,
            routing_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A complex type that contains information about the Amazon Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

            .. epigraph::

               The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .

            :param dns_records: An array that contains one ``DnsRecord`` object for each Route 53 DNS record that you want AWS Cloud Map to create when you register an instance.
            :param namespace_id: The ID of the namespace to use for DNS configuration. .. epigraph:: You must specify a value for ``NamespaceId`` either for ``DnsConfig`` or for the `service properties <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html>`_ . Don't specify a value in both places.
            :param routing_policy: The routing policy that you want to apply to all Route 53 DNS records that AWS Cloud Map creates when you register an instance and specify this service. .. epigraph:: If you want to use this service to register instances that create alias records, specify ``WEIGHTED`` for the routing policy. You can specify the following values: - **MULTIVALUE** - If you define a health check for the service and the health check is healthy, Route 53 returns the applicable value for up to eight instances. For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with IP addresses for up to eight healthy instances. If fewer than eight instances are healthy, Route 53 responds to every DNS query with the IP addresses for all of the healthy instances. If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the values for up to eight instances. For more information about the multivalue routing policy, see `Multivalue Answer Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-multivalue>`_ in the *Route 53 Developer Guide* . - **WEIGHTED** - Route 53 returns the applicable value from one randomly selected instance from among the instances that you registered using the same service. Currently, all records have the same weight, so you can't route more or less traffic to any instances. For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with the IP address for one randomly selected instance from among the healthy instances. If no instances are healthy, Route 53 responds to DNS queries as if all of the instances were healthy. If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the applicable value for one randomly selected instance. For more information about the weighted routing policy, see `Weighted Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-weighted>`_ in the *Route 53 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                dns_config_property = servicediscovery.CfnService.DnsConfigProperty(
                    dns_records=[servicediscovery.CfnService.DnsRecordProperty(
                        ttl=123,
                        type="type"
                    )],
                
                    # the properties below are optional
                    namespace_id="namespaceId",
                    routing_policy="routingPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d76be492073b8754207624aba64c9346c089a9b0b402790859a2d8ca85ed618)
                check_type(argname="argument dns_records", value=dns_records, expected_type=type_hints["dns_records"])
                check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
                check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dns_records": dns_records,
            }
            if namespace_id is not None:
                self._values["namespace_id"] = namespace_id
            if routing_policy is not None:
                self._values["routing_policy"] = routing_policy

        @builtins.property
        def dns_records(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsRecordProperty"]]]:
            '''An array that contains one ``DnsRecord`` object for each Route 53 DNS record that you want AWS Cloud Map to create when you register an instance.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-dnsrecords
            '''
            result = self._values.get("dns_records")
            assert result is not None, "Required property 'dns_records' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsRecordProperty"]]], result)

        @builtins.property
        def namespace_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the namespace to use for DNS configuration.

            .. epigraph::

               You must specify a value for ``NamespaceId`` either for ``DnsConfig`` or for the `service properties <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html>`_ . Don't specify a value in both places.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-namespaceid
            '''
            result = self._values.get("namespace_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def routing_policy(self) -> typing.Optional[builtins.str]:
            '''The routing policy that you want to apply to all Route 53 DNS records that AWS Cloud Map creates when you register an instance and specify this service.

            .. epigraph::

               If you want to use this service to register instances that create alias records, specify ``WEIGHTED`` for the routing policy.

            You can specify the following values:

            - **MULTIVALUE** - If you define a health check for the service and the health check is healthy, Route 53 returns the applicable value for up to eight instances.

            For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with IP addresses for up to eight healthy instances. If fewer than eight instances are healthy, Route 53 responds to every DNS query with the IP addresses for all of the healthy instances.

            If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the values for up to eight instances.

            For more information about the multivalue routing policy, see `Multivalue Answer Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-multivalue>`_ in the *Route 53 Developer Guide* .

            - **WEIGHTED** - Route 53 returns the applicable value from one randomly selected instance from among the instances that you registered using the same service. Currently, all records have the same weight, so you can't route more or less traffic to any instances.

            For example, suppose that the service includes configurations for one ``A`` record and a health check. You use the service to register 10 instances. Route 53 responds to DNS queries with the IP address for one randomly selected instance from among the healthy instances. If no instances are healthy, Route 53 responds to DNS queries as if all of the instances were healthy.

            If you don't define a health check for the service, Route 53 assumes that all instances are healthy and returns the applicable value for one randomly selected instance.

            For more information about the weighted routing policy, see `Weighted Routing <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-policy.html#routing-policy-weighted>`_ in the *Route 53 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html#cfn-servicediscovery-service-dnsconfig-routingpolicy
            '''
            result = self._values.get("routing_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnService.DnsRecordProperty",
        jsii_struct_bases=[],
        name_mapping={"ttl": "ttl", "type": "type"},
    )
    class DnsRecordProperty:
        def __init__(self, *, ttl: jsii.Number, type: builtins.str) -> None:
            '''A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

            :param ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. .. epigraph:: Alias records don't include a TTL because Route 53 uses the TTL for the AWS resource that an alias record routes traffic to. If you include the ``AWS_ALIAS_DNS_NAME`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request, the ``TTL`` value is ignored. Always specify a TTL for the service; you can use a service to register instances that create either alias or non-alias records.
            :param type: The type of the resource, which indicates the type of value that Route 53 returns in response to DNS queries. You can specify values for ``Type`` in the following combinations: - ``A`` - ``AAAA`` - ``A`` and ``AAAA`` - ``SRV`` - ``CNAME`` If you want AWS Cloud Map to create a Route 53 alias record when you register an instance, specify ``A`` or ``AAAA`` for ``Type`` . You specify other settings, such as the IP address for ``A`` and ``AAAA`` records, when you register an instance. For more information, see `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ . The following values are supported: - **A** - Route 53 returns the IP address of the resource in IPv4 format, such as 192.0.2.44. - **AAAA** - Route 53 returns the IP address of the resource in IPv6 format, such as 2001:0db8:85a3:0000:0000:abcd:0001:2345. - **CNAME** - Route 53 returns the domain name of the resource, such as www.example.com. Note the following: - You specify the domain name that you want to route traffic to when you register an instance. For more information, see `Attributes <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html#cloudmap-RegisterInstance-request-Attributes>`_ in the topic `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ . - You must specify ``WEIGHTED`` for the value of ``RoutingPolicy`` . - You can't specify both ``CNAME`` for ``Type`` and settings for ``HealthCheckConfig`` . If you do, the request will fail with an ``InvalidInput`` error. - **SRV** - Route 53 returns the value for an ``SRV`` record. The value for an ``SRV`` record uses the following values: ``priority weight port service-hostname`` Note the following about the values: - The values of ``priority`` and ``weight`` are both set to ``1`` and can't be changed. - The value of ``port`` comes from the value that you specify for the ``AWS_INSTANCE_PORT`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request. - The value of ``service-hostname`` is a concatenation of the following values: - The value that you specify for ``InstanceId`` when you register an instance. - The name of the service. - The name of the namespace. For example, if the value of ``InstanceId`` is ``test`` , the name of the service is ``backend`` , and the name of the namespace is ``example.com`` , the value of ``service-hostname`` is: ``test.backend.example.com`` If you specify settings for an ``SRV`` record and if you specify values for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both in the ``RegisterInstance`` request, AWS Cloud Map automatically creates ``A`` and/or ``AAAA`` records that have the same name as the value of ``service-hostname`` in the ``SRV`` record. You can ignore these records.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                dns_record_property = servicediscovery.CfnService.DnsRecordProperty(
                    ttl=123,
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__408ede9864d2517cf4a259e330374b6d9189a768df982c51843a57f64ca034d5)
                check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "ttl": ttl,
                "type": type,
            }

        @builtins.property
        def ttl(self) -> jsii.Number:
            '''The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record.

            .. epigraph::

               Alias records don't include a TTL because Route 53 uses the TTL for the AWS resource that an alias record routes traffic to. If you include the ``AWS_ALIAS_DNS_NAME`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request, the ``TTL`` value is ignored. Always specify a TTL for the service; you can use a service to register instances that create either alias or non-alias records.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html#cfn-servicediscovery-service-dnsrecord-ttl
            '''
            result = self._values.get("ttl")
            assert result is not None, "Required property 'ttl' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of the resource, which indicates the type of value that Route 53 returns in response to DNS queries.

            You can specify values for ``Type`` in the following combinations:

            - ``A``
            - ``AAAA``
            - ``A`` and ``AAAA``
            - ``SRV``
            - ``CNAME``

            If you want AWS Cloud Map to create a Route 53 alias record when you register an instance, specify ``A`` or ``AAAA`` for ``Type`` .

            You specify other settings, such as the IP address for ``A`` and ``AAAA`` records, when you register an instance. For more information, see `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ .

            The following values are supported:

            - **A** - Route 53 returns the IP address of the resource in IPv4 format, such as 192.0.2.44.
            - **AAAA** - Route 53 returns the IP address of the resource in IPv6 format, such as 2001:0db8:85a3:0000:0000:abcd:0001:2345.
            - **CNAME** - Route 53 returns the domain name of the resource, such as www.example.com. Note the following:
            - You specify the domain name that you want to route traffic to when you register an instance. For more information, see `Attributes <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html#cloudmap-RegisterInstance-request-Attributes>`_ in the topic `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ .
            - You must specify ``WEIGHTED`` for the value of ``RoutingPolicy`` .
            - You can't specify both ``CNAME`` for ``Type`` and settings for ``HealthCheckConfig`` . If you do, the request will fail with an ``InvalidInput`` error.
            - **SRV** - Route 53 returns the value for an ``SRV`` record. The value for an ``SRV`` record uses the following values:

            ``priority weight port service-hostname``

            Note the following about the values:

            - The values of ``priority`` and ``weight`` are both set to ``1`` and can't be changed.
            - The value of ``port`` comes from the value that you specify for the ``AWS_INSTANCE_PORT`` attribute when you submit a `RegisterInstance <https://docs.aws.amazon.com/cloud-map/latest/api/API_RegisterInstance.html>`_ request.
            - The value of ``service-hostname`` is a concatenation of the following values:
            - The value that you specify for ``InstanceId`` when you register an instance.
            - The name of the service.
            - The name of the namespace.

            For example, if the value of ``InstanceId`` is ``test`` , the name of the service is ``backend`` , and the name of the namespace is ``example.com`` , the value of ``service-hostname`` is:

            ``test.backend.example.com``

            If you specify settings for an ``SRV`` record and if you specify values for ``AWS_INSTANCE_IPV4`` , ``AWS_INSTANCE_IPV6`` , or both in the ``RegisterInstance`` request, AWS Cloud Map automatically creates ``A`` and/or ``AAAA`` records that have the same name as the value of ``service-hostname`` in the ``SRV`` record. You can ignore these records.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsrecord.html#cfn-servicediscovery-service-dnsrecord-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsRecordProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnService.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "failure_threshold": "failureThreshold",
            "resource_path": "resourcePath",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            failure_threshold: typing.Optional[jsii.Number] = None,
            resource_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''*Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` .

            .. epigraph::

               If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

            Health checks are basic Route 53 health checks that monitor an AWS endpoint. For information about pricing for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

            Note the following about configuring health checks.

            - **A and AAAA records** - If ``DnsConfig`` includes configurations for both ``A`` and ``AAAA`` records, AWS Cloud Map creates a health check that uses the IPv4 address to check the health of the resource. If the endpoint tthat's specified by the IPv4 address is unhealthy, Route 53 considers both the ``A`` and ``AAAA`` records to be unhealthy.
            - **CNAME records** - You can't specify settings for ``HealthCheckConfig`` when the ``DNSConfig`` includes ``CNAME`` for the value of ``Type`` . If you do, the ``CreateService`` request will fail with an ``InvalidInput`` error.
            - **Request interval** - A Route 53 health checker in each health-checking AWS Region sends a health check request to an endpoint every 30 seconds. On average, your endpoint receives a health check request about every two seconds. However, health checkers don't coordinate with one another. Therefore, you might sometimes see several requests in one second that's followed by a few seconds with no health checks at all.
            - **Health checking regions** - Health checkers perform checks from all Route 53 health-checking Regions. For a list of the current Regions, see `Regions <https://docs.aws.amazon.com/Route53/latest/APIReference/API_HealthCheckConfig.html#Route53-Type-HealthCheckConfig-Regions>`_ .
            - **Alias records** - When you register an instance, if you include the ``AWS_ALIAS_DNS_NAME`` attribute, AWS Cloud Map creates a Route 53 alias record. Note the following:
            - Route 53 automatically sets ``EvaluateTargetHealth`` to true for alias records. When ``EvaluateTargetHealth`` is true, the alias record inherits the health of the referenced AWS resource. such as an ELB load balancer. For more information, see `EvaluateTargetHealth <https://docs.aws.amazon.com/Route53/latest/APIReference/API_AliasTarget.html#Route53-Type-AliasTarget-EvaluateTargetHealth>`_ .
            - If you include ``HealthCheckConfig`` and then use the service to register an instance that creates an alias record, Route 53 doesn't create the health check.
            - **Charges for health checks** - Health checks are basic Route 53 health checks that monitor an AWS endpoint. For information about pricing for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

            :param type: The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. .. epigraph:: You can't change the value of ``Type`` after you create a health check. You can create the following types of health checks: - *HTTP* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400. - *HTTPS* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400. .. epigraph:: If you specify HTTPS for the value of ``Type`` , the endpoint must support TLS v1.0 or later. - *TCP* : Route 53 tries to establish a TCP connection. If you specify ``TCP`` for ``Type`` , don't specify a value for ``ResourcePath`` . For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .
            :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or the other way around. For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .
            :param resource_path: The path that you want Route 53 to request when performing health checks. The path can be any value that your endpoint returns an HTTP status code of a 2xx or 3xx format for when the endpoint is healthy. An example file is ``/docs/route53-health-check.html`` . Route 53 automatically adds the DNS name for the service. If you don't specify a value for ``ResourcePath`` , the default value is ``/`` . If you specify ``TCP`` for ``Type`` , you must *not* specify a value for ``ResourcePath`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                health_check_config_property = servicediscovery.CfnService.HealthCheckConfigProperty(
                    type="type",
                
                    # the properties below are optional
                    failure_threshold=123,
                    resource_path="resourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b59eb50c9f8bf3b49765ad199e1f6a9813964555c1550233e4808bb3a070570e)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
                check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if failure_threshold is not None:
                self._values["failure_threshold"] = failure_threshold
            if resource_path is not None:
                self._values["resource_path"] = resource_path

        @builtins.property
        def type(self) -> builtins.str:
            '''The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy.

            .. epigraph::

               You can't change the value of ``Type`` after you create a health check.

            You can create the following types of health checks:

            - *HTTP* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTP request and waits for an HTTP status code of 200 or greater and less than 400.
            - *HTTPS* : Route 53 tries to establish a TCP connection. If successful, Route 53 submits an HTTPS request and waits for an HTTP status code of 200 or greater and less than 400.

            .. epigraph::

               If you specify HTTPS for the value of ``Type`` , the endpoint must support TLS v1.0 or later.

            - *TCP* : Route 53 tries to establish a TCP connection.

            If you specify ``TCP`` for ``Type`` , don't specify a value for ``ResourcePath`` .

            For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or the other way around.

            For more information, see `How Route 53 Determines Whether an Endpoint Is Healthy <https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/dns-failover-determining-health-of-endpoints.html>`_ in the *Route 53 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-failurethreshold
            '''
            result = self._values.get("failure_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def resource_path(self) -> typing.Optional[builtins.str]:
            '''The path that you want Route 53 to request when performing health checks.

            The path can be any value that your endpoint returns an HTTP status code of a 2xx or 3xx format for when the endpoint is healthy. An example file is ``/docs/route53-health-check.html`` . Route 53 automatically adds the DNS name for the service. If you don't specify a value for ``ResourcePath`` , the default value is ``/`` .

            If you specify ``TCP`` for ``Type`` , you must *not* specify a value for ``ResourcePath`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckconfig.html#cfn-servicediscovery-service-healthcheckconfig-resourcepath
            '''
            result = self._values.get("resource_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-servicediscovery.CfnService.HealthCheckCustomConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"failure_threshold": "failureThreshold"},
    )
    class HealthCheckCustomConfigProperty:
        def __init__(
            self,
            *,
            failure_threshold: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A complex type that contains information about an optional custom health check.

            A custom health check, which requires that you use a third-party health checker to evaluate the health of your resources, is useful in the following circumstances:

            - You can't use a health check that's defined by ``HealthCheckConfig`` because the resource isn't available over the internet. For example, you can use a custom health check when the instance is in an Amazon VPC. (To check the health of resources in a VPC, the health checker must also be in the VPC.)
            - You want to use a third-party health checker regardless of where your resources are located.

            .. epigraph::

               If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

            To change the status of a custom health check, submit an ``UpdateInstanceCustomHealthStatus`` request. AWS Cloud Map doesn't monitor the status of the resource, it just keeps a record of the status specified in the most recent ``UpdateInstanceCustomHealthStatus`` request.

            Here's how custom health checks work:

            - You create a service.
            - You register an instance.
            - You configure a third-party health checker to monitor the resource that's associated with the new instance.

            .. epigraph::

               AWS Cloud Map doesn't check the health of the resource directly.

            - The third-party health-checker determines that the resource is unhealthy and notifies your application.
            - Your application submits an ``UpdateInstanceCustomHealthStatus`` request.
            - AWS Cloud Map waits for 30 seconds.
            - If another ``UpdateInstanceCustomHealthStatus`` request doesn't arrive during that time to change the status back to healthy, AWS Cloud Map stops routing traffic to the resource.

            :param failure_threshold: .. epigraph:: This parameter is no longer supported and is always set to 1. AWS Cloud Map waits for approximately 30 seconds after receiving an ``UpdateInstanceCustomHealthStatus`` request before changing the status of the service instance. The number of 30-second intervals that you want AWS Cloud Map to wait after receiving an ``UpdateInstanceCustomHealthStatus`` request before it changes the health status of a service instance. Sending a second or subsequent ``UpdateInstanceCustomHealthStatus`` request with the same value before 30 seconds has passed doesn't accelerate the change. AWS Cloud Map still waits ``30`` seconds after the first request to make the change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckcustomconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_servicediscovery as servicediscovery
                
                health_check_custom_config_property = servicediscovery.CfnService.HealthCheckCustomConfigProperty(
                    failure_threshold=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__468be5abe9af45767370eb3133ab632a9add264b8fed770fdd95186a5030b62c)
                check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failure_threshold is not None:
                self._values["failure_threshold"] = failure_threshold

        @builtins.property
        def failure_threshold(self) -> typing.Optional[jsii.Number]:
            '''.. epigraph::

   This parameter is no longer supported and is always set to 1.

            AWS Cloud Map waits for approximately 30 seconds after receiving an ``UpdateInstanceCustomHealthStatus`` request before changing the status of the service instance.

            The number of 30-second intervals that you want AWS Cloud Map to wait after receiving an ``UpdateInstanceCustomHealthStatus`` request before it changes the health status of a service instance.

            Sending a second or subsequent ``UpdateInstanceCustomHealthStatus`` request with the same value before 30 seconds has passed doesn't accelerate the change. AWS Cloud Map still waits ``30`` seconds after the first request to make the change.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-healthcheckcustomconfig.html#cfn-servicediscovery-service-healthcheckcustomconfig-failurethreshold
            '''
            result = self._values.get("failure_threshold")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckCustomConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "dns_config": "dnsConfig",
        "health_check_config": "healthCheckConfig",
        "health_check_custom_config": "healthCheckCustomConfig",
        "name": "name",
        "namespace_id": "namespaceId",
        "tags": "tags",
        "type": "type",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        dns_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        health_check_custom_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckCustomConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        namespace_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnService``.

        :param description: The description of the service.
        :param dns_config: A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance. .. epigraph:: The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .
        :param health_check_config: *Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` . For information about the charges for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .
        :param health_check_custom_config: A complex type that contains information about an optional custom health check. .. epigraph:: If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.
        :param name: The name of the service.
        :param namespace_id: The ID of the namespace that was used to create the service. .. epigraph:: You must specify a value for ``NamespaceId`` either for the service properties or for `DnsConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html>`_ . Don't specify a value in both places.
        :param tags: The tags for the service. Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.
        :param type: If present, specifies that the service instances are only discoverable using the ``DiscoverInstances`` API operation. No DNS records is registered for the service instances. The only valid value is ``HTTP`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            cfn_service_props = servicediscovery.CfnServiceProps(
                description="description",
                dns_config=servicediscovery.CfnService.DnsConfigProperty(
                    dns_records=[servicediscovery.CfnService.DnsRecordProperty(
                        ttl=123,
                        type="type"
                    )],
            
                    # the properties below are optional
                    namespace_id="namespaceId",
                    routing_policy="routingPolicy"
                ),
                health_check_config=servicediscovery.CfnService.HealthCheckConfigProperty(
                    type="type",
            
                    # the properties below are optional
                    failure_threshold=123,
                    resource_path="resourcePath"
                ),
                health_check_custom_config=servicediscovery.CfnService.HealthCheckCustomConfigProperty(
                    failure_threshold=123
                ),
                name="name",
                namespace_id="namespaceId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1995db71cbce145528bd7d73dbfbe2c6e315a97e0979ebd234a52223fb37a0ec)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dns_config", value=dns_config, expected_type=type_hints["dns_config"])
            check_type(argname="argument health_check_config", value=health_check_config, expected_type=type_hints["health_check_config"])
            check_type(argname="argument health_check_custom_config", value=health_check_custom_config, expected_type=type_hints["health_check_custom_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if dns_config is not None:
            self._values["dns_config"] = dns_config
        if health_check_config is not None:
            self._values["health_check_config"] = health_check_config
        if health_check_custom_config is not None:
            self._values["health_check_custom_config"] = health_check_custom_config
        if name is not None:
            self._values["name"] = name
        if namespace_id is not None:
            self._values["namespace_id"] = namespace_id
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.DnsConfigProperty]]:
        '''A complex type that contains information about the Route 53 DNS records that you want AWS Cloud Map to create when you register an instance.

        .. epigraph::

           The record types of a service can only be changed by deleting the service and recreating it with a new ``Dnsconfig`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-dnsconfig
        '''
        result = self._values.get("dns_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.DnsConfigProperty]], result)

    @builtins.property
    def health_check_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckConfigProperty]]:
        '''*Public DNS and HTTP namespaces only.* A complex type that contains settings for an optional health check. If you specify settings for a health check, AWS Cloud Map associates the health check with the records that you specify in ``DnsConfig`` .

        For information about the charges for health checks, see `Amazon Route 53 Pricing <https://docs.aws.amazon.com/route53/pricing/>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckconfig
        '''
        result = self._values.get("health_check_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckConfigProperty]], result)

    @builtins.property
    def health_check_custom_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckCustomConfigProperty]]:
        '''A complex type that contains information about an optional custom health check.

        .. epigraph::

           If you specify a health check configuration, you can specify either ``HealthCheckCustomConfig`` or ``HealthCheckConfig`` but not both.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-healthcheckcustomconfig
        '''
        result = self._values.get("health_check_custom_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckCustomConfigProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def namespace_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the namespace that was used to create the service.

        .. epigraph::

           You must specify a value for ``NamespaceId`` either for the service properties or for `DnsConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-servicediscovery-service-dnsconfig.html>`_ . Don't specify a value in both places.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-namespaceid
        '''
        result = self._values.get("namespace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the service.

        Each tag consists of a key and an optional value, both of which you define. Tag keys can have a maximum character length of 128 characters, and tag values can have a maximum length of 256 characters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''If present, specifies that the service instances are only discoverable using the ``DiscoverInstances`` API operation.

        No DNS records is registered for the service instances. The only valid value is ``HTTP`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-servicediscovery-service.html#cfn-servicediscovery-service-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CnameInstanceBaseProps",
    jsii_struct_bases=[BaseInstanceProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
        "instance_cname": "instanceCname",
    },
)
class CnameInstanceBaseProps(BaseInstanceProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_cname: builtins.str,
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.

        :exampleMetadata: lit=test/integ.service-with-cname-record.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
                name="foobar.com"
            )
            
            service = namespace.create_service("Service",
                name="foo",
                dns_record_type=servicediscovery.DnsRecordType.CNAME,
                dns_ttl=cdk.Duration.seconds(30)
            )
            
            service.register_cname_instance("CnameInstance",
                instance_cname="service.pizza"
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8cd60f4c551c799d49032e9d51a4c65c89304e1d5c853440c53f438353a1ba)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_cname", value=instance_cname, expected_type=type_hints["instance_cname"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_cname": instance_cname,
        }
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_cname(self) -> builtins.str:
        '''If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.'''
        result = self._values.get("instance_cname")
        assert result is not None, "Required property 'instance_cname' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CnameInstanceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.CnameInstanceProps",
    jsii_struct_bases=[CnameInstanceBaseProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
        "instance_cname": "instanceCname",
        "service": "service",
    },
)
class CnameInstanceProps(CnameInstanceBaseProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        instance_cname: builtins.str,
        service: "IService",
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        :param service: The Cloudmap service this resource is registered to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            # service: servicediscovery.Service
            
            cname_instance_props = servicediscovery.CnameInstanceProps(
                instance_cname="instanceCname",
                service=service,
            
                # the properties below are optional
                custom_attributes={
                    "custom_attributes_key": "customAttributes"
                },
                instance_id="instanceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a8eea4c66595a339dbcb97493c30c984ed1d2c9e5bad11bd692ff1c4eeed089)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument instance_cname", value=instance_cname, expected_type=type_hints["instance_cname"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "instance_cname": instance_cname,
            "service": service,
        }
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def instance_cname(self) -> builtins.str:
        '''If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.'''
        result = self._values.get("instance_cname")
        assert result is not None, "Required property 'instance_cname' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> "IService":
        '''The Cloudmap service this resource is registered to.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast("IService", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CnameInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.DnsRecordType")
class DnsRecordType(enum.Enum):
    '''
    :exampleMetadata: lit=test/integ.service-with-cname-record.lit.ts infused

    Example::

        import aws_cdk.core as cdk
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        app = cdk.App()
        stack = cdk.Stack(app, "aws-servicediscovery-integ")
        
        namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
            name="foobar.com"
        )
        
        service = namespace.create_service("Service",
            name="foo",
            dns_record_type=servicediscovery.DnsRecordType.CNAME,
            dns_ttl=cdk.Duration.seconds(30)
        )
        
        service.register_cname_instance("CnameInstance",
            instance_cname="service.pizza"
        )
        
        app.synth()
    '''

    A = "A"
    '''An A record.'''
    AAAA = "AAAA"
    '''An AAAA record.'''
    A_AAAA = "A_AAAA"
    '''Both an A and AAAA record.'''
    SRV = "SRV"
    '''A Srv record.'''
    CNAME = "CNAME"
    '''A CNAME record.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.DnsServiceProps",
    jsii_struct_bases=[BaseServiceProps],
    name_mapping={
        "custom_health_check": "customHealthCheck",
        "description": "description",
        "health_check": "healthCheck",
        "name": "name",
        "dns_record_type": "dnsRecordType",
        "dns_ttl": "dnsTtl",
        "load_balancer": "loadBalancer",
        "routing_policy": "routingPolicy",
    },
)
class DnsServiceProps(BaseServiceProps):
    def __init__(
        self,
        *,
        custom_health_check: typing.Optional[typing.Union["HealthCheckCustomConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union["HealthCheckConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        dns_record_type: typing.Optional[DnsRecordType] = None,
        dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancer: typing.Optional[builtins.bool] = None,
        routing_policy: typing.Optional["RoutingPolicy"] = None,
    ) -> None:
        '''Service props needed to create a service in a given namespace.

        Used by createService() for PrivateDnsNamespace and
        PublicDnsNamespace

        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise

        :exampleMetadata: lit=test/integ.service-with-public-dns-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
                name="foobar.com"
            )
            
            service = namespace.create_service("Service",
                name="foo",
                dns_record_type=servicediscovery.DnsRecordType.A,
                dns_ttl=cdk.Duration.seconds(30),
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTPS,
                    resource_path="/healthcheck",
                    failure_threshold=2
                )
            )
            
            service.register_ip_instance("IpInstance",
                ipv4="54.239.25.192",
                port=443
            )
            
            app.synth()
        '''
        if isinstance(custom_health_check, dict):
            custom_health_check = HealthCheckCustomConfig(**custom_health_check)
        if isinstance(health_check, dict):
            health_check = HealthCheckConfig(**health_check)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc8eec49cf21e5c49d1905c5f2262d2ba757bfc69a29b34024b589fd594e3fd8)
            check_type(argname="argument custom_health_check", value=custom_health_check, expected_type=type_hints["custom_health_check"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dns_record_type", value=dns_record_type, expected_type=type_hints["dns_record_type"])
            check_type(argname="argument dns_ttl", value=dns_ttl, expected_type=type_hints["dns_ttl"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_health_check is not None:
            self._values["custom_health_check"] = custom_health_check
        if description is not None:
            self._values["description"] = description
        if health_check is not None:
            self._values["health_check"] = health_check
        if name is not None:
            self._values["name"] = name
        if dns_record_type is not None:
            self._values["dns_record_type"] = dns_record_type
        if dns_ttl is not None:
            self._values["dns_ttl"] = dns_ttl
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if routing_policy is not None:
            self._values["routing_policy"] = routing_policy

    @builtins.property
    def custom_health_check(self) -> typing.Optional["HealthCheckCustomConfig"]:
        '''Structure containing failure threshold for a custom health checker.

        Only one of healthCheckConfig or healthCheckCustomConfig can be specified.
        See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html

        :default: none
        '''
        result = self._values.get("custom_health_check")
        return typing.cast(typing.Optional["HealthCheckCustomConfig"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check(self) -> typing.Optional["HealthCheckConfig"]:
        '''Settings for an optional health check.

        If you specify health check settings, AWS Cloud Map associates the health
        check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can
        be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to
        this service.

        :default: none
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional["HealthCheckConfig"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the Service.

        :default: CloudFormation-generated name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_record_type(self) -> typing.Optional[DnsRecordType]:
        '''The DNS type of the record that you want AWS Cloud Map to create.

        Supported record types
        include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV.

        :default: A
        '''
        result = self._values.get("dns_record_type")
        return typing.cast(typing.Optional[DnsRecordType], result)

    @builtins.property
    def dns_ttl(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("dns_ttl")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance.

        Setting this to ``true`` correctly configures the ``routingPolicy``
        and performs some additional validation.

        :default: false
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def routing_policy(self) -> typing.Optional["RoutingPolicy"]:
        '''The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service.

        :default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        '''
        result = self._values.get("routing_policy")
        return typing.cast(typing.Optional["RoutingPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DnsServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckConfig",
    jsii_struct_bases=[],
    name_mapping={
        "failure_threshold": "failureThreshold",
        "resource_path": "resourcePath",
        "type": "type",
    },
)
class HealthCheckConfig:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
        resource_path: typing.Optional[builtins.str] = None,
        type: typing.Optional["HealthCheckType"] = None,
    ) -> None:
        '''Settings for an optional Amazon Route 53 health check.

        If you specify settings for a health check, AWS Cloud Map
        associates the health check with all the records that you specify in DnsConfig. Only valid with a PublicDnsNamespace.

        :param failure_threshold: The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or vice versa. Default: 1
        :param resource_path: The path that you want Route 53 to request when performing health checks. Do not use when health check type is TCP. Default: '/'
        :param type: The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy. Cannot be modified once created. Supported values are HTTP, HTTPS, and TCP. Default: HTTP

        :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
                name="covfefe"
            )
            
            service1 = namespace.create_service("NonIpService",
                description="service registering non-ip instances"
            )
            
            service1.register_non_ip_instance("NonIpInstance",
                custom_attributes={"arn": "arn:aws:s3:::mybucket"}
            )
            
            service2 = namespace.create_service("IpService",
                description="service registering ip instances",
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTP,
                    resource_path="/check"
                )
            )
            
            service2.register_ip_instance("IpInstance",
                ipv4="54.239.25.192"
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740cb9890b14bef0e4afa9518502938e853131f225731373de8e6c693ce1a6c2)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
            check_type(argname="argument resource_path", value=resource_path, expected_type=type_hints["resource_path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold
        if resource_path is not None:
            self._values["resource_path"] = resource_path
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of consecutive health checks that an endpoint must pass or fail for Route 53 to change the current status of the endpoint from unhealthy to healthy or vice versa.

        :default: 1
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def resource_path(self) -> typing.Optional[builtins.str]:
        '''The path that you want Route 53 to request when performing health checks.

        Do not use when health check type is TCP.

        :default: '/'
        '''
        result = self._values.get("resource_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional["HealthCheckType"]:
        '''The type of health check that you want to create, which indicates how Route 53 determines whether an endpoint is healthy.

        Cannot be modified once created. Supported values are HTTP, HTTPS, and TCP.

        :default: HTTP
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["HealthCheckType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheckConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckCustomConfig",
    jsii_struct_bases=[],
    name_mapping={"failure_threshold": "failureThreshold"},
)
class HealthCheckCustomConfig:
    def __init__(
        self,
        *,
        failure_threshold: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Specifies information about an optional custom health check.

        :param failure_threshold: The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance. Default: 1

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            health_check_custom_config = servicediscovery.HealthCheckCustomConfig(
                failure_threshold=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0e1c2289eeea083eb366ab7987ed3f41c3d017fa2b0c265081b23f80c438ee)
            check_type(argname="argument failure_threshold", value=failure_threshold, expected_type=type_hints["failure_threshold"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if failure_threshold is not None:
            self._values["failure_threshold"] = failure_threshold

    @builtins.property
    def failure_threshold(self) -> typing.Optional[jsii.Number]:
        '''The number of 30-second intervals that you want Cloud Map to wait after receiving an UpdateInstanceCustomHealthStatus request before it changes the health status of a service instance.

        :default: 1
        '''
        result = self._values.get("failure_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HealthCheckCustomConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.HealthCheckType")
class HealthCheckType(enum.Enum):
    '''
    :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

    Example::

        import aws_cdk.core as cdk
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        app = cdk.App()
        stack = cdk.Stack(app, "aws-servicediscovery-integ")
        
        namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
            name="covfefe"
        )
        
        service1 = namespace.create_service("NonIpService",
            description="service registering non-ip instances"
        )
        
        service1.register_non_ip_instance("NonIpInstance",
            custom_attributes={"arn": "arn:aws:s3:::mybucket"}
        )
        
        service2 = namespace.create_service("IpService",
            description="service registering ip instances",
            health_check=servicediscovery.HealthCheckConfig(
                type=servicediscovery.HealthCheckType.HTTP,
                resource_path="/check"
            )
        )
        
        service2.register_ip_instance("IpInstance",
            ipv4="54.239.25.192"
        )
        
        app.synth()
    '''

    HTTP = "HTTP"
    '''Route 53 tries to establish a TCP connection.

    If successful, Route 53 submits an HTTP request and waits for an HTTP
    status code of 200 or greater and less than 400.
    '''
    HTTPS = "HTTPS"
    '''Route 53 tries to establish a TCP connection.

    If successful, Route 53 submits an HTTPS request and waits for an
    HTTP status code of 200 or greater and less than 400.  If you specify HTTPS for the value of Type, the endpoint
    must support TLS v1.0 or later.
    '''
    TCP = "TCP"
    '''Route 53 tries to establish a TCP connection.

    If you specify TCP for Type, don't specify a value for ResourcePath.
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespaceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_arn": "namespaceArn",
        "namespace_id": "namespaceId",
        "namespace_name": "namespaceName",
    },
)
class HttpNamespaceAttributes:
    def __init__(
        self,
        *,
        namespace_arn: builtins.str,
        namespace_id: builtins.str,
        namespace_name: builtins.str,
    ) -> None:
        '''
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            http_namespace_attributes = servicediscovery.HttpNamespaceAttributes(
                namespace_arn="namespaceArn",
                namespace_id="namespaceId",
                namespace_name="namespaceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9296592640a61e4a041a6552f79232ee4666fe3a7b6c60441456ee61473cadb)
            check_type(argname="argument namespace_arn", value=namespace_arn, expected_type=type_hints["namespace_arn"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_arn": namespace_arn,
            "namespace_id": namespace_id,
            "namespace_name": namespace_name,
        }

    @builtins.property
    def namespace_arn(self) -> builtins.str:
        '''Namespace ARN for the Namespace.'''
        result = self._values.get("namespace_arn")
        assert result is not None, "Required property 'namespace_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the Namespace.'''
        result = self._values.get("namespace_id")
        assert result is not None, "Required property 'namespace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNamespaceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespaceProps",
    jsii_struct_bases=[BaseNamespaceProps],
    name_mapping={"name": "name", "description": "description"},
)
class HttpNamespaceProps(BaseNamespaceProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none

        :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
                name="covfefe"
            )
            
            service1 = namespace.create_service("NonIpService",
                description="service registering non-ip instances"
            )
            
            service1.register_non_ip_instance("NonIpInstance",
                custom_attributes={"arn": "arn:aws:s3:::mybucket"}
            )
            
            service2 = namespace.create_service("IpService",
                description="service registering ip instances",
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTP,
                    resource_path="/check"
                )
            )
            
            service2.register_ip_instance("IpInstance",
                ipv4="54.239.25.192"
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86268690f595ac7c38e970ab712d550adc8204e21d4bf5d5022743f861df382d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Namespace.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IInstance")
class IInstance(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The id of the instance resource.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        '''The Cloudmap service this resource is registered to.'''
        ...


class _IInstanceProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicediscovery.IInstance"

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The id of the instance resource.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> "IService":
        '''The Cloudmap service this resource is registered to.'''
        return typing.cast("IService", jsii.get(self, "service"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInstance).__jsii_proxy_class__ = lambda : _IInstanceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.INamespace")
class INamespace(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> builtins.str:
        '''Namespace ARN for the Namespace.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the Namespace.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''A name for the Namespace.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        '''Type of Namespace.'''
        ...


class _INamespaceProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicediscovery.INamespace"

    @builtins.property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> builtins.str:
        '''Namespace ARN for the Namespace.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the Namespace.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''A name for the Namespace.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> "NamespaceType":
        '''Type of Namespace.'''
        return typing.cast("NamespaceType", jsii.get(self, "type"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, INamespace).__jsii_proxy_class__ = lambda : _INamespaceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IPrivateDnsNamespace")
class IPrivateDnsNamespace(INamespace, typing_extensions.Protocol):
    pass


class _IPrivateDnsNamespaceProxy(
    jsii.proxy_for(INamespace), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicediscovery.IPrivateDnsNamespace"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPrivateDnsNamespace).__jsii_proxy_class__ = lambda : _IPrivateDnsNamespaceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IPublicDnsNamespace")
class IPublicDnsNamespace(INamespace, typing_extensions.Protocol):
    pass


class _IPublicDnsNamespaceProxy(
    jsii.proxy_for(INamespace), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicediscovery.IPublicDnsNamespace"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPublicDnsNamespace).__jsii_proxy_class__ = lambda : _IPublicDnsNamespaceProxy


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IService")
class IService(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> DnsRecordType:
        '''The DnsRecordType used by the service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> INamespace:
        '''The namespace for the Cloudmap Service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        '''The Routing Policy used by the service.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''The Arn of the namespace that you want to use for DNS configuration.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''The ID of the namespace that you want to use for DNS configuration.

        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''A name for the Cloudmap Service.

        :attribute: true
        '''
        ...


class _IServiceProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicediscovery.IService"

    @builtins.property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> DnsRecordType:
        '''The DnsRecordType used by the service.'''
        return typing.cast(DnsRecordType, jsii.get(self, "dnsRecordType"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> INamespace:
        '''The namespace for the Cloudmap Service.'''
        return typing.cast(INamespace, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> "RoutingPolicy":
        '''The Routing Policy used by the service.'''
        return typing.cast("RoutingPolicy", jsii.get(self, "routingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''The Arn of the namespace that you want to use for DNS configuration.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''The ID of the namespace that you want to use for DNS configuration.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''A name for the Cloudmap Service.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IService).__jsii_proxy_class__ = lambda : _IServiceProxy


@jsii.implements(IInstance)
class InstanceBase(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-servicediscovery.InstanceBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b20dff37751e51559f2ca8f7af6a30d8128ddde85ba6d29afe2e6a2eb2e47748)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = _aws_cdk_core_f4b25747.ResourceProps(
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="uniqueInstanceId")
    def _unique_instance_id(self) -> builtins.str:
        '''Generate a unique instance Id that is safe to pass to CloudMap.'''
        return typing.cast(builtins.str, jsii.invoke(self, "uniqueInstanceId", []))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    @abc.abstractmethod
    def instance_id(self) -> builtins.str:
        '''The Id of the instance.'''
        ...

    @builtins.property
    @jsii.member(jsii_name="service")
    @abc.abstractmethod
    def service(self) -> IService:
        '''The Cloudmap service to which the instance is registered.'''
        ...


class _InstanceBaseProxy(
    InstanceBase,
    jsii.proxy_for(_aws_cdk_core_f4b25747.Resource), # type: ignore[misc]
):
    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Id of the instance.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The Cloudmap service to which the instance is registered.'''
        return typing.cast(IService, jsii.get(self, "service"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, InstanceBase).__jsii_proxy_class__ = lambda : _InstanceBaseProxy


class IpInstance(
    InstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.IpInstance",
):
    '''Instance that is accessible using an IP address.

    :resource: AWS::ServiceDiscovery::Instance
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        # service: servicediscovery.Service
        
        ip_instance = servicediscovery.IpInstance(self, "MyIpInstance",
            service=service,
        
            # the properties below are optional
            custom_attributes={
                "custom_attributes_key": "customAttributes"
            },
            instance_id="instanceId",
            ipv4="ipv4",
            ipv6="ipv6",
            port=123
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service: IService,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param service: The Cloudmap service this resource is registered to.
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd995cca1ff422abd6c31ccb22564be78c5df0f50d302d9df18c6ce8c26285db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpInstanceProps(
            service=service,
            ipv4=ipv4,
            ipv6=ipv6,
            port=port,
            custom_attributes=custom_attributes,
            instance_id=instance_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Id of the instance.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="ipv4")
    def ipv4(self) -> builtins.str:
        '''The Ipv4 address of the instance, or blank string if none available.'''
        return typing.cast(builtins.str, jsii.get(self, "ipv4"))

    @builtins.property
    @jsii.member(jsii_name="ipv6")
    def ipv6(self) -> builtins.str:
        '''The Ipv6 address of the instance, or blank string if none available.'''
        return typing.cast(builtins.str, jsii.get(self, "ipv6"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        '''The exposed port of the instance.'''
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The Cloudmap service to which the instance is registered.'''
        return typing.cast(IService, jsii.get(self, "service"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.IpInstanceBaseProps",
    jsii_struct_bases=[BaseInstanceProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
        "ipv4": "ipv4",
        "ipv6": "ipv6",
        "port": "port",
    },
)
class IpInstanceBaseProps(BaseInstanceProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80

        :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
                name="covfefe"
            )
            
            service1 = namespace.create_service("NonIpService",
                description="service registering non-ip instances"
            )
            
            service1.register_non_ip_instance("NonIpInstance",
                custom_attributes={"arn": "arn:aws:s3:::mybucket"}
            )
            
            service2 = namespace.create_service("IpService",
                description="service registering ip instances",
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTP,
                    resource_path="/check"
                )
            )
            
            service2.register_ip_instance("IpInstance",
                ipv4="54.239.25.192"
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81afefb2fe8b6b52bdabb4532030f2a86c8b0930910fdf21ec8540c0238f10fb)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4(self) -> typing.Optional[builtins.str]:
        '''If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record.

        :default: none
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(self) -> typing.Optional[builtins.str]:
        '''If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record.

        :default: none
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on the endpoint that you want AWS Cloud Map to perform health checks on.

        This value is also used for
        the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a
        default port that is applied to all instances in the Service configuration.

        :default: 80
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpInstanceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.IpInstanceProps",
    jsii_struct_bases=[IpInstanceBaseProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
        "ipv4": "ipv4",
        "ipv6": "ipv6",
        "port": "port",
        "service": "service",
    },
)
class IpInstanceProps(IpInstanceBaseProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service: IService,
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        :param service: The Cloudmap service this resource is registered to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            # service: servicediscovery.Service
            
            ip_instance_props = servicediscovery.IpInstanceProps(
                service=service,
            
                # the properties below are optional
                custom_attributes={
                    "custom_attributes_key": "customAttributes"
                },
                instance_id="instanceId",
                ipv4="ipv4",
                ipv6="ipv6",
                port=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__959fdf6a2ae18a3c3c68ca9db3b368d071b1b98ad301decaa72eea88362669f0)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument ipv4", value=ipv4, expected_type=type_hints["ipv4"])
            check_type(argname="argument ipv6", value=ipv6, expected_type=type_hints["ipv6"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id
        if ipv4 is not None:
            self._values["ipv4"] = ipv4
        if ipv6 is not None:
            self._values["ipv6"] = ipv6
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv4(self) -> typing.Optional[builtins.str]:
        '''If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record.

        :default: none
        '''
        result = self._values.get("ipv4")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ipv6(self) -> typing.Optional[builtins.str]:
        '''If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record.

        :default: none
        '''
        result = self._values.get("ipv6")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port on the endpoint that you want AWS Cloud Map to perform health checks on.

        This value is also used for
        the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a
        default port that is applied to all instances in the Service configuration.

        :default: 80
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service(self) -> IService:
        '''The Cloudmap service this resource is registered to.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IpInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.NamespaceType")
class NamespaceType(enum.Enum):
    HTTP = "HTTP"
    '''Choose this option if you want your application to use only API calls to discover registered instances.'''
    DNS_PRIVATE = "DNS_PRIVATE"
    '''Choose this option if you want your application to be able to discover instances using either API calls or using DNS queries in a VPC.'''
    DNS_PUBLIC = "DNS_PUBLIC"
    '''Choose this option if you want your application to be able to discover instances using either API calls or using public DNS queries.

    You aren't required to use both methods.
    '''


class NonIpInstance(
    InstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstance",
):
    '''Instance accessible using values other than an IP address or a domain name (CNAME).

    Specify the other values in Custom attributes.

    :resource: AWS::ServiceDiscovery::Instance
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        # service: servicediscovery.Service
        
        non_ip_instance = servicediscovery.NonIpInstance(self, "MyNonIpInstance",
            service=service,
        
            # the properties below are optional
            custom_attributes={
                "custom_attributes_key": "customAttributes"
            },
            instance_id="instanceId"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service: IService,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param service: The Cloudmap service this resource is registered to.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d6a03f12a1da2d36be809022e5f0e17953688ff598f743701f37872f27d1fba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NonIpInstanceProps(
            service=service,
            custom_attributes=custom_attributes,
            instance_id=instance_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Id of the instance.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The Cloudmap service to which the instance is registered.'''
        return typing.cast(IService, jsii.get(self, "service"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstanceBaseProps",
    jsii_struct_bases=[BaseInstanceProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
    },
)
class NonIpInstanceBaseProps(BaseInstanceProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name

        :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
                name="covfefe"
            )
            
            service1 = namespace.create_service("NonIpService",
                description="service registering non-ip instances"
            )
            
            service1.register_non_ip_instance("NonIpInstance",
                custom_attributes={"arn": "arn:aws:s3:::mybucket"}
            )
            
            service2 = namespace.create_service("IpService",
                description="service registering ip instances",
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTP,
                    resource_path="/check"
                )
            )
            
            service2.register_ip_instance("IpInstance",
                ipv4="54.239.25.192"
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f42d702c99f25a526fa7849b5a2599bb4e7db128d8dda9f66185b480a78b02a9)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NonIpInstanceBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.NonIpInstanceProps",
    jsii_struct_bases=[NonIpInstanceBaseProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
        "service": "service",
    },
)
class NonIpInstanceProps(NonIpInstanceBaseProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        service: IService,
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param service: The Cloudmap service this resource is registered to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            # service: servicediscovery.Service
            
            non_ip_instance_props = servicediscovery.NonIpInstanceProps(
                service=service,
            
                # the properties below are optional
                custom_attributes={
                    "custom_attributes_key": "customAttributes"
                },
                instance_id="instanceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21c0501dec47b0c8a855eb3674764cd6275428cb44daad6613649e18672cb92d)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service(self) -> IService:
        '''The Cloudmap service this resource is registered to.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NonIpInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPrivateDnsNamespace)
class PrivateDnsNamespace(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespace",
):
    '''Define a Service Discovery HTTP Namespace.

    :exampleMetadata: infused

    Example::

        # mesh: appmesh.Mesh
        # Cloud Map service discovery is currently required for host ejection by outlier detection
        vpc = ec2.Vpc(self, "vpc")
        namespace = cloudmap.PrivateDnsNamespace(self, "test-namespace",
            vpc=vpc,
            name="domain.local"
        )
        service = namespace.create_service("Svc")
        node = mesh.add_virtual_node("virtual-node",
            service_discovery=appmesh.ServiceDiscovery.cloud_map(service),
            listeners=[appmesh.VirtualNodeListener.http(
                outlier_detection=appmesh.OutlierDetection(
                    base_ejection_duration=cdk.Duration.seconds(10),
                    interval=cdk.Duration.seconds(30),
                    max_ejection_percent=50,
                    max_server_errors=5
                )
            )]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param vpc: The Amazon VPC that you want to associate the namespace with.
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__875ce416a682d118cb431a0a728ed1c03ff81341441798a5e1a24a6c9bb60521)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PrivateDnsNamespaceProps(vpc=vpc, name=name, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPrivateDnsNamespaceAttributes")
    @builtins.classmethod
    def from_private_dns_namespace_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        namespace_arn: builtins.str,
        namespace_id: builtins.str,
        namespace_name: builtins.str,
    ) -> IPrivateDnsNamespace:
        '''
        :param scope: -
        :param id: -
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9b15c9fdbd10190d2d8cfb4ace46db3a6ea27650d5ac975b75e54ddd448936)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = PrivateDnsNamespaceAttributes(
            namespace_arn=namespace_arn,
            namespace_id=namespace_id,
            namespace_name=namespace_name,
        )

        return typing.cast(IPrivateDnsNamespace, jsii.sinvoke(cls, "fromPrivateDnsNamespaceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="createService")
    def create_service(
        self,
        id: builtins.str,
        *,
        dns_record_type: typing.Optional[DnsRecordType] = None,
        dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancer: typing.Optional[builtins.bool] = None,
        routing_policy: typing.Optional["RoutingPolicy"] = None,
        custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "Service":
        '''Creates a service within the namespace.

        :param id: -
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1e2262eaaf762390dd6932863b1d386e88c36778cb8e2f510942fc8e8636a9a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DnsServiceProps(
            dns_record_type=dns_record_type,
            dns_ttl=dns_ttl,
            load_balancer=load_balancer,
            routing_policy=routing_policy,
            custom_health_check=custom_health_check,
            description=description,
            health_check=health_check,
            name=name,
        )

        return typing.cast("Service", jsii.invoke(self, "createService", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> builtins.str:
        '''Namespace Arn of the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        '''Namespace Id of the PrivateDnsNamespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''The name of the PrivateDnsNamespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsNamespaceArn")
    def private_dns_namespace_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "privateDnsNamespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsNamespaceId")
    def private_dns_namespace_id(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "privateDnsNamespaceId"))

    @builtins.property
    @jsii.member(jsii_name="privateDnsNamespaceName")
    def private_dns_namespace_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "privateDnsNamespaceName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> NamespaceType:
        '''Type of the namespace.'''
        return typing.cast(NamespaceType, jsii.get(self, "type"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespaceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_arn": "namespaceArn",
        "namespace_id": "namespaceId",
        "namespace_name": "namespaceName",
    },
)
class PrivateDnsNamespaceAttributes:
    def __init__(
        self,
        *,
        namespace_arn: builtins.str,
        namespace_id: builtins.str,
        namespace_name: builtins.str,
    ) -> None:
        '''
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            private_dns_namespace_attributes = servicediscovery.PrivateDnsNamespaceAttributes(
                namespace_arn="namespaceArn",
                namespace_id="namespaceId",
                namespace_name="namespaceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b78345ad900e8b49d34f3cdacec708a3c135fa02e0c352ac713b0333991095b0)
            check_type(argname="argument namespace_arn", value=namespace_arn, expected_type=type_hints["namespace_arn"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_arn": namespace_arn,
            "namespace_id": namespace_id,
            "namespace_name": namespace_name,
        }

    @builtins.property
    def namespace_arn(self) -> builtins.str:
        '''Namespace ARN for the Namespace.'''
        result = self._values.get("namespace_arn")
        assert result is not None, "Required property 'namespace_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the Namespace.'''
        result = self._values.get("namespace_id")
        assert result is not None, "Required property 'namespace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivateDnsNamespaceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.PrivateDnsNamespaceProps",
    jsii_struct_bases=[BaseNamespaceProps],
    name_mapping={"name": "name", "description": "description", "vpc": "vpc"},
)
class PrivateDnsNamespaceProps(BaseNamespaceProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    ) -> None:
        '''
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        :param vpc: The Amazon VPC that you want to associate the namespace with.

        :exampleMetadata: infused

        Example::

            # mesh: appmesh.Mesh
            # Cloud Map service discovery is currently required for host ejection by outlier detection
            vpc = ec2.Vpc(self, "vpc")
            namespace = cloudmap.PrivateDnsNamespace(self, "test-namespace",
                vpc=vpc,
                name="domain.local"
            )
            service = namespace.create_service("Svc")
            node = mesh.add_virtual_node("virtual-node",
                service_discovery=appmesh.ServiceDiscovery.cloud_map(service),
                listeners=[appmesh.VirtualNodeListener.http(
                    outlier_detection=appmesh.OutlierDetection(
                        base_ejection_duration=cdk.Duration.seconds(10),
                        interval=cdk.Duration.seconds(30),
                        max_ejection_percent=50,
                        max_server_errors=5
                    )
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50856db1b872ef8e548826b7dd57a2597afe1a14baf6b4da4232ac483637291)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "vpc": vpc,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Namespace.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''The Amazon VPC that you want to associate the namespace with.'''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PrivateDnsNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPublicDnsNamespace)
class PublicDnsNamespace(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespace",
):
    '''Define a Public DNS Namespace.

    :exampleMetadata: lit=test/integ.service-with-public-dns-namespace.lit.ts infused

    Example::

        import aws_cdk.core as cdk
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        app = cdk.App()
        stack = cdk.Stack(app, "aws-servicediscovery-integ")
        
        namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
            name="foobar.com"
        )
        
        service = namespace.create_service("Service",
            name="foo",
            dns_record_type=servicediscovery.DnsRecordType.A,
            dns_ttl=cdk.Duration.seconds(30),
            health_check=servicediscovery.HealthCheckConfig(
                type=servicediscovery.HealthCheckType.HTTPS,
                resource_path="/healthcheck",
                failure_threshold=2
            )
        )
        
        service.register_ip_instance("IpInstance",
            ipv4="54.239.25.192",
            port=443
        )
        
        app.synth()
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c908bdc3b29f07272bdb1631fd1619204448b080563553fc6004e4c90270815)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PublicDnsNamespaceProps(name=name, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPublicDnsNamespaceAttributes")
    @builtins.classmethod
    def from_public_dns_namespace_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        namespace_arn: builtins.str,
        namespace_id: builtins.str,
        namespace_name: builtins.str,
    ) -> IPublicDnsNamespace:
        '''
        :param scope: -
        :param id: -
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6a487cd415447d56b5a16b0dc8ae994e9bb4156cb127cb889277e92797fe676)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = PublicDnsNamespaceAttributes(
            namespace_arn=namespace_arn,
            namespace_id=namespace_id,
            namespace_name=namespace_name,
        )

        return typing.cast(IPublicDnsNamespace, jsii.sinvoke(cls, "fromPublicDnsNamespaceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="createService")
    def create_service(
        self,
        id: builtins.str,
        *,
        dns_record_type: typing.Optional[DnsRecordType] = None,
        dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancer: typing.Optional[builtins.bool] = None,
        routing_policy: typing.Optional["RoutingPolicy"] = None,
        custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> "Service":
        '''Creates a service within the namespace.

        :param id: -
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33e2b9fbf4386f94bdba59e2f99c35dde693199b034202b0278de5e897127ba9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DnsServiceProps(
            dns_record_type=dns_record_type,
            dns_ttl=dns_ttl,
            load_balancer=load_balancer,
            routing_policy=routing_policy,
            custom_health_check=custom_health_check,
            description=description,
            health_check=health_check,
            name=name,
        )

        return typing.cast("Service", jsii.invoke(self, "createService", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> builtins.str:
        '''Namespace Arn for the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''A name for the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @builtins.property
    @jsii.member(jsii_name="publicDnsNamespaceArn")
    def public_dns_namespace_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "publicDnsNamespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="publicDnsNamespaceId")
    def public_dns_namespace_id(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "publicDnsNamespaceId"))

    @builtins.property
    @jsii.member(jsii_name="publicDnsNamespaceName")
    def public_dns_namespace_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "publicDnsNamespaceName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> NamespaceType:
        '''Type of the namespace.'''
        return typing.cast(NamespaceType, jsii.get(self, "type"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespaceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "namespace_arn": "namespaceArn",
        "namespace_id": "namespaceId",
        "namespace_name": "namespaceName",
    },
)
class PublicDnsNamespaceAttributes:
    def __init__(
        self,
        *,
        namespace_arn: builtins.str,
        namespace_id: builtins.str,
        namespace_name: builtins.str,
    ) -> None:
        '''
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            public_dns_namespace_attributes = servicediscovery.PublicDnsNamespaceAttributes(
                namespace_arn="namespaceArn",
                namespace_id="namespaceId",
                namespace_name="namespaceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7830336264a79c51f5c874d13efd637c551b66b7f7f97a04577af390048d4d4)
            check_type(argname="argument namespace_arn", value=namespace_arn, expected_type=type_hints["namespace_arn"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument namespace_name", value=namespace_name, expected_type=type_hints["namespace_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_arn": namespace_arn,
            "namespace_id": namespace_id,
            "namespace_name": namespace_name,
        }

    @builtins.property
    def namespace_arn(self) -> builtins.str:
        '''Namespace ARN for the Namespace.'''
        result = self._values.get("namespace_arn")
        assert result is not None, "Required property 'namespace_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the Namespace.'''
        result = self._values.get("namespace_id")
        assert result is not None, "Required property 'namespace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def namespace_name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("namespace_name")
        assert result is not None, "Required property 'namespace_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublicDnsNamespaceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.PublicDnsNamespaceProps",
    jsii_struct_bases=[BaseNamespaceProps],
    name_mapping={"name": "name", "description": "description"},
)
class PublicDnsNamespaceProps(BaseNamespaceProps):
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none

        :exampleMetadata: lit=test/integ.service-with-public-dns-namespace.lit.ts infused

        Example::

            import aws_cdk.core as cdk
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            app = cdk.App()
            stack = cdk.Stack(app, "aws-servicediscovery-integ")
            
            namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
                name="foobar.com"
            )
            
            service = namespace.create_service("Service",
                name="foo",
                dns_record_type=servicediscovery.DnsRecordType.A,
                dns_ttl=cdk.Duration.seconds(30),
                health_check=servicediscovery.HealthCheckConfig(
                    type=servicediscovery.HealthCheckType.HTTPS,
                    resource_path="/healthcheck",
                    failure_threshold=2
                )
            )
            
            service.register_ip_instance("IpInstance",
                ipv4="54.239.25.192",
                port=443
            )
            
            app.synth()
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__178f39ceeaec447d3a507b01c4360dc199e55c93c9232a4c1ba3e772407cdd7c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the Namespace.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the Namespace.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublicDnsNamespaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-servicediscovery.RoutingPolicy")
class RoutingPolicy(enum.Enum):
    WEIGHTED = "WEIGHTED"
    '''Route 53 returns the applicable value from one randomly selected instance from among the instances that you registered using the same service.'''
    MULTIVALUE = "MULTIVALUE"
    '''If you define a health check for the service and the health check is healthy, Route 53 returns the applicable value for up to eight instances.'''


@jsii.implements(IService)
class Service(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.Service",
):
    '''Define a CloudMap Service.

    :exampleMetadata: lit=test/integ.service-with-public-dns-namespace.lit.ts infused

    Example::

        import aws_cdk.core as cdk
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        app = cdk.App()
        stack = cdk.Stack(app, "aws-servicediscovery-integ")
        
        namespace = servicediscovery.PublicDnsNamespace(stack, "Namespace",
            name="foobar.com"
        )
        
        service = namespace.create_service("Service",
            name="foo",
            dns_record_type=servicediscovery.DnsRecordType.A,
            dns_ttl=cdk.Duration.seconds(30),
            health_check=servicediscovery.HealthCheckConfig(
                type=servicediscovery.HealthCheckType.HTTPS,
                resource_path="/healthcheck",
                failure_threshold=2
            )
        )
        
        service.register_ip_instance("IpInstance",
            ipv4="54.239.25.192",
            port=443
        )
        
        app.synth()
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        namespace: INamespace,
        dns_record_type: typing.Optional[DnsRecordType] = None,
        dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancer: typing.Optional[builtins.bool] = None,
        routing_policy: typing.Optional[RoutingPolicy] = None,
        custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param namespace: The namespace that you want to use for DNS configuration.
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b07d6ca9e1a3ddacf7f8ab52d742b896c9ec34ad806e479e9ce3a8630828eb56)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ServiceProps(
            namespace=namespace,
            dns_record_type=dns_record_type,
            dns_ttl=dns_ttl,
            load_balancer=load_balancer,
            routing_policy=routing_policy,
            custom_health_check=custom_health_check,
            description=description,
            health_check=health_check,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromServiceAttributes")
    @builtins.classmethod
    def from_service_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dns_record_type: DnsRecordType,
        namespace: INamespace,
        routing_policy: RoutingPolicy,
        service_arn: builtins.str,
        service_id: builtins.str,
        service_name: builtins.str,
    ) -> IService:
        '''
        :param scope: -
        :param id: -
        :param dns_record_type: 
        :param namespace: 
        :param routing_policy: 
        :param service_arn: 
        :param service_id: 
        :param service_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9805a230f9f9a8893d95c50f4be7506e2125579659994f48c06af99ab8206cd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = ServiceAttributes(
            dns_record_type=dns_record_type,
            namespace=namespace,
            routing_policy=routing_policy,
            service_arn=service_arn,
            service_id=service_id,
            service_name=service_name,
        )

        return typing.cast(IService, jsii.sinvoke(cls, "fromServiceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="registerCnameInstance")
    def register_cname_instance(
        self,
        id: builtins.str,
        *,
        instance_cname: builtins.str,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> IInstance:
        '''Registers a resource that is accessible using a CNAME.

        :param id: -
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c3ab559f7637734c893e5951d9c2780a0577b6fcabb7b62e0648046bb0364ed)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CnameInstanceBaseProps(
            instance_cname=instance_cname,
            custom_attributes=custom_attributes,
            instance_id=instance_id,
        )

        return typing.cast(IInstance, jsii.invoke(self, "registerCnameInstance", [id, props]))

    @jsii.member(jsii_name="registerIpInstance")
    def register_ip_instance(
        self,
        id: builtins.str,
        *,
        ipv4: typing.Optional[builtins.str] = None,
        ipv6: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> IInstance:
        '''Registers a resource that is accessible using an IP address.

        :param id: -
        :param ipv4: If the service that you specify contains a template for an A record, the IPv4 address that you want AWS Cloud Map to use for the value of the A record. Default: none
        :param ipv6: If the service that you specify contains a template for an AAAA record, the IPv6 address that you want AWS Cloud Map to use for the value of the AAAA record. Default: none
        :param port: The port on the endpoint that you want AWS Cloud Map to perform health checks on. This value is also used for the port value in an SRV record if the service that you specify includes an SRV record. You can also specify a default port that is applied to all instances in the Service configuration. Default: 80
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96e45af0d0161a647590abd9f93fdaa59fd52f0ea21c9f9bf090b79c9b2d7b3a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IpInstanceBaseProps(
            ipv4=ipv4,
            ipv6=ipv6,
            port=port,
            custom_attributes=custom_attributes,
            instance_id=instance_id,
        )

        return typing.cast(IInstance, jsii.invoke(self, "registerIpInstance", [id, props]))

    @jsii.member(jsii_name="registerLoadBalancer")
    def register_load_balancer(
        self,
        id: builtins.str,
        load_balancer: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ILoadBalancerV2,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> IInstance:
        '''Registers an ELB as a new instance with unique name instanceId in this service.

        :param id: -
        :param load_balancer: -
        :param custom_attributes: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b932e1c83207129355a1e073c42463df4d7b53431b9bc7cc15554b97fa53699)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
        return typing.cast(IInstance, jsii.invoke(self, "registerLoadBalancer", [id, load_balancer, custom_attributes]))

    @jsii.member(jsii_name="registerNonIpInstance")
    def register_non_ip_instance(
        self,
        id: builtins.str,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> IInstance:
        '''Registers a resource that is accessible using values other than an IP address or a domain name (CNAME).

        :param id: -
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea7cdd9bb1b870d66c2e75244fc5dce982df263ddd0431a0500877f24eae42e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NonIpInstanceBaseProps(
            custom_attributes=custom_attributes, instance_id=instance_id
        )

        return typing.cast(IInstance, jsii.invoke(self, "registerNonIpInstance", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="dnsRecordType")
    def dns_record_type(self) -> DnsRecordType:
        '''The DnsRecordType used by the service.'''
        return typing.cast(DnsRecordType, jsii.get(self, "dnsRecordType"))

    @builtins.property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> INamespace:
        '''The namespace for the Cloudmap Service.'''
        return typing.cast(INamespace, jsii.get(self, "namespace"))

    @builtins.property
    @jsii.member(jsii_name="routingPolicy")
    def routing_policy(self) -> RoutingPolicy:
        '''The Routing Policy used by the service.'''
        return typing.cast(RoutingPolicy, jsii.get(self, "routingPolicy"))

    @builtins.property
    @jsii.member(jsii_name="serviceArn")
    def service_arn(self) -> builtins.str:
        '''The Arn of the namespace that you want to use for DNS configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceArn"))

    @builtins.property
    @jsii.member(jsii_name="serviceId")
    def service_id(self) -> builtins.str:
        '''The ID of the namespace that you want to use for DNS configuration.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceId"))

    @builtins.property
    @jsii.member(jsii_name="serviceName")
    def service_name(self) -> builtins.str:
        '''A name for the Cloudmap Service.'''
        return typing.cast(builtins.str, jsii.get(self, "serviceName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.ServiceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "dns_record_type": "dnsRecordType",
        "namespace": "namespace",
        "routing_policy": "routingPolicy",
        "service_arn": "serviceArn",
        "service_id": "serviceId",
        "service_name": "serviceName",
    },
)
class ServiceAttributes:
    def __init__(
        self,
        *,
        dns_record_type: DnsRecordType,
        namespace: INamespace,
        routing_policy: RoutingPolicy,
        service_arn: builtins.str,
        service_id: builtins.str,
        service_name: builtins.str,
    ) -> None:
        '''
        :param dns_record_type: 
        :param namespace: 
        :param routing_policy: 
        :param service_arn: 
        :param service_id: 
        :param service_name: 

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            # namespace: servicediscovery.INamespace
            
            service_attributes = servicediscovery.ServiceAttributes(
                dns_record_type=servicediscovery.DnsRecordType.A,
                namespace=namespace,
                routing_policy=servicediscovery.RoutingPolicy.WEIGHTED,
                service_arn="serviceArn",
                service_id="serviceId",
                service_name="serviceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c29c8c4958d6dbe0bea53f64c9ab2645ee9d1de536a88aa9638070bc9399d2da)
            check_type(argname="argument dns_record_type", value=dns_record_type, expected_type=type_hints["dns_record_type"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
            check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
            check_type(argname="argument service_arn", value=service_arn, expected_type=type_hints["service_arn"])
            check_type(argname="argument service_id", value=service_id, expected_type=type_hints["service_id"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_record_type": dns_record_type,
            "namespace": namespace,
            "routing_policy": routing_policy,
            "service_arn": service_arn,
            "service_id": service_id,
            "service_name": service_name,
        }

    @builtins.property
    def dns_record_type(self) -> DnsRecordType:
        result = self._values.get("dns_record_type")
        assert result is not None, "Required property 'dns_record_type' is missing"
        return typing.cast(DnsRecordType, result)

    @builtins.property
    def namespace(self) -> INamespace:
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(INamespace, result)

    @builtins.property
    def routing_policy(self) -> RoutingPolicy:
        result = self._values.get("routing_policy")
        assert result is not None, "Required property 'routing_policy' is missing"
        return typing.cast(RoutingPolicy, result)

    @builtins.property
    def service_arn(self) -> builtins.str:
        result = self._values.get("service_arn")
        assert result is not None, "Required property 'service_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_id(self) -> builtins.str:
        result = self._values.get("service_id")
        assert result is not None, "Required property 'service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.ServiceProps",
    jsii_struct_bases=[DnsServiceProps],
    name_mapping={
        "custom_health_check": "customHealthCheck",
        "description": "description",
        "health_check": "healthCheck",
        "name": "name",
        "dns_record_type": "dnsRecordType",
        "dns_ttl": "dnsTtl",
        "load_balancer": "loadBalancer",
        "routing_policy": "routingPolicy",
        "namespace": "namespace",
    },
)
class ServiceProps(DnsServiceProps):
    def __init__(
        self,
        *,
        custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
        dns_record_type: typing.Optional[DnsRecordType] = None,
        dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
        load_balancer: typing.Optional[builtins.bool] = None,
        routing_policy: typing.Optional[RoutingPolicy] = None,
        namespace: INamespace,
    ) -> None:
        '''
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        :param dns_record_type: The DNS type of the record that you want AWS Cloud Map to create. Supported record types include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV. Default: A
        :param dns_ttl: The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record. Default: Duration.minutes(1)
        :param load_balancer: Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance. Setting this to ``true`` correctly configures the ``routingPolicy`` and performs some additional validation. Default: false
        :param routing_policy: The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service. Default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        :param namespace: The namespace that you want to use for DNS configuration.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            import aws_cdk.core as cdk
            
            # namespace: servicediscovery.INamespace
            
            service_props = servicediscovery.ServiceProps(
                namespace=namespace,
            
                # the properties below are optional
                custom_health_check=servicediscovery.HealthCheckCustomConfig(
                    failure_threshold=123
                ),
                description="description",
                dns_record_type=servicediscovery.DnsRecordType.A,
                dns_ttl=cdk.Duration.minutes(30),
                health_check=servicediscovery.HealthCheckConfig(
                    failure_threshold=123,
                    resource_path="resourcePath",
                    type=servicediscovery.HealthCheckType.HTTP
                ),
                load_balancer=False,
                name="name",
                routing_policy=servicediscovery.RoutingPolicy.WEIGHTED
            )
        '''
        if isinstance(custom_health_check, dict):
            custom_health_check = HealthCheckCustomConfig(**custom_health_check)
        if isinstance(health_check, dict):
            health_check = HealthCheckConfig(**health_check)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8607ad503ffffd20363e36ed518cc1c0e0c0a3b0099ae96129acb71e942162)
            check_type(argname="argument custom_health_check", value=custom_health_check, expected_type=type_hints["custom_health_check"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument dns_record_type", value=dns_record_type, expected_type=type_hints["dns_record_type"])
            check_type(argname="argument dns_ttl", value=dns_ttl, expected_type=type_hints["dns_ttl"])
            check_type(argname="argument load_balancer", value=load_balancer, expected_type=type_hints["load_balancer"])
            check_type(argname="argument routing_policy", value=routing_policy, expected_type=type_hints["routing_policy"])
            check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace": namespace,
        }
        if custom_health_check is not None:
            self._values["custom_health_check"] = custom_health_check
        if description is not None:
            self._values["description"] = description
        if health_check is not None:
            self._values["health_check"] = health_check
        if name is not None:
            self._values["name"] = name
        if dns_record_type is not None:
            self._values["dns_record_type"] = dns_record_type
        if dns_ttl is not None:
            self._values["dns_ttl"] = dns_ttl
        if load_balancer is not None:
            self._values["load_balancer"] = load_balancer
        if routing_policy is not None:
            self._values["routing_policy"] = routing_policy

    @builtins.property
    def custom_health_check(self) -> typing.Optional[HealthCheckCustomConfig]:
        '''Structure containing failure threshold for a custom health checker.

        Only one of healthCheckConfig or healthCheckCustomConfig can be specified.
        See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html

        :default: none
        '''
        result = self._values.get("custom_health_check")
        return typing.cast(typing.Optional[HealthCheckCustomConfig], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the service.

        :default: none
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check(self) -> typing.Optional[HealthCheckConfig]:
        '''Settings for an optional health check.

        If you specify health check settings, AWS Cloud Map associates the health
        check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can
        be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to
        this service.

        :default: none
        '''
        result = self._values.get("health_check")
        return typing.cast(typing.Optional[HealthCheckConfig], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the Service.

        :default: CloudFormation-generated name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_record_type(self) -> typing.Optional[DnsRecordType]:
        '''The DNS type of the record that you want AWS Cloud Map to create.

        Supported record types
        include A, AAAA, A and AAAA (A_AAAA), CNAME, and SRV.

        :default: A
        '''
        result = self._values.get("dns_record_type")
        return typing.cast(typing.Optional[DnsRecordType], result)

    @builtins.property
    def dns_ttl(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''The amount of time, in seconds, that you want DNS resolvers to cache the settings for this record.

        :default: Duration.minutes(1)
        '''
        result = self._values.get("dns_ttl")
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], result)

    @builtins.property
    def load_balancer(self) -> typing.Optional[builtins.bool]:
        '''Whether or not this service will have an Elastic LoadBalancer registered to it as an AliasTargetInstance.

        Setting this to ``true`` correctly configures the ``routingPolicy``
        and performs some additional validation.

        :default: false
        '''
        result = self._values.get("load_balancer")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def routing_policy(self) -> typing.Optional[RoutingPolicy]:
        '''The routing policy that you want to apply to all DNS records that AWS Cloud Map creates when you register an instance and specify this service.

        :default: WEIGHTED for CNAME records and when loadBalancer is true, MULTIVALUE otherwise
        '''
        result = self._values.get("routing_policy")
        return typing.cast(typing.Optional[RoutingPolicy], result)

    @builtins.property
    def namespace(self) -> INamespace:
        '''The namespace that you want to use for DNS configuration.'''
        result = self._values.get("namespace")
        assert result is not None, "Required property 'namespace' is missing"
        return typing.cast(INamespace, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AliasTargetInstance(
    InstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.AliasTargetInstance",
):
    '''Instance that uses Route 53 Alias record type.

    Currently, the only resource types supported are Elastic Load
    Balancers.

    :resource: AWS::ServiceDiscovery::Instance
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        # service: servicediscovery.Service
        
        alias_target_instance = servicediscovery.AliasTargetInstance(self, "MyAliasTargetInstance",
            dns_name="dnsName",
            service=service,
        
            # the properties below are optional
            custom_attributes={
                "custom_attributes_key": "customAttributes"
            },
            instance_id="instanceId"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        dns_name: builtins.str,
        service: IService,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param dns_name: DNS name of the target.
        :param service: The Cloudmap service this resource is registered to.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de2b48a0ad1fec672b49d292857be51abb63013bc416eab7d3c058ad5dba6db)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AliasTargetInstanceProps(
            dns_name=dns_name,
            service=service,
            custom_attributes=custom_attributes,
            instance_id=instance_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="dnsName")
    def dns_name(self) -> builtins.str:
        '''The Route53 DNS name of the alias target.'''
        return typing.cast(builtins.str, jsii.get(self, "dnsName"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Id of the instance.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The Cloudmap service to which the instance is registered.'''
        return typing.cast(IService, jsii.get(self, "service"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-servicediscovery.AliasTargetInstanceProps",
    jsii_struct_bases=[BaseInstanceProps],
    name_mapping={
        "custom_attributes": "customAttributes",
        "instance_id": "instanceId",
        "dns_name": "dnsName",
        "service": "service",
    },
)
class AliasTargetInstanceProps(BaseInstanceProps):
    def __init__(
        self,
        *,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
        dns_name: builtins.str,
        service: IService,
    ) -> None:
        '''
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        :param dns_name: DNS name of the target.
        :param service: The Cloudmap service this resource is registered to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_servicediscovery as servicediscovery
            
            # service: servicediscovery.Service
            
            alias_target_instance_props = servicediscovery.AliasTargetInstanceProps(
                dns_name="dnsName",
                service=service,
            
                # the properties below are optional
                custom_attributes={
                    "custom_attributes_key": "customAttributes"
                },
                instance_id="instanceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c379076a11b5a725cbe8486f4e6a8b4203e0526cfdd3d8668ed972ead032a56)
            check_type(argname="argument custom_attributes", value=custom_attributes, expected_type=type_hints["custom_attributes"])
            check_type(argname="argument instance_id", value=instance_id, expected_type=type_hints["instance_id"])
            check_type(argname="argument dns_name", value=dns_name, expected_type=type_hints["dns_name"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dns_name": dns_name,
            "service": service,
        }
        if custom_attributes is not None:
            self._values["custom_attributes"] = custom_attributes
        if instance_id is not None:
            self._values["instance_id"] = instance_id

    @builtins.property
    def custom_attributes(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Custom attributes of the instance.

        :default: none
        '''
        result = self._values.get("custom_attributes")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def instance_id(self) -> typing.Optional[builtins.str]:
        '''The id of the instance resource.

        :default: Automatically generated name
        '''
        result = self._values.get("instance_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_name(self) -> builtins.str:
        '''DNS name of the target.'''
        result = self._values.get("dns_name")
        assert result is not None, "Required property 'dns_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> IService:
        '''The Cloudmap service this resource is registered to.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(IService, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AliasTargetInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CnameInstance(
    InstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.CnameInstance",
):
    '''Instance that is accessible using a domain name (CNAME).

    :resource: AWS::ServiceDiscovery::Instance
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        # service: servicediscovery.Service
        
        cname_instance = servicediscovery.CnameInstance(self, "MyCnameInstance",
            instance_cname="instanceCname",
            service=service,
        
            # the properties below are optional
            custom_attributes={
                "custom_attributes_key": "customAttributes"
            },
            instance_id="instanceId"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        service: IService,
        instance_cname: builtins.str,
        custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        instance_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param service: The Cloudmap service this resource is registered to.
        :param instance_cname: If the service configuration includes a CNAME record, the domain name that you want Route 53 to return in response to DNS queries, for example, example.com. This value is required if the service specified by ServiceId includes settings for an CNAME record.
        :param custom_attributes: Custom attributes of the instance. Default: none
        :param instance_id: The id of the instance resource. Default: Automatically generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c65602f0c4706fb19199d68fdacd258c5969681a6f3024a6a01c10e08e61f40)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CnameInstanceProps(
            service=service,
            instance_cname=instance_cname,
            custom_attributes=custom_attributes,
            instance_id=instance_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="cname")
    def cname(self) -> builtins.str:
        '''The domain name returned by DNS queries for the instance.'''
        return typing.cast(builtins.str, jsii.get(self, "cname"))

    @builtins.property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> builtins.str:
        '''The Id of the instance.'''
        return typing.cast(builtins.str, jsii.get(self, "instanceId"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> IService:
        '''The Cloudmap service to which the instance is registered.'''
        return typing.cast(IService, jsii.get(self, "service"))


@jsii.interface(jsii_type="@aws-cdk/aws-servicediscovery.IHttpNamespace")
class IHttpNamespace(INamespace, typing_extensions.Protocol):
    pass


class _IHttpNamespaceProxy(
    jsii.proxy_for(INamespace), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-servicediscovery.IHttpNamespace"
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IHttpNamespace).__jsii_proxy_class__ = lambda : _IHttpNamespaceProxy


@jsii.implements(IHttpNamespace)
class HttpNamespace(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-servicediscovery.HttpNamespace",
):
    '''Define an HTTP Namespace.

    :exampleMetadata: lit=test/integ.service-with-http-namespace.lit.ts infused

    Example::

        import aws_cdk.core as cdk
        import aws_cdk.aws_servicediscovery as servicediscovery
        
        app = cdk.App()
        stack = cdk.Stack(app, "aws-servicediscovery-integ")
        
        namespace = servicediscovery.HttpNamespace(stack, "MyNamespace",
            name="covfefe"
        )
        
        service1 = namespace.create_service("NonIpService",
            description="service registering non-ip instances"
        )
        
        service1.register_non_ip_instance("NonIpInstance",
            custom_attributes={"arn": "arn:aws:s3:::mybucket"}
        )
        
        service2 = namespace.create_service("IpService",
            description="service registering ip instances",
            health_check=servicediscovery.HealthCheckConfig(
                type=servicediscovery.HealthCheckType.HTTP,
                resource_path="/check"
            )
        )
        
        service2.register_ip_instance("IpInstance",
            ipv4="54.239.25.192"
        )
        
        app.synth()
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: A name for the Namespace.
        :param description: A description of the Namespace. Default: none
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4038d364bd3aaff03323642be223ee665faf9d23ee5544cceb243e6a301b3f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = HttpNamespaceProps(name=name, description=description)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromHttpNamespaceAttributes")
    @builtins.classmethod
    def from_http_namespace_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        namespace_arn: builtins.str,
        namespace_id: builtins.str,
        namespace_name: builtins.str,
    ) -> IHttpNamespace:
        '''
        :param scope: -
        :param id: -
        :param namespace_arn: Namespace ARN for the Namespace.
        :param namespace_id: Namespace Id for the Namespace.
        :param namespace_name: A name for the Namespace.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b48e13d67f841bc8436cf5479e4e179b73b20ed27ee7d3f0e6a37e8c1c9bb111)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = HttpNamespaceAttributes(
            namespace_arn=namespace_arn,
            namespace_id=namespace_id,
            namespace_name=namespace_name,
        )

        return typing.cast(IHttpNamespace, jsii.sinvoke(cls, "fromHttpNamespaceAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="createService")
    def create_service(
        self,
        id: builtins.str,
        *,
        custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> Service:
        '''Creates a service within the namespace.

        :param id: -
        :param custom_health_check: Structure containing failure threshold for a custom health checker. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. See: https://docs.aws.amazon.com/cloud-map/latest/api/API_HealthCheckCustomConfig.html Default: none
        :param description: A description of the service. Default: none
        :param health_check: Settings for an optional health check. If you specify health check settings, AWS Cloud Map associates the health check with the records that you specify in DnsConfig. Only one of healthCheckConfig or healthCheckCustomConfig can be specified. Not valid for PrivateDnsNamespaces. If you use healthCheck, you can only register IP instances to this service. Default: none
        :param name: A name for the Service. Default: CloudFormation-generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c337572e88313bcfef6d5cab1523a95e06e67edc6bcf56c6c30b01734f3de05)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BaseServiceProps(
            custom_health_check=custom_health_check,
            description=description,
            health_check=health_check,
            name=name,
        )

        return typing.cast(Service, jsii.invoke(self, "createService", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="httpNamespaceArn")
    def http_namespace_arn(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpNamespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="httpNamespaceId")
    def http_namespace_id(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpNamespaceId"))

    @builtins.property
    @jsii.member(jsii_name="httpNamespaceName")
    def http_namespace_name(self) -> builtins.str:
        '''
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "httpNamespaceName"))

    @builtins.property
    @jsii.member(jsii_name="namespaceArn")
    def namespace_arn(self) -> builtins.str:
        '''Namespace Arn for the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceArn"))

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        '''Namespace Id for the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @builtins.property
    @jsii.member(jsii_name="namespaceName")
    def namespace_name(self) -> builtins.str:
        '''A name for the namespace.'''
        return typing.cast(builtins.str, jsii.get(self, "namespaceName"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> NamespaceType:
        '''Type of the namespace.'''
        return typing.cast(NamespaceType, jsii.get(self, "type"))


__all__ = [
    "AliasTargetInstance",
    "AliasTargetInstanceProps",
    "BaseInstanceProps",
    "BaseNamespaceProps",
    "BaseServiceProps",
    "CfnHttpNamespace",
    "CfnHttpNamespaceProps",
    "CfnInstance",
    "CfnInstanceProps",
    "CfnPrivateDnsNamespace",
    "CfnPrivateDnsNamespaceProps",
    "CfnPublicDnsNamespace",
    "CfnPublicDnsNamespaceProps",
    "CfnService",
    "CfnServiceProps",
    "CnameInstance",
    "CnameInstanceBaseProps",
    "CnameInstanceProps",
    "DnsRecordType",
    "DnsServiceProps",
    "HealthCheckConfig",
    "HealthCheckCustomConfig",
    "HealthCheckType",
    "HttpNamespace",
    "HttpNamespaceAttributes",
    "HttpNamespaceProps",
    "IHttpNamespace",
    "IInstance",
    "INamespace",
    "IPrivateDnsNamespace",
    "IPublicDnsNamespace",
    "IService",
    "InstanceBase",
    "IpInstance",
    "IpInstanceBaseProps",
    "IpInstanceProps",
    "NamespaceType",
    "NonIpInstance",
    "NonIpInstanceBaseProps",
    "NonIpInstanceProps",
    "PrivateDnsNamespace",
    "PrivateDnsNamespaceAttributes",
    "PrivateDnsNamespaceProps",
    "PublicDnsNamespace",
    "PublicDnsNamespaceAttributes",
    "PublicDnsNamespaceProps",
    "RoutingPolicy",
    "Service",
    "ServiceAttributes",
    "ServiceProps",
]

publication.publish()

def _typecheckingstub__a583c7464f8c139d8dceb66f956e5eebba623400a7680b46c6ccf75f0444249e(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee522871d4628f82b79f6e596467b8d6ae558a0c0e319cdec7ee0b649b0dd18(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3234580726ea7c1baa9bfb41a16e5e12552a916340e9671bfe9898cdfd467c2f(
    *,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2911f77aa685ed17d42b798cae8b06b1d85a964a2a3b9704aa149b4e01483fd1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610af52d6f2eaf2034ee4c2227daafd04fb1be9474dc54562126efad6fbdab28(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0056dcf9bfeb6b3fe02b1ef2c996c450056757b4d7455f5b464adfcd162622c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d124a27920c5dab8d282baf3e08d222ea680b984dd2bdf123a1321b90595b65(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f910bd79b25571798e6e3fef6b16493f0dc0a0f0153417a120adf22b1211e363(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1a661f1544296619903f44581126a75cda827e9c5cc8b5eb5cb7aab3b9e691(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2dd80dc637822332f087219a98eaeba9a57c808c6087345bd115908f85f852(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    instance_attributes: typing.Any,
    service_id: builtins.str,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f5529a591cdc85f4fe487954fc2490c9c49a6874b81c08e6ed85c2675bae5f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec7f237c5a4deb84df6ec3057ad52dcd2c3db48ee9753218e82e74eb75a3aff(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2597aea5bf8a8df900153f5d55b760439e30ecc44bf1d802f19796b2ee1ea610(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48280bf88ef8c77a1406aeb5ff45c0133556134c24fd6ac63c035ab03c6dabe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20980649ae5374738eeee56d611f3e1b528a15011a1ac7ed7998acedd1098c20(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f66bd527852b58bfda784fbbd343d14bf76e664a0fa0232c509deb73c8ff469a(
    *,
    instance_attributes: typing.Any,
    service_id: builtins.str,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1794382d187fc6030f15b6d87ce7e723479c15363167b200cfa2b0813a9b242e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    vpc: builtins.str,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPrivateDnsNamespace.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06b3a5d1e7e28add33a9c5c817b80bdbcde5add53db88fd6562ce0158e26088(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87c02d4c20283defa1567deaec184b7134d524aa0b192dee99ad16c23af25b5f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c69cb8c4613b4475ff6774ca21118a415444422e0220369b0140e46635cb3b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ec3073d6251823d7958711c3fd808c6c90a3e905985ac21679c1f551ab9d63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38dc8138d7f4d3bbdf045a806a9d0009983b71b2f86a377e71842e210745091b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb06930f8a3d10b38e2259b72cf5a901cb5820c36444c752f76d39275e9135d8(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPrivateDnsNamespace.PropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d9656d93cd4eb5626700402532389d894f3b9f3600d3f6726a17097f802929(
    *,
    soa: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPrivateDnsNamespace.SOAProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c92d0f581d14b979a9eba84f458e99b8f7d047b3b0cf9e62ce1528c7973a0f(
    *,
    dns_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPrivateDnsNamespace.PrivateDnsPropertiesMutableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2424720246f242b6ebc693ab54e03c6869388ea9b7a560bdb3a8ac5480976ee(
    *,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b539a93a0f92851fc3dc947e81944261d1176424ddca25083d29c1385381d4(
    *,
    name: builtins.str,
    vpc: builtins.str,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPrivateDnsNamespace.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2343ad30b0962c71e204183b106a7663df321812f54e73f6173c3d14cf29ab4e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPublicDnsNamespace.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dc84819f5515601e96cb9e7575ee9135fc704506f23eeb67af484f0d953c8d2(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd09b4983469e0bdcd04e47f63e2beacbfe81efadc47514cf8c179a8ce64bf1c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba834a9219d132cfbc9fb02c446a8faab31df58be2b088d1626957058fa3cca6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0672e6797c215b8bfca48131cf43eba5427bdb4700e96c22da7ee25d3de8d8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f361c2dac1ca7d13c6852778184b6b4a1f1939293b89c32ac3a20462c480da1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPublicDnsNamespace.PropertiesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11c5d7144b029acde30dcd0c119e536322e1a812164b9b5c1ff6ddfcab19107b(
    *,
    dns_properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPublicDnsNamespace.PublicDnsPropertiesMutableProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a32b20b6499fe7aa98b60def15629e0fbc0a1192890c1c9f9c6b26b1e106a88(
    *,
    soa: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPublicDnsNamespace.SOAProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f895639c4c1a78d206dfe04b5d8570fda7e7638dc180a39aad413173b005c8(
    *,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__642a04150e405d0273f65a0aae73705b0e8fff3061867b01bc4b665b8672bdb8(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    properties: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPublicDnsNamespace.PropertiesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db652afe83160664aba67161cefe1937d1f0688e65436994223c61ee5cf6600b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    dns_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_custom_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckCustomConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbed11ee98645877be78be36680db1292df4aa7de386942f466c61affc413d8e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30578c47261b37f8529be14614a05b7155b0bf5a533b6abf117a3140fe414c39(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f7a430fb8cfb8860ec3a1700d83427b670914d8f3f61d52a86fd75f4fa53a66(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d8aaa5b9c56a45c8da24bb9bc8e0fc27dbb158b9c58428edb645221e5ae3bdc(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.DnsConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__908c71ea29ec1d8d74a898e932507b91f38c04d0373e1069d485541a626c39ae(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0507e4b3b026b952ba34fe6f767d6886b85297e1fdb4ef2e16a03b0ca04161bf(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.HealthCheckCustomConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6f59696f7c161ca2aba72658ac73d1e276d8d69a0d19edf2916a915e0795bb(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8ac8383f66ffda9394b914e35b199e14c87758c42838304dc2a0523976d0f8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__675d00478c3ea444c1241d56f1a1aff667e5e8bcf41ea08a73c95cbdfa2ed1b9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d76be492073b8754207624aba64c9346c089a9b0b402790859a2d8ca85ed618(
    *,
    dns_records: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsRecordProperty, typing.Dict[builtins.str, typing.Any]]]]],
    namespace_id: typing.Optional[builtins.str] = None,
    routing_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__408ede9864d2517cf4a259e330374b6d9189a768df982c51843a57f64ca034d5(
    *,
    ttl: jsii.Number,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59eb50c9f8bf3b49765ad199e1f6a9813964555c1550233e4808bb3a070570e(
    *,
    type: builtins.str,
    failure_threshold: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468be5abe9af45767370eb3133ab632a9add264b8fed770fdd95186a5030b62c(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1995db71cbce145528bd7d73dbfbe2c6e315a97e0979ebd234a52223fb37a0ec(
    *,
    description: typing.Optional[builtins.str] = None,
    dns_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    health_check_custom_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.HealthCheckCustomConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    namespace_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8cd60f4c551c799d49032e9d51a4c65c89304e1d5c853440c53f438353a1ba(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_cname: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a8eea4c66595a339dbcb97493c30c984ed1d2c9e5bad11bd692ff1c4eeed089(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    instance_cname: builtins.str,
    service: IService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc8eec49cf21e5c49d1905c5f2262d2ba757bfc69a29b34024b589fd594e3fd8(
    *,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    dns_record_type: typing.Optional[DnsRecordType] = None,
    dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancer: typing.Optional[builtins.bool] = None,
    routing_policy: typing.Optional[RoutingPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740cb9890b14bef0e4afa9518502938e853131f225731373de8e6c693ce1a6c2(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
    resource_path: typing.Optional[builtins.str] = None,
    type: typing.Optional[HealthCheckType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0e1c2289eeea083eb366ab7987ed3f41c3d017fa2b0c265081b23f80c438ee(
    *,
    failure_threshold: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9296592640a61e4a041a6552f79232ee4666fe3a7b6c60441456ee61473cadb(
    *,
    namespace_arn: builtins.str,
    namespace_id: builtins.str,
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86268690f595ac7c38e970ab712d550adc8204e21d4bf5d5022743f861df382d(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b20dff37751e51559f2ca8f7af6a30d8128ddde85ba6d29afe2e6a2eb2e47748(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd995cca1ff422abd6c31ccb22564be78c5df0f50d302d9df18c6ce8c26285db(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service: IService,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81afefb2fe8b6b52bdabb4532030f2a86c8b0930910fdf21ec8540c0238f10fb(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__959fdf6a2ae18a3c3c68ca9db3b368d071b1b98ad301decaa72eea88362669f0(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service: IService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d6a03f12a1da2d36be809022e5f0e17953688ff598f743701f37872f27d1fba(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service: IService,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f42d702c99f25a526fa7849b5a2599bb4e7db128d8dda9f66185b480a78b02a9(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21c0501dec47b0c8a855eb3674764cd6275428cb44daad6613649e18672cb92d(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    service: IService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__875ce416a682d118cb431a0a728ed1c03ff81341441798a5e1a24a6c9bb60521(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9b15c9fdbd10190d2d8cfb4ace46db3a6ea27650d5ac975b75e54ddd448936(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace_arn: builtins.str,
    namespace_id: builtins.str,
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1e2262eaaf762390dd6932863b1d386e88c36778cb8e2f510942fc8e8636a9a(
    id: builtins.str,
    *,
    dns_record_type: typing.Optional[DnsRecordType] = None,
    dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancer: typing.Optional[builtins.bool] = None,
    routing_policy: typing.Optional[RoutingPolicy] = None,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b78345ad900e8b49d34f3cdacec708a3c135fa02e0c352ac713b0333991095b0(
    *,
    namespace_arn: builtins.str,
    namespace_id: builtins.str,
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50856db1b872ef8e548826b7dd57a2597afe1a14baf6b4da4232ac483637291(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c908bdc3b29f07272bdb1631fd1619204448b080563553fc6004e4c90270815(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a487cd415447d56b5a16b0dc8ae994e9bb4156cb127cb889277e92797fe676(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace_arn: builtins.str,
    namespace_id: builtins.str,
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e2b9fbf4386f94bdba59e2f99c35dde693199b034202b0278de5e897127ba9(
    id: builtins.str,
    *,
    dns_record_type: typing.Optional[DnsRecordType] = None,
    dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancer: typing.Optional[builtins.bool] = None,
    routing_policy: typing.Optional[RoutingPolicy] = None,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7830336264a79c51f5c874d13efd637c551b66b7f7f97a04577af390048d4d4(
    *,
    namespace_arn: builtins.str,
    namespace_id: builtins.str,
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__178f39ceeaec447d3a507b01c4360dc199e55c93c9232a4c1ba3e772407cdd7c(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b07d6ca9e1a3ddacf7f8ab52d742b896c9ec34ad806e479e9ce3a8630828eb56(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace: INamespace,
    dns_record_type: typing.Optional[DnsRecordType] = None,
    dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancer: typing.Optional[builtins.bool] = None,
    routing_policy: typing.Optional[RoutingPolicy] = None,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9805a230f9f9a8893d95c50f4be7506e2125579659994f48c06af99ab8206cd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dns_record_type: DnsRecordType,
    namespace: INamespace,
    routing_policy: RoutingPolicy,
    service_arn: builtins.str,
    service_id: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c3ab559f7637734c893e5951d9c2780a0577b6fcabb7b62e0648046bb0364ed(
    id: builtins.str,
    *,
    instance_cname: builtins.str,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96e45af0d0161a647590abd9f93fdaa59fd52f0ea21c9f9bf090b79c9b2d7b3a(
    id: builtins.str,
    *,
    ipv4: typing.Optional[builtins.str] = None,
    ipv6: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b932e1c83207129355a1e073c42463df4d7b53431b9bc7cc15554b97fa53699(
    id: builtins.str,
    load_balancer: _aws_cdk_aws_elasticloadbalancingv2_e93c784f.ILoadBalancerV2,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea7cdd9bb1b870d66c2e75244fc5dce982df263ddd0431a0500877f24eae42e(
    id: builtins.str,
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c29c8c4958d6dbe0bea53f64c9ab2645ee9d1de536a88aa9638070bc9399d2da(
    *,
    dns_record_type: DnsRecordType,
    namespace: INamespace,
    routing_policy: RoutingPolicy,
    service_arn: builtins.str,
    service_id: builtins.str,
    service_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8607ad503ffffd20363e36ed518cc1c0e0c0a3b0099ae96129acb71e942162(
    *,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
    dns_record_type: typing.Optional[DnsRecordType] = None,
    dns_ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    load_balancer: typing.Optional[builtins.bool] = None,
    routing_policy: typing.Optional[RoutingPolicy] = None,
    namespace: INamespace,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de2b48a0ad1fec672b49d292857be51abb63013bc416eab7d3c058ad5dba6db(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    dns_name: builtins.str,
    service: IService,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c379076a11b5a725cbe8486f4e6a8b4203e0526cfdd3d8668ed972ead032a56(
    *,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
    dns_name: builtins.str,
    service: IService,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c65602f0c4706fb19199d68fdacd258c5969681a6f3024a6a01c10e08e61f40(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    service: IService,
    instance_cname: builtins.str,
    custom_attributes: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    instance_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4038d364bd3aaff03323642be223ee665faf9d23ee5544cceb243e6a301b3f5(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b48e13d67f841bc8436cf5479e4e179b73b20ed27ee7d3f0e6a37e8c1c9bb111(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    namespace_arn: builtins.str,
    namespace_id: builtins.str,
    namespace_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c337572e88313bcfef6d5cab1523a95e06e67edc6bcf56c6c30b01734f3de05(
    id: builtins.str,
    *,
    custom_health_check: typing.Optional[typing.Union[HealthCheckCustomConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    health_check: typing.Optional[typing.Union[HealthCheckConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
