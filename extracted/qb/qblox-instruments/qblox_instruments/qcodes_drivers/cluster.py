# --------------------------------------------------------------------------
# Description    : Cluster QCoDeS interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# --------------------------------------------------------------------------
import warnings
from functools import partial

# -- include -----------------------------------------------------------------
from typing import Any, Callable, Optional, Union

from qcodes import Instrument, InstrumentChannel, Parameter
from qcodes import validators as vals

from qblox_instruments import DeviceInfo, SystemStatusFlags
from qblox_instruments.native import Cluster as ClusterNative
from qblox_instruments.qcodes_drivers.module import Module, get_item
from qblox_instruments.qcodes_drivers.time import Time
from qblox_instruments.types import DebugLevel

# -- class -------------------------------------------------------------------


class Cluster(ClusterNative, Instrument):
    """
    This class connects `QCoDeS <https://microsoft.github.io/Qcodes/>`_ to the
    Cluster native interface.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        name: str,
        identifier: Optional[str] = None,
        port: Optional[int] = None,
        debug: Optional[DebugLevel] = None,
        dummy_cfg: Optional[dict] = None,
    ) -> None:
        """
        Creates Cluster QCoDeS class and adds all relevant instrument
        parameters. These instrument parameters call the associated methods
        provided by the native interface.

        Parameters
        ----------
        name : str
            Instrument name.
        identifier : Optional[str]
            Instrument identifier. See :func:`~qblox_instruments.resolve()`.
            If None, the instrument is identified by name.
        port : Optional[int]
            Override for the TCP port through which we should connect.
        debug : Optional[DebugLevel]
            Debug level. See :class:`~qblox_instruments.types.DebugLevel` for more
            information. By default None, which means that for a connection to a dummy
            cluster, `DebugLevel.ERROR_CHECK` will be used, and for a real cluster,
            `DebugLevel.VERSION_CHECK`.
        dummy_cfg : Optional[dict]
            Configure as dummy using this configuration. For each slot that
            needs to be occupied by a module add the slot index as key and
            specify the type of module in the slot using the type
            :class:`~qblox_instruments.ClusterType`.
        """
        # For backwards compatibility: a boolean used to work, where True was
        # interpreted as "no version check" and False as the default value.
        if isinstance(debug, bool):
            warnings.warn(
                "Passing a boolean argument for the `debug` parameter is deprecated and could "
                "cause unexpected behaviour in a future version.",
                FutureWarning,
            )
            debug = DebugLevel.ERROR_CHECK if debug else None

        # Initialize parent classes.
        if identifier is None:
            identifier = name
        super().__init__(identifier, port, debug, dummy_cfg)
        Instrument.__init__(self, name)

        # Check for any errors that occurred during initialization
        status = self.get_system_status()
        if status.status == "ERROR":
            for slot_idx, slot_err in enumerate(status.slot_flags):
                if slot_err and any(
                    err == SystemStatusFlags.MODULE_FIRM_OR_HARDWARE_INCOMPATIBLE
                    for err in slot_err
                ):
                    if self._debug in (DebugLevel.ERROR_CHECK, DebugLevel.NO_CHECK):
                        warnings.warn(
                            f"Received a module incompatibility error in slot "
                            f"{slot_idx + 1}: \n -> {status}"
                        )
                    else:
                        raise ConnectionError(
                            f"Received the following Error Status in slot "
                            f"{slot_idx + 1}: \n -> {status}"
                        )

        # Set number of slots
        self._num_slots = 20

        # Add QCoDeS parameters
        self.add_parameter(
            "led_brightness",
            label="LED brightness",
            docstring="Sets/gets frontpanel LED brightness.",
            unit="",
            vals=vals.Strings(),
            val_mapping={
                "off": "OFF",
                "low": "LOW",
                "medium": "MEDIUM",
                "high": "HIGH",
            },
            set_parser=str,
            get_parser=str,
            set_cmd=self._set_led_brightness,
            get_cmd=self._get_led_brightness,
        )

        self.add_parameter(
            "reference_source",
            label="Reference source.",
            docstring="Sets/gets reference source ('internal' = internal "
            "10 MHz, 'external' = external 10 MHz).",
            unit="",
            vals=vals.Bool(),
            val_mapping={"internal": True, "external": False},
            set_parser=bool,
            get_parser=bool,
            set_cmd=self._set_reference_source,
            get_cmd=self._get_reference_source,
        )

        self.add_parameter(
            "ext_trigger_input_delay",
            label="Trigger input delay.",
            docstring="Sets/gets the delay of the external input trigger in picoseconds.",
            unit="ps",
            vals=vals.Multiples(39, min_value=0, max_value=31 * 39),
            set_parser=int,
            get_parser=int,
            set_cmd=self.set_trg_in_delay,
            get_cmd=self.get_trg_in_delay,
        )

        self.add_parameter(
            "ext_trigger_input_trigger_en",
            label="Trigger input enable.",
            docstring="Enable/disable the external input trigger.",
            unit="",
            vals=vals.Bool(),
            set_parser=bool,
            get_parser=bool,
            set_cmd=self.set_trg_in_map_en,
            get_cmd=self.get_trg_in_map_en,
        )

        self.add_parameter(
            "ext_trigger_input_trigger_address",
            label="Trigger address.",
            docstring="Sets/gets the external input trigger address to which "
            "the input trigger is mapped to the trigger network (T1 to "
            "T15).",
            unit="",
            vals=vals.Numbers(1, 15),
            set_parser=int,
            get_parser=int,
            set_cmd=self.set_trg_in_map_addr,
            get_cmd=self.get_trg_in_map_addr,
        )

        for x in range(1, 16):
            self.add_parameter(
                f"trigger{x}_monitor_count",
                label=f"Trigger monitor count for trigger address T{x}.",
                docstring=f"Gets the trigger monitor count from trigger address T{x}.",
                unit="",
                get_cmd=partial(self.get_trigger_monitor_count, int(x)),
            )

        self.add_parameter(
            "trigger_monitor_latest",
            label="Latest monitor trigger for trigger address.",
            docstring="Gets the trigger address which was triggered last (T1 to T15).",
            unit="",
            get_cmd=self.get_trigger_monitor_latest,
        )

        self.__add_modules()

    # ------------------------------------------------------------------------
    def __reinitialize_modules(self) -> None:
        """
        Reinitialize modules based on the physical state of the slots.
        """
        slot_info = self.get_json_description().get("modules", {})

        # Iterate over slot information to update or add modules
        for slot_str, info in slot_info.items():
            slot_id = int(slot_str)

            # Skip if serial matches
            if (
                slot_id in self._mod_handles
                and DeviceInfo.from_dict(info).serial == self._mod_handles[slot_id]["serial"]
            ):
                continue

            # Recreate module handle and add module
            self._create_mod_handles(slot_id)
            self.__add_modules(slot_id)

        # Remove entries if their slot_id is not in slot_info
        for slot_id in list(self._mod_handles.keys()):
            if str(slot_id) not in slot_info:
                del self._mod_handles[slot_id]
                # Remove the module and add it again
                self.__add_modules(slot_id)

    # ------------------------------------------------------------------------
    def __add_modules(self, slot: Optional[int] = None) -> None:
        """
        Create and add modules.

        Parameters
        ----------
        slot : int, optional
            Specific slot number to add the module for. If None, adds modules for all slots.
        """
        if slot is not None:
            # Add the specific module for the provided slot
            del self.submodules[f"module{slot}"]
            module = Module(self, f"module{slot}", slot)
            self.add_submodule(f"module{slot}", module)
        else:
            self.submodules.clear()
            # Add modules for all slots
            for slot_idx in range(1, self._num_slots + 1):
                module = Module(self, f"module{slot_idx}", slot_idx)
                self.add_submodule(f"module{slot_idx}", module)

        # Add time-keeping functionality
        if "time" not in self.submodules:
            time = Time(self)
            self.add_submodule("time", time)

    # ------------------------------------------------------------------------
    @property
    def modules(self) -> list:
        """
        Get list of modules.

        Returns
        ----------
        list
            List of modules.
        """

        modules_list = [
            submodule for submodule in self.submodules.values() if "module" in str(submodule)
        ]
        return modules_list

    # ------------------------------------------------------------------------
    @property
    def times(self) -> list:
        """
        Get list of time blocks.

        Returns
        ----------
        list
            List of digital time modules. There is only one, but we still need
            to be able to iterate through it as if it was a list to not break
            pytest.
        """
        time_list = [
            submodule for submodule in self.submodules.values() if "time" in str(submodule)
        ]
        return time_list

    # -------------------------------------------------------------------------
    def get_connected_modules(
        self, filter_fn: Optional[Callable[[Module], bool]] = None
    ) -> dict[int, Module]:
        """
        Get the currently connected modules for each occupied slot in the Cluster.

        A selection of modules can be made by passing a filter function. For example:

        .. code-block:: python

            cluster.get_connected_modules(
                filter_fn = lambda mod: mod.is_qrm_type and not mod.is_rf_type
            )

        Parameters
        ----------
        filter_fn
            Optional filter function that must return True for the modules that should
            be included in the return value, and False otherwise.

        Returns
        -------
        dict
            Dictionary with key-value pairs consisting of slot numbers and corresponding
            :class:`~.Module` objects. Only contains entries for modules that are
            present and match the `filter_fn`.
        """

        def checked_filter_fn(mod) -> bool:
            if filter_fn is not None:
                return filter_fn(mod)
            return True

        return {
            mod.slot_idx: mod
            for mod in self.modules
            if mod.present() and mod.connected() and checked_filter_fn(mod)
        }

    # ------------------------------------------------------------------------
    def reset(self) -> None:
        """
        Resets device, invalidates QCoDeS parameter cache and clears all
        status and event registers (see
        `SCPI <https://www.ivifoundation.org/downloads/SCPI/scpi-99.pdf>`_).
        """

        self._reset()

        # Reinitialize modules
        self.__reinitialize_modules()

        # Invalidate the QCoDeS cache
        self._invalidate_qcodes_parameter_cache()

    # ------------------------------------------------------------------------
    def disconnect_outputs(self, slot: int) -> None:
        """
        Disconnects all outputs from the waveform generator paths of the
        sequencers.

        Parameters
        ----------
        slot: int
            Slot index
        """

        self._disconnect_outputs(slot)
        self._invalidate_qcodes_parameter_cache(slot)

    # ------------------------------------------------------------------------
    def disconnect_inputs(self, slot: int) -> None:
        """
        Disconnects all inputs from the acquisition paths of the sequencers.

        Parameters
        ----------
        slot: int
            Slot index
        """

        self._disconnect_inputs(slot)
        self._invalidate_qcodes_parameter_cache(slot)

    # ------------------------------------------------------------------------
    def connect_sequencer(self, slot: int, sequencer: int, *connections: str) -> None:
        """
        Makes new connections between the indexed sequencer and some inputs
        and/or outputs. This will fail if a requested connection already
        existed, or if the connection could not be made due to a conflict with
        an existing connection (hardware constraints). In such a case, the
        channel map will not be affected.

        Parameters
        ----------
        slot: int
            Slot index
        sequencer : int
            Sequencer index
        *connections : str
            Zero or more connections to make, each specified using a string.
            The string should have the format `<direction><channel>` or
            `<direction><I-channel>_<Q-channel>`. `<direction>` must be `in`
            to make a connection between an input and the acquisition path,
            `out` to make a connection from the waveform generator to an
            output, or `io` to do both. The channels must be integer channel
            indices. If only one channel is specified, the sequencer operates
            in real mode; if two channels are specified, it operates in complex
            mode.

        Raises
        ----------
        RuntimeError
            If the connection command could not be completed due to a conflict.
        ValueError
            If parsing of a connection fails.
        """

        self._sequencer_connect(slot, sequencer, *connections)
        self._invalidate_qcodes_parameter_cache(slot, sequencer)

    # ------------------------------------------------------------------------
    def _invalidate_qcodes_parameter_cache(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        """
        Marks the cache of all QCoDeS parameters in the module, including in
        any sequencers the module might have, as invalid. Optionally,
        a slot and a sequencer can be specified. This will invalidate the cache
        of that slot or sequencer in that specific slot only instead of all
        parameters.

        Parameters
        ----------
        slot : Optional[int]
            Slot index of slot for which to invalidate the QCoDeS
            parameters.
        sequencer : Optional[int]
            Sequencer index of sequencer for which to invalidate the QCoDeS
            parameters.
        """

        # Invalidate instrument parameters
        if slot is None:
            for param in self.parameters.values():
                param.cache.invalidate()
            module_list = self.modules
        else:
            module_list = [self.modules[slot - 1]]

        # Invalidate module parameters
        for module in module_list:
            module._invalidate_qcodes_parameter_cache(sequencer)

        # Invalidate time-keeping parameters
        for tim in self.times:
            tim._invalidate_qcodes_parameter_cache()

    # ------------------------------------------------------------------------
    def __getitem__(self, key: str) -> Union[InstrumentChannel, Parameter, Callable[..., Any]]:
        """
        Get module or parameter using string based lookup.

        Parameters
        ----------
        key : str
            Module, parameter or function to retrieve.

        Returns
        ----------
        Union[InstrumentChannel, Parameter, Callable[..., Any]]
            Module, parameter or function.

        Raises
        ----------
        KeyError
            Module, parameter or function does not exist.
        """

        return get_item(self, key)

    # ------------------------------------------------------------------------
    def __repr__(self) -> str:
        """
        Returns simplified representation of class giving just the class,
        name and connection.

        Returns
        ----------
        str
            String representation of class.
        """

        loc_str = ""
        if hasattr(self._transport, "_socket"):
            address, port = self._transport._socket.getpeername()
            loc_str = f" at {address}:{port}"
        return f"<{type(self).__name__}: {self.name}" + loc_str + ">"
