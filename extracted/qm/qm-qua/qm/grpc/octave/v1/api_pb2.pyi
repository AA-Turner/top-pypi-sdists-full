from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DEVICE_STATE_UNSPECIFIED: _ClassVar[DeviceState]
    DEVICE_STATE_NON_OPERATIONAL: _ClassVar[DeviceState]
    DEVICE_STATE_BOOTED: _ClassVar[DeviceState]
    DEVICE_STATE_CONFIGURED: _ClassVar[DeviceState]
    DEVICE_STATE_CLOCK_READY: _ClassVar[DeviceState]
    DEVICE_STATE_INITIALIZED: _ClassVar[DeviceState]
    DEVICE_STATE_OPERATIONAL: _ClassVar[DeviceState]
    DEVICE_STATE_ERRORED: _ClassVar[DeviceState]

class DeviceError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DEVICE_ERROR_UNSPECIFIED: _ClassVar[DeviceError]
    DEVICE_ERROR_PLL: _ClassVar[DeviceError]
    DEVICE_ERROR_MOTHERBOARD_FW_UPD: _ClassVar[DeviceError]
    DEVICE_ERROR_MODULES_DETECT: _ClassVar[DeviceError]
    DEVICE_ERROR_SYNTH_FW_UPD: _ClassVar[DeviceError]
    DEVICE_ERROR_SYNTH_COMM: _ClassVar[DeviceError]
    DEVICE_ERROR_START_FPGA: _ClassVar[DeviceError]
    DEVICE_ERROR_ATTACH_FPGA: _ClassVar[DeviceError]
    DEVICE_ERROR_MAIN_PIC: _ClassVar[DeviceError]
    DEVICE_ERROR_GPIO_COMM: _ClassVar[DeviceError]
    DEVICE_ERROR_FPGA_OVERHEAT: _ClassVar[DeviceError]
    DEVICE_ERROR_FPGA_HW_FAIL: _ClassVar[DeviceError]
    DEVICE_ERROR_BAD_INPUT_CLOCK: _ClassVar[DeviceError]
    DEVICE_ERROR_SYNTH_OVERHEAT: _ClassVar[DeviceError]
    DEVICE_ERROR_SYNTH_BAD_READ: _ClassVar[DeviceError]
    DEVICE_ERROR_IF_DOWN_CONV_OVERHEAT: _ClassVar[DeviceError]
    DEVICE_ERROR_IF_DOWN_CONV_BAD_READ: _ClassVar[DeviceError]
    DEVICE_ERROR_RF_DOWN_CONV_OVERHEAT: _ClassVar[DeviceError]
    DEVICE_ERROR_RF_DOWN_CONV_BAD_READ: _ClassVar[DeviceError]
    DEVICE_ERROR_RF_UP_CONV_OVERHEAT: _ClassVar[DeviceError]
    DEVICE_ERROR_RF_UP_CONV_BAD_READ: _ClassVar[DeviceError]

