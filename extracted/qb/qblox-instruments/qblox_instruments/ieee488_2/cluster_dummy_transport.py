# ----------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import json
from collections.abc import Iterable
from typing import Optional, Union

from qblox_instruments import ClusterType
from qblox_instruments.ieee488_2 import (
    DummyBinnedAcquisitionData,
    DummyScopeAcquisitionData,
    DummyTransport,
    ModuleDummyTransport,
)

# -- class -------------------------------------------------------------------


class ClusterDummyTransport(DummyTransport):
    """
    Class to replace Cluster device with dummy device to support software
    stack testing without hardware. The class implements all mandatory,
    required and Cluster specific SCPI calls. Call responses are largely
    artificially constructed to be inline with the call's functionality (e.g.
    `*IDN?` returns valid, but artificial IDN data.) To assist development,
    the Q1ASM assembler has been completely implemented. Please have a look
    at the call's implementation to know what to expect from its response.
    """

    # ------------------------------------------------------------------------
    def __init__(self, dummy_cfg: dict[Union[str, int], ClusterType]) -> None:
        """
        Create Cluster dummy transport class.

        Parameters
        ----------
        dummy_cfg : dict
            Dictionary of dummy module types (e.g. Cluster QCM, Cluster QRM).
            Each key of the dictionary is a slot index with a dummy type
            specification of type :class:`~qblox_instruments.ClusterType`.
        """

        # Initialize base class
        super().__init__(dummy_cfg.get("0", ClusterType._CLUSTER_MM))

        # Set number of slots
        self._num_slots = 20

        # Initialize time module
        self._time_dict = {}
        self._capture_dict = {}

        # Configure module dummy transports
        self._modules = {str(slot_idx): None for slot_idx in range(1, self._num_slots + 1)}
        for slot_idx, slot_cfg in dummy_cfg.items():
            if str(slot_idx) in self._modules:
                self._modules[str(slot_idx)] = ModuleDummyTransport(slot_cfg)

        # Set command list
        self._cmds.update(
            {
                "STATus:QUEStionable:LED:BRIGHTness?": self._get_led_brightness,
                "STATus:GENeral:STATE?": self._get_system_state,
                "*MODS?": self._get_mods_info,
                "*DESCribe?": self._get_json_description,
                "BP:MODules?": self._get_modules_present,
                "TIMEkeeping:CURRent:TIMEstamp?": self._get_current_timestamp,
                "TIMEkeeping:CAPTure?": self._get_timekeeping_capture,
            }
        )

    # ------------------------------------------------------------------------
    def _execute_cmd(
        self,
        cmd_parts: list,
        cmd_params: list,
        cmd_args: list,
        bin_in: Optional[bytes] = None,
    ) -> None:
        """
        Execute associated command method found in command dictionary.
        If the command is intended for a slot as indicated by the first
        command part being "SLOT#", the command is executed by the
        associated module.

        Parameters
        ----------
        cmd_parts : list
            Reformatted command sections
        cmd_params : list
            Command parameters
        cmd_args : list
            Command arguments
        bin_in : Optional[bytes]
            Binary data that needs to be send by the command.
        """

        def is_fanout_command(cmd_parts: list[str]) -> bool:
            """
            Check whether the command can fan out to all slots. Not all commands have
            this behavior.
            """
            cmd_str = ":".join(cmd_parts)
            return cmd_str in {
                "SLOT:SEQuencer:ARM",
                "SLOT:SEQuencer:START",
                "SLOT:SEQuencer:STOP",
                "SLOT:SEQuencer:CLR:FLAGS",
            }

        # If command is intended for a slot, remove the slot specification
        # and execute the command on the module instead.
        if cmd_parts[0] == "SLOT#":
            cmd_parts.pop(0)
            slot = cmd_params.pop(0)
            if slot in self._modules:
                mod = self._modules[slot]

                mod._execute_cmd(cmd_parts, cmd_params, cmd_args, bin_in)

                # Copy results and errors from module.
                self._data_out = mod._data_out
                self._bin_out = mod._bin_out
                for error in mod._system_error:
                    self._system_error.append(error)
                mod._system_error = []
            else:
                self._system_error.append(f"Module in slot {slot} is not available.")

        # If command is intended for all slots, execute it on all modules.
        elif is_fanout_command(cmd_parts):
            cmd_parts.pop(0)
            for mod in self._modules.values():
                if mod is None:
                    continue
                mod._execute_cmd(cmd_parts, cmd_params, cmd_args, bin_in)

                # Copy results and errors from module.
                self._data_out = mod._data_out
                self._bin_out = mod._bin_out
                for error in mod._system_error:
                    self._system_error.append(error)
                mod._system_error = []
        else:
            super()._execute_cmd(cmd_parts, cmd_params, cmd_args, bin_in)

    # ------------------------------------------------------------------------
    def _get_led_brightness(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get LED brightness

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._data_out = "HIGH"

    # ------------------------------------------------------------------------
    def _get_system_state(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get system status.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        super()._get_system_state(cmd_params, cmd_args, bin_in)
        for slot_idx in self._modules:
            if self._modules[slot_idx] is not None:
                self._modules[slot_idx]._get_system_state(cmd_params, cmd_args, bin_in)

                flags = self._modules[slot_idx]._data_out.split(";")[1]
                flags = flags.split(",")[:-1]
                flags = [f"SLOT {slot_idx} {flag}" for flag in flags]

                self._data_out += ",".join(flags)
                if len(flags) > 0:
                    self._data_out += ","

    # ------------------------------------------------------------------------
    def _get_mods_info(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get information about the modules in the Cluster (i.e. IDN and RF indication).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        mod_info = {}
        for slot_idx in self._modules:
            if self._modules[slot_idx] is not None:
                self._modules[slot_idx]._get_idn([], [], None)
                mod_info["SLOT " + slot_idx] = {
                    "IDN": self._modules[slot_idx]._data_out,
                    "EOM": self._modules[slot_idx].is_eom_type,
                }

        self._bin_out = self._encode_bin(json.dumps(mod_info).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_current_timestamp(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get current timestamp

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if len(self._time_dict) > 0:
            self._bin_out = self._encode_bin(self._time_dict)
        else:
            self._time_dict = {
                "ns": 100000,
                "sub": 2047,
            }
            self._bin_out = self._encode_bin(json.dumps(self._time_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_timekeeping_capture(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get timekeeping capture

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if len(self._capture_dict) > 0:
            self._bin_out = self._encode_bin(self._capture_dict)
        else:
            self._capture_dict = {
                "ns": 100000,
                "sub": 2047,
            }
            self._bin_out = self._encode_bin(json.dumps(self._capture_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_json_description(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get information about the modules in the Cluster in a JSON format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        json_description = {
            "cfg_man": {
                "build": 1731922856,
                "dirty": True,
                "hash": "51D8517D",
                "version": [0, 0, 0],
            },
            "fw": {
                "build": 1726644953,
                "dirty": False,
                "hash": "98F2499F",
                "version": [0, 0, 0],
            },
            "kmod": {
                "build": 1731922856,
                "dirty": True,
                "hash": "51D8517D",
                "version": [0, 0, 0],
            },
            "manufacturer": "Qblox",
            "model": "cluster_mm",
            "modules": {},
        }

        for slot_idx in self._modules:
            if self._modules[slot_idx] is not None:
                json_description["modules"][slot_idx] = {
                    "cfg_man": {
                        "build": 1731922856,
                        "dirty": True,
                        "hash": "51D8517D",
                        "version": [0, 0, 0],
                    },
                    "fw": {
                        "build": 1727269481,
                        "dirty": True,
                        "hash": "EDE27EF1",
                        "version": [0, 0, 0],
                    },
                    "kmod": {
                        "build": 1731922856,
                        "dirty": True,
                        "hash": "51D8517D",
                        "version": [0, 0, 0],
                    },
                    "manufacturer": "Qblox",
                    "model": "Cluster_" + str(self._modules[slot_idx].module_type),
                    "name": "Cluster-" + str(self._modules[slot_idx].module_type),
                    "ser": "00019_2426_027",
                    "sw": {
                        "build": 1731922856,
                        "dirty": True,
                        "hash": "51D8517D",
                        "version": [0, 0, 0],
                    },
                    "is_rf": self._modules[slot_idx].is_rf_type,
                    "qtm_eom": self._modules[slot_idx].is_eom_type,
                }
        self._bin_out = self._encode_bin(json.dumps(json_description).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_modules_present(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get modules present in the Cluster.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        mod_present = 0
        for slot_idx in self._modules:
            if self._modules[slot_idx] is not None:
                mod_present |= 1 << (int(slot_idx) - 1)

        self._data_out = mod_present

    # ------------------------------------------------------------------------
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
        self._modules[str(slot_idx)].delete_dummy_binned_acquisition_data(sequencer, acq_index_name)

    # ------------------------------------------------------------------------
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
        self._modules[str(slot_idx)].set_dummy_binned_acquisition_data(
            sequencer, acq_index_name, data
        )

    # ------------------------------------------------------------------------
    def delete_dummy_scope_acquisition_data(self, slot_idx: int) -> None:
        """
        Delete dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        """

        self._modules[str(slot_idx)].delete_dummy_scope_acquisition_data()

    # ------------------------------------------------------------------------
    def set_dummy_scope_acquisition_data(
        self, slot_idx: int, data: DummyScopeAcquisitionData
    ) -> None:
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        slot_idx : int
            Slot of the hardware you want to set the data to on a cluster.
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.
        """

        self._modules[str(slot_idx)].set_dummy_scope_acquisition_data(data)
