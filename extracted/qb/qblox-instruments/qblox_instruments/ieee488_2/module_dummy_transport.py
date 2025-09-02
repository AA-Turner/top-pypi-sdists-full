# ----------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import collections.abc
import json
import os
import struct
import subprocess
import sys
from collections.abc import Iterable
from copy import deepcopy
from typing import Optional, Union

from qblox_instruments import ClusterType, InstrumentType
from qblox_instruments.ieee488_2 import (
    DummyBinnedAcquisitionData,
    DummyScopeAcquisitionData,
    DummyTransport,
)

# -- class -------------------------------------------------------------------


class ModuleDummyTransport(DummyTransport):
    """
    Class to replace a module with a dummy device to support software
    stack testing without hardware. The class implements all mandatory,
    required and module specific SCPI calls. Call responses are largely
    artificially constructed to be inline with the call's functionality (e.g.
    `*IDN?` returns valid, but artificial IDN data.) To assist development,
    the Q1ASM assembler has been completely implemented. Please have a look
    at the call's implementation to know what to expect from its response.
    """

    # ------------------------------------------------------------------------
    def __init__(self, dummy_type: ClusterType) -> None:
        """
        Create module dummy transport class.

        Parameters
        ----------
        dummy_type : ClusterType
            Dummy module type
        """

        # Initialize base class
        super().__init__(dummy_type)

        # Initialize variables
        self._asm_status = False
        self._asm_log = ""
        self._pre_distortion_cfg = {}
        self._acq_scope_cfg: bytes = b""
        self._sequencer_cfg: dict[str, bytes] = {}
        self._sequencer_status: dict[str, str] = {}
        # For QRC, the indexed attenuation parameters are set (indexed by sm_channel),
        # which is different than the regular attenuation parameter.
        self._out_att_indexed = {}

        self._num_seq = 6
        if self.is_qcm_type:
            self._channelmap = {str(n): [[0, 2], [1, 3]] for n in range(self._num_seq)}
            self._acq_channelmap = {}
        elif self.is_qrm_type:
            self._channelmap = {str(n): [[0], [1]] for n in range(self._num_seq)}
            self._acq_channelmap = {str(n): [[0], [1]] for n in range(self._num_seq)}
        elif self.is_qrc_type:
            self._num_seq = 12
            self._channelmap = {
                str(n): [[0, 2, 4, 6, 8, 10], [1, 3, 5, 7, 9, 11]] for n in range(self._num_seq)
            }
            self._acq_channelmap = {str(n): [[0], [1]] for n in range(self._num_seq)}
            self._out_att_indexed = {str(sm_channel): 0.0 for sm_channel in range(self._num_seq)}
        elif self.is_qtm_type:
            self._num_seq = 8
            # The channel map is fixed 1x1.
            self._channelmap = {str(n): [n] for n in range(self._num_seq)}
            self._acq_channelmap = {str(n): [n] for n in range(self._num_seq)}

        self._awg_waveforms = {}
        self._acq_weights = {}
        self._acq_metadata = {}
        self._acq_acquisitions = {}
        self._acq_acquisitions_dummy = {}
        self._acq_scope_acquisition = None
        self._acq_scope_acquisition_dummy = None
        self._port_cfg = {}

        self._io_channel_cfg = {}
        self._io_channel_status_cfg = {}
        self._quad_cfg = {}
        self._current_timestamp = {}
        self._current_capture = {}

        # Set command dictionary
        self._cmds.update(
            {
                "STATus:ASSEMbler:SUCCess?": self._get_assembler_status,
                "STATus:ASSEMbler:LOG?": self._get_assembler_log,
                "ACQ:SCOpe:CONFiguration": self._set_acq_scope_config,
                "ACQ:SCOpe:CONFiguration?": self._get_acq_scope_config,
                "SEQuencer#:PROGram": self._set_sequencer_program,
                "SEQuencer#:CONFiguration": self._set_sequencer_config,
                "SEQuencer#:CONFiguration?": self._get_sequencer_config,
                "SEQuencer#:STATE?": self._get_sequencer_state,
                "SEQuencer#:AWG:WLISt:WAVeform:NEW": self._add_awg_waveform,
                "SEQuencer#:AWG:WLISt:WAVeform:DELete": self._del_awg_waveform,
                "SEQuencer#:AWG:WLISt:WAVeform:DATA": self._set_awg_waveform_data,
                "SEQuencer#:AWG:WLISt:WAVeform:DATA?": self._get_awg_waveform_data,
                "SEQuencer#:AWG:WLISt:WAVeform:INDex": self._set_awg_waveform_index,
                "SEQuencer#:AWG:WLISt:WAVeform:INDex?": self._get_awg_waveform_index,
                "SEQuencer#:AWG:WLISt:WAVeform:LENGth?": self._get_awg_waveform_length,
                "SEQuencer#:AWG:WLISt:WAVeform:NAME?": self._get_awg_waveform_name,
                "SEQuencer#:AWG:WLISt:SIZE?": self._get_num_awg_waveforms,
                "SEQuencer#:AWG:WLISt?": self._get_awg_waveforms,
                "SEQuencer#:ACQ:WLISt:WEIght:NEW": self._add_acq_weight,
                "SEQuencer#:ACQ:WLISt:WEIght:DELete": self._del_acq_weight,
                "SEQuencer#:ACQ:WLISt:WEIght:DATA": self._set_acq_weight_data,
                "SEQuencer#:ACQ:WLISt:WEIght:DATA?": self._get_acq_weight_data,
                "SEQuencer#:ACQ:WLISt:WEIght:INDex": self._set_acq_weight_index,
                "SEQuencer#:ACQ:WLISt:WEIght:INDex?": self._get_acq_weight_index,
                "SEQuencer#:ACQ:WLISt:WEIght:LENGth?": self._get_acq_weight_length,
                "SEQuencer#:ACQ:WLISt:WEIght:NAME?": self._get_acq_weight_name,
                "SEQuencer#:ACQ:WLISt:SIZE?": self._get_num_acq_weights,
                "SEQuencer#:ACQ:WLISt?": self._get_acq_weights,
                "SEQuencer#:ACQ:ALISt:ACQuisition:NEW": self._add_acq_acquisition,
                "SEQuencer#:ACQ:ALISt:ACQuisition:DELete": self._del_acq_acquisition,
                "SEQuencer#:ACQ:ALISt:ACQuisition:DATA": self._set_acq_acquisition_data,
                "SEQuencer#:ACQ:ALISt:ACQuisition:DATA?": self._get_acq_acquisition_data,
                "SEQuencer#:ACQ:ALISt:ACQuisition:DATA:DELete": self._del_acq_acquisition_data,
                "SEQuencer#:ACQ:ALISt:ACQuisition:INDex": self._set_acq_acquisition_index,
                "SEQuencer#:ACQ:ALISt:ACQuisition:INDex?": self._get_acq_acquisition_index,
                "SEQuencer#:ACQ:ALISt:ACQuisition:NUM_BINS?": self._get_acq_acquisition_num_bins,
                "SEQuencer#:ACQ:ALISt:ACQuisition:NAME?": self._get_acq_acquisition_name,
                "SEQuencer#:ACQ:ALISt:SIZE?": self._get_num_acq_acquisitions,
                "SEQuencer#:ACQ:ALISt?": self._get_acq_acquisitions,
                "SEQuencer#:ACQ:CHANnelmap": self._set_acq_channelmap,
                "SEQuencer#:ACQ:CHANnelmap?": self._get_acq_channelmap,
                "SEQuencer#:CHANnelmap": self._set_channelmap,
                "SEQuencer#:CHANnelmap?": self._get_channelmap,
                "SEQuencer#:ARM": self._arm,
                "SEQuencer#:START": self._start,
                "SEQuencer#:STOP": self._stop,
                "AFE:ATT:OUT#": self._set_out_att,
                "AFE:ATT:OUT#?": self._get_out_att,
                "AFE:ATT:OUT#:MAX?": self._get_max_out_att,
                "AFE:OUT:ATT:SET?": self._set_out_att_indexed,
                "AFE:OUT:ATT:GET?": self._get_out_att_indexed,
                "AFE:OUT:MAX:ATT:GET?": self._get_max_out_att_indexed,
                "AFE:ATT:IN#": self._set_in_att,
                "AFE:ATT:IN#?": self._get_in_att,
                "LO#:ENAble": self._set_lo_enable,
                "LO#:ENAble?": self._get_lo_enable,
                "STATus:QUEStionable:FREQuency:LO#": self._set_lo_freq,
                "STATus:QUEStionable:FREQuency:LO#?": self._get_lo_freq,
                "AFE:OFFSet:OUTAMP#": self._set_out_amp_offset,
                "AFE:OFFSet:OUTAMP#?": self._get_out_amp_offset,
                "AFE:OFFSet:DAC#": self._set_dac_offset,
                "AFE:OFFSet:DAC#?": self._get_dac_offset,
                "AFE:GAIN:INAMP#": self._set_in_amp_gain,
                "AFE:GAIN:INAMP#?": self._get_in_amp_gain,
                "STATus:QUEStionable:POWer:LO#": self._set_lo_pwr,
                "STATus:QUEStionable:POWer:LO#?": self._get_lo_pwr,
                "PREDISTortion:CONFiguration": self._set_pre_distortion_config,
                "PREDISTortion:CONFiguration?": self._get_pre_distortion_config,
                "IO:CHANnel#:CONFig": self._set_io_channel_config,
                "IO:CHANnel#:CONFig?": self._get_io_channel_config,
                "IO:CHANnel#:STATus?": self._get_io_channel_status,
                "QUAD#:CONFig": self._set_quad_config,
                "QUAD#:CONFig?": self._get_quad_config,
                "TIMEkeeping:CURRent:TIMEstamp?": self._get_current_timestamp,
                "TIMEkeeping:CAPTure?": self._get_timekeeping_capture,
            }
        )

    # ------------------------------------------------------------------------
    @property
    def is_qcm_type(self) -> bool:
        """
        Return if module is of type QCM.

        Returns
        ----------
        bool
            True if module is of type QCM.
        """

        return self._type_handle.is_qcm_type

    # ------------------------------------------------------------------------
    @property
    def is_qrm_type(self) -> bool:
        """
        Return if module is of type QRM.

        Returns
        ----------
        bool
            True if module is of type QRM.
        """

        return self._type_handle.is_qrm_type

    # ------------------------------------------------------------------------
    @property
    def is_qtm_type(self) -> bool:
        """
        Return if module is of type QTM.

        Returns
        ----------
        bool
            True if module is of type QTM.
        """

        return self._type_handle.is_qtm_type

    # ------------------------------------------------------------------------
    @property
    def is_qdm_type(self) -> bool:
        """
        Return if module is of type QDM.

        Returns
        ----------
        bool
            True if module is of type QDM.
        """

        return self._type_handle.is_qdm_type

    # ------------------------------------------------------------------------
    @property
    def module_type(self) -> InstrumentType:
        """
        Return module type.

        Returns
        ----------
        InstrumentType
            Module type.
        """

        return self._type_handle.instrument_type

    # ------------------------------------------------------------------------
    @property
    def is_linq_type(self) -> bool:
        """
        Return if module is of type LINQ.

        Returns
        ----------
        bool
            True if module is of type LINQ.
        """

        return self._type_handle.is_linq_type

    # ------------------------------------------------------------------------
    @property
    def is_eom_type(self) -> bool:
        """
        Return if module is of type EOM.

        Returns
        ----------
        bool
            True if module is of type EOM.
        """

        return self._type_handle.is_eom_type

    # ------------------------------------------------------------------------
    @property
    def is_qrc_type(self) -> bool:
        """
        Return if module is of type QRC.

        Returns
        ----------
        bool
            True if module is of type QRC.
        """

        return self._type_handle.is_qrc_type

    # ------------------------------------------------------------------------
    @property
    def is_qsm_type(self) -> bool:
        """
        Return if module is of type QSM.

        Returns
        ----------
        bool
            True if module is of type QSM.
        """

        return self._type_handle.is_qsm_type

    # ------------------------------------------------------------------------
    @property
    def is_rf_type(self) -> bool:
        """
        Return if module is of type QCM-RF or QRM-RF.

        Returns
        ----------
        bool
            True if module is of type QCM-RF or QRM-RF.
        """

        return self._type_handle.is_rf_type

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
        If the command is not in the command dictionary, respond with the
        default response ('0').

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
            Check whether the command can fan out to all sequencers. Not all commands
            have this behavior.
            """
            cmd_str = ":".join(cmd_parts)
            return cmd_str in {
                "SEQuencer:ARM",
                "SEQuencer:START",
                "SEQuencer:STOP",
                "SEQuencer:CLR:FLAGS",
            }

        if is_fanout_command(cmd_parts):
            # Command is meant for all sequencers.
            new_cmd_parts = ["SEQuencer#", *cmd_parts[1:]]
            for sequencer_idx in range(self._num_seq):
                super()._execute_cmd(new_cmd_parts, [sequencer_idx, *cmd_params], cmd_args, bin_in)
        else:
            super()._execute_cmd(cmd_parts, cmd_params, cmd_args, bin_in)

    # ------------------------------------------------------------------------
    def delete_dummy_binned_acquisition_data(
        self, sequencer: Optional[int] = None, acq_index_name: Optional[str] = None
    ) -> None:
        """
        Set dummy binned acquisition data for the dummy.

        Parameters
        ----------
        sequencer : Optional[int]
            Sequencer.
        acq_index_name : Optional[str]
            Acquisition index name.
        """

        sequencer = str(sequencer)
        if sequencer is None:
            self._acq_acquisitions_dummy = {}
        elif acq_index_name is None:
            self._acq_acquisitions_dummy.pop(sequencer, None)
        else:
            self._acq_acquisitions_dummy.get(sequencer, {}).pop(acq_index_name, None)

    # ------------------------------------------------------------------------
    def set_dummy_binned_acquisition_data(
        self,
        sequencer: int,
        acq_index_name: str,
        data: Iterable[Union[DummyBinnedAcquisitionData, None]],
    ) -> None:
        """
        Set dummy binned acquisition data for the dummy.

        Parameters
        ----------
        sequencer : int
            Sequencer.
        acq_index_name : str
            Acquisition index name.
        data : Iterable[Union[DummyBinnedAcquisitionData, None]]
            Dummy data for the binned acquisition.
            An iterable of all the bin values.
        """

        def _unnormalized_int(single_data: DummyBinnedAcquisitionData) -> list[int]:
            sample_width = 12
            max_sample_value = 2 ** (sample_width - 1) - 1
            max_sample_value_sqrd = max_sample_value**2

            int0, int1 = single_data.data[0], single_data.data[1]
            int0 *= max_sample_value_sqrd * (single_data.avg_cnt or 1)
            int1 *= max_sample_value_sqrd * (single_data.avg_cnt or 1)
            return [round(int0), round(int1)]

        sequencer = str(sequencer)
        if sequencer not in self._acq_acquisitions_dummy:
            self._acq_acquisitions_dummy[sequencer] = {}

        bins = []
        for single_data in data:
            if single_data is None:
                bins.append({"valid": False, "int": [0, 0], "thres": 0, "avg_cnt": 0})
            else:
                bins.append(
                    {
                        "valid": True,
                        "int": _unnormalized_int(single_data),
                        "thres": round(single_data.thres * (single_data.avg_cnt or 1)),
                        "avg_cnt": single_data.avg_cnt,
                    }
                )

        if acq_index_name not in self._acq_acquisitions_dummy[sequencer]:
            self._acq_acquisitions_dummy[sequencer][acq_index_name] = {}
        if "acq" not in self._acq_acquisitions_dummy[sequencer][acq_index_name]:
            self._acq_acquisitions_dummy[sequencer][acq_index_name]["acq"] = {}
        self._acq_acquisitions_dummy[sequencer][acq_index_name]["acq"]["bins"] = bins
        if "scope" not in self._acq_acquisitions_dummy[sequencer][acq_index_name]:
            self._acq_acquisitions_dummy[sequencer][acq_index_name]["acq"]["scope"] = (
                self._initial_scope_acquisition_data()
            )

    # ------------------------------------------------------------------------
    def delete_dummy_scope_acquisition_data(self) -> None:
        """
        Delete dummy scope acquisition data for the dummy.
        """

        self._acq_scope_acquisition_dummy = self._initial_scope_acquisition_data()

    # ------------------------------------------------------------------------
    def set_dummy_scope_acquisition_data(self, data: DummyScopeAcquisitionData) -> None:
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.
        """

        def _unnormalized_int(val, avg_cnt) -> int:
            sample_width = 12
            max_sample_value = 2 ** (sample_width - 1) - 1
            return round(val * max_sample_value * (avg_cnt or 1))

        def _pack_data(data) -> bytes:
            return struct.pack("i" * len(data), *data)

        converted_data = ([], [], [], [])
        for single_data in data.data:
            num_paths = 4 if self.is_qrc_type else 2
            for i in range(num_paths):
                if (i < len(single_data)) and (i < len(data.avg_cnt)):
                    converted_data[i].append(_unnormalized_int(single_data[i], data.avg_cnt[i]))

        if self.is_qrc_type:
            data_data = (
                _pack_data(converted_data[0]),
                _pack_data(converted_data[1]),
                _pack_data(converted_data[2]),
                _pack_data(converted_data[3]),
            )
        else:
            data_data = (
                _pack_data(converted_data[0]),
                _pack_data(converted_data[1]),
            )

        self._acq_scope_acquisition_dummy = {
            "data": data_data,
            "or": data.out_of_range,
            "avg_cnt": data.avg_cnt,
        }

    # ------------------------------------------------------------------------
    def _get_assembler_status(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler status. Refer to the assembler log to get more
        information regarding the assembler result.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._data_out = str(int(self._asm_status))

    # ------------------------------------------------------------------------
    def _get_assembler_log(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler log.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._bin_out = self._encode_bin(self._asm_log.encode())

    # ------------------------------------------------------------------------
    def _set_acq_scope_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of scope acquisition; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._acq_scope_cfg = self._decode_bin(bin_in)

    # ------------------------------------------------------------------------
    def _get_acq_scope_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of scope acquisition. If no
        configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if len(self._acq_scope_cfg) > 0:
            self._bin_out = self._encode_bin(self._acq_scope_cfg)
        else:
            if self.is_qrm_type or self.is_qtm_type:
                acq_scope_dict = {
                    "sel_acq": False,
                    "avg_en_path": [False, False],
                    "trig": {"mode_path": [False, False], "lvl_path": [0.0, 0.0]},
                }
            elif self.is_qrc_type:
                acq_scope_dict = {
                    "sel_acq": False,
                    "avg_en_path": [False, False, False, False],
                    "sel_path": [0, 0, 0, 0],
                    "trig": {
                        "mode_path": [False, False, False, False],
                        "lvl_path": [0.0, 0.0, 0.0, 0.0],
                    },
                }

            self._bin_out = self._encode_bin(json.dumps(acq_scope_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _set_pre_distortion_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of pre-distortion settings; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        # recursive function to update the endpoints of a dictionary.
        # https://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
        def update(d, u) -> dict:
            for k, v in u.items():
                if isinstance(v, collections.abc.Mapping):
                    d[k] = update(d.get(k, {}), v)
                else:
                    d[k] = v
            return d

        self._get_pre_distortion_config([], [], b"")
        old_cfg = json.loads(self._decode_bin(self._bin_out))
        old_cfg = update(old_cfg, json.loads(self._decode_bin(bin_in)))
        self._pre_distortion_cfg = old_cfg

    # ------------------------------------------------------------------------
    def _get_pre_distortion_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of predistortion. If no
        configuration was previously stored a default config is returned.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if len(self._pre_distortion_cfg) > 0:
            self._bin_out = self._encode_bin(json.dumps(self._pre_distortion_cfg).encode("utf-8"))
        else:
            state_config = {f"stage{n}": "enabled" for n in range(6)}
            output_config = {
                "state": deepcopy(state_config),
                "markers": {"state": deepcopy(state_config)},
                "IIR": {f"stage{n}": {"tau": 0.0, "amp": 0.0} for n in range(4)},
                "FIR": {"stage0": [0] * 32},
            }
            pre_distortion_cfg = {f"out{n}": deepcopy(output_config) for n in range(12)}

            self._bin_out = self._encode_bin(json.dumps(pre_distortion_cfg).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _set_sequencer_program(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Runs provided sequencer Q1ASM program through assembler. The assembler
        is a pre-compiled application, which is selected based on the platform
        this method is called on. The assembler status and log are stored and
        can be retrieved using corresponding methods. On a failure to assemble
        an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        q1asm_str = self._decode_bin(bin_in).decode()
        with open("./tmp.q1asm", "w") as fid:
            fid.write(q1asm_str)

        if os.name == "nt":  # Windows
            assembler_path = os.path.abspath(
                os.path.dirname(os.path.abspath(__file__)) + "../../assemblers/q1asm_windows.exe"
            )
            proc = subprocess.Popen(
                [assembler_path, "-o", "tmp", "tmp.q1asm"],
                shell=True,
                text=True,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        elif sys.platform == "darwin":  # MacOS
            assembler_path = os.path.abspath(
                os.path.dirname(os.path.abspath(__file__)) + "../../assemblers/q1asm_macos"
            )
            proc = subprocess.Popen(
                [assembler_path + " -o tmp tmp.q1asm"],
                shell=True,
                text=True,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:  # Linux
            assembler_path = os.path.abspath(
                os.path.dirname(os.path.abspath(__file__)) + "../../assemblers/q1asm_linux"
            )
            proc = subprocess.Popen(
                [assembler_path + " -o tmp tmp.q1asm"],
                shell=True,
                text=True,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        self._asm_log = proc.communicate()[0]
        self._asm_status = not proc.returncode

        if not self._asm_status:
            self._system_error.append("Assembly failed.")

    # ------------------------------------------------------------------------
    def _set_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of indexed sequencer; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._sequencer_cfg[cmd_params[0]] = self._decode_bin(bin_in)

    # ------------------------------------------------------------------------
    def _get_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of the indexed sequencer.
        If no configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._sequencer_cfg:
            self._bin_out = self._encode_bin(self._sequencer_cfg[cmd_params[0]])
        else:
            cfg_dict = {
                "acq": [
                    {
                        "demod": {"en": False},
                        "th_acq": {
                            "discr_threshold": 0.0,
                            "non_weighed_integration_len": 1024,
                            "rotation_matrix_a11": 1.0,
                            "rotation_matrix_a12": 0.0,
                        },
                        "th_acq_mrk_map": {
                            "addr": 0,
                            "en": False,
                            "inv": False,
                        },
                        "th_acq_trg_map": {
                            "addr": 0,
                            "en": False,
                            "inv": False,
                        },
                        "ttl": {
                            "auto_bin_incr_en": False,
                            "in": False,
                            "threshold": 0.0,
                        },
                    }
                ],
                "awg": [
                    {
                        "cont_mode": {
                            "en_path": [False, False],
                            "wave_idx_path": [0, 0],
                        },
                        "mixer": {
                            "en": False,
                            "corr_gain_ratio": 1.0,
                            "corr_phase_offset_degree": -0.0,
                        },
                        "marker_ovr": {"en": False, "val": 0},
                        "gain_path": [1.0, 1.0],
                        "nco": {
                            "freq_hz": 0.0,
                            "po": 0.0,
                            "delay_comp": 0,
                            "delay_comp_en": False,
                        },
                        "offs_path": [0.0, 0.0],
                        "upsample_rate_path": [0, 0],
                    }
                ],
                "seq_proc": {
                    "sync_en": False,
                    "trg": [{"count_threshold": 1, "threshold_invert": False} for _ in range(15)],
                },
            }

            self._bin_out = self._encode_bin(json.dumps(cfg_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _set_io_channel_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of indexed io_channel; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._io_channel_cfg[cmd_params[0]] = self._decode_bin(bin_in)

    # ------------------------------------------------------------------------
    def _get_io_channel_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of the indexed io channel.
        If no configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._io_channel_cfg:
            self._bin_out = self._encode_bin(self._io_channel_cfg[cmd_params[0]])
        else:
            cfg_dict = {
                "out_mode": "low",
                "in_threshold_primary": 0.0,
                "binned_acq_time_source": "first",
                "binned_acq_time_ref": "start",
                "binned_acq_on_invalid_time_delta": "error",
                "binned_acq_count_source": "timetags",
                "binned_acq_on_invalid_count": "error",
                "binned_acq_threshold_source": "thresh0",
                "binned_acq_on_invalid_threshold": "error",
                "in_trigger_en": False,
                "in_trigger_mode": "sequencer",
                "in_trigger_address": 1,
                "scope_trigger_mode": "sequencer",
                "scope_trigger_level": "any",
                "scope_mode": "scope",
                "thresholded_acq_trigger_en": False,
                "thresholded_acq_trigger_address_low": 0,
                "thresholded_acq_trigger_address_mid": 0,
                "thresholded_acq_trigger_address_high": 0,
                "thresholded_acq_trigger_address_invalid": 0,
                "thresholded_acq_lut_en": False,
                "thresholded_acq_lut_data": {},
            }

            self._bin_out = self._encode_bin(json.dumps(cfg_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_io_channel_status(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored status of the indexed io channel.
        If no configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._io_channel_status_cfg:
            self._bin_out = self._encode_bin(self._io_channel_status_cfg[cmd_params[0]])
        else:
            cfg_dict = {
                "io_monitor": 0,
            }

            self._bin_out = self._encode_bin(json.dumps(cfg_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _set_quad_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of indexed quad; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._quad_cfg[cmd_params[0]] = self._decode_bin(bin_in)

    # ------------------------------------------------------------------------
    def _get_quad_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of the indexed sequencer.
        If no configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._quad_cfg:
            self._bin_out = self._encode_bin(self._quad_cfg[cmd_params[0]])
        else:
            cfg_dict = {
                "timetag_oversampling": "disabled",
                "tdc_latency": 0.0,
                "channel_combine": "fan-out",
            }

            self._bin_out = self._encode_bin(json.dumps(cfg_dict).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_sequencer_state(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get sequencer state.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        sequencer_idx = str(cmd_params[0])
        self._data_out = self._sequencer_status.get(sequencer_idx, "OKAY;IDLE;;;;")

    # ------------------------------------------------------------------------
    def _add_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds waveform to the waveform list of the indexed sequencer's AWG
        path. If the waveform name is already in use, an error is set in
        system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                error = f"Waveform {cmd_args[0]} already in waveform list."
                self._system_error.append(error)
                return

            for index in range(0, len(self._awg_waveforms[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._awg_waveforms[cmd_params[0]]:
                    if self._awg_waveforms[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused is True:
                    break
        else:
            self._awg_waveforms[cmd_params[0]] = {}
            index = 0

        self._awg_waveforms[cmd_params[0]][cmd_args[0]] = {
            "wave": bytearray([]),
            "index": index,
        }

    # ------------------------------------------------------------------------
    def _del_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes waveform from the waveform list of the indexed sequencer's
        AWG path. If the waveform name does not exist, an error is set in
        system error. The names "all" and "ALL" are reserved and those are
        deleted all waveforms in the waveform list of the indexed sequencer's
        AWG path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_args[0].lower() == "all":
            self._awg_waveforms[cmd_params[0]] = {}
        else:
            if (
                cmd_params[0] in self._awg_waveforms
                and cmd_args[0] in self._awg_waveforms[cmd_params[0]]
            ):
                del self._awg_waveforms[cmd_params[0]][cmd_args[0]]
                return
            error = f"Waveform {cmd_args[0]} does not exist in waveform list."
            self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform data for the waveform in the waveform list of the
        indexed sequencer's AWG path. If the waveform name does not exist,
        an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._awg_waveforms
            and cmd_args[0] in self._awg_waveforms[cmd_params[0]]
        ):
            self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
            return
        error = f"Waveform {cmd_args[0]} does not exist in waveform list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform data of the waveform in the waveform list of the indexed
        sequencer's AWG path. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._awg_waveforms
            and cmd_args[0] in self._awg_waveforms[cmd_params[0]]
        ):
            self._bin_out = self._encode_bin(
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"]
            )
            return
        error = f"Waveform {cmd_args[0]} does not exist in waveform list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform index of the waveform in the waveform list of the
        indexed sequencer's AWG path. If the waveform name does not exist or
        the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._awg_waveforms
            and cmd_args[0] in self._awg_waveforms[cmd_params[0]]
        ):
            for name in self._awg_waveforms[cmd_params[0]]:
                if (
                    self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[1]
                    and name != cmd_args[0]
                ):
                    error = f"Waveform index {cmd_args[0]} already in use by {name}."
                    self._system_error.append(error)
                    return
            self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
            return
        error = f"Waveform {cmd_args[0]} does not exist in waveform list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform index of the waveform in the waveform list of the indexed
        sequencer's AWG path. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._awg_waveforms
            and cmd_args[0] in self._awg_waveforms[cmd_params[0]]
        ):
            self._data_out = self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"]
            return
        error = f"Waveform {cmd_args[0]} does not exist in waveform list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform length of the waveform in the waveform list of the
        indexed sequencer's AWG path. The waveform length is returned as the
        number of samples. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._awg_waveforms
            and cmd_args[0] in self._awg_waveforms[cmd_params[0]]
        ):
            self._data_out = int(len(self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"]) / 4)
            return
        error = f"Waveform {cmd_args[0]} does not exist in waveform list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform name of the waveform in the waveform list of the indexed
        sequencer's AWG path. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._awg_waveforms:
            for name in self._awg_waveforms[cmd_params[0]]:
                if self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name
                    return
        error = f"Waveform {cmd_args[0]} does not exist in waveform list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_num_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Number of waveforms in the waveform list of the indexed sequencer's
        AWG path.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._awg_waveforms:
            self._data_out = len(self._awg_waveforms[cmd_params[0]])
        else:
            self._data_out = 0

    # ------------------------------------------------------------------------
    def _get_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get every waveform in the waveform list of the indexed sequencer's
        AWG path.The waveforms are returned in a binary structure.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._awg_waveforms:
            if len(self._awg_waveforms[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True

            self._bin_out = self._encode_bin(
                struct.pack("I", len(self._awg_waveforms[cmd_params[0]])), end_of_line
            )

            for it, name in enumerate(self._awg_waveforms[cmd_params[0]]):
                if it < len(self._awg_waveforms[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(
                    struct.pack("I", int(self._awg_waveforms[cmd_params[0]][name]["index"])),
                    False,
                )
                self._bin_out += self._encode_bin(
                    self._awg_waveforms[cmd_params[0]][name]["wave"], end_of_line
                )
        else:
            self._bin_out = self._encode_bin(struct.pack("I", 0), True)

    # ------------------------------------------------------------------------
    def _add_acq_weight(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds weight to the weight list of the indexed sequencer's acquisition
        path. If the weight name is already in use, an error is set in system
        error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                error = f"Weight {cmd_args[0]} already in weight list."
                self._system_error.append(error)
                return

            for index in range(0, len(self._acq_weights[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._acq_weights[cmd_params[0]]:
                    if self._acq_weights[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused is True:
                    break
        else:
            self._acq_weights[cmd_params[0]] = {}
            index = 0

        self._acq_weights[cmd_params[0]][cmd_args[0]] = {
            "wave": bytearray([]),
            "index": index,
        }

    # ------------------------------------------------------------------------
    def _del_acq_weight(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes weight from the weight list of the indexed sequencer's
        acquisition path. If the weight name does not exist, an error is set
        in system error. The names "all" and "ALL" are reserved and those are
        deleted all weights in the weight list of the indexed sequencer's
        acquisition path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_args[0].lower() == "all":
            self._acq_weights[cmd_params[0]] = {}
        else:
            if (
                cmd_params[0] in self._acq_weights
                and cmd_args[0] in self._acq_weights[cmd_params[0]]
            ):
                del self._acq_weights[cmd_params[0]][cmd_args[0]]
                return
            error = f"Weight {cmd_args[0]} does not exist in weight list."
            self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_weight_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets weight data for the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist, an
        error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights and cmd_args[0] in self._acq_weights[cmd_params[0]]:
            self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
            return
        error = f"Weight {cmd_args[0]} does not exist in weight list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight data of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist, an
        error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights and cmd_args[0] in self._acq_weights[cmd_params[0]]:
            self._bin_out = self._encode_bin(self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"])
            return
        error = f"Weight {cmd_args[0]} does not exist in weight list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_weight_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets weight index of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist or the
        index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights and cmd_args[0] in self._acq_weights[cmd_params[0]]:
            for name in self._acq_weights[cmd_params[0]]:
                if (
                    self._acq_weights[cmd_params[0]][name]["index"] == cmd_args[1]
                    and name != cmd_args[0]
                ):
                    error = f"Weight index {cmd_args[0]} already in use by {name}."
                    self._system_error.append(error)
                    return
            self._acq_weights[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
            return
        error = f"Weight {cmd_args[0]} does not exist in weight list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight index of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist,
        an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights and cmd_args[0] in self._acq_weights[cmd_params[0]]:
            self._data_out = self._acq_weights[cmd_params[0]][cmd_args[0]]["index"]
            return
        error = f"Weight {cmd_args[0]} does not exist in weight list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight length of the weight in the weight list of the indexed
        sequencer's acquisition path. The weight length is returned as the
        number of samples. If the weight name does not exist, an error is set
        in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights and cmd_args[0] in self._acq_weights[cmd_params[0]]:
            self._data_out = int(len(self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"]) / 4)
            return
        error = f"Weight {cmd_args[0]} does not exist in weight list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight name of the weight in the weight list of the indexed sequencer's
        acquisition path. If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights:
            for name in self._acq_weights[cmd_params[0]]:
                if self._acq_weights[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name
                    return
        error = f"Weight {cmd_args[0]} does not exist in weight list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_num_acq_weights(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight name of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist, an
        error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights:
            self._data_out = len(self._acq_weights[cmd_params[0]])
        else:
            self._data_out = 0

    # ------------------------------------------------------------------------
    def _get_acq_weights(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get every weight in the weight list of the indexed sequencer's
        acquisition path. The weights are returned in a binary structure.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_weights:
            if len(self._acq_weights[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True

            self._bin_out = self._encode_bin(
                struct.pack("I", len(self._acq_weights[cmd_params[0]])), end_of_line
            )

            for it, name in enumerate(self._acq_weights[cmd_params[0]]):
                if it < len(self._acq_weights[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(
                    struct.pack("I", int(self._acq_weights[cmd_params[0]][name]["index"])),
                    False,
                )
                self._bin_out += self._encode_bin(
                    self._acq_weights[cmd_params[0]][name]["wave"], end_of_line
                )
        else:
            self._bin_out = self._encode_bin(struct.pack("I", 0), True)

    # ------------------------------------------------------------------------
    def _add_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Add acquisition to acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        def _next_free_acq_index(acq_metadata) -> str:
            index_int = 0
            used_indices = {metadata["index"] for metadata in acq_metadata.values()}
            while str(index_int) in used_indices:
                index_int += 1
            return str(index_int)

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                error = f"Acquisition {cmd_args[0]} already in acquisition list."
                self._system_error.append(error)
                return

            index = _next_free_acq_index(self._acq_metadata[cmd_params[0]])
        else:
            self._acq_acquisitions[cmd_params[0]] = {}
            index = "0"

        if cmd_args[0] not in self._acq_acquisitions[cmd_params[0]]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]] = {}

        if cmd_params[0] not in self._acq_metadata:
            self._acq_metadata[cmd_params[0]] = {}
        if cmd_args[0] not in self._acq_metadata[cmd_params[0]]:
            self._acq_metadata[cmd_params[0]][cmd_args[0]] = {}
        self._acq_metadata[cmd_params[0]][cmd_args[0]]["index"] = index
        self._acq_metadata[cmd_params[0]][cmd_args[0]]["bins"] = int(cmd_args[1])

        if "acq" not in self._acq_acquisitions[cmd_params[0]][cmd_args[0]]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"] = {}
        if "scope" not in self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"] = (
                self._initial_scope_acquisition_data()
            )
        if "bins" not in self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]:
            self._set_initial_binned_acquisition_data(cmd_params[0], cmd_args[0])

    # ------------------------------------------------------------------------
    def _del_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes acquisition (data and index data) from the acquisition list of the indexed
        sequencer. If the acquisition name does not exist, an error is set in
        system error. The names "all" and "ALL" are reserved and those are
        deleted all acquisitions in the acquisition list of the indexed
        sequencer are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0].lower() == "all":
                self._acq_acquisitions[cmd_params[0]] = {}
                self._acq_metadata[cmd_params[0]] = {}
            else:
                if (
                    cmd_args[0] in self._acq_acquisitions[cmd_params[0]]
                    and cmd_args[0] in self._acq_metadata[cmd_params[0]]
                ):
                    del self._acq_acquisitions[cmd_params[0]][cmd_args[0]]
                    del self._acq_metadata[cmd_params[0]][cmd_args[0]]
                    return
                error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
                self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _del_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes acquisition data from the acquisition list of the indexed
        sequencer. If the acquisition name does not exist, an error is set in
        system error. The names "all" and "ALL" are reserved and those are
        deleted all acquisitions in the acquisition list of the indexed
        sequencer are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0].lower() == "all":
                self._set_initial_binned_acquisition_data(cmd_params[0])
            else:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                    self._set_initial_binned_acquisition_data(cmd_params[0], cmd_args[0])
                    return
                error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
                self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds scope acquisition data to the selected acquisition in the
        specified sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._acq_acquisitions
            and cmd_args[0] in self._acq_acquisitions[cmd_params[0]]
        ):
            if self._acq_scope_acquisition is not None:
                self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"] = (
                    self._acq_scope_acquisition
                )
            return
        error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get acquisition data of a single acquisition from the specified
        sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._acq_acquisitions
            and cmd_args[0] in self._acq_acquisitions[cmd_params[0]]
        ):
            self._bin_out = b""
            num_scope_acq_channels = 0
            if self.is_qrm_type or self.is_qtm_type:
                num_scope_acq_channels = 2
            elif self.is_qrc_type:
                num_scope_acq_channels = 4
            for i in range(num_scope_acq_channels):
                self._bin_out += self._encode_bin(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][i],
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack(
                        "?",
                        self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["or"][i],
                    ),
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack(
                        "I",
                        self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"][
                            "avg_cnt"
                        ][i],
                    ),
                    False,
                )

            num_bins = len(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"])
            bins = []
            for bin_it in range(0, num_bins):
                bins.append(
                    int(
                        self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it][
                            "valid"
                        ]
                    )
                )
                bins.append(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it][
                        "int"
                    ][0]
                )
                bins.append(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it][
                        "int"
                    ][1]
                )
                bins.append(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it][
                        "thres"
                    ]
                )
                bins.append(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it][
                        "avg_cnt"
                    ]
                )
            self._bin_out += self._encode_bin(
                struct.pack("=" + num_bins * "QqqLL", *bins),
                True,
            )
            return
        error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_acquisition_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets acquisition index of the acquisition in the acquisition list
        of the indexed sequencer's acquisition path. If the acquisition name
        does not exist or the index is already in use, an error is set in
        system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_metadata and cmd_args[0] in self._acq_metadata[cmd_params[0]]:
            for name, metadata in self._acq_metadata[cmd_params[0]].items():
                index = metadata["index"]
                if index == cmd_args[1] and name != cmd_args[0]:
                    error = f"Acquisition index {cmd_args[0]} already in use by {name}."
                    self._system_error.append(error)
                    return
            self._acq_metadata[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
            return
        error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets acquisition index of the acquisition in the acquisition list of
        the indexed sequencer's acquisition path. If the acquisition name does
        not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_metadata and cmd_args[0] in self._acq_metadata[cmd_params[0]]:
            self._data_out = self._acq_metadata[cmd_params[0]][cmd_args[0]]["index"]
            return
        error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_num_bins(
        self, cmd_params: list, cmd_args: list, bin_in: bytes
    ) -> None:
        """
        Get number of bins of the acquisition in the specified sequencer's
        acquisition list. If the acquisition name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if (
            cmd_params[0] in self._acq_acquisitions
            and cmd_args[0] in self._acq_acquisitions[cmd_params[0]]
        ):
            self._data_out = int(len(self._acq_acquisitions[cmd_params[0]]["acq"]["bins"]))
            return
        error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets acquisition name of the acquisition in the acquisition list of
        the indexed sequencer's acquisition path. If the acquisition name does
        not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_metadata:
            for name, metadata in self._acq_metadata[cmd_params[0]].items():
                if str(metadata["index"]) == cmd_args[0]:
                    self._data_out = name
                    return
        error = f"Acquisition {cmd_args[0]} does not exist in acquisition list."
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_num_acq_acquisitions(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of acquisitions in the specified sequencer's acquisition
        list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._data_out = 0
        if cmd_params[0] in self._acq_acquisitions:
            self._data_out = len(self._acq_acquisitions[cmd_params[0]])
            return

    # ------------------------------------------------------------------------
    def _get_acq_acquisitions(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Return all acquisitions in the specified sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if cmd_params[0] in self._acq_acquisitions:
            if len(self._acq_acquisitions[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True

            self._bin_out = self._encode_bin(
                struct.pack("I", len(self._acq_acquisitions[cmd_params[0]])),
                end_of_line,
            )

            for it, name in enumerate(self._acq_acquisitions[cmd_params[0]]):
                if it < len(self._acq_acquisitions[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(
                    struct.pack("I", int(self._acq_metadata[cmd_params[0]][name]["index"])),
                    False,
                )

                num_scope_acq_channels = 0
                if self.is_qrm_type or self.is_qtm_type:
                    num_scope_acq_channels = 2
                elif self.is_qrc_type:
                    num_scope_acq_channels = 4
                for i in range(num_scope_acq_channels):
                    self._bin_out += self._encode_bin(
                        self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["data"][i],
                        False,
                    )
                    self._bin_out += self._encode_bin(
                        struct.pack(
                            "?",
                            self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["or"][i],
                        ),
                        False,
                    )
                    self._bin_out += self._encode_bin(
                        struct.pack(
                            "I",
                            self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["avg_cnt"][
                                i
                            ],
                        ),
                        False,
                    )

                num_bins = len(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"])
                bins = []
                for bin_it in range(num_bins):
                    bins += [
                        int(
                            self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it][
                                "valid"
                            ]
                        ),
                        self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["int"][
                            0
                        ],
                        self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["int"][
                            1
                        ],
                        self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["thres"],
                        self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it][
                            "avg_cnt"
                        ],
                    ]
                self._bin_out += self._encode_bin(
                    struct.pack("=" + num_bins * "QqqLL", *bins), end_of_line
                )
        else:
            self._bin_out = self._encode_bin(struct.pack("I", 0), True)

    # ------------------------------------------------------------------------
    def _set_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the channelmap list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        self._channelmap[cmd_params[0]] = json.loads(self._decode_bin(bin_in).decode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the channelmap list. If not set previously, returns an empty list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        self._bin_out = self._encode_bin(
            json.dumps(self._channelmap[cmd_params[0]]).encode("utf-8")
        )

    # ------------------------------------------------------------------------
    def _set_acq_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the acquisition channelmap list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        self._acq_channelmap[cmd_params[0]] = json.loads(self._decode_bin(bin_in).decode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_acq_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the acquisition channelmap list. If not set previously, returns an empty list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        self._bin_out = self._encode_bin(
            json.dumps(self._acq_channelmap[cmd_params[0]]).encode("utf-8")
        )

    # ------------------------------------------------------------------------
    def _arm(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Arms the sequencer.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        sequencer_idx = str(cmd_params[0])
        self._sequencer_status[sequencer_idx] = "OKAY;ARMED;;;;"

    # ------------------------------------------------------------------------
    def _start(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Starts the sequencer.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        sequencer_idx = cmd_params[0]
        sequencer_idx_str = str(sequencer_idx)
        if sequencer_idx_str in self._acq_acquisitions_dummy:
            self._acq_acquisitions[sequencer_idx_str] = deepcopy(
                self._acq_acquisitions_dummy[sequencer_idx_str]
            )
        self._acq_scope_acquisition = deepcopy(self._acq_scope_acquisition_dummy)
        self._sequencer_status[sequencer_idx_str] = "OKAY;STOPPED;ACQ_BINNING_DONE,;;;"

    # ------------------------------------------------------------------------
    def _stop(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stops the sequencer.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        sequencer_idx = str(cmd_params[0])
        self._sequencer_status[sequencer_idx] = "OKAY;STOPPED;ACQ_BINNING_DONE,;;;"

    # ------------------------------------------------------------------------
    def _set_out_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the output attenuation.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["out_att"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_out_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the output attenuation. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("out_att", 0)

    # ------------------------------------------------------------------------
    def _set_out_att_indexed(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the output attenuation.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        sm_channel = cmd_args[0]
        att_value = float(cmd_args[1])
        self._out_att_indexed[sm_channel] = att_value
        self._bin_out = self._encode_bin(json.dumps("Ok").encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_out_att_indexed(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the output attenuation.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        sm_channel = cmd_args[0]
        self._data_out = self._out_att_indexed.get(sm_channel, 0.0)

    # ------------------------------------------------------------------------
    def _get_max_out_att_indexed(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the output attenuation.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        self._data_out = 31.5

    # ------------------------------------------------------------------------
    def _set_in_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the input attenuation.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"in{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["in_att"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_max_out_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the maximum possible output attenuation. Returns 60 by default.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        # key = f"out{cmd_params[0]}"
        # port = self._port_cfg.get(key, {})
        self._data_out = 60

    # ------------------------------------------------------------------------
    def _get_in_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the input attenuation. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"in{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("in_att", 0)

    # ------------------------------------------------------------------------
    def _set_lo_enable(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the LO status

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["lo_ena"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_lo_enable(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the LO status. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("lo_ena", 0)

    # ------------------------------------------------------------------------
    def _set_lo_freq(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the LO frequency

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["lo_freq"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_lo_freq(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the LO frequency. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("lo_freq", 0)

    # ------------------------------------------------------------------------
    def _set_out_amp_offset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the output amplifier offset

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["amp_offs"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_out_amp_offset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the output amplifier offset. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("amp_offs", 0)

    # ------------------------------------------------------------------------
    def _set_dac_offset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the DAC offset

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["dac_offs"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_dac_offset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the DAC offset. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("dac_offs", 0)

    # ------------------------------------------------------------------------
    def _set_in_amp_gain(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the input amplifier gain

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"in{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["amp_gain"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_in_amp_gain(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the input amplifier gain. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"in{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("amp_gain", 0)

    # ------------------------------------------------------------------------
    def _set_lo_pwr(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the LO power

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["lo_pwr"] = cmd_args[0]
        self._port_cfg[key] = port

    # ------------------------------------------------------------------------
    def _get_lo_pwr(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the LO power If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("lo_pwr", 0)

    # ------------------------------------------------------------------------
    def _initial_scope_acquisition_data(self) -> dict[str, list]:
        if self.is_qrm_type or self.is_qtm_type:
            return {
                "data": [bytearray([]), bytearray([])],
                "or": [False, False],
                "avg_cnt": [0, 0],
            }
        elif self.is_qrc_type:
            return {
                "data": [bytearray([]), bytearray([]), bytearray([]), bytearray([])],
                "or": [False, False, False, False],
                "avg_cnt": [0, 0, 0, 0],
            }

    # ------------------------------------------------------------------------
    def _set_initial_binned_acquisition_data(
        self, sequencer: int, acq_index_name: Optional[str] = None
    ) -> None:
        """
        Sets initial binned acquisition data.
        It will add as many invalid, 0 values for the acquisition index as set by the sequence.

        Parameters
        ----------
        sequencer : int
            Sequencer.
        acq_index_name : Optional[str]
            Command arguments.
        """

        def _set_initial_for_index(sequencer, name, bins) -> None:
            self._acq_acquisitions[sequencer][name]["acq"]["bins"] = [
                {"valid": False, "int": [0, 0], "thres": 0, "avg_cnt": 0}
            ] * bins

        if sequencer in self._acq_metadata:
            if acq_index_name is None:
                for name, acq_metadata in self._acq_metadata[sequencer].items():
                    bins = acq_metadata["bins"]
                    _set_initial_for_index(sequencer, name, bins)
            elif acq_index_name in self._acq_metadata[sequencer]:
                bins = self._acq_metadata[sequencer][acq_index_name]["bins"]
                _set_initial_for_index(sequencer, acq_index_name, bins)

    # ------------------------------------------------------------------------
    def _get_current_timestamp(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves current timestamp

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if "ns" in self._current_timestamp:
            self._bin_out = self._encode_bin(self._current_timestamp)
        else:
            self._current_timestamp = {"ns": 0, "sub": 0}
            self._bin_out = self._encode_bin(json.dumps(self._current_timestamp).encode("utf-8"))

    # ------------------------------------------------------------------------
    def _get_timekeeping_capture(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get capture value after capture had been armed.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if "ns" in self._current_capture:
            self._bin_out = self._encode_bin(self._current_capture)
        else:
            cfg_dict = {"ns": 0, "sub": 0}
            self._bin_out = self._encode_bin(json.dumps(cfg_dict).encode("utf-8"))
