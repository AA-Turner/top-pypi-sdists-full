from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from qm.grpc.qm.pb import inc_qua_config_pb2 as _inc_qua_config_pb2
from google.protobuf import any_pb2 as _any_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuaProgram(_message.Message):
    __slots__ = ["config", "dynConfig", "script", "compilerOptions", "resultAnalysis", "config_update"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        INT: _ClassVar[QuaProgram.Type]
        BOOL: _ClassVar[QuaProgram.Type]
        REAL: _ClassVar[QuaProgram.Type]
    INT: QuaProgram.Type
    BOOL: QuaProgram.Type
    REAL: QuaProgram.Type
    class Direction(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        INCOMING: _ClassVar[QuaProgram.Direction]
        OUTGOING: _ClassVar[QuaProgram.Direction]
    INCOMING: QuaProgram.Direction
    OUTGOING: QuaProgram.Direction
    class GlobalVarOperation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        read: _ClassVar[QuaProgram.GlobalVarOperation]
        read_shift: _ClassVar[QuaProgram.GlobalVarOperation]
        xor: _ClassVar[QuaProgram.GlobalVarOperation]
    read: QuaProgram.GlobalVarOperation
    read_shift: QuaProgram.GlobalVarOperation
    xor: QuaProgram.GlobalVarOperation
    class CompilerOptions(_message.Message):
        __slots__ = ["useExperimentalCalculationCompiler", "optimizeMergeCodeExecution", "optimizeWriteReadCommands", "skipOptimizations", "strict", "flags"]
        USEEXPERIMENTALCALCULATIONCOMPILER_FIELD_NUMBER: _ClassVar[int]
        OPTIMIZEMERGECODEEXECUTION_FIELD_NUMBER: _ClassVar[int]
        OPTIMIZEWRITEREADCOMMANDS_FIELD_NUMBER: _ClassVar[int]
        SKIPOPTIMIZATIONS_FIELD_NUMBER: _ClassVar[int]
        STRICT_FIELD_NUMBER: _ClassVar[int]
        FLAGS_FIELD_NUMBER: _ClassVar[int]
        useExperimentalCalculationCompiler: bool
        optimizeMergeCodeExecution: bool
        optimizeWriteReadCommands: bool
        skipOptimizations: _containers.RepeatedScalarFieldContainer[str]
        strict: bool
        flags: _containers.RepeatedScalarFieldContainer[str]
        def __init__(self, useExperimentalCalculationCompiler: bool = ..., optimizeMergeCodeExecution: bool = ..., optimizeWriteReadCommands: bool = ..., skipOptimizations: _Optional[_Iterable[str]] = ..., strict: bool = ..., flags: _Optional[_Iterable[str]] = ...) -> None: ...
    class Script(_message.Message):
        __slots__ = ["variables", "externalStreams", "body"]
        VARIABLES_FIELD_NUMBER: _ClassVar[int]
        EXTERNALSTREAMS_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        variables: _containers.RepeatedCompositeFieldContainer[QuaProgram.VarDeclaration]
        externalStreams: _containers.RepeatedCompositeFieldContainer[QuaProgram.ExternalStreamDeclaration]
        body: QuaProgram.StatementsCollection
        def __init__(self, variables: _Optional[_Iterable[_Union[QuaProgram.VarDeclaration, _Mapping]]] = ..., externalStreams: _Optional[_Iterable[_Union[QuaProgram.ExternalStreamDeclaration, _Mapping]]] = ..., body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ...) -> None: ...
    class VarDeclaration(_message.Message):
        __slots__ = ["name", "type", "size", "value", "dim", "isInputStream", "structMember"]
        class StructMember(_message.Message):
            __slots__ = ["name", "position"]
            NAME_FIELD_NUMBER: _ClassVar[int]
            POSITION_FIELD_NUMBER: _ClassVar[int]
            name: str
            position: int
            def __init__(self, name: _Optional[str] = ..., position: _Optional[int] = ...) -> None: ...
        NAME_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        SIZE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        DIM_FIELD_NUMBER: _ClassVar[int]
        ISINPUTSTREAM_FIELD_NUMBER: _ClassVar[int]
        STRUCTMEMBER_FIELD_NUMBER: _ClassVar[int]
        name: str
        type: QuaProgram.Type
        size: int
        value: _containers.RepeatedCompositeFieldContainer[QuaProgram.LiteralExpression]
        dim: int
        isInputStream: bool
        structMember: QuaProgram.VarDeclaration.StructMember
        def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[QuaProgram.Type, str]] = ..., size: _Optional[int] = ..., value: _Optional[_Iterable[_Union[QuaProgram.LiteralExpression, _Mapping]]] = ..., dim: _Optional[int] = ..., isInputStream: bool = ..., structMember: _Optional[_Union[QuaProgram.VarDeclaration.StructMember, _Mapping]] = ...) -> None: ...
    class ExternalStreamDeclaration(_message.Message):
        __slots__ = ["stream_id", "expectedTypes", "direction"]
        STREAM_ID_FIELD_NUMBER: _ClassVar[int]
        EXPECTEDTYPES_FIELD_NUMBER: _ClassVar[int]
        DIRECTION_FIELD_NUMBER: _ClassVar[int]
        stream_id: int
        expectedTypes: _containers.RepeatedCompositeFieldContainer[QuaProgram.VarDeclaration]
        direction: QuaProgram.Direction
        def __init__(self, stream_id: _Optional[int] = ..., expectedTypes: _Optional[_Iterable[_Union[QuaProgram.VarDeclaration, _Mapping]]] = ..., direction: _Optional[_Union[QuaProgram.Direction, str]] = ...) -> None: ...
    class QuantumElementReference(_message.Message):
        __slots__ = ["loc", "name"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        loc: str
        name: str
        def __init__(self, loc: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    class PulseReference(_message.Message):
        __slots__ = ["loc", "name"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        loc: str
        name: str
        def __init__(self, loc: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    class IntegrationWeightReference(_message.Message):
        __slots__ = ["loc", "name"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        loc: str
        name: str
        def __init__(self, loc: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
    class AnyStatement(_message.Message):
        __slots__ = ["play", "measure", "wait", "sync", "assign", "rus", "align", "updateFrequency", "zRotation", "pause", "save", "forEach", "waitForTrigger", "qrun", "updateCorrection", "resetPhase", "rampToZero", "resetFrame", "setDcOffset", "advanceInputStream", "strictTiming", "fastFrameRotation", "updateOscillatorFrequency", "resetGlobalPhase", "loadWaveform", "sendToExternalStream", "receiveFromExternalStream", "globalVariableAssignment", "arbitrary", "arbitraryContext"]
        PLAY_FIELD_NUMBER: _ClassVar[int]
        MEASURE_FIELD_NUMBER: _ClassVar[int]
        WAIT_FIELD_NUMBER: _ClassVar[int]
        SYNC_FIELD_NUMBER: _ClassVar[int]
        IF_FIELD_NUMBER: _ClassVar[int]
        ASSIGN_FIELD_NUMBER: _ClassVar[int]
        FOR_FIELD_NUMBER: _ClassVar[int]
        RUS_FIELD_NUMBER: _ClassVar[int]
        ALIGN_FIELD_NUMBER: _ClassVar[int]
        UPDATEFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        ZROTATION_FIELD_NUMBER: _ClassVar[int]
        PAUSE_FIELD_NUMBER: _ClassVar[int]
        SAVE_FIELD_NUMBER: _ClassVar[int]
        FOREACH_FIELD_NUMBER: _ClassVar[int]
        WAITFORTRIGGER_FIELD_NUMBER: _ClassVar[int]
        QRUN_FIELD_NUMBER: _ClassVar[int]
        UPDATECORRECTION_FIELD_NUMBER: _ClassVar[int]
        RESETPHASE_FIELD_NUMBER: _ClassVar[int]
        RAMPTOZERO_FIELD_NUMBER: _ClassVar[int]
        RESETFRAME_FIELD_NUMBER: _ClassVar[int]
        SETDCOFFSET_FIELD_NUMBER: _ClassVar[int]
        ADVANCEINPUTSTREAM_FIELD_NUMBER: _ClassVar[int]
        STRICTTIMING_FIELD_NUMBER: _ClassVar[int]
        FASTFRAMEROTATION_FIELD_NUMBER: _ClassVar[int]
        UPDATEOSCILLATORFREQUENCY_FIELD_NUMBER: _ClassVar[int]
        RESETGLOBALPHASE_FIELD_NUMBER: _ClassVar[int]
        LOADWAVEFORM_FIELD_NUMBER: _ClassVar[int]
        SENDTOEXTERNALSTREAM_FIELD_NUMBER: _ClassVar[int]
        RECEIVEFROMEXTERNALSTREAM_FIELD_NUMBER: _ClassVar[int]
        GLOBALVARIABLEASSIGNMENT_FIELD_NUMBER: _ClassVar[int]
        ARBITRARY_FIELD_NUMBER: _ClassVar[int]
        ARBITRARYCONTEXT_FIELD_NUMBER: _ClassVar[int]
        play: QuaProgram.PlayStatement
        measure: QuaProgram.MeasureStatement
        wait: QuaProgram.WaitStatement
        sync: QuaProgram.SyncStatement
        assign: QuaProgram.AssignmentStatement
        rus: QuaProgram.RusStatement
        align: QuaProgram.AlignStatement
        updateFrequency: QuaProgram.UpdateFrequencyStatement
        zRotation: QuaProgram.ZRotationStatement
        pause: QuaProgram.PauseStatement
        save: QuaProgram.SaveStatement
        forEach: QuaProgram.ForEachStatement
        waitForTrigger: QuaProgram.WaitForTriggerStatement
        qrun: QuaProgram.QRunStatement
        updateCorrection: QuaProgram.UpdateCorrectionStatement
        resetPhase: QuaProgram.ResetPhaseStatement
        rampToZero: QuaProgram.RampToZeroStatement
        resetFrame: QuaProgram.ResetFrameStatement
        setDcOffset: QuaProgram.SetDcOffsetStatement
        advanceInputStream: QuaProgram.AdvanceInputStreamStatement
        strictTiming: QuaProgram.StrictTimingStatement
        fastFrameRotation: QuaProgram.FastFrameRotationStatement
        updateOscillatorFrequency: QuaProgram.UpdateOscillatorFrequencyStatement
        resetGlobalPhase: QuaProgram.ResetGlobalPhaseStatement
        loadWaveform: QuaProgram.LoadWaveformStatement
        sendToExternalStream: QuaProgram.SendToExternalStreamStatement
        receiveFromExternalStream: QuaProgram.ReceiveFromExternalStreamStatement
        globalVariableAssignment: QuaProgram.GlobalVariableAssignmentStatement
        arbitrary: QuaProgram.ArbitraryStatement
        arbitraryContext: QuaProgram.ArbitraryContextStatement
        def __init__(self, play: _Optional[_Union[QuaProgram.PlayStatement, _Mapping]] = ..., measure: _Optional[_Union[QuaProgram.MeasureStatement, _Mapping]] = ..., wait: _Optional[_Union[QuaProgram.WaitStatement, _Mapping]] = ..., sync: _Optional[_Union[QuaProgram.SyncStatement, _Mapping]] = ..., assign: _Optional[_Union[QuaProgram.AssignmentStatement, _Mapping]] = ..., rus: _Optional[_Union[QuaProgram.RusStatement, _Mapping]] = ..., align: _Optional[_Union[QuaProgram.AlignStatement, _Mapping]] = ..., updateFrequency: _Optional[_Union[QuaProgram.UpdateFrequencyStatement, _Mapping]] = ..., zRotation: _Optional[_Union[QuaProgram.ZRotationStatement, _Mapping]] = ..., pause: _Optional[_Union[QuaProgram.PauseStatement, _Mapping]] = ..., save: _Optional[_Union[QuaProgram.SaveStatement, _Mapping]] = ..., forEach: _Optional[_Union[QuaProgram.ForEachStatement, _Mapping]] = ..., waitForTrigger: _Optional[_Union[QuaProgram.WaitForTriggerStatement, _Mapping]] = ..., qrun: _Optional[_Union[QuaProgram.QRunStatement, _Mapping]] = ..., updateCorrection: _Optional[_Union[QuaProgram.UpdateCorrectionStatement, _Mapping]] = ..., resetPhase: _Optional[_Union[QuaProgram.ResetPhaseStatement, _Mapping]] = ..., rampToZero: _Optional[_Union[QuaProgram.RampToZeroStatement, _Mapping]] = ..., resetFrame: _Optional[_Union[QuaProgram.ResetFrameStatement, _Mapping]] = ..., setDcOffset: _Optional[_Union[QuaProgram.SetDcOffsetStatement, _Mapping]] = ..., advanceInputStream: _Optional[_Union[QuaProgram.AdvanceInputStreamStatement, _Mapping]] = ..., strictTiming: _Optional[_Union[QuaProgram.StrictTimingStatement, _Mapping]] = ..., fastFrameRotation: _Optional[_Union[QuaProgram.FastFrameRotationStatement, _Mapping]] = ..., updateOscillatorFrequency: _Optional[_Union[QuaProgram.UpdateOscillatorFrequencyStatement, _Mapping]] = ..., resetGlobalPhase: _Optional[_Union[QuaProgram.ResetGlobalPhaseStatement, _Mapping]] = ..., loadWaveform: _Optional[_Union[QuaProgram.LoadWaveformStatement, _Mapping]] = ..., sendToExternalStream: _Optional[_Union[QuaProgram.SendToExternalStreamStatement, _Mapping]] = ..., receiveFromExternalStream: _Optional[_Union[QuaProgram.ReceiveFromExternalStreamStatement, _Mapping]] = ..., globalVariableAssignment: _Optional[_Union[QuaProgram.GlobalVariableAssignmentStatement, _Mapping]] = ..., arbitrary: _Optional[_Union[QuaProgram.ArbitraryStatement, _Mapping]] = ..., arbitraryContext: _Optional[_Union[QuaProgram.ArbitraryContextStatement, _Mapping]] = ..., **kwargs) -> None: ...
    class AmpMultiplier(_message.Message):
        __slots__ = ["loc", "v0", "v1", "v2", "v3"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        V0_FIELD_NUMBER: _ClassVar[int]
        V1_FIELD_NUMBER: _ClassVar[int]
        V2_FIELD_NUMBER: _ClassVar[int]
        V3_FIELD_NUMBER: _ClassVar[int]
        loc: str
        v0: QuaProgram.AnyScalarExpression
        v1: QuaProgram.AnyScalarExpression
        v2: QuaProgram.AnyScalarExpression
        v3: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., v0: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., v1: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., v2: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., v3: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class RampToZeroStatement(_message.Message):
        __slots__ = ["loc", "qe", "duration"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        duration: _wrappers_pb2.UInt32Value
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., duration: _Optional[_Union[_wrappers_pb2.UInt32Value, _Mapping]] = ...) -> None: ...
    class RampPulse(_message.Message):
        __slots__ = ["loc", "value"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        value: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., value: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class Chirp(_message.Message):
        __slots__ = ["loc", "scalarRate", "arrayRate", "units", "times", "continueChirp"]
        class Units(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            HzPerNanoSec: _ClassVar[QuaProgram.Chirp.Units]
            mHzPerNanoSec: _ClassVar[QuaProgram.Chirp.Units]
            uHzPerNanoSec: _ClassVar[QuaProgram.Chirp.Units]
            nHzPerNanoSec: _ClassVar[QuaProgram.Chirp.Units]
            pHzPerNanoSec: _ClassVar[QuaProgram.Chirp.Units]
        HzPerNanoSec: QuaProgram.Chirp.Units
        mHzPerNanoSec: QuaProgram.Chirp.Units
        uHzPerNanoSec: QuaProgram.Chirp.Units
        nHzPerNanoSec: QuaProgram.Chirp.Units
        pHzPerNanoSec: QuaProgram.Chirp.Units
        LOC_FIELD_NUMBER: _ClassVar[int]
        SCALARRATE_FIELD_NUMBER: _ClassVar[int]
        ARRAYRATE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        TIMES_FIELD_NUMBER: _ClassVar[int]
        CONTINUECHIRP_FIELD_NUMBER: _ClassVar[int]
        loc: str
        scalarRate: QuaProgram.AnyScalarExpression
        arrayRate: QuaProgram.ArrayVarRefExpression
        units: QuaProgram.Chirp.Units
        times: _containers.RepeatedScalarFieldContainer[int]
        continueChirp: bool
        def __init__(self, loc: _Optional[str] = ..., scalarRate: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., arrayRate: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., units: _Optional[_Union[QuaProgram.Chirp.Units, str]] = ..., times: _Optional[_Iterable[int]] = ..., continueChirp: bool = ...) -> None: ...
    class PlayStatement(_message.Message):
        __slots__ = ["loc", "qe", "pulse", "namedPulse", "rampPulse", "amp", "duration", "condition", "port_condition", "targetInput", "chirp", "truncate", "timestampLabel"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        PULSE_FIELD_NUMBER: _ClassVar[int]
        NAMEDPULSE_FIELD_NUMBER: _ClassVar[int]
        RAMPPULSE_FIELD_NUMBER: _ClassVar[int]
        AMP_FIELD_NUMBER: _ClassVar[int]
        DURATION_FIELD_NUMBER: _ClassVar[int]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        PORT_CONDITION_FIELD_NUMBER: _ClassVar[int]
        TARGETINPUT_FIELD_NUMBER: _ClassVar[int]
        CHIRP_FIELD_NUMBER: _ClassVar[int]
        TRUNCATE_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMPLABEL_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        pulse: QuaProgram.PulseReference
        namedPulse: QuaProgram.PulseReference
        rampPulse: QuaProgram.RampPulse
        amp: QuaProgram.AmpMultiplier
        duration: QuaProgram.AnyScalarExpression
        condition: QuaProgram.AnyScalarExpression
        port_condition: QuaProgram.AnyScalarExpression
        targetInput: str
        chirp: QuaProgram.Chirp
        truncate: QuaProgram.AnyScalarExpression
        timestampLabel: str
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., pulse: _Optional[_Union[QuaProgram.PulseReference, _Mapping]] = ..., namedPulse: _Optional[_Union[QuaProgram.PulseReference, _Mapping]] = ..., rampPulse: _Optional[_Union[QuaProgram.RampPulse, _Mapping]] = ..., amp: _Optional[_Union[QuaProgram.AmpMultiplier, _Mapping]] = ..., duration: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., condition: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., port_condition: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., targetInput: _Optional[str] = ..., chirp: _Optional[_Union[QuaProgram.Chirp, _Mapping]] = ..., truncate: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., timestampLabel: _Optional[str] = ...) -> None: ...
    class UpdateFrequencyStatement(_message.Message):
        __slots__ = ["loc", "qe", "value", "units", "keepPhase"]
        class Units(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            Hz: _ClassVar[QuaProgram.UpdateFrequencyStatement.Units]
            mHz: _ClassVar[QuaProgram.UpdateFrequencyStatement.Units]
            uHz: _ClassVar[QuaProgram.UpdateFrequencyStatement.Units]
            nHz: _ClassVar[QuaProgram.UpdateFrequencyStatement.Units]
            pHz: _ClassVar[QuaProgram.UpdateFrequencyStatement.Units]
        Hz: QuaProgram.UpdateFrequencyStatement.Units
        mHz: QuaProgram.UpdateFrequencyStatement.Units
        uHz: QuaProgram.UpdateFrequencyStatement.Units
        nHz: QuaProgram.UpdateFrequencyStatement.Units
        pHz: QuaProgram.UpdateFrequencyStatement.Units
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        KEEPPHASE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        value: QuaProgram.AnyScalarExpression
        units: QuaProgram.UpdateFrequencyStatement.Units
        keepPhase: bool
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., value: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., units: _Optional[_Union[QuaProgram.UpdateFrequencyStatement.Units, str]] = ..., keepPhase: bool = ...) -> None: ...
    class UpdateOscillatorFrequencyStatement(_message.Message):
        __slots__ = ["loc", "qe", "value", "units", "keepPhase", "updateComponent"]
        class Units(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            GHz: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.Units]
            MHz: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.Units]
            KHz: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.Units]
            Hz: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.Units]
        GHz: QuaProgram.UpdateOscillatorFrequencyStatement.Units
        MHz: QuaProgram.UpdateOscillatorFrequencyStatement.Units
        KHz: QuaProgram.UpdateOscillatorFrequencyStatement.Units
        Hz: QuaProgram.UpdateOscillatorFrequencyStatement.Units
        class UpdateComponentSelection(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            both: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection]
            upconverter: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection]
            downconverter: _ClassVar[QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection]
        both: QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection
        upconverter: QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection
        downconverter: QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        UNITS_FIELD_NUMBER: _ClassVar[int]
        KEEPPHASE_FIELD_NUMBER: _ClassVar[int]
        UPDATECOMPONENT_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        value: QuaProgram.AnyScalarExpression
        units: QuaProgram.UpdateOscillatorFrequencyStatement.Units
        keepPhase: bool
        updateComponent: QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., value: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., units: _Optional[_Union[QuaProgram.UpdateOscillatorFrequencyStatement.Units, str]] = ..., keepPhase: bool = ..., updateComponent: _Optional[_Union[QuaProgram.UpdateOscillatorFrequencyStatement.UpdateComponentSelection, str]] = ...) -> None: ...
    class SetDcOffsetStatement(_message.Message):
        __slots__ = ["loc", "qe", "qeInputReference", "offset"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        QEINPUTREFERENCE_FIELD_NUMBER: _ClassVar[int]
        OFFSET_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        qeInputReference: str
        offset: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., qeInputReference: _Optional[str] = ..., offset: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class ZRotationStatement(_message.Message):
        __slots__ = ["loc", "qe", "value"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        value: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., value: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class ResetFrameStatement(_message.Message):
        __slots__ = ["loc", "qe"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ...) -> None: ...
    class FastFrameRotationStatement(_message.Message):
        __slots__ = ["loc", "qe", "cosine", "sine"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        COSINE_FIELD_NUMBER: _ClassVar[int]
        SINE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        cosine: QuaProgram.AnyScalarExpression
        sine: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., cosine: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., sine: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class AlignStatement(_message.Message):
        __slots__ = ["loc", "qe"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: _containers.RepeatedCompositeFieldContainer[QuaProgram.QuantumElementReference]
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Iterable[_Union[QuaProgram.QuantumElementReference, _Mapping]]] = ...) -> None: ...
    class MeasureProcess(_message.Message):
        __slots__ = ["analog", "digital"]
        ANALOG_FIELD_NUMBER: _ClassVar[int]
        DIGITAL_FIELD_NUMBER: _ClassVar[int]
        analog: QuaProgram.AnalogMeasureProcess
        digital: QuaProgram.DigitalMeasureProcess
        def __init__(self, analog: _Optional[_Union[QuaProgram.AnalogMeasureProcess, _Mapping]] = ..., digital: _Optional[_Union[QuaProgram.DigitalMeasureProcess, _Mapping]] = ...) -> None: ...
    class AnalogMeasureProcess(_message.Message):
        __slots__ = ["loc", "bareIntegration", "demodIntegration", "rawTimeTagging", "dualBareIntegration", "dualDemodIntegration", "highResTimeTagging"]
        class BareIntegration(_message.Message):
            __slots__ = ["integration", "target", "elementOutput"]
            INTEGRATION_FIELD_NUMBER: _ClassVar[int]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT_FIELD_NUMBER: _ClassVar[int]
            integration: QuaProgram.IntegrationWeightReference
            target: QuaProgram.AnalogProcessTarget
            elementOutput: str
            def __init__(self, integration: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., target: _Optional[_Union[QuaProgram.AnalogProcessTarget, _Mapping]] = ..., elementOutput: _Optional[str] = ...) -> None: ...
        class DualBareIntegration(_message.Message):
            __slots__ = ["integration1", "integration2", "target", "elementOutput1", "elementOutput2"]
            INTEGRATION1_FIELD_NUMBER: _ClassVar[int]
            INTEGRATION2_FIELD_NUMBER: _ClassVar[int]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT1_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT2_FIELD_NUMBER: _ClassVar[int]
            integration1: QuaProgram.IntegrationWeightReference
            integration2: QuaProgram.IntegrationWeightReference
            target: QuaProgram.AnalogProcessTarget
            elementOutput1: str
            elementOutput2: str
            def __init__(self, integration1: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., integration2: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., target: _Optional[_Union[QuaProgram.AnalogProcessTarget, _Mapping]] = ..., elementOutput1: _Optional[str] = ..., elementOutput2: _Optional[str] = ...) -> None: ...
        class DemodIntegration(_message.Message):
            __slots__ = ["integration", "target", "elementOutput"]
            INTEGRATION_FIELD_NUMBER: _ClassVar[int]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT_FIELD_NUMBER: _ClassVar[int]
            integration: QuaProgram.IntegrationWeightReference
            target: QuaProgram.AnalogProcessTarget
            elementOutput: str
            def __init__(self, integration: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., target: _Optional[_Union[QuaProgram.AnalogProcessTarget, _Mapping]] = ..., elementOutput: _Optional[str] = ...) -> None: ...
        class DualDemodIntegration(_message.Message):
            __slots__ = ["integration1", "integration2", "target", "elementOutput1", "elementOutput2"]
            INTEGRATION1_FIELD_NUMBER: _ClassVar[int]
            INTEGRATION2_FIELD_NUMBER: _ClassVar[int]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT1_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT2_FIELD_NUMBER: _ClassVar[int]
            integration1: QuaProgram.IntegrationWeightReference
            integration2: QuaProgram.IntegrationWeightReference
            target: QuaProgram.AnalogProcessTarget
            elementOutput1: str
            elementOutput2: str
            def __init__(self, integration1: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., integration2: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., target: _Optional[_Union[QuaProgram.AnalogProcessTarget, _Mapping]] = ..., elementOutput1: _Optional[str] = ..., elementOutput2: _Optional[str] = ...) -> None: ...
        class RawTimeTagging(_message.Message):
            __slots__ = ["target", "targetLen", "maxTime", "elementOutput"]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            TARGETLEN_FIELD_NUMBER: _ClassVar[int]
            MAXTIME_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT_FIELD_NUMBER: _ClassVar[int]
            target: QuaProgram.ArrayVarRefExpression
            targetLen: QuaProgram.VarRefExpression
            maxTime: int
            elementOutput: str
            def __init__(self, target: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., targetLen: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., maxTime: _Optional[int] = ..., elementOutput: _Optional[str] = ...) -> None: ...
        class HighResTimeTagging(_message.Message):
            __slots__ = ["target", "targetLen", "maxTime", "elementOutput"]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            TARGETLEN_FIELD_NUMBER: _ClassVar[int]
            MAXTIME_FIELD_NUMBER: _ClassVar[int]
            ELEMENTOUTPUT_FIELD_NUMBER: _ClassVar[int]
            target: QuaProgram.ArrayVarRefExpression
            targetLen: QuaProgram.VarRefExpression
            maxTime: int
            elementOutput: str
            def __init__(self, target: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., targetLen: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., maxTime: _Optional[int] = ..., elementOutput: _Optional[str] = ...) -> None: ...
        LOC_FIELD_NUMBER: _ClassVar[int]
        BAREINTEGRATION_FIELD_NUMBER: _ClassVar[int]
        DEMODINTEGRATION_FIELD_NUMBER: _ClassVar[int]
        RAWTIMETAGGING_FIELD_NUMBER: _ClassVar[int]
        DUALBAREINTEGRATION_FIELD_NUMBER: _ClassVar[int]
        DUALDEMODINTEGRATION_FIELD_NUMBER: _ClassVar[int]
        HIGHRESTIMETAGGING_FIELD_NUMBER: _ClassVar[int]
        loc: str
        bareIntegration: QuaProgram.AnalogMeasureProcess.BareIntegration
        demodIntegration: QuaProgram.AnalogMeasureProcess.DemodIntegration
        rawTimeTagging: QuaProgram.AnalogMeasureProcess.RawTimeTagging
        dualBareIntegration: QuaProgram.AnalogMeasureProcess.DualBareIntegration
        dualDemodIntegration: QuaProgram.AnalogMeasureProcess.DualDemodIntegration
        highResTimeTagging: QuaProgram.AnalogMeasureProcess.HighResTimeTagging
        def __init__(self, loc: _Optional[str] = ..., bareIntegration: _Optional[_Union[QuaProgram.AnalogMeasureProcess.BareIntegration, _Mapping]] = ..., demodIntegration: _Optional[_Union[QuaProgram.AnalogMeasureProcess.DemodIntegration, _Mapping]] = ..., rawTimeTagging: _Optional[_Union[QuaProgram.AnalogMeasureProcess.RawTimeTagging, _Mapping]] = ..., dualBareIntegration: _Optional[_Union[QuaProgram.AnalogMeasureProcess.DualBareIntegration, _Mapping]] = ..., dualDemodIntegration: _Optional[_Union[QuaProgram.AnalogMeasureProcess.DualDemodIntegration, _Mapping]] = ..., highResTimeTagging: _Optional[_Union[QuaProgram.AnalogMeasureProcess.HighResTimeTagging, _Mapping]] = ...) -> None: ...
    class DigitalMeasureProcess(_message.Message):
        __slots__ = ["loc", "rawTimeTagging", "counting"]
        class RawTimeTagging(_message.Message):
            __slots__ = ["elementOutput", "target", "targetLen", "maxTime"]
            ELEMENTOUTPUT_FIELD_NUMBER: _ClassVar[int]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            TARGETLEN_FIELD_NUMBER: _ClassVar[int]
            MAXTIME_FIELD_NUMBER: _ClassVar[int]
            elementOutput: str
            target: QuaProgram.ArrayVarRefExpression
            targetLen: QuaProgram.VarRefExpression
            maxTime: int
            def __init__(self, elementOutput: _Optional[str] = ..., target: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., targetLen: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., maxTime: _Optional[int] = ...) -> None: ...
        class Counting(_message.Message):
            __slots__ = ["elementOutputs", "target", "maxTime"]
            ELEMENTOUTPUTS_FIELD_NUMBER: _ClassVar[int]
            TARGET_FIELD_NUMBER: _ClassVar[int]
            MAXTIME_FIELD_NUMBER: _ClassVar[int]
            elementOutputs: _containers.RepeatedScalarFieldContainer[str]
            target: QuaProgram.VarRefExpression
            maxTime: int
            def __init__(self, elementOutputs: _Optional[_Iterable[str]] = ..., target: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., maxTime: _Optional[int] = ...) -> None: ...
        LOC_FIELD_NUMBER: _ClassVar[int]
        RAWTIMETAGGING_FIELD_NUMBER: _ClassVar[int]
        COUNTING_FIELD_NUMBER: _ClassVar[int]
        loc: str
        rawTimeTagging: QuaProgram.DigitalMeasureProcess.RawTimeTagging
        counting: QuaProgram.DigitalMeasureProcess.Counting
        def __init__(self, loc: _Optional[str] = ..., rawTimeTagging: _Optional[_Union[QuaProgram.DigitalMeasureProcess.RawTimeTagging, _Mapping]] = ..., counting: _Optional[_Union[QuaProgram.DigitalMeasureProcess.Counting, _Mapping]] = ...) -> None: ...
    class AnalogProcessTarget(_message.Message):
        __slots__ = ["loc", "scalarProcess", "vectorProcess"]
        class ScalarProcessTarget(_message.Message):
            __slots__ = ["variable", "arrayCell"]
            VARIABLE_FIELD_NUMBER: _ClassVar[int]
            ARRAYCELL_FIELD_NUMBER: _ClassVar[int]
            variable: QuaProgram.VarRefExpression
            arrayCell: QuaProgram.ArrayCellRefExpression
            def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., arrayCell: _Optional[_Union[QuaProgram.ArrayCellRefExpression, _Mapping]] = ...) -> None: ...
        class VectorProcessTarget(_message.Message):
            __slots__ = ["array", "timeDivision"]
            ARRAY_FIELD_NUMBER: _ClassVar[int]
            TIMEDIVISION_FIELD_NUMBER: _ClassVar[int]
            array: QuaProgram.ArrayVarRefExpression
            timeDivision: QuaProgram.AnalogProcessTarget.TimeDivision
            def __init__(self, array: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., timeDivision: _Optional[_Union[QuaProgram.AnalogProcessTarget.TimeDivision, _Mapping]] = ...) -> None: ...
        class TimeDivision(_message.Message):
            __slots__ = ["sliced", "accumulated", "movingWindow"]
            SLICED_FIELD_NUMBER: _ClassVar[int]
            ACCUMULATED_FIELD_NUMBER: _ClassVar[int]
            MOVINGWINDOW_FIELD_NUMBER: _ClassVar[int]
            sliced: QuaProgram.AnalogTimeDivision.Sliced
            accumulated: QuaProgram.AnalogTimeDivision.Accumulated
            movingWindow: QuaProgram.AnalogTimeDivision.MovingWindow
            def __init__(self, sliced: _Optional[_Union[QuaProgram.AnalogTimeDivision.Sliced, _Mapping]] = ..., accumulated: _Optional[_Union[QuaProgram.AnalogTimeDivision.Accumulated, _Mapping]] = ..., movingWindow: _Optional[_Union[QuaProgram.AnalogTimeDivision.MovingWindow, _Mapping]] = ...) -> None: ...
        LOC_FIELD_NUMBER: _ClassVar[int]
        SCALARPROCESS_FIELD_NUMBER: _ClassVar[int]
        VECTORPROCESS_FIELD_NUMBER: _ClassVar[int]
        loc: str
        scalarProcess: QuaProgram.AnalogProcessTarget.ScalarProcessTarget
        vectorProcess: QuaProgram.AnalogProcessTarget.VectorProcessTarget
        def __init__(self, loc: _Optional[str] = ..., scalarProcess: _Optional[_Union[QuaProgram.AnalogProcessTarget.ScalarProcessTarget, _Mapping]] = ..., vectorProcess: _Optional[_Union[QuaProgram.AnalogProcessTarget.VectorProcessTarget, _Mapping]] = ...) -> None: ...
    class AnalogTimeDivision(_message.Message):
        __slots__ = []
        class Sliced(_message.Message):
            __slots__ = ["loc", "samplesPerChunk"]
            LOC_FIELD_NUMBER: _ClassVar[int]
            SAMPLESPERCHUNK_FIELD_NUMBER: _ClassVar[int]
            loc: str
            samplesPerChunk: int
            def __init__(self, loc: _Optional[str] = ..., samplesPerChunk: _Optional[int] = ...) -> None: ...
        class Accumulated(_message.Message):
            __slots__ = ["loc", "samplesPerChunk"]
            LOC_FIELD_NUMBER: _ClassVar[int]
            SAMPLESPERCHUNK_FIELD_NUMBER: _ClassVar[int]
            loc: str
            samplesPerChunk: int
            def __init__(self, loc: _Optional[str] = ..., samplesPerChunk: _Optional[int] = ...) -> None: ...
        class MovingWindow(_message.Message):
            __slots__ = ["loc", "samplesPerChunk", "chunksPerWindow"]
            LOC_FIELD_NUMBER: _ClassVar[int]
            SAMPLESPERCHUNK_FIELD_NUMBER: _ClassVar[int]
            CHUNKSPERWINDOW_FIELD_NUMBER: _ClassVar[int]
            loc: str
            samplesPerChunk: int
            chunksPerWindow: int
            def __init__(self, loc: _Optional[str] = ..., samplesPerChunk: _Optional[int] = ..., chunksPerWindow: _Optional[int] = ...) -> None: ...
        def __init__(self) -> None: ...
    class MeasureOutput(_message.Message):
        __slots__ = ["loc", "integration", "variable", "output", "target"]
        class Target(_message.Message):
            __slots__ = ["variable", "arrayCell"]
            VARIABLE_FIELD_NUMBER: _ClassVar[int]
            ARRAYCELL_FIELD_NUMBER: _ClassVar[int]
            variable: QuaProgram.VarRefExpression
            arrayCell: QuaProgram.ArrayCellRefExpression
            def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., arrayCell: _Optional[_Union[QuaProgram.ArrayCellRefExpression, _Mapping]] = ...) -> None: ...
        LOC_FIELD_NUMBER: _ClassVar[int]
        INTEGRATION_FIELD_NUMBER: _ClassVar[int]
        VARIABLE_FIELD_NUMBER: _ClassVar[int]
        OUTPUT_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        loc: str
        integration: QuaProgram.IntegrationWeightReference
        variable: QuaProgram.VarRefExpression
        output: str
        target: QuaProgram.MeasureOutput.Target
        def __init__(self, loc: _Optional[str] = ..., integration: _Optional[_Union[QuaProgram.IntegrationWeightReference, _Mapping]] = ..., variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., output: _Optional[str] = ..., target: _Optional[_Union[QuaProgram.MeasureOutput.Target, _Mapping]] = ...) -> None: ...
    class MeasureStatement(_message.Message):
        __slots__ = ["loc", "qe", "pulse", "amp", "outputs", "streamAs", "measureProcesses", "timestampLabel"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        PULSE_FIELD_NUMBER: _ClassVar[int]
        AMP_FIELD_NUMBER: _ClassVar[int]
        OUTPUTS_FIELD_NUMBER: _ClassVar[int]
        STREAMAS_FIELD_NUMBER: _ClassVar[int]
        MEASUREPROCESSES_FIELD_NUMBER: _ClassVar[int]
        TIMESTAMPLABEL_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        pulse: QuaProgram.PulseReference
        amp: QuaProgram.AmpMultiplier
        outputs: _containers.RepeatedCompositeFieldContainer[QuaProgram.MeasureOutput]
        streamAs: str
        measureProcesses: _containers.RepeatedCompositeFieldContainer[QuaProgram.MeasureProcess]
        timestampLabel: str
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., pulse: _Optional[_Union[QuaProgram.PulseReference, _Mapping]] = ..., amp: _Optional[_Union[QuaProgram.AmpMultiplier, _Mapping]] = ..., outputs: _Optional[_Iterable[_Union[QuaProgram.MeasureOutput, _Mapping]]] = ..., streamAs: _Optional[str] = ..., measureProcesses: _Optional[_Iterable[_Union[QuaProgram.MeasureProcess, _Mapping]]] = ..., timestampLabel: _Optional[str] = ...) -> None: ...
    class WaitStatement(_message.Message):
        __slots__ = ["loc", "qe", "time"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        TIME_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: _containers.RepeatedCompositeFieldContainer[QuaProgram.QuantumElementReference]
        time: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Iterable[_Union[QuaProgram.QuantumElementReference, _Mapping]]] = ..., time: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class ArbitraryStatement(_message.Message):
        __slots__ = ["loc", "name", "data"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        loc: str
        name: str
        data: _any_pb2.Any
        def __init__(self, loc: _Optional[str] = ..., name: _Optional[str] = ..., data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ...) -> None: ...
    class ArbitraryContextStatement(_message.Message):
        __slots__ = ["loc", "name", "data", "body"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        NAME_FIELD_NUMBER: _ClassVar[int]
        DATA_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        loc: str
        name: str
        data: _any_pb2.Any
        body: QuaProgram.StatementsCollection
        def __init__(self, loc: _Optional[str] = ..., name: _Optional[str] = ..., data: _Optional[_Union[_any_pb2.Any, _Mapping]] = ..., body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ...) -> None: ...
    class WaitForTriggerStatement(_message.Message):
        __slots__ = ["loc", "qe", "pulseToPlay", "globalTrigger", "elementOutput", "timeTagTarget"]
        class ElementOutput(_message.Message):
            __slots__ = ["element", "output"]
            ELEMENT_FIELD_NUMBER: _ClassVar[int]
            OUTPUT_FIELD_NUMBER: _ClassVar[int]
            element: str
            output: str
            def __init__(self, element: _Optional[str] = ..., output: _Optional[str] = ...) -> None: ...
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        PULSETOPLAY_FIELD_NUMBER: _ClassVar[int]
        GLOBALTRIGGER_FIELD_NUMBER: _ClassVar[int]
        ELEMENTOUTPUT_FIELD_NUMBER: _ClassVar[int]
        TIMETAGTARGET_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: _containers.RepeatedCompositeFieldContainer[QuaProgram.QuantumElementReference]
        pulseToPlay: QuaProgram.PulseReference
        globalTrigger: _empty_pb2.Empty
        elementOutput: QuaProgram.WaitForTriggerStatement.ElementOutput
        timeTagTarget: QuaProgram.VarRefExpression
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Iterable[_Union[QuaProgram.QuantumElementReference, _Mapping]]] = ..., pulseToPlay: _Optional[_Union[QuaProgram.PulseReference, _Mapping]] = ..., globalTrigger: _Optional[_Union[_empty_pb2.Empty, _Mapping]] = ..., elementOutput: _Optional[_Union[QuaProgram.WaitForTriggerStatement.ElementOutput, _Mapping]] = ..., timeTagTarget: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ...) -> None: ...
    class UpdateCorrectionStatement(_message.Message):
        __slots__ = ["loc", "qe", "correction"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        CORRECTION_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        correction: QuaProgram.Correction
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., correction: _Optional[_Union[QuaProgram.Correction, _Mapping]] = ...) -> None: ...
    class ResetPhaseStatement(_message.Message):
        __slots__ = ["loc", "qe"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ...) -> None: ...
    class ResetGlobalPhaseStatement(_message.Message):
        __slots__ = ["loc"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        loc: str
        def __init__(self, loc: _Optional[str] = ...) -> None: ...
    class SendToExternalStreamStatement(_message.Message):
        __slots__ = ["loc", "stream", "struct"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        STREAM_FIELD_NUMBER: _ClassVar[int]
        STRUCT_FIELD_NUMBER: _ClassVar[int]
        loc: str
        stream: QuaProgram.ExternalStreamRefExpression
        struct: QuaProgram.StructVarRefExpression
        def __init__(self, loc: _Optional[str] = ..., stream: _Optional[_Union[QuaProgram.ExternalStreamRefExpression, _Mapping]] = ..., struct: _Optional[_Union[QuaProgram.StructVarRefExpression, _Mapping]] = ...) -> None: ...
    class ReceiveFromExternalStreamStatement(_message.Message):
        __slots__ = ["loc", "stream", "struct"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        STREAM_FIELD_NUMBER: _ClassVar[int]
        STRUCT_FIELD_NUMBER: _ClassVar[int]
        loc: str
        stream: QuaProgram.ExternalStreamRefExpression
        struct: QuaProgram.StructVarRefExpression
        def __init__(self, loc: _Optional[str] = ..., stream: _Optional[_Union[QuaProgram.ExternalStreamRefExpression, _Mapping]] = ..., struct: _Optional[_Union[QuaProgram.StructVarRefExpression, _Mapping]] = ...) -> None: ...
    class GlobalVariableAssignmentStatement(_message.Message):
        __slots__ = ["loc", "variables"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        VARIABLES_FIELD_NUMBER: _ClassVar[int]
        loc: str
        variables: _containers.RepeatedCompositeFieldContainer[QuaProgram.VarRefExpression]
        def __init__(self, loc: _Optional[str] = ..., variables: _Optional[_Iterable[_Union[QuaProgram.VarRefExpression, _Mapping]]] = ...) -> None: ...
    class Correction(_message.Message):
        __slots__ = ["loc", "c0", "c1", "c2", "c3"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        C0_FIELD_NUMBER: _ClassVar[int]
        C1_FIELD_NUMBER: _ClassVar[int]
        C2_FIELD_NUMBER: _ClassVar[int]
        C3_FIELD_NUMBER: _ClassVar[int]
        loc: str
        c0: QuaProgram.AnyScalarExpression
        c1: QuaProgram.AnyScalarExpression
        c2: QuaProgram.AnyScalarExpression
        c3: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., c0: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., c1: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., c2: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., c3: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class SyncStatement(_message.Message):
        __slots__ = ["loc"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        loc: str
        def __init__(self, loc: _Optional[str] = ...) -> None: ...
    class ElseIf(_message.Message):
        __slots__ = ["condition", "body", "loc"]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        condition: QuaProgram.AnyScalarExpression
        body: QuaProgram.StatementsCollection
        loc: str
        def __init__(self, condition: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class IfStatement(_message.Message):
        __slots__ = ["condition", "body", "elseifs", "unsafe", "loc"]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        ELSE_FIELD_NUMBER: _ClassVar[int]
        ELSEIFS_FIELD_NUMBER: _ClassVar[int]
        UNSAFE_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        condition: QuaProgram.AnyScalarExpression
        body: QuaProgram.StatementsCollection
        elseifs: _containers.RepeatedCompositeFieldContainer[QuaProgram.ElseIf]
        unsafe: bool
        loc: str
        def __init__(self, condition: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., elseifs: _Optional[_Iterable[_Union[QuaProgram.ElseIf, _Mapping]]] = ..., unsafe: bool = ..., loc: _Optional[str] = ..., **kwargs) -> None: ...
    class ForStatement(_message.Message):
        __slots__ = ["init", "condition", "update", "body", "loc"]
        INIT_FIELD_NUMBER: _ClassVar[int]
        CONDITION_FIELD_NUMBER: _ClassVar[int]
        UPDATE_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        init: QuaProgram.StatementsCollection
        condition: QuaProgram.AnyScalarExpression
        update: QuaProgram.StatementsCollection
        body: QuaProgram.StatementsCollection
        loc: str
        def __init__(self, init: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., condition: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., update: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class QRunStatement(_message.Message):
        __slots__ = ["body", "loc"]
        BODY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        body: QuaProgram.StatementsCollection
        loc: str
        def __init__(self, body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class StrictTimingStatement(_message.Message):
        __slots__ = ["body", "loc"]
        BODY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        body: QuaProgram.StatementsCollection
        loc: str
        def __init__(self, body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class ForEachStatement(_message.Message):
        __slots__ = ["iterator", "body", "loc"]
        class VariableWithValues(_message.Message):
            __slots__ = ["variable", "array"]
            VARIABLE_FIELD_NUMBER: _ClassVar[int]
            ARRAY_FIELD_NUMBER: _ClassVar[int]
            variable: QuaProgram.VarRefExpression
            array: QuaProgram.ArrayVarRefExpression
            def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., array: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ...) -> None: ...
        ITERATOR_FIELD_NUMBER: _ClassVar[int]
        BODY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        iterator: _containers.RepeatedCompositeFieldContainer[QuaProgram.ForEachStatement.VariableWithValues]
        body: QuaProgram.StatementsCollection
        loc: str
        def __init__(self, iterator: _Optional[_Iterable[_Union[QuaProgram.ForEachStatement.VariableWithValues, _Mapping]]] = ..., body: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class RusStatement(_message.Message):
        __slots__ = ["doBlock", "failBlock", "until", "loc"]
        DOBLOCK_FIELD_NUMBER: _ClassVar[int]
        FAILBLOCK_FIELD_NUMBER: _ClassVar[int]
        UNTIL_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        doBlock: QuaProgram.StatementsCollection
        failBlock: QuaProgram.StatementsCollection
        until: QuaProgram.AnyScalarExpression
        loc: str
        def __init__(self, doBlock: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., failBlock: _Optional[_Union[QuaProgram.StatementsCollection, _Mapping]] = ..., until: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class AssignmentStatement(_message.Message):
        __slots__ = ["variable", "expression", "save", "target", "loc"]
        class Target(_message.Message):
            __slots__ = ["variable", "arrayCell"]
            VARIABLE_FIELD_NUMBER: _ClassVar[int]
            ARRAYCELL_FIELD_NUMBER: _ClassVar[int]
            variable: QuaProgram.VarRefExpression
            arrayCell: QuaProgram.ArrayCellRefExpression
            def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., arrayCell: _Optional[_Union[QuaProgram.ArrayCellRefExpression, _Mapping]] = ...) -> None: ...
        VARIABLE_FIELD_NUMBER: _ClassVar[int]
        EXPRESSION_FIELD_NUMBER: _ClassVar[int]
        SAVE_FIELD_NUMBER: _ClassVar[int]
        TARGET_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        variable: QuaProgram.VarRefExpression
        expression: QuaProgram.AnyScalarExpression
        save: bool
        target: QuaProgram.AssignmentStatement.Target
        loc: str
        def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., expression: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., save: bool = ..., target: _Optional[_Union[QuaProgram.AssignmentStatement.Target, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class PauseStatement(_message.Message):
        __slots__ = ["qes", "loc"]
        QES_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        qes: _containers.RepeatedCompositeFieldContainer[QuaProgram.QuantumElementReference]
        loc: str
        def __init__(self, qes: _Optional[_Iterable[_Union[QuaProgram.QuantumElementReference, _Mapping]]] = ..., loc: _Optional[str] = ...) -> None: ...
    class SaveStatement(_message.Message):
        __slots__ = ["variable", "tag", "source", "loc"]
        class Source(_message.Message):
            __slots__ = ["variable", "arrayCell", "literal"]
            VARIABLE_FIELD_NUMBER: _ClassVar[int]
            ARRAYCELL_FIELD_NUMBER: _ClassVar[int]
            LITERAL_FIELD_NUMBER: _ClassVar[int]
            variable: QuaProgram.VarRefExpression
            arrayCell: QuaProgram.ArrayCellRefExpression
            literal: QuaProgram.LiteralExpression
            def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., arrayCell: _Optional[_Union[QuaProgram.ArrayCellRefExpression, _Mapping]] = ..., literal: _Optional[_Union[QuaProgram.LiteralExpression, _Mapping]] = ...) -> None: ...
        VARIABLE_FIELD_NUMBER: _ClassVar[int]
        TAG_FIELD_NUMBER: _ClassVar[int]
        SOURCE_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        variable: QuaProgram.VarRefExpression
        tag: str
        source: QuaProgram.SaveStatement.Source
        loc: str
        def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., tag: _Optional[str] = ..., source: _Optional[_Union[QuaProgram.SaveStatement.Source, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class LoadWaveformStatement(_message.Message):
        __slots__ = ["loc", "qe", "pulse", "waveform_index"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        QE_FIELD_NUMBER: _ClassVar[int]
        PULSE_FIELD_NUMBER: _ClassVar[int]
        WAVEFORM_INDEX_FIELD_NUMBER: _ClassVar[int]
        loc: str
        qe: QuaProgram.QuantumElementReference
        pulse: QuaProgram.PulseReference
        waveform_index: QuaProgram.AnyScalarExpression
        def __init__(self, loc: _Optional[str] = ..., qe: _Optional[_Union[QuaProgram.QuantumElementReference, _Mapping]] = ..., pulse: _Optional[_Union[QuaProgram.PulseReference, _Mapping]] = ..., waveform_index: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ...) -> None: ...
    class StatementsCollection(_message.Message):
        __slots__ = ["statements"]
        STATEMENTS_FIELD_NUMBER: _ClassVar[int]
        statements: _containers.RepeatedCompositeFieldContainer[QuaProgram.AnyStatement]
        def __init__(self, statements: _Optional[_Iterable[_Union[QuaProgram.AnyStatement, _Mapping]]] = ...) -> None: ...
    class AnyScalarExpression(_message.Message):
        __slots__ = ["variable", "literal", "binaryOperation", "arrayCell", "arrayLength", "libFunction", "function", "broadcast", "globalVariable"]
        VARIABLE_FIELD_NUMBER: _ClassVar[int]
        LITERAL_FIELD_NUMBER: _ClassVar[int]
        BINARYOPERATION_FIELD_NUMBER: _ClassVar[int]
        ARRAYCELL_FIELD_NUMBER: _ClassVar[int]
        ARRAYLENGTH_FIELD_NUMBER: _ClassVar[int]
        LIBFUNCTION_FIELD_NUMBER: _ClassVar[int]
        FUNCTION_FIELD_NUMBER: _ClassVar[int]
        BROADCAST_FIELD_NUMBER: _ClassVar[int]
        GLOBALVARIABLE_FIELD_NUMBER: _ClassVar[int]
        variable: QuaProgram.VarRefExpression
        literal: QuaProgram.LiteralExpression
        binaryOperation: QuaProgram.BinaryExpression
        arrayCell: QuaProgram.ArrayCellRefExpression
        arrayLength: QuaProgram.ArrayLengthExpression
        libFunction: QuaProgram.LibFunctionExpression
        function: QuaProgram.FunctionExpression
        broadcast: QuaProgram.BroadcastExpression
        globalVariable: QuaProgram.GlobalVarRefExpression
        def __init__(self, variable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., literal: _Optional[_Union[QuaProgram.LiteralExpression, _Mapping]] = ..., binaryOperation: _Optional[_Union[QuaProgram.BinaryExpression, _Mapping]] = ..., arrayCell: _Optional[_Union[QuaProgram.ArrayCellRefExpression, _Mapping]] = ..., arrayLength: _Optional[_Union[QuaProgram.ArrayLengthExpression, _Mapping]] = ..., libFunction: _Optional[_Union[QuaProgram.LibFunctionExpression, _Mapping]] = ..., function: _Optional[_Union[QuaProgram.FunctionExpression, _Mapping]] = ..., broadcast: _Optional[_Union[QuaProgram.BroadcastExpression, _Mapping]] = ..., globalVariable: _Optional[_Union[QuaProgram.GlobalVarRefExpression, _Mapping]] = ...) -> None: ...
    class AdvanceInputStreamStatement(_message.Message):
        __slots__ = ["streamVariable", "streamArray", "loc"]
        STREAMVARIABLE_FIELD_NUMBER: _ClassVar[int]
        STREAMARRAY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        streamVariable: QuaProgram.VarRefExpression
        streamArray: QuaProgram.ArrayVarRefExpression
        loc: str
        def __init__(self, streamVariable: _Optional[_Union[QuaProgram.VarRefExpression, _Mapping]] = ..., streamArray: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class ArrayLengthExpression(_message.Message):
        __slots__ = ["array", "loc"]
        ARRAY_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        array: QuaProgram.ArrayVarRefExpression
        loc: str
        def __init__(self, array: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class VarRefExpression(_message.Message):
        __slots__ = ["name", "ioNumber", "loc"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        IONUMBER_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        name: str
        ioNumber: int
        loc: str
        def __init__(self, name: _Optional[str] = ..., ioNumber: _Optional[int] = ..., loc: _Optional[str] = ...) -> None: ...
    class StructVarRefExpression(_message.Message):
        __slots__ = ["name", "loc"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        name: str
        loc: str
        def __init__(self, name: _Optional[str] = ..., loc: _Optional[str] = ...) -> None: ...
    class ExternalStreamRefExpression(_message.Message):
        __slots__ = ["stream_id", "loc"]
        STREAM_ID_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        stream_id: int
        loc: str
        def __init__(self, stream_id: _Optional[int] = ..., loc: _Optional[str] = ...) -> None: ...
    class ArrayVarRefExpression(_message.Message):
        __slots__ = ["name", "structVar", "loc"]
        NAME_FIELD_NUMBER: _ClassVar[int]
        STRUCTVAR_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        name: str
        structVar: QuaProgram.StructVarRefExpression
        loc: str
        def __init__(self, name: _Optional[str] = ..., structVar: _Optional[_Union[QuaProgram.StructVarRefExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class ArrayCellRefExpression(_message.Message):
        __slots__ = ["arrayVar", "index", "loc"]
        ARRAYVAR_FIELD_NUMBER: _ClassVar[int]
        INDEX_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        arrayVar: QuaProgram.ArrayVarRefExpression
        index: QuaProgram.AnyScalarExpression
        loc: str
        def __init__(self, arrayVar: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ..., index: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class LiteralExpression(_message.Message):
        __slots__ = ["value", "type", "loc"]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        value: str
        type: QuaProgram.Type
        loc: str
        def __init__(self, value: _Optional[str] = ..., type: _Optional[_Union[QuaProgram.Type, str]] = ..., loc: _Optional[str] = ...) -> None: ...
    class BinaryExpression(_message.Message):
        __slots__ = ["op", "left", "right", "loc"]
        class BinaryOperator(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
            __slots__ = []
            ADD: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            SUB: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            MULT: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            DIV: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            AND: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            OR: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            XOR: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            LT: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            LET: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            GT: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            GET: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            EQ: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            SHL: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
            SHR: _ClassVar[QuaProgram.BinaryExpression.BinaryOperator]
        ADD: QuaProgram.BinaryExpression.BinaryOperator
        SUB: QuaProgram.BinaryExpression.BinaryOperator
        MULT: QuaProgram.BinaryExpression.BinaryOperator
        DIV: QuaProgram.BinaryExpression.BinaryOperator
        AND: QuaProgram.BinaryExpression.BinaryOperator
        OR: QuaProgram.BinaryExpression.BinaryOperator
        XOR: QuaProgram.BinaryExpression.BinaryOperator
        LT: QuaProgram.BinaryExpression.BinaryOperator
        LET: QuaProgram.BinaryExpression.BinaryOperator
        GT: QuaProgram.BinaryExpression.BinaryOperator
        GET: QuaProgram.BinaryExpression.BinaryOperator
        EQ: QuaProgram.BinaryExpression.BinaryOperator
        SHL: QuaProgram.BinaryExpression.BinaryOperator
        SHR: QuaProgram.BinaryExpression.BinaryOperator
        OP_FIELD_NUMBER: _ClassVar[int]
        LEFT_FIELD_NUMBER: _ClassVar[int]
        RIGHT_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        op: QuaProgram.BinaryExpression.BinaryOperator
        left: QuaProgram.AnyScalarExpression
        right: QuaProgram.AnyScalarExpression
        loc: str
        def __init__(self, op: _Optional[_Union[QuaProgram.BinaryExpression.BinaryOperator, str]] = ..., left: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., right: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class LibFunctionExpression(_message.Message):
        __slots__ = ["functionName", "arguments", "libraryName", "loc"]
        class Argument(_message.Message):
            __slots__ = ["scalar", "array"]
            SCALAR_FIELD_NUMBER: _ClassVar[int]
            ARRAY_FIELD_NUMBER: _ClassVar[int]
            scalar: QuaProgram.AnyScalarExpression
            array: QuaProgram.ArrayVarRefExpression
            def __init__(self, scalar: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., array: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ...) -> None: ...
        FUNCTIONNAME_FIELD_NUMBER: _ClassVar[int]
        ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
        LIBRARYNAME_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        functionName: str
        arguments: _containers.RepeatedCompositeFieldContainer[QuaProgram.LibFunctionExpression.Argument]
        libraryName: str
        loc: str
        def __init__(self, functionName: _Optional[str] = ..., arguments: _Optional[_Iterable[_Union[QuaProgram.LibFunctionExpression.Argument, _Mapping]]] = ..., libraryName: _Optional[str] = ..., loc: _Optional[str] = ...) -> None: ...
    class FunctionExpression(_message.Message):
        __slots__ = ["xor", "loc"]
        class ScalarOrVectorArgument(_message.Message):
            __slots__ = ["scalar", "array"]
            SCALAR_FIELD_NUMBER: _ClassVar[int]
            ARRAY_FIELD_NUMBER: _ClassVar[int]
            scalar: QuaProgram.AnyScalarExpression
            array: QuaProgram.ArrayVarRefExpression
            def __init__(self, scalar: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., array: _Optional[_Union[QuaProgram.ArrayVarRefExpression, _Mapping]] = ...) -> None: ...
        class AndFunction(_message.Message):
            __slots__ = ["values"]
            VALUES_FIELD_NUMBER: _ClassVar[int]
            values: _containers.RepeatedCompositeFieldContainer[QuaProgram.FunctionExpression.ScalarOrVectorArgument]
            def __init__(self, values: _Optional[_Iterable[_Union[QuaProgram.FunctionExpression.ScalarOrVectorArgument, _Mapping]]] = ...) -> None: ...
        class OrFunction(_message.Message):
            __slots__ = ["values"]
            VALUES_FIELD_NUMBER: _ClassVar[int]
            values: _containers.RepeatedCompositeFieldContainer[QuaProgram.FunctionExpression.ScalarOrVectorArgument]
            def __init__(self, values: _Optional[_Iterable[_Union[QuaProgram.FunctionExpression.ScalarOrVectorArgument, _Mapping]]] = ...) -> None: ...
        class XorFunction(_message.Message):
            __slots__ = ["values"]
            VALUES_FIELD_NUMBER: _ClassVar[int]
            values: _containers.RepeatedCompositeFieldContainer[QuaProgram.FunctionExpression.ScalarOrVectorArgument]
            def __init__(self, values: _Optional[_Iterable[_Union[QuaProgram.FunctionExpression.ScalarOrVectorArgument, _Mapping]]] = ...) -> None: ...
        AND_FIELD_NUMBER: _ClassVar[int]
        OR_FIELD_NUMBER: _ClassVar[int]
        XOR_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        xor: QuaProgram.FunctionExpression.XorFunction
        loc: str
        def __init__(self, xor: _Optional[_Union[QuaProgram.FunctionExpression.XorFunction, _Mapping]] = ..., loc: _Optional[str] = ..., **kwargs) -> None: ...
    class BroadcastExpression(_message.Message):
        __slots__ = ["value", "loc"]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        LOC_FIELD_NUMBER: _ClassVar[int]
        value: QuaProgram.AnyScalarExpression
        loc: str
        def __init__(self, value: _Optional[_Union[QuaProgram.AnyScalarExpression, _Mapping]] = ..., loc: _Optional[str] = ...) -> None: ...
    class GlobalVarRefExpression(_message.Message):
        __slots__ = ["loc", "bits", "operation"]
        LOC_FIELD_NUMBER: _ClassVar[int]
        BITS_FIELD_NUMBER: _ClassVar[int]
        OPERATION_FIELD_NUMBER: _ClassVar[int]
        loc: str
        bits: _containers.RepeatedScalarFieldContainer[int]
        operation: QuaProgram.GlobalVarOperation
        def __init__(self, loc: _Optional[str] = ..., bits: _Optional[_Iterable[int]] = ..., operation: _Optional[_Union[QuaProgram.GlobalVarOperation, str]] = ...) -> None: ...
    class DynamicConfig(_message.Message):
        __slots__ = ["version", "root"]
        VERSION_FIELD_NUMBER: _ClassVar[int]
        ROOT_FIELD_NUMBER: _ClassVar[int]
        version: int
        root: _struct_pb2.Struct
        def __init__(self, version: _Optional[int] = ..., root: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    DYNCONFIG_FIELD_NUMBER: _ClassVar[int]
    SCRIPT_FIELD_NUMBER: _ClassVar[int]
    COMPILEROPTIONS_FIELD_NUMBER: _ClassVar[int]
    RESULTANALYSIS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_UPDATE_FIELD_NUMBER: _ClassVar[int]
    config: _inc_qua_config_pb2.QuaConfig
    dynConfig: QuaProgram.DynamicConfig
    script: QuaProgram.Script
    compilerOptions: QuaProgram.CompilerOptions
    resultAnalysis: QuaResultAnalysis
    config_update: _inc_qua_config_pb2.QuaConfig
    def __init__(self, config: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ..., dynConfig: _Optional[_Union[QuaProgram.DynamicConfig, _Mapping]] = ..., script: _Optional[_Union[QuaProgram.Script, _Mapping]] = ..., compilerOptions: _Optional[_Union[QuaProgram.CompilerOptions, _Mapping]] = ..., resultAnalysis: _Optional[_Union[QuaResultAnalysis, _Mapping]] = ..., config_update: _Optional[_Union[_inc_qua_config_pb2.QuaConfig, _Mapping]] = ...) -> None: ...

class QuaResultAnalysis(_message.Message):
    __slots__ = ["version", "model"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    version: int
    model: _containers.RepeatedCompositeFieldContainer[_struct_pb2.ListValue]
    def __init__(self, version: _Optional[int] = ..., model: _Optional[_Iterable[_Union[_struct_pb2.ListValue, _Mapping]]] = ...) -> None: ...
