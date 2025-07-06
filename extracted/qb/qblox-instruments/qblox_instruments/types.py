# ----------------------------------------------------------------------------
# Description    : Qblox instruments instrument and module types
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import re
from enum import Enum, IntEnum
from typing import Any, Union

from qcodes import DelegateParameter

# -- definitions -------------------------------------------------------------


class DebugLevel(IntEnum):
    """Debug level for communication with the instrument."""

    MINIMAL_CHECK = 0
    """
    Check for version mismatch between qblox-instruments and the firmware.
    Perform a system error check only when starting or stopping sequencers.
    """
    ERROR_CHECK = 1
    """Do not check for a version mismatch. Perform an error check on every SCPI call."""
    NO_CHECK = 2
    """Do not check for a version mismatch or system errors."""
    VERSION_AND_ERROR_CHECK = 3
    """
    Check for version mismatch between qblox-instruments and the firmware. Perform an
    error check on every SCPI call.
    """


class TypeEnum(Enum):
    """
    Type base class that arranges child enum string representations.
    """

    def __repr__(self) -> str:
        return "<{}.{}>".format(str(type(self)).split("'")[1], self.name)

    def __str__(self) -> str:
        return str(self.value)

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


class InstrumentClass(TypeEnum):
    """
    Instrument class enum.
    """

    CLUSTER = "Cluster"


class InstrumentType(TypeEnum):
    """
    Instrument/module type enum.
    """

    MM = "MM"
    QCM = "QCM"
    QRM = "QRM"
    QTM = "QTM"
    QDM = "QDM"
    LINQ = "LINQ"
    QRC = "QRC"
    QSM = "QSM"
    _RF = "RF"
    _EOM = "EOM"


class ClusterType(TypeEnum):
    """
    Cluster module type enum.
    """

    _CLUSTER_MM = "Cluster MM"
    CLUSTER_QCM = "Cluster QCM"
    CLUSTER_QCM_RF = "Cluster QCM-RF"
    CLUSTER_QRM = "Cluster QRM"
    CLUSTER_QRM_RF = "Cluster QRM-RF"
    CLUSTER_QTM = "Cluster QTM"
    CLUSTER_QTM_EOM = "Cluster QTM-Pulse"
    CLUSTER_QDM = "Cluster QDM"
    CLUSTER_LINQ = "Cluster LINQ"
    CLUSTER_QRC = "Cluster QRC"
    CLUSTER_QSM = "Cluster QSM"


# -- class -------------------------------------------------------------------
class TypeHandle:
    """
    Instrument type handler class.
    """

    # ------------------------------------------------------------------------
    def __init__(self, instrument: Union[ClusterType, str]) -> None:
        """
        Create instrument type handler object.

        Parameters
        ----------
        instrument : Union[ClusterType, str]
            Instrument/module type specification.
        """

        # Set instrument type specification
        try:
            instrument = (
                instrument.name.removeprefix("_")
                if isinstance(instrument, Enum)
                else instrument.upper()
            )
            instrument = re.split(" |_|-", instrument)
            self._instrument_class = InstrumentClass[instrument[0]]
            self._instrument_type = InstrumentType[instrument[1]]

            self._is_mm_type = self._instrument_type == InstrumentType.MM
            self._is_qrm_type = self._instrument_type == InstrumentType.QRM
            self._is_qcm_type = self._instrument_type == InstrumentType.QCM
            self._is_qtm_type = self._instrument_type == InstrumentType.QTM
            self._is_qdm_type = self._instrument_type == InstrumentType.QDM
            self._is_linq_type = self._instrument_type == InstrumentType.LINQ
            self._is_qrc_type = self._instrument_type == InstrumentType.QRC
            self._is_qsm_type = self._instrument_type == InstrumentType.QSM
        except Exception:
            raise RuntimeError("Invalid instrument type.")

        # Do a first RF assignment.
        # It is necessary for dummy modules but will get overwritten for real ones.
        self._is_rf_type = False
        self._is_eom_type = False

        if len(instrument) > 2:
            self._is_rf_type = instrument[2] == str(InstrumentType._RF)
            self._is_eom_type = instrument[2] == str(InstrumentType._EOM)
            if not (self._is_rf_type or self._is_eom_type):
                raise RuntimeError("Invalid instrument type.")
        # Add QRC to RF types
        self._is_rf_type |= self._is_qrc_type

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

        return self._instrument_class

    # ------------------------------------------------------------------------
    @property
    def instrument_type(self) -> InstrumentType:
        """
        Get instrument type (e.g. MM, QRM, QCM, QTM).

        Returns
        ----------
        InstrumentType
            Instrument type
        """

        return self._instrument_type

    # ------------------------------------------------------------------------
    @property
    def is_mm_type(self) -> bool:
        """
        Return if module is of type MM.

        Returns
        ----------
        bool
            True if module is of type MM.
        """

        return self._is_mm_type

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

        return self._is_qcm_type

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

        return self._is_qrm_type

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

        return self._is_qtm_type

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

        return self._is_qdm_type

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
        return self._is_eom_type

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

        return self._is_linq_type

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

        return self._is_qrc_type

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

        return self._is_qsm_type

    # ------------------------------------------------------------------------
    @property
    def is_rf_type(self) -> bool:
        """
        Return if has RF functionality.

        Returns
        ----------
        bool
            True if module has RF functionality.
        """

        return self._is_rf_type


class FrequencyParameter(DelegateParameter):
    def __init__(self, *args, calibration_function, **kwargs) -> None:
        self._calibration_function = calibration_function
        super().__init__(*args, **kwargs)

    def set_raw(self, val, cal_type=None) -> None:
        self.source.set(val)
        self._calibration_function(cal_type=cal_type)
