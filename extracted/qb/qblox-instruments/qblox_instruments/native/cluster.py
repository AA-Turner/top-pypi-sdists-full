# ----------------------------------------------------------------------------
# Description    : Cluster native interface
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------

import json
import re
import struct
import time

# -- include -----------------------------------------------------------------
import warnings
from collections.abc import Iterable, Iterator
from functools import partial
from typing import Any, Callable, Optional, Union

import numpy

from qblox_instruments.build import DeviceInfo
from qblox_instruments.ieee488_2 import (
    ClusterDummyTransport,
    DummyBinnedAcquisitionData,
    DummyScopeAcquisitionData,
    IpTransport,
)
from qblox_instruments.native.definitions import (
    SequencerStates,
    SequencerStatus,
    SequencerStatuses,
    SequencerStatusFlags,
    SystemStatus,
    SystemStatuses,
    SystemStatusFlags,
    SystemStatusSlotFlags,
)
from qblox_instruments.native.helpers import (
    ChannelMapCache,
    check_io_channel_index,
    check_is_valid_type,
    check_program_length,
    check_sequencer_index,
    create_read_bin,
    get_generic_json_config_val,
    parse_sequencer_status,
    set_generic_json_config_val,
    validate_acq,
    validate_qcm_sequence,
    validate_qrm_sequence,
    validate_qtm_sequence,
    validate_wave,
)
from qblox_instruments.pnp import resolve
from qblox_instruments.scpi import Cluster as ClusterScpi
from qblox_instruments.scpi import scpi_error_check
from qblox_instruments.types import DebugLevel, InstrumentClass, InstrumentType, TypeHandle

# -- class -------------------------------------------------------------------


