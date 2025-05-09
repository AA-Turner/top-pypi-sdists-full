# SPDX-FileCopyrightText: 2013 SAP SE Srdjan Boskovic <srdjan.boskovic@sap.com>
#
# SPDX-License-Identifier: Apache-2.0

""":mod:`pyrfc`-specific exception classes."""

from enum import Enum, auto

from pyrfc._utils import enum_values


class RFCError(Exception):
    """Exception base class.

    Indicates that there was an error in the Python connector.
    """


class RFCLibError(RFCError):
    """RFC library error.

    Base class for exceptions raised by the local underlying C connector (sapnwrfc.c).
    """

    def __init__(
        self,
        message=None,
        code=None,
        key=None,
        msg_class=None,
        msg_type=None,
        msg_number=None,
        msg_v1=None,
        msg_v2=None,
        msg_v3=None,
        msg_v4=None,
    ):
        """Init RFCLibError class."""
        super(RFCLibError, self).__init__(message)
        self.message = message  # Exception.message removed in Py3
        self.code = code
        self.key = key
        self.msg_class = msg_class
        self.msg_type = msg_type
        self.msg_number = msg_number
        self.msg_v1 = msg_v1
        self.msg_v2 = msg_v2
        self.msg_v3 = msg_v3
        self.msg_v4 = msg_v4

    def __str__(self):
        """Convert RFCLibError object to string."""
        code = 28 if self.code is None else self.code  # 28 = RFC_UNKNOWN_ERROR
        rc_text = RcCodeText(code).value if code in enum_values(RcCodeText) else "??"
        return (
            f"{rc_text} (rc={self.code}): key={self.key}, message={self.message}"
            f" [MSG: class={self.msg_class}, type={self.msg_type}, number={self.msg_number},"
            f" v1-4:={self.msg_v1};{self.msg_v2};{self.msg_v3};{self.msg_v4}]"
        )


class ABAPApplicationError(RFCLibError):
    """ABAP application error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    ABAP_APPLICATION_FAILURE.
    """


class ABAPRuntimeError(RFCLibError):
    """ABAP runtime error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    ABAP_RUNTIME_FAILURE.
    """


class LogonError(RFCLibError):
    """Logon error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    LOGON_FAILURE.
    """

    def __init__(
        self,
        message=None,
        code=2,
        key="RFC_LOGON_FAILURE",
        msg_class=None,
        msg_type=None,
        msg_number=None,
        msg_v1=None,
        msg_v2=None,
        msg_v3=None,
        msg_v4=None,
    ):
        """Init LogonError."""
        # Setting default values allows for raising an error with one parameter.
        super(LogonError, self).__init__(
            message,
            code,
            key,
            msg_class,
            msg_type,
            msg_number,
            msg_v1,
            msg_v2,
            msg_v3,
            msg_v4,
        )


class CommunicationError(RFCLibError):
    """Communication error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    COMMUNICATION_FAILURE.
    """


class ExternalRuntimeError(RFCLibError):
    """External runtime error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    EXTERNAL_RUNTIME_FAILURE.
    """


class ExternalApplicationError(RFCLibError):
    """External application error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    EXTERNAL_APPLICATION_FAILURE.
    """


class ExternalAuthorizationError(RFCLibError):
    """External authorization error.

    This exception is raised if a RFC call returns an RC code greater than 0
    and the error object has an RFC_ERROR_GROUP value of
    EXTERNAL_AUTHORIZATION_FAILURE.
    """


class RFCTypeError(RFCLibError):
    """Type concersion error.

    This exception is raised when invalid data type detected in RFC input (fill) conversion
    and the error object has an RFC_ERROR_GROUP value of
    RFC_TYPE_ERROR
    """


class RcCodeText(Enum):
    """RFC library return codes."""

    RFC_OK = auto()
    RFC_COMMUNICATION_FAILURE = auto()
    RFC_LOGON_FAILURE = auto()
    RFC_ABAP_RUNTIME_FAILURE = auto()
    RFC_ABAP_MESSAGE = auto()
    RFC_ABAP_EXCEPTION = auto()
    RFC_CLOSED = auto()
    RFC_CANCELED = auto()
    RFC_TIMEOUT = auto()
    RFC_MEMORY_INSUFFICIENT = auto()
    RFC_VERSION_MISMATCH = auto()
    RFC_INVALID_PROTOCOL = auto()
    RFC_SERIALIZATION_FAILURE = auto()
    RFC_INVALID_HANDLE = auto()
    RFC_RETRY = auto()
    RFC_EXTERNAL_FAILURE = auto()
    RFC_EXECUTED = auto()
    RFC_NOT_FOUND = auto()
    RFC_NOT_SUPPORTED = auto()
    RFC_ILLEGAL_STATE = auto()
    RFC_INVALID_PARAMETER = auto()
    RFC_CODEPAGE_CONVERSION_FAILURE = auto()
    RFC_CONVERSION_FAILURE = auto()
    RFC_BUFFER_TOO_SMALL = auto()
    RFC_TABLE_MOVE_BOF = auto()
    RFC_TABLE_MOVE_EOF = auto()
    RFC_START_SAPGUI_FAILURE = auto()
    RFC_ABAP_CLASS_EXCEPTION = auto()
    RFC_UNKNOWN_ERROR = auto()
    RFC_AUTHORIZATION_FAILURE = auto()
    RFC_AUTHENTICATION_FAILURE = auto()
    RFC_CRYPTOLIB_FAILURE = auto()
    RFC_IO_FAILURE = auto()
    RFC_LOCKING_FAILURE = auto()
