# ----------------------------------------------------------------------------
# Description    : Native interface constants and enums
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import copy
import warnings
from builtins import FutureWarning
from collections import namedtuple
from enum import Enum
from typing import Any, Optional

# -- definitions -------------------------------------------------------------


# State enum base class
class StateEnum(Enum):
    """
    State enum base class that arranges child enum string representations.
    """

    def __repr__(self) -> str:
        return "<{}.{}>".format(str(type(self)).split("'")[1], self.name)

    def __str__(self) -> str:
        return str(self.name)

    def __eq__(self, other: Any) -> bool:
        if type(self) is type(other):
            return str(self) == str(other)
        elif other in [str(val) for val in type(self)]:
            return str(self) == other
        else:
            raise KeyError(f"{other} is not of type {type(self)}")

    def __key__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash(self.__key__())


class DeprecatedStateEnum(StateEnum):
    """
    State enum class that throws deprecation warning.
    """

    def __init__(self, _warning_message) -> None:
        self.warning_message = _warning_message

    def _deprecation_warning(self) -> None:
        warnings.warn(
            f"{self.warning_message}",
            FutureWarning,
            stacklevel=2,
        )

    def __str__(self) -> str:
        self._deprecation_warning()
        return StateEnum.__str__(self)

    def __repr__(self) -> str:
        self._deprecation_warning()
        return StateEnum.__repr__(self)

    def __eq__(self, other: Any) -> bool:
        self._deprecation_warning()
        return StateEnum.__eq__(self, other)

    def __key__(self) -> str:
        self._deprecation_warning()
        return StateEnum.__key__(self)

    def __hash__(self) -> int:
        self._deprecation_warning()
        return StateEnum.__hash__(self)


# It will be deprecated
# State tuple base class
class StateTuple:
    """
    State tuple base class that arranges child tuple string representations.
    """

    def __init__(self, _warning_message) -> None:
        self.warning_message = _warning_message

    def _deprecation_warning(self) -> None:
        warnings.warn(
            f"{self.warning_message}",
            FutureWarning,
            stacklevel=2,
        )

    def __str__(self) -> str:
        # Status, flags and slot_flags are inherited from the child class
        # using virtual inheritance, so we retrieve these attributes through
        # getattr to not upset Pylint
        status = getattr(self, "status")
        flags = getattr(self, "flags")
        flags = ", ".join([str(flag) for flag in flags]) if len(flags) > 0 else "NONE"
        pretty_str = f"Status: {status}, Flags: {flags}"

        if hasattr(self, "slot_flags"):
            slot_flags = getattr(self, "slot_flags")
            pretty_str += f", Slot flags: {slot_flags}"
        self._deprecation_warning()
        return pretty_str


# State tuple base class
class SystemStatusTuple:
    """
    System Status tuple base class that arranges child tuple string representations.
    """

    def __str__(self) -> str:
        # Status, flags and slot_flags are inherited from the child class
        # using virtual inheritance, so we retrieve these attributes through
        # getattr to not upset Pylint
        status = getattr(self, "status")
        flags = getattr(self, "flags")
        flags = ", ".join([str(flag) for flag in flags]) if len(flags) > 0 else "NONE"
        pretty_str = f"Status: {status}, Flags: {flags}"

        if hasattr(self, "slot_flags"):
            slot_flags = getattr(self, "slot_flags")
            pretty_str += f", Slot flags: {slot_flags}"
        return pretty_str


class StatusTuple:
    """
    Status tuple base class that arranges child tuple string representations.
    """

    def __str__(self) -> str:
        # getattr to not upset Pylint
        state = getattr(self, "state")
        status = getattr(self, "status")
        info_flags = getattr(self, "info_flags")
        warn_flags = getattr(self, "warn_flags")
        err_flags = getattr(self, "err_flags")
        log = getattr(self, "log")

        flags = [info_flags, warn_flags, err_flags]
        for type_idx, type_flags in enumerate(flags):
            if len(type_flags) > 0:
                flags[type_idx] = ", ".join([str(flag) for flag in type_flags])
            else:
                flags[type_idx] = "NONE"

        pretty_str = (
            f"Status: {status}, "
            f"State: {state}, "
            f"Info Flags: {flags[0]}, "
            f"Warning Flags: {flags[1]}, "
            f"Error Flags: {flags[2]}, "
            f"Log: {log}"
        )

        return pretty_str


