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


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_iotevents.AlarmModelReference",
    jsii_struct_bases=[],
    name_mapping={},
)
class AlarmModelReference:
    def __init__(self) -> None:
        '''A reference to a AlarmModel resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_iotevents as interfaces_iotevents
            
            alarm_model_reference = interfaces_iotevents.AlarmModelReference()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlarmModelReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_iotevents.DetectorModelReference",
    jsii_struct_bases=[],
    name_mapping={},
)
class DetectorModelReference:
    def __init__(self) -> None:
        '''A reference to a DetectorModel resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_iotevents as interfaces_iotevents
            
            detector_model_reference = interfaces_iotevents.DetectorModelReference()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DetectorModelReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_iotevents.IAlarmModelRef")
class IAlarmModelRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a AlarmModel.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="alarmModelRef")
    def alarm_model_ref(self) -> "AlarmModelReference":
        '''(experimental) A reference to a AlarmModel resource.

        :stability: experimental
        '''
        ...


class _IAlarmModelRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a AlarmModel.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_iotevents.IAlarmModelRef"

    @builtins.property
    @jsii.member(jsii_name="alarmModelRef")
    def alarm_model_ref(self) -> "AlarmModelReference":
        '''(experimental) A reference to a AlarmModel resource.

        :stability: experimental
        '''
        return typing.cast("AlarmModelReference", jsii.get(self, "alarmModelRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAlarmModelRef).__jsii_proxy_class__ = lambda : _IAlarmModelRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_iotevents.IDetectorModelRef")
class IDetectorModelRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a DetectorModel.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="detectorModelRef")
    def detector_model_ref(self) -> "DetectorModelReference":
        '''(experimental) A reference to a DetectorModel resource.

        :stability: experimental
        '''
        ...


class _IDetectorModelRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a DetectorModel.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_iotevents.IDetectorModelRef"

    @builtins.property
    @jsii.member(jsii_name="detectorModelRef")
    def detector_model_ref(self) -> "DetectorModelReference":
        '''(experimental) A reference to a DetectorModel resource.

        :stability: experimental
        '''
        return typing.cast("DetectorModelReference", jsii.get(self, "detectorModelRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDetectorModelRef).__jsii_proxy_class__ = lambda : _IDetectorModelRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_iotevents.IInputRef")
class IInputRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Input.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="inputRef")
    def input_ref(self) -> "InputReference":
        '''(experimental) A reference to a Input resource.

        :stability: experimental
        '''
        ...


class _IInputRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Input.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_iotevents.IInputRef"

    @builtins.property
    @jsii.member(jsii_name="inputRef")
    def input_ref(self) -> "InputReference":
        '''(experimental) A reference to a Input resource.

        :stability: experimental
        '''
        return typing.cast("InputReference", jsii.get(self, "inputRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IInputRef).__jsii_proxy_class__ = lambda : _IInputRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_iotevents.InputReference",
    jsii_struct_bases=[],
    name_mapping={},
)
class InputReference:
    def __init__(self) -> None:
        '''A reference to a Input resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_iotevents as interfaces_iotevents
            
            input_reference = interfaces_iotevents.InputReference()
        '''
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InputReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AlarmModelReference",
    "DetectorModelReference",
    "IAlarmModelRef",
    "IDetectorModelRef",
    "IInputRef",
    "InputReference",
]

publication.publish()

for cls in [IAlarmModelRef, IDetectorModelRef, IInputRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
