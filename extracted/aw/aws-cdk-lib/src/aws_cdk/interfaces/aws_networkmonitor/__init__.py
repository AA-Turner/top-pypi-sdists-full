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


from ..._jsii import *

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

    import aws_cdk.interfaces as _interfaces_8ca7e747
    import constructs as _constructs_77d1e7e8
else:

    _constructs_77d1e7e8 = _LazyImport("constructs")
    _interfaces_8ca7e747 = _LazyImport("aws_cdk.interfaces")


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_networkmonitor.IMonitorRef")
class IMonitorRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Monitor.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="monitorRef")
    def monitor_ref(self) -> "MonitorReference":
        '''(experimental) A reference to a Monitor resource.

        :stability: experimental
        '''
        ...


class _IMonitorRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Monitor.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networkmonitor.IMonitorRef"

    @builtins.property
    @jsii.member(jsii_name="monitorRef")
    def monitor_ref(self) -> "MonitorReference":
        '''(experimental) A reference to a Monitor resource.

        :stability: experimental
        '''
        return typing.cast("MonitorReference", jsii.get(self, "monitorRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IMonitorRef).__jsii_proxy_class__ = lambda : _IMonitorRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_networkmonitor.IProbeRef")
class IProbeRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Probe.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="probeRef")
    def probe_ref(self) -> "ProbeReference":
        '''(experimental) A reference to a Probe resource.

        :stability: experimental
        '''
        ...


class _IProbeRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Probe.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_networkmonitor.IProbeRef"

    @builtins.property
    @jsii.member(jsii_name="probeRef")
    def probe_ref(self) -> "ProbeReference":
        '''(experimental) A reference to a Probe resource.

        :stability: experimental
        '''
        return typing.cast("ProbeReference", jsii.get(self, "probeRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProbeRef).__jsii_proxy_class__ = lambda : _IProbeRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networkmonitor.MonitorReference",
    jsii_struct_bases=[],
    name_mapping={"monitor_arn": "monitorArn"},
)
class MonitorReference:
    def __init__(self, *, monitor_arn: builtins.str) -> None:
        '''A reference to a Monitor resource.

        :param monitor_arn: The MonitorArn of the Monitor resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networkmonitor as interfaces_networkmonitor
            
            monitor_reference = interfaces_networkmonitor.MonitorReference(
                monitor_arn="monitorArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__cafa1141323f6571193f70f0b16663b17e9968df11caf6329223990b8d4f7ee0)
            check_type(argname="argument monitor_arn", value=monitor_arn, expected_type=type_hints["monitor_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_arn": monitor_arn,
        }

    @builtins.property
    def monitor_arn(self) -> builtins.str:
        '''The MonitorArn of the Monitor resource.'''
        result = self._values.get("monitor_arn")
        assert result is not None, "Required property 'monitor_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_networkmonitor.ProbeReference",
    jsii_struct_bases=[],
    name_mapping={
        "monitor_name": "monitorName",
        "probe_arn": "probeArn",
        "probe_id": "probeId",
    },
)
class ProbeReference:
    def __init__(
        self,
        *,
        monitor_name: builtins.str,
        probe_arn: builtins.str,
        probe_id: builtins.str,
    ) -> None:
        '''A reference to a Probe resource.

        :param monitor_name: The MonitorName of the Probe resource.
        :param probe_arn: The ARN of the Probe resource.
        :param probe_id: The ProbeId of the Probe resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_networkmonitor as interfaces_networkmonitor
            
            probe_reference = interfaces_networkmonitor.ProbeReference(
                monitor_name="monitorName",
                probe_arn="probeArn",
                probe_id="probeId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ba6763f50cdc1688b04483abac0fb6344c872344376cb045e8b8c7b4b8b9c399)
            check_type(argname="argument monitor_name", value=monitor_name, expected_type=type_hints["monitor_name"])
            check_type(argname="argument probe_arn", value=probe_arn, expected_type=type_hints["probe_arn"])
            check_type(argname="argument probe_id", value=probe_id, expected_type=type_hints["probe_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "monitor_name": monitor_name,
            "probe_arn": probe_arn,
            "probe_id": probe_id,
        }

    @builtins.property
    def monitor_name(self) -> builtins.str:
        '''The MonitorName of the Probe resource.'''
        result = self._values.get("monitor_name")
        assert result is not None, "Required property 'monitor_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def probe_arn(self) -> builtins.str:
        '''The ARN of the Probe resource.'''
        result = self._values.get("probe_arn")
        assert result is not None, "Required property 'probe_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def probe_id(self) -> builtins.str:
        '''The ProbeId of the Probe resource.'''
        result = self._values.get("probe_id")
        assert result is not None, "Required property 'probe_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProbeReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IMonitorRef",
    "IProbeRef",
    "MonitorReference",
    "ProbeReference",
]

publication.publish()

def _typecheckingstub__cafa1141323f6571193f70f0b16663b17e9968df11caf6329223990b8d4f7ee0(
    *,
    monitor_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba6763f50cdc1688b04483abac0fb6344c872344376cb045e8b8c7b4b8b9c399(
    *,
    monitor_name: builtins.str,
    probe_arn: builtins.str,
    probe_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IMonitorRef, IProbeRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