# All System status enum
class SystemStatuses(StateEnum):
    """
    System status enum.
    """

    BOOTING = "System is booting."
    OKAY = "System is okay."
    RESOLVED = "An error indicated by the flags occurred, but has been resolved."
    ERROR = "An error indicated by the flags is occurring."
    CRIT_ERROR = "A critical error indicated by the flags is occurring"


# System status flags enum
class SystemStatusFlags(StateEnum):
    """
    System status flags enum.
    """

    PLL_UNLOCKED = "PLL is unlocked."
    TEMPERATURE_OUT_OF_RANGE = "Temperature is out of range."
    CRIT_TEMPERATURE_OUT_OF_RANGE = "Temperature is critically out of range."
    MODULE_NOT_CONNECTED = "Module is not connected."
    MODULE_FIRM_OR_HARDWARE_INCOMPATIBLE = "Module firmware is incompatible"
    FEEDBACK_NETWORK_CALIBRATION_FAILED = "The feedback network calibration failed."
    HARDWARE_COMPONENT_FAILED = "Hardware component failed"
    TRIGGER_NETWORK_MISSED_EXT_TRIGGER = "Trigger Network Missed External Trigger."


# Namedtuple representing the slot status flags
NUM_SLOTS = 20


class SystemStatusSlotFlags(
    namedtuple(
        "SystemStatusSlotFlags",
        [f"slot{slot}" for slot in range(1, NUM_SLOTS + 1)],
    )
):
    """
    Tuple containing lists of Cluster slot status flag enums of type
    :class:`~qblox_instruments.native.definitions.SystemStatusFlags`. Each Cluster slot has its
    own status flag list attribute named `slot<X>`.
    """

    __name__ = "SystemStatusSlotFlags"
    __slots__ = ()

    def __new__(cls, slot_flags: Optional[dict] = None) -> "SystemStatusSlotFlags":
        slot_flags = slot_flags or {}  # Avoid mutable default argument
        slot_flag_lists = [[] for _ in range(NUM_SLOTS)]
        for slot in range(0, NUM_SLOTS):
            slot_str = f"slot{slot + 1}"
            if slot_str in slot_flags:
                slot_flag_lists[slot] = slot_flags[slot_str]
        return super().__new__(cls, *slot_flag_lists)

    def __repr__(self) -> str:
        slot_str_list = []
        for slot in range(0, NUM_SLOTS):
            if len(self[slot]) > 0:
                slot_str_list.append(f"slot{slot + 1}={self[slot]}")  # noqa: PERF401
        return f"{self.__name__}({', '.join(slot_str_list)})"

    def __str__(self) -> str:
        slot_str_list = []
        for slot in range(0, NUM_SLOTS):
            for flag in self[slot]:
                slot_str_list.append(f"SLOT{slot + 1}_{flag}")  # noqa: PERF401
        if len(slot_str_list) > 0:
            return ", ".join(slot_str_list)
        else:
            return "NONE"


# Namedtuple representing the system status
class SystemStatus(
    namedtuple("SystemStatus", ["status", "flags", "slot_flags"]), SystemStatusTuple
):
    """
    System status tuple returned by :func:`!get_system_status`. The tuple
    contains a system status enum of type
    :class:`~qblox_instruments.native.definitions.SystemStatuses`, a list of associated system
    status flag enums of type
    :class:`~qblox_instruments.native.definitions.SystemStatusFlags` and a tuple of type
    :class:`~qblox_instruments.native.definitions.SystemStatusSlotFlags` containing Cluster slot
    status flags.
    """

    pass


SystemStatus.status.__doc__ = """
System status enum of type :class:`~qblox_instruments.native.definitions.SystemStatuses`.
"""
SystemStatus.flags.__doc__ = """
List of system status flag enums of type
:class:`~qblox_instruments.native.definitions.SystemStatusFlags`.
"""
SystemStatus.slot_flags.__doc__ = """
Tuple of type :class:`~qblox_instruments.native.definitions.SystemStatusSlotFlags containing
Cluster slot status flags
"""


# Sequencer states enum
class SequencerStates(StateEnum):
    """
    Sequencer state enum.
    """

    IDLE = "Sequencer waiting to be armed and started."
    ARMED = "Sequencer is armed and ready to start."
    RUNNING = "Sequencer is running."
    Q1_STOPPED = "Classical part of the sequencer has stopped; waiting for real-time part to stop."
    STOPPED = "Sequencer has completely stopped."


# Sequencer statuses enum
class SequencerStatuses(StateEnum):
    """
    Sequencer status enum.
    """

    OKAY = "OKAY"
    WARNING = "WARNING"
    ERROR = "ERROR"


