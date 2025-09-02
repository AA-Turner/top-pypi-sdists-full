# ----------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import abc
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Optional, Union

from qblox_instruments import ClusterType, TypeHandle
from qblox_instruments.ieee488_2 import Transport

# -- class -------------------------------------------------------------------


@dataclass
class DummyBinnedAcquisitionData:
    """
    Class to hold data for the dummy hardware for the binned acquisition.
    This class contains all values for one bin.
    """

    data: tuple[float, float]
    thres: int
    avg_cnt: int


# -- class -------------------------------------------------------------------


@dataclass
class DummyScopeAcquisitionData:
    """
    Class to hold data for the dummy hardware for the scope acquisition.
    This class contains all values for the scope acquisition on one module.
    """

    data: Iterable[tuple[float, float]]
    out_of_range: tuple[bool, bool]
    avg_cnt: tuple[int, int]


# -- class -------------------------------------------------------------------


class DummyTransport(abc.ABC, Transport):
    """
    Class to replace device with dummy device to support software stack
    testing without hardware. The class implements all mandatory and required
    SCPI calls. Call responses are largely artificially constructed to be inline
    with the call's functionality (e.g. `*IDN?` returns valid, but artificial
    IDN data.)
    """

    # ------------------------------------------------------------------------
    def __init__(self, dummy_type: ClusterType) -> None:
        """
        Create dummy transport class.

        Parameters
        ----------
        dummy_type : ClusterType
            Dummy instrument type
        """

        # Set instrument type handle
        self._type_handle = TypeHandle(dummy_type)

        # Initialize variables
        self._cmd_hist = []
        self._data_out = 0
        self._bin_out = None
        self._system_error = []

        # Set command dictionary
        self._cmds = {
            "*CMDS?": self._get_cmds,
            "*IDN?": self._get_idn,
            "*RST": self._reset,
            "SYSTem:ERRor:NEXT?": self._get_system_error,
            "SYSTem:ERRor:COUNt?": self._get_system_error_cnt,
            "STATus:GENeral:STATE?": self._get_system_state,
        }

    # ------------------------------------------------------------------------
    @property
    def instrument_class(self) -> str:
        """
        Get instrument class (e.g. Cluster).

        Returns
        ----------
        str
            Instrument class
        """

        return self._type_handle.instrument_class

    # ------------------------------------------------------------------------
    @property
    def instrument_type(self) -> str:
        """
        Get instrument type (e.g. MM, QRM, QCM).

        Returns
        ----------
        str
            Instrument type
        """

        return self._type_handle.instrument_type

    # ------------------------------------------------------------------------
    def close(self) -> None:
        """
        Close and resets base dummy transport class.
        """

        self._cmd_hist = []
        self._data_out = 0
        self._bin_out = None
        self._system_error = []

    # ------------------------------------------------------------------------
    def write(self, cmd_str: str) -> None:
        """
        Write command to dummy. Stores command in command history.

        Parameters
        ----------
        cmd_str : str
            Command
        """

        cmd_parts, cmd_params, cmd_args = self._parse_cmd(cmd_str)
        self._execute_cmd(cmd_parts, cmd_params, cmd_args)

    # ------------------------------------------------------------------------
    def write_binary(self, data: bytes) -> None:
        """
        Write binary data to dummy. Stores command in command history.

        Parameters
        ----------
        data : bytes
            Binary data
        """

        cmd_parts = data.split(b"#")
        cmd_str = cmd_parts[0].decode()
        bin_in = b"#" + b"#".join(cmd_parts[1:])

        cmd_parts, cmd_params, cmd_args = self._parse_cmd(cmd_str)
        self._execute_cmd(cmd_parts, cmd_params, cmd_args, bin_in)

    # ------------------------------------------------------------------------
    def read_binary(self, size: int) -> bytes:
        """
        Read binary data from dummy.

        Parameters
        ----------
        size : int
            Number of bytes

        Returns
        ----------
        bytes
            Binary data array of length "size".
        """

        bin_var = self._bin_out[:size]
        self._bin_out = self._bin_out[size:]
        return bin_var

    # ------------------------------------------------------------------------
    def readline(self) -> str:
        """
        Read data from dummy.

        Returns
        ----------
        str
            String with data.
        """

        return str(self._data_out)

    # ------------------------------------------------------------------------
    @abc.abstractmethod
    def delete_dummy_binned_acquisition_data(
        self, sequencer: Optional[int] = None, acq_index_name: Optional[str] = None
    ) -> None:
        """
        Delete all dummy binned acquisition data for the dummy.

        Parameters
        ----------
        sequencer : Optional[int]
            Sequencer.
        acq_index_name : Optional[str]
            Acquisition index name.

        Raises
        ----------
        ValueError
            If the slot_idx doesn't make sense for the transport.
        """

        pass

    # ------------------------------------------------------------------------
    @abc.abstractmethod
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

        Raises
        ----------
        ValueError
            If the slot_idx doesn't make sense for the transport.
        """

        pass

    # ------------------------------------------------------------------------
    @abc.abstractmethod
    def delete_dummy_scope_acquisition_data(self) -> None:
        """
        Delete dummy scope acquisition data for the dummy.

        Raises
        ----------
        ValueError
            If the slot_idx doesn't make sense for the transport.
        """

        pass

    # ------------------------------------------------------------------------
    @abc.abstractmethod
    def set_dummy_scope_acquisition_data(self, data: DummyScopeAcquisitionData) -> None:
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.

        Raises
        ----------
        ValueError
            If the slot_idx doesn't make sense for the transport.
        """

        pass

    # ------------------------------------------------------------------------
    def _parse_cmd(self, cmd_str: str) -> tuple[list, list, list]:
        """
        Parse command and split it into command, parameters and arguments. The
        command is stored in the command history
        (see :func:`~.qblox_instruments.ieee488_2.DummyTransport.get_cmd_hist`).

        Parameters
        ----------
        cmd_str : str
            Command

        Returns
        ----------
        list
            Reformatted command sections
        list
            Command parameters
        list
            Command arguments
        """

        # Create command part list
        # Substitute command parameters with #
        cmd_list = cmd_str.split(" ")
        cmd_sub = re.sub("[0-9]+", "#", cmd_list[0])
        cmd_parts = cmd_sub.split(":")

        # Get all command parameters
        cmd_params = re.findall("[0-9]+", cmd_list[0])

        # Get all command arguments
        # Remove any " characters
        cmd_args = cmd_list[1].split(",") if len(cmd_list) > 1 else []
        cmd_args = [arg.strip('"') for arg in cmd_args]

        # Append command to command history
        self._cmd_hist.append(cmd_sub)

        return cmd_parts, cmd_params, cmd_args

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

        cmd_str = ":".join(cmd_parts)
        if cmd_str in self._cmds:
            self._cmds[cmd_str](cmd_params, cmd_args, bin_in)
        else:
            self._data_out = 0
            self._bin_out = self._encode_bin(b"0")

    # ------------------------------------------------------------------------
    @staticmethod
    def _encode_bin(data: bytes, end_of_line: bool = True) -> bytes:
        """
        Encode binary data to be compatible with IEEE488.2.

        Parameters
        ----------
        data : bytes
            Binary data.
        end_of_line: bool
            Indicates if end-of-line needs to be added.

        Returns
        ----------
        bytes
            Encoded data.
        """

        header_b = str(len(data)).encode()
        header_a = ("#" + str(len(header_b))).encode()
        if end_of_line:
            out = header_a + header_b + data + b"\r\n"
        else:
            out = header_a + header_b + data

        return out

    # ------------------------------------------------------------------------
    @staticmethod
    def _decode_bin(data: bytes) -> bytes:
        """
        Decode IEEE488.2 binary data.

        Parameters
        ----------
        data : bytes
            Binary data.

        Raises
        ----------
        RunTimeError
            Header error.
        """

        header_a = data[:2].decode()  # Read '#N'
        data = data[2:]

        if header_a[0] != "#":
            raise RuntimeError(f"Header error: received {header_a}")
        header_b = data[: int(header_a[1])].decode()
        data = data[int(header_a[1]) :]

        return data[: int(header_b)]

    # ------------------------------------------------------------------------
    def get_cmd_hist(self) -> list:
        """
        Get list of every executed command since the initialization or reset
        of the class.

        Returns
        ----------
        list
            List of executed command strings including arguments (does not
            include binary data argument).
        """

        return self._cmd_hist

    # ------------------------------------------------------------------------
    def _get_cmds(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get SCPI commands.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._data_out = (
            "THe:CAke:Is:A:LIe;"
            "cake;"
            "str;"
            "get_cake;"
            "lie;"
            "cake;"
            "str;"
            "0;"
            "Your trusty AI companion promised you a cake.;"
        )

    # ------------------------------------------------------------------------
    def _get_idn(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get device identity and build information.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._data_out = (
            f"Qblox,{self.instrument_class} {self.instrument_type},whatever,"
            f"fwVersion=0.0.0 fwBuild=28/11/1967-00:00:00 fwHash=0xDEADBEAF fwDirty=0 "
            f"kmodVersion=0.0.0 kmodBuild=15/07/1943-00:00:00 kmodHash=0x0D15EA5E kmodDirty=0 "
            f"swVersion=0.0.0 swBuild=11/05/1924-00:00:00 swHash=0xBEEFBABE swDirty=0"
        )

    # ------------------------------------------------------------------------
    def _reset(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Reset dummy.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self.close()

    # ------------------------------------------------------------------------
    def _get_system_error(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get system error from queue (see
        `SCPI <https://www.ivifoundation.org/downloads/SCPI/scpi-99.pdf>`_).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        if len(self._system_error) > 0:
            self._data_out = "0," + self._system_error[0]
            self._system_error = self._system_error[1:]
        else:
            self._data_out = "No error"

    # ------------------------------------------------------------------------
    def _get_system_error_cnt(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of system errors (see
        `SCPI <https://www.ivifoundation.org/downloads/SCPI/scpi-99.pdf>`_).

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.
        """

        self._data_out = str(len(self._system_error))

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

        self._data_out = "RESOLVED;TEMPERATURE OUT-OF-RANGE,"
