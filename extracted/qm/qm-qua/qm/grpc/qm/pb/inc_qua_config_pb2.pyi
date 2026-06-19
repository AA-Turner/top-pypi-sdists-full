from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuaConfig(_message.Message):
    __slots__ = ["v1beta", "v2", "revision"]
    class VoltageLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        LVTTL: _ClassVar[QuaConfig.VoltageLevel]
        TTL: _ClassVar[QuaConfig.VoltageLevel]
    LVTTL: QuaConfig.VoltageLevel
    TTL: QuaConfig.VoltageLevel
    class OutputSwitchState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        unset: _ClassVar[QuaConfig.OutputSwitchState]
        always_on: _ClassVar[QuaConfig.OutputSwitchState]
        always_off: _ClassVar[QuaConfig.OutputSwitchState]
        triggered: _ClassVar[QuaConfig.OutputSwitchState]
        triggered_reversed: _ClassVar[QuaConfig.OutputSwitchState]
    unset: QuaConfig.OutputSwitchState
    always_on: QuaConfig.OutputSwitchState
    always_off: QuaConfig.OutputSwitchState
    triggered: QuaConfig.OutputSwitchState
    triggered_reversed: QuaConfig.OutputSwitchState
    class QuaConfigV1(_message.Message):
        __slots__ = ["controllers", "controlDevices", "oscillators", "elements", "pulses", "mixers", "waveforms", "digitalWaveforms", "integrationWeights", "octaves"]
        class ControllersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.ControllerDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.ControllerDec, _Mapping]] = ...) -> None: ...
        class ControlDevicesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DeviceDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DeviceDec, _Mapping]] = ...) -> None: ...
        class OscillatorsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.Oscillator
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.Oscillator, _Mapping]] = ...) -> None: ...
        class ElementsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.ElementDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.ElementDec, _Mapping]] = ...) -> None: ...
        class PulsesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.PulseDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.PulseDec, _Mapping]] = ...) -> None: ...
        class MixersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.MixerDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.MixerDec, _Mapping]] = ...) -> None: ...
        class WaveformsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.WaveformDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.WaveformDec, _Mapping]] = ...) -> None: ...
        class DigitalWaveformsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DigitalWaveformDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DigitalWaveformDec, _Mapping]] = ...) -> None: ...
        class IntegrationWeightsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.IntegrationWeightDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.IntegrationWeightDec, _Mapping]] = ...) -> None: ...
        class OctavesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.Octave.Config
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.Octave.Config, _Mapping]] = ...) -> None: ...
        CONTROLLERS_FIELD_NUMBER: _ClassVar[int]
        CONTROLDEVICES_FIELD_NUMBER: _ClassVar[int]
        OSCILLATORS_FIELD_NUMBER: _ClassVar[int]
        ELEMENTS_FIELD_NUMBER: _ClassVar[int]
        PULSES_FIELD_NUMBER: _ClassVar[int]
        MIXERS_FIELD_NUMBER: _ClassVar[int]
        WAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        DIGITALWAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        INTEGRATIONWEIGHTS_FIELD_NUMBER: _ClassVar[int]
        OCTAVES_FIELD_NUMBER: _ClassVar[int]
        controllers: _containers.MessageMap[str, QuaConfig.ControllerDec]
        controlDevices: _containers.MessageMap[str, QuaConfig.DeviceDec]
        oscillators: _containers.MessageMap[str, QuaConfig.Oscillator]
        elements: _containers.MessageMap[str, QuaConfig.ElementDec]
        pulses: _containers.MessageMap[str, QuaConfig.PulseDec]
        mixers: _containers.MessageMap[str, QuaConfig.MixerDec]
        waveforms: _containers.MessageMap[str, QuaConfig.WaveformDec]
        digitalWaveforms: _containers.MessageMap[str, QuaConfig.DigitalWaveformDec]
        integrationWeights: _containers.MessageMap[str, QuaConfig.IntegrationWeightDec]
        octaves: _containers.MessageMap[str, QuaConfig.Octave.Config]
        def __init__(self, controllers: _Optional[_Mapping[str, QuaConfig.ControllerDec]] = ..., controlDevices: _Optional[_Mapping[str, QuaConfig.DeviceDec]] = ..., oscillators: _Optional[_Mapping[str, QuaConfig.Oscillator]] = ..., elements: _Optional[_Mapping[str, QuaConfig.ElementDec]] = ..., pulses: _Optional[_Mapping[str, QuaConfig.PulseDec]] = ..., mixers: _Optional[_Mapping[str, QuaConfig.MixerDec]] = ..., waveforms: _Optional[_Mapping[str, QuaConfig.WaveformDec]] = ..., digitalWaveforms: _Optional[_Mapping[str, QuaConfig.DigitalWaveformDec]] = ..., integrationWeights: _Optional[_Mapping[str, QuaConfig.IntegrationWeightDec]] = ..., octaves: _Optional[_Mapping[str, QuaConfig.Octave.Config]] = ...) -> None: ...
    class QuaConfigV2(_message.Message):
        __slots__ = ["controller_config", "logical_config"]
        CONTROLLER_CONFIG_FIELD_NUMBER: _ClassVar[int]
        LOGICAL_CONFIG_FIELD_NUMBER: _ClassVar[int]
        controller_config: QuaConfig.ControllerConfig
        logical_config: QuaConfig.LogicalConfig
        def __init__(self, controller_config: _Optional[_Union[QuaConfig.ControllerConfig, _Mapping]] = ..., logical_config: _Optional[_Union[QuaConfig.LogicalConfig, _Mapping]] = ...) -> None: ...
    class ControllerConfig(_message.Message):
        __slots__ = ["controlDevices", "mixers", "octaves"]
        class ControlDevicesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DeviceDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DeviceDec, _Mapping]] = ...) -> None: ...
        class MixersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.MixerDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.MixerDec, _Mapping]] = ...) -> None: ...
        class OctavesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.Octave.Config
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.Octave.Config, _Mapping]] = ...) -> None: ...
        CONTROLDEVICES_FIELD_NUMBER: _ClassVar[int]
        MIXERS_FIELD_NUMBER: _ClassVar[int]
        OCTAVES_FIELD_NUMBER: _ClassVar[int]
        controlDevices: _containers.MessageMap[str, QuaConfig.DeviceDec]
        mixers: _containers.MessageMap[str, QuaConfig.MixerDec]
        octaves: _containers.MessageMap[str, QuaConfig.Octave.Config]
        def __init__(self, controlDevices: _Optional[_Mapping[str, QuaConfig.DeviceDec]] = ..., mixers: _Optional[_Mapping[str, QuaConfig.MixerDec]] = ..., octaves: _Optional[_Mapping[str, QuaConfig.Octave.Config]] = ...) -> None: ...
    class LogicalConfig(_message.Message):
        __slots__ = ["elements", "oscillators", "pulses", "waveforms", "digitalWaveforms", "integrationWeights"]
        class ElementsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.ElementDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.ElementDec, _Mapping]] = ...) -> None: ...
        class OscillatorsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.Oscillator
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.Oscillator, _Mapping]] = ...) -> None: ...
        class PulsesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.PulseDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.PulseDec, _Mapping]] = ...) -> None: ...
        class WaveformsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.WaveformDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.WaveformDec, _Mapping]] = ...) -> None: ...
        class DigitalWaveformsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DigitalWaveformDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DigitalWaveformDec, _Mapping]] = ...) -> None: ...
        class IntegrationWeightsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.IntegrationWeightDec
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.IntegrationWeightDec, _Mapping]] = ...) -> None: ...
        ELEMENTS_FIELD_NUMBER: _ClassVar[int]
        OSCILLATORS_FIELD_NUMBER: _ClassVar[int]
        PULSES_FIELD_NUMBER: _ClassVar[int]
        WAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        DIGITALWAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        INTEGRATIONWEIGHTS_FIELD_NUMBER: _ClassVar[int]
        elements: _containers.MessageMap[str, QuaConfig.ElementDec]
        oscillators: _containers.MessageMap[str, QuaConfig.Oscillator]
        pulses: _containers.MessageMap[str, QuaConfig.PulseDec]
        waveforms: _containers.MessageMap[str, QuaConfig.WaveformDec]
        digitalWaveforms: _containers.MessageMap[str, QuaConfig.DigitalWaveformDec]
        integrationWeights: _containers.MessageMap[str, QuaConfig.IntegrationWeightDec]
        def __init__(self, elements: _Optional[_Mapping[str, QuaConfig.ElementDec]] = ..., oscillators: _Optional[_Mapping[str, QuaConfig.Oscillator]] = ..., pulses: _Optional[_Mapping[str, QuaConfig.PulseDec]] = ..., waveforms: _Optional[_Mapping[str, QuaConfig.WaveformDec]] = ..., digitalWaveforms: _Optional[_Mapping[str, QuaConfig.DigitalWaveformDec]] = ..., integrationWeights: _Optional[_Mapping[str, QuaConfig.IntegrationWeightDec]] = ...) -> None: ...
    class DeviceDec(_message.Message):
        __slots__ = ["fems"]
        class FemsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.FEMTypes
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.FEMTypes, _Mapping]] = ...) -> None: ...
        FEMS_FIELD_NUMBER: _ClassVar[int]
        fems: _containers.MessageMap[int, QuaConfig.FEMTypes]
        def __init__(self, fems: _Optional[_Mapping[int, QuaConfig.FEMTypes]] = ...) -> None: ...
    class FEMTypes(_message.Message):
        __slots__ = ["opx", "octo_dac", "microwave"]
        OPX_FIELD_NUMBER: _ClassVar[int]
        OCTO_DAC_FIELD_NUMBER: _ClassVar[int]
        MICROWAVE_FIELD_NUMBER: _ClassVar[int]
        opx: QuaConfig.ControllerDec
        octo_dac: QuaConfig.OctoDacFemDec
        microwave: QuaConfig.MicrowaveFemDec
        def __init__(self, opx: _Optional[_Union[QuaConfig.ControllerDec, _Mapping]] = ..., octo_dac: _Optional[_Union[QuaConfig.OctoDacFemDec, _Mapping]] = ..., microwave: _Optional[_Union[QuaConfig.MicrowaveFemDec, _Mapping]] = ...) -> None: ...
    class ControllerDec(_message.Message):
        __slots__ = ["type", "analogOutputs", "analogInputs", "digitalOutputs", "digitalInputs"]
        class AnalogOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.AnalogOutputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.AnalogOutputPortDec, _Mapping]] = ...) -> None: ...
        class AnalogInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.AnalogInputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.AnalogInputPortDec, _Mapping]] = ...) -> None: ...
        class DigitalOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.DigitalOutputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.DigitalOutputPortDec, _Mapping]] = ...) -> None: ...
        class DigitalInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.DigitalInputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.DigitalInputPortDec, _Mapping]] = ...) -> None: ...
        TYPE_FIELD_NUMBER: _ClassVar[int]
        ANALOGOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        ANALOGINPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALINPUTS_FIELD_NUMBER: _ClassVar[int]
        type: str
        analogOutputs: _containers.MessageMap[int, QuaConfig.AnalogOutputPortDec]
        analogInputs: _containers.MessageMap[int, QuaConfig.AnalogInputPortDec]
        digitalOutputs: _containers.MessageMap[int, QuaConfig.DigitalOutputPortDec]
        digitalInputs: _containers.MessageMap[int, QuaConfig.DigitalInputPortDec]
        def __init__(self, type: _Optional[str] = ..., analogOutputs: _Optional[_Mapping[int, QuaConfig.AnalogOutputPortDec]] = ..., analogInputs: _Optional[_Mapping[int, QuaConfig.AnalogInputPortDec]] = ..., digitalOutputs: _Optional[_Mapping[int, QuaConfig.DigitalOutputPortDec]] = ..., digitalInputs: _Optional[_Mapping[int, QuaConfig.DigitalInputPortDec]] = ...) -> None: ...
    class OctoDacFemDec(_message.Message):
        __slots__ = ["analogOutputs", "analogInputs", "digitalOutputs", "digitalInputs"]
        class AnalogOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.OctoDacAnalogOutputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec, _Mapping]] = ...) -> None: ...
        class AnalogInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.AnalogInputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.AnalogInputPortDec, _Mapping]] = ...) -> None: ...
        class DigitalOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.DigitalOutputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.DigitalOutputPortDec, _Mapping]] = ...) -> None: ...
        class DigitalInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.DigitalInputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.DigitalInputPortDec, _Mapping]] = ...) -> None: ...
        ANALOGOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        ANALOGINPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALINPUTS_FIELD_NUMBER: _ClassVar[int]
        analogOutputs: _containers.MessageMap[int, QuaConfig.OctoDacAnalogOutputPortDec]
        analogInputs: _containers.MessageMap[int, QuaConfig.AnalogInputPortDec]
        digitalOutputs: _containers.MessageMap[int, QuaConfig.DigitalOutputPortDec]
        digitalInputs: _containers.MessageMap[int, QuaConfig.DigitalInputPortDec]
        def __init__(self, analogOutputs: _Optional[_Mapping[int, QuaConfig.OctoDacAnalogOutputPortDec]] = ..., analogInputs: _Optional[_Mapping[int, QuaConfig.AnalogInputPortDec]] = ..., digitalOutputs: _Optional[_Mapping[int, QuaConfig.DigitalOutputPortDec]] = ..., digitalInputs: _Optional[_Mapping[int, QuaConfig.DigitalInputPortDec]] = ...) -> None: ...
    class MicrowaveFemDec(_message.Message):
        __slots__ = ["analogOutputs", "analogInputs", "digitalOutputs", "digitalInputs"]
        class AnalogOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.MicrowaveAnalogOutputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.MicrowaveAnalogOutputPortDec, _Mapping]] = ...) -> None: ...
        class AnalogInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.MicrowaveAnalogInputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.MicrowaveAnalogInputPortDec, _Mapping]] = ...) -> None: ...
        class DigitalOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.DigitalOutputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.DigitalOutputPortDec, _Mapping]] = ...) -> None: ...
        class DigitalInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.DigitalInputPortDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.DigitalInputPortDec, _Mapping]] = ...) -> None: ...
        ANALOGOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        ANALOGINPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALINPUTS_FIELD_NUMBER: _ClassVar[int]
        analogOutputs: _containers.MessageMap[int, QuaConfig.MicrowaveAnalogOutputPortDec]
        analogInputs: _containers.MessageMap[int, QuaConfig.MicrowaveAnalogInputPortDec]
        digitalOutputs: _containers.MessageMap[int, QuaConfig.DigitalOutputPortDec]
        digitalInputs: _containers.MessageMap[int, QuaConfig.DigitalInputPortDec]
        def __init__(self, analogOutputs: _Optional[_Mapping[int, QuaConfig.MicrowaveAnalogOutputPortDec]] = ..., analogInputs: _Optional[_Mapping[int, QuaConfig.MicrowaveAnalogInputPortDec]] = ..., digitalOutputs: _Optional[_Mapping[int, QuaConfig.DigitalOutputPortDec]] = ..., digitalInputs: _Optional[_Mapping[int, QuaConfig.DigitalInputPortDec]] = ...) -> None: ...
    class AnalogOutputPortDec(_message.Message):
        __slots__ = ["offset", "filter", "delay", "channelWeights", "shareable", "crosstalk", "min_voltage_limit", "max_voltage_limit"]
        class ChannelWeightsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: float
            def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
        class CrosstalkEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: float
            def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        FILTER_FIELD_NUMBER: _ClassVar[int]
        DELAY_FIELD_NUMBER: _ClassVar[int]
        CHANNELWEIGHTS_FIELD_NUMBER: _ClassVar[int]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        CROSSTALK_FIELD_NUMBER: _ClassVar[int]
        MIN_VOLTAGE_LIMIT_FIELD_NUMBER: _ClassVar[int]
        MAX_VOLTAGE_LIMIT_FIELD_NUMBER: _ClassVar[int]
        offset: float
        filter: QuaConfig.AnalogOutputPortFilter
        delay: int
        channelWeights: _containers.ScalarMap[int, float]
        shareable: bool
        crosstalk: _containers.ScalarMap[int, float]
        min_voltage_limit: float
        max_voltage_limit: float
        def __init__(self, offset: _Optional[float] = ..., filter: _Optional[_Union[QuaConfig.AnalogOutputPortFilter, _Mapping]] = ..., delay: _Optional[int] = ..., channelWeights: _Optional[_Mapping[int, float]] = ..., shareable: bool = ..., crosstalk: _Optional[_Mapping[int, float]] = ..., min_voltage_limit: _Optional[float] = ..., max_voltage_limit: _Optional[float] = ...) -> None: ...
    class MicrowaveAnalogOutputPortDec(_message.Message):
        __slots__ = ["samplingRate", "fullScalePowerDbm", "band", "delay", "shareable", "upconverters", "upconverters_v2"]
        class UpconvertersEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: QuaConfig.UpConverterConfigDec
            def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.UpConverterConfigDec, _Mapping]] = ...) -> None: ...
        class UpConvertersContainer(_message.Message):
            __slots__ = ["value"]
            class ValueEntry(_message.Message):
                __slots__ = ["key", "value"]
                KEY_FIELD_NUMBER: _ClassVar[int]
                VALUE_FIELD_NUMBER: _ClassVar[int]
                key: int
                value: QuaConfig.UpConverterConfigDec
                def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.UpConverterConfigDec, _Mapping]] = ...) -> None: ...
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: _containers.MessageMap[int, QuaConfig.UpConverterConfigDec]
            def __init__(self, value: _Optional[_Mapping[int, QuaConfig.UpConverterConfigDec]] = ...) -> None: ...
        SAMPLINGRATE_FIELD_NUMBER: _ClassVar[int]
        FULLSCALEPOWERDBM_FIELD_NUMBER: _ClassVar[int]
        BAND_FIELD_NUMBER: _ClassVar[int]
        DELAY_FIELD_NUMBER: _ClassVar[int]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        UPCONVERTERS_FIELD_NUMBER: _ClassVar[int]
        UPCONVERTERS_V2_FIELD_NUMBER: _ClassVar[int]
        samplingRate: float
        fullScalePowerDbm: int
        band: int
        delay: int
        shareable: bool
        upconverters: _containers.MessageMap[int, QuaConfig.UpConverterConfigDec]
        upconverters_v2: QuaConfig.MicrowaveAnalogOutputPortDec.UpConvertersContainer
        def __init__(self, samplingRate: _Optional[float] = ..., fullScalePowerDbm: _Optional[int] = ..., band: _Optional[int] = ..., delay: _Optional[int] = ..., shareable: bool = ..., upconverters: _Optional[_Mapping[int, QuaConfig.UpConverterConfigDec]] = ..., upconverters_v2: _Optional[_Union[QuaConfig.MicrowaveAnalogOutputPortDec.UpConvertersContainer, _Mapping]] = ...) -> None: ...
    class UpConverterConfigDec(_message.Message):
        __slots__ = ["frequency"]
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        frequency: float
        def __init__(self, frequency: _Optional[float] = ...) -> None: ...
    class MicrowaveAnalogInputPortDec(_message.Message):
        __slots__ = ["samplingRate", "gain_db", "shareable", "band", "downconverter", "lo_mode"]
        class LoMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            AUTO: _ClassVar[QuaConfig.MicrowaveAnalogInputPortDec.LoMode]
            ALWAYS_ON: _ClassVar[QuaConfig.MicrowaveAnalogInputPortDec.LoMode]
        AUTO: QuaConfig.MicrowaveAnalogInputPortDec.LoMode
        ALWAYS_ON: QuaConfig.MicrowaveAnalogInputPortDec.LoMode
        SAMPLINGRATE_FIELD_NUMBER: _ClassVar[int]
        GAIN_DB_FIELD_NUMBER: _ClassVar[int]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        BAND_FIELD_NUMBER: _ClassVar[int]
        DOWNCONVERTER_FIELD_NUMBER: _ClassVar[int]
        LO_MODE_FIELD_NUMBER: _ClassVar[int]
        samplingRate: float
        gain_db: int
        shareable: bool
        band: int
        downconverter: QuaConfig.DownConverterConfigDec
        lo_mode: QuaConfig.MicrowaveAnalogInputPortDec.LoMode
        def __init__(self, samplingRate: _Optional[float] = ..., gain_db: _Optional[int] = ..., shareable: bool = ..., band: _Optional[int] = ..., downconverter: _Optional[_Union[QuaConfig.DownConverterConfigDec, _Mapping]] = ..., lo_mode: _Optional[_Union[QuaConfig.MicrowaveAnalogInputPortDec.LoMode, str]] = ...) -> None: ...
    class DownConverterConfigDec(_message.Message):
        __slots__ = ["frequency"]
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        frequency: float
        def __init__(self, frequency: _Optional[float] = ...) -> None: ...
    class OctoDacAnalogOutputPortDec(_message.Message):
        __slots__ = ["offset", "filter", "delay", "shareable", "crosstalk", "sampling_rate", "upsampling_mode", "output_mode", "crosstalk_v2", "min_voltage_limit", "max_voltage_limit"]
        class OutputMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            direct: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.OutputMode]
            amplified: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.OutputMode]
        direct: QuaConfig.OctoDacAnalogOutputPortDec.OutputMode
        amplified: QuaConfig.OctoDacAnalogOutputPortDec.OutputMode
        class SamplingRate(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            Undefined: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate]
            GSPS1: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate]
            GSPS2: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate]
        Undefined: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate
        GSPS1: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate
        GSPS2: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate
        class SamplingRateMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            unset: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode]
            mw: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode]
            pulse: _ClassVar[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode]
        unset: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode
        mw: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode
        pulse: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode
        class CrosstalkEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: int
            value: float
            def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
        class CrosstalkContainer(_message.Message):
            __slots__ = ["value"]
            class ValueEntry(_message.Message):
                __slots__ = ["key", "value"]
                KEY_FIELD_NUMBER: _ClassVar[int]
                VALUE_FIELD_NUMBER: _ClassVar[int]
                key: int
                value: float
                def __init__(self, key: _Optional[int] = ..., value: _Optional[float] = ...) -> None: ...
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: _containers.ScalarMap[int, float]
            def __init__(self, value: _Optional[_Mapping[int, float]] = ...) -> None: ...
        class VoltageLimitContainer(_message.Message):
            __slots__ = ["value"]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: float
            def __init__(self, value: _Optional[float] = ...) -> None: ...
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        FILTER_FIELD_NUMBER: _ClassVar[int]
        DELAY_FIELD_NUMBER: _ClassVar[int]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        CROSSTALK_FIELD_NUMBER: _ClassVar[int]
        SAMPLING_RATE_FIELD_NUMBER: _ClassVar[int]
        UPSAMPLING_MODE_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_MODE_FIELD_NUMBER: _ClassVar[int]
        CROSSTALK_V2_FIELD_NUMBER: _ClassVar[int]
        MIN_VOLTAGE_LIMIT_FIELD_NUMBER: _ClassVar[int]
        MAX_VOLTAGE_LIMIT_FIELD_NUMBER: _ClassVar[int]
        offset: float
        filter: QuaConfig.AnalogOutputPortFilter
        delay: int
        shareable: bool
        crosstalk: _containers.ScalarMap[int, float]
        sampling_rate: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate
        upsampling_mode: QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode
        output_mode: QuaConfig.OctoDacAnalogOutputPortDec.OutputMode
        crosstalk_v2: QuaConfig.OctoDacAnalogOutputPortDec.CrosstalkContainer
        min_voltage_limit: QuaConfig.OctoDacAnalogOutputPortDec.VoltageLimitContainer
        max_voltage_limit: QuaConfig.OctoDacAnalogOutputPortDec.VoltageLimitContainer
        def __init__(self, offset: _Optional[float] = ..., filter: _Optional[_Union[QuaConfig.AnalogOutputPortFilter, _Mapping]] = ..., delay: _Optional[int] = ..., shareable: bool = ..., crosstalk: _Optional[_Mapping[int, float]] = ..., sampling_rate: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRate, str]] = ..., upsampling_mode: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec.SamplingRateMode, str]] = ..., output_mode: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec.OutputMode, str]] = ..., crosstalk_v2: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec.CrosstalkContainer, _Mapping]] = ..., min_voltage_limit: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec.VoltageLimitContainer, _Mapping]] = ..., max_voltage_limit: _Optional[_Union[QuaConfig.OctoDacAnalogOutputPortDec.VoltageLimitContainer, _Mapping]] = ...) -> None: ...
    class ExponentialParameters(_message.Message):
        __slots__ = ["amplitude", "time_constant"]
        AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
        TIME_CONSTANT_FIELD_NUMBER: _ClassVar[int]
        amplitude: float
        time_constant: float
        def __init__(self, amplitude: _Optional[float] = ..., time_constant: _Optional[float] = ...) -> None: ...
    class IirFilter(_message.Message):
        __slots__ = ["exponential", "high_pass", "exponential_v2", "high_pass_v2", "exponential_dc_gain"]
        class ExponentialParametersContainer(_message.Message):
            __slots__ = ["value"]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: _containers.RepeatedCompositeFieldContainer[QuaConfig.ExponentialParameters]
            def __init__(self, value: _Optional[_Iterable[_Union[QuaConfig.ExponentialParameters, _Mapping]]] = ...) -> None: ...
        class HighPassContainer(_message.Message):
            __slots__ = ["value"]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: float
            def __init__(self, value: _Optional[float] = ...) -> None: ...
        class ExponentialDcGainContainer(_message.Message):
            __slots__ = ["value"]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: float
            def __init__(self, value: _Optional[float] = ...) -> None: ...
        EXPONENTIAL_FIELD_NUMBER: _ClassVar[int]
        HIGH_PASS_FIELD_NUMBER: _ClassVar[int]
        EXPONENTIAL_V2_FIELD_NUMBER: _ClassVar[int]
        HIGH_PASS_V2_FIELD_NUMBER: _ClassVar[int]
        EXPONENTIAL_DC_GAIN_FIELD_NUMBER: _ClassVar[int]
        exponential: _containers.RepeatedCompositeFieldContainer[QuaConfig.ExponentialParameters]
        high_pass: float
        exponential_v2: QuaConfig.IirFilter.ExponentialParametersContainer
        high_pass_v2: QuaConfig.IirFilter.HighPassContainer
        exponential_dc_gain: QuaConfig.IirFilter.ExponentialDcGainContainer
        def __init__(self, exponential: _Optional[_Iterable[_Union[QuaConfig.ExponentialParameters, _Mapping]]] = ..., high_pass: _Optional[float] = ..., exponential_v2: _Optional[_Union[QuaConfig.IirFilter.ExponentialParametersContainer, _Mapping]] = ..., high_pass_v2: _Optional[_Union[QuaConfig.IirFilter.HighPassContainer, _Mapping]] = ..., exponential_dc_gain: _Optional[_Union[QuaConfig.IirFilter.ExponentialDcGainContainer, _Mapping]] = ...) -> None: ...
    class AnalogOutputPortFilter(_message.Message):
        __slots__ = ["feedforward", "feedback", "iir", "feedforward_v2"]
        class FeedforwardContainer(_message.Message):
            __slots__ = ["value"]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            value: _containers.RepeatedScalarFieldContainer[float]
            def __init__(self, value: _Optional[_Iterable[float]] = ...) -> None: ...
        FEEDFORWARD_FIELD_NUMBER: _ClassVar[int]
        FEEDBACK_FIELD_NUMBER: _ClassVar[int]
        IIR_FIELD_NUMBER: _ClassVar[int]
        FEEDFORWARD_V2_FIELD_NUMBER: _ClassVar[int]
        feedforward: _containers.RepeatedScalarFieldContainer[float]
        feedback: _containers.RepeatedScalarFieldContainer[float]
        iir: QuaConfig.IirFilter
        feedforward_v2: QuaConfig.AnalogOutputPortFilter.FeedforwardContainer
        def __init__(self, feedforward: _Optional[_Iterable[float]] = ..., feedback: _Optional[_Iterable[float]] = ..., iir: _Optional[_Union[QuaConfig.IirFilter, _Mapping]] = ..., feedforward_v2: _Optional[_Union[QuaConfig.AnalogOutputPortFilter.FeedforwardContainer, _Mapping]] = ...) -> None: ...
    class AnalogInputPortDec(_message.Message):
        __slots__ = ["offset", "gainDb", "shareable", "samplingRate"]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        GAINDB_FIELD_NUMBER: _ClassVar[int]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        SAMPLINGRATE_FIELD_NUMBER: _ClassVar[int]
        offset: float
        gainDb: _wrappers_pb2.Int32Value
        shareable: bool
        samplingRate: float
        def __init__(self, offset: _Optional[float] = ..., gainDb: _Optional[_Union[_wrappers_pb2.Int32Value, _Mapping]] = ..., shareable: bool = ..., samplingRate: _Optional[float] = ...) -> None: ...
    class DigitalOutputPortDec(_message.Message):
        __slots__ = ["shareable", "inverted", "level"]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        INVERTED_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        shareable: bool
        inverted: bool
        level: QuaConfig.VoltageLevel
        def __init__(self, shareable: bool = ..., inverted: bool = ..., level: _Optional[_Union[QuaConfig.VoltageLevel, str]] = ...) -> None: ...
    class DigitalInputPortDec(_message.Message):
        __slots__ = ["deadtime", "polarity", "threshold", "shareable", "level"]
        class Polarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            RISING: _ClassVar[QuaConfig.DigitalInputPortDec.Polarity]
            FALLING: _ClassVar[QuaConfig.DigitalInputPortDec.Polarity]
        RISING: QuaConfig.DigitalInputPortDec.Polarity
        FALLING: QuaConfig.DigitalInputPortDec.Polarity
        DEADTIME_FIELD_NUMBER: _ClassVar[int]
        POLARITY_FIELD_NUMBER: _ClassVar[int]
        THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        SHAREABLE_FIELD_NUMBER: _ClassVar[int]
        LEVEL_FIELD_NUMBER: _ClassVar[int]
        deadtime: int
        polarity: QuaConfig.DigitalInputPortDec.Polarity
        threshold: float
        shareable: bool
        level: QuaConfig.VoltageLevel
        def __init__(self, deadtime: _Optional[int] = ..., polarity: _Optional[_Union[QuaConfig.DigitalInputPortDec.Polarity, str]] = ..., threshold: _Optional[float] = ..., shareable: bool = ..., level: _Optional[_Union[QuaConfig.VoltageLevel, str]] = ...) -> None: ...
    class MixerRef(_message.Message):
        __slots__ = ["mixer", "loFrequency", "loFrequencyDouble"]
        MIXER_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        mixer: str
        loFrequency: int
        loFrequencyDouble: float
        def __init__(self, mixer: _Optional[str] = ..., loFrequency: _Optional[int] = ..., loFrequencyDouble: _Optional[float] = ...) -> None: ...
    class Oscillator(_message.Message):
        __slots__ = ["intermediateFrequency", "mixer", "intermediateFrequencyDouble"]
        INTERMEDIATEFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        MIXER_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        intermediateFrequency: _wrappers_pb2.Int64Value
        mixer: QuaConfig.MixerRef
        intermediateFrequencyDouble: float
        def __init__(self, intermediateFrequency: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ..., mixer: _Optional[_Union[QuaConfig.MixerRef, _Mapping]] = ..., intermediateFrequencyDouble: _Optional[float] = ...) -> None: ...
    class SingleInput(_message.Message):
        __slots__ = ["port"]
        PORT_FIELD_NUMBER: _ClassVar[int]
        port: QuaConfig.DacPortReference
        def __init__(self, port: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ...) -> None: ...
    class MixInputs(_message.Message):
        __slots__ = ["I", "Q", "mixer", "loFrequency", "loFrequencyDouble"]
        I_FIELD_NUMBER: _ClassVar[int]
        Q_FIELD_NUMBER: _ClassVar[int]
        MIXER_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        I: QuaConfig.DacPortReference
        Q: QuaConfig.DacPortReference
        mixer: str
        loFrequency: int
        loFrequencyDouble: float
        def __init__(self, I: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ..., Q: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ..., mixer: _Optional[str] = ..., loFrequency: _Optional[int] = ..., loFrequencyDouble: _Optional[float] = ...) -> None: ...
    class SingleInputCollection(_message.Message):
        __slots__ = ["inputs"]
        class InputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DacPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ...) -> None: ...
        INPUTS_FIELD_NUMBER: _ClassVar[int]
        inputs: _containers.MessageMap[str, QuaConfig.DacPortReference]
        def __init__(self, inputs: _Optional[_Mapping[str, QuaConfig.DacPortReference]] = ...) -> None: ...
    class MultipleInputs(_message.Message):
        __slots__ = ["inputs"]
        class InputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DacPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ...) -> None: ...
        INPUTS_FIELD_NUMBER: _ClassVar[int]
        inputs: _containers.MessageMap[str, QuaConfig.DacPortReference]
        def __init__(self, inputs: _Optional[_Mapping[str, QuaConfig.DacPortReference]] = ...) -> None: ...
    class GeneralPortReference(_message.Message):
        __slots__ = ["device_name", "port"]
        DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
        PORT_FIELD_NUMBER: _ClassVar[int]
        device_name: str
        port: int
        def __init__(self, device_name: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...
    class MultipleOutputs(_message.Message):
        __slots__ = ["port_references"]
        class PortReferencesEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.AdcPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.AdcPortReference, _Mapping]] = ...) -> None: ...
        PORT_REFERENCES_FIELD_NUMBER: _ClassVar[int]
        port_references: _containers.MessageMap[str, QuaConfig.AdcPortReference]
        def __init__(self, port_references: _Optional[_Mapping[str, QuaConfig.AdcPortReference]] = ...) -> None: ...
    class ElementDec(_message.Message):
        __slots__ = ["outputs", "digitalInputs", "digitalOutputs", "RFInputs", "RFOutputs", "singleInput", "mixInputs", "singleInputCollection", "multipleInputs", "microwaveInput", "microwaveOutput", "multipleOutputs", "timeOfFlight", "smearing", "intermediateFrequency", "intermediateFrequencyDouble", "intermediateFrequencyNegative", "operations", "measurementQe", "outputPulseParameters", "holdOffset", "sticky", "thread", "intermediateFrequencyOscillator", "intermediateFrequencyOscillatorDouble", "namedOscillator", "noOscillator", "persistent"]
        class OutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.AdcPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.AdcPortReference, _Mapping]] = ...) -> None: ...
        class DigitalInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DigitalInputPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DigitalInputPortReference, _Mapping]] = ...) -> None: ...
        class DigitalOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.DigitalOutputPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.DigitalOutputPortReference, _Mapping]] = ...) -> None: ...
        class RFInputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.GeneralPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.GeneralPortReference, _Mapping]] = ...) -> None: ...
        class RFOutputsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: QuaConfig.GeneralPortReference
            def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[QuaConfig.GeneralPortReference, _Mapping]] = ...) -> None: ...
        class OperationsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        OUTPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALINPUTS_FIELD_NUMBER: _ClassVar[int]
        DIGITALOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        RFINPUTS_FIELD_NUMBER: _ClassVar[int]
        RFOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        SINGLEINPUT_FIELD_NUMBER: _ClassVar[int]
        MIXINPUTS_FIELD_NUMBER: _ClassVar[int]
        SINGLEINPUTCOLLECTION_FIELD_NUMBER: _ClassVar[int]
        MULTIPLEINPUTS_FIELD_NUMBER: _ClassVar[int]
        MICROWAVEINPUT_FIELD_NUMBER: _ClassVar[int]
        MICROWAVEOUTPUT_FIELD_NUMBER: _ClassVar[int]
        MULTIPLEOUTPUTS_FIELD_NUMBER: _ClassVar[int]
        TIMEOFFLIGHT_FIELD_NUMBER: _ClassVar[int]
        SMEARING_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCYNEGATIVE_FIELD_NUMBER: _ClassVar[int]
        OPERATIONS_FIELD_NUMBER: _ClassVar[int]
        MEASUREMENTQE_FIELD_NUMBER: _ClassVar[int]
        OUTPUTPULSEPARAMETERS_FIELD_NUMBER: _ClassVar[int]
        HOLDOFFSET_FIELD_NUMBER: _ClassVar[int]
        STICKY_FIELD_NUMBER: _ClassVar[int]
        THREAD_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCYOSCILLATOR_FIELD_NUMBER: _ClassVar[int]
        INTERMEDIATEFREQUENCYOSCILLATORDOUBLE_FIELD_NUMBER: _ClassVar[int]
        NAMEDOSCILLATOR_FIELD_NUMBER: _ClassVar[int]
        NOOSCILLATOR_FIELD_NUMBER: _ClassVar[int]
        PERSISTENT_FIELD_NUMBER: _ClassVar[int]
        outputs: _containers.MessageMap[str, QuaConfig.AdcPortReference]
        digitalInputs: _containers.MessageMap[str, QuaConfig.DigitalInputPortReference]
        digitalOutputs: _containers.MessageMap[str, QuaConfig.DigitalOutputPortReference]
        RFInputs: _containers.MessageMap[str, QuaConfig.GeneralPortReference]
        RFOutputs: _containers.MessageMap[str, QuaConfig.GeneralPortReference]
        singleInput: QuaConfig.SingleInput
        mixInputs: QuaConfig.MixInputs
        singleInputCollection: QuaConfig.SingleInputCollection
        multipleInputs: QuaConfig.MultipleInputs
        microwaveInput: QuaConfig.MicrowaveInputPortReference
        microwaveOutput: QuaConfig.MicrowaveOutputPortReference
        multipleOutputs: QuaConfig.MultipleOutputs
        timeOfFlight: _wrappers_pb2.UInt32Value
        smearing: _wrappers_pb2.UInt32Value
        intermediateFrequency: _wrappers_pb2.UInt64Value
        intermediateFrequencyDouble: float
        intermediateFrequencyNegative: bool
        operations: _containers.ScalarMap[str, str]
        measurementQe: _wrappers_pb2.StringValue
        outputPulseParameters: QuaConfig.OutputPulseParameters
        holdOffset: QuaConfig.HoldOffset
        sticky: QuaConfig.Sticky
        thread: QuaConfig.ElementThread
        intermediateFrequencyOscillator: _wrappers_pb2.Int64Value
        intermediateFrequencyOscillatorDouble: float
        namedOscillator: _wrappers_pb2.StringValue
        noOscillator: _empty_pb2.Empty
        persistent: bool
        def __init__(self, outputs: _Optional[_Mapping[str, QuaConfig.AdcPortReference]] = ..., digitalInputs: _Optional[_Mapping[str, QuaConfig.DigitalInputPortReference]] = ..., digitalOutputs: _Optional[_Mapping[str, QuaConfig.DigitalOutputPortReference]] = ..., RFInputs: _Optional[_Mapping[str, QuaConfig.GeneralPortReference]] = ..., RFOutputs: _Optional[_Mapping[str, QuaConfig.GeneralPortReference]] = ..., singleInput: _Optional[_Union[QuaConfig.SingleInput, _Mapping]] = ..., mixInputs: _Optional[_Union[QuaConfig.MixInputs, _Mapping]] = ..., singleInputCollection: _Optional[_Union[QuaConfig.SingleInputCollection, _Mapping]] = ..., multipleInputs: _Optional[_Union[QuaConfig.MultipleInputs, _Mapping]] = ..., microwaveInput: _Optional[_Union[QuaConfig.MicrowaveInputPortReference, _Mapping]] = ..., microwaveOutput: _Optional[_Union[QuaConfig.MicrowaveOutputPortReference, _Mapping]] = ..., multipleOutputs: _Optional[_Union[QuaConfig.MultipleOutputs, _Mapping]] = ..., timeOfFlight: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., smearing: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ..., intermediateFrequency: _Optional[_Union[_wrappers_pb2.UInt64Value, _Mapping]] = ..., intermediateFrequencyDouble: _Optional[float] = ..., intermediateFrequencyNegative: bool = ..., operations: _Optional[_Mapping[str, str]] = ..., measurementQe: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., outputPulseParameters: _Optional[_Union[QuaConfig.OutputPulseParameters, _Mapping]] = ..., holdOffset: _Optional[_Union[QuaConfig.HoldOffset, _Mapping]] = ..., sticky: _Optional[_Union[QuaConfig.Sticky, _Mapping]] = ..., thread: _Optional[_Union[QuaConfig.ElementThread, _Mapping]] = ..., intermediateFrequencyOscillator: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ..., intermediateFrequencyOscillatorDouble: _Optional[float] = ..., namedOscillator: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., noOscillator: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., persistent: bool = ...) -> None: ...
    class ElementThread(_message.Message):
        __slots__ = ["threadName"]
        THREADNAME_FIELD_NUMBER: _ClassVar[int]
        threadName: str
        def __init__(self, threadName: _Optional[str] = ...) -> None: ...
    class OutputPulseParameters(_message.Message):
        __slots__ = ["threshold", "table", "signalThreshold", "signalPolarity", "derivativeThreshold", "derivativePolarity"]
        class Polarity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            ASCENDING: _ClassVar[QuaConfig.OutputPulseParameters.Polarity]
            DESCENDING: _ClassVar[QuaConfig.OutputPulseParameters.Polarity]
        ASCENDING: QuaConfig.OutputPulseParameters.Polarity
        DESCENDING: QuaConfig.OutputPulseParameters.Polarity
        THRESHOLD_FIELD_NUMBER: _ClassVar[int]
        TABLE_FIELD_NUMBER: _ClassVar[int]
        SIGNALTHRESHOLD_FIELD_NUMBER: _ClassVar[int]
        SIGNALPOLARITY_FIELD_NUMBER: _ClassVar[int]
        DERIVATIVETHRESHOLD_FIELD_NUMBER: _ClassVar[int]
        DERIVATIVEPOLARITY_FIELD_NUMBER: _ClassVar[int]
        threshold: int
        table: _containers.RepeatedScalarFieldContainer[int]
        signalThreshold: int
        signalPolarity: QuaConfig.OutputPulseParameters.Polarity
        derivativeThreshold: int
        derivativePolarity: QuaConfig.OutputPulseParameters.Polarity
        def __init__(self, threshold: _Optional[int] = ..., table: _Optional[_Iterable[int]] = ..., signalThreshold: _Optional[int] = ..., signalPolarity: _Optional[_Union[QuaConfig.OutputPulseParameters.Polarity, str]] = ..., derivativeThreshold: _Optional[int] = ..., derivativePolarity: _Optional[_Union[QuaConfig.OutputPulseParameters.Polarity, str]] = ...) -> None: ...
    class HoldOffset(_message.Message):
        __slots__ = ["duration"]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        duration: int
        def __init__(self, duration: _Optional[int] = ...) -> None: ...
    class Sticky(_message.Message):
        __slots__ = ["analog", "digital", "duration"]
        ANALOG_FIELD_NUMBER: _ClassVar[int]
        DIGITAL_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        analog: bool
        digital: bool
        duration: int
        def __init__(self, analog: bool = ..., digital: bool = ..., duration: _Optional[int] = ...) -> None: ...
    class DacPortReference(_message.Message):
        __slots__ = ["controller", "number", "fem"]
        CONTROLLER_FIELD_NUMBER: _ClassVar[int]
        NUMBER_FIELD_NUMBER: _ClassVar[int]
        FEM_FIELD_NUMBER: _ClassVar[int]
        controller: str
        number: int
        fem: int
        def __init__(self, controller: _Optional[str] = ..., number: _Optional[int] = ..., fem: _Optional[int] = ...) -> None: ...
    class AdcPortReference(_message.Message):
        __slots__ = ["controller", "number", "fem"]
        CONTROLLER_FIELD_NUMBER: _ClassVar[int]
        NUMBER_FIELD_NUMBER: _ClassVar[int]
        FEM_FIELD_NUMBER: _ClassVar[int]
        controller: str
        number: int
        fem: int
        def __init__(self, controller: _Optional[str] = ..., number: _Optional[int] = ..., fem: _Optional[int] = ...) -> None: ...
    class DigitalInputPortReference(_message.Message):
        __slots__ = ["port", "delay", "buffer"]
        PORT_FIELD_NUMBER: _ClassVar[int]
        DELAY_FIELD_NUMBER: _ClassVar[int]
        BUFFER_FIELD_NUMBER: _ClassVar[int]
        port: QuaConfig.PortReference
        delay: int
        buffer: int
        def __init__(self, port: _Optional[_Union[QuaConfig.PortReference, _Mapping]] = ..., delay: _Optional[int] = ..., buffer: _Optional[int] = ...) -> None: ...
    class DigitalOutputPortReference(_message.Message):
        __slots__ = ["port"]
        PORT_FIELD_NUMBER: _ClassVar[int]
        port: QuaConfig.PortReference
        def __init__(self, port: _Optional[_Union[QuaConfig.PortReference, _Mapping]] = ...) -> None: ...
    class PortReference(_message.Message):
        __slots__ = ["controller", "number", "fem"]
        CONTROLLER_FIELD_NUMBER: _ClassVar[int]
        NUMBER_FIELD_NUMBER: _ClassVar[int]
        FEM_FIELD_NUMBER: _ClassVar[int]
        controller: str
        number: int
        fem: int
        def __init__(self, controller: _Optional[str] = ..., number: _Optional[int] = ..., fem: _Optional[int] = ...) -> None: ...
    class MicrowaveInputPortReference(_message.Message):
        __slots__ = ["port", "upconverter"]
        PORT_FIELD_NUMBER: _ClassVar[int]
        UPCONVERTER_FIELD_NUMBER: _ClassVar[int]
        port: QuaConfig.DacPortReference
        upconverter: int
        def __init__(self, port: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ..., upconverter: _Optional[int] = ...) -> None: ...
    class MicrowaveOutputPortReference(_message.Message):
        __slots__ = ["port"]
        PORT_FIELD_NUMBER: _ClassVar[int]
        port: QuaConfig.AdcPortReference
        def __init__(self, port: _Optional[_Union[QuaConfig.AdcPortReference, _Mapping]] = ...) -> None: ...
    class PulseDec(_message.Message):
        __slots__ = ["length", "operation", "waveforms", "digitalMarker", "integrationWeights"]
        class Operation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            MEASUREMENT: _ClassVar[QuaConfig.PulseDec.Operation]
            CONTROL: _ClassVar[QuaConfig.PulseDec.Operation]
        MEASUREMENT: QuaConfig.PulseDec.Operation
        CONTROL: QuaConfig.PulseDec.Operation
        class WaveformsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        class IntegrationWeightsEntry(_message.Message):
            __slots__ = ["key", "value"]
            KEY_FIELD_NUMBER: _ClassVar[int]
            VALUE_FIELD_NUMBER: _ClassVar[int]
            key: str
            value: str
            def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        WAVEFORMS_FIELD_NUMBER: _ClassVar[int]
        DIGITALMARKER_FIELD_NUMBER: _ClassVar[int]
        INTEGRATIONWEIGHTS_FIELD_NUMBER: _ClassVar[int]
        length: int
        operation: int
        waveforms: _containers.ScalarMap[str, str]
        digitalMarker: _wrappers_pb2.StringValue
        integrationWeights: _containers.ScalarMap[str, str]
        def __init__(self, length: _Optional[int] = ..., operation: _Optional[int] = ..., waveforms: _Optional[_Mapping[str, str]] = ..., digitalMarker: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., integrationWeights: _Optional[_Mapping[str, str]] = ...) -> None: ...
    class WaveformDec(_message.Message):
        __slots__ = ["arbitrary", "constant", "compressed", "array"]
        ARBITRARY_FIELD_NUMBER: _ClassVar[int]
        CONSTANT_FIELD_NUMBER: _ClassVar[int]
        COMPRESSED_FIELD_NUMBER: _ClassVar[int]
        ARRAY_FIELD_NUMBER: _ClassVar[int]
        arbitrary: QuaConfig.ArbitraryWaveformDec
        constant: QuaConfig.ConstantWaveformDec
        compressed: QuaConfig.CompressedWaveformDec
        array: QuaConfig.WaveformArrayDec
        def __init__(self, arbitrary: _Optional[_Union[QuaConfig.ArbitraryWaveformDec, _Mapping]] = ..., constant: _Optional[_Union[QuaConfig.ConstantWaveformDec, _Mapping]] = ..., compressed: _Optional[_Union[QuaConfig.CompressedWaveformDec, _Mapping]] = ..., array: _Optional[_Union[QuaConfig.WaveformArrayDec, _Mapping]] = ...) -> None: ...
    class ArbitraryWaveformDec(_message.Message):
        __slots__ = ["samples", "multiplier", "deprecatedMaxAllowedError", "maxAllowedError", "samplingRate", "isOverridable"]
        SAMPLES_FIELD_NUMBER: _ClassVar[int]
        MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
        DEPRECATEDMAXALLOWEDERROR_FIELD_NUMBER: _ClassVar[int]
        MAXALLOWEDERROR_FIELD_NUMBER: _ClassVar[int]
        SAMPLINGRATE_FIELD_NUMBER: _ClassVar[int]
        ISOVERRIDABLE_FIELD_NUMBER: _ClassVar[int]
        samples: _containers.RepeatedScalarFieldContainer[float]
        multiplier: float
        deprecatedMaxAllowedError: float
        maxAllowedError: _wrappers_pb2.DoubleValue
        samplingRate: _wrappers_pb2.DoubleValue
        isOverridable: bool
        def __init__(self, samples: _Optional[_Iterable[float]] = ..., multiplier: _Optional[float] = ..., deprecatedMaxAllowedError: _Optional[float] = ..., maxAllowedError: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., samplingRate: _Optional[_Union[_wrappers_pb2.DoubleValue, _Mapping]] = ..., isOverridable: bool = ...) -> None: ...
    class ConstantWaveformDec(_message.Message):
        __slots__ = ["sample", "multiplier"]
        SAMPLE_FIELD_NUMBER: _ClassVar[int]
        MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
        sample: float
        multiplier: float
        def __init__(self, sample: _Optional[float] = ..., multiplier: _Optional[float] = ...) -> None: ...
    class WaveformArrayDec(_message.Message):
        __slots__ = ["samples_array"]
        SAMPLES_ARRAY_FIELD_NUMBER: _ClassVar[int]
        samples_array: _containers.RepeatedCompositeFieldContainer[QuaConfig.WaveformSamples]
        def __init__(self, samples_array: _Optional[_Iterable[_Union[QuaConfig.WaveformSamples, _Mapping]]] = ...) -> None: ...
    class WaveformSamples(_message.Message):
        __slots__ = ["samples"]
        SAMPLES_FIELD_NUMBER: _ClassVar[int]
        samples: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, samples: _Optional[_Iterable[float]] = ...) -> None: ...
    class CompressedWaveformDec(_message.Message):
        __slots__ = ["samples", "sampleRate"]
        SAMPLES_FIELD_NUMBER: _ClassVar[int]
        SAMPLERATE_FIELD_NUMBER: _ClassVar[int]
        samples: _containers.RepeatedScalarFieldContainer[float]
        sampleRate: float
        def __init__(self, samples: _Optional[_Iterable[float]] = ..., sampleRate: _Optional[float] = ...) -> None: ...
    class DigitalWaveformDec(_message.Message):
        __slots__ = ["samples"]
        SAMPLES_FIELD_NUMBER: _ClassVar[int]
        samples: _containers.RepeatedCompositeFieldContainer[QuaConfig.DigitalWaveformSample]
        def __init__(self, samples: _Optional[_Iterable[_Union[QuaConfig.DigitalWaveformSample, _Mapping]]] = ...) -> None: ...
    class DigitalWaveformSample(_message.Message):
        __slots__ = ["value", "length"]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        value: bool
        length: int
        def __init__(self, value: bool = ..., length: _Optional[int] = ...) -> None: ...
    class MixerDec(_message.Message):
        __slots__ = ["correction"]
        CORRECTION_FIELD_NUMBER: _ClassVar[int]
        correction: _containers.RepeatedCompositeFieldContainer[QuaConfig.CorrectionEntry]
        def __init__(self, correction: _Optional[_Iterable[_Union[QuaConfig.CorrectionEntry, _Mapping]]] = ...) -> None: ...
    class IntegrationWeightDec(_message.Message):
        __slots__ = ["cosine", "sine"]
        COSINE_FIELD_NUMBER: _ClassVar[int]
        SINE_FIELD_NUMBER: _ClassVar[int]
        cosine: _containers.RepeatedCompositeFieldContainer[QuaConfig.IntegrationWeightSample]
        sine: _containers.RepeatedCompositeFieldContainer[QuaConfig.IntegrationWeightSample]
        def __init__(self, cosine: _Optional[_Iterable[_Union[QuaConfig.IntegrationWeightSample, _Mapping]]] = ..., sine: _Optional[_Iterable[_Union[QuaConfig.IntegrationWeightSample, _Mapping]]] = ...) -> None: ...
    class IntegrationWeightSample(_message.Message):
        __slots__ = ["value", "length"]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        LENGTH_FIELD_NUMBER: _ClassVar[int]
        value: float
        length: int
        def __init__(self, value: _Optional[float] = ..., length: _Optional[int] = ...) -> None: ...
    class CorrectionEntry(_message.Message):
        __slots__ = ["frequency", "loFrequency", "correction", "frequencyNegative", "frequencyDouble", "loFrequencyDouble"]
        FREQUENCY_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        CORRECTION_FIELD_NUMBER: _ClassVar[int]
        FREQUENCYNEGATIVE_FIELD_NUMBER: _ClassVar[int]
        FREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        LOFREQUENCYDOUBLE_FIELD_NUMBER: _ClassVar[int]
        frequency: int
        loFrequency: int
        correction: QuaConfig.Matrix
        frequencyNegative: bool
        frequencyDouble: float
        loFrequencyDouble: float
        def __init__(self, frequency: _Optional[int] = ..., loFrequency: _Optional[int] = ..., correction: _Optional[_Union[QuaConfig.Matrix, _Mapping]] = ..., frequencyNegative: bool = ..., frequencyDouble: _Optional[float] = ..., loFrequencyDouble: _Optional[float] = ...) -> None: ...
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
    class Octave(_message.Message):
        __slots__ = []
        class SynthesizerOutputName(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            synth1: _ClassVar[QuaConfig.Octave.SynthesizerOutputName]
            synth2: _ClassVar[QuaConfig.Octave.SynthesizerOutputName]
            synth3: _ClassVar[QuaConfig.Octave.SynthesizerOutputName]
            synth4: _ClassVar[QuaConfig.Octave.SynthesizerOutputName]
            synth5: _ClassVar[QuaConfig.Octave.SynthesizerOutputName]
        synth1: QuaConfig.Octave.SynthesizerOutputName
        synth2: QuaConfig.Octave.SynthesizerOutputName
        synth3: QuaConfig.Octave.SynthesizerOutputName
        synth4: QuaConfig.Octave.SynthesizerOutputName
        synth5: QuaConfig.Octave.SynthesizerOutputName
        class LOSourceInput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            not_set: _ClassVar[QuaConfig.Octave.LOSourceInput]
            internal: _ClassVar[QuaConfig.Octave.LOSourceInput]
            external: _ClassVar[QuaConfig.Octave.LOSourceInput]
            analyzer: _ClassVar[QuaConfig.Octave.LOSourceInput]
        not_set: QuaConfig.Octave.LOSourceInput
        internal: QuaConfig.Octave.LOSourceInput
        external: QuaConfig.Octave.LOSourceInput
        analyzer: QuaConfig.Octave.LOSourceInput
        class LoopbackInput(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            undefined: _ClassVar[QuaConfig.Octave.LoopbackInput]
            LO1: _ClassVar[QuaConfig.Octave.LoopbackInput]
            LO2: _ClassVar[QuaConfig.Octave.LoopbackInput]
            LO3: _ClassVar[QuaConfig.Octave.LoopbackInput]
            LO4: _ClassVar[QuaConfig.Octave.LoopbackInput]
            LO5: _ClassVar[QuaConfig.Octave.LoopbackInput]
            Dmd1LO: _ClassVar[QuaConfig.Octave.LoopbackInput]
            Dmd2LO: _ClassVar[QuaConfig.Octave.LoopbackInput]
        undefined: QuaConfig.Octave.LoopbackInput
        LO1: QuaConfig.Octave.LoopbackInput
        LO2: QuaConfig.Octave.LoopbackInput
        LO3: QuaConfig.Octave.LoopbackInput
        LO4: QuaConfig.Octave.LoopbackInput
        LO5: QuaConfig.Octave.LoopbackInput
        Dmd1LO: QuaConfig.Octave.LoopbackInput
        Dmd2LO: QuaConfig.Octave.LoopbackInput
        class DownconverterRFSource(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            rf_in: _ClassVar[QuaConfig.Octave.DownconverterRFSource]
            loopback_1: _ClassVar[QuaConfig.Octave.DownconverterRFSource]
            loopback_2: _ClassVar[QuaConfig.Octave.DownconverterRFSource]
            loopback_3: _ClassVar[QuaConfig.Octave.DownconverterRFSource]
            loopback_4: _ClassVar[QuaConfig.Octave.DownconverterRFSource]
            loopback_5: _ClassVar[QuaConfig.Octave.DownconverterRFSource]
        rf_in: QuaConfig.Octave.DownconverterRFSource
        loopback_1: QuaConfig.Octave.DownconverterRFSource
        loopback_2: QuaConfig.Octave.DownconverterRFSource
        loopback_3: QuaConfig.Octave.DownconverterRFSource
        loopback_4: QuaConfig.Octave.DownconverterRFSource
        loopback_5: QuaConfig.Octave.DownconverterRFSource
        class OutputSwitchState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            unset: _ClassVar[QuaConfig.Octave.OutputSwitchState]
            always_on: _ClassVar[QuaConfig.Octave.OutputSwitchState]
            always_off: _ClassVar[QuaConfig.Octave.OutputSwitchState]
            triggered: _ClassVar[QuaConfig.Octave.OutputSwitchState]
            triggered_reversed: _ClassVar[QuaConfig.Octave.OutputSwitchState]
        unset: QuaConfig.Octave.OutputSwitchState
        always_on: QuaConfig.Octave.OutputSwitchState
        always_off: QuaConfig.Octave.OutputSwitchState
        triggered: QuaConfig.Octave.OutputSwitchState
        triggered_reversed: QuaConfig.Octave.OutputSwitchState
        class IFMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            direct: _ClassVar[QuaConfig.Octave.IFMode]
            mixer: _ClassVar[QuaConfig.Octave.IFMode]
            envelope: _ClassVar[QuaConfig.Octave.IFMode]
            off: _ClassVar[QuaConfig.Octave.IFMode]
        direct: QuaConfig.Octave.IFMode
        mixer: QuaConfig.Octave.IFMode
        envelope: QuaConfig.Octave.IFMode
        off: QuaConfig.Octave.IFMode
        class Config(_message.Message):
            __slots__ = ["loopbacks", "rf_outputs", "rf_inputs", "if_outputs"]
            class RfOutputsEntry(_message.Message):
                __slots__ = ["key", "value"]
                KEY_FIELD_NUMBER: _ClassVar[int]
                VALUE_FIELD_NUMBER: _ClassVar[int]
                key: int
                value: QuaConfig.Octave.RFOutputConfig
                def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.Octave.RFOutputConfig, _Mapping]] = ...) -> None: ...
            class RfInputsEntry(_message.Message):
                __slots__ = ["key", "value"]
                KEY_FIELD_NUMBER: _ClassVar[int]
                VALUE_FIELD_NUMBER: _ClassVar[int]
                key: int
                value: QuaConfig.Octave.RFInputConfig
                def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[QuaConfig.Octave.RFInputConfig, _Mapping]] = ...) -> None: ...
            LOOPBACKS_FIELD_NUMBER: _ClassVar[int]
            RF_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
            RF_INPUTS_FIELD_NUMBER: _ClassVar[int]
            IF_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
            loopbacks: _containers.RepeatedCompositeFieldContainer[QuaConfig.Octave.Loopback]
            rf_outputs: _containers.MessageMap[int, QuaConfig.Octave.RFOutputConfig]
            rf_inputs: _containers.MessageMap[int, QuaConfig.Octave.RFInputConfig]
            if_outputs: QuaConfig.Octave.IFOutputsConfig
            def __init__(self, loopbacks: _Optional[_Iterable[_Union[QuaConfig.Octave.Loopback, _Mapping]]] = ..., rf_outputs: _Optional[_Mapping[int, QuaConfig.Octave.RFOutputConfig]] = ..., rf_inputs: _Optional[_Mapping[int, QuaConfig.Octave.RFInputConfig]] = ..., if_outputs: _Optional[_Union[QuaConfig.Octave.IFOutputsConfig, _Mapping]] = ...) -> None: ...
        class Loopback(_message.Message):
            __slots__ = ["lo_source_input", "lo_source_generator"]
            LO_SOURCE_INPUT_FIELD_NUMBER: _ClassVar[int]
            LO_SOURCE_GENERATOR_FIELD_NUMBER: _ClassVar[int]
            lo_source_input: QuaConfig.Octave.LoopbackInput
            lo_source_generator: QuaConfig.Octave.SynthesizerPort
            def __init__(self, lo_source_input: _Optional[_Union[QuaConfig.Octave.LoopbackInput, str]] = ..., lo_source_generator: _Optional[_Union[QuaConfig.Octave.SynthesizerPort, _Mapping]] = ...) -> None: ...
        class SynthesizerPort(_message.Message):
            __slots__ = ["device_name", "port_name"]
            DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
            PORT_NAME_FIELD_NUMBER: _ClassVar[int]
            device_name: str
            port_name: QuaConfig.Octave.SynthesizerOutputName
            def __init__(self, device_name: _Optional[str] = ..., port_name: _Optional[_Union[QuaConfig.Octave.SynthesizerOutputName, str]] = ...) -> None: ...
        class RFOutputConfig(_message.Message):
            __slots__ = ["LO_frequency", "LO_source", "output_mode", "gain", "input_attenuators", "I_connection", "Q_connection"]
            LO_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
            LO_SOURCE_FIELD_NUMBER: _ClassVar[int]
            OUTPUT_MODE_FIELD_NUMBER: _ClassVar[int]
            GAIN_FIELD_NUMBER: _ClassVar[int]
            INPUT_ATTENUATORS_FIELD_NUMBER: _ClassVar[int]
            I_CONNECTION_FIELD_NUMBER: _ClassVar[int]
            Q_CONNECTION_FIELD_NUMBER: _ClassVar[int]
            LO_frequency: float
            LO_source: QuaConfig.Octave.LOSourceInput
            output_mode: QuaConfig.Octave.OutputSwitchState
            gain: float
            input_attenuators: bool
            I_connection: QuaConfig.DacPortReference
            Q_connection: QuaConfig.DacPortReference
            def __init__(self, LO_frequency: _Optional[float] = ..., LO_source: _Optional[_Union[QuaConfig.Octave.LOSourceInput, str]] = ..., output_mode: _Optional[_Union[QuaConfig.Octave.OutputSwitchState, str]] = ..., gain: _Optional[float] = ..., input_attenuators: bool = ..., I_connection: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ..., Q_connection: _Optional[_Union[QuaConfig.DacPortReference, _Mapping]] = ...) -> None: ...
        class RFInputConfig(_message.Message):
            __slots__ = ["RF_source", "LO_frequency", "LO_source", "IF_mode_I", "IF_mode_Q"]
            RF_SOURCE_FIELD_NUMBER: _ClassVar[int]
            LO_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
            LO_SOURCE_FIELD_NUMBER: _ClassVar[int]
            IF_MODE_I_FIELD_NUMBER: _ClassVar[int]
            IF_MODE_Q_FIELD_NUMBER: _ClassVar[int]
            RF_source: QuaConfig.Octave.DownconverterRFSource
            LO_frequency: float
            LO_source: QuaConfig.Octave.LOSourceInput
            IF_mode_I: QuaConfig.Octave.IFMode
            IF_mode_Q: QuaConfig.Octave.IFMode
            def __init__(self, RF_source: _Optional[_Union[QuaConfig.Octave.DownconverterRFSource, str]] = ..., LO_frequency: _Optional[float] = ..., LO_source: _Optional[_Union[QuaConfig.Octave.LOSourceInput, str]] = ..., IF_mode_I: _Optional[_Union[QuaConfig.Octave.IFMode, str]] = ..., IF_mode_Q: _Optional[_Union[QuaConfig.Octave.IFMode, str]] = ...) -> None: ...
        class SingleIFOutputConfig(_message.Message):
            __slots__ = ["port", "name"]
            PORT_FIELD_NUMBER: _ClassVar[int]
            NAME_FIELD_NUMBER: _ClassVar[int]
            port: QuaConfig.AdcPortReference
            name: str
            def __init__(self, port: _Optional[_Union[QuaConfig.AdcPortReference, _Mapping]] = ..., name: _Optional[str] = ...) -> None: ...
        class IFOutputsConfig(_message.Message):
            __slots__ = ["IF_out1", "IF_out2"]
            IF_OUT1_FIELD_NUMBER: _ClassVar[int]
            IF_OUT2_FIELD_NUMBER: _ClassVar[int]
            IF_out1: QuaConfig.Octave.SingleIFOutputConfig
            IF_out2: QuaConfig.Octave.SingleIFOutputConfig
            def __init__(self, IF_out1: _Optional[_Union[QuaConfig.Octave.SingleIFOutputConfig, _Mapping]] = ..., IF_out2: _Optional[_Union[QuaConfig.Octave.SingleIFOutputConfig, _Mapping]] = ...) -> None: ...
        def __init__(self) -> None: ...
    V1BETA_FIELD_NUMBER: _ClassVar[int]
    V2_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    v1beta: QuaConfig.QuaConfigV1
    v2: QuaConfig.QuaConfigV2
    revision: int
    def __init__(self, v1beta: _Optional[_Union[QuaConfig.QuaConfigV1, _Mapping]] = ..., v2: _Optional[_Union[QuaConfig.QuaConfigV2, _Mapping]] = ..., revision: _Optional[int] = ...) -> None: ...
