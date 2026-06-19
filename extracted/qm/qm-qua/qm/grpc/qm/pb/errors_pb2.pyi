from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class JobManagerErrorTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    JobManagerUnspecifiedError: _ClassVar[JobManagerErrorTypes]
    MissingJobError: _ClassVar[JobManagerErrorTypes]
    InvalidJobExecutionStatusError: _ClassVar[JobManagerErrorTypes]
    InvalidOperationOnSimulatorJobError: _ClassVar[JobManagerErrorTypes]
    InvalidOperationOnRealJobError: _ClassVar[JobManagerErrorTypes]
    JobOperationSpecificError: _ClassVar[JobManagerErrorTypes]
    ConfigQueryError: _ClassVar[JobManagerErrorTypes]
    UnknownInputStreamError: _ClassVar[JobManagerErrorTypes]

class JobOperationSpecificErrorTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    JobOperationUnspecifiedError: _ClassVar[JobOperationSpecificErrorTypes]
    SingleInputElementError: _ClassVar[JobOperationSpecificErrorTypes]
    InvalidCorrectionMatrixError: _ClassVar[JobOperationSpecificErrorTypes]
    ElementWithoutIntermediateFrequencyError: _ClassVar[JobOperationSpecificErrorTypes]
    InvalidDigitalInputThresholdError: _ClassVar[JobOperationSpecificErrorTypes]
    InvalidDigitalInputDeadtimeError: _ClassVar[JobOperationSpecificErrorTypes]
    InvalidDigitalInputPolarityError: _ClassVar[JobOperationSpecificErrorTypes]

class ConfigQueryErrorTypes(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    ConfigQueryUnspecifiedError: _ClassVar[ConfigQueryErrorTypes]
    MissingControllerError: _ClassVar[ConfigQueryErrorTypes]
    MissingElementError: _ClassVar[ConfigQueryErrorTypes]
    MissingDigitalInputError: _ClassVar[ConfigQueryErrorTypes]
JobManagerUnspecifiedError: JobManagerErrorTypes
MissingJobError: JobManagerErrorTypes
InvalidJobExecutionStatusError: JobManagerErrorTypes
InvalidOperationOnSimulatorJobError: JobManagerErrorTypes
InvalidOperationOnRealJobError: JobManagerErrorTypes
JobOperationSpecificError: JobManagerErrorTypes
ConfigQueryError: JobManagerErrorTypes
UnknownInputStreamError: JobManagerErrorTypes
JobOperationUnspecifiedError: JobOperationSpecificErrorTypes
SingleInputElementError: JobOperationSpecificErrorTypes
InvalidCorrectionMatrixError: JobOperationSpecificErrorTypes
ElementWithoutIntermediateFrequencyError: JobOperationSpecificErrorTypes
InvalidDigitalInputThresholdError: JobOperationSpecificErrorTypes
InvalidDigitalInputDeadtimeError: JobOperationSpecificErrorTypes
InvalidDigitalInputPolarityError: JobOperationSpecificErrorTypes
ConfigQueryUnspecifiedError: ConfigQueryErrorTypes
MissingControllerError: ConfigQueryErrorTypes
MissingElementError: ConfigQueryErrorTypes
MissingDigitalInputError: ConfigQueryErrorTypes