class OctaveModule(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    OCTAVE_MODULE_UNSPECIFIED: _ClassVar[OctaveModule]
    OCTAVE_MODULE_RF_UPCONVERTER: _ClassVar[OctaveModule]
    OCTAVE_MODULE_RF_DOWNCONVERTER: _ClassVar[OctaveModule]
    OCTAVE_MODULE_IF_DOWNCONVERTER: _ClassVar[OctaveModule]
    OCTAVE_MODULE_SYNTHESIZER: _ClassVar[OctaveModule]
    OCTAVE_MODULE_MOTHERBOARD: _ClassVar[OctaveModule]
    OCTAVE_MODULE_SOM: _ClassVar[OctaveModule]

class ConstantSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    CONSTANT_SOURCE_UNSPECIFIED: _ClassVar[ConstantSource]
    CONSTANT_SOURCE_50_OHM: _ClassVar[ConstantSource]
    CONSTANT_SOURCE_SHORT: _ClassVar[ConstantSource]
    CONSTANT_SOURCE_OPEN: _ClassVar[ConstantSource]
DEVICE_STATE_UNSPECIFIED: DeviceState
DEVICE_STATE_NON_OPERATIONAL: DeviceState
DEVICE_STATE_BOOTED: DeviceState
DEVICE_STATE_CONFIGURED: DeviceState
DEVICE_STATE_CLOCK_READY: DeviceState
DEVICE_STATE_INITIALIZED: DeviceState
DEVICE_STATE_OPERATIONAL: DeviceState
DEVICE_STATE_ERRORED: DeviceState
DEVICE_ERROR_UNSPECIFIED: DeviceError
DEVICE_ERROR_PLL: DeviceError
DEVICE_ERROR_MOTHERBOARD_FW_UPD: DeviceError
DEVICE_ERROR_MODULES_DETECT: DeviceError
DEVICE_ERROR_SYNTH_FW_UPD: DeviceError
DEVICE_ERROR_SYNTH_COMM: DeviceError
DEVICE_ERROR_START_FPGA: DeviceError
DEVICE_ERROR_ATTACH_FPGA: DeviceError
DEVICE_ERROR_MAIN_PIC: DeviceError
DEVICE_ERROR_GPIO_COMM: DeviceError
DEVICE_ERROR_FPGA_OVERHEAT: DeviceError
DEVICE_ERROR_FPGA_HW_FAIL: DeviceError
DEVICE_ERROR_BAD_INPUT_CLOCK: DeviceError
DEVICE_ERROR_SYNTH_OVERHEAT: DeviceError
DEVICE_ERROR_SYNTH_BAD_READ: DeviceError
DEVICE_ERROR_IF_DOWN_CONV_OVERHEAT: DeviceError
DEVICE_ERROR_IF_DOWN_CONV_BAD_READ: DeviceError
DEVICE_ERROR_RF_DOWN_CONV_OVERHEAT: DeviceError
DEVICE_ERROR_RF_DOWN_CONV_BAD_READ: DeviceError
DEVICE_ERROR_RF_UP_CONV_OVERHEAT: DeviceError
DEVICE_ERROR_RF_UP_CONV_BAD_READ: DeviceError
OCTAVE_MODULE_UNSPECIFIED: OctaveModule
OCTAVE_MODULE_RF_UPCONVERTER: OctaveModule
OCTAVE_MODULE_RF_DOWNCONVERTER: OctaveModule
OCTAVE_MODULE_IF_DOWNCONVERTER: OctaveModule
OCTAVE_MODULE_SYNTHESIZER: OctaveModule
OCTAVE_MODULE_MOTHERBOARD: OctaveModule
OCTAVE_MODULE_SOM: OctaveModule
CONSTANT_SOURCE_UNSPECIFIED: ConstantSource
CONSTANT_SOURCE_50_OHM: ConstantSource
CONSTANT_SOURCE_SHORT: ConstantSource
CONSTANT_SOURCE_OPEN: ConstantSource

class SubscribeStateRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SubscribeStateResponse(_message.Message):
    __slots__ = ["state", "error"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    state: DeviceState
    error: DeviceError
    def __init__(self, state: _Optional[_Union[DeviceState, str]] = ..., error: _Optional[_Union[DeviceError, str]] = ...) -> None: ...

class ResetRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ResetResponse(_message.Message):
    __slots__ = ["is_success", "error_message"]
    IS_SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_success: bool
    error_message: str
    def __init__(self, is_success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class HealthRequest(_message.Message):
    __slots__ = ["monitor_interval_seconds", "stop_stream"]
    MONITOR_INTERVAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    STOP_STREAM_FIELD_NUMBER: _ClassVar[int]
    monitor_interval_seconds: int
    stop_stream: bool
    def __init__(self, monitor_interval_seconds: _Optional[int] = ..., stop_stream: bool = ...) -> None: ...

class HealthResponse(_message.Message):
    __slots__ = ["explore", "monitor"]
    EXPLORE_FIELD_NUMBER: _ClassVar[int]
    MONITOR_FIELD_NUMBER: _ClassVar[int]
    explore: ExploreResponse
    monitor: MonitorResponse
    def __init__(self, explore: _Optional[_Union[ExploreResponse, _Mapping]] = ..., monitor: _Optional[_Union[MonitorResponse, _Mapping]] = ...) -> None: ...

class GetVersionRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetVersionResponse(_message.Message):
    __slots__ = ["version"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    version: str
    def __init__(self, version: _Optional[str] = ...) -> None: ...

class ModuleReference(_message.Message):
    __slots__ = ["type", "index"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    type: OctaveModule
    index: int
    def __init__(self, type: _Optional[_Union[OctaveModule, str]] = ..., index: _Optional[int] = ...) -> None: ...

class SaveRequest(_message.Message):
    __slots__ = ["id", "modules", "overwrite", "timestamp"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MODULES_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    id: str
    modules: _containers.RepeatedCompositeFieldContainer[ModuleReference]
    overwrite: bool
    timestamp: int
    def __init__(self, id: _Optional[str] = ..., modules: _Optional[_Iterable[_Union[ModuleReference, _Mapping]]] = ..., overwrite: bool = ..., timestamp: _Optional[int] = ...) -> None: ...

class SaveResponse(_message.Message):
    __slots__ = ["success", "message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class RecallRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class RecallResponse(_message.Message):
    __slots__ = ["success", "error_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class ListRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SaveInfo(_message.Message):
    __slots__ = ["request", "content"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    request: SaveRequest
    content: UpdateRequest
    def __init__(self, request: _Optional[_Union[SaveRequest, _Mapping]] = ..., content: _Optional[_Union[UpdateRequest, _Mapping]] = ...) -> None: ...

class ListResponse(_message.Message):
    __slots__ = ["save_infos"]
    SAVE_INFOS_FIELD_NUMBER: _ClassVar[int]
    save_infos: _containers.RepeatedCompositeFieldContainer[SaveInfo]
    def __init__(self, save_infos: _Optional[_Iterable[_Union[SaveInfo, _Mapping]]] = ...) -> None: ...

class MonitorRequest(_message.Message):
    __slots__ = ["sense_only"]
    SENSE_ONLY_FIELD_NUMBER: _ClassVar[int]
    sense_only: bool
    def __init__(self, sense_only: bool = ...) -> None: ...

class MonitorResponse(_message.Message):
    __slots__ = ["modules"]
    class OctaveError(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        OCTAVE_ERROR_UNSPECIFIED: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_BAD_EXTERNAL_CLOCK: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_BAD_INTERNAL_CLOCK: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_FPGA_NOT_FOUND: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_FPGA_HW_FAIL: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_FPGA_BITFILE_FAIL: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_MODULE_NOT_FOUND: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_OVERHEAT: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_OVERHEAT_PROTECTION: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_READ_TEMP_FAIL: _ClassVar[MonitorResponse.OctaveError]
        OCTAVE_ERROR_PLL_NOT_LOCKED: _ClassVar[MonitorResponse.OctaveError]
    OCTAVE_ERROR_UNSPECIFIED: MonitorResponse.OctaveError
    OCTAVE_ERROR_BAD_EXTERNAL_CLOCK: MonitorResponse.OctaveError
    OCTAVE_ERROR_BAD_INTERNAL_CLOCK: MonitorResponse.OctaveError
    OCTAVE_ERROR_FPGA_NOT_FOUND: MonitorResponse.OctaveError
    OCTAVE_ERROR_FPGA_HW_FAIL: MonitorResponse.OctaveError
    OCTAVE_ERROR_FPGA_BITFILE_FAIL: MonitorResponse.OctaveError
    OCTAVE_ERROR_MODULE_NOT_FOUND: MonitorResponse.OctaveError
    OCTAVE_ERROR_OVERHEAT: MonitorResponse.OctaveError
    OCTAVE_ERROR_OVERHEAT_PROTECTION: MonitorResponse.OctaveError
    OCTAVE_ERROR_READ_TEMP_FAIL: MonitorResponse.OctaveError
    OCTAVE_ERROR_PLL_NOT_LOCKED: MonitorResponse.OctaveError
    class ModuleStatusError(_message.Message):
        __slots__ = ["type"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        type: MonitorResponse.OctaveError
        def __init__(self, type: _Optional[_Union[MonitorResponse.OctaveError, str]] = ...) -> None: ...
    class ModuleStatus(_message.Message):
        __slots__ = ["module", "temperature", "errors"]
        MODULE_FIELD_NUMBER: _ClassVar[int]
        TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
        ERRORS_FIELD_NUMBER: _ClassVar[int]
        module: ModuleReference
        temperature: float
        errors: _containers.RepeatedCompositeFieldContainer[MonitorResponse.ModuleStatusError]
        def __init__(self, module: _Optional[_Union[ModuleReference, _Mapping]] = ..., temperature: _Optional[float] = ..., errors: _Optional[_Iterable[_Union[MonitorResponse.ModuleStatusError, _Mapping]]] = ...) -> None: ...
    MODULES_FIELD_NUMBER: _ClassVar[int]
    modules: _containers.RepeatedCompositeFieldContainer[MonitorResponse.ModuleStatus]
    def __init__(self, modules: _Optional[_Iterable[_Union[MonitorResponse.ModuleStatus, _Mapping]]] = ...) -> None: ...

class ControlRequest(_message.Message):
    __slots__ = ["w_data", "r_length"]
    W_DATA_FIELD_NUMBER: _ClassVar[int]
    R_LENGTH_FIELD_NUMBER: _ClassVar[int]
    w_data: bytes
    r_length: int
    def __init__(self, w_data: _Optional[bytes] = ..., r_length: _Optional[int] = ...) -> None: ...

class ControlResponse(_message.Message):
    __slots__ = ["r_data"]
    class RdataDebug(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        RDATA_DEBUG_UNSPECIFIED: _ClassVar[ControlResponse.RdataDebug]
        RDATA_DEBUG_ERROR_RESPONSE: _ClassVar[ControlResponse.RdataDebug]
        RDATA_DEBUG_SUCCESS_RESPONSE: _ClassVar[ControlResponse.RdataDebug]
    RDATA_DEBUG_UNSPECIFIED: ControlResponse.RdataDebug
    RDATA_DEBUG_ERROR_RESPONSE: ControlResponse.RdataDebug
    RDATA_DEBUG_SUCCESS_RESPONSE: ControlResponse.RdataDebug
    R_DATA_FIELD_NUMBER: _ClassVar[int]
    r_data: bytes
    def __init__(self, r_data: _Optional[bytes] = ...) -> None: ...

class ExploreRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ExploreResponse(_message.Message):
    __slots__ = ["modules"]
    class ModuleId(_message.Message):
        __slots__ = ["module", "id"]
        MODULE_FIELD_NUMBER: _ClassVar[int]
        ID_FIELD_NUMBER: _ClassVar[int]
        module: ModuleReference
        id: str
        def __init__(self, module: _Optional[_Union[ModuleReference, _Mapping]] = ..., id: _Optional[str] = ...) -> None: ...
    MODULES_FIELD_NUMBER: _ClassVar[int]
    modules: _containers.RepeatedCompositeFieldContainer[ExploreResponse.ModuleId]
    def __init__(self, modules: _Optional[_Iterable[_Union[ExploreResponse.ModuleId, _Mapping]]] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["updates"]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    updates: _containers.RepeatedCompositeFieldContainer[SingleUpdate]
    def __init__(self, updates: _Optional[_Iterable[_Union[SingleUpdate, _Mapping]]] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["success", "error_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...

class SingleUpdate(_message.Message):
    __slots__ = ["rf_up_conv", "rf_down_conv", "if_down_conv", "synth", "clock", "motherboard"]
    RF_UP_CONV_FIELD_NUMBER: _ClassVar[int]
    RF_DOWN_CONV_FIELD_NUMBER: _ClassVar[int]
    IF_DOWN_CONV_FIELD_NUMBER: _ClassVar[int]
    SYNTH_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    MOTHERBOARD_FIELD_NUMBER: _ClassVar[int]
    rf_up_conv: RFUpConvUpdate
    rf_down_conv: RFDownConvUpdate
    if_down_conv: IFDownConvUpdate
    synth: SynthUpdate
    clock: ClockUpdate
    motherboard: MotherboardUpdate
    def __init__(self, rf_up_conv: _Optional[_Union[RFUpConvUpdate, _Mapping]] = ..., rf_down_conv: _Optional[_Union[RFDownConvUpdate, _Mapping]] = ..., if_down_conv: _Optional[_Union[IFDownConvUpdate, _Mapping]] = ..., synth: _Optional[_Union[SynthUpdate, _Mapping]] = ..., clock: _Optional[_Union[ClockUpdate, _Mapping]] = ..., motherboard: _Optional[_Union[MotherboardUpdate, _Mapping]] = ...) -> None: ...

class RFUpConvUpdate(_message.Message):
    __slots__ = ["index", "input_attn", "enabled", "mixer_output_attn", "power_amp_enabled", "power_amp_attn", "fast_switch_mode"]
    class IfInputSelection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        IF_INPUT_SELECTION_UNSPECIFIED: _ClassVar[RFUpConvUpdate.IfInputSelection]
        IF_INPUT_SELECTION_PASS_THROUGH: _ClassVar[RFUpConvUpdate.IfInputSelection]
        IF_INPUT_SELECTION_ATTENUATE_10DB: _ClassVar[RFUpConvUpdate.IfInputSelection]
    IF_INPUT_SELECTION_UNSPECIFIED: RFUpConvUpdate.IfInputSelection
    IF_INPUT_SELECTION_PASS_THROUGH: RFUpConvUpdate.IfInputSelection
    IF_INPUT_SELECTION_ATTENUATE_10DB: RFUpConvUpdate.IfInputSelection
    class FastSwitchMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        FAST_SWITCH_MODE_UNSPECIFIED: _ClassVar[RFUpConvUpdate.FastSwitchMode]
        FAST_SWITCH_MODE_ON: _ClassVar[RFUpConvUpdate.FastSwitchMode]
        FAST_SWITCH_MODE_OFF: _ClassVar[RFUpConvUpdate.FastSwitchMode]
        FAST_SWITCH_MODE_DIRECT: _ClassVar[RFUpConvUpdate.FastSwitchMode]
        FAST_SWITCH_MODE_INVERTED: _ClassVar[RFUpConvUpdate.FastSwitchMode]
    FAST_SWITCH_MODE_UNSPECIFIED: RFUpConvUpdate.FastSwitchMode
    FAST_SWITCH_MODE_ON: RFUpConvUpdate.FastSwitchMode
    FAST_SWITCH_MODE_OFF: RFUpConvUpdate.FastSwitchMode
    FAST_SWITCH_MODE_DIRECT: RFUpConvUpdate.FastSwitchMode
    FAST_SWITCH_MODE_INVERTED: RFUpConvUpdate.FastSwitchMode
    INDEX_FIELD_NUMBER: _ClassVar[int]
    INPUT_ATTN_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    MIXER_OUTPUT_ATTN_FIELD_NUMBER: _ClassVar[int]
    POWER_AMP_ENABLED_FIELD_NUMBER: _ClassVar[int]
    POWER_AMP_ATTN_FIELD_NUMBER: _ClassVar[int]
    FAST_SWITCH_MODE_FIELD_NUMBER: _ClassVar[int]
    index: int
    input_attn: RFUpConvUpdate.IfInputSelection
    enabled: _wrappers_pb2.BoolValue
    mixer_output_attn: _wrappers_pb2.UInt32Value
    power_amp_enabled: _wrappers_pb2.BoolValue
    power_amp_attn: _wrappers_pb2.UInt32Value
    fast_switch_mode: RFUpConvUpdate.FastSwitchMode
    def __init__(self, index: _Optional[int] = ..., input_attn: _Optional[_Union[RFUpConvUpdate.IfInputSelection, str]] = ..., enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., mixer_output_attn: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., power_amp_enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ..., power_amp_attn: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., fast_switch_mode: _Optional[_Union[RFUpConvUpdate.FastSwitchMode, str]] = ...) -> None: ...

class RFDownConvUpdate(_message.Message):
    __slots__ = ["index", "rf_input", "lo_input", "enabled"]
    class RFInput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        RF_INPUT_UNSPECIFIED: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_DEBUG_1: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_DEBUG_2: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_DEBUG_3: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_DEBUG_4: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_DEBUG_5: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_MAIN: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_FPGA_CONTROL: _ClassVar[RFDownConvUpdate.RFInput]
        RF_INPUT_DISCONNECT: _ClassVar[RFDownConvUpdate.RFInput]
    RF_INPUT_UNSPECIFIED: RFDownConvUpdate.RFInput
    RF_INPUT_DEBUG_1: RFDownConvUpdate.RFInput
    RF_INPUT_DEBUG_2: RFDownConvUpdate.RFInput
    RF_INPUT_DEBUG_3: RFDownConvUpdate.RFInput
    RF_INPUT_DEBUG_4: RFDownConvUpdate.RFInput
    RF_INPUT_DEBUG_5: RFDownConvUpdate.RFInput
    RF_INPUT_MAIN: RFDownConvUpdate.RFInput
    RF_INPUT_FPGA_CONTROL: RFDownConvUpdate.RFInput
    RF_INPUT_DISCONNECT: RFDownConvUpdate.RFInput
    class LOInput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        LO_INPUT_UNSPECIFIED: _ClassVar[RFDownConvUpdate.LOInput]
        LO_INPUT_1: _ClassVar[RFDownConvUpdate.LOInput]
        LO_INPUT_2: _ClassVar[RFDownConvUpdate.LOInput]
        LO_INPUT_FPGA_CONTROL: _ClassVar[RFDownConvUpdate.LOInput]
    LO_INPUT_UNSPECIFIED: RFDownConvUpdate.LOInput
    LO_INPUT_1: RFDownConvUpdate.LOInput
    LO_INPUT_2: RFDownConvUpdate.LOInput
    LO_INPUT_FPGA_CONTROL: RFDownConvUpdate.LOInput
    INDEX_FIELD_NUMBER: _ClassVar[int]
    RF_INPUT_FIELD_NUMBER: _ClassVar[int]
    LO_INPUT_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    index: int
    rf_input: RFDownConvUpdate.RFInput
    lo_input: RFDownConvUpdate.LOInput
    enabled: _wrappers_pb2.BoolValue
    def __init__(self, index: _Optional[int] = ..., rf_input: _Optional[_Union[RFDownConvUpdate.RFInput, str]] = ..., lo_input: _Optional[_Union[RFDownConvUpdate.LOInput, str]] = ..., enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...

class IFDownConvUpdate(_message.Message):
    __slots__ = ["index", "channel1", "channel2"]
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        MODE_UNSPECIFIED: _ClassVar[IFDownConvUpdate.Mode]
        MODE_OFF: _ClassVar[IFDownConvUpdate.Mode]
        MODE_BYPASS: _ClassVar[IFDownConvUpdate.Mode]
        MODE_POWER_DETECT: _ClassVar[IFDownConvUpdate.Mode]
        MODE_MIXER: _ClassVar[IFDownConvUpdate.Mode]
    MODE_UNSPECIFIED: IFDownConvUpdate.Mode
    MODE_OFF: IFDownConvUpdate.Mode
    MODE_BYPASS: IFDownConvUpdate.Mode
    MODE_POWER_DETECT: IFDownConvUpdate.Mode
    MODE_MIXER: IFDownConvUpdate.Mode
    class Coupling(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        COUPLING_UNSPECIFIED: _ClassVar[IFDownConvUpdate.Coupling]
        COUPLING_OPEN: _ClassVar[IFDownConvUpdate.Coupling]
        COUPLING_DC: _ClassVar[IFDownConvUpdate.Coupling]
        COUPLING_AC: _ClassVar[IFDownConvUpdate.Coupling]
    COUPLING_UNSPECIFIED: IFDownConvUpdate.Coupling
    COUPLING_OPEN: IFDownConvUpdate.Coupling
    COUPLING_DC: IFDownConvUpdate.Coupling
    COUPLING_AC: IFDownConvUpdate.Coupling
    class Channel(_message.Message):
        __slots__ = ["mode", "coupling"]
        MODE_FIELD_NUMBER: _ClassVar[int]
        COUPLING_FIELD_NUMBER: _ClassVar[int]
        mode: IFDownConvUpdate.Mode
        coupling: IFDownConvUpdate.Coupling
        def __init__(self, mode: _Optional[_Union[IFDownConvUpdate.Mode, str]] = ..., coupling: _Optional[_Union[IFDownConvUpdate.Coupling, str]] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CHANNEL1_FIELD_NUMBER: _ClassVar[int]
    CHANNEL2_FIELD_NUMBER: _ClassVar[int]
    index: int
    channel1: IFDownConvUpdate.Channel
    channel2: IFDownConvUpdate.Channel
    def __init__(self, index: _Optional[int] = ..., channel1: _Optional[_Union[IFDownConvUpdate.Channel, _Mapping]] = ..., channel2: _Optional[_Union[IFDownConvUpdate.Channel, _Mapping]] = ...) -> None: ...

class ClockUpdate(_message.Message):
    __slots__ = ["mode", "clock_frequency", "synthesizers_clock", "clustered"]
    class Mode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        MODE_UNSPECIFIED: _ClassVar[ClockUpdate.Mode]
        MODE_BUFFERED: _ClassVar[ClockUpdate.Mode]
        MODE_EXTERNAL: _ClassVar[ClockUpdate.Mode]
        MODE_INTERNAL: _ClassVar[ClockUpdate.Mode]
    MODE_UNSPECIFIED: ClockUpdate.Mode
    MODE_BUFFERED: ClockUpdate.Mode
    MODE_EXTERNAL: ClockUpdate.Mode
    MODE_INTERNAL: ClockUpdate.Mode
    MODE_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    SYNTHESIZERS_CLOCK_FIELD_NUMBER: _ClassVar[int]
    CLUSTERED_FIELD_NUMBER: _ClassVar[int]
    mode: ClockUpdate.Mode
    clock_frequency: _wrappers_pb2.DoubleValue
    synthesizers_clock: _wrappers_pb2.DoubleValue
    clustered: bool
    def __init__(self, mode: _Optional[_Union[ClockUpdate.Mode, str]] = ..., clock_frequency: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., synthesizers_clock: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., clustered: bool = ...) -> None: ...

class MotherboardUpdate(_message.Message):
    __slots__ = ["fan_speed"]
    FAN_SPEED_FIELD_NUMBER: _ClassVar[int]
    fan_speed: _wrappers_pb2.DoubleValue
    def __init__(self, fan_speed: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ...) -> None: ...

class SynthUpdate(_message.Message):
    __slots__ = ["index", "reference_clock", "synth_output", "synth_output_power", "heater", "gain", "digital_attn", "main_source", "main_output", "secondary_output", "stabilizer"]
    class ReferenceSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        REFERENCE_SOURCE_UNSPECIFIED: _ClassVar[SynthUpdate.ReferenceSource]
        REFERENCE_SOURCE_INTERNAL: _ClassVar[SynthUpdate.ReferenceSource]
        REFERENCE_SOURCE_EXTERNAL: _ClassVar[SynthUpdate.ReferenceSource]
    REFERENCE_SOURCE_UNSPECIFIED: SynthUpdate.ReferenceSource
    REFERENCE_SOURCE_INTERNAL: SynthUpdate.ReferenceSource
    REFERENCE_SOURCE_EXTERNAL: SynthUpdate.ReferenceSource
    class SynthOutputPower(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        SYNTH_OUTPUT_POWER_UNSPECIFIED: _ClassVar[SynthUpdate.SynthOutputPower]
        SYNTH_OUTPUT_POWER_NEG4DB: _ClassVar[SynthUpdate.SynthOutputPower]
        SYNTH_OUTPUT_POWER_NEG1DB: _ClassVar[SynthUpdate.SynthOutputPower]
        SYNTH_OUTPUT_POWER_POS2DB: _ClassVar[SynthUpdate.SynthOutputPower]
        SYNTH_OUTPUT_POWER_POS5DB: _ClassVar[SynthUpdate.SynthOutputPower]
    SYNTH_OUTPUT_POWER_UNSPECIFIED: SynthUpdate.SynthOutputPower
    SYNTH_OUTPUT_POWER_NEG4DB: SynthUpdate.SynthOutputPower
    SYNTH_OUTPUT_POWER_NEG1DB: SynthUpdate.SynthOutputPower
    SYNTH_OUTPUT_POWER_POS2DB: SynthUpdate.SynthOutputPower
    SYNTH_OUTPUT_POWER_POS5DB: SynthUpdate.SynthOutputPower
    class MainSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        MAIN_SOURCE_UNSPECIFIED: _ClassVar[SynthUpdate.MainSource]
        MAIN_SOURCE_EXTERNAL: _ClassVar[SynthUpdate.MainSource]
        MAIN_SOURCE_SYNTHESIZER: _ClassVar[SynthUpdate.MainSource]
    MAIN_SOURCE_UNSPECIFIED: SynthUpdate.MainSource
    MAIN_SOURCE_EXTERNAL: SynthUpdate.MainSource
    MAIN_SOURCE_SYNTHESIZER: SynthUpdate.MainSource
    class MainOutput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        MAIN_OUTPUT_UNSPECIFIED: _ClassVar[SynthUpdate.MainOutput]
        MAIN_OUTPUT_MAIN: _ClassVar[SynthUpdate.MainOutput]
        MAIN_OUTPUT_OFF: _ClassVar[SynthUpdate.MainOutput]
        MAIN_OUTPUT_FPGA_CONTROL: _ClassVar[SynthUpdate.MainOutput]
    MAIN_OUTPUT_UNSPECIFIED: SynthUpdate.MainOutput
    MAIN_OUTPUT_MAIN: SynthUpdate.MainOutput
    MAIN_OUTPUT_OFF: SynthUpdate.MainOutput
    MAIN_OUTPUT_FPGA_CONTROL: SynthUpdate.MainOutput
    class SecondaryOutput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        SECONDARY_OUTPUT_UNSPECIFIED: _ClassVar[SynthUpdate.SecondaryOutput]
        SECONDARY_OUTPUT_MAIN: _ClassVar[SynthUpdate.SecondaryOutput]
        SECONDARY_OUTPUT_AUXILARY: _ClassVar[SynthUpdate.SecondaryOutput]
        SECONDARY_OUTPUT_OFF: _ClassVar[SynthUpdate.SecondaryOutput]
        SECONDARY_OUTPUT_FPGA_CONTROL: _ClassVar[SynthUpdate.SecondaryOutput]
    SECONDARY_OUTPUT_UNSPECIFIED: SynthUpdate.SecondaryOutput
    SECONDARY_OUTPUT_MAIN: SynthUpdate.SecondaryOutput
    SECONDARY_OUTPUT_AUXILARY: SynthUpdate.SecondaryOutput
    SECONDARY_OUTPUT_OFF: SynthUpdate.SecondaryOutput
    SECONDARY_OUTPUT_FPGA_CONTROL: SynthUpdate.SecondaryOutput
    class ReferenceClock(_message.Message):
        __slots__ = ["source", "frequency", "divider"]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        DIVIDER_FIELD_NUMBER: _ClassVar[int]
        source: SynthUpdate.ReferenceSource
        frequency: _wrappers_pb2.DoubleValue
        divider: _wrappers_pb2.Int32Value
        def __init__(self, source: _Optional[_Union[SynthUpdate.ReferenceSource, str]] = ..., frequency: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., divider: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ...) -> None: ...
    class SynthOutput(_message.Message):
        __slots__ = ["frequency", "disabled"]
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        DISABLED_FIELD_NUMBER: _ClassVar[int]
        frequency: _wrappers_pb2.DoubleValue
        disabled: _wrappers_pb2.BoolValue
        def __init__(self, frequency: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., disabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...
    class Stabilizer(_message.Message):
        __slots__ = ["k_p", "k_i", "k_d", "a", "b", "heater_max", "set_point", "enabled"]
        K_P_FIELD_NUMBER: _ClassVar[int]
        K_I_FIELD_NUMBER: _ClassVar[int]
        K_D_FIELD_NUMBER: _ClassVar[int]
        A_FIELD_NUMBER: _ClassVar[int]
        B_FIELD_NUMBER: _ClassVar[int]
        HEATER_MAX_FIELD_NUMBER: _ClassVar[int]
        SET_POINT_FIELD_NUMBER: _ClassVar[int]
        ENABLED_FIELD_NUMBER: _ClassVar[int]
        k_p: _wrappers_pb2.FloatValue
        k_i: _wrappers_pb2.FloatValue
        k_d: _wrappers_pb2.FloatValue
        a: _wrappers_pb2.FloatValue
        b: _wrappers_pb2.FloatValue
        heater_max: _wrappers_pb2.UInt32Value
        set_point: _wrappers_pb2.FloatValue
        enabled: _wrappers_pb2.BoolValue
        def __init__(self, k_p: _Optional[_Union[_wrappers_pb2.FloatValue, _Mapping]] = ..., k_i: _Optional[_Union[_wrappers_pb2.FloatValue, _Mapping]] = ..., k_d: _Optional[_Union[_wrappers_pb2.FloatValue, _Mapping]] = ..., a: _Optional[_Union[_wrappers_pb2.FloatValue, _Mapping]] = ..., b: _Optional[_Union[_wrappers_pb2.FloatValue, _Mapping]] = ..., heater_max: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., set_point: _Optional[_Union[_wrappers_pb2.FloatValue, _Mapping]] = ..., enabled: _Optional[_Union[_wrappers_pb2.BoolValue, _Mapping]] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_CLOCK_FIELD_NUMBER: _ClassVar[int]
    SYNTH_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SYNTH_OUTPUT_POWER_FIELD_NUMBER: _ClassVar[int]
    HEATER_FIELD_NUMBER: _ClassVar[int]
    GAIN_FIELD_NUMBER: _ClassVar[int]
    DIGITAL_ATTN_FIELD_NUMBER: _ClassVar[int]
    MAIN_SOURCE_FIELD_NUMBER: _ClassVar[int]
    MAIN_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    STABILIZER_FIELD_NUMBER: _ClassVar[int]
    index: int
    reference_clock: SynthUpdate.ReferenceClock
    synth_output: SynthUpdate.SynthOutput
    synth_output_power: SynthUpdate.SynthOutputPower
    heater: _wrappers_pb2.UInt32Value
    gain: _wrappers_pb2.UInt32Value
    digital_attn: _wrappers_pb2.UInt32Value
    main_source: SynthUpdate.MainSource
    main_output: SynthUpdate.MainOutput
    secondary_output: SynthUpdate.SecondaryOutput
    stabilizer: SynthUpdate.Stabilizer
    def __init__(self, index: _Optional[int] = ..., reference_clock: _Optional[_Union[SynthUpdate.ReferenceClock, _Mapping]] = ..., synth_output: _Optional[_Union[SynthUpdate.SynthOutput, _Mapping]] = ..., synth_output_power: _Optional[_Union[SynthUpdate.SynthOutputPower, str]] = ..., heater: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., gain: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., digital_attn: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., main_source: _Optional[_Union[SynthUpdate.MainSource, str]] = ..., main_output: _Optional[_Union[SynthUpdate.MainOutput, str]] = ..., secondary_output: _Optional[_Union[SynthUpdate.SecondaryOutput, str]] = ..., stabilizer: _Optional[_Union[SynthUpdate.Stabilizer, _Mapping]] = ...) -> None: ...

class AquireRequest(_message.Message):
    __slots__ = ["modules", "use_cache"]
    MODULES_FIELD_NUMBER: _ClassVar[int]
    USE_CACHE_FIELD_NUMBER: _ClassVar[int]
    modules: _containers.RepeatedCompositeFieldContainer[ModuleReference]
    use_cache: bool
    def __init__(self, modules: _Optional[_Iterable[_Union[ModuleReference, _Mapping]]] = ..., use_cache: bool = ...) -> None: ...

class AquireResponse(_message.Message):
    __slots__ = ["state"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    state: UpdateRequest
    def __init__(self, state: _Optional[_Union[UpdateRequest, _Mapping]] = ...) -> None: ...

class IdentifyRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class IdentifyResponse(_message.Message):
    __slots__ = ["rf_up_converters", "rf_down_converters", "if_down_converters", "synthesizers", "panel_identity"]
    RF_UP_CONVERTERS_FIELD_NUMBER: _ClassVar[int]
    RF_DOWN_CONVERTERS_FIELD_NUMBER: _ClassVar[int]
    IF_DOWN_CONVERTERS_FIELD_NUMBER: _ClassVar[int]
    SYNTHESIZERS_FIELD_NUMBER: _ClassVar[int]
    PANEL_IDENTITY_FIELD_NUMBER: _ClassVar[int]
    rf_up_converters: _containers.RepeatedCompositeFieldContainer[RFUpConvIdentity]
    rf_down_converters: _containers.RepeatedCompositeFieldContainer[RFDownConvIdentity]
    if_down_converters: _containers.RepeatedCompositeFieldContainer[IFDownConvIdentity]
    synthesizers: _containers.RepeatedCompositeFieldContainer[SynthIdentity]
    panel_identity: PanelIdentity
    def __init__(self, rf_up_converters: _Optional[_Iterable[_Union[RFUpConvIdentity, _Mapping]]] = ..., rf_down_converters: _Optional[_Iterable[_Union[RFDownConvIdentity, _Mapping]]] = ..., if_down_converters: _Optional[_Iterable[_Union[IFDownConvIdentity, _Mapping]]] = ..., synthesizers: _Optional[_Iterable[_Union[SynthIdentity, _Mapping]]] = ..., panel_identity: _Optional[_Union[PanelIdentity, _Mapping]] = ...) -> None: ...

class UpConvRFOutput(_message.Message):
    __slots__ = ["index"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class SynthRFOutput(_message.Message):
    __slots__ = ["index", "output_port"]
    class OutputPort(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        OUTPUT_PORT_UNSPECIFIED: _ClassVar[SynthRFOutput.OutputPort]
        OUTPUT_PORT_SYNTH: _ClassVar[SynthRFOutput.OutputPort]
        OUTPUT_PORT_MAIN: _ClassVar[SynthRFOutput.OutputPort]
        OUTPUT_PORT_SECONDARY: _ClassVar[SynthRFOutput.OutputPort]
    OUTPUT_PORT_UNSPECIFIED: SynthRFOutput.OutputPort
    OUTPUT_PORT_SYNTH: SynthRFOutput.OutputPort
    OUTPUT_PORT_MAIN: SynthRFOutput.OutputPort
    OUTPUT_PORT_SECONDARY: SynthRFOutput.OutputPort
    INDEX_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PORT_FIELD_NUMBER: _ClassVar[int]
    index: int
    output_port: SynthRFOutput.OutputPort
    def __init__(self, index: _Optional[int] = ..., output_port: _Optional[_Union[SynthRFOutput.OutputPort, str]] = ...) -> None: ...

class ExternalRFInput(_message.Message):
    __slots__ = ["lo_input_index", "demod_lo_input_index", "rf_in_index"]
    LO_INPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    DEMOD_LO_INPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    RF_IN_INDEX_FIELD_NUMBER: _ClassVar[int]
    lo_input_index: int
    demod_lo_input_index: int
    rf_in_index: int
    def __init__(self, lo_input_index: _Optional[int] = ..., demod_lo_input_index: _Optional[int] = ..., rf_in_index: _Optional[int] = ...) -> None: ...

class RFSource(_message.Message):
    __slots__ = ["rf_up_conv_output", "synth_output", "external_input", "constant_source"]
    RF_UP_CONV_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    SYNTH_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_INPUT_FIELD_NUMBER: _ClassVar[int]
    CONSTANT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    rf_up_conv_output: UpConvRFOutput
    synth_output: SynthRFOutput
    external_input: ExternalRFInput
    constant_source: ConstantSource
    def __init__(self, rf_up_conv_output: _Optional[_Union[UpConvRFOutput, _Mapping]] = ..., synth_output: _Optional[_Union[SynthRFOutput, _Mapping]] = ..., external_input: _Optional[_Union[ExternalRFInput, _Mapping]] = ..., constant_source: _Optional[_Union[ConstantSource, str]] = ...) -> None: ...

class RFDownConvIFSource(_message.Message):
    __slots__ = ["index", "output_port"]
    class OutputPort(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        OUTPUT_PORT_UNSPECIFIED: _ClassVar[RFDownConvIFSource.OutputPort]
        OUTPUT_PORT_I: _ClassVar[RFDownConvIFSource.OutputPort]
        OUTPUT_PORT_Q: _ClassVar[RFDownConvIFSource.OutputPort]
    OUTPUT_PORT_UNSPECIFIED: RFDownConvIFSource.OutputPort
    OUTPUT_PORT_I: RFDownConvIFSource.OutputPort
    OUTPUT_PORT_Q: RFDownConvIFSource.OutputPort
    INDEX_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_PORT_FIELD_NUMBER: _ClassVar[int]
    index: int
    output_port: RFDownConvIFSource.OutputPort
    def __init__(self, index: _Optional[int] = ..., output_port: _Optional[_Union[RFDownConvIFSource.OutputPort, str]] = ...) -> None: ...

class IFDownConvIFSource(_message.Message):
    __slots__ = ["index", "channel_index"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    channel_index: int
    def __init__(self, index: _Optional[int] = ..., channel_index: _Optional[int] = ...) -> None: ...

class ExternalIFInput(_message.Message):
    __slots__ = ["i_index", "q_index", "if_lo_i_index", "if_lo_q_index"]
    I_INDEX_FIELD_NUMBER: _ClassVar[int]
    Q_INDEX_FIELD_NUMBER: _ClassVar[int]
    IF_LO_I_INDEX_FIELD_NUMBER: _ClassVar[int]
    IF_LO_Q_INDEX_FIELD_NUMBER: _ClassVar[int]
    i_index: int
    q_index: int
    if_lo_i_index: int
    if_lo_q_index: int
    def __init__(self, i_index: _Optional[int] = ..., q_index: _Optional[int] = ..., if_lo_i_index: _Optional[int] = ..., if_lo_q_index: _Optional[int] = ...) -> None: ...

class IFSource(_message.Message):
    __slots__ = ["rf_downconv_if_source", "if_downconv_if_source", "external_if_input", "constant_source"]
    RF_DOWNCONV_IF_SOURCE_FIELD_NUMBER: _ClassVar[int]
    IF_DOWNCONV_IF_SOURCE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_IF_INPUT_FIELD_NUMBER: _ClassVar[int]
    CONSTANT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    rf_downconv_if_source: RFDownConvIFSource
    if_downconv_if_source: IFDownConvIFSource
    external_if_input: ExternalIFInput
    constant_source: ConstantSource
    def __init__(self, rf_downconv_if_source: _Optional[_Union[RFDownConvIFSource, _Mapping]] = ..., if_downconv_if_source: _Optional[_Union[IFDownConvIFSource, _Mapping]] = ..., external_if_input: _Optional[_Union[ExternalIFInput, _Mapping]] = ..., constant_source: _Optional[_Union[ConstantSource, str]] = ...) -> None: ...

class RFUpConvIdentity(_message.Message):
    __slots__ = ["index", "connectivity", "parameters"]
    class Connectivity(_message.Message):
        __slots__ = ["i_input", "q_input", "lo_input"]
        I_INPUT_FIELD_NUMBER: _ClassVar[int]
        Q_INPUT_FIELD_NUMBER: _ClassVar[int]
        LO_INPUT_FIELD_NUMBER: _ClassVar[int]
        i_input: IFSource
        q_input: IFSource
        lo_input: RFSource
        def __init__(self, i_input: _Optional[_Union[IFSource, _Mapping]] = ..., q_input: _Optional[_Union[IFSource, _Mapping]] = ..., lo_input: _Optional[_Union[RFSource, _Mapping]] = ...) -> None: ...
    class Parameters(_message.Message):
        __slots__ = ["attn_1_db", "attn_2_db"]
        ATTN_1_DB_FIELD_NUMBER: _ClassVar[int]
        ATTN_2_DB_FIELD_NUMBER: _ClassVar[int]
        attn_1_db: float
        attn_2_db: float
        def __init__(self, attn_1_db: _Optional[float] = ..., attn_2_db: _Optional[float] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    index: int
    connectivity: RFUpConvIdentity.Connectivity
    parameters: RFUpConvIdentity.Parameters
    def __init__(self, index: _Optional[int] = ..., connectivity: _Optional[_Union[RFUpConvIdentity.Connectivity, _Mapping]] = ..., parameters: _Optional[_Union[RFUpConvIdentity.Parameters, _Mapping]] = ...) -> None: ...

class RFDownConvIdentity(_message.Message):
    __slots__ = ["index", "connectivity"]
    class Connectivity(_message.Message):
        __slots__ = ["debug_rf_input_1", "debug_rf_input_2", "debug_rf_input_3", "debug_rf_input_4", "debug_rf_input_5", "rf_main_input", "lo_input_1", "lo_input_2"]
        DEBUG_RF_INPUT_1_FIELD_NUMBER: _ClassVar[int]
        DEBUG_RF_INPUT_2_FIELD_NUMBER: _ClassVar[int]
        DEBUG_RF_INPUT_3_FIELD_NUMBER: _ClassVar[int]
        DEBUG_RF_INPUT_4_FIELD_NUMBER: _ClassVar[int]
        DEBUG_RF_INPUT_5_FIELD_NUMBER: _ClassVar[int]
        RF_MAIN_INPUT_FIELD_NUMBER: _ClassVar[int]
        LO_INPUT_1_FIELD_NUMBER: _ClassVar[int]
        LO_INPUT_2_FIELD_NUMBER: _ClassVar[int]
        debug_rf_input_1: RFSource
        debug_rf_input_2: RFSource
        debug_rf_input_3: RFSource
        debug_rf_input_4: RFSource
        debug_rf_input_5: RFSource
        rf_main_input: RFSource
        lo_input_1: RFSource
        lo_input_2: RFSource
        def __init__(self, debug_rf_input_1: _Optional[_Union[RFSource, _Mapping]] = ..., debug_rf_input_2: _Optional[_Union[RFSource, _Mapping]] = ..., debug_rf_input_3: _Optional[_Union[RFSource, _Mapping]] = ..., debug_rf_input_4: _Optional[_Union[RFSource, _Mapping]] = ..., debug_rf_input_5: _Optional[_Union[RFSource, _Mapping]] = ..., rf_main_input: _Optional[_Union[RFSource, _Mapping]] = ..., lo_input_1: _Optional[_Union[RFSource, _Mapping]] = ..., lo_input_2: _Optional[_Union[RFSource, _Mapping]] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_FIELD_NUMBER: _ClassVar[int]
    index: int
    connectivity: RFDownConvIdentity.Connectivity
    def __init__(self, index: _Optional[int] = ..., connectivity: _Optional[_Union[RFDownConvIdentity.Connectivity, _Mapping]] = ...) -> None: ...

class IFDownConvIdentity(_message.Message):
    __slots__ = ["index", "connectivity"]
    class Connectivity(_message.Message):
        __slots__ = ["channel_1_input", "channel_1_lo_input", "channel_2_input", "channel_2_lo_input"]
        CHANNEL_1_INPUT_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_1_LO_INPUT_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_2_INPUT_FIELD_NUMBER: _ClassVar[int]
        CHANNEL_2_LO_INPUT_FIELD_NUMBER: _ClassVar[int]
        channel_1_input: IFSource
        channel_1_lo_input: IFSource
        channel_2_input: IFSource
        channel_2_lo_input: IFSource
        def __init__(self, channel_1_input: _Optional[_Union[IFSource, _Mapping]] = ..., channel_1_lo_input: _Optional[_Union[IFSource, _Mapping]] = ..., channel_2_input: _Optional[_Union[IFSource, _Mapping]] = ..., channel_2_lo_input: _Optional[_Union[IFSource, _Mapping]] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_FIELD_NUMBER: _ClassVar[int]
    index: int
    connectivity: IFDownConvIdentity.Connectivity
    def __init__(self, index: _Optional[int] = ..., connectivity: _Optional[_Union[IFDownConvIdentity.Connectivity, _Mapping]] = ...) -> None: ...

class SynthIdentity(_message.Message):
    __slots__ = ["index", "connectivity", "parameters"]
    class Connectivity(_message.Message):
        __slots__ = ["main_lo_input", "secondary_lo_input"]
        MAIN_LO_INPUT_FIELD_NUMBER: _ClassVar[int]
        SECONDARY_LO_INPUT_FIELD_NUMBER: _ClassVar[int]
        main_lo_input: RFSource
        secondary_lo_input: RFSource
        def __init__(self, main_lo_input: _Optional[_Union[RFSource, _Mapping]] = ..., secondary_lo_input: _Optional[_Union[RFSource, _Mapping]] = ...) -> None: ...
    class Parameters(_message.Message):
        __slots__ = ["low_frequency_filters", "medium_frequency_filter", "high_frequency_filter"]
        class LowFrequencyFilter(_message.Message):
            __slots__ = ["index", "filter_1", "filter_2"]
            INDEX_FIELD_NUMBER: _ClassVar[int]
            FILTER_1_FIELD_NUMBER: _ClassVar[int]
            FILTER_2_FIELD_NUMBER: _ClassVar[int]
            index: int
            filter_1: str
            filter_2: str
            def __init__(self, index: _Optional[int] = ..., filter_1: _Optional[str] = ..., filter_2: _Optional[str] = ...) -> None: ...
        class ParametrizedFilter(_message.Message):
            __slots__ = []
            def __init__(self) -> None: ...
        LOW_FREQUENCY_FILTERS_FIELD_NUMBER: _ClassVar[int]
        MEDIUM_FREQUENCY_FILTER_FIELD_NUMBER: _ClassVar[int]
        HIGH_FREQUENCY_FILTER_FIELD_NUMBER: _ClassVar[int]
        low_frequency_filters: _containers.RepeatedCompositeFieldContainer[SynthIdentity.Parameters.LowFrequencyFilter]
        medium_frequency_filter: SynthIdentity.Parameters.ParametrizedFilter
        high_frequency_filter: SynthIdentity.Parameters.ParametrizedFilter
        def __init__(self, low_frequency_filters: _Optional[_Iterable[_Union[SynthIdentity.Parameters.LowFrequencyFilter, _Mapping]]] = ..., medium_frequency_filter: _Optional[_Union[SynthIdentity.Parameters.ParametrizedFilter, _Mapping]] = ..., high_frequency_filter: _Optional[_Union[SynthIdentity.Parameters.ParametrizedFilter, _Mapping]] = ...) -> None: ...
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CONNECTIVITY_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    index: int
    connectivity: SynthIdentity.Connectivity
    parameters: SynthIdentity.Parameters
    def __init__(self, index: _Optional[int] = ..., connectivity: _Optional[_Union[SynthIdentity.Connectivity, _Mapping]] = ..., parameters: _Optional[_Union[SynthIdentity.Parameters, _Mapping]] = ...) -> None: ...

class PanelIdentity(_message.Message):
    __slots__ = ["rf_outputs", "if_output_i", "if_output_q", "synth_outputs"]
    class RFOutput(_message.Message):
        __slots__ = ["index", "source"]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        index: int
        source: RFSource
        def __init__(self, index: _Optional[int] = ..., source: _Optional[_Union[RFSource, _Mapping]] = ...) -> None: ...
    class SynthOutput(_message.Message):
        __slots__ = ["index", "source"]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        index: int
        source: RFSource
        def __init__(self, index: _Optional[int] = ..., source: _Optional[_Union[RFSource, _Mapping]] = ...) -> None: ...
    RF_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    IF_OUTPUT_I_FIELD_NUMBER: _ClassVar[int]
    IF_OUTPUT_Q_FIELD_NUMBER: _ClassVar[int]
    SYNTH_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    rf_outputs: _containers.RepeatedCompositeFieldContainer[PanelIdentity.RFOutput]
    if_output_i: _containers.RepeatedCompositeFieldContainer[IFSource]
    if_output_q: _containers.RepeatedCompositeFieldContainer[IFSource]
    synth_outputs: _containers.RepeatedCompositeFieldContainer[PanelIdentity.SynthOutput]
    def __init__(self, rf_outputs: _Optional[_Iterable[_Union[PanelIdentity.RFOutput, _Mapping]]] = ..., if_output_i: _Optional[_Iterable[_Union[IFSource, _Mapping]]] = ..., if_output_q: _Optional[_Iterable[_Union[IFSource, _Mapping]]] = ..., synth_outputs: _Optional[_Iterable[_Union[PanelIdentity.SynthOutput, _Mapping]]] = ...) -> None: ...

class MotherboardStatus(_message.Message):
    __slots__ = ["valid_1g_vco"]
    VALID_1G_VCO_FIELD_NUMBER: _ClassVar[int]
    valid_1g_vco: bool
    def __init__(self, valid_1g_vco: bool = ...) -> None: ...
