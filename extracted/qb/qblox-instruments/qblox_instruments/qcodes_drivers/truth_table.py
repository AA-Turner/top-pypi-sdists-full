# --------------------------------------------------------------------------
# Description    : TruthTable QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2025)
# --------------------------------------------------------------------------

from __future__ import annotations

import itertools
import warnings
from dataclasses import dataclass
from typing import Any

# Define valid options for measurement and level.
MEASUREMENT_OPTIONS = ("count", "digital")
LEVEL_OPTIONS = ("low", "mid", "high", "invalid")


@dataclass(frozen=True)
class ChannelMeasurement:
    """
    Represents a measurement on a specific channel.

    Parameters
    ----------
    channel : int
        The channel number (must be in 0...7).
    measurement : str
        The measurement type (must be one of :class:`MEASUREMENT_OPTIONS`).
    """

    channel: int
    measurement: str

    def __post_init__(self) -> None:
        if not (0 <= self.channel <= 7):
            raise ValueError(f"Invalid channel '{self.channel}'. Channel must be in range 0...7")
        if self.measurement not in MEASUREMENT_OPTIONS:
            raise ValueError(
                f"Invalid measurement type '{self.measurement}'. "
                f"Valid options: {MEASUREMENT_OPTIONS}"
            )


@dataclass(frozen=True)
class Condition:
    """
    Represents a condition for a truth table entry, combining a channel measurement with a level.

    Parameters
    ----------
    channel_measurement : ChannelMeasurement
        The channel measurement.
    level : str
        The level (must be one of :class:`LEVEL_OPTIONS`).
    """

    channel_measurement: ChannelMeasurement
    level: str

    def __post_init__(self) -> None:
        if self.level not in LEVEL_OPTIONS:
            raise ValueError(f"Invalid level '{self.level}'. Valid options: {LEVEL_OPTIONS}")

    def __str__(self) -> str:
        return (
            f"channel{self.channel_measurement.channel}_"
            f"{self.channel_measurement.measurement}_"
            f"{self.level}"
        )


@dataclass(frozen=True)
class TruthTableEntry:
    """
    Represents an entry in the truth table.

    Parameters
    ----------
    conditions : list[Condition]
        List of conditions that must be met.
    trigger_address : int
        The trigger address associated with these conditions.
    """

    conditions: list[Condition]
    trigger_address: int


