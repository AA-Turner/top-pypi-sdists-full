r'''
# AWS::NetworkMonitor Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_networkmonitor as networkmonitor
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for NetworkMonitor construct libraries](https://constructs.dev/search?q=networkmonitor)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::NetworkMonitor resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkMonitor.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::NetworkMonitor](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkMonitor.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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


from .._jsii import *

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

    import aws_cdk as _aws_cdk_0cae9daa
    import aws_cdk.interfaces.aws_networkmonitor as _aws_networkmonitor_df4af559
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_networkmonitor_df4af559 = _LazyImport("aws_cdk.interfaces.aws_networkmonitor")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networkmonitor_df4af559.IMonitorRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnMonitor(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmonitor.CfnMonitor",
):
    '''An Amazon CloudWatch Network Monitor resource that monitors network traffic between a source VPC subnet and a destination IP address.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-monitor.html
    :cloudformationResource: AWS::NetworkMonitor::Monitor
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networkmonitor as networkmonitor
        
        cfn_monitor = networkmonitor.CfnMonitor(self, "MyCfnMonitor",
            monitor_name="monitorName",
        
            # the properties below are optional
            aggregation_period=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        monitor_name: builtins.str,
        aggregation_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkMonitor::Monitor``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param monitor_name: The name identifying the monitor. It can contain only letters, underscores (_), or dashes (-), and can be up to 200 characters.
        :param aggregation_period: The time, in seconds, that metrics are aggregated and sent to Amazon CloudWatch. Valid values are either 30 or 60.
        :param tags: The tags for the monitor.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5c0f9045c078ffb6c8076e92b53faacc060d04ef6dd51f97813a90199ea252d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMonitorProps(
            monitor_name=monitor_name, aggregation_period=aggregation_period, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForMonitor")
    @builtins.classmethod
    def arn_for_monitor(
        cls,
        resource: "_aws_networkmonitor_df4af559.IMonitorRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e1475c86246c9406dce5c842111362fc36c48d41fa5d2c8b8d804a5ddd801dae)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForMonitor", [resource]))

    @jsii.member(jsii_name="isCfnMonitor")
    @builtins.classmethod
    def is_cfn_monitor(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnMonitor.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0bf12328a1edb716e08ab3792eb29858af5c78334b15e767b8bfc318f4666a8f)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnMonitor", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d5bd4b00385986fcd728f62e1f738b5dee9fb5089d5892e5e2455c8e98518eb6)
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
            type_hints = cached_type_hints(_typecheckingstub__463970bf73c636fa0e5910ed6354d53a72768527ff9cf29ed5e9e3d74e00032c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time and date when the monitor was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedAt")
    def attr_modified_at(self) -> builtins.str:
        '''The time and date when the monitor was last modified.

        :cloudformationAttribute: ModifiedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrMonitorArn")
    def attr_monitor_arn(self) -> builtins.str:
        '''The ARN of the monitor.

        :cloudformationAttribute: MonitorArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMonitorArn"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the monitor.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="monitorRef")
    def monitor_ref(self) -> "_aws_networkmonitor_df4af559.MonitorReference":
        '''A reference to a Monitor resource.'''
        return typing.cast("_aws_networkmonitor_df4af559.MonitorReference", jsii.get(self, "monitorRef"))

    @builtins.property
    @jsii.member(jsii_name="monitorName")
    def monitor_name(self) -> builtins.str:
        '''The name identifying the monitor.'''
        return typing.cast(builtins.str, jsii.get(self, "monitorName"))

    @monitor_name.setter
    def monitor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e322d44376a19c92cbb57448249fbd6743ef2029acb5ba3c305096a6864eb8f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorName", value)

    @builtins.property
    @jsii.member(jsii_name="aggregationPeriod")
    def aggregation_period(self) -> typing.Optional[jsii.Number]:
        '''The time, in seconds, that metrics are aggregated and sent to Amazon CloudWatch.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "aggregationPeriod"))

    @aggregation_period.setter
    def aggregation_period(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c64184b589f3340850d3ee7f2a5a37958ff23c484d62174a3c9fcbfa50ba148e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregationPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the monitor.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d328784c5c619237cb7a9a210ca3934769a878b90d2199dc0c70768cc0e337c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmonitor.CfnMonitorProps",
    jsii_struct_bases=[],
    name_mapping={
        "monitor_name": "monitorName",
        "aggregation_period": "aggregationPeriod",
        "tags": "tags",
    },
)
class CfnMonitorProps:
    def __init__(
        self,
        *,
        monitor_name: builtins.str,
        aggregation_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnMonitor``.

        :param monitor_name: The name identifying the monitor. It can contain only letters, underscores (_), or dashes (-), and can be up to 200 characters.
        :param aggregation_period: The time, in seconds, that metrics are aggregated and sent to Amazon CloudWatch. Valid values are either 30 or 60.
        :param tags: The tags for the monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-monitor.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networkmonitor as networkmonitor
            
            cfn_monitor_props = networkmonitor.CfnMonitorProps(
                monitor_name="monitorName",
            
                # the properties below are optional
                aggregation_period=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e34e6f340189f7c3f3a8eb57768286262e76793d7bf3d7c567aeaecac2562b7f)
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument aggregation_period", value=aggregation_period, expected_type=type_hints["aggregation_period"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_name": monitor_name,
        }
        if aggregation_period is not None:
            self._values["aggregation_period"] = aggregation_period
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def monitor_name(self) -> builtins.str:
        '''The name identifying the monitor.

        It can contain only letters, underscores (_), or dashes (-), and can be up to 200 characters.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-monitor.html#cfn-networkmonitor-monitor-monitorname
        '''
        result = self._values.get("monitor_name")
        assert result is not None, "Required property 'monitor_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def aggregation_period(self) -> typing.Optional[jsii.Number]:
        '''The time, in seconds, that metrics are aggregated and sent to Amazon CloudWatch.

        Valid values are either 30 or 60.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-monitor.html#cfn-networkmonitor-monitor-aggregationperiod
        '''
        result = self._values.get("aggregation_period")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the monitor.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-monitor.html#cfn-networkmonitor-monitor-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMonitorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_networkmonitor_df4af559.IProbeRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnProbe(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_networkmonitor.CfnProbe",
):
    '''An Amazon CloudWatch Network Monitor probe that measures network traffic between a source subnet and a destination.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html
    :cloudformationResource: AWS::NetworkMonitor::Probe
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_networkmonitor as networkmonitor
        
        cfn_probe = networkmonitor.CfnProbe(self, "MyCfnProbe",
            destination="destination",
            monitor_name="monitorName",
            protocol="protocol",
            source_arn="sourceArn",
        
            # the properties below are optional
            destination_port=123,
            packet_size=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        destination: builtins.str,
        monitor_name: builtins.str,
        protocol: builtins.str,
        source_arn: builtins.str,
        destination_port: typing.Optional[jsii.Number] = None,
        packet_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkMonitor::Probe``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param destination: The literal IPv4 or IPv6 address the probe sends traffic to. The service rejects a domain name and a CIDR block.
        :param monitor_name: The name of the monitor the probe belongs to.
        :param protocol: The protocol the probe uses.
        :param source_arn: The ARN of the subnet the probe sends traffic from.
        :param destination_port: The port the probe sends traffic to. Applies to the TCP protocol only.
        :param packet_size: The size, in bytes, of the packets the probe sends.
        :param tags: The tags for the probe.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__25521dff807a2f28b2568db30ed144748c59fa22b844aabec47fe0b15f03de4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProbeProps(
            destination=destination,
            monitor_name=monitor_name,
            protocol=protocol,
            source_arn=source_arn,
            destination_port=destination_port,
            packet_size=packet_size,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForProbe")
    @builtins.classmethod
    def arn_for_probe(
        cls,
        resource: "_aws_networkmonitor_df4af559.IProbeRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c12ca134be3ac13a3a8c0c0820d09fe9ca6a66a812ac1faf9e7d610e180f7fcc)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForProbe", [resource]))

    @jsii.member(jsii_name="isCfnProbe")
    @builtins.classmethod
    def is_cfn_probe(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnProbe.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f9a76bf93daa89cd79e48b22260eb9cbc1917c5359eaaf3b70a83644dbebf665)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnProbe", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__08e984afb31e03386f7d88ae78a85cbb8b12ce2cdb4597a2fed2d7d4b9c6970d)
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
            type_hints = cached_type_hints(_typecheckingstub__35f7bc2d57356b22fec40d137fe9d553960ae78a97642535af0bfab8b3498490)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAddressFamily")
    def attr_address_family(self) -> builtins.str:
        '''The IP address family the probe uses, computed by the service from the source and destination.

        :cloudformationAttribute: AddressFamily
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAddressFamily"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The time and date when the probe was created.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrModifiedAt")
    def attr_modified_at(self) -> builtins.str:
        '''The time and date when the probe was last modified.

        :cloudformationAttribute: ModifiedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModifiedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrProbeArn")
    def attr_probe_arn(self) -> builtins.str:
        '''The ARN of the probe.

        :cloudformationAttribute: ProbeArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProbeArn"))

    @builtins.property
    @jsii.member(jsii_name="attrProbeId")
    def attr_probe_id(self) -> builtins.str:
        '''The ID of the probe.

        :cloudformationAttribute: ProbeId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrProbeId"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the probe.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcId")
    def attr_vpc_id(self) -> builtins.str:
        '''The ID of the VPC containing the probe's source subnet.

        :cloudformationAttribute: VpcId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcId"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="probeRef")
    def probe_ref(self) -> "_aws_networkmonitor_df4af559.ProbeReference":
        '''A reference to a Probe resource.'''
        return typing.cast("_aws_networkmonitor_df4af559.ProbeReference", jsii.get(self, "probeRef"))

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> builtins.str:
        '''The literal IPv4 or IPv6 address the probe sends traffic to.'''
        return typing.cast(builtins.str, jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__096c05cdde04ce513067b48a02f748ae370f9974593ed71b6d4c1c7720aabf10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value)

    @builtins.property
    @jsii.member(jsii_name="monitorName")
    def monitor_name(self) -> builtins.str:
        '''The name of the monitor the probe belongs to.'''
        return typing.cast(builtins.str, jsii.get(self, "monitorName"))

    @monitor_name.setter
    def monitor_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f18bf6e542f6bce2dd1ed854cc3a7c7e7c29ea817fdc0cb7f14ca0490f00085d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitorName", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''The protocol the probe uses.'''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e1a0c643baa5cd3fed763f732d08b1f195e913fb27db36150d055a09fb6861e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="sourceArn")
    def source_arn(self) -> builtins.str:
        '''The ARN of the subnet the probe sends traffic from.'''
        return typing.cast(builtins.str, jsii.get(self, "sourceArn"))

    @source_arn.setter
    def source_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__42ea8ffb8bd2930af8e9c5e9decbe1ab39a13691b51bf0d9eae8b0e1ef4e52cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceArn", value)

    @builtins.property
    @jsii.member(jsii_name="destinationPort")
    def destination_port(self) -> typing.Optional[jsii.Number]:
        '''The port the probe sends traffic to.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "destinationPort"))

    @destination_port.setter
    def destination_port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__876091db6e260d683702ce29b331ebc83f0db087b211369b1ae980c05399349f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationPort", value)

    @builtins.property
    @jsii.member(jsii_name="packetSize")
    def packet_size(self) -> typing.Optional[jsii.Number]:
        '''The size, in bytes, of the packets the probe sends.'''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "packetSize"))

    @packet_size.setter
    def packet_size(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2417615837d8d88ea72163f756f3b529eccb37c7eaaf99cf536cc987c1826dd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "packetSize", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the probe.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3a7518b9558a94eb278e9a15cf90bc5e17a4bd847c791603a4e378e6da41e12c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_networkmonitor.CfnProbeProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "monitor_name": "monitorName",
        "protocol": "protocol",
        "source_arn": "sourceArn",
        "destination_port": "destinationPort",
        "packet_size": "packetSize",
        "tags": "tags",
    },
)
class CfnProbeProps:
    def __init__(
        self,
        *,
        destination: builtins.str,
        monitor_name: builtins.str,
        protocol: builtins.str,
        source_arn: builtins.str,
        destination_port: typing.Optional[jsii.Number] = None,
        packet_size: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProbe``.

        :param destination: The literal IPv4 or IPv6 address the probe sends traffic to. The service rejects a domain name and a CIDR block.
        :param monitor_name: The name of the monitor the probe belongs to.
        :param protocol: The protocol the probe uses.
        :param source_arn: The ARN of the subnet the probe sends traffic from.
        :param destination_port: The port the probe sends traffic to. Applies to the TCP protocol only.
        :param packet_size: The size, in bytes, of the packets the probe sends.
        :param tags: The tags for the probe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_networkmonitor as networkmonitor
            
            cfn_probe_props = networkmonitor.CfnProbeProps(
                destination="destination",
                monitor_name="monitorName",
                protocol="protocol",
                source_arn="sourceArn",
            
                # the properties below are optional
                destination_port=123,
                packet_size=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c53fbb38c8cea7f24dc37c41eb66032668dda555fa9b6b78cff0a8074f55fe9d)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
            check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
            check_type(argname="argument packet_size", value=packet_size, expected_type=type_hints["packet_size"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination": destination,
            "monitor_name": monitor_name,
            "protocol": protocol,
            "source_arn": source_arn,
        }
        if destination_port is not None:
            self._values["destination_port"] = destination_port
        if packet_size is not None:
            self._values["packet_size"] = packet_size
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination(self) -> builtins.str:
        '''The literal IPv4 or IPv6 address the probe sends traffic to.

        The service rejects a domain name and a CIDR block.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-destination
        '''
        result = self._values.get("destination")
        assert result is not None, "Required property 'destination' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def monitor_name(self) -> builtins.str:
        '''The name of the monitor the probe belongs to.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-monitorname
        '''
        result = self._values.get("monitor_name")
        assert result is not None, "Required property 'monitor_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The protocol the probe uses.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_arn(self) -> builtins.str:
        '''The ARN of the subnet the probe sends traffic from.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-sourcearn
        '''
        result = self._values.get("source_arn")
        assert result is not None, "Required property 'source_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def destination_port(self) -> typing.Optional[jsii.Number]:
        '''The port the probe sends traffic to.

        Applies to the TCP protocol only.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-destinationport
        '''
        result = self._values.get("destination_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def packet_size(self) -> typing.Optional[jsii.Number]:
        '''The size, in bytes, of the packets the probe sends.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-packetsize
        '''
        result = self._values.get("packet_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags for the probe.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkmonitor-probe.html#cfn-networkmonitor-probe-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProbeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMonitor",
    "CfnMonitorProps",
    "CfnProbe",
    "CfnProbeProps",
]

publication.publish()

def _typecheckingstub__5c0f9045c078ffb6c8076e92b53faacc060d04ef6dd51f97813a90199ea252d6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    monitor_name: builtins.str,
    aggregation_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1475c86246c9406dce5c842111362fc36c48d41fa5d2c8b8d804a5ddd801dae(
    resource: _aws_networkmonitor_df4af559.IMonitorRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf12328a1edb716e08ab3792eb29858af5c78334b15e767b8bfc318f4666a8f(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5bd4b00385986fcd728f62e1f738b5dee9fb5089d5892e5e2455c8e98518eb6(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463970bf73c636fa0e5910ed6354d53a72768527ff9cf29ed5e9e3d74e00032c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e322d44376a19c92cbb57448249fbd6743ef2029acb5ba3c305096a6864eb8f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64184b589f3340850d3ee7f2a5a37958ff23c484d62174a3c9fcbfa50ba148e(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d328784c5c619237cb7a9a210ca3934769a878b90d2199dc0c70768cc0e337c9(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e34e6f340189f7c3f3a8eb57768286262e76793d7bf3d7c567aeaecac2562b7f(
    *,
    monitor_name: builtins.str,
    aggregation_period: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25521dff807a2f28b2568db30ed144748c59fa22b844aabec47fe0b15f03de4b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    destination: builtins.str,
    monitor_name: builtins.str,
    protocol: builtins.str,
    source_arn: builtins.str,
    destination_port: typing.Optional[jsii.Number] = None,
    packet_size: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c12ca134be3ac13a3a8c0c0820d09fe9ca6a66a812ac1faf9e7d610e180f7fcc(
    resource: _aws_networkmonitor_df4af559.IProbeRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9a76bf93daa89cd79e48b22260eb9cbc1917c5359eaaf3b70a83644dbebf665(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e984afb31e03386f7d88ae78a85cbb8b12ce2cdb4597a2fed2d7d4b9c6970d(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f7bc2d57356b22fec40d137fe9d553960ae78a97642535af0bfab8b3498490(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096c05cdde04ce513067b48a02f748ae370f9974593ed71b6d4c1c7720aabf10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18bf6e542f6bce2dd1ed854cc3a7c7e7c29ea817fdc0cb7f14ca0490f00085d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1a0c643baa5cd3fed763f732d08b1f195e913fb27db36150d055a09fb6861e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ea8ffb8bd2930af8e9c5e9decbe1ab39a13691b51bf0d9eae8b0e1ef4e52cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876091db6e260d683702ce29b331ebc83f0db087b211369b1ae980c05399349f(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2417615837d8d88ea72163f756f3b529eccb37c7eaaf99cf536cc987c1826dd2(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a7518b9558a94eb278e9a15cf90bc5e17a4bd847c791603a4e378e6da41e12c(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53fbb38c8cea7f24dc37c41eb66032668dda555fa9b6b78cff0a8074f55fe9d(
    *,
    destination: builtins.str,
    monitor_name: builtins.str,
    protocol: builtins.str,
    source_arn: builtins.str,
    destination_port: typing.Optional[jsii.Number] = None,
    packet_size: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