# Sequencer status flags enum
class SequencerStatusFlags(StateEnum):
    """
    Sequencer status flags enum.
    """

    DISARMED = "Sequencer was disarmed."
    FORCED_STOP = "Sequencer was stopped while still running."
    SEQUENCE_PROCESSOR_Q1_ILLEGAL_INSTRUCTION = (
        "Classical sequencer part executed an unknown instruction."
    )
    SEQUENCE_PROCESSOR_RT_EXEC_ILLEGAL_INSTRUCTION = (
        "Real-time sequencer part executed an unknown instruction."
    )
    SEQUENCE_PROCESSOR_RT_EXEC_COMMAND_UNDERFLOW = (
        "Real-time sequencer part command queue underflow."
    )
    AWG_WAVE_PLAYBACK_INDEX_INVALID_PATH_0 = "AWG path 0 tried to play an unknown waveform."
    AWG_WAVE_PLAYBACK_INDEX_INVALID_PATH_1 = "AWG path 1 tried to play an unknown waveform."
    ACQ_WEIGHT_PLAYBACK_INDEX_INVALID_PATH_0 = "Acquisition path 0 tried to play an unknown weight."
    ACQ_WEIGHT_PLAYBACK_INDEX_INVALID_PATH_1 = "Acquisition path 1 tried to play an unknown weight."
    ACQ_SCOPE_DONE_PATH_0 = "Scope acquisition for path 0 has finished."
    ACQ_SCOPE_OUT_OF_RANGE_PATH_0 = "Scope acquisition data for path 0 was out-of-range."
    ACQ_SCOPE_OVERWRITTEN_PATH_0 = "Scope acquisition data for path 0 was overwritten."
    ACQ_SCOPE_DONE_PATH_1 = "Scope acquisition for path 1 has finished."
    ACQ_SCOPE_OUT_OF_RANGE_PATH_1 = "Scope acquisition data for path 1 was out-of-range."
    ACQ_SCOPE_OVERWRITTEN_PATH_1 = "Scope acquisition data for path 1 was overwritten."
    ACQ_SCOPE_DONE_PATH_2 = "Scope acquisition for path 2 has finished."
    ACQ_SCOPE_OUT_OF_RANGE_PATH_2 = "Scope acquisition data for path 2 was out-of-range."
    ACQ_SCOPE_OVERWRITTEN_PATH_2 = "Scope acquisition data for path 2 was overwritten."
    ACQ_SCOPE_DONE_PATH_3 = "Scope acquisition for path 3 has finished."
    ACQ_SCOPE_OUT_OF_RANGE_PATH_3 = "Scope acquisition data for path 3 was out-of-range."
    ACQ_SCOPE_OVERWRITTEN_PATH_3 = "Scope acquisition data for path 3 was overwritten."
    ACQ_BINNING_DONE = "Acquisition binning completed."
    ACQ_BINNING_FIFO_ERROR = "Acquisition binning encountered internal FIFO error."
    ACQ_BINNING_COMM_ERROR = "Acquisition binning encountered internal communication error."
    ACQ_BINNING_OUT_OF_RANGE = "Acquisition binning data out-of-range."
    ACQ_INDEX_INVALID = "Acquisition tried to process an invalid acquisition."
    ACQ_BIN_INDEX_INVALID = "Acquisition tried to process an invalid bin."
    TRIGGER_NETWORK_CONFLICT = "Trigger network has encountered a conflict."
    TRIGGER_NETWORK_MISSED_INTERNAL_TRIGGER = "Trigger network missed an internal trigger."
    OUTPUT_OVERFLOW = "Output overflow."
    CLOCK_INSTABILITY = "Clock source instability occurred."
    ACQ_INTEGRATOR_OUT_OF_RANGE_PATH_0 = (
        "Acquisition integration input data for path 0 was out-of-range."
    )
    ACQ_INTEGRATOR_OUT_OF_RANGE_PATH_1 = (
        "Acquisition integration input data for path 1 was out-of-range."
    )
    DIO_COMMAND_OVERFLOW = "DIO_COMMAND_OVERFLOW"
    DIO_DELAY_OUT_OF_ORDER = "DIO_DELAY_OUT_OF_ORDER"
    DIO_UNSUPPORTED_PULSE_WIDTH = "DIO_UNSUPPORTED_PULSE_WIDTH"
    DIO_TIMETAG_DEADLINE_MISSED = "DIO_TIMETAG_DEADLINE_MISSED"
    DIO_TIME_DELTA_INVALID = "DIO_TIME_DELTA_INVALID"
    DIO_COUNT_INVALID = "DIO_COUNT_INVALID"
    DIO_THRESHOLD_INVALID = "DIO_THRESHOLD_INVALID"
    DIO_INTERNAL_ERROR = "DIO_INTERNAL_ERROR"