class TruthTable:
    """
    Truth table manager class.

    Attributes
    ----------
    MAX_INPUTS : int
        Maximum number of distinct input channels allowed.
    MAX_TRIGGER_ADDRESSES : int
        Maximum number of distinct trigger addresses allowed.
    """

    MAX_INPUTS: int = 4
    MAX_TRIGGER_ADDRESSES: int = 4

    def __init__(self, default_trigger_address: int = 0, overwrite_conflict: bool = False) -> None:
        """
        Initialize the TruthTable.

        Parameters
        ----------
        default_trigger_address : int, optional
            The default trigger address. Must be in range 0...15.
        overwrite_conflict : bool, optional
            Whether to overwrite existing LUT entries on conflict.

        Raises
        ------
        ValueError
            If the default trigger address is not in range 0...15.
        """
        if not (0 <= default_trigger_address <= 15):
            raise ValueError(
                f"Invalid default trigger address '{default_trigger_address}'. "
                "Default trigger address must be in range 0...15"
            )
        self._default_trigger_address: int = default_trigger_address
        self._overwrite_conflict: bool = overwrite_conflict

        self._truth_table: list[TruthTableEntry] = []
        # Stores the user-defined conditions and their corresponding trigger addresses.

        self._all_entries: list[TruthTableEntry] = []
        # Contains the expanded version of `self._truth_table`.
        # It includes all possible input combinations that map to a specific trigger address,
        # accounting for implicit conditions where certain inputs can take multiple valid levels.

        self._truth_table_inputs: list[ChannelMeasurement] = []
        self._trigger_addresses: set[int] = {default_trigger_address}
        self._lut: dict[str, Any] = {}

    def __str__(self) -> str:
        """
        Returns a string representation of the entire `TruthTable`.

        Returns
        -------
        str
            For each combination of input levels, displays a line in the format:
            IF (channel0_count_low && channel1_digital_high ... ) THEN set trigger address <value>
        """
        msg = "Truth Table:\n"
        for entry in self._all_entries:
            msg += f"  IF ({' && '.join(str(cond) for cond in entry.conditions)}) "
            msg += f"THEN set trigger address {entry.trigger_address}\n"
        msg += f"Default Trigger Address: {self._default_trigger_address}\n"
        return msg

    @property
    def lut(self) -> dict[str, Any]:
        """
        Returns the lookup table (LUT).

        Returns
        -------
        dict
            A dictionary with keys: `src` and `lut`,
                `src` - list of input configurations,
                `lut` - list of trigger addresses.
        """
        return self._lut

    def _encode(self) -> dict[str, Any]:
        """
        Encodes the current truth table into a lookup table (LUT).

        Returns
        -------
        dict
            A dictionary with keys: `src` and `lut`,
                `src` - list of input configurations,
                `lut` - list of trigger addresses.
        """
        # Create mapping from each ChannelMeasurement to its index.
        input_mapping = {cm: idx for idx, cm in enumerate(self._truth_table_inputs)}
        num_inputs_used = len(input_mapping)
        num_levels = len(LEVEL_OPTIONS)
        lut_size = num_levels**num_inputs_used
        lut = [self._default_trigger_address] * lut_size
        self._all_entries = []

        for entry in self._truth_table:
            conditions = entry.conditions
            trigger_address = entry.trigger_address

            # For each input, start with all possible level indices.
            input_options = [tuple(range(num_levels)) for _ in range(num_inputs_used)]
            for condition in conditions:
                cm = condition.channel_measurement
                if cm in input_mapping:
                    ch_index = input_mapping[cm]
                    try:
                        level_index = LEVEL_OPTIONS.index(condition.level)
                    except ValueError as e:
                        raise ValueError(
                            f"Invalid level '{condition.level}'. Valid options: {LEVEL_OPTIONS}"
                        ) from e
                    # Restrict this channel to the specific level.
                    input_options[ch_index] = (level_index,)

            # For every combination of input levels, update the LUT.
            for input_values in itertools.product(*input_options):
                index = sum(val * (num_levels**i) for i, val in enumerate(input_values))
                combined_conditions = [
                    Condition(channel_measurement=cm, level=LEVEL_OPTIONS[level])
                    for cm, level in zip(self._truth_table_inputs, input_values)
                ]

                self._all_entries.append(TruthTableEntry(combined_conditions, trigger_address))

                if lut[index] != self._default_trigger_address and lut[index] != trigger_address:
                    conflict_msg = (
                        f"Conflict while setting LUT entry to trigger address {trigger_address}.\n"
                        f"Condition ({' && '.join(str(cond) for cond in combined_conditions)}) "
                        f"is already set to trigger address {lut[index]}."
                    )
                    if self._overwrite_conflict:
                        warnings.warn(
                            f"{conflict_msg}\nOverwriting with trigger address {trigger_address}."
                        )
                    else:
                        raise ValueError(conflict_msg)
                lut[index] = trigger_address

        src = [{"ch": cm.channel, "cfg": cm.measurement} for cm in self._truth_table_inputs]
        return {"src": src, "lut": lut}

    def add_conditions(self, conditions: list[Condition], trigger_address: int) -> None:
        """
        Adds a set of conditions with an associated trigger address to the truth table.

        Parameters
        ----------
        conditions : list[Condition]
            List of conditions to add.
        trigger_address : int
            Trigger address to associate with these conditions. Must be in range 1...15.

        Raises
        ------
        ValueError
            If trigger_address is not in range 1...15.
            If number of distinct inputs exceeds `MAX_INPUTS`.
            If adding the trigger_address would exceed `MAX_TRIGGER_ADDRESSES`.
            If a conflict is detected in the LUT and overwriting is disabled.
        """
        # Validate trigger address range.
        if not (1 <= trigger_address <= 15):
            raise ValueError(
                f"Invalid trigger address '{trigger_address}'. "
                "Trigger address must be in range 1...15"
            )

        for condition in conditions:
            if condition.channel_measurement not in self._truth_table_inputs:
                self._truth_table_inputs.append(condition.channel_measurement)
                if len(self._truth_table_inputs) > self.MAX_INPUTS:
                    raise ValueError(
                        f"Only {self.MAX_INPUTS} distinct inputs are allowed. "
                        f"Current inputs: {self._truth_table_inputs}"
                    )

        self._trigger_addresses.add(trigger_address)
        if len(self._trigger_addresses) > self.MAX_TRIGGER_ADDRESSES:
            raise ValueError(
                f"Trigger address {trigger_address} cannot be added. "
                "It exceeds the maximum number of trigger addresses "
                f"({self.MAX_TRIGGER_ADDRESSES}). "
                f"Current trigger addresses: {self._trigger_addresses}"
            )

        entry = TruthTableEntry(conditions=conditions, trigger_address=trigger_address)
        self._truth_table.append(entry)
        self._lut = self._encode()

    @classmethod
    def from_config(
        cls, entries: list, default_trigger_address: int = 0, overwrite_conflict: bool = False
    ) -> TruthTable:
        """
        Builds a TruthTable from a list of dictionaries.

        Parameters
        ----------
        entries : list of dict
            List of configuration dictionary entries.
        default_trigger_address : int, optional
            Default trigger address.
        overwrite_conflict : bool, optional
            Whether to overwrite conflicts in the LUT.

        Returns
        -------
        TruthTable
            The constructed truth table.

        Notes
        -----
        Each dictionary is expected to have the format:

        .. code-block:: python

            {
                "conditions": [
                    {"channel": int, "measurement": str, "level": str},
                    ...
                ],
                "trigger": int
            }
        """
        tt = cls(default_trigger_address, overwrite_conflict)
        for entry in entries:
            conditions = [
                Condition(
                    channel_measurement=ChannelMeasurement(
                        channel=condition["channel"], measurement=condition["measurement"]
                    ),
                    level=condition["level"],
                )
                for condition in entry["conditions"]
            ]
            tt.add_conditions(conditions, entry["trigger"])
        return tt
