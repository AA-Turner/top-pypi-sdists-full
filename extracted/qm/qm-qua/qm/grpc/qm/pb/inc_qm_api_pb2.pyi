from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from qm.grpc.qm.pb import general_messages_pb2 as _general_messages_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DigitalInputPortPolarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    RISING: _ClassVar[DigitalInputPortPolarity]
    FALLING: _ClassVar[DigitalInputPortPolarity]
RISING: DigitalInputPortPolarity
FALLING: DigitalInputPortPolarity

class HighQmApiRequest(_message.Message):
    __slots__ = ["config", "strongConfig", "quantumMachineId", "setCorrection", "setFrequency", "setDcOffset", "setDigitalRoute", "setIOValues", "setInputDcOffset", "setOutputDcOffset", "setOutputFilterTaps", "setDigitalInputThreshold", "setDigitalInputDeadtime", "setDigitalInputPolarity"]
    class SetCorrection(_message.Message):
        __slots__ = ["correction", "qe", "mixer"]
        CORRECTION_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        MIXER_FIELD_NUMBER: _ClassVar[int]
        correction: Matrix
        qe: str
        mixer: HighQmApiRequest.SetCorrectionMixerInfo
        def __init__(self, correction: _Optional[_Union[Matrix, _Mapping]] = ..., qe: _Optional[str] = ..., mixer: _Optional[_Union[HighQmApiRequest.SetCorrectionMixerInfo, _Mapping]] = ...) -> None: ...
    class SetCorrectionMixerInfo(_message.Message):
        __slots__ = ["mixer", "intermediateFrequency", "loFrequency", "frequencyNegative", "intermediateFrequencyDouble", "loFrequencyDouble"]
        MIXER_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        FREQUENCYNEGATIVE_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        mixer: str
        intermediateFrequency: int
        loFrequency: int
        frequencyNegative: bool
        intermediateFrequencyDouble: float
        loFrequencyDouble: float
        def __init__(self, mixer: _Optional[str] = ..., intermediateFrequency: _Optional[int] = ..., loFrequency: _Optional[int] = ..., frequencyNegative: bool = ..., intermediateFrequencyDouble: _Optional[float] = ..., loFrequencyDouble: _Optional[float] = ...) -> None: ...
    class SetFrequency(_message.Message):
        __slots__ = ["value", "qe"]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        value: float
        qe: str
        def __init__(self, value: _Optional[float] = ..., qe: _Optional[str] = ...) -> None: ...
    class SetDcOffset(_message.Message):
        __slots__ = ["I", "Q", "qe"]
        I_FIELD_NUMBER: _ClassVar[int]
        Q_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        I: float
        Q: float
        qe: HighQmApiRequest.QePort
        def __init__(self, I: _Optional[float] = ..., Q: _Optional[float] = ..., qe: _Optional[_Union[HighQmApiRequest.QePort, _Mapping]] = ...) -> None: ...
    class SetOutputDcOffset(_message.Message):
        __slots__ = ["I", "Q", "qe"]
        I_FIELD_NUMBER: _ClassVar[int]
        Q_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        I: float
        Q: float
        qe: HighQmApiRequest.QePort
        def __init__(self, I: _Optional[float] = ..., Q: _Optional[float] = ..., qe: _Optional[_Union[HighQmApiRequest.QePort, _Mapping]] = ...) -> None: ...
    class SetOutputFilterTaps(_message.Message):
        __slots__ = ["filter", "qe"]
        FILTER_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        filter: HighQmApiRequest.AnalogOutputPortFilter
        qe: HighQmApiRequest.QePort
        def __init__(self, filter: _Optional[_Union[HighQmApiRequest.AnalogOutputPortFilter, _Mapping]] = ..., qe: _Optional[_Union[HighQmApiRequest.QePort, _Mapping]] = ...) -> None: ...
    class AnalogOutputPortFilter(_message.Message):
        __slots__ = ["feedforward", "feedback"]
        FEEDFORWARD_FIELD_NUMBER: _ClassVar[int]
        FEEDBACK_FIELD_NUMBER: _ClassVar[int]
        feedforward: _containers.RepeatedScalarFieldContainer[float]
        feedback: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, feedforward: _Optional[_Iterable[float]] = ..., feedback: _Optional[_Iterable[float]] = ...) -> None: ...
    class SetInputDcOffset(_message.Message):
        __slots__ = ["offset", "qe"]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        offset: float
        qe: HighQmApiRequest.QePort
        def __init__(self, offset: _Optional[float] = ..., qe: _Optional[_Union[HighQmApiRequest.QePort, _Mapping]] = ...) -> None: ...
    class SetDigitalRoute(_message.Message):
        __slots__ = ["value", "delay", "buffer", "tof", "smearing"]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        DELAY_FIELD_NUMBER: _ClassVar[int]
        BUFFER_FIELD_NUMBER: _ClassVar[int]
        TOF_FIELD_NUMBER: _ClassVar[int]
        SMEARING_FIELD_NUMBER: _ClassVar[int]
        value: int
        delay: HighQmApiRequest.QePort
        buffer: HighQmApiRequest.QePort
        tof: str
        smearing: str
        def __init__(self, value: _Optional[int] = ..., delay: _Optional[_Union[HighQmApiRequest.QePort, _Mapping]] = ..., buffer: _Optional[_Union[HighQmApiRequest.QePort, _Mapping]] = ..., tof: _Optional[str] = ..., smearing: _Optional[str] = ...) -> None: ...
    class SetIOValues(_message.Message):
        __slots__ = ["all", "ioValueSetData"]
        ALL_FIELD_NUMBER: _ClassVar[int]
        IOVALUESETDATA_FIELD_NUMBER: _ClassVar[int]
        all: bool
        ioValueSetData: _containers.RepeatedCompositeFieldContainer[HighQmApiRequest.IOValueSetData]
        def __init__(self, all: bool = ..., ioValueSetData: _Optional[_Iterable[_Union[HighQmApiRequest.IOValueSetData, _Mapping]]] = ...) -> None: ...
    class QePort(_message.Message):
        __slots__ = ["qe", "port"]
        QE_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        qe: str
        port: str
        def __init__(self, qe: _Optional[str] = ..., port: _Optional[str] = ...) -> None: ...
    class IOValueSetData(_message.Message):
        __slots__ = ["io_number", "intValue", "doubleValue", "booleanValue"]
        IO_NUMBER_FIELD_NUMBER: _ClassVar[int]
        INTVALUE_FIELD_NUMBER: _ClassVar[int]
        DOUBLEVALUE_FIELD_NUMBER: _ClassVar[int]
        BOOLEANVALUE_FIELD_NUMBER: _ClassVar[int]
        io_number: int
        intValue: int
        doubleValue: float
        booleanValue: bool
        def __init__(self, io_number: _Optional[int] = ..., intValue: _Optional[int] = ..., doubleValue: _Optional[float] = ..., booleanValue: bool = ...) -> None: ...
    class SetDigitalInputThreshold(_message.Message):
        __slots__ = ["digitalPort", "threshold"]
        DIGITALPORT_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        digitalPort: DigitalInputPort
        threshold: float
        def __init__(self, digitalPort: _Optional[_Union[DigitalInputPort, _Mapping]] = ..., threshold: _Optional[float] = ...) -> None: ...
    class SetDigitalInputPolarity(_message.Message):
        __slots__ = ["digitalPort", "polarity"]
        DIGITALPORT_FIELD_NUMBER: _ClassVar[int]
        POLARITY_FIELD_NUMBER: _ClassVar[int]
        digitalPort: DigitalInputPort
        polarity: DigitalInputPortPolarity
        def __init__(self, digitalPort: _Optional[_Union[DigitalInputPort, _Mapping]] = ..., polarity: _Optional[_Union[DigitalInputPortPolarity, str]] = ...) -> None: ...
    class SetDigitalInputDeadtime(_message.Message):
        __slots__ = ["digitalPort", "deadtime"]
        DIGITALPORT_FIELD_NUMBER: _ClassVar[int]
        DEADTIME_FIELD_NUMBER: _ClassVar[int]
        digitalPort: DigitalInputPort
        deadtime: int
        def __init__(self, digitalPort: _Optional[_Union[DigitalInputPort, _Mapping]] = ..., deadtime: _Optional[int] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    STRONGCONFIG_FIELD_NUMBER: _ClassVar[int]
    QUANTUMMACHINEID_FIELD_NUMBER: _ClassVar[int]
    SETCORRECTION_FIELD_NUMBER: _ClassVar[int]
    SETFREQUENCY_FIELD_NUMBER: _ClassVar[int]
    SETDCOFFSET_FIELD_NUMBER: _ClassVar[int]
    SETDIGITALROUTE_FIELD_NUMBER: _ClassVar[int]
    SETIOVALUES_FIELD_NUMBER: _ClassVar[int]
    SETINPUTDCOFFSET_FIELD_NUMBER: _ClassVar[int]
    SETOUTPUTDCOFFSET_FIELD_NUMBER: _ClassVar[int]
    SETOUTPUTFILTERTAPS_FIELD_NUMBER: _ClassVar[int]
    SETDIGITALINPUTTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
    SETDIGITALINPUTDEADTIME_FIELD_NUMBER: _ClassVar[int]
    SETDIGITALINPUTPOLARITY_FIELD_NUMBER: _ClassVar[int]
    config: QmConfig
    strongConfig: _inc_qua_config_pb2.QuaConfig
    quantumMachineId: str
    setCorrection: HighQmApiRequest.SetCorrection
    setFrequency: HighQmApiRequest.SetFrequency
    setDcOffset: HighQmApiRequest.SetDcOffset
    setDigitalRoute: HighQmApiRequest.SetDigitalRoute
    setIOValues: HighQmApiRequest.SetIOValues
    setInputDcOffset: HighQmApiRequest.SetInputDcOffset
    setOutputDcOffset: HighQmApiRequest.SetOutputDcOffset
    setOutputFilterTaps: HighQmApiRequest.SetOutputFilterTaps
    setDigitalInputThreshold: HighQmApiRequest.SetDigitalInputThreshold
    setDigitalInputDeadtime: HighQmApiRequest.SetDigitalInputDeadtime
    setDigitalInputPolarity: HighQmApiRequest.SetDigitalInputPolarity
    def __init__(self, config: _Optional[_Union[QmConfig, _Mapping]] = ..., strongConfig: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., quantumMachineId: _Optional[str] = ..., setCorrection: _Optional[_Union[HighQmApiRequest.SetCorrection, _Mapping]] = ..., setFrequency: _Optional[_Union[HighQmApiRequest.SetFrequency, _Mapping]] = ..., setDcOffset: _Optional[_Union[HighQmApiRequest.SetDcOffset, _Mapping]] = ..., setDigitalRoute: _Optional[_Union[HighQmApiRequest.SetDigitalRoute, _Mapping]] = ..., setIOValues: _Optional[_Union[HighQmApiRequest.SetIOValues, _Mapping]] = ..., setInputDcOffset: _Optional[_Union[HighQmApiRequest.SetInputDcOffset, _Mapping]] = ..., setOutputDcOffset: _Optional[_Union[HighQmApiRequest.SetOutputDcOffset, _Mapping]] = ..., setOutputFilterTaps: _Optional[_Union[HighQmApiRequest.SetOutputFilterTaps, _Mapping]] = ..., setDigitalInputThreshold: _Optional[_Union[HighQmApiRequest.SetDigitalInputThreshold, _Mapping]] = ..., setDigitalInputDeadtime: _Optional[_Union[HighQmApiRequest.SetDigitalInputDeadtime, _Mapping]] = ..., setDigitalInputPolarity: _Optional[_Union[HighQmApiRequest.SetDigitalInputPolarity, _Mapping]] = ...) -> None: ...

class DigitalInputPort(_message.Message):
    __slots__ = ["controllerName", "portNumber", "fem_Number"]
    CONTROLLERNAME_FIELD_NUMBER: _ClassVar[int]
    PORTNUMBER_FIELD_NUMBER: _ClassVar[int]
    FEM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    controllerName: str
    portNumber: int
    fem_Number: int
    def __init__(self, controllerName: _Optional[str] = ..., portNumber: _Optional[int] = ..., fem_Number: _Optional[int] = ...) -> None: ...

class HighQmApiResponse(_message.Message):
    __slots__ = ["ok", "errors"]
    OK_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    errors: _containers.RepeatedCompositeFieldContainer[_general_messages_pb2.ErrorMessage]
    def __init__(self, ok: bool = ..., errors: _Optional[_Iterable[_Union[_general_messages_pb2.ErrorMessage, _Mapping]]] = ...) -> None: ...

class QmConfig(_message.Message):
    __slots__ = ["version", "root"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    version: int
    root: _struct_pb2.Struct
    def __init__(self, version: _Optional[int] = ..., root: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Matrix(_message.Message):
    __slots__ = ["v00", "v01", "v10", "v11"]
    V00_FIELD_NUMBER: _ClassVar[int]
    V01_FIELD_NUMBER: _ClassVar[int]
    V10_FIELD_NUMBER: _ClassVar[int]
    V11_FIELD_NUMBER: _ClassVar[int]
    v00: float
    v01: float
    v10: float
    v11: float
    def __init__(self, v00: _Optional[float] = ..., v01: _Optional[float] = ..., v10: _Optional[float] = ..., v11: _Optional[float] = ...) -> None: ...

class PortReference(_message.Message):
    __slots__ = ["controller", "number"]
    CONTROLLER_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    controller: str
    number: int
    def __init__(self, controller: _Optional[str] = ..., number: _Optional[int] = ...) -> None: ...