class SequencerStatus(
    namedtuple(
        "SequencerStatus",
        ["status", "state", "info_flags", "warn_flags", "err_flags", "log"],
    ),
    StatusTuple,
):
    """
    Sequencer status tuple returned by :func:`!get_sequencer_status`. The tuple
    contains a sequencer status, state, flags and log. The tuple contains:
    a sequencer status enum of type :class:`~qblox_instruments.native.definitions.SequencerStatuses`,
    a sequencer state enum of type :class:`~qblox_instruments.native.definitions.SequencerStates`,
    a list of associated info flags enums of type :class:`~qblox_instruments.native.definitions.SequencerStatusFlags`,
    a list of associated warning flags enums of type :class:`~qblox_instruments.native.definitions.SequencerStatusFlags`,
    a list of associated error flags enums of type :class:`~qblox_instruments.native.definitions.SequencerStatusFlags`,
    a list of informative log message of type :class:`str`.
    """  # noqa: E501

    pass


SequencerStatus.status.__doc__ = """
Sequencer status enum of type :class:`~qblox_instruments.native.definitions.SequencerStatuses`.
"""

SequencerStatus.state.__doc__ = """
Sequencer state enum of type :class:`~qblox_instruments.native.definitions.SequencerStates`.
"""

SequencerStatus.info_flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.definitions.SequencerStatusFlags`.
"""

SequencerStatus.warn_flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.definitions.SequencerStatusFlags`.
"""

SequencerStatus.err_flags.__doc__ = """
List of sequencer status flag enums of type
:class:`~qblox_instruments.native.definitions.SequencerStatusFlags`.
"""

SequencerStatus.log.__doc__ = """
List of log message with more detailed information in case of WARNING status.
"""

# Maximum program length allowed
MAX_PROGRAM_LENGTH = 10 * (128 * 1024 * 8 + 1024)

# JSON schema to validate sequence dictionaries with
QCM_SEQUENCE_JSON_SCHEMA = {
    "title": "Sequence container",
    "description": (
        "Contains all waveforms, weights and acquisitions and a program required for a sequence."
    ),
    "type": "object",
    "required": ["program", "waveforms"],
    "properties": {
        "program": {
            "description": "Sequencer assembly program in string format.",
            "type": "string",
        },
        "waveforms": {
            "description": "Waveform dictionary containing one or multiple AWG waveform(s).",
            "type": "object",
        },
        "weights": {
            "description": "Weight dictionary containing one or multiple acquisition weights(s).",
            "type": "object",
        },
        "acquisitions": {
            "description": (
                "Acquisition dictionary containing information about one "
                "or multiple acquisition(s)."
            ),
            "type": "object",
        },
    },
}

# JSON schema to validate QRM sequence dictionaries with
QRM_SEQUENCE_JSON_SCHEMA = copy.deepcopy(QCM_SEQUENCE_JSON_SCHEMA)
QRM_SEQUENCE_JSON_SCHEMA["required"] = [
    "program",
    "waveforms",
    "weights",
    "acquisitions",
]

# JSON schema to validate waveform and weight dictionaries with
WAVE_JSON_SCHEMA = {
    "title": "Waveform/weight container",
    "description": "Waveform/weight dictionary for a single waveform.",
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {"description": "List of waveform samples.", "type": "array"},
        "index": {"description": "Optional waveform index number.", "type": "number"},
    },
}

# JSON schema to validate acquisition dictionaries with
ACQ_JSON_SCHEMA = {
    "title": "Acquisition container",
    "description": "Acquisition dictionary for a single acquisition.",
    "type": "object",
    "required": ["num_bins"],
    "properties": {
        "num_bins": {"description": "Number of bins in acquisition.", "type": "number"},
        "index": {"description": "Optional waveform index number.", "type": "number"},
    },
}

# JSON schema to validate sequence dictionaries with
# TODO QTM, add more fields here for V2
QTM_SEQUENCE_JSON_SCHEMA = {
    "title": "Sequence container",
    "description": "Contains all acquisitions and a program required for a sequence.",
    "type": "object",
    "required": ["program"],
    "properties": {
        "program": {
            "description": "Sequencer assembly program in string format.",
            "type": "string",
        },
        "acquisitions": {
            "description": (
                "Acquisition dictionary containing information about one "
                "or multiple acquisition(s)."
            ),
            "type": "object",
        },
    },
}