class Cluster(ClusterScpi):
    """
    Class that provides the native API for the Cluster. It provides methods
    to control all functions and features provided by the Cluster.
    """

    # Binary read functions with preconfigured commands, used by `_get` methods.
    _awg_wlist_rb: Callable = create_read_bin(
        ClusterScpi._read_bin, "SLOT{}:SEQuencer{}:AWG:WLISt?"
    )
    _acq_wlist_rb: Callable = create_read_bin(
        ClusterScpi._read_bin, "SLOT{}:SEQuencer{}:ACQ:WLISt?"
    )
    _acq_data_rb: Callable = create_read_bin(
        ClusterScpi._read_bin, 'SLOT{}:SEQuencer{}:ACQ:ALISt:ACQuisition:DATA? "{}"'
    )
    _acq_list_rb: Callable = create_read_bin(ClusterScpi._read_bin, "SLOT{}:SEQuencer{}:ACQ:ALISt?")

    # ------------------------------------------------------------------------
    def __init__(
        self,
        identifier: str,
        port: Optional[int] = None,
        debug: Optional[DebugLevel] = None,
        dummy_cfg: Optional[dict] = None,
    ) -> None:
        """
        Creates Cluster native interface object.

        Parameters
        ----------
        identifier : str
            Instrument identifier. See :func:`~qblox_instruments.resolve()`
            for more information.
        port : Optional[int]
            Instrument port. If None, this will be determined automatically.
        debug : Optional[DebugLevel]
            Debug level. See :class:`~qblox_instruments.types.DebugLevel` for more
            information. By default None, which means that for a connection to a dummy
            cluster, `DebugLevel.ERROR_CHECK` will be used, and for a real cluster,
            `DebugLevel.MINIMAL_CHECK`.
        dummy_cfg : Optional[dict]
            Configure as dummy using this configuration. For each slot that
            needs to be occupied by a module add the slot index as key and
            specify the type of module in the slot using the type
            :class:`~qblox_instruments.ClusterType`.

        Raises
        ----------
        RuntimeError
            Instrument cannot be reached due to invalid IP configuration.
        ConnectionError
            Instrument type is not supported.
        """
        # Create transport layer (dummy or socket interface)
        self._dummy_config_present = False
        if dummy_cfg is not None:
            self._dummy_config_present = True
            self._transport = ClusterDummyTransport(dummy_cfg)
            if debug is None:
                debug = DebugLevel.ERROR_CHECK
        else:
            addr_info = resolve(identifier)
            if addr_info.protocol != "ip":
                raise RuntimeError(
                    f"Instrument cannot be reached due to invalid IP configuration. "
                    f"Use qblox-pnp tool to rectify; serial number is {addr_info.address}"
                )
            host = addr_info.address
            if port is None:
                port = addr_info.scpi_port
            self._transport = IpTransport(host=host, port=port)
            if debug is None:
                debug = DebugLevel.MINIMAL_CHECK

        self._debug = debug

        # Initialize parent class.
        super().__init__(self._transport, debug=debug)

        # Set instrument type handle
        self._cmm_dev_info = DeviceInfo.from_idn(super()._get_idn())
        model = self._cmm_dev_info.model
        self._type_handle = TypeHandle(model)
        if not self._type_handle.is_mm_type:
            raise ConnectionError(f"Unsupported instrument type detected ({self.instrument_type})")

        self._create_mod_handles()

    @property
    def is_dummy(self) -> bool:
        """
        Return True if the cluster is configured as dummy.

        Returns
        -------
        bool
            Whether this is a dummy cluster.
        """
        return self._dummy_config_present

    def _create_mod_handles(self, slot: Optional[int] = None) -> None:
        """
        Set up module-specific type and function reference handles for each
        module slot or a specific slot if provided. This method initializes and
        populates the `_mod_handles` dictionary with information about the modules.
        It retrieves module information, checks for firmware version mismatches,
        and sets up type handles and function references for the modules.

        Parameters
        ----------
        slot : Optional[int]
            The slot to update. If None, updates all slots.

        Raises
        ----------
        ConnectionError
            If there is a mismatch between the application version of the CMM
            and a module, and debug mode is not enabled. This requires a
            firmware update for the entire cluster.
        """
        # Set module specific type and FuncRefs handles
        if slot is None:
            # No specific slot provided, update all slots
            self._mod_handles = {}
            slot_info = self.get_json_description().get("modules", {})
        else:
            # Only update the specified slot
            self._mod_handles.pop(slot, None)
            slot_info = (
                {slot: self.get_json_description()["modules"][str(slot)]}
                if str(slot) in self.get_json_description().get("modules", {})
                else {}
            )

        for slot_str, info in slot_info.items():
            slot_id = int(slot_str)
            mod_dev_info = DeviceInfo.from_dict(info)

            # Module type handle
            model = mod_dev_info.model
            mod_type_handle = TypeHandle(model)
            if "is_rf" not in info:
                warnings.warn(
                    f"Module in slot {slot_id} has responded with incomplete information "
                    f"(missing `is_rf` field) due to an incompatible firmware version. "
                    f"Please proceed with caution."
                )
            mod_type_handle._is_rf_type = bool(info.get("is_rf", False))
            mod_type_handle._is_eom_type = bool(info.get("qtm_eom", False))

            # Update module handles dictionary
            self._mod_handles[slot_id] = {
                "serial": mod_dev_info.serial,
                "type_handle": mod_type_handle,
            }

    # ------------------------------------------------------------------------
    @property
    def instrument_class(self) -> InstrumentClass:
        """
        Get instrument class (e.g. Cluster).

        Returns
        ----------
        InstrumentClass
            Instrument class
        """
        return self._type_handle.instrument_class

    # ------------------------------------------------------------------------
    @property
    def instrument_type(self) -> InstrumentType:
        """
        Get instrument type (e.g. MM, QRM, QCM).

        Returns
        ----------
        InstrumentType
            Instrument type
        """
        return self._type_handle.instrument_type

    # ------------------------------------------------------------------------
    def _present_at_init(self, slot: int) -> TypeHandle:
        """
        Get an indication of module presence during initialization of this
        object for a specific slot in the Cluster and return the associated
        module type handle and function reference container if present.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        TypeHandle
            Module type handle

        Raises
        ----------
        KeyError
            Module is not available.
        """
        if slot in self._mod_handles:
            return self._mod_handles[slot]["type_handle"]
        else:
            raise KeyError(f"Module at slot {slot} is not available.")

    # ------------------------------------------------------------------------
    def _module_type(self, slot: int) -> InstrumentType:
        """
        Get indexed module's type (e.g. QRM, QCM, QTM, QDM, LINQ, QRC).

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        InstrumentType
            Module type
        """
        type_handle = self._present_at_init(slot)
        return type_handle.instrument_type

    # ------------------------------------------------------------------------
    def _is_qcm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QCM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            True if module is of type QCM.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_qcm_type

    # ------------------------------------------------------------------------
    def _is_qrm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QRM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QRM.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_qrm_type

    # ------------------------------------------------------------------------
    def _is_qtm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QTM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QTM.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_qtm_type

    # ------------------------------------------------------------------------
    def _is_qdm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QDM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QDM.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_qdm_type

    # ------------------------------------------------------------------------
    def _is_eom_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type EOM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type EOM.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_eom_type

    # ------------------------------------------------------------------------
    def _is_linq_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type LINQ

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type LINQ.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_linq_type

    # ------------------------------------------------------------------------
    def _is_qrc_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QRC.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QRC.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_qrc_type

    # ------------------------------------------------------------------------
    def _is_qsm_type(self, slot: int) -> bool:
        """
        Return if indexed module is of type QSM.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module is of type QSM.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_qsm_type

    # ------------------------------------------------------------------------
    def _is_rf_type(self, slot: int) -> bool:
        """
        Return if indexed module has RF functionality.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool:
            True if module has RF functionality.
        """
        type_handle = self._present_at_init(slot)
        return type_handle.is_rf_type

    # ------------------------------------------------------------------------
    def _get_scpi_commands(self) -> dict:
        """
        Get SCPI commands and convert to dictionary.

        Returns
        ----------
        dict
            Dictionary containing all available SCPI commands, corresponding
            parameters, arguments and Python methods and finally a descriptive
            comment.
        """

        # Split function
        def split(cmd_elem: str) -> list:
            if cmd_elem not in ("None", ""):
                return cmd_elem.split(",")
            else:
                return []

        # Format command string
        cmds = super()._get_scpi_commands()
        cmd_elem_list = cmds.split(";")[:-1]
        cmd_list = numpy.reshape(cmd_elem_list, (int(len(cmd_elem_list) / 9), 9))
        cmd_dict = {
            cmd[0]: {
                "scpi_in_type": split(cmd[1]),
                "scpi_out_type": split(cmd[2]),
                "python_func": cmd[3],
                "python_in_type": split(cmd[4]),
                "python_in_var": split(cmd[5]),
                "python_out_type": split(cmd[6]),
                "comment": cmd[8].replace("\t", "\n"),
            }
            for cmd in cmd_list
        }
        return cmd_dict

    # ------------------------------------------------------------------------
    def get_idn(self) -> dict:
        """
        Get device identity and build information and convert them to a
        dictionary.

        Returns
        ----------
        dict
            Dictionary containing manufacturer, model, serial number and build
            information. The build information is subdivided into FPGA firmware,
            kernel module software, application software and driver software build
            information. Each of those consist of the version, build date,
            build Git hash and Git build dirty indication.
        """
        return DeviceInfo.from_idn(super()._get_idn()).to_idn_dict()

    # ------------------------------------------------------------------------
    def get_system_status(self) -> SystemStatus:
        """
        Get general system status and convert it to a
        :class:`~qblox_instruments.native.definitions.SystemStatus`.

        Returns
        ----------
        SystemStatus
            Tuple containing general system status and corresponding flags.
        """
        # Format status string
        state = super()._get_system_state()
        state_elem_list = re.sub(" |-", "_", state).split(";")
        if state_elem_list[-1] != "":
            state_flag_list = state_elem_list[-1].split(",")[:-1]
        else:
            state_flag_list = []

        # Split system status flags from slot status flags
        system_flags = []
        slot_flags = {}
        for flag in state_flag_list:
            flag_parts = flag.split("_")
            if flag_parts[0] != "SLOT":
                system_flags.append(SystemStatusFlags[flag])
            else:
                slot = "slot" + flag_parts[1]
                flag_ = SystemStatusFlags["_".join(flag_parts[2:])]
                if slot not in slot_flags:
                    slot_flags[slot] = [flag_]
                else:
                    slot_flags[slot].append(flag_)

        return SystemStatus(
            SystemStatuses[state_elem_list[0]],
            system_flags,
            SystemStatusSlotFlags(slot_flags),
        )

    # ----------------------------------------------------------------------------
    def _set_acq_scope_config(self, slot: int, config: dict) -> None:
        """
        Set configuration of the scope acquisition. The configuration consists of
        multiple parameters in a C struct format. If an invalid sequencer index
        is given or the configuration struct does not have the correct format, an
        error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        config : dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        super()._set_acq_scope_config(slot, config)

    # ----------------------------------------------------------------------------
    def _get_acq_scope_config(self, slot: int) -> dict:
        """
        Get configuration of the scope acquisition. The configuration consists of
        multiple parameters in a C struct format. If an invalid sequencer index is
        given, an error is set in system error.

        Returns
        ----------
        slot : int
            The slot index of the module being referred to.
        dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))
        return super()._get_acq_scope_config(slot)

    # ------------------------------------------------------------------------
    def _set_acq_scope_config_val(self, slot: int, keys: Any, val: Any) -> None:
        """
        Set value of specific scope acquisition parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof
        val: Any
            Value to set parameter to.
        """
        self._present_at_init(slot)

        set_generic_json_config_val(
            lambda: self._get_acq_scope_config(slot),
            lambda cfg: self._set_acq_scope_config(slot, cfg),
            keys,
            val,
        )

    # ------------------------------------------------------------------------
    def _get_acq_scope_config_val(self, slot: int, keys: Any) -> Any:
        """
        Get value of specific scope acquisition parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        self._present_at_init(slot)

        return get_generic_json_config_val(
            lambda: self._get_acq_scope_config(slot),
            keys,
        )

    # ------------------------------------------------------------------------
    def _set_io_channel_config(self, slot: int, channel: int, config: dict) -> None:
        """
        Set IO channel configuration. The configuration consists of
        multiple parameters in a JSON format. If the configuration struct does not
        have the correct format, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.
        config : dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        super()._set_io_channel_config(slot, channel, config)

    # ------------------------------------------------------------------------
    def _set_output_normalized_amplitude(self, slot: int, channel: int, amplitude: float) -> None:
        """
        Set IO Pulse output amplitude.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            Channel index.
        amplitude : float
            Normalized amplitude.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot) and self._is_eom_type(slot))
        super()._set_output_normalized_amplitude(slot, channel, amplitude)

    # ------------------------------------------------------------------------
    def _get_output_normalized_amplitude(self, slot: int, channel: int) -> float:
        """
        Get IO Pulse output amplitude.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            Channel index.

        Returns
        ----------
        amplitude : float
            Normalized output amplitude

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot) and self._is_eom_type(slot))
        return super()._get_output_normalized_amplitude(slot, channel)

    # ------------------------------------------------------------------------
    def _set_io_pulse_output_offset(self, slot: int, channel: int, offset: float) -> None:
        """
        Set IO Pulse channel output offset.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            Channel index.
        offset : float
            I/O channel index.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot) and self._is_eom_type(slot))
        super()._set_io_pulse_output_offset(slot, channel, offset)

    # ------------------------------------------------------------------------
    def _get_io_pulse_output_offset(self, slot: int, channel: int) -> float:
        """
        Get IO Pulse channel output offset.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            Channel index.

        Returns
        ----------
        offset : float
            output offset

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot) and self._is_eom_type(slot))
        return super()._get_io_pulse_output_offset(slot, channel)

    # ------------------------------------------------------------------------
    def _set_io_pulse_width_config(self, slot: int, channel: int, config: dict) -> None:
        """
        Set IO Pulse width. Config must be a dict containing coarse and fine settings.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O quad index.
        config : dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot) and self._is_eom_type(slot))
        super()._set_io_pulse_width(slot, channel, config)

    # ------------------------------------------------------------------------
    def _get_io_pulse_width_config(self, slot: int, channel: int) -> Any:
        """
        Get IO Pulse width. Config must be a dict containing coarse and fine settings.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.

        Returns
        ----------
        dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot) and self._is_eom_type(slot))
        return super()._get_io_pulse_width(slot, channel)

    # --------------------------------------------------------------------------
    def set_io_pulse_width_config_val(self, slot: int, channel: int, keys: Any, val: Any) -> None:
        """
        Set value of specific IO channel configuration parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.
        keys : Union[List[str], str]
            Configuration key to access, or hierarchical list thereof.
        val: Any
            Value to set parameter to.
        """
        set_generic_json_config_val(
            lambda: self._get_io_pulse_width_config(slot, channel),
            lambda cfg: self._set_io_pulse_width_config(slot, channel, cfg),
            keys,
            val,
        )

    # --------------------------------------------------------------------------
    def get_io_pulse_width_config_val(self, slot: int, channel: int, keys: Any) -> Any:
        """
        Get value of specific IO channel configuration parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.
        keys : Union[List[str], str]
            Configuration key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        return get_generic_json_config_val(lambda: self._get_io_channel_config(slot, channel), keys)

    # ------------------------------------------------------------------------
    def _get_io_channel_config(self, slot: int, channel: int) -> dict:
        """
        Get IO channel configuration. The configuration consists of
        multiple parameters in a JSON format.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.

        Returns
        ----------
        dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        return super()._get_io_channel_config(slot, channel)

    # ------------------------------------------------------------------------
    def _get_io_channel_status(self, slot: int, channel: int) -> dict:
        """
        Get IO channel status. The status consists of multiple values in a JSON
        format.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.

        Returns
        ----------
        dict
            Status dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        return super()._get_io_channel_status(slot, channel)

    # ------------------------------------------------------------------------
    def _set_io_channel_config_val(self, slot: int, channel: int, keys: Any, val: Any) -> None:
        """
        Set value of specific IO channel configuration parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof.
        channel : int
            I/O channel index.
        val: Any
            Value to set parameter to.
        """
        self._present_at_init(slot)

        set_generic_json_config_val(
            lambda: self._get_io_channel_config(slot, channel),
            lambda cfg: self._set_io_channel_config(slot, channel, cfg),
            keys,
            val,
        )

    # ------------------------------------------------------------------------
    def _get_io_channel_config_val(self, slot: int, channel: int, keys: Any) -> Any:
        """
        Get value of specific IO channel configuration parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        self._present_at_init(slot)

        return get_generic_json_config_val(
            lambda: self._get_io_channel_config(slot, channel),
            keys,
        )

    # ------------------------------------------------------------------------
    def _get_io_channel_status_val(self, slot: int, channel: int, keys: Any) -> Any:
        """
        Get value of specific IO channel status parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        channel : int
            I/O channel index.
        keys : Union[list[str], str]
            Status key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        self._present_at_init(slot)

        return get_generic_json_config_val(
            lambda: self._get_io_channel_status(slot, channel),
            keys,
        )

    # ----------------------------------------------------------------------------
    def _set_quad_config(self, slot: int, quad: int, config: dict) -> None:
        """
        Set quad configuration. The configuration consists of
        multiple parameters in a JSON format. If the configuration struct does not
        have the correct format, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        quad : int
            I/O quad index.
        config : dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        super()._set_quad_config(slot, quad, config)

    # ----------------------------------------------------------------------------
    def _get_quad_config(self, slot: int, quad: int) -> Any:
        """
        Get quad configuration. The configuration consists of
        multiple parameters in a JSON format.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        quad : int
            I/O quad index.

        Returns
        ----------
        dict
            Configuration dictionary.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        return super()._get_quad_config(slot, quad)

    # ------------------------------------------------------------------------
    def _set_quad_config_val(self, slot: int, quad: int, keys: Any, val: Any) -> None:
        """
        Set value of specific quad configuration parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        quad : int
            I/O quad index.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof
        val: Any
            Value to set parameter to.
        """
        self._present_at_init(slot)

        set_generic_json_config_val(
            lambda: self._get_quad_config(slot, quad),
            lambda cfg: self._set_quad_config(slot, quad, cfg),
            keys,
            val,
        )

    # ------------------------------------------------------------------------
    def _get_quad_config_val(self, slot: int, quad: int, keys: Any) -> Any:
        """
        Get value of specific quad configuration parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        quad : int
            I/O quad index.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        self._present_at_init(slot)

        return get_generic_json_config_val(
            lambda: self._get_quad_config(slot, quad),
            keys,
        )

    # ----------------------------------------------------------------------------
    def _set_sequencer_program(self, slot: int, sequencer: int, program: str) -> None:
        """
        Assemble and set Q1ASM program for the indexed sequencer. If assembling
        fails, an RuntimeError is thrown with the assembler log attached.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        program : str
            Q1ASM program.

        Raises
        ----------
        RuntimeError
            Assembly failed.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)

        try:
            super()._set_sequencer_program(slot, sequencer, check_program_length(program))
        except:
            print(self.get_assembler_log(slot))
            raise

    # ----------------------------------------------------------------------------
    def _set_sequencer_config(self, slot: int, sequencer: int, config: dict) -> None:
        """
        Set configuration of the indexed sequencer. The configuration consists
        dictionary containing multiple parameters that will be converted into a
        JSON object supported by the device.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        config : dict
            Configuration dictionary.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        super()._set_sequencer_config(slot, sequencer, config)

    # ----------------------------------------------------------------------------
    def _get_sequencer_config(self, slot: int, sequencer: int) -> dict:
        """
        Get configuration of the indexed sequencer. The configuration consists
        dictionary containing multiple parameters that will be converted from a
        JSON object provided by the device.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Configuration dictionary.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        return super()._get_sequencer_config(slot, sequencer)

    # ------------------------------------------------------------------------
    def _set_sequencer_config_val(self, slot: int, sequencer: int, keys: Any, val: Any) -> None:
        """
        Set value of specific sequencer parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof
        val : Any
            Value to set parameter to.
        """
        self._present_at_init(slot)

        try:
            set_generic_json_config_val(
                lambda: self._get_sequencer_config(slot, sequencer),
                lambda cfg: self._set_sequencer_config(slot, sequencer, cfg),
                keys,
                val,
                is_sequencer=True,
            )
        except TypeError as e:
            typ = e.args[1]
            raise TypeError(
                f"{'.'.join(str(k) for k in keys)} should be of type {typ.__name__}: {e.__cause__}"
            )
        except KeyError:
            raise KeyError(f"{'.'.join(str(k) for k in keys)} is an incomplete sequencer path")

    # ------------------------------------------------------------------------
    def _get_sequencer_config_val(self, slot: int, sequencer: int, keys: Any) -> Any:
        """
        Get value of specific sequencer parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        self._present_at_init(slot)

        try:
            return get_generic_json_config_val(
                lambda: self._get_sequencer_config(slot, sequencer),
                keys,
                is_sequencer=True,
            )
        except KeyError as e:
            key = e.args[1]
            raise KeyError(
                f"cfg_dict[{']['.join(str(e) for e in keys)}] is not a valid sequencer path, "
                f"failed at {key}"
            )

    # ------------------------------------------------------------------------
    def _set_sequencer_config_rotation_matrix(
        self, slot: int, sequencer: int, phase_incr: float
    ) -> None:
        """
        Sets the integration result phase rotation matrix in the acquisition path.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        phase_incr : float
            Phase increment in degrees.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))

        cfg_dict = self._get_sequencer_config(slot, sequencer)

        cfg_dict["acq"][0]["th_acq"]["rotation_matrix_a11"] = numpy.cos(
            numpy.deg2rad(360 - phase_incr)
        )
        cfg_dict["acq"][0]["th_acq"]["rotation_matrix_a12"] = numpy.sin(
            numpy.deg2rad(360 - phase_incr)
        )

        self._set_sequencer_config(slot, sequencer, cfg_dict)

    # ------------------------------------------------------------------------
    def _get_sequencer_config_rotation_matrix(self, slot: int, sequencer: int) -> float:
        """
        Gets the integration result phase rotation matrix in the acquisition path.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        float
            Phase increment in degrees.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))
        cfg = self._get_sequencer_config(slot, sequencer)
        vector = (
            cfg["acq"][0]["th_acq"]["rotation_matrix_a11"]
            + cfg["acq"][0]["th_acq"]["rotation_matrix_a12"] * 1j
        )
        phase_incr = numpy.angle(vector, deg=True)
        if phase_incr == 0:
            return 0
        elif phase_incr >= 0:
            return 360 - phase_incr
        else:
            return -1.0 * phase_incr

    # ------------------------------------------------------------------------
    def _set_sequencer_connect_out(
        self, slot: int, sequencer: int, output: int, state: str
    ) -> None:
        """
        Set whether the output of the indexed sequencer is connected to the given
        output and if so with which path.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        output : int
            Zero-based output index.
        state : str | bool
            - For baseband modules, one of:
                - "off": the output is not connected.
                - "I": the output is connected to path0/I.
                - "Q": the output is connected to path1/Q.
            - For RF modules, one of:
                - "off" or False: the RF output is not connected.
                - "IQ" or True: the RF output is connected.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)

        with ChannelMapCache(self, slot) as channel_map:
            # Note that for RF modules, each connect_out parameter controls the
            # configuration for two DACs, hardwired to the I and Q input of the
            # RF mixer on the front end. It doesn't make sense to control the
            # DACs individually in this case.
            if self._is_rf_type(slot):
                if state is False or state == "off":
                    channel_map.disconnect(ChannelMapCache.AWG, sequencer, 0, output * 2)
                    channel_map.disconnect(ChannelMapCache.AWG, sequencer, 0, output * 2 + 1)
                    channel_map.disconnect(ChannelMapCache.AWG, sequencer, 1, output * 2)
                    channel_map.disconnect(ChannelMapCache.AWG, sequencer, 1, output * 2 + 1)
                elif state is True or state == "IQ":
                    channel_map.connect(ChannelMapCache.AWG, sequencer, 0, output * 2)
                    channel_map.connect(ChannelMapCache.AWG, sequencer, 1, output * 2 + 1)
                else:
                    raise ValueError(f"invalid new connection state {state!r} for RF device")
            elif state == "off":
                channel_map.disconnect(ChannelMapCache.AWG, sequencer, 0, output)
                channel_map.disconnect(ChannelMapCache.AWG, sequencer, 1, output)
            elif state == "I":
                channel_map.connect(ChannelMapCache.AWG, sequencer, 0, output)
                channel_map.disconnect(ChannelMapCache.AWG, sequencer, 1, output)
            elif state == "Q":
                channel_map.disconnect(ChannelMapCache.AWG, sequencer, 0, output)
                channel_map.connect(ChannelMapCache.AWG, sequencer, 1, output)
            else:
                raise ValueError(f"invalid new connection state {state!r} for baseband device")

    # -------------------------------------------------------------------------
    def _get_sequencer_connect_out(self, slot: int, sequencer: int, output: int) -> str:
        """
        Returns whether the output of the indexed sequencer is connected to the
        given output and if so with which path.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        output : int
            Zero-based output index.

        Returns
        ----------
        str
            - For baseband modules, one of:
                - "off": the output is not connected.
                - "I": the output is connected to path0/I.
                - "Q": the output is connected to path1/Q.
            - For RF modules, one of:
                - "off": the RF output is not connected.
                - "IQ": the RF output is connected.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)

        with ChannelMapCache(self, slot) as channel_map:
            # Note that for RF modules, each connect_out parameter controls the
            # configuration for two DACs, hardwired to the I and Q input of the
            # RF mixer on the front end. It doesn't make sense to control the
            # DACs individually in this case, and as such the user isn't given
            # that level of control, but nevertheless the channel map state
            # could hypothetically be in some weird in-between state. However,
            # since we have to return something either way, just checking one
            # of the paths should be good enough.
            if self._is_rf_type(slot):
                if channel_map.is_connected(ChannelMapCache.AWG, sequencer, 0, output * 2):
                    return "IQ"
            elif channel_map.is_connected(ChannelMapCache.AWG, sequencer, 0, output):
                return "I"
            elif channel_map.is_connected(ChannelMapCache.AWG, sequencer, 1, output):
                return "Q"
        return "off"

    # ------------------------------------------------------------------------
    def _set_sequencer_connect_acq(self, slot: int, sequencer: int, path: int, state: str) -> None:
        """
        Set whether the input of the indexed sequencer's acquisition path is
        connected to an external input and if so which.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        path : int
            Path index: 0 for baseband path0/I, 1 for baseband path1/Q, ignored for RF.
        state : str | bool
            - One of:
                - "off" or False: connection disabled.
                - "in#": the acquisition input path is connected to external input #,
                  where # is a zero-based input index.
                - True: if there is only one option other than off, True is allowed as alias.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))

        # Desugar state input.
        if state is False:
            input_ = None
        elif state is True and self._is_rf_type(slot):
            input_ = 0  # only 1 input
        elif state == "off":
            input_ = None
        elif m := re.fullmatch(r"in(0|[1-9][0-9]*)", state):
            input_ = int(m.group(1))
        else:
            raise ValueError(f"invalid new connection state {state!r}")

        with ChannelMapCache(self, slot) as channel_map:
            # Note that for RF modules, each connect_acq parameter controls the
            # configuration for both paths of the acquisition engine, because
            # each input maps to two ADCs.
            if self._is_rf_type(slot):
                channel_map.clear(ChannelMapCache.ACQ, sequencer)
                if input_ is not None:
                    channel_map.connect(ChannelMapCache.ACQ, sequencer, 0, input_ * 2)
                    channel_map.connect(ChannelMapCache.ACQ, sequencer, 1, input_ * 2 + 1)
            else:
                channel_map.clear_path(ChannelMapCache.ACQ, sequencer, path)
                if input_ is not None:
                    channel_map.connect(ChannelMapCache.ACQ, sequencer, path, input_)

    # -------------------------------------------------------------------------
    def _get_sequencer_connect_acq(self, slot: int, sequencer: int, path: int) -> str:
        """
        Get whether the input of the indexed sequencer's acquisition path is
        connected to an external input and if so which.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        path : int
            Path index: 0 for baseband path0/I, 1 for baseband path1/Q, ignored for RF.

        Returns
        ----------
        str
            - One of:
                - "off": connection disabled.
                - "in#": the acquisition input path is connected to external input #,
                  where # is a zero-based input index.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))

        with ChannelMapCache(self, slot) as channel_map:
            channels = list(
                channel_map.get_connected_channels(ChannelMapCache.ACQ, sequencer, path)
            )

        if not channels:
            return "off"

        # If multiple inputs are connected to the same acquisition path in the
        # channel map (an illegal configuration), do the same thing the firmware
        # does, which is prioritizing lower-indexed channels because there is no
        # good error path here.
        channel = min(channels)

        # Divide by two for RF modules to map from ADC channel to input, as there
        # are two ADCs per input (I and Q). For baseband modules the mapping is
        # one to one.
        if self._is_rf_type(slot):
            channel //= 2

        return f"in{channel}"

    # ----------------------------------------------------------------------------
    def _get_output_latency(self, slot: int, output: int) -> float:
        """
        Get the latency in output path. The output path can change depending on "
        "the filter configuration of the output."

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        output: int
            The output for which the latency should be returned.

        Returns
        ----------
        latency: float
            Latency of the output path.
        """
        self._present_at_init(slot)

        return super()._get_output_latency(slot, output)

    # ----------------------------------------------------------------------------
    def _set_pre_distortion_config(self, slot: int, config: dict) -> None:
        """
        Set pre distortion configuration. The configuration consists
        dictionary containing multiple parameters that will be converted into a
        JSON object.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        config : dict
            Configuration dictionary.
        """
        self._present_at_init(slot)

        super()._set_pre_distortion_config(slot, config)

    # ----------------------------------------------------------------------------
    def _get_pre_distortion_config(self, slot: int) -> dict:
        """
        Get pre-distortion configuration. The configuration consists
        dictionary containing multiple parameters that will be converted from a
        JSON object.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.

        Returns
        ----------
        dict
            Configuration dictionary.
        """
        self._present_at_init(slot)

        return super()._get_pre_distortion_config(slot)

    # ------------------------------------------------------------------------
    def _set_pre_distortion_config_val(self, slot: int, keys: Any, val: Any) -> None:
        """
        Set value of specific pre-distortion filtering parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof
        val : Any
            Value to set parameter to.
        """
        self._present_at_init(slot)

        set_generic_json_config_val(
            lambda: self._get_pre_distortion_config(slot),
            lambda cfg: self._set_pre_distortion_config(slot, cfg),
            keys,
            val,
        )

    # ------------------------------------------------------------------------
    def _get_pre_distortion_config_val(self, slot: int, keys: Any) -> Any:
        """
        Get value of specific pre-distortion filtering parameter.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        keys : Union[list[str], str]
            Configuration key to access, or hierarchical list thereof

        Returns
        ----------
        Any
            Parameter value.
        """
        self._present_at_init(slot)

        return get_generic_json_config_val(
            lambda: self._get_pre_distortion_config(slot),
            keys,
        )

    # -------------------------------------------------------------------------
    def _disconnect_outputs(self, slot: int) -> None:
        """
        Disconnects all outputs from the sequencers.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        """
        self._present_at_init(slot)

        with ChannelMapCache(self, slot) as channel_map:
            channel_map.clear(ChannelMapCache.AWG)

    # -------------------------------------------------------------------------
    def _disconnect_inputs(self, slot: int) -> None:
        """
        Disconnects all inputs from the sequencers.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        """
        self._present_at_init(slot)

        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        with ChannelMapCache(self, slot) as channel_map:
            channel_map.clear(ChannelMapCache.ACQ)

    # -------------------------------------------------------------------------
    def _iter_connections(self, slot: int) -> Iterator[tuple[int, str, str]]:
        """
        Iterates over all enabled connections between ADCs, DACs, and
        sequencers.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.

        Returns
        ----------
        Iterator[tuple[int, str, str]]
            An iterator of connections. The four components of each connection are:

                - the index of the sequencer for the connection;
                - the connection point of the sequencer being connected to,
                  being one of `I`, `Q`, `acq_I`, or `acq_Q`;
                - the external connection, being either `adc#` or `dac#`,
                  where `#` is the zero-based ADC or DAC index.

            Note that these are ADC and DAC indices. For baseband modules,
            these indices map one-to-one to the external SMA ports, but for RF
            modules they don't: each pair of DACs or ADCs maps to a single RF
            port, the I component being generated by ADC/DAC index 0/2/... and
            the Q component being generated by ADC/DAC index 1/3/...
        """
        self._present_at_init(slot)

        return ChannelMapCache(self, slot).iter_connections()

    # -------------------------------------------------------------------------
    def _sequencer_connect(self, slot: int, sequencer: int, *connections: str) -> None:
        """
        Makes new connections between the indexed sequencer and some inputs and/or
        outputs. This will fail if a requested connection already existed, or if
        the connection could not be made due to a conflict with an existing
        connection (hardware constraints). In such a case, the channel map will
        not be affected.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        *connections : str
            Zero or more connections to make, each specified using a string. The
            string should have the format `<direction><channel>` or
            `<direction><I-channel>_<Q-channel>`. `<direction>` must be `in` to
            make a connection between an input and the acquisition path, `out` to
            make a connection from the waveform generator to an output, or `io` to
            do both. The channels must be integer channel indices. If only one
            channel is specified, the sequencer operates in real mode; if two
            channels are specified, it operates in complex mode.

        Raises
        ----------
        RuntimeError
            If the connection command could not be completed due to a conflict.
        ValueError
            If parsing of a connection fails.
        """
        self._present_at_init(slot)

        # Intentionally don't use the context manager: in case of an exception,
        # do not make *any* changes.
        channel_map = ChannelMapCache(self, slot)
        is_rf = self._is_rf_type(slot)

        for index, connection in enumerate(connections):
            try:
                # Parse syntax.
                m = re.fullmatch(r"(in|out|io)(0|[1-9][0-9]*)(?:_(0|[1-9][0-9]*))?", connection)
                if not m:
                    raise ValueError("syntax error")

                # Decode direction.
                directions = []
                if m.group(1) != "in":
                    directions.append(ChannelMapCache.AWG)
                if m.group(1) != "out":
                    directions.append(ChannelMapCache.ACQ)

                # Decode channel indices.
                i_channel = int(m.group(2))
                q_channel = m.group(3)
                if q_channel is not None:
                    q_channel = int(q_channel)

                # Catch some expected mistakes gracefully.
                if i_channel == q_channel:
                    suggestion = m.group(1) + m.group(2)
                    raise ValueError(
                        "cannot connect I and Q path to the same I/O port "
                        f"(did you mean {suggestion!r}?)"
                    )
                if is_rf and q_channel is not None:
                    message = "for RF connections, only one I/O port should be specified"
                    if i_channel % 2 == 0 and q_channel == i_channel + 1:
                        # they're probably thinking in terms of DAC/ADC indices
                        suggestion = f"{m.group(1)}{i_channel // 2}"
                        message += (
                            f" (you may be confused with DAC/ADC indices, "
                            f"did you mean {suggestion!r}?)"
                        )
                    raise ValueError(message)

                # Convert from I/O indices to DAC/ADC indices on RF devices.
                if is_rf:
                    q_channel = i_channel * 2 + 1
                    i_channel = i_channel * 2

                # Try to apply the changes.
                for direction in directions:
                    channel_map.connect(direction, sequencer, 0, i_channel, False)
                    if q_channel is not None:
                        channel_map.connect(direction, sequencer, 1, q_channel, False)

            except RuntimeError as e:  # noqa: PERF203
                raise RuntimeError(f"connection command {connection!r} (index {index}): {e}")
            except ValueError as e:
                raise ValueError(f"connection command {connection!r} (index {index}): {e}")

        # Everything seems to have worked: write new configuration to the
        # instrument.
        channel_map.flush()

    # ------------------------------------------------------------------------
    def arm_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        """
        Prepare the indexed sequencer to start by putting it in the armed state.
        If no sequencer index is given, all sequencers are armed. Any sequencer
        that was already running is stopped and rearmed. If an invalid sequencer
        index is given, an error is set in system error.

        Parameters
        ----------
        slot : Optional[int]
            The slot index of the module being referred to.
        sequencer : Optional[int]
            Sequencer index.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Arm sequencers across all modules

        if sequencer is not None:
            check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Arm all sequencers within a module

        scpi_cmd_prefix = f"SLOT{slot}:SEQuencer{sequencer}"

        # The SCPI command prefix is set by the native instrument layer so that
        # it can select to arm a specific sequencer (e.g. "SLOT1:SEQuencer0") or
        # all sequencers (e.g. "SLOT:SEQuencer")
        # The actual SCPI call is wrapped in a function to make use of the
        # scpi_error_check method.
        @scpi_error_check
        def arm_sequencer_func(instrument: Any) -> None:
            instrument._write(f"{scpi_cmd_prefix}:ARM")

        arm_sequencer_func(self)

    # ------------------------------------------------------------------------
    def start_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        """
        Start the indexed sequencer, thereby putting it in the running state.
        If an invalid sequencer index is given or the indexed sequencer was not
        yet armed, an error is set in system error. If no sequencer index is
        given, all armed sequencers are started and any sequencer not in the armed
        state is ignored. However, if no sequencer index is given and no
        sequencers are armed, and error is set in system error.

        Parameters
        ----------
        slot : Optional[int]
            The slot index of the module being referred to.
        sequencer : Optional[int]
            Sequencer index.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Start sequencers across all modules

        if sequencer is not None:
            check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Start all sequencers within a module

        scpi_cmd_prefix = f"SLOT{slot}:SEQuencer{sequencer}"

        # The SCPI command prefix is set by the native instrument layer so that
        # it can select to start a specific sequencer (e.g. "SLOT1:SEQuencer0") or
        # all sequencers (e.g. "SLOT:SEQuencer")
        # The actual SCPI call is wrapped in a function to make use of the
        # scpi_error_check method.
        @scpi_error_check(minimal_check=True)
        def start_sequencer_func(instrument: Any) -> None:
            instrument._write(f"{scpi_cmd_prefix}:START")

        start_sequencer_func(self)

    # ------------------------------------------------------------------------
    def stop_sequencer(self, slot: Optional[int] = None, sequencer: Optional[int] = None) -> None:
        """
        Stop the indexed sequencer, thereby putting it in the stopped state. If
        an invalid sequencer index is given, an error is set in system error. If
        no sequencer index is given, all sequencers are stopped.

        Parameters
        ----------
        slot : Optional[int]
            The slot index of the module being referred to.
        sequencer : Optional[int]
            Sequencer index.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Stop sequencers across all modules

        if sequencer is not None:
            check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Stop all sequencers within a module

        scpi_cmd_prefix = f"SLOT{slot}:SEQuencer{sequencer}"

        # The SCPI command prefix is set by the native instrument layer so that
        # it can select to stop a specific sequencer (e.g. "SLOT1:SEQuencer0") or
        # all sequencers (e.g. "SLOT:SEQuencer")
        # The actual SCPI call is wrapped in a function to make use of the
        # scpi_error_check method.
        @scpi_error_check(minimal_check=True)
        def stop_sequencer_func(instrument: Any) -> None:
            instrument._write(f"{scpi_cmd_prefix}:STOP")

        stop_sequencer_func(self)

    # ------------------------------------------------------------------------
    def clear_sequencer_flags(
        self, slot: Optional[int] = None, sequencer: Optional[int] = None
    ) -> None:
        """
        Clear flags.

        Parameters
        ----------
        slot : Optional[int]
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        """
        if slot is not None:
            self._present_at_init(slot)
        else:
            slot = ""  # Clear sequencer flags across all modules

        if sequencer is not None:
            check_sequencer_index(sequencer)
        else:
            sequencer = ""  # Clear all sequencers flags within a module

        scpi_cmd_prefix = f"SLOT{slot}:SEQuencer{sequencer}"

        # The SCPI command prefix is set by the native instrument layer so that
        # it can select to clear a specific sequencer flag (e.g. "SLOT1:SEQuencer0") or
        # all sequencers (e.g. "SLOT:SEQuencer")
        # The actual SCPI call is wrapped in a function to make use of the
        # scpi_error_check method.
        @scpi_error_check
        def clear_sequencer_flags_func(instrument: Any) -> None:
            instrument._write(f"{scpi_cmd_prefix}:CLR:FLAGS")

        clear_sequencer_flags_func(self)

    # ------------------------------------------------------------------------
    def get_sequencer_status(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
    ) -> SequencerStatus:
        """
        Get the sequencer status. If an invalid sequencer index is given, an error
        is set in system error. If the timeout is set to zero, the function
        returns the state immediately. If a positive non-zero timeout is set, the
        function blocks until the sequencer completes. If the sequencer hasn't
        stopped before the timeout expires, a TimeoutError is thrown.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        timeout : int
            Timeout in minutes.
        timeout_poll_res : float
            Timeout polling resolution in seconds.

        Returns
        ----------
        SequencerStatus
            Tuple containing sequencer status and corresponding flags.

        Raises
        ----------
        TimeoutError
            Timeout
        """
        self._present_at_init(slot)

        # Format status string
        check_sequencer_index(sequencer)
        full_status = self._get_sequencer_state(slot, sequencer)

        status, state, info_flags, warn_flags, err_flags, log = parse_sequencer_status(full_status)

        state_tuple = SequencerStatus(
            SequencerStatuses[status],
            SequencerStates[state],
            [SequencerStatusFlags[flag] for flag in info_flags],
            [SequencerStatusFlags[flag] for flag in warn_flags],
            [SequencerStatusFlags[flag] for flag in err_flags],
            log,
        )

        elapsed_time = 0.0
        start_time = time.time()
        timeout = timeout * 60.0
        while (
            state_tuple.state in (SequencerStates.RUNNING, SequencerStates.Q1_STOPPED)
            and elapsed_time < timeout
        ):
            time.sleep(timeout_poll_res)

            state_tuple = self.get_sequencer_status(slot, sequencer)
            elapsed_time = time.time() - start_time

            if elapsed_time >= timeout:
                raise TimeoutError(
                    f"Sequencer {sequencer} did not stop in timeout period "
                    f"of {int(timeout / 60)} minutes."
                )

        return state_tuple

    # ------------------------------------------------------------------------
    def arm_scope_trigger(self, slot: Optional[int] = None) -> None:
        """
        Prepare the scope trigger to start by putting it in the armed state.
        If it was already running, it is stopped and rearmed.

        Parameters
        ----------
        slot : Optional[int]
            The slot index of the module being referred to.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        if slot is not None:
            self._present_at_init(slot)
        else:
            # Arm scope triggers across all modules
            pass

        check_is_valid_type(self._is_qtm_type(slot))
        # self._arm_scope_trigger()  # NOTE: function doesn't exist.

    # ----------------------------------------------------------------------------
    def _get_acq_acquisitions(self, slot: int, sequencer: int) -> dict:
        """
        Get all acquisitions in acquisition list of indexed sequencer's
        acquisition path. If an invalid sequencer index is given, an error is set
        in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with acquisitions.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        self._present_at_init(slot)

        # SCPI call
        num_acq = struct.unpack("I", self._acq_list_rb(slot, sequencer))[0]
        if num_acq == 0:
            self._flush_line_end()

        acquisition_dict = {}
        for acq_it in range(0, num_acq):
            # Get name and index
            name = str(self._read_bin("", False), "utf-8")
            index = struct.unpack("I", self._read_bin("", False))[0]

            # Get data
            if self._is_qtm_type(slot):
                acq = self._get_acq_data(
                    slot, partial(self._read_bin, "", False), acq_it >= (num_acq - 1)
                )
            else:
                acq = self._get_acq_data_and_convert(
                    slot, partial(self._read_bin, "", False), acq_it >= (num_acq - 1)
                )

            # Add to dictionary
            acquisition_dict[name] = {"index": index, "acquisition": acq}

        return acquisition_dict

    # ----------------------------------------------------------------------------
    def _get_acq_data_and_convert(
        self,
        slot: int,
        init_read_func: Callable[[Optional[int], Optional[str]], bytes],
        flush_line_end: bool,
    ) -> dict:
        """
        Get acquisition data and convert it to a dictionary.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        init_read_func : Callable[[Optional[int], Optional[str]], bytes]
            Function that performs the initial binary read.
        flush_line_end : bool
            Indication to flush final characters after final read.

        Returns
        ----------
        dict
            Dictionary with data of single acquisition.
        """
        acquisition_dict = {
            "scope": {
                "path0": {"data": [], "out-of-range": False, "avg_cnt": 0},
                "path1": {"data": [], "out-of-range": False, "avg_cnt": 0},
            },
            "bins": {
                "integration": {"path0": [], "path1": []},
                "threshold": [],
                "avg_cnt": [],
            },
        }

        # QRC-related changes
        if self._is_qrc_type(slot):
            acquisition_dict["scope"].update(
                {"path2": {"data": [], "out-of-range": False, "avg_cnt": 0}}
            )
            acquisition_dict["scope"].update(
                {"path3": {"data": [], "out-of-range": False, "avg_cnt": 0}}
            )

        sample_width = 12
        max_sample_value = 2 ** (sample_width - 1) - 1
        max_sample_value_sqrd = max_sample_value**2

        # Retrieve scope data
        if self._is_qrc_type(slot):
            (
                path0_scope_raw,
                path0_avg_cnt,
                path0_oor,
                path1_scope_raw,
                path1_avg_cnt,
                path1_oor,
                path2_scope_raw,
                path2_avg_cnt,
                path2_oor,
                path3_scope_raw,
                path3_avg_cnt,
                path3_oor,
            ) = self._read_acquisition_raw_data(slot, init_read_func)
        else:
            (
                path0_scope_raw,
                path0_avg_cnt,
                path0_oor,
                path1_scope_raw,
                path1_avg_cnt,
                path1_oor,
            ) = self._read_acquisition_raw_data(slot, init_read_func)

        # Normalize scope data (Ignore division by 0)
        with numpy.errstate(divide="ignore", invalid="ignore"):
            path0_scope = numpy.where(
                path0_avg_cnt > 0,
                path0_scope_raw / max_sample_value / path0_avg_cnt,
                path0_scope_raw / max_sample_value,
            )
            path1_scope = numpy.where(
                path1_avg_cnt > 0,
                path1_scope_raw / max_sample_value / path1_avg_cnt,
                path1_scope_raw / max_sample_value,
            )
            if self._is_qrc_type(slot):
                path2_scope = numpy.where(
                    path2_avg_cnt > 0,
                    path2_scope_raw / max_sample_value / path2_avg_cnt,
                    path2_scope_raw / max_sample_value,
                )
                path3_scope = numpy.where(
                    path3_avg_cnt > 0,
                    path3_scope_raw / max_sample_value / path3_avg_cnt,
                    path3_scope_raw / max_sample_value,
                )

        # Retrieve bin data and convert to long values
        path0_raw, path1_raw, valid, avg_cnt, thres_raw = self._read_bin_raw_data(flush_line_end)

        # Specific data manipulation for QRM
        path0_data = numpy.where(valid, path0_raw / max_sample_value_sqrd, numpy.nan)
        path1_data = numpy.where(valid, path1_raw / max_sample_value_sqrd, numpy.nan)
        thres_data = numpy.where(valid, thres_raw, numpy.nan)
        avg_cnt_data = numpy.where(valid, avg_cnt, 0)

        # Set final results
        acquisition_dict["scope"]["path0"]["data"] = path0_scope.tolist()
        acquisition_dict["scope"]["path0"]["out-of-range"] = path0_oor
        acquisition_dict["scope"]["path0"]["avg_cnt"] = path0_avg_cnt

        acquisition_dict["scope"]["path1"]["data"] = path1_scope.tolist()
        acquisition_dict["scope"]["path1"]["out-of-range"] = path1_oor
        acquisition_dict["scope"]["path1"]["avg_cnt"] = path1_avg_cnt

        if self._is_qrc_type(slot):
            acquisition_dict["scope"]["path2"]["data"] = path2_scope.tolist()
            acquisition_dict["scope"]["path2"]["out-of-range"] = path2_oor
            acquisition_dict["scope"]["path2"]["avg_cnt"] = path2_avg_cnt
            acquisition_dict["scope"]["path3"]["data"] = path3_scope.tolist()
            acquisition_dict["scope"]["path3"]["out-of-range"] = path3_oor
            acquisition_dict["scope"]["path3"]["avg_cnt"] = path3_avg_cnt

        acquisition_dict["bins"]["integration"]["path0"] = path0_data.tolist()
        acquisition_dict["bins"]["integration"]["path1"] = path1_data.tolist()
        acquisition_dict["bins"]["threshold"] = thres_data.tolist()
        acquisition_dict["bins"]["avg_cnt"] = avg_cnt_data.tolist()

        return acquisition_dict

    # ----------------------------------------------------------------------------
    # Next two functions are meant to be used only inside _get_acq_data_* functions
    # because they are tied together of how firmware sends raw scope and bin data
    # QTM fix end
    # ----------------------------------------------------------------------------
    def _read_bin_raw_data(self, flush_line_end) -> tuple:
        bins = self._read_bin("", flush_line_end)
        packet_layout = numpy.dtype(
            [
                ("valid", numpy.uint64),
                ("path0", numpy.int64),
                ("path1", numpy.int64),
                ("thres_raw", numpy.uint32),
                ("avg_cnt", numpy.uint32),
            ]
        )
        bin_data = numpy.frombuffer(bins, dtype=packet_layout)

        # This prevents any copies from being made while
        # still able to interpret the data normally
        valid = bin_data["valid"]
        path0_raw = bin_data["path0"]
        path1_raw = bin_data["path1"]
        thres_raw = bin_data["thres_raw"]
        avg_cnt = bin_data["avg_cnt"]

        # Normalize bin data (Ignore division by 0)
        with numpy.errstate(divide="ignore", invalid="ignore"):
            # numpy.where creates copies of the array, which is not desired.
            # No alternatives that edit the array in-place exist as far as I know
            path0_raw = numpy.where(avg_cnt > 0, path0_raw / avg_cnt, path0_raw)
            path1_raw = numpy.where(avg_cnt > 0, path1_raw / avg_cnt, path1_raw)
            thres_raw = numpy.where(avg_cnt > 0, thres_raw / avg_cnt, thres_raw)

        return path0_raw, path1_raw, valid, avg_cnt, thres_raw

    # ----------------------------------------------------------------------------
    def _read_acquisition_raw_data(self, slot, init_read_func) -> tuple:
        def _retrieve_scope_data(init: bool = False) -> tuple:
            scope_data = init_read_func() if init else self._read_bin("", False)
            path_scope_raw = numpy.frombuffer(scope_data, dtype=numpy.int32)
            path_oor = struct.unpack("?", self._read_bin("", False))[0]
            path_avg_cnt = struct.unpack("I", self._read_bin("", False))[0]
            return path_scope_raw, path_oor, path_avg_cnt

        # Retrieve scope data
        path0_scope_raw, path0_oor, path0_avg_cnt = _retrieve_scope_data(init=True)
        path1_scope_raw, path1_oor, path1_avg_cnt = _retrieve_scope_data()

        if self._is_qrc_type(slot):
            path2_scope_raw, path2_oor, path2_avg_cnt = _retrieve_scope_data()
            path3_scope_raw, path3_oor, path3_avg_cnt = _retrieve_scope_data()

        return (
            (
                path0_scope_raw,
                path0_avg_cnt,
                path0_oor,
                path1_scope_raw,
                path1_avg_cnt,
                path1_oor,
                path2_scope_raw,
                path2_avg_cnt,
                path2_oor,
                path3_scope_raw,
                path3_avg_cnt,
                path3_oor,
            )
            if self._is_qrc_type(slot)
            else (
                path0_scope_raw,
                path0_avg_cnt,
                path0_oor,
                path1_scope_raw,
                path1_avg_cnt,
                path1_oor,
            )
        )

    # ----------------------------------------------------------------------------
    # QTM fix end
    # ----------------------------------------------------------------------------
    def _get_acq_data(
        self,
        slot: int,
        init_read_func: Callable[[Optional[int], Optional[str]], bytes],
        flush_line_end: bool,
    ) -> dict:
        """
        Get acquisition data and convert it to a dictionary.

        Parameters
        ----------
        init_read_func : Callable[[Optional[int], Optional[str]], bytes]
            Function that performs the initial binary read.
        flush_line_end : bool
            Indication to flush final characters after final read.

        Returns
        ----------
        dict
            Dictionary with data of single acquisition.
        """
        # TODO this is only needed here because of the consecutive calls to _read_bin
        # which retrieves data from the socket.
        # So scope_data is not used all in this function
        (
            _path0_scope_raw,
            _path0_avg_cnt,
            _path0_oor,
            _path1_scope_raw,
            _path1_avg_cnt,
            _path1_oor,
        ) = self._read_acquisition_raw_data(slot, init_read_func)

        # Retrieve bin data and convert to long values
        path0_raw, path1_raw, valid, avg_cnt, thres_raw = self._read_bin_raw_data(flush_line_end)

        # Specific data manipulation for QTM
        path0_data = numpy.where(valid, path0_raw, numpy.nan)
        path1_data = numpy.where(valid, path1_raw, numpy.nan)
        thres_data = numpy.where(valid, thres_raw, numpy.nan)
        avg_cnt_data = numpy.where(valid, avg_cnt, 0)

        # Set final results
        acquisition_dict = {
            "bins": {
                "count": path0_data.tolist(),
                "timedelta": path1_data.tolist(),
                "threshold": thres_data.tolist(),
                "avg_cnt": avg_cnt_data.tolist(),
            },
        }

        return acquisition_dict

    # ------------------------------------------------------------------------
    def _add_waveforms(self, slot: int, sequencer: int, waveforms: dict) -> None:
        """
        Add all waveforms in JSON compatible dictionary to the AWG waveform list
        of indexed sequencer. The dictionary must be structured as follows:

        - name: waveform name.

            - data: waveform samples in a range of 1.0 to -1.0.
            - index: optional waveform index used by the sequencer Q1ASM program
              to refer to the waveform.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        waveforms : dict
            JSON compatible dictionary with one or more waveforms and weights.

        Raises
        ----------
        KeyError
            Missing waveform data of waveform in dictionary.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        for name, waveform in waveforms.items():
            if "data" in waveform:
                if "index" in waveform:
                    self._add_awg_waveform(
                        slot,
                        sequencer,
                        name,
                        waveform["data"],
                        waveform["index"],
                    )
                else:
                    self._add_awg_waveform(slot, sequencer, name, waveform["data"])
            else:
                raise KeyError(f"Missing data key for {name} in AWG waveform dictionary")

    def _add_awg_waveform(
        self,
        slot: int,
        sequencer: int,
        name: str,
        waveform: list[float],
        index: Optional[int] = None,
    ) -> None:
        """
        Add new waveform to AWG waveform list of indexed sequencer's AWG path. If
        an invalid sequencer index is given or if the waveform causes the waveform
        memory limit to be exceeded or if the waveform samples are out-of-range,
        an error is set in the system error. The waveform names 'all' and 'ALL'
        are reserved and adding waveforms with those names will also result in an
        error being set in system error. The optional index argument is used to
        specify an index for the waveform in the waveform list which is used by
        the sequencer Q1ASM program to refer to the waveform. If no index is
        given, the next available waveform index is selected (starting from 0).
        If an invalid waveform index is given, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Waveform name.
        waveform : list
            List of floats in the range of 1.0 to -1.0 representing the waveform.
        index : Optional[int]
            Waveform index of the waveform in the waveform list.
        """
        super()._add_awg_waveform(slot, sequencer, name, len(waveform), False)
        super()._set_awg_waveform_data(slot, sequencer, name, waveform)
        if index is not None:
            super()._set_awg_waveform_index(slot, sequencer, name, index)

    # ------------------------------------------------------------------------
    def _delete_waveform(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        """
        Delete a waveform specified by name in the AWG waveform list of indexed
        sequencer or delete all waveforms if `all` is True.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Waveform name
        all : bool
            All waveforms
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        super()._delete_awg_waveform(slot, sequencer, "all" if all else name)

    # ----------------------------------------------------------------------------
    def _get_awg_waveforms(self, slot: int, sequencer: int) -> dict:
        """
        Get all waveforms in waveform list of indexed sequencer's AWG path. If an
        invalid sequencer index is given, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with waveforms.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        # SCPI call
        num_waveforms = struct.unpack("I", self._awg_wlist_rb(slot, sequencer))[0]
        if num_waveforms == 0:
            self._flush_line_end()

        waveform_dict = {}
        for wave_it in range(0, num_waveforms):
            # Get name and index
            name = str(self._read_bin("", False), "utf-8")
            index = struct.unpack("I", self._read_bin("", False))[0]

            # Get data
            raw_bytes = self._read_bin("", wave_it >= (num_waveforms - 1))
            data = numpy.frombuffer(raw_bytes, dtype=numpy.float32)

            # Add to dictionary
            waveform_dict[name] = {"index": index, "data": list(data)}

        return waveform_dict

    # ----------------------------------------------------------------------------
    def _add_acq_weight(
        self,
        slot: int,
        sequencer: int,
        name: str,
        weight: list[float],
        index: Optional[int] = None,
    ) -> None:
        """
        Add new weight to acquisition weight list of indexed sequencer's
        acquisition path. If an invalid sequencer index is given or if the weight
        causes the weight memory limit to be exceeded or if the weight samples are
        out-of-range, an error is set in the system error. The weight names 'all'
        and 'ALL' are reserved and adding weights with those names will also
        result in an error being set in system error. The optional index argument
        is used to specify an index for the weight in the weight list which is
        used by the sequencer Q1ASM program to refer to the weight. If no index
        is given, the next available weight index is selected (starting from 0).
        If an invalid weight index is given, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Weight name.
        weight : list
            List of floats in the range of 1.0 to -1.0 representing the weight.
        index : Optional[int]
            Weight index of the weight in the weight list.
        """
        super()._add_acq_weight(slot, sequencer, name, len(weight), False)
        super()._set_acq_weight_data(slot, sequencer, name, weight)
        if index is not None:
            super()._set_acq_weight_index(slot, sequencer, name, index)

    # ------------------------------------------------------------------------
    def get_waveforms(self, slot: int, sequencer: int) -> dict:
        """
        Get all waveforms and weights in the AWG waveform list of indexed
        sequencer. The returned dictionary is structured as follows:

        - name: waveform name.

            - data: waveform samples in a range of 1.0 to -1.0.
            - index: waveform index used by the sequencer Q1ASM program to refer
                     to the waveform.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with waveforms.
        """
        self._present_at_init(slot)

        check_sequencer_index(sequencer)
        return self._get_awg_waveforms(slot, sequencer)

    # ------------------------------------------------------------------------
    def _add_weights(self, slot: int, sequencer: int, weights: dict) -> None:
        """
        Add all weights in JSON compatible dictionary to the acquisition weight
        list of indexed sequencer. The dictionary must be structured as follows:

        - name : weight name.

            - data: weight samples in a range of 1.0 to -1.0.
            - index: optional waveform index used by the sequencer Q1ASM program to refer
                     to the weight.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        weights : dict
            JSON compatible dictionary with one or more weights.

        Raises
        ----------
        KeyError
            Missing weight data of weight in dictionary.
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))
        check_sequencer_index(sequencer)
        for name, weight in weights.items():
            if "data" in weight:
                if "index" in weight:
                    self._add_acq_weight(
                        slot,
                        sequencer,
                        name,
                        weight["data"],
                        weight["index"],
                    )
                else:
                    self._add_acq_weight(slot, sequencer, name, weight["data"])
            else:
                raise KeyError(f"Missing data key for {name} in acquisition weight dictionary")

    # ------------------------------------------------------------------------
    def _delete_weight(self, slot: int, sequencer: int, name: str = "", all: bool = False) -> None:
        """
        Delete a weight specified by name in the acquisition weight list of
        indexed sequencer or delete all weights if `all` is True.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Weight name
        all : bool
            All weights

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))
        check_sequencer_index(sequencer)
        self._delete_acq_weight(slot, sequencer, "all" if all else name)

    # ------------------------------------------------------------------------
    def get_weights(self, slot: int, sequencer: int) -> dict:
        """
        Get all weights in the acquisition weight lists of indexed sequencer.
        The returned dictionary is structured as follows:

        -name : weight name.

            - data: weight samples in a range of 1.0 to -1.0.
            - index: weight index used by the sequencer Q1ASM program to refer
                     to the weight.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with weights.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qrm_type(slot) or self._is_qrc_type(slot))
        check_sequencer_index(sequencer)
        return self._get_acq_weights(slot, sequencer)

    # ----------------------------------------------------------------------------
    def _get_acq_weights(self, slot: int, sequencer: int) -> dict:
        """
        Get all weights in weight list of indexed sequencer's acquisition path.
        If an invalid sequencer index is given, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with weights.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        # SCPI call
        num_weights = struct.unpack("I", self._acq_wlist_rb(slot, sequencer))[0]
        if num_weights == 0:
            self._flush_line_end()

        weight_dict = {}
        for weight_it in range(0, num_weights):
            # Get name and index
            name = str(self._read_bin("", False), "utf-8")
            index = struct.unpack("I", self._read_bin("", False))[0]

            # Get data
            data = self._read_bin("", weight_it >= (num_weights - 1))
            data = struct.unpack("f" * int(len(data) / 4), data)

            # Add to dictionary
            weight_dict[name] = {"index": index, "data": list(data)}

        return weight_dict

    # ----------------------------------------------------------------------------
    def _add_acq_acquisition(
        self,
        slot: int,
        sequencer: int,
        name: str,
        num_bins: int,
        index: Optional[int] = None,
    ) -> None:
        """
        Add new acquisition to acquisition list of indexed sequencer's acquisition
        path. If an invalid sequencer index is given or if the required
        acquisition memory cannot be allocated, an error is set in system error.
        The acquisition names 'all' and 'ALL' are reserved and adding those will
        also result in an error being set in system error. If no index is given,
        the next available weight index is selected (starting from 0). If an
        invalid weight index is given, an error is set in system error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Acquisition name.
        num_bins : int
            Number of bins in acquisition. Maximum is 2^24.
        index : Optional[int]
            Waveform index of the acquisition in the acquisition list.
        """
        super()._add_acq_acquisition(slot, sequencer, name, num_bins)
        if index is not None:
            super()._set_acq_acquisition_index(slot, sequencer, name, index)

    # ------------------------------------------------------------------------
    def get_acquisition_status(
        self,
        slot: int,
        sequencer: int,
        timeout: int = 0,
        timeout_poll_res: float = 0.02,
        check_seq_state: bool = True,
    ) -> bool:
        """
        Return acquisition binning completion status of the indexed sequencer. If
        an invalid sequencer is given, an error is set in system error. If the
        timeout is set to zero, the function returns the status immediately. If a
        positive non-zero timeout is set, the function blocks until the acquisition
        binning completes. If the acquisition hasn't completed before the timeout
        expires, a TimeoutError is thrown. Note that when sequencer state checking
        is enabled, the sequencer state is checked using get_sequencer_status with
        the selected timeout period first and then the acquisition status is checked
        with the same timeout period. This means that the total timeout period is
        two times the set timeout period.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        timeout : int
            Timeout in minutes.
        timeout_poll_res : float
            Timeout polling resolution in seconds.
        check_seq_state : bool
            Check if sequencer is done before checking acquisition status.

        Returns
        ----------
        bool
            Indicates the acquisition binning completion status (False = uncompleted,
            True = completed).

        Raises
        ----------
        TimeoutError
            Timeout
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        # Check if sequencer has stopped
        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        if check_seq_state:
            seq_status = self.get_sequencer_status(slot, sequencer, timeout, timeout_poll_res)
            if seq_status.state != SequencerStates.STOPPED:
                return False
        else:
            seq_status = self.get_sequencer_status(slot, sequencer)

        # Get acquisition status
        acq_status = SequencerStatusFlags.ACQ_BINNING_DONE in seq_status.info_flags
        elapsed_time = 0.0
        timeout = timeout * 60.0
        while acq_status is False and elapsed_time < timeout:
            time.sleep(timeout_poll_res)

            seq_status = self.get_sequencer_status(slot, sequencer)
            acq_status = SequencerStatusFlags.ACQ_BINNING_DONE in seq_status.info_flags
            elapsed_time += timeout_poll_res

            if elapsed_time >= timeout:
                raise TimeoutError(
                    f"Acquisitions on sequencer {sequencer} did not complete in timeout period "
                    f"of {int(timeout / 60)} minutes."
                )

        return acq_status

    # ------------------------------------------------------------------------
    def _add_acquisitions(self, slot: int, sequencer: int, acquisitions: dict) -> None:
        """
        Add all waveforms and weights in JSON compatible dictionary to AWG
        waveform and acquisition weight lists of indexed sequencer. The dictionary
        must be structured as follows:

        - name: acquisition name.
            - num_bins: number of bins in acquisition.
            - index: optional acquisition index used by the sequencer Q1ASM program to refer
                     to the acquisition.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        acquisitions : dict
            JSON compatible dictionary with one or more acquisitions.

        Raises
        ----------
        KeyError
            Missing dictionary key in acquisitions.
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        check_sequencer_index(sequencer)
        for name, acquisition in acquisitions.items():
            if "num_bins" in acquisition:
                if "index" in acquisition:
                    self._add_acq_acquisition(
                        slot,
                        sequencer,
                        name,
                        acquisition["num_bins"],
                        acquisition["index"],
                    )
                else:
                    self._add_acq_acquisition(slot, sequencer, name, acquisition["num_bins"])
            else:
                raise KeyError(f"Missing num_bins key for {name} in acquisition dictionary")

    # ------------------------------------------------------------------------
    def _delete_acquisition(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        """
        Delete an acquisition specified by name in the acquisition list of indexed
        sequencer or delete all acquisitions if `all` is True.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Weight name
        all : bool
            All weights

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        check_sequencer_index(sequencer)
        self._delete_acq_acquisition(slot, sequencer, "all" if all else name)

    # --------------------------------------------------------------------------
    def delete_acquisition_data(
        self, slot: int, sequencer: int, name: str = "", all: bool = False
    ) -> None:
        """
        Delete data from an acquisition specified by name in the acquisition list
        of indexed sequencer or delete data in all acquisitions if `all` is True.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Weight name

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        check_sequencer_index(sequencer)
        self._delete_acq_acquisition_data(slot, sequencer, "all" if all else name)

    # -------------------------------------------------------------------------
    def store_scope_acquisition(self, slot: int, sequencer: int, name: str) -> None:
        """
        After an acquisition has completed, store the scope acquisition results
        in the acquisition specified by name of the indexed sequencers. If an
        invalid sequencer index is given an error is set in system error. To get
        access to the acquisition results, the sequencer will be stopped when
        calling this function.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Acquisition name.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        check_sequencer_index(sequencer)
        self._set_acq_acquisition_data(slot, sequencer, name)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_data(self, slot: int, sequencer: int, name: str) -> dict:
        """
        Get acquisition data of acquisition in acquisition list of indexed
        sequencer's acquisition path. The acquisition scope and bin data is
        normalized to a range of -1.0 to 1.0 taking both the bit widths of the
        processing path and average count into consideration. For the binned
        integration results, the integration length is not handled during
        normalization and therefore these values have to be divided by their
        respective integration lengths. If an invalid sequencer index is given or
        if a non-existing acquisition name is given, an error is set in system
        error.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        name : str
            Acquisition name.

        Returns
        ----------
        dict
            Dictionary with data of single acquisition.

        Raises
        ----------
        RuntimeError
            An error is reported in system error and debug <= 1.
            All errors are read from system error and listed in the exception.
        """
        self._present_at_init(slot)

        # SCPI call
        check_sequencer_index(sequencer)
        return self._get_acq_data_and_convert(
            slot,
            partial(self._acq_data_rb, slot, sequencer, name),
            True,
        )

    # ------------------------------------------------------------------------
    def get_acquisitions(self, slot: int, sequencer: int) -> dict:
        """
        Get all acquisitions in acquisition lists of indexed sequencer. The
        acquisition scope and bin data is normalized to a range of -1.0 to 1.0
        taking both the bit widths of the processing path and average count into
        consideration. For the binned integration results, the integration length
        is not handled during normalization and therefore these values have to be
        divided by their respective integration lengths. The returned dictionary
        is structured as follows:

        - name: acquisition name

            - index: acquisition index used by the sequencer Q1ASM program to refer
                     to the acquisition.
            - acquisition: acquisition dictionary

                - scope: Scope data

                    - path0: input path 0

                        - data: acquisition samples in a range of 1.0 to -1.0.
                        - out-of-range: out-of-range indication for the entire acquisition
                          (False = in-range, True = out-of-range).
                        - avg_cnt: number of averages.

                    - path1: input path 1

                        - data: acquisition samples in a range of 1.0 to -1.0.
                        - out-of-range: out-of-range indication for the entire acquisition
                          (False = in-range, True = out-of-range).
                        - avg_cnt: number of averages.

                - bins: bin data

                    - integration: integration data

                        - path_0: input path 0 integration result bin list
                        - path_1: input path 1 integration result bin list

                    - threshold: threshold result bin list
                    - valid: list of valid indications per bin
                    - avg_cnt: list of number of averages per bin

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.

        Returns
        ----------
        dict
            Dictionary with acquisitions.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(
            self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot)
        )
        check_sequencer_index(sequencer)
        return self._get_acq_acquisitions(slot, sequencer)

    # ------------------------------------------------------------------------
    def scope_trigger_arm(self, slot: int) -> None:
        """
        Arms the external scope trigger logic on a QTM, such that it will send
        a trigger to scope acquisition blocks in the I/O channels when the trigger
        condition is satisfied.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        self._scope_trigger_arm(slot)

    # ------------------------------------------------------------------------
    def get_scope_data(self, slot: int, io_channel: int) -> Any:
        """
        Returns the QTM I/O channel scope data for the given slot and channel
        acquired since the previous call.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        io_channel : int
            I/O channel you want to get the data for.

        Returns
        ----------
        Any
            The acquired data. Empty if no data acquired since last call.

        Raises
        ----------
        NotImplementedError
            Functionality not available on this module.
        """
        self._present_at_init(slot)

        check_is_valid_type(self._is_qtm_type(slot))
        check_io_channel_index(io_channel)
        return self._get_io_channel_scope_data(slot, io_channel)

    # --------------------------------------------------------------------------
    def delete_dummy_binned_acquisition_data(
        self,
        slot_idx: int,
        sequencer: Optional[int] = None,
        acq_index_name: Optional[str] = None,
    ) -> None:
        """
        Delete all dummy binned acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Optional[int]
            Sequencer.
        acq_index_name : Optional[str]
            Acquisition index name.
        """
        self._transport.delete_dummy_binned_acquisition_data(slot_idx, sequencer, acq_index_name)

    # --------------------------------------------------------------------------
    def set_dummy_binned_acquisition_data(
        self,
        slot_idx: int,
        sequencer: int,
        acq_index_name: str,
        data: Iterable[Union[DummyBinnedAcquisitionData, None]],
    ) -> None:
        """
        Set dummy binned acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : int
            Sequencer.
        acq_index_name : str
            Acquisition index name.
        data : Iterable[Union[DummyBinnedAcquisitionData, None]]
            Dummy data for the binned acquisition.
            An iterable of all the bin values.
        """
        self._transport.set_dummy_binned_acquisition_data(slot_idx, sequencer, acq_index_name, data)

    # --------------------------------------------------------------------------
    def delete_dummy_scope_acquisition_data(
        self, slot_idx: int, sequencer: Union[int, None]
    ) -> None:
        """
        Delete dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Union[int, None]
            Sequencer.
        """
        self._transport.delete_dummy_scope_acquisition_data(slot_idx)

    # --------------------------------------------------------------------------
    def set_dummy_scope_acquisition_data(
        self,
        slot_idx: int,
        sequencer: Union[int, None],
        data: DummyScopeAcquisitionData,
    ) -> None:
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        sequencer : Union[int, None]
            Sequencer.
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.
        """
        self._transport.set_dummy_scope_acquisition_data(slot_idx, data)

    # ------------------------------------------------------------------------
    def _set_sequence(
        self,
        slot: int,
        sequencer: int,
        sequence: Union[str, dict[str, Any]],
        validation_enable: bool = True,
    ) -> None:
        """
        Set sequencer program, AWG waveforms, acquisition weights and acquisitions
        from a JSON file or from a dictionary directly. The JSON file or
        dictionary need to apply the schema specified by
        `QCM_SEQUENCE_JSON_SCHEMA`, `QRM_SEQUENCE_JSON_SCHEMA`, `WAVE_JSON_SCHEMA`
        and `ACQ_JSON_SCHEMA`.

        Parameters
        ----------
        slot : int
            The slot index of the module being referred to.
        sequencer : int
            Sequencer index.
        sequence : Union[str, dict[str, Any]]
            Path to sequence file or dictionary.
        validation_enable : bool
            Enable JSON schema validation on sequence.

        Raises
        ----------
        JsonSchemaValueException
            Invalid JSON object.
        """
        self._present_at_init(slot)

        # Set dictionary
        if isinstance(sequence, dict):
            sequence_dict = sequence
        else:
            with open(sequence, "r") as file:
                sequence_dict = json.load(file)

        # Validate dictionary
        if validation_enable:
            if self._is_qrm_type(slot):
                validate_qrm_sequence(sequence_dict)
            elif self._is_qcm_type(slot):
                validate_qcm_sequence(sequence_dict)
            elif self._is_qtm_type(slot):
                validate_qtm_sequence(sequence_dict)
            elif self._is_qrc_type(slot):
                # TO BE IMPLEMENTED, MAYBE THE CHECKS ARE SIMILAR TO THOSE OF A QRM?
                validate_qrm_sequence(sequence_dict)
            else:
                raise TypeError("Device type not supported")

            if self._is_qcm_type(slot) or self._is_qrm_type(slot) or self._is_qrc_type(slot):
                for name in sequence_dict["waveforms"]:
                    validate_wave(sequence_dict["waveforms"][name])

            if self._is_qrm_type(slot) or self._is_qrc_type(slot):
                for name in sequence_dict["weights"]:
                    validate_wave(sequence_dict["weights"][name])

            if self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot):
                for name in sequence_dict["acquisitions"]:
                    validate_acq(sequence_dict["acquisitions"][name])

        # Set sequence
        self._set_sequencer_program(slot, sequencer, sequence_dict["program"])
        if self._is_qcm_type(slot) or self._is_qrm_type(slot) or self._is_qrc_type(slot):
            self._delete_waveform(slot, sequencer, all=True)
            self._add_waveforms(slot, sequencer, sequence_dict["waveforms"])

        if self._is_qrm_type(slot) or self._is_qrc_type(slot):
            self._delete_weight(slot, sequencer, all=True)
            self._add_weights(slot, sequencer, sequence_dict["weights"])

        if self._is_qrm_type(slot) or self._is_qtm_type(slot) or self._is_qrc_type(slot):
            self._delete_acquisition(slot, sequencer, all=True)
            self._add_acquisitions(slot, sequencer, sequence_dict["acquisitions"])

    # ------------------------------------------------------------------------
    def _get_modules_present(self, slot: int) -> bool:
        """
        Get an indication of module presence for a specific slot in the Cluster.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            Module presence.
        """
        return (int(super()._get_modules_present()) >> (slot - 1)) & 1 == 1

    def _get_modules_connected(self, slot: int) -> bool:
        """
        Get an indication of module connection for a specific slot in the Cluster.

        Parameters
        ----------
        slot : int
            Slot index ranging from 1 to 20.

        Returns
        ----------
        bool
            Module connection
        """
        keys = super()._get_mods_info().keys()
        return slot in [int(key.split()[-1]) for key in keys]
