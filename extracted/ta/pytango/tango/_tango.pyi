from __future__ import annotations

import collections.abc
import enum
import typing

import tango
from tango import constants

from . import _telemetry

__all__: list[str] = [
    "AccessControlType",
    "ApiUtil",
    "ArchiveEventInfo",
    "ArchiveEventProp",
    "AsynCall",
    "AsynReplyNotArrived",
    "AttReqType",
    "Attr",
    "AttrConfEventData",
    "AttrDataFormat",
    "AttrMemorizedType",
    "AttrProperty",
    "AttrQuality",
    "AttrReadEvent",
    "AttrSerialModel",
    "AttrWriteType",
    "AttrWrittenEvent",
    "Attribute",
    "AttributeAlarm",
    "AttributeAlarmInfo",
    "AttributeConfig",
    "AttributeConfig_2",
    "AttributeConfig_3",
    "AttributeConfig_5",
    "AttributeDimension",
    "AttributeEventInfo",
    "AttributeInfo",
    "AttributeInfoEx",
    "AttributeInfoList",
    "AttributeInfoListEx",
    "AutoTangoAllowThreads",
    "AutoTangoMonitor",
    "ChangeEventInfo",
    "ChangeEventProp",
    "ClientAddr",
    "CmdArgType",
    "CmdDoneEvent",
    "CommandInfo",
    "CommandInfoList",
    "CommunicationFailed",
    "Connection",
    "ConnectionFailed",
    "ConstDevString",
    "DServer",
    "DataReadyEventData",
    "Database",
    "DbData",
    "DbDatum",
    "DbDevExportInfo",
    "DbDevExportInfos",
    "DbDevFullInfo",
    "DbDevImportInfo",
    "DbDevImportInfos",
    "DbDevInfo",
    "DbDevInfos",
    "DbHistory",
    "DbHistoryList",
    "DbServerData",
    "DbServerInfo",
    "DevBoolean",
    "DevCommandInfo",
    "DevDouble",
    "DevEncoded",
    "DevEnum",
    "DevError",
    "DevFailed",
    "DevFloat",
    "DevIntrChangeEventData",
    "DevLong",
    "DevLong64",
    "DevShort",
    "DevSource",
    "DevState",
    "DevString",
    "DevUChar",
    "DevULong",
    "DevULong64",
    "DevUShort",
    "DevVarBooleanArray",
    "DevVarCharArray",
    "DevVarDoubleArray",
    "DevVarDoubleStringArray",
    "DevVarEncodedArray",
    "DevVarFloatArray",
    "DevVarLong64Array",
    "DevVarLongArray",
    "DevVarLongStringArray",
    "DevVarShortArray",
    "DevVarStateArray",
    "DevVarStringArray",
    "DevVarULong64Array",
    "DevVarULongArray",
    "DevVarUShortArray",
    "DevVoid",
    "DeviceAttribute",
    "DeviceAttributeConfig",
    "DeviceAttributeHistory",
    "DeviceClass",
    "DeviceData",
    "DeviceDataHistory",
    "DeviceDataHistoryList",
    "DeviceDataList",
    "DeviceImpl",
    "DeviceInfo",
    "DeviceProxy",
    "DeviceUnlocked",
    "Device_2Impl",
    "Device_3Impl",
    "Device_4Impl",
    "Device_5Impl",
    "Device_6Impl",
    "DispLevel",
    "EncodedAttribute",
    "EnsureOmniThread",
    "ErrSeverity",
    "EventData",
    "EventDataList",
    "EventProperties",
    "EventReason",
    "EventSubMode",
    "EventSystemFailed",
    "EventType",
    "Except",
    "ExtractAs",
    "FMT_UNKNOWN",
    "FwdAttr",
    "GreenMode",
    "GroupAttrReply",
    "GroupAttrReplyList",
    "GroupCmdReply",
    "GroupCmdReplyList",
    "GroupReply",
    "GroupReplyList",
    "IMAGE",
    "ImageAttr",
    "Interceptors",
    "KeepAliveCmdCode",
    "Level",
    "LevelLevel",
    "LockCmdCode",
    "LockerInfo",
    "LockerLanguage",
    "LogLevel",
    "LogTarget",
    "Logger",
    "Logging",
    "MessBoxType",
    "MultiAttribute",
    "MultiClassAttribute",
    "NamedDevFailed",
    "NamedDevFailedList",
    "NonDbDevice",
    "NonSupportedFeature",
    "NotAllowed",
    "PeriodicEventInfo",
    "PeriodicEventProp",
    "PollCmdCode",
    "PollDevice",
    "PollObjType",
    "READ",
    "READ_WITH_WRITE",
    "READ_WRITE",
    "SCALAR",
    "SPECTRUM",
    "SerialModel",
    "SpectrumAttr",
    "StdDoubleVector",
    "StdLongVector",
    "StdNamedDevFailedVector",
    "StdStringVector",
    "SubDevDiag",
    "TimeVal",
    "Unknown",
    "UserDefaultAttrProp",
    "UserDefaultFwdAttrProp",
    "Util",
    "WAttribute",
    "WRITE",
    "WT_UNKNOWN",
    "WrongData",
    "WrongNameSyntax",
    "alarm_flags",
    "asyn_req_type",
    "cb_sub_model",
    "constants",
    "is_omni_thread",
    "raise_asynch_exception",
]

class AccessControlType(enum.IntEnum):
    """An enumeration representing the AccessControlType

    New in PyTango 7.0.0
    """

    ACCESS_READ: typing.ClassVar[
        AccessControlType
    ]  # value = <AccessControlType.ACCESS_READ: 0>
    ACCESS_WRITE: typing.ClassVar[
        AccessControlType
    ]  # value = <AccessControlType.ACCESS_WRITE: 1>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class ApiUtil:
    """This class allows you to access the tango synchronization model API.
    It is designed as a singleton. To get a reference to the singleton object
    you must do:

        import tango
        apiutil = tango.ApiUtil.instance()

    New in PyTango 7.1.3

    """
    @staticmethod
    def cleanup() -> None:
        """cleanup() -> None

            Destroy the ApiUtil singleton instance.
            After calling cleanup(), any existing DeviceProxy, AttributeProxy,
            or Database objects become invalid and must be reconstructed.

        :return: None

        New in PyTango 9.3.0
        """
    @staticmethod
    def get_env_var(name: str) -> typing.Any:
        """get_env_var(name) -> str

            Return the environment variable for the given name.

        :param name: Environment variable name
        :type name: str

        :return: The value of the environment variable
        :rtype: str
        """
    @staticmethod
    def instance() -> ApiUtil:
        """instance() -> ApiUtil

            Returns the ApiUtil singleton instance.

        :return: (ApiUtil) a reference to the ApiUtil singleton object.

        New in PyTango 7.1.3
        """
    def get_asynch_cb_sub_model(self) -> cb_sub_model:
        """get_asynch_cb_sub_model(self) -> cb_sub_model

            Get the asynchronous callback sub-model.

        :return: the active asynchronous callback sub-model
        :rtype: cb_sub_model

        New in PyTango 7.1.3
        """
    @typing.overload
    def get_asynch_replies(self) -> None:
        """get_asynch_replies(self) -> None

            Fire callback methods for all asynchronous requests (command and attribute)
            which already have arrived replies. Returns immediately if no replies arrived
            or there are no asynchronous requests.

        :return: None

        Throws: None, all errors are reported via the callback's err/errors fields.

        New in PyTango 7.1.3
        """
    @typing.overload
    def get_asynch_replies(self, timeout: typing.SupportsInt) -> None:
        """get_asynch_replies(self, timeout: int) -> None

            Fire callback methods for all asynchronous requests (command and attributes)
            with already arrived replies. Wait up to `timeout` milliseconds if some replies
            haven't arrived yet. If timeout=0, waits until all requests receive a reply.

        :param timeout: timeout in milliseconds
        :type timeout: int
        :return: None

        Throws: AsynReplyNotArrived if some replies did not arrive in time.
                Other errors are reported via the callback's err/errors fields.

        New in PyTango 7.1.3
        """
    def get_ip_from_if(self, interface_name: StdStringVector) -> None:
        """get_ip_from_if(self, interface_name: str) -> str

           Get the IP address for the given network interface name.

        :param interface_name: The name of the network interface
        :type interface_name: str

        :return: IP address associated to that interface
        :rtype: str
        """
    def get_user_connect_timeout(self) -> int:
        """get_user_connect_timeout(self) -> int

            Get the user connect timeout (in milliseconds).

        :return: The timeout in milliseconds
        :rtype: int
        """
    def in_server(self) -> bool:
        """in_server() -> bool

            Returns True if the current process is running a Tango device server.

        :return: True if running in a server, otherwise False
        :rtype: bool

        .. versionadded:: 10.0.0
        """
    def is_notifd_event_consumer_created(self) -> bool:
        """is_notifd_event_consumer_created(self) -> bool

            Check if the notifd event consumer was created.

        :return: True if created, False otherwise
        :rtype: bool
        """
    def is_zmq_event_consumer_created(self) -> bool:
        """is_zmq_event_consumer_created(self) -> bool

            Check if the ZMQ event consumer was created.

        :return: True if created, False otherwise
        :rtype: bool
        """
    def pending_asynch_call(self, req: asyn_req_type) -> int:
        """pending_asynch_call(self, req) -> int

            Return the number of asynchronous pending requests (any device).
            The input parameter is an enumeration with three values:
            - POLLING
            - CALL_BACK
            - ALL_ASYNCH

        :param req: asynchronous request type
        :type req: asyn_req_type
        :return: the number of pending requests for the given type
        :rtype: int

        New in PyTango 7.1.3
        """
    def set_asynch_cb_sub_model(self, model: cb_sub_model) -> None:
        """set_asynch_cb_sub_model(self, model) -> None

            Set the asynchronous callback sub-model between PULL_CALLBACK or PUSH_CALLBACK.

        :param model: the callback sub-model
        :type model: cb_sub_model
        :return: None

        New in PyTango 7.1.3
        """

class ArchiveEventInfo:
    """A structure containing available archiving event information for an attribute
    with the following members:

        - archive_rel_change : (str) relative change that will generate an event
        - archive_abs_change : (str) absolute change that will generate an event
        - archive_period : (str) archive period
        - extensions : (sequence<str>) extensions (currently not used)
    """

    archive_abs_change: str
    archive_period: str
    archive_rel_change: str
    extensions: StdStringVector
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class ArchiveEventProp:
    abs_change: str
    extensions: list[str]
    period: str
    rel_change: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""

class AsynCall(DevFailed): ...
class AsynReplyNotArrived(DevFailed): ...

class AttReqType(enum.IntEnum):
    """An enumeration representing the type of attribute request"""

    READ_REQ: typing.ClassVar[AttReqType]  # value = <AttReqType.READ_REQ: 0>
    WRITE_REQ: typing.ClassVar[AttReqType]  # value = <AttReqType.WRITE_REQ: 1>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class Attr:
    """ """
    def __init__(
        self,
        name: str,
        data_type: typing.SupportsInt,
        w_type: AttrWriteType = tango.AttrWriteType.READ,
    ) -> None: ...
    def __repr__(self): ...
    def __str__(self): ...
    def check_type(self) -> None:
        """check_type(self)

            This method checks data type and throws an exception in case of unsupported data type

        :raises: :class:`DevFailed`: If the data type is unsupported.
        """
    def get_assoc(self) -> str:
        """get_assoc(self) -> str

            Get the associated name.

        :returns: the associated name
        :rtype: bool
        """
    def get_cl_name(self) -> str:
        """get_cl_name(self) -> str

            Returns the class name.

        :returns: the class name
        :rtype: str

        New in PyTango 7.2.0
        """
    def get_class_properties(self) -> list[AttrProperty]:
        """get_class_properties(self) -> Sequence[AttrProperty]

            Get the class level attribute properties.

        :returns: the class attribute properties
        :rtype: Sequence[AttrProperty]
        """
    def get_disp_level(self) -> DispLevel:
        """get_disp_level(self) -> DispLevel

            Get the attribute display level.

        :returns: the attribute display level
        :rtype: DispLevel
        """
    def get_format(self) -> AttrDataFormat:
        """get_format(self) -> AttrDataFormat

            Get the attribute format.

        :returns: the attribute format
        :rtype: AttrDataFormat
        """
    def get_memorized(self) -> bool:
        """get_memorized(self) -> bool

            Determine if the attribute is memorized or not.

        :returns: True if the attribute is memorized
        :rtype: bool
        """
    def get_memorized_init(self) -> bool:
        """get_memorized_init(self) -> bool

            Determine if the attribute is written at startup from the memorized
            value if it is memorized.

        :returns: True if initialized with memorized value or not
        :rtype: bool
        """
    def get_name(self) -> str:
        """get_name(self) -> str

            Get the attribute name.

        :returns: the attribute name
        :rtype: str
        """
    def get_polling_period(self) -> int:
        """get_polling_period(self) -> int

            Get the polling period (mS).

        :returns: the polling period (mS)
        :rtype: int
        """
    def get_type(self) -> int:
        """get_type(self) -> int

            Get the attribute data type.

        :returns: the attribute data type
        :rtype: int
        """
    def get_user_default_properties(self) -> list[AttrProperty]:
        """get_user_default_properties(self) -> Sequence[AttrProperty]

            Get the user default attribute properties.

        :returns: the user default attribute properties
        :rtype: Sequence[AttrProperty]
        """
    def get_writable(self) -> AttrWriteType:
        """get_writable(self) -> AttrWriteType

            Get the attribute write type.

        :returns: the attribute write type
        :rtype: AttrWriteType
        """
    def is_alarm_event(self) -> bool:
        """is_alarm_event(self) -> bool

            Check if the alarm event is fired manually (without polling) for this attribute.

        :return: true if a manual fire alarm event is implemented
        :rtype: bool

        .. versionadded:: 10.0.0
        """
    def is_allowed(self, device: ..., request_type: AttReqType) -> bool:
        """is_allowed(self, device, request_type) -> bool

            Returns whether the request_type is allowed for the specified device

        :param device: instance of Device
        :type device: :class:`tango.server.Device`

        :param request_type: AttReqType.READ_REQ for read request or AttReqType.WRITE_REQ for write request
        :type request_type: :const:`AttReqType`

        :returns: True if request_type is allowed for the specified device
        :rtype: bool
        """
    def is_archive_event(self) -> bool:
        """is_archive_event(self) -> bool

            Check if the archive event is fired manually for this attribute.

        :returns: true if a manual fire archive event is implemented.
        :rtype: bool
        """
    def is_assoc(self) -> bool:
        """is_assoc(self) -> bool

            Determine if it is assoc.

        :returns: if it is assoc
        :rtype: bool
        """
    def is_change_event(self) -> bool:
        """is_change_event(self) -> bool

        Check if the change event is fired manually for this attribute.

        :returns: true if a manual fire change event is implemented.
        :rtype: bool
        """
    def is_check_archive_criteria(self) -> bool:
        """is_check_archive_criteria(self) -> bool

            Check if the archive event criteria should be checked when firing the event manually.

        :returns: true if a archive event criteria will be checked.
        :rtype: bool
        """
    def is_check_change_criteria(self) -> bool:
        """is_check_change_criteria(self) -> bool

            Check if the change event criteria should be checked when firing the event manually.

        :returns: true if a change event criteria will be checked.
        :rtype: bool
        """
    def is_data_ready_event(self) -> bool:
        """is_data_ready_event(self) -> bool

        Check if the data ready event is fired for this attribute.

        :returns: true if firing data ready event is implemented.
        :rtype: bool

        New in PyTango 7.2.0
        """
    def read(self, arg0: ..., arg1: Attribute) -> None: ...
    def set_alarm_event(self, implemented: bool, detect: bool) -> None:
        """set_alarm_event(self, implemented, detect)

        Set a flag to indicate that the server fires alarm events manually
        without the polling to be started for the attribute.

        If the detect parameter is set to true, the criteria specified for the
        alarm event (rel_change and abs_change) are verified and
        the event is only pushed if a least one of them are fulfilled
        (change in value compared to previous event exceeds a threshold).

        If detect is set to false the event is fired without checking!

        :param implemented: True when the server fires alarm events manually.
        :type implemented: bool
        :param detect: Triggers the verification of the alarm event properties
                       when set to true.
        :type detect: bool

        .. versionadded:: 10.0.0
        """
    def set_archive_event(self, implemented: bool, detect: bool) -> None:
        """set_archive_event(self)

            Set a flag to indicate that the server fires archive events manually
            without the polling to be started for the attribute.

            If the detect parameter is set to true, the criteria specified for the
            archive event (rel_change and abs_change) are verified and
            the event is only pushed if a least one of them are fulfilled
            (change in value compared to previous event exceeds a threshold).

            If detect is set to false the event is fired without checking!

        :param implemented: True when the server fires change events manually.
        :type implemented: bool
        :param detect: Triggers the verification of the archive event properties
                       when set to true.
        :type detect: bool
        """
    def set_change_event(self, implemented: bool, detect: bool) -> None:
        """set_change_event(self, implemented, detect)

        Set a flag to indicate that the server fires change events manually
        without the polling to be started for the attribute.

        If the detect parameter is set to true, the criteria specified for the
        change event (rel_change and abs_change) are verified and
        the event is only pushed if a least one of them are fulfilled
        (change in value compared to previous event exceeds a threshold).

        If detect is set to false the event is fired without checking!

        :param implemented: True when the server fires change events manually.
        :type implemented: bool
        :param detect: Triggers the verification of the change event properties
                       when set to true.
        :type detect: bool
        """
    def set_cl_name(self, arg0: str) -> None:
        """set_cl_name(self, cl)

            Sets the class name.

        :param cl: new class name
        :type cl: str

        New in PyTango 7.2.0
        """
    def set_class_properties(
        self, arg0: collections.abc.Sequence[AttrProperty]
    ) -> None:
        """set_class_properties(self, props)

            Set the class level attribute properties.

        :param props: new class level attribute properties
        :type props: StdAttrPropertyVector
        """
    def set_data_ready_event(self, implemented: bool) -> None:
        """set_data_ready_event(self, implemented)

            Set a flag to indicate that the server fires data ready events.

        :param implemented: True when the server fires data ready events
        :type implemented: bool

        New in PyTango 7.2.0
        """
    def set_default_properties(self, arg0: UserDefaultAttrProp) -> None:
        """set_default_properties(self)

        Set default attribute properties.

        :param attr_prop: the user default property class
        :type attr_prop: UserDefaultAttrProp
        """
    def set_disp_level(self, disp_level: DispLevel) -> None:
        """set_disp_level(self, disp_level)

        Set the attribute display level.

        :param disp_level: the new display level
        :type disp_level: DispLevel
        """
    def set_memorized(self) -> None:
        """set_memorized(self)

        Set the attribute as memorized in database (only for scalar
        and writable attribute).

        By default the setpoint will be written to the attribute during initialisation!
        Use method set_memorized_init() with False as argument if you don't
        want this feature.
        """
    def set_memorized_init(self, write_on_init: bool) -> None:
        """set_memorized_init(self, write_on_init)

        Set the initialisation flag for memorized attributes.

        - true = the setpoint value will be written to the attribute on initialisation
        - false = only the attribute setpoint is initialised.

        No action is taken on the attribute

        :param write_on_init: if true the setpoint value will be written
                              to the attribute on initialisation
        :type write_on_init: bool
        """
    def set_polling_period(self, period_ms: typing.SupportsInt) -> None:
        """set_polling_period(self, period_ms)

        Set the attribute polling update period.

        :param period_ms: the attribute polling period (in mS)
        :type period_ms: int
        """
    def write(self, arg0: ..., arg1: WAttribute) -> None: ...

class AttrConfEventData:
    """This class is used to pass data to the callback method when an
    attribute configuration event (:obj:`tango.EventType.ATTR_CONF_EVENT`)
    is sent to the client. It contains the
    following public fields:

        - device : (DeviceProxy) The DeviceProxy object on which the call was executed
        - attr_name : (str) The attribute name
        - event : (str) The event type name
        - event_reason : (EventReason) The reason for the event
        - attr_conf : (AttributeInfoEx) The attribute data
        - err : (bool) A boolean flag set to true if the request failed. False
          otherwise
        - errors : (sequence<DevError>) The error stack
        - reception_date: (TimeVal)
    """

    attr_name: str
    device: DeviceProxy
    err: bool
    event: str
    event_reason: EventReason
    reception_date: TimeVal
    @typing.overload
    def __init__(self, arg0: AttrConfEventData) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal

            Returns the timestamp of the event.

        :returns: the timestamp of the event
        :rtype: TimeVal

        New in PyTango 7.0.0
        """
    @property
    def errors(self) -> list[DevError]: ...
    @errors.setter
    def errors(self, arg1: typing.Any) -> None: ...

class AttrDataFormat(enum.IntEnum):
    """An enumeration representing the attribute format"""

    FMT_UNKNOWN: typing.ClassVar[
        AttrDataFormat
    ]  # value = <AttrDataFormat.FMT_UNKNOWN: 3>
    IMAGE: typing.ClassVar[AttrDataFormat]  # value = <AttrDataFormat.IMAGE: 2>
    SCALAR: typing.ClassVar[AttrDataFormat]  # value = <AttrDataFormat.SCALAR: 0>
    SPECTRUM: typing.ClassVar[AttrDataFormat]  # value = <AttrDataFormat.SPECTRUM: 1>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class AttrMemorizedType(enum.IntEnum):
    MEMORIZED: typing.ClassVar[
        AttrMemorizedType
    ]  # value = <AttrMemorizedType.MEMORIZED: 2>
    MEMORIZED_WRITE_INIT: typing.ClassVar[
        AttrMemorizedType
    ]  # value = <AttrMemorizedType.MEMORIZED_WRITE_INIT: 3>
    NONE: typing.ClassVar[AttrMemorizedType]  # value = <AttrMemorizedType.NONE: 1>
    NOT_KNOWN: typing.ClassVar[
        AttrMemorizedType
    ]  # value = <AttrMemorizedType.NOT_KNOWN: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class AttrProperty:
    def __init__(self, arg0: str, arg1: str) -> None: ...
    def get_lg_value(self) -> int: ...
    def get_name(self) -> str: ...
    def get_value(self) -> str: ...

class AttrQuality(enum.IntEnum):
    """An enumeration representing the attribute quality"""

    ATTR_ALARM: typing.ClassVar[AttrQuality]  # value = <AttrQuality.ATTR_ALARM: 2>
    ATTR_CHANGING: typing.ClassVar[
        AttrQuality
    ]  # value = <AttrQuality.ATTR_CHANGING: 3>
    ATTR_INVALID: typing.ClassVar[AttrQuality]  # value = <AttrQuality.ATTR_INVALID: 1>
    ATTR_VALID: typing.ClassVar[AttrQuality]  # value = <AttrQuality.ATTR_VALID: 0>
    ATTR_WARNING: typing.ClassVar[AttrQuality]  # value = <AttrQuality.ATTR_WARNING: 4>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class AttrReadEvent:
    """ """
    @property
    def argout(self) -> typing.Any:
        """(DeviceAttribute) The attribute value"""
    @property
    def attr_names(self) -> StdStringVector:
        """(sequence<str>) The attribute name list"""
    @property
    def device(self) -> DeviceProxy:
        """(DeviceProxy) The DeviceProxy object on which the call was executed"""
    @property
    def err(self) -> bool:
        """(bool) A boolean flag set to true if the command failed. False otherwise"""
    @property
    def errors(self) -> list[DevError]:
        """(sequence<DevError>) The error stack"""

class AttrSerialModel(enum.IntEnum):
    """An enumeration representing the AttrSerialModel

    New in PyTango 7.1.0
    """

    ATTR_BY_KERNEL: typing.ClassVar[
        AttrSerialModel
    ]  # value = <AttrSerialModel.ATTR_BY_KERNEL: 1>
    ATTR_BY_USER: typing.ClassVar[
        AttrSerialModel
    ]  # value = <AttrSerialModel.ATTR_BY_USER: 2>
    ATTR_NO_SYNC: typing.ClassVar[
        AttrSerialModel
    ]  # value = <AttrSerialModel.ATTR_NO_SYNC: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class AttrWriteType(enum.IntEnum):
    """An enumeration representing the attribute type"""

    READ: typing.ClassVar[AttrWriteType]  # value = <AttrWriteType.READ: 0>
    READ_WITH_WRITE: typing.ClassVar[
        AttrWriteType
    ]  # value = <AttrWriteType.READ_WITH_WRITE: 1>
    READ_WRITE: typing.ClassVar[AttrWriteType]  # value = <AttrWriteType.READ_WRITE: 3>
    WRITE: typing.ClassVar[AttrWriteType]  # value = <AttrWriteType.WRITE: 2>
    WT_UNKNOWN: typing.ClassVar[AttrWriteType]  # value = <AttrWriteType.WT_UNKNOWN: 4>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class AttrWrittenEvent:
    """ """
    @property
    def attr_names(self) -> StdStringVector:
        """(sequence<str>) The attribute name list"""
    @property
    def device(self) -> DeviceProxy:
        """(DeviceProxy) The DeviceProxy object on which the call was executed"""
    @property
    def err(self) -> bool:
        """(bool) A boolean flag set to true if the command failed. False otherwise"""
    @property
    def errors(self) -> NamedDevFailedList:
        """(sequence<DevError>) The error stack"""

class Attribute:
    """This class represents a Tango attribute"""
    def __repr__(self): ...
    def __str__(self): ...
    def _get_properties_multi_attr_prop(
        self, multi_attr_prop: typing.Any
    ) -> typing.Any: ...
    def _set_properties_multi_attr_prop(self, multi_attr_prop: typing.Any) -> None: ...
    @typing.overload
    def _set_value(self, data: typing.Any) -> None: ...
    @typing.overload
    def _set_value(self, encoding: typing.Any, data: typing.Any) -> None: ...
    @typing.overload
    def _set_value_date_quality(
        self, data: typing.Any, time: typing.SupportsFloat, quality: AttrQuality
    ) -> None: ...
    @typing.overload
    def _set_value_date_quality(
        self,
        encoding: typing.Any,
        data: typing.Any,
        time: typing.SupportsFloat,
        quality: AttrQuality,
    ) -> None: ...
    def alarm_event_subscribed(self) -> bool:
        """alarm_event_subscribed(self) -> bool

        :return: true if there are some subscriber listening for alarm event
        :rtype: bool
        """
    def archive_event_subscribed(self) -> bool:
        """archive_event_subscribed(self) -> bool

        :return: true if there are some subscriber listening for archive event
        :rtype: bool
        """
    def change_event_subscribed(self) -> bool:
        """change_event_subscribed(self) -> bool

        :return: true if there are some subscriber listening for change event
        :rtype: bool
        """
    def check_alarm(self) -> bool:
        """check_alarm(self) -> bool

            Check if the attribute read value is below/above the alarm level.

        :returns: true if the attribute is in alarm condition.
        :rtype: bool

        :raises DevFailed: If no alarm level is defined.
        """
    @typing.overload
    def fire_alarm_event(self) -> None: ...
    @typing.overload
    def fire_alarm_event(self, exception: typing.Any) -> None: ...
    @typing.overload
    def fire_change_event(self) -> None: ...
    @typing.overload
    def fire_change_event(self, exception: typing.Any) -> None: ...
    def get_assoc_ind(self) -> int:
        """get_assoc_ind(self) -> int

            Get index of the associated writable attribute.

        :returns: the index in the main attribute vector of the associated writable attribute
        :rtype: int
        """
    def get_assoc_name(self) -> str:
        """get_assoc_name(self) -> str

            Get name of the associated writable attribute.

        :returns: the associated writable attribute name
        :rtype: str
        """
    def get_attr_serial_model(self) -> AttrSerialModel:
        """get_attr_serial_model(self) -> AttrSerialModel

            Get attribute serialization model.

        :returns: The attribute serialization model
        :rtype: AttrSerialModel

        New in PyTango 7.1.0
        """
    def get_data_format(self) -> AttrDataFormat:
        """get_data_format(self) -> AttrDataFormat

            Get attribute data format.

        :returns: the attribute data format
        :rtype: AttrDataFormat
        """
    def get_data_size(self) -> int:
        """get_data_size(self)

            Get attribute data size.

        :returns: the attribute data size
        :rtype: int
        """
    def get_data_type(self) -> int:
        """get_data_type(self) -> int

            Get attribute data type.

        :returns: the attribute data type
        :rtype: int
        """
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal

            Get a COPY of the attribute date.

        :returns: the attribute date
        :rtype: TimeVal
        """
    def get_disp_level(self) -> DispLevel:
        """get_disp_level(self) -> DisplLevel

        :return: attribute display level
        :rtype: DispLevel
        """
    def get_label(self) -> str:
        """get_label(self) -> str

            Get attribute label property.

        :returns: the attribute label
        :rtype: str
        """
    def get_max_alarm(self) -> typing.Any: ...
    def get_max_dim_x(self) -> int:
        """get_max_dim_x(self) -> int

            Get attribute maximum data size in x dimension.

        :returns: the attribute maximum data size in x dimension. Set to 1 for scalar attribute
        :rtype: int
        """
    def get_max_dim_y(self) -> int:
        """get_max_dim_y(self) -> int

            Get attribute maximum data size in y dimension.

        :returns: the attribute maximum data size in y dimension. Set to 0 for scalar attribute
        :rtype: int
        """
    def get_max_warning(self) -> typing.Any: ...
    def get_min_alarm(self) -> typing.Any: ...
    def get_min_warning(self) -> typing.Any: ...
    def get_name(self) -> str:
        """get_name(self) -> str

            Get attribute name.

        :returns: The attribute name
        :rtype: str
        """
    def get_polling_period(self) -> int:
        """get_polling_period(self) -> int

            Get attribute polling period.

        :returns: The attribute polling period in mS. Set to 0 when the attribute is not polled
        :rtype: int
        """
    def get_properties(self, attr_cfg=None):
        """get_properties(self: Attribute, attr_cfg: AttributeConfig = None) -> AttributeConfig

        Get attribute properties.

        :param conf: the config object to be filled with
                     the attribute configuration. Default is None meaning the
                     method will create internally a new :obj:`tango.AttributeConfig_5`
                     and return it.
                     Can be :obj:`tango.AttributeConfig`, :obj:`tango.AttributeConfig_2`,
                     :obj:`tango.AttributeConfig_3`, :obj:`tango.AttributeConfig_5` or
                     :obj:`tango.MultiAttrProp`

        :returns: the config object filled with attribute configuration information
        :rtype: :obj:`tango.AttributeConfig`

        New in PyTango 7.1.4
        """
    def get_quality(self) -> AttrQuality:
        """get_quality(self) -> AttrQuality

            Get a COPY of the attribute data quality.

        :returns: the attribute data quality
        :rtype: AttrQuality
        """
    def get_writable(self) -> AttrWriteType:
        """get_writable(self) -> AttrWriteType

            Get the attribute writable type (RO/WO/RW).

        :returns: The attribute write type.
        :rtype: AttrWriteType
        """
    def get_x(self) -> int:
        """get_x(self) -> int

            Get attribute data size in x dimension.

        :returns: the attribute data size in x dimension. Set to 1 for scalar attribute
        :rtype: int
        """
    def get_y(self) -> int:
        """get_y(self) -> int

            Get attribute data size in y dimension.

        :returns: the attribute data size in y dimension. Set to 0 for scalar attribute
        :rtype: int
        """
    def is_alarm_event(self) -> bool:
        """is_alarm_event(self) -> bool

            Check if the alarm event is fired manually for this attribute.

        :returns: True if a manual fire alarm event is implemented.
        :rtype: bool

        New in PyTango 10.0.0
        """
    def is_archive_event(self) -> bool:
        """is_archive_event(self) -> bool

            Check if the archive event is fired manually (without polling) for this attribute.

        :returns: True if a manual fire archive event is implemented.
        :rtype: bool

        New in PyTango 7.1.0
        """
    def is_change_event(self) -> bool:
        """is_change_event(self) -> bool

            Check if the change event is fired manually (without polling) for this attribute.

        :returns: True if a manual fire change event is implemented.
        :rtype: bool

        New in PyTango 7.1.0
        """
    def is_check_alarm_criteria(self) -> bool:
        """is_check_alarm_criteria(self) -> bool

            Check if the alarm event criteria should be checked when firing the
            event manually.

        :returns: True if a change event criteria will be checked.
        :rtype: bool

        New in PyTango 10.0.0
        """
    def is_check_archive_criteria(self) -> bool:
        """is_check_archive_criteria(self) -> bool

            Check if the archive event criteria should be checked when firing the
            event manually.

        :returns: True if a archive event criteria will be checked.
        :rtype: bool

        New in PyTango 7.1.0
        """
    def is_check_change_criteria(self) -> bool:
        """is_check_change_criteria(self) -> bool

            Check if the change event criteria should be checked when firing the
            event manually.

        :returns: True if a change event criteria will be checked.
        :rtype: bool

        New in PyTango 7.1.0
        """
    def is_data_ready_event(self) -> bool:
        """is_data_ready_event(self) -> bool

            Check if the data ready event is fired manually (without polling)
            for this attribute.

        :returns: True if a manual fire data ready event is implemented.
        :rtype: bool

        New in PyTango 7.2.0
        """
    def is_max_alarm(self) -> bool:
        """is_max_alarm(self) -> bool

            Check if the attribute is in maximum alarm condition.

        :returns: true if the attribute is in alarm condition (read value above the max. alarm).
        :rtype: bool
        """
    def is_max_warning(self) -> bool:
        """is_max_warning(self) -> bool

            Check if the attribute is in maximum warning condition.

        :returns: true if the attribute is in warning condition (read value above the max. warning).
        :rtype: bool
        """
    def is_min_alarm(self) -> bool:
        """is_min_alarm(self) -> bool

            Check if the attribute is in minimum alarm condition.

        :returns: true if the attribute is in alarm condition (read value below the min. alarm).
        :rtype: bool
        """
    def is_min_warning(self) -> bool:
        """is_min_warning(self) -> bool

            Check if the attribute is in minimum warning condition.

        :returns: true if the attribute is in warning condition (read value below the min. warning).
        :rtype: bool
        """
    def is_polled(self) -> bool:
        """is_polled(self) -> bool

            Check if the attribute is polled.

        :returns: true if the attribute is polled.
        :rtype: bool
        """
    def is_rds_alarm(self) -> bool:
        """is_rds_alarm(self) -> bool

            Check if the attribute is in RDS alarm condition.

        :returns: true if the attribute is in RDS condition (Read Different than Set).
        :rtype: bool
        """
    def is_write_associated(self) -> bool:
        """is_write_associated(self) -> bool

            Check if the attribute has an associated writable attribute.

        :returns: True if there is an associated writable attribute
        :rtype: bool
        """
    def periodic_event_subscribed(self) -> bool:
        """periodic_event_subscribed(self) -> bool

        :return: true if there are some subscriber listening for periodic event
        :rtype: bool
        """
    def remove_configuration(self) -> None:
        """remove_configuration(self)

        Remove the attribute configuration from the database.

        This method can be used to clean-up all the configuration of an
        attribute to come back to its default values or the remove all
        configuration of a dynamic attribute before deleting it.

        The method removes all configured attribute properties and removes
        the attribute from the list of polled attributes.

        New in PyTango 7.1.0
        """
    def reset_value(self) -> None:
        """reset_value(self) -> None

        Clear attribute value
        """
    def set_alarm_event(self, implemented: bool, detect: bool = True) -> None:
        """Set a flag to indicate that the server fires alarm events manually,
        without the polling to be started for the attribute.

        If the detect parameter is set to true, the criteria specified for the
        alarm event (rel_change and abs_change) are verified and
        the event is only pushed if a least one of them are fulfilled
        (change in value compared to previous event exceeds a threshold).
        If detect is set to false the event is fired without
        any value checking!

        :param implemented: True when the server fires alarm events manually.
        :type implemented: bool
        :param detect: (optional, default is True) Triggers the verification of
                        the alarm event properties when set to true.
        :type detect: bool

        .. versionadded:: 10.0.0
        """
    def set_archive_event(self, implemented: bool, detect: bool = True) -> None:
        """Set a flag to indicate that the server fires archive events manually,
        without the polling to be started for the attribute.

        If the detect parameter is set to true, the criteria specified for the
        archive event (rel_change and abs_change) are verified and
        the event is only pushed if a least one of them are fulfilled
        (change in value compared to previous event exceeds a threshold).

        If detect is set to false the event is fired without any value checking!

        :param implemented: True when the server fires archive events manually.
        :type implemented: bool
        :param detect: (optional, default is True) Triggers the verification of
                        the archive event properties when set to true.
        :type detect: bool

        New in PyTango 7.1.0
        """
    def set_assoc_ind(self, index: typing.SupportsInt) -> None:
        """set_assoc_ind(self, index)

            Set index of the associated writable attribute.

        :param index: The new index in the main attribute vector of the associated writable attribute
        :type index: int
        """
    def set_attr_serial_model(self, ser_model: AttrSerialModel) -> None:
        """set_attr_serial_model(self, ser_model) -> None

            Set attribute serialization model.

            This method allows the user to choose the attribute serialization model.

        :param ser_model: The new serialisation model. The
                          serialization model must be one of ATTR_BY_KERNEL,
                          ATTR_BY_USER or ATTR_NO_SYNC
        :type ser_model: AttrSerialModel

        New in PyTango 7.1.0
        """
    def set_change_event(self, implemented: bool, detect: bool = True) -> None:
        """Set a flag to indicate that the server fires change events manually,
        without the polling to be started for the attribute.

        If the detect parameter is set to true, the criteria specified for the
        change event (rel_change and abs_change) are verified and
        the event is only pushed if a least one of them are fulfilled
        (change in value compared to previous event exceeds a threshold).
        If detect is set to false the event is fired without
        any value checking!

        :param implemented: True when the server fires change events manually.
        :type implemented: bool
        :param detect: (optional, default is True) Triggers the verification of
                        the change event properties when set to true.
        :type detect: bool

        New in PyTango 7.1.0
        """
    def set_data_ready_event(self, implemented: bool) -> None:
        """set_data_ready_event(self, implemented)

            Set a flag to indicate that the server fires data ready events.

        :param implemented: True when the server fires data ready events manually.
        :type implemented: bool

        New in PyTango 7.2.0
        """
    def set_date(self, new_date: TimeVal) -> None:
        """set_date(self, new_date)

            Set attribute date.

        :param new_date: the attribute date
        :type new_date: TimeVal
        """
    def set_max_alarm(self, value: typing.Any) -> None: ...
    def set_max_warning(self, value: typing.Any) -> None: ...
    def set_min_alarm(self, value: typing.Any) -> None: ...
    def set_min_warning(self, value: typing.Any) -> None: ...
    def set_properties(self, attr_cfg, dev=None):
        """set_properties(self: Attribute, attr_cfg: AttributeConfig, dev: DeviceImpl = None)

        Set attribute properties.

        This method sets the attribute properties value with the content
        of the fields in the :obj:`tango.AttributeConfig`/ :obj:`tango.AttributeConfig_3` object

        :param conf: the config object.
        :type conf: :obj:`tango.AttributeConfig` or :obj:`tango.AttributeConfig_3`
        :param dev: the device (not used, maintained
                    for backward compatibility)
        :type dev: :obj:`tango.DeviceImpl`

        New in PyTango 7.1.4
        """
    def set_quality(self, quality: AttrQuality, send_event: bool = False) -> None:
        """set_quality(self, quality, send_event=False)

            Set attribute data quality.

        :param quality: the new attribute data quality
        :type quality: AttrQuality
        :param send_event: true if a change event should be sent. Default is false.
        :type send_event: bool
        """
    @typing.overload
    def set_upd_properties(self, attr_cfg: typing.Any) -> None: ...
    @typing.overload
    def set_upd_properties(
        self, attr_cfg: typing.Any, dev_name: typing.Any
    ) -> None: ...
    def set_value(self, *args):
        """.. function:: set_value(self, data)
                      set_value(self, str_data, data)
            :noindex:

        Set internal attribute value.

        This method stores the attribute read value inside the object.
        This method also stores the date when it is called and initializes the
        attribute quality factor.

        :param data: the data to be set. Data must be compatible with the attribute type and format.
                     E.g., sequence for SPECTRUM and a SEQUENCE of equal-length SEQUENCES
                     for IMAGE attributes.
                     The recommended sequence is a C continuous and aligned numpy
                     array, as it can be optimized.
        :param str_data: special variation for DevEncoded data type. In this case 'data' must
                         be a str or an object with the buffer interface.
        :type str_data: str

        .. versionchanged:: 10.1.0
            The dim_x and dim_y parameters were removed.
        """
    def set_value_date_quality(self, *args):
        """.. function::   set_value_date_quality(self, data, time_stamp, quality)
                        set_value_date_quality(self, str_data, data, time_stamp, quality)
            :noindex:

        Set internal attribute value, date and quality factor.

        This method stores the attribute read value, the date and the attribute quality
        factor inside the object.

        :param data: the data to be set. Data must be compatible with the attribute type and format.
                     E.g., sequence for SPECTRUM and a SEQUENCE of equal-length SEQUENCES
                     for IMAGE attributes.
                     The recommended sequence is a C continuous and aligned numpy
                     array, as it can be optimized.
        :param str_data: special variation for DevEncoded data type. In this case 'data' must
                         be a str or an object with the buffer interface.
        :type str_data: str
        :param time_stamp: the time stamp
        :type time_stamp: double
        :param quality: the attribute quality factor
        :type quality: AttrQuality

        .. versionchanged:: 10.1.0
            The dim_x and dim_y parameters were removed.
        """
    def use_notifd_event(self) -> bool:
        """use_notifd_event(self) -> bool

        :return: true if notifd events are emited
        :rtype: bool
        """
    def use_zmq_event(self) -> bool:
        """use_zmq_event(self) -> bool

        :return: true if zmq events are emited
        :rtype: bool
        """
    def user_event_subscribed(self) -> bool:
        """user_event_subscribed(self) -> bool

        :return: true if there are some subscriber listening for user event
        :rtype: bool
        """
    def value_is_set(self) -> bool:
        """value_is_set(self) -> bool

        :return: true if attribute has a value
        :rtype: bool
        """

class AttributeAlarm:
    delta_t: str
    delta_val: str
    extensions: list[str]
    max_alarm: str
    max_warning: str
    min_alarm: str
    min_warning: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""

class AttributeAlarmInfo:
    """A structure containing available alarm information for an attribute
    with the following members:

        - min_alarm : (str) low alarm level
        - max_alarm : (str) high alarm level
        - min_warning : (str) low warning level
        - max_warning : (str) high warning level
        - delta_t : (str) time delta
        - delta_val : (str) value delta
        - extensions : (StdStringVector) extensions (currently not used)
    """

    delta_t: str
    delta_val: str
    extensions: StdStringVector
    max_alarm: str
    max_warning: str
    min_alarm: str
    min_warning: str
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class AttributeConfig:
    data_format: AttrDataFormat
    description: str
    display_unit: str
    extensions: list[str]
    format: str
    label: str
    max_alarm: str
    max_value: str
    min_alarm: str
    min_value: str
    name: str
    standard_unit: str
    unit: str
    writable: AttrWriteType
    writable_attr_name: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def data_type(self) -> int: ...
    @data_type.setter
    def data_type(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_x(self) -> int: ...
    @max_dim_x.setter
    def max_dim_x(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_y(self) -> int: ...
    @max_dim_y.setter
    def max_dim_y(self, arg0: typing.SupportsInt) -> None: ...

class AttributeConfig_2:
    data_format: AttrDataFormat
    description: str
    display_unit: str
    extensions: list[str]
    format: str
    label: str
    level: DispLevel
    max_alarm: str
    max_value: str
    min_alarm: str
    min_value: str
    name: str
    standard_unit: str
    unit: str
    writable: AttrWriteType
    writable_attr_name: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def data_type(self) -> int: ...
    @data_type.setter
    def data_type(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_x(self) -> int: ...
    @max_dim_x.setter
    def max_dim_x(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_y(self) -> int: ...
    @max_dim_y.setter
    def max_dim_y(self, arg0: typing.SupportsInt) -> None: ...

class AttributeConfig_3:
    att_alarm: AttributeAlarm
    data_format: AttrDataFormat
    description: str
    display_unit: str
    event_prop: EventProperties
    extensions: list[str]
    format: str
    label: str
    level: DispLevel
    max_value: str
    min_value: str
    name: str
    standard_unit: str
    sys_extensions: list[str]
    unit: str
    writable: AttrWriteType
    writable_attr_name: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def data_type(self) -> int: ...
    @data_type.setter
    def data_type(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_x(self) -> int: ...
    @max_dim_x.setter
    def max_dim_x(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_y(self) -> int: ...
    @max_dim_y.setter
    def max_dim_y(self, arg0: typing.SupportsInt) -> None: ...

class AttributeConfig_5:
    att_alarm: AttributeAlarm
    data_format: AttrDataFormat
    description: str
    display_unit: str
    enum_labels: list[str]
    event_prop: EventProperties
    extensions: list[str]
    format: str
    label: str
    level: DispLevel
    max_value: str
    mem_init: bool
    memorized: bool
    min_value: str
    name: str
    root_attr_name: str
    standard_unit: str
    sys_extensions: list[str]
    unit: str
    writable: AttrWriteType
    writable_attr_name: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def data_type(self) -> int: ...
    @data_type.setter
    def data_type(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_x(self) -> int: ...
    @max_dim_x.setter
    def max_dim_x(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_y(self) -> int: ...
    @max_dim_y.setter
    def max_dim_y(self, arg0: typing.SupportsInt) -> None: ...

class AttributeDimension:
    """A structure containing x and y attribute data dimensions with
    the following members:

        - dim_x : (int) x dimension
        - dim_y : (int) y dimension
    """
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def dim_x(self) -> int: ...
    @property
    def dim_y(self) -> int: ...

class AttributeEventInfo:
    """A structure containing available event information for an attribute
    with the following members:

        - ch_event : (ChangeEventInfo) change event information
        - per_event : (PeriodicEventInfo) periodic event information
        - arch_event :  (ArchiveEventInfo) archiving event information
    """

    arch_event: ArchiveEventInfo
    ch_event: ChangeEventInfo
    per_event: PeriodicEventInfo
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class AttributeInfo(DeviceAttributeConfig):
    """A structure (inheriting from :class:`DeviceAttributeConfig`) containing
    available information for an attribute with the following members:

        - disp_level : (DispLevel) display level (OPERATOR, EXPERT)

        Inherited members are:

            - name : (str) attribute name
            - writable : (AttrWriteType) write type (R, W, RW, R with W)
            - data_format : (AttrDataFormat) data format (SCALAR, SPECTRUM, IMAGE)
            - data_type : (int) attribute type (float, string,..)
            - max_dim_x : (int) first dimension of attribute (spectrum or image attributes)
            - max_dim_y : (int) second dimension of attribute(image attribute)
            - description : (int) attribute description
            - label : (str) attribute label (Voltage, time, ...)
            - unit : (str) attribute unit (V, ms, ...)
            - standard_unit : (str) standard unit
            - display_unit : (str) display unit
            - format : (str) how to display the attribute value (ex: for floats could be '%6.2f')
            - min_value : (str) minimum allowed value
            - max_value : (str) maximum allowed value
            - min_alarm : (str) low alarm level
            - max_alarm : (str) high alarm level
            - writable_attr_name : (str) name of the writable attribute
            - extensions : (StdStringVector) extensions (currently not used)
    """

    disp_level: DispLevel
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: AttributeInfo) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class AttributeInfoEx(AttributeInfo):
    """A structure (inheriting from :class:`AttributeInfo`) containing
    available information for an attribute with the following members:

        - alarms : object containing alarm information (see AttributeAlarmInfo).
        - events : object containing event information (see AttributeEventInfo).
        - sys_extensions : StdStringVector

        Inherited members are:

            - name : (str) attribute name
            - writable : (AttrWriteType) write type (R, W, RW, R with W)
            - data_format : (AttrDataFormat) data format (SCALAR, SPECTRUM, IMAGE)
            - data_type : (int) attribute type (float, string,..)
            - max_dim_x : (int) first dimension of attribute (spectrum or image attributes)
            - max_dim_y : (int) second dimension of attribute(image attribute)
            - description : (int) attribute description
            - label : (str) attribute label (Voltage, time, ...)
            - unit : (str) attribute unit (V, ms, ...)
            - standard_unit : (str) standard unit
            - display_unit : (str) display unit
            - format : (str) how to display the attribute value (ex: for floats could be '%6.2f')
            - min_value : (str) minimum allowed value
            - max_value : (str) maximum allowed value
            - min_alarm : (str) low alarm level
            - max_alarm : (str) high alarm level
            - writable_attr_name : (str) name of the writable attribute
            - extensions : (StdStringVector) extensions (currently not used)
            - disp_level : (DispLevel) display level (OPERATOR, EXPERT)
    """

    alarms: AttributeAlarmInfo
    enum_labels: StdStringVector
    events: ...
    memorized: AttrMemorizedType
    root_attr_name: str
    sys_extensions: StdStringVector
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: AttributeInfoEx) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class AttributeInfoList:
    """List of AttributeInfo objects, containing available information for the attributes"""
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    @typing.overload
    def __getitem__(self, s: slice) -> AttributeInfoList:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> AttributeInfo: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: AttributeInfoList) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[AttributeInfo]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: AttributeInfo) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: AttributeInfoList) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: AttributeInfo) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    @typing.overload
    def extend(self, L: AttributeInfoList) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: AttributeInfo) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> AttributeInfo:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> AttributeInfo:
        """Remove and return the item at index ``i``"""

class AttributeInfoListEx:
    """List of AttributeInfoEx objects, containing available information for the attributes"""
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    @typing.overload
    def __getitem__(self, s: slice) -> AttributeInfoListEx:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> AttributeInfoEx: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: AttributeInfoListEx) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[AttributeInfoEx]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: AttributeInfoEx) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: AttributeInfoListEx) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: AttributeInfoEx) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    @typing.overload
    def extend(self, L: AttributeInfoListEx) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: AttributeInfoEx) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> AttributeInfoEx:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> AttributeInfoEx:
        """Remove and return the item at index ``i``"""

class AutoTangoAllowThreads:
    """In a tango server, free the tango monitor within a context:

    with AutoTangoAllowThreads(dev):
        # code here is not under the tango device monitor
        do something
    """
    def __enter__(self): ...
    def __exit__(self, *args, **kwargs): ...
    def __init__(self, device: DeviceImpl) -> None: ...
    def _acquire(self) -> None: ...

class AutoTangoMonitor:
    """In a tango server, guard the tango monitor within a python context::

    with AutoTangoMonitor(dev):
        # code here is protected by the tango device monitor
        do something
    """
    def __enter__(self): ...
    def __exit__(self, *args, **kwargs): ...
    @typing.overload
    def __init__(self, arg0: DeviceImpl) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceClass) -> None: ...
    def _acquire(self) -> None: ...
    def _release(self) -> None: ...

class ChangeEventInfo:
    """A structure containing available change event information for an attribute
    with the following members:

        - rel_change : (str) relative change that will generate an event
        - abs_change : (str) absolute change that will generate an event
        - extensions : (StdStringVector) extensions (currently not used)
    """

    abs_change: str
    extensions: StdStringVector
    rel_change: str
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class ChangeEventProp:
    abs_change: str
    extensions: list[str]
    rel_change: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""

class ClientAddr:
    __hash__: typing.ClassVar[None] = None
    def __eq__(self, arg0: ClientAddr) -> bool: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, addr: str) -> None: ...
    def __ne__(self, arg0: ClientAddr) -> bool: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self) -> str: ...
    def get_client_hostname(self) -> str:
        """get_client_hostname(self) -> str

        Returns client host name, extracted from client ip.

        :returns: client host name
        :rtype: str

        :throws: ValueError
        """
    @property
    def client_ident(self) -> bool: ...
    @property
    def client_ip(self) -> str: ...
    @property
    def client_lang(self) -> LockerLanguage: ...
    @property
    def client_pid(self) -> int: ...
    @property
    def java_ident(self) -> tuple: ...
    @property
    def java_main_class(self) -> str: ...

class CmdArgType(enum.IntEnum):
    """An enumeration representing the Tango data types."""

    ConstDevString: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.ConstDevString: 20>
    DevBoolean: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevBoolean: 1>
    DevDouble: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevDouble: 5>
    DevEncoded: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevEncoded: 28>
    DevEnum: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevEnum: 29>
    DevFloat: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevFloat: 4>
    DevLong: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevLong: 3>
    DevLong64: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevLong64: 23>
    DevShort: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevShort: 2>
    DevState: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevState: 19>
    DevString: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevString: 8>
    DevUChar: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevUChar: 22>
    DevULong: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevULong: 7>
    DevULong64: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevULong64: 24>
    DevUShort: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevUShort: 6>
    DevVarBooleanArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarBooleanArray: 21>
    DevVarCharArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarCharArray: 9>
    DevVarDoubleArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarDoubleArray: 13>
    DevVarDoubleStringArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarDoubleStringArray: 18>
    DevVarEncodedArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarEncodedArray: 32>
    DevVarFloatArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarFloatArray: 12>
    DevVarLong64Array: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarLong64Array: 25>
    DevVarLongArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarLongArray: 11>
    DevVarLongStringArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarLongStringArray: 17>
    DevVarShortArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarShortArray: 10>
    DevVarStateArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarStateArray: 31>
    DevVarStringArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarStringArray: 16>
    DevVarULong64Array: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarULong64Array: 26>
    DevVarULongArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarULongArray: 15>
    DevVarUShortArray: typing.ClassVar[
        CmdArgType
    ]  # value = <CmdArgType.DevVarUShortArray: 14>
    DevVoid: typing.ClassVar[CmdArgType]  # value = <CmdArgType.DevVoid: 0>
    Unknown: typing.ClassVar[CmdArgType]  # value = <CmdArgType.Unknown: 100>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class CmdDoneEvent:
    """This class is used to pass data to the callback method in
    asynchronous callback model for command execution.
    """
    @property
    def argout(self) -> typing.Any:
        """The command argout"""
    @property
    def cmd_name(self) -> str:
        """(str) The command name"""
    @property
    def device(self) -> DeviceProxy:
        """(DeviceProxy) The DeviceProxy object on which the call was executed."""
    @property
    def err(self) -> bool:
        """(bool) A boolean flag set to true if the command failed. False otherwise"""
    @property
    def errors(self) -> list[DevError]:
        """(sequence<DevError>) The error stack"""

class CommandInfo(DevCommandInfo):
    """A device command info (inheriting from :class:`DevCommandInfo`) with the following members:

    - disp_level : (DispLevel) command display level

    Inherited members are (from :class:`DevCommandInfo`):

        - cmd_name : (str) command name
        - cmd_tag : (str) command as binary value (for TACO)
        - in_type : (CmdArgType) input type
        - out_type : (CmdArgType) output type
        - in_type_desc : (str) description of input type
        - out_type_desc : (str) description of output type
    """
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def disp_level(self) -> DispLevel: ...

class CommandInfoList:
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    @typing.overload
    def __getitem__(self, s: slice) -> CommandInfoList:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> CommandInfo: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: CommandInfoList) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[CommandInfo]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: CommandInfo) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: CommandInfoList) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: CommandInfo) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    @typing.overload
    def extend(self, L: CommandInfoList) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: CommandInfo) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> CommandInfo:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> CommandInfo:
        """Remove and return the item at index ``i``"""

class CommunicationFailed(DevFailed): ...

class Connection:
    """The abstract Connection class for DeviceProxy. Not to be initialized directly."""

    defaultCommandExtractAs: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Numpy: 0>
    @staticmethod
    def get_fqdn() -> str:
        """get_fqdn(self) -> str

            Returns the fully qualified domain name

        Parameters : None
        Return     : (str) the fully qualified domain name

        New in PyTango 7.2.0
        """
    def __command_inout(self, arg0: str, arg1: DeviceData) -> DeviceData: ...
    def __command_inout_asynch_cb(
        self, arg0: str, arg1: DeviceData, arg2: typing.Any
    ) -> None: ...
    def __command_inout_asynch_id(
        self, arg0: str, arg1: DeviceData, arg2: bool
    ) -> int: ...
    def cancel_all_polling_asynch_request(self) -> None:
        """cancel_all_polling_asynch_request(self) -> None

            Cancel all running asynchronous request

            This is a client side call. Obviously, the calls cannot be
            aborted while it is running in the device.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
        """
    def cancel_asynch_request(self, id: typing.SupportsInt) -> None:
        """cancel_asynch_request(self, id) -> None

            Cancel a running asynchronous request

            This is a client side call. Obviously, the call cannot be
            aborted while it is running in the device.

        Parameters :
            - id : The asynchronous call identifier
        Return     : None

            New in PyTango 7.0.0
        """
    def command_inout(
        self,
        name,
        cmd_param=None,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ):
        """command_inout( self, cmd_name, cmd_param=None, green_mode=None, wait=True, timeout=None) -> any

            Execute a command on a device.

        :param cmd_name: Command name
        :type value: str

        :param cmd_param: It should be a value of the type expected by the command or a DeviceData object with this value inserted.
                          It can be omitted if the command should not get any argument.
        :type cmd_param: Any

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: The result of the command. The type depends on the command. It may be None
        :rtype: Any

        :throws: TypeError: if cmd_param's type is not compatible with the command
        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: :obj:`tango.DeviceUnlocked`: Raised in case of a device failure.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 8.1.0
            *green_mode* parameter.
            *wait* parameter.
            *timeout* parameter.

        .. versionchanged:: 10.0.0
            TypeError's for invalid command input arguments are now more detailed.
            For commands with a DEV_STRING input argument, invalid data will now raise TypeError instead of SystemError.
        """
    def command_inout_asynch(self, cmd_name, *args):
        """command_inout_asynch(self, cmd_name) -> id
        command_inout_asynch(self, cmd_name, cmd_param) -> id
        command_inout_asynch(self, cmd_name, cmd_param, forget) -> id

                Execute asynchronously (polling model) a command on a device

            Parameters :
                    - cmd_name  : (str) Command name.
                    - cmd_param : (any) It should be a value of the type expected by the
                                  command or a DeviceData object with this value inserted.
                                  It can be omitted if the command should not get any argument.
                                  If the command should get no argument and you want
                                  to set the 'forget' param, use None for cmd_param.
                    - forget    : (bool) If this flag is set to true, this means that the client
                                  does not care at all about the server answer and will even
                                  not try to get it. Default value is False. Please,
                                  note that device re-connection will not take place (in case
                                  it is needed) if the fire and forget mode is used. Therefore,
                                  an application using only fire and forget requests is not able
                                  to automatically re-connnect to device.
            Return     : (int) This call returns an asynchronous call identifier which is
                         needed to get the command result (see command_inout_reply)

            Throws     : ConnectionFailed, TypeError, anything thrown by command_query

        command_inout_asynch( self, cmd_name, callback) -> None
        command_inout_asynch( self, cmd_name, cmd_param, callback) -> None

                Execute asynchronously (callback model) a command on a device.

            Parameters :
                    - cmd_name  : (str) Command name.
                    - cmd_param : (any)It should be a value of the type expected by the
                                  command or a DeviceData object with this value inserted.
                                  It can be omitted if the command should not get any argument.
                    - callback  : Any callable object (function, lambda...) or any oject
                                  with a method named "cmd_ended".
            Return     : None

            Throws     : ConnectionFailed, TypeError, anything thrown by command_query

        .. important::
            by default, TANGO is initialized with the **polling** model. If you want
            to use the **push** model (the one with the callback parameter), you
            need to change the global TANGO model to PUSH_CALLBACK.
            You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

        .. important::
            Multiple asynchronous calls are not guaranteed to be executed by the device
            server in the same order they are invoked by the client.  E.g., a call
            to ``command_inout_asynch("A")`` followed immediately with a call to
            ``command_inout_asynch("B")`` could result in the device invoking
            command ``B`` before command ``A``.

        .. versionchanged:: 10.0.0
            TypeError's for invalid command input arguments are now more detailed.
            For commands with a DEV_STRING input argument, invalid data will now raise TypeError instead of SystemError.
        """
    def command_inout_raw(self, cmd_name, cmd_param=None):
        """command_inout_raw( self, cmd_name, cmd_param=None) -> DeviceData

            Execute a command on a device. Does not convert result.

        :param cmd_name: Command name
        :type value: str

        :param cmd_param: It should be a value of the type expected by the command or a DeviceData object with this value inserted.
                          It can be omitted if the command should not get any argument.
        :type cmd_param: Any

        :returns: The result of the command. The type depends on the command. It may be None
        :rtype: Any

        :throws: TypeError: if cmd_param's type is not compatible with the command
        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: :obj:`tango.DeviceUnlocked`: Raised in case of a device failure.

        .. versionchanged:: 10.0.0
            TypeError's for invalid command input arguments are now more detailed.
            For commands with a DEV_STRING input argument, invalid data will now raise TypeError instead of SystemError.
        """
    def command_inout_reply(self, idx, timeout=None):
        """command_inout_reply(self, idx, timeout=None) -> DeviceData

            Check if the answer of an asynchronous command_inout is arrived
            (polling model). If the reply is arrived and if it is a valid
            reply, it is returned to the caller in a DeviceData object. If
            the reply is an exception, it is re-thrown by this call. If optional
            `timeout` parameter is not provided an exception is also thrown in case
            of the reply is not yet arrived. If `timeout` is provided, the call will
            wait (blocking the process) for the time specified
            in timeout. If after timeout milliseconds, the reply is still
            not there, an exception is thrown. If timeout is set to 0, the
            call waits until the reply arrived.

        Parameters :
            - idx      : (int) Asynchronous call identifier.
            - timeout  : (int) (optional) Milliseconds to wait for the reply.
        Return     : (DeviceData)
        Throws     : AsynCall, AsynReplyNotArrived, CommunicationFailed, DevFailed from device
        """
    @typing.overload
    def command_inout_reply_raw(self, id: typing.SupportsInt) -> DeviceData:
        """command_inout_reply_raw(self, id) -> DeviceData

            Check if the answer of an asynchronous command_inout is arrived
            (polling model). If the reply is arrived and if it is a valid
            reply, it is returned to the caller in a DeviceData object. If
            the reply is an exception, it is re-thrown by this call. An
            exception is also thrown in case of the reply is not yet arrived.

        Parameters :
            - id      : (int) Asynchronous call identifier.
        Return     : (DeviceData)
        Throws     : AsynCall, AsynReplyNotArrived, CommunicationFailed, DevFailed from device
        """
    @typing.overload
    def command_inout_reply_raw(
        self, id: typing.SupportsInt, timeout: typing.SupportsInt
    ) -> DeviceData:
        """command_inout_reply_raw(self, id, timeout) -> DeviceData

            Check if the answer of an asynchronous command_inout is arrived
            (polling model). id is the asynchronous call identifier. If the
            reply is arrived and if it is a valid reply, it is returned to
            the caller in a DeviceData object. If the reply is an exception,
            it is re-thrown by this call. If the reply is not yet arrived,
            the call will wait (blocking the process) for the time specified
            in timeout. If after timeout milliseconds, the reply is still
            not there, an exception is thrown. If timeout is set to 0, the
            call waits until the reply arrived.

        Parameters :
            - id      : (int) Asynchronous call identifier.
            - timeout : (int)
        Return     : (DeviceData)
        Throws     : AsynCall, AsynReplyNotArrived, CommunicationFailed, DevFailed from device
        """
    def connect(self, corba_name: str) -> None:
        """connect(self, corba_name) -> None

            Creates a connection to a TANGO device using it's stringified
            CORBA reference i.e. IOR or corbaloc.

        Parameters :
            - corba_name : (str) Name of the CORBA object
        Return     : None

        New in PyTango 7.0.0
        """
    def dev_name(self) -> str:
        """dev_name(self) -> str

        Return the device name as it is stored locally

        Parameters : None
        Return     : (str)
        """
    def get_access_control(self) -> AccessControlType:
        """get_access_control(self) -> AccessControlType

            Returns the current access control type

        Parameters : None
        Return     : (AccessControlType) The current access control type

        New in PyTango 7.0.0
        """
    def get_access_right(self) -> AccessControlType:
        """get_access_right(self) -> AccessControlType

            Returns the current access control type

        Parameters : None
        Return     : (AccessControlType) The current access control type

        New in PyTango 8.0.0
        """
    @typing.overload
    def get_asynch_replies(self) -> None:
        """get_asynch_replies(self) -> None

            Try to obtain data returned by a command asynchronously
            requested. This method does not block if the reply has not yet
            arrived. It fires callback for already arrived replies.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
        """
    @typing.overload
    def get_asynch_replies(self, call_timeout: typing.SupportsInt) -> None:
        """get_asynch_replies(self, call_timeout) -> None

            Try to obtain data returned by a command asynchronously
            requested. This method blocks for the specified timeout if the
            reply is not yet arrived. This method fires callback when the
            reply arrived. If the timeout is set to 0, the call waits
            undefinitely for the reply

        Parameters :
            - call_timeout : (int) timeout in miliseconds
        Return     : None

        New in PyTango 7.0.0
        """
    def get_db_host(self) -> str:
        """get_db_host(self) -> str

            Returns a string with the database host.

        Parameters : None
        Return     : (str)

        New in PyTango 7.0.0
        """
    def get_db_port(self) -> str:
        """get_db_port(self) -> str

            Returns a string with the database port.

        Parameters : None
        Return     : (str)

        New in PyTango 7.0.0
        """
    def get_db_port_num(self) -> int:
        """get_db_port_num(self) -> int

            Returns an integer with the database port.

        Parameters : None
        Return     : (int)

        New in PyTango 7.0.0
        """
    def get_dev_host(self) -> str:
        """get_dev_host(self) -> str

            Returns the current host

        Parameters : None
        Return     : (str) the current host

        New in PyTango 7.2.0
        """
    def get_dev_port(self) -> str:
        """get_dev_port(self) -> str

            Returns the current port

        Parameters : None
        Return     : (str) the current port

        New in PyTango 7.2.0
        """
    def get_from_env_var(self) -> bool:
        """get_from_env_var(self) -> bool

            Returns True if determined by environment variable or
            False otherwise

        Parameters : None
        Return     : (bool)

        New in PyTango 7.0.0
        """
    def get_idl_version(self) -> int:
        """get_idl_version(self) -> int

            Get the version of the Tango Device interface implemented
            by the device

        Parameters : None
        Return     : (int)
        """
    def get_source(self) -> DevSource:
        """get_source(self) -> DevSource

            Get the data source(device, polling buffer, polling buffer
            then device) used by command_inout or read_attribute methods

        Parameters : None
        Return     : (DevSource)
        Example    :
                    source = dev.get_source()
                    if source == DevSource.CACHE_DEV : ...
        """
    def get_timeout_millis(self) -> int:
        """get_timeout_millis(self) -> int

            Get the client side timeout in milliseconds

        Parameters : None
        Return     : (int)
        """
    def get_transparency_reconnection(self) -> bool:
        """get_transparency_reconnection(self) -> bool

            Returns the device transparency reconnection flag.

        Parameters : None
        Return     : (bool) True if transparency reconnection is set
                            or False otherwise
        """
    def is_dbase_used(self) -> bool:
        """is_dbase_used(self) -> bool

            Returns if the database is being used

        Parameters : None
        Return     : (bool) True if the database is being used

        New in PyTango 7.2.0
        """
    def reconnect(self, db_used: bool) -> None:
        """reconnect(self, db_used) -> None

            Reconnecto to a CORBA object.

        Parameters :
            - db_used : (bool) Use thatabase
        Return     : None

        New in PyTango 7.0.0
        """
    def set_access_control(self, acc: AccessControlType) -> None:
        """set_access_control(self, acc) -> None

            Sets the current access control type

        Parameters :
            - acc: (AccessControlType) the type of access
                   control to set
        Return     : None

        New in PyTango 7.0.0
        """
    def set_source(self, source: DevSource) -> None:
        """set_source(self, source) -> None

            Set the data source(device, polling buffer, polling buffer
            then device) for command_inout and read_attribute methods.

        Parameters :
            - source: (DevSource) constant.
        Return     : None
        Example    :
                    dev.set_source(DevSource.CACHE_DEV)
        """
    def set_timeout_millis(self, timeout_ms: typing.SupportsInt) -> None:
        """set_timeout_millis(self, timeout_ms) -> None

            Set client side timeout for device in milliseconds. Any method
            which takes longer than this time to execute will throw an
            exception

        Parameters :
            - timeout_ms : (int) integer value of timeout in milliseconds
        Return     : None
        Example    :
                    dev.set_timeout_millis(1000)
        """
    def set_transparency_reconnection(self, yesno: bool) -> None:
        """set_transparency_reconnection(self, yesno) -> None

            Set the device transparency reconnection flag

        Parameters :
            "    - val : (bool) True to set transparency reconnection
            "                   or False otherwise
        Return     : None
        """

class ConnectionFailed(DevFailed): ...

class DServer(Device_6Impl):
    def add_event_heartbeat(self) -> None:
        """add_event_heartbeat(self) -> None

        Command to ask the heartbeat thread to send the event heartbeat every 9 seconds
        """
    def add_obj_polling(
        self,
        argin: tuple[list[int], list[str]],
        with_db_upd: bool = True,
        delta_ms: typing.SupportsInt = 0,
    ) -> None:
        """add_obj_polling(self, argin, with_db_upd, delta_ms) -> None

            command to add one object to be polled

        :param argin:
            The polling parameters, as a sequence of two sequences.
            First, a list of integers, index 0:  update period in milliseconds.
            Second, a list of strings:
                index 0: device name,
                index 1: object type, either "command" or "attribute",
                index 2: object name.
            Example:  ([2000], ["sys/tg_test/1", "attribute", "double_scalar"])
        :type argin: tuple[list[int], list[str]]

        :param with_db_upd: set to true if db has to be updated
        :type with_db_upd: bool

        :param delta_ms:
        :type delta_ms: int
        """
    def delete_devices(self) -> None:
        """delete_devices(self) -> None

        Call destructor for all objects registered in the server
        """
    def dev_lock_status(self, dev_name: str) -> tuple[list[int], list[str]]:
        """dev_lock_status(self, dev_name: str) -> tuple[list[int], list[str]]

            command to get device lock status

        :param dev_name: device name
        :type dev_name: str

        :return: device lock status
        :rtype: tuple[list[int], list[str]]
        """
    def dev_poll_status(self, arg0: str) -> list[str]:
        """dev_poll_status(self, dev_name) -> list[str]

            Command to read device polling status

        :param dev_name: The device name
        :type dev_name: str

        :return: The device polling status as a string (multiple lines)
        :rtype: list[str]
        """
    def get_fqdn(self) -> str: ...
    def get_full_name(self) -> str: ...
    def get_instance_name(self) -> str: ...
    def get_opt_pool_usage(self) -> bool: ...
    def get_personal_name(self) -> str: ...
    def get_poll_th_conf(self) -> StdStringVector: ...
    def get_poll_th_pool_size(self) -> int: ...
    def get_process_name(self) -> str: ...
    def kill(self) -> None:
        """kill(self) -> KillThread

            Command to kill the device server process. This is done by starting a thread which will kill the process.
            Starting a thread allows the client to receive something from the server before it is killed

        :return: killing thread
        :rtype: KillThread
        """
    def lock_device(self, in_data: tuple[list[int], list[str]]) -> None:
        """lock_device(self, in_data: tuple[list[int], list[str]]) -> None

            command to lock device

        :param in_data: a structure with: (lock validity, name of the device(s) to be locked,)
        :type in_data: tuple[list[int], list[str]]
        """
    def polled_device(self) -> list[str]:
        """polled_device(self) -> list[str]

            Command to read all the devices actually polled by the device server

        :return: The device name list in a strings sequence
        :rtype: list[str]
        """
    def query_class(self) -> list[str]:
        """query_class(self) -> list[str]

            Command to read all the classes used in a device server process

        :return: The class name list in a strings sequence
        :rtype: list[str]
        """
    def query_dev_prop(self, arg0: str) -> list[str]:
        """query_dev_prop(self) -> list[str]

            Command to return the list of property device at device level for the specified class

        :return: the list of property device
        :rtype: list[str]
        """
    def query_device(self) -> list[str]:
        """query_device(self) -> list[str]

            Command to read all the devices implemented by a device server process

        :return: The device name list in a strings sequence
        :rtype: list[str]
        """
    def query_sub_device(self) -> list[str]:
        """query_sub_device(self) -> list[str]

            Command to read all the sub devices used by a device server process

        :return: The sub device name list in a sequence of strings
        :rtype: list[str]
        """
    def re_lock_devices(self, in_data: list[str]) -> None:
        """un_lock_device(self, in_data: tuple[list[int], list[str]]) -> None

            command to relock device

        :param in_data: a structure with: (lock validity, name of the device(s) to be relocked)
        :type in_data: tuple[list[int], list[str]]
        """
    def rem_event_heartbeat(self) -> None:
        """rem_event_heartbeat(self) -> None

        Command to ask the heartbeat thread to stop sending the event heartbeat
        """
    def rem_obj_polling(self, argin: list[str], with_db_upd: bool = True) -> None:
        """rem_obj_polling(self, argin, with_db_upd) -> None

            command to remove an already polled object from the device polled object list

        :param argin: The polling parameters: device name; object type (command or attribute); object name
        :type argin: list[str]

        :param with_db_upd: set to true if db has to be updated
        :type with_db_upd: bool
        """
    def restart(self, d_name: str) -> None:
        """restart(self, d_name) -> None

            Command to restart a device

        :param d_name: The device name to be re-started
        :type d_name: str
        """
    def restart_server(self) -> None:
        """restart_server(self) -> None
                    Command to restart a server (all devices embedded within the server))
                doc")
        .def("query_class_prop",
             &Tango::DServer::query_class_prop,
             R"doc(
                query_class_prop(self) -> list[str]

                    Command to return the list of property device at class level for the specified class

                :return: the list of property device
                :rtype: list[str]
        """
    def start_logging(self) -> None: ...
    def start_polling(self) -> None:
        """start_polling(self) -> None

        Command to start the polling thread
        """
    def stop_logging(self) -> None: ...
    def stop_polling(self) -> None:
        """stop_polling(self) -> None

        Command to stop the polling thread
        """
    def un_lock_device(self, in_data: tuple[list[int], list[str]]) -> int:
        """un_lock_device(self, in_data: tuple[list[int], list[str]]) -> int

            command to unlock device

        :param in_data: a structure with: (lock validity, name of the device(s) to be unlocked)
        :type in_data: tuple[list[int], list[str]]

        :return:
        :rtype: int
        """
    def upd_obj_polling_period(
        self, argin: tuple[list[int], list[str]], with_db_upd: bool = True
    ) -> None:
        """upd_obj_polling_period(self, argin, with_db_upd) -> None

            command to update an already polled object update period

        :param argin:
            The polling parameters, as a sequence of two sequences.
            First, a list of integers, index 0:  update period in milliseconds.
            Second, a list of strings:
                index 0: device name,
                index 1: object type, either "command" or "attribute",
                index 2: object name.
            Example:  ([2000], ["sys/tg_test/1", "attribute", "double_scalar"])
        :type argin: tuple[list[int], list[str]]

        :param with_db_upd: set to true if db has to be updated
        :type with_db_upd: bool
        """

class DataReadyEventData:
    """This class is used to pass data to the callback method when an
    attribute data ready event (:obj:`tango.EventType.DATA_READY_EVENT`)
    is sent to the client. It contains the
    following public fields:

        - device : (DeviceProxy) The DeviceProxy object on which the call was executed
        - attr_name : (str) The attribute name
        - event : (str) The event type name
        - event_reason : (EventReason) The reason for the event
        - attr_data_type : (int) The attribute data type
        - ctr : (int) The user counter. Set to 0 if not defined when sent by the
          server
        - err : (bool) A boolean flag set to true if the request failed. False
          otherwise
        - errors : (sequence<DevError>) The error stack
        - reception_date: (TimeVal)

        New in PyTango 7.0.0
    """

    attr_name: str
    device: DeviceProxy
    err: bool
    event: str
    event_reason: EventReason
    reception_date: TimeVal
    @typing.overload
    def __init__(self, arg0: DataReadyEventData) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal

            Returns the timestamp of the event.

        :returns: the timestamp of the event
        :rtype: TimeVal

        New in PyTango 7.0.0
        """
    @property
    def attr_data_type(self) -> int: ...
    @attr_data_type.setter
    def attr_data_type(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def ctr(self) -> int: ...
    @ctr.setter
    def ctr(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def errors(self) -> list[DevError]: ...
    @errors.setter
    def errors(self, arg1: typing.Any) -> None: ...

class Database(Connection):
    """Database is the high level Tango object which contains the link to the static database.
    Database provides methods for all database commands : get_device_property(),
    put_device_property(), info(), etc..
    To create a Database, use the default constructor. Example::

        db = Database()

    The constructor uses the TANGO_HOST env. variable to determine which
    instance of the Database to connect to.

    If TANGO_HOST env is not set, or you want to connect to a specific database, you can provide host and port to constructor:

         db = Database(host: str, port: int)

         or:

         db = Database(host: str, port: str)

    Alternatively, it is possible to start Database using file instead of a real database:

        db = Database(filename: str)
    """
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, database: Database) -> None: ...
    @typing.overload
    def __init__(self, host: str, port: typing.SupportsInt) -> None: ...
    @typing.overload
    def __init__(self, trl: str) -> None: ...
    @typing.overload
    def __init__(self, host: str, port: str) -> None: ...
    def __repr__(self): ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self): ...
    def _add_server(self, serv_name: str, dev_info: DbDevInfos) -> None:
        """_add_server(self, serv_name, dev_info) -> None

            Add a group of devices to the database.
            This corresponds to the pure C++ API call.

        Parameters :
            - serv_name : (str) server name
            - dev_info : (DbDevInfos) server device(s) information
        Return     : None
        """
    def _delete_class_attribute_property(self, class_name: str, props: DbData) -> None:
        """_delete_class_attribute_property(self, class_name, props) -> None

            Delete a list of attribute properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props : (DbData) attribute property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _delete_class_property(self, class_name: str, props: DbData) -> None:
        """_delete_class_property(self, class_name, props) -> None

            Delete a list of properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props  : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _delete_device_attribute_property(self, dev_name: str, props: DbData) -> None:
        """_delete_device_attribute_property(self, dev_name, props) -> None

            Delete a list of attribute properties for the specified device.
            The attribute names are specified by the vector of DbDatum structures. Here
            is an example of how to delete the unit property of the velocity attribute of
            the id11/motor/1 device using this method :

            db_data = tango.DbData();
            db_data.append(DbDatum("velocity"));
            db_data.append(DbDatum("unit"));
            db.delete_device_attribute_property("id11/motor/1", db_data);

            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) server name
            - props : (DbData) attribute property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _delete_device_property(self, dev_name: str, props: DbData) -> None:
        """_delete_device_property(self, dev_name, props) -> None

            Delete a list of properties for the specified device.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property names to be deleted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _delete_property(self, obj_name: str, props: DbData) -> None:
        """_delete_property(self, obj_name, props) -> None

            Delete a list of properties for the specified object.
            This corresponds to the pure C++ API call.

        Parameters :
            - obj_name : (str) object name
            - props : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _export_server(self, dev_info: DbDevExportInfos) -> None:
        """_export_server(self, dev_info) -> None

            Export a group of devices to the database.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_info : (DbDevExportInfos) device(s) to export information
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _get_class_attribute_property(self, class_name: str, props: DbData) -> None:
        """_get_class_attribute_property(self, class_name, props) -> None

            Query the database for a list of class attribute properties for
            the specified object. The attribute names are returned with the
            number of properties specified as their value. The first DbDatum
            element of the returned DbData vector contains the first
            attribute name and the first attribute property number. The
            following DbDatum element contains the first attribute property
            name and property values.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props [in,out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _get_class_property(self, class_name: str, props: DbData) -> None:
        """_get_class_property(self, class_name, props) -> None

            Query the database for a list of class properties. The property
            names are specified by the DbData (seq<DbDatum>) structures.
            The method returns the properties in the same DbDatum structures.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props [in, out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _get_device_attribute_property(self, dev_name: str, props: DbData) -> None:
        """_get_device_attribute_property(self, dev_name, props) -> None

            Query the database for a list of device attribute properties for
            the specified device. The attribute names are specified by the
            DbData (seq<DbDatum>) structures. The method returns all the
            properties for the specified attributes in the same DbDatum structures.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props [in, out] : (DbData) attribute names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _get_device_property(self, dev_name: str, props: DbData) -> None:
        """_get_device_property(self, dev_name, props) -> None

            Query the database for a list of device properties for the
            specified device. The property names are specified by the
            DbData (seq<DbDatum>) structures. The method returns the
            properties in the same DbDatum structures
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    @typing.overload
    def _get_device_property_list(self, dev_name: str, wildcard: str) -> DbDatum:
        """_get_device_property_list(self, dev_name, wildcard) -> DbDatum

            Query the database for a list of properties defined for the
            specified device and which match the specified wildcard.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - wildcard : (str) property name wildcard
        Return     : DbDatum containing the list of property names or None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    @typing.overload
    def _get_device_property_list(
        self, dev_name: str, wildcard: str, container: StdStringVector, dsc: ... = None
    ) -> None:
        """_get_device_property_list(self, dev_name, wildcard, container) -> None

            Query the database for a list of properties defined for the
            specified device and which match the specified wildcard.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - wildcard : (str) property name wildcard
            - container [out] : (StdStringVector) array that will contain the matching
                                property names
        Return     : DbDatum containing the list of property names or None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _get_property(self, obj_name: str, props: DbData) -> None:
        """_get_property(self, obj_name, props) -> None

            Query the database for a list of object (i.e non-device)
            properties. The property names are specified by the
            DbData (seq<DbDatum>) structures. The method returns the
            properties in the same DbDatum structures
            This corresponds to the pure C++ API call.

        Parameters :
            - obj_name : (str) object name
            - props [in, out] : (DbData) property names
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _get_property_forced(self, obj: str, db_data: DbData, dsc: ...) -> None:
        """_get_property_forced(self, obj, db_data, dsc) -> None

        :param obj:
        :type obj: str

        :param db_data:
        :type db_data: DbData

        :param dsc:
        :type dsc: DbServerCache
        """
    def _put_class_attribute_property(self, class_name: str, props: DbData) -> None:
        """_put_class_attribute_property(self, class_name, props) -> None

            Insert or update a list of attribute properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props : (DbData) property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _put_class_property(self, class_name: str, props: DbData) -> None:
        """_put_class_property(self, class_name, props) -> None

            Insert or update a list of properties for the specified class.
            This corresponds to the pure C++ API call.

        Parameters :
            - class_name : (str) class name
            - props : (DbData) property data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _put_device_attribute_property(self, dev_name: str, props: DbData) -> None:
        """_put_device_attribute_property(self, dev_name, props) -> None

            Insert or update a list of attribute properties for the specified device.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _put_device_property(self, dev_name: str, props: DbData) -> None:
        """_put_device_property(self, dev_name, props) -> None

            Insert or update a list of properties for the specified device.
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - props : (DbData) property data
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def _put_property(self, obj_name: str, value: DbData) -> None: ...
    def add_device(self, dev_info: DbDevInfo) -> None:
        """add_device(self, dev_info) -> None

            Add a device to the database. The device name, server and class
            are specified in the DbDevInfo structure

            Example :
                dev_info = DbDevInfo()
                dev_info.name = 'my/own/device'
                dev_info._class = 'MyDevice'
                dev_info.server = 'MyServer/test'
                db.add_device(dev_info)

        Parameters :
            - dev_info : (DbDevInfo) device information
        Return     : None
        """
    def add_server(self, servname, dev_info, with_dserver=False):
        """add_server( self, servname, dev_info, with_dserver=False) -> None

            Add a (group of) devices to the database. This is considered as a
            low level call because it may render the database inconsistent
            if it is not used properly.

            If *with_dserver* parameter is set to False (default), this
            call will only register the given dev_info(s). You should include
            in the list of dev_info an entry to the usually hidden **DServer**
            device.

            If *with_dserver* parameter is set to True, the call will add an
            additional **DServer** device if it is not included in the
            *dev_info* parameter.

        Example using *with_dserver=True*::

            dev_info1 = DbDevInfo()
            dev_info1.name = 'my/own/device'
            dev_info1._class = 'MyDevice'
            dev_info1.server = 'MyServer/test'
            db.add_server(dev_info1.server, dev_info1, with_dserver=True)

        Same example using *with_dserver=False*::

            dev_info1 = DbDevInfo()
            dev_info1.name = 'my/own/device'
            dev_info1._class = 'MyDevice'
            dev_info1.server = 'MyServer/test'

            dev_info2 = DbDevInfo()
            dev_info2.name = 'dserver/' + dev_info1.server
            dev_info2._class = 'DServer
            dev_info2.server = dev_info1.server

            dev_info = dev_info1, dev_info2
            db.add_server(dev_info1.server, dev_info)

        .. versionadded:: 8.1.7
            added *with_dserver* parameter

        Parameters :
            - servname : (str) server name
            - dev_info : (sequence<DbDevInfo> | DbDevInfos | DbDevInfo) containing the server device(s) information
            - with_dserver: (bool) whether or not to auto create **DServer** device in server
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def build_connection(self) -> None:
        """build_connection(self) -> None

            Tries to build a connection to the Database server.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
        """
    def check_access_control(self, dev_name: str) -> AccessControlType:
        """check_access_control(self, dev_name) -> AccessControlType

            Check the access for the given device for this client.

        Parameters :
            - dev_name : (str) device name
        Return     : the access control type as a AccessControlType object

        New in PyTango 7.0.0
        """
    def check_tango_host(self, tango_host_env: str) -> None:
        """check_tango_host(self, tango_host_env) -> None

            Check the TANGO_HOST environment variable syntax and extract
            database server host(s) and port(s) from it.

        Parameters :
            - tango_host_env : (str) The TANGO_HOST env. variable value
        Return     : None

        New in PyTango 7.0.0
        """
    def delete_attribute_alias(self, alias: str) -> None:
        """delete_attribute_alias(self, alias) -> None

            Remove the alias associated to an attribute name.

        Parameters :
            - alias : (str) alias
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def delete_class_attribute_property(self, class_name, value):
        """delete_class_attribute_property(self, class_name, value) -> None

            Delete a list of attribute properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - propnames : can be one of the following:

                1. DbData [in] - several property data to be deleted
                2. sequence<str> [in]- several property data to be deleted
                3. sequence<DbDatum> [in] - several property data to be deleted
                4. dict<str, seq<str>> keys are attribute names and value being a
                   list of attribute property names

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed
                     DevFailed from device (DB_SQLError)
        """
    def delete_class_property(self, class_name, value):
        """delete_class_property(self, class_name, value) -> None

            Delete a the given of properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - value : can be one of the following:

                1. str [in] - single property data to be deleted
                2. DbDatum [in] - single property data to be deleted
                3. DbData [in] - several property data to be deleted
                4. sequence<str> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted
                   (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names
                   to be deleted (keys are ignored)

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def delete_device(self, dev_name: str) -> None:
        """delete_device(self, dev_name) -> None

            Delete the device of the specified name from the database.

        Parameters :
            - dev_name : (str) device name
        Return     : None
        """
    def delete_device_alias(self, alias: str) -> None:
        """delete_device_alias(self, alias) -> void

            Delete a device alias

        Parameters :
            - alias : (str) alias name
        Return     : None
        """
    def delete_device_attribute_property(self, dev_name, value):
        """delete_device_attribute_property(self, dev_name, value) -> None

            Delete a list of attribute properties for the specified device.

        Parameters :
            - devname : (str) device name
            - propnames : can be one of the following:

                1. DbData [in] - several property data to be deleted
                2. sequence<str> [in]- several property data to be deleted
                3. sequence<DbDatum> [in] - several property data to be deleted
                4. dict<str, seq<str>> with each key an attribute name and the value a list of attribute property names to delete from that attribute

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def delete_device_property(self, dev_name, value):
        """delete_device_property(self, dev_name, value) -> None

        Delete a the given of properties for the specified device.

        Parameters :
            - dev_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be deleted
                2. DbDatum [in] - single property data to be deleted
                3. DbData [in] - several property data to be deleted
                4. sequence<str> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names to be deleted (keys are ignored)

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def delete_property(self, obj_name, value):
        """delete_property(self, obj_name, value) -> None

            Delete a the given of properties for the specified object.

        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be deleted
                2. DbDatum [in] - single property data to be deleted
                3. DbData [in] - several property data to be deleted
                4. sequence<string> [in]- several property data to be deleted
                5. sequence<DbDatum> [in] - several property data to be deleted
                6. dict<str, obj> [in] - keys are property names to be deleted
                   (values are ignored)
                7. dict<str, DbDatum> [in] - several DbDatum.name are property names
                   to be deleted (keys are ignored)
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def delete_server(self, server: str) -> None:
        """delete_server(self, server) -> None

            Delete the device server and its associated devices from database.

        Parameters :
            - server : (str) name of the server to be deleted with
                       format: <server name>/<instance>
        Return     : None
        """
    def delete_server_info(self, server: str) -> None:
        """delete_server_info(self, server) -> None

            Delete server information of the specified server from the database.

        Parameters :
            - server : (str) name of the server to be deleted with
                       format: <server name>/<instance>
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def dev_name(self) -> str: ...
    def export_device(self, dev_export: DbDevExportInfo) -> None:
        """export_device(self, dev_export) -> None

            Update the export info for this device in the database.

            Example :
                dev_export = DbDevExportInfo()
                dev_export.name = 'my/own/device'
                dev_export.ior = <the real ior>
                dev_export.host = <the host>
                dev_export.version = '3.0'
                dev_export.pid = '....'
                db.export_device(dev_export)

        Parameters :
            - dev_export : (DbDevExportInfo) export information
        Return     : None
        """
    def export_event(self, event_data: list[str]) -> None:
        """export_event(self, event_data) -> None

            Export an event to the database.

        Parameters :
            - event_data : (sequence<str>) event data (same as DbExportEvent Database command)
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def export_server(self, dev_info):
        """export_server(self, dev_info) -> None

            Export a group of devices to the database.

        Parameters :
            - devinfo : (sequence<DbDevExportInfo> | DbDevExportInfos | DbDevExportInfo)
                        containing the device(s) to export information
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_access_except_errors(self) -> list[DevError]:
        """get_access_except_errors(self) -> DevErrorList

            Returns a reference to the control access exceptions.

        Parameters : None
        Return     : DevErrorList

        New in PyTango 7.0.0
        """
    def get_alias(self, dev_name: str) -> str:
        """get_alias(self, dev_name) -> str

            Get the device alias name from its name.

        Parameters :
            - dev_name : (str) device name
        Return     : alias

        New in PyTango 3.0.4

        .. deprecated:: 8.1.0
            Use :meth:`~tango.Database.get_alias_from_device` instead
        """
    def get_alias_from_attribute(self, attr_name: str) -> str:
        """get_alias_from_attribute(self, attr_name) -> str

            Get the attribute alias from the full attribute name.

        Parameters :
            - attr_name : (str) full attribute name
        Return     :  attribute alias

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 8.1.0
        """
    def get_alias_from_device(self, dev_name: str) -> str:
        """get_alias_from_device(self, dev_name) -> str

            Get the device alias name from its name.

        Parameters :
            - dev_name : (str) device name
        Return     : alias

        New in PyTango 8.1.0
        """
    def get_attribute_alias(self, alias: str) -> str:
        """get_attribute_alias(self, alias) -> str

            Get the full attribute name from an alias.

        Parameters :
            - alias : (str) attribute alias
        Return     :  full attribute name

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        .. deprecated:: 8.1.0
            Use :meth:`~tango.Database.get_attribute_from_alias` instead
        """
    def get_attribute_alias_list(self, filter: str) -> DbDatum:
        """get_attribute_alias_list(self, filter) -> DbDatum

            Get attribute alias list. The parameter alias is a string to
            filter the alias list returned. Wildcard (*) is supported. For
            instance, if the string alias passed as the method parameter
            is initialised with only the * character, all the defined
            attribute alias will be returned. If there is no alias with the
            given filter, the returned array will have a 0 size.

        Parameters :
            - filter : (str) attribute alias filter
        Return     : DbDatum containing the list of matching attribute alias

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_attribute_from_alias(self, alias: str) -> str:
        """get_attribute_from_alias(self, alias) -> str

            Get the full attribute name from an alias.

        Parameters :
            - alias : (str) attribute alias
        Return     :  full attribute name

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 8.1.0
        """
    def get_class_attribute_list(self, class_name: str, wildcard: str) -> DbDatum:
        """get_class_attribute_list(self, class_name, wildcard) -> DbDatum

            Query the database for a list of attributes defined for the specified
            class which match the specified wildcard.

        Parameters :
            - class_name : (str) class name
            - wildcard : (str) attribute name
        Return     : DbDatum containing the list of matching attributes for the given class

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_class_attribute_property(self, class_name, value):
        """get_class_attribute_property( self, class_name, value) -> dict<str, dict<str, seq<str>>

            Query the database for a list of class attribute properties for the
            specified class. The method returns all the properties for the specified
            attributes.

        Parameters :
            - class_name : (str) class name
            - propnames : can be one of the following:

                1. str [in] - single attribute properties to be fetched
                2. DbDatum [in] - single attribute properties to be fetched
                3. DbData [in,out] - several attribute properties to be fetched
                   In this case (direct C++ API) the DbData will be filled with the property
                   values
                4. sequence<str> [in] - several attribute properties to be fetched
                5. sequence<DbDatum> [in] - several attribute properties to be fetched
                6. dict<str, obj> [in,out] - keys are attribute names
                   In this case the given dict values will be changed to contain the several
                   attribute property values

        Return     : a dictionary which keys are the attribute names the
                     value associated with each key being a another
                     dictionary where keys are property names and value is
                     a sequence of strings being the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_class_attribute_property_history(
        self, class_name: str, attr_name: str, prop_name: str
    ) -> DbHistoryList:
        """get_class_attribute_property_history(self, class_name, attr_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specifed class attribute
            property. Note that prop_name and attr_name can contain a wildcard character
            (eg: 'prop*').

        Parameters :
            - class_name : (str) class name
            - attr_name : (str) attribute name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_class_for_device(self, dev_name: str) -> str:
        """get_class_for_device(self, dev_name) -> str

            Return the class of the specified device.

        Parameters :
            - dev_name : (str) device name
        Return     : a string containing the device class
        """
    def get_class_inheritance_for_device(self, dev_name: str) -> DbDatum:
        """get_class_inheritance_for_device(self, dev_name) -> DbDatum

            Return the class inheritance scheme of the specified device.

        Parameters :
            - devn_ame : (str) device name
        Return     : DbDatum with the inheritance class list

        New in PyTango 7.0.0
        """
    def get_class_list(self, wildcard: str) -> DbDatum:
        """get_class_list(self, wildcard) -> DbDatum

            Query the database for a list of classes which match the specified wildcard

        Parameters :
            - wildcard : (str) class wildcard
        Return     : DbDatum containing the list of matching classes

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_class_property(self, class_name, value):
        """get_class_property(self, class_name, value) -> dict<str, seq<str>>

            Query the database for a list of class properties.

        Parameters :
            - class_name : (str) class name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. tango.DbDatum [in] - single property data to be fetched
                3. tango.DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                     associated with each key being a a sequence of strings being the
                     property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_class_property_history(self, class_name: str, props: str) -> DbHistoryList:
        """get_class_property_history(self, class_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specified class
            property. Note that propname can contain a wildcard character
            (eg: 'prop*').

        Parameters :
            - class_name : (str) class name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_class_property_list(self, class_name: str) -> DbDatum:
        """get_class_property_list(self, class_name) -> DbDatum

            Query the database for a list of properties defined for the specified class.

        Parameters :
            - class_name : (str) class name
        Return     : DbDatum containing the list of properties for the specified class

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_device_alias(self, alias: str) -> str:
        """get_device_alias(self, alias) -> str

            Get the device name from an alias.

        Parameters :
            - alias : (str) alias
        Return     : device name

        .. deprecated:: 8.1.0
            Use :meth:`~tango.Database.get_device_from_alias` instead
        """
    def get_device_alias_list(self, filter: str) -> DbDatum:
        """get_device_alias_list(self, filter) -> DbDatum

            Get device alias list. The parameter alias is a string to filter
            the alias list returned. Wildcard (*) is supported.

        Parameters :
            - filter : (str) a string with the alias filter (wildcard (*) is supported)
        Return     : DbDatum with the list of device names

        New in PyTango 7.0.0
        """
    def get_device_attribute_list(
        self, dev_name: str, att_list: StdStringVector
    ) -> None:
        """get_device_attribute_list(self, dev_name, att_list) -> None

            Get the list of attribute(s) with some data defined in database
            for a specified device. Note that this is not the list of all
            device attributes because not all attribute(s) have some data
            in database
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) device name
            - att_list [out] : (StdStringVector) array that will contain the
                               attribute name list
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_device_attribute_property(self, dev_name, value):
        """get_device_attribute_property(self, dev_name, value) -> dict<str, dict<str, seq<str>>>

            Query the database for a list of device attribute properties for the
            specified device. The method returns all the properties for the specified
            attributes.

        Parameters :
            - dev_name : (string) device name
            - value : can be one of the following:

                1. str [in] - single attribute properties to be fetched
                2. DbDatum [in] - single attribute properties to be fetched
                3. DbData [in,out] - several attribute properties to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several attribute properties to be fetched
                5. sequence<DbDatum> [in] - several attribute properties to be fetched
                6. dict<str, obj> [in,out] - keys are attribute names
                   In this case the given dict values will be changed to contain the
                   several attribute property values

        Return     :  a dictionary which keys are the attribute names the
                             value associated with each key being a another
                             dictionary where keys are property names and value is
                             a DbDatum containing the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_device_attribute_property_history(
        self, dev_name: str, attr_name: str, prop_name: str
    ) -> DbHistoryList:
        """get_device_attribute_property_history(self, dev_name, attr_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specified device
            attribute property. Note that propname and devname can contain a
            wildcard character (eg: 'prop*').

        Parameters :
            - dev_name : (str) device name
            - attr_name : (str) attribute name
            - prop_name : (str) property name

        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_device_class_list(self, server: str) -> DbDatum:
        """get_device_class_list(self, server) -> DbDatum

            Query the database for a list of devices and classes served by
            the specified server. Return a list with the following structure:
            [device name, class name, device name, class name, ...]

        Parameters :
            - server : (str) name of the server with format: <server name>/<instance>
        Return     : DbDatum containing list with the following structure:
                     [device_name, class name]

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def get_device_domain(self, wildcard: str) -> DbDatum:
        """get_device_domain(self, wildcard) -> DbDatum

            Query the database for a list of of device domain names which
            match the wildcard provided (* is wildcard for any character(s)).
            Domain names are case insensitive.

        Parameters :
            - wildcard : (str) domain filter
        Return     : DbDatum with the list of device domain names
        """
    def get_device_exported(self, filter: str) -> DbDatum:
        """get_device_exported(self, filter) -> DbDatum

            Query the database for a list of exported devices whose names
            satisfy the supplied filter (* is wildcard for any character(s))

        Parameters :
            - filter : (str) device name filter (wildcard)
        Return     : DbDatum with the list of exported devices
        """
    def get_device_exported_for_class(self, class_name: str) -> DbDatum:
        """get_device_exported_for_class(self, class_name) -> DbDatum

            Query database for list of exported devices for the specified class.

        Parameters :
            - class_name : (str) class name
        Return     : DbDatum with the list of exported devices for the

        New in PyTango 7.0.0
        """
    def get_device_family(self, wildcard: str) -> DbDatum:
        """get_device_family(self, wildcard) -> DbDatum

            Query the database for a list of of device family names which
            match the wildcard provided (* is wildcard for any character(s)).
            Family names are case insensitive.

        Parameters :
            - wildcard : (str) family filter
        Return     : DbDatum with the list of device family names
        """
    def get_device_from_alias(self, alias: str) -> str:
        """get_device_from_alias(self, alias) -> str

            Get the device name from an alias.

        Parameters :
            - alias : (str) alias
        Return     : device name

        New in PyTango 8.1.0
        """
    def get_device_info(self, dev_name: str) -> DbDevFullInfo:
        """get_device_info(self, dev_name) -> DbDevFullInfo

            Query the database for the full info of the specified device.

            Example :
                dev_info = db.get_device_info('my/own/device')
                print(dev_info.name)
                print(dev_info.class_name)
                print(dev_info.ds_full_name)
                print(dev_info.host)
                print(dev_info.exported)
                print(dev_info.ior)
                print(dev_info.version)
                print(dev_info.pid)
                print(dev_info.started_date)
                print(dev_info.stopped_date)

        Parameters :
            - dev_name : (str) device name
        Return     : DbDevFullInfo

        .. versionadded:: 8.1.0

        .. versionchanged:: 10.1.0 Added *host* field to DbDevFullInfo
        """
    def get_device_member(self, wildcard: str) -> DbDatum:
        """get_device_member(self, wildcard) -> DbDatum

            Query the database for a list of of device member names which
            match the wildcard provided (* is wildcard for any character(s)).
            Member names are case insensitive.

        Parameters :
            - wildcard : (str) member filter
        Return     : DbDatum with the list of device member names
        """
    def get_device_name(self, serv_name: str, class_name: str) -> DbDatum:
        """get_device_name(self, serv_name, class_name) -> DbDatum

            Query the database for a list of devices served by a server for
            a given device class

        Parameters :
            - serv_name : (str) server name
            - class_name : (str) device class name
        Return     : DbDatum with the list of device names
        """
    def get_device_property(self, dev_name, value):
        """get_device_property(self, dev_name, value) -> dict<str, seq<str>>

        Query the database for a list of device properties.

        Parameters :
            - dev_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. DbDatum [in] - single property data to be fetched
                3. DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                    associated with each key being a a sequence of strings being the
                    property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_device_property_history(
        self, dev_name: str, prop_name: str
    ) -> DbHistoryList:
        """get_device_property_history(self, dev_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specified device
            property. Note that propname can contain a wildcard character
            (eg: 'prop*').
            This corresponds to the pure C++ API call.

        Parameters :
            - dev_name : (str) server name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_device_property_list(self, dev_name, wildcard, array=None):
        """get_device_property_list(self, dev_name, wildcard, array=None) -> DbData

            Query the database for a list of properties defined for the
            specified device and which match the specified wildcard.
            If array parameter is given, it must be an object implementing de 'append'
            method. If given, it is filled with the matching property names. If not given
            the method returns a new DbDatum containing the matching property names.

        New in PyTango 7.0.0

        Parameters :
            - dev_name : (str) device name
            - wildcard : (str) property name wildcard
            - array : [out] (sequence) (optional) array that
                          will contain the matching property names.
        Return     : if container is None, return is a new DbDatum containing the
                     matching property names. Otherwise returns the given array
                     filled with the property names

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
        """
    def get_device_service_list(self, dev_name: str) -> DbDatum:
        """get_device_service_list(self, dev_name) -> DbDatum

            Query database for the list of services provided by the given device.

        Parameters :
            - dev_name : (str) device name
        Return     : DbDatum with the list of services

        New in PyTango 8.1.0
        """
    def get_file_name(self) -> str:
        """get_file_name(self) -> str

            Returns the database file name or throws an exception
            if not using a file database

        Parameters : None
        Return     : a string containing the database file name

        Throws     : DevFailed

        New in PyTango 7.2.0
        """
    @typing.overload
    def get_host_list(self) -> DbDatum:
        """get_host_list(self) -> DbDatum

            Returns the list of all host names registered in the database.

        Return     : DbDatum with the list of registered host names
        """
    @typing.overload
    def get_host_list(self, wildcard: str) -> DbDatum:
        """get_host_list(self, wildcard) -> DbDatum

            Returns the list of all host names registered in the database.

        Parameters :
            - wildcard : (str) (optional) wildcard (eg: 'l-c0*')
        Return     : DbDatum with the list of registered host names
        """
    def get_host_server_list(self, host_name: str) -> DbDatum:
        """get_host_server_list(self, host_name) -> DbDatum

            Query the database for a list of servers registered on the specified host.

        Parameters :
            - host_name : (str) host name
        Return     : DbDatum containing list of servers for the specified host

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def get_info(self) -> str:
        """get_info(self) -> str

            Query the database for some general info about the tables.

        Parameters : None
        Return     : a multiline string
        """
    def get_instance_name_list(self, serv_name: str) -> DbDatum:
        """get_instance_name_list(self, serv_name) -> DbDatum

            Return the list of all instance names existing in the database for the specifed server.

        Parameters :
            - serv_name : (str) server name with format <server name>
        Return     : DbDatum containing list of instance names for the specified server

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def get_object_list(self, wildcard: str) -> DbDatum:
        """get_object_list(self, wildcard) -> DbDatum

            Query the database for a list of object (free properties) for
            which properties are defined and which match the specified
            wildcard.

        Parameters :
            - wildcard : (str) object wildcard
        Return     : DbDatum containing the list of object names matching the given wildcard

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_object_property_list(self, obj_name: str, wildcard: str) -> DbDatum:
        """get_object_property_list(self, obj_name, wildcard) -> DbDatum

            Query the database for a list of properties defined for the
            specified object and which match the specified wildcard.

        Parameters :
            - obj_name : (str) object name
            - wildcard : (str) property name wildcard
        Return     : DbDatum with list of properties defined for the specified
                     object and which match the specified wildcard

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_property(self, obj_name, value):
        """get_property(self, obj_name, value) -> dict<str, seq<str>>

            Query the database for a list of object (i.e non-device) properties.

        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. DbDatum [in] - single property data to be fetched
                3. DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                     associated with each key being a a sequence of strings being
                     the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_property_forced(self, obj_name, value):
        """get_property(self, obj_name, value) -> dict<str, seq<str>>

            Query the database for a list of object (i.e non-device) properties.

        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:

                1. str [in] - single property data to be fetched
                2. DbDatum [in] - single property data to be fetched
                3. DbData [in,out] - several property data to be fetched
                   In this case (direct C++ API) the DbData will be filled with
                   the property values
                4. sequence<str> [in] - several property data to be fetched
                5. sequence<DbDatum> [in] - several property data to be fetched
                6. dict<str, obj> [in,out] - keys are property names
                   In this case the given dict values will be changed to contain
                   the several property values

        Return     : a dictionary which keys are the property names the value
                     associated with each key being a a sequence of strings being
                     the property value.

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def get_property_history(self, obj_name: str, props: str) -> DbHistoryList:
        """get_property_history(self, obj_name, prop_name) -> DbHistoryList

            Get the list of the last 10 modifications of the specifed object
            property. Note that propname can contain a wildcard character
            (eg: 'prop*')

        Parameters :
            - serv_name : (str) server name
            - prop_name : (str) property name
        Return     : DbHistoryList containing the list of modifications

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def get_server_class_list(self, server: str) -> DbDatum:
        """get_server_class_list(self, server) -> DbDatum

            Query the database for a list of classes instantiated by the
            specified server. The DServer class exists in all TANGO servers
            and for this reason this class is removed from the returned list.

        Parameters :
            - server : (str) name of the server to be deleted with
                       format: <server name>/<instance>
        Return     : DbDatum containing list of class names instanciated by
                     the specified server

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def get_server_info(self, server: str) -> DbServerInfo:
        """get_server_info(self, server) -> DbServerInfo

            Query the database for server information.

        Parameters :
            - server : (str) name of the server with format: <server name>/<instance>
        Return     : DbServerInfo with server information

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    @typing.overload
    def get_server_list(self) -> DbDatum:
        """get_server_list(self) -> DbDatum

            Return the list of all servers registered in the database.

        Return     : DbDatum containing list of registered servers
        """
    @typing.overload
    def get_server_list(self, wildcard: str) -> DbDatum:
        """get_server_list(self, wildcard) -> DbDatum

            Return the list of of matching servers
            will be returned (ex: Serial/\\\\*)

        Parameters :
            - wildcard : (str) host wildcard (ex: Serial/\\\\*)
        Return     : DbDatum containing list of registered servers
        """
    def get_server_name_list(self) -> DbDatum:
        """get_server_name_list(self) -> DbDatum

            Return the list of all server names registered in the database.

        Parameters : None
        Return     : DbDatum containing list of server names

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def get_server_release(self) -> int:
        """get_server_release(self) -> int

        :return: server version
        :rtype: int
        """
    def get_service_list(self, filter=".*"): ...
    def get_services(self, serv_name: str, inst_name: str) -> DbDatum:
        """get_services(self, serv_name, inst_name) -> DbDatum

            Query database for specified services.

        Parameters :
            - serv_name : (str) service name
            - inst_name : (str) instance name (can be a wildcard character ('*'))
        Return     : DbDatum with the list of available services

        New in PyTango 3.0.4
        """
    def import_device(self, dev_name: str) -> DbDevImportInfo:
        """import_device(self, dev_name) -> DbDevImportInfo

            Query the databse for the export info of the specified device.

            Example :
                dev_imp_info = db.import_device('my/own/device')
                print(dev_imp_info.name)
                print(dev_imp_info.exported)
                print(dev_imp_info.ior)
                print(dev_imp_info.version)

        Parameters :
            - dev_name : (str) device name
        Return     : DbDevImportInfo
        """
    def is_control_access_checked(self) -> bool:
        """is_control_access_checked(self) -> bool

            Returns True if control access is checked or False otherwise.

        Parameters : None
        Return     : (bool) True if control access is checked or False

        New in PyTango 7.0.0
        """
    def is_multi_tango_host(self) -> bool:
        """is_multi_tango_host(self) -> bool

            Returns if in multi tango host.

        Parameters : None
        Return     : True if multi tango host or False otherwise

        New in PyTango 7.1.4
        """
    def put_attribute_alias(self, attr_name: str, alias: str) -> None:
        """put_attribute_alias(self, attr_name, alias) -> None

            Set an alias for an attribute name. The attribute alias is
            specified by alias and the attribute name is specifed by
            attr_name. If the given alias already exists, a DevFailed exception
            is thrown.

        Parameters :
            - attr_name : (str) full attribute name
            - alias : (str) alias
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def put_class_attribute_property(self, class_name, value):
        """put_class_attribute_property(self, class_name, value) -> None

            Insert or update a list of properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - propdata : can be one of the following:

                1. tango.DbData - several property data to be inserted
                2. sequence<DbDatum> - several property data to be inserted
                3. dict<str, dict<str, obj>> keys are attribute names and value
                   being another dictionary which keys are the attribute property
                   names and the value associated with each key being seq<str> or
                   tango.DbDatum

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def put_class_property(self, class_name, value):
        """put_class_property(self, class_name, value) -> None

            Insert or update a list of properties for the specified class.

        Parameters :
            - class_name : (str) class name
            - value : can be one of the following:

                1. DbDatum - single property data to be inserted
                2. DbData - several property data to be inserted
                3. sequence<DbDatum> - several property data to be inserted
                4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                5. dict<str, obj> - keys are property names and str(obj) is property value
                6. dict<str, seq<str>> - keys are property names and value has data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def put_device_alias(self, dev_name: str, alias: str) -> None:
        """put_device_alias(self, dev_name, alias) -> None

            Query database for list of exported devices for the specified class.

        Parameters :
            - dev_name : (str) device name
            - alias : (str) alias name
        Return     : None
        """
    def put_device_attribute_property(self, dev_name, value):
        """put_device_attribute_property( self, dev_name, value) -> None

            Insert or update a list of properties for the specified device.

        Parameters :
            - dev_name : (str) device name
            - value : can be one of the following:

                1. DbData - several property data to be inserted
                2. sequence<DbDatum> - several property data to be inserted
                3. dict<str, dict<str, obj>> keys are attribute names and value being another
                   dictionary which keys are the attribute property names and the value
                   associated with each key being seq<str> or tango.DbDatum.

        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def put_device_property(self, dev_name, value):
        """put_device_property(self, dev_name, value) -> None

        Insert or update a list of properties for the specified device.

        Parameters :
            - dev_name : (str) object name
            - value : can be one of the following:

                1. DbDatum - single property data to be inserted
                2. DbData - several property data to be inserted
                3. sequence<DbDatum> - several property data to be inserted
                4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                5. dict<str, obj> - keys are property names and str(obj) is property value
                6. dict<str, seq<str>> - keys are property names and value has data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def put_property(self, obj_name, value):
        """put_property(self, obj_name, value) -> None

            Insert or update a list of properties for the specified object.

        Parameters :
            - obj_name : (str) object name
            - value : can be one of the following:

                1. DbDatum - single property data to be inserted
                2. DbData - several property data to be inserted
                3. sequence<DbDatum> - several property data to be inserted
                4. dict<str, DbDatum> - keys are property names and value has data to be inserted
                5. dict<str, obj> - keys are property names and str(obj) is property value
                6. dict<str, seq<str>> - keys are property names and value has data to be inserted
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def put_server_info(self, info: DbServerInfo) -> None:
        """put_server_info(self, info) -> None

            Add/update server information in the database.

        Parameters :
            - info : (DbServerInfo) new server information
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 3.0.4
        """
    def register_service(self, serv_name: str, inst_name: str, dev_name: str) -> None:
        """register_service(self, serv_name, inst_name, dev_name) -> None

            Register the specified service wihtin the database.

        Parameters :
            - serv_name : (str) service name
            - inst_name : (str) instance name
            - dev_name : (str) device name
        Return     : None

        New in PyTango 3.0.4
        """
    def rename_server(self, old_ds_name: str, new_ds_name: str) -> None:
        """rename_server(self, old_ds_name, new_ds_name) -> None

            Rename a device server process.

        Parameters :
            - old_ds_name : (str) old name
            - new_ds_name : (str) new name
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 8.1.0
        """
    def reread_filedatabase(self) -> None:
        """reread_filedatabase(self) -> None

            Force a complete refresh over the database if using a file based database.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
        """
    def set_access_checked(self, val: bool) -> None:
        """set_access_checked(self, val) -> None

            Sets or unsets the control access check.

        Parameters :
            - val : (bool) True to set or False to unset the access control
        Return     : None

        New in PyTango 7.0.0
        """
    def unexport_device(self, dev_name: str) -> None:
        """unexport_device(self, dev_name) -> None

            Mark the specified device as unexported in the database

            Example :
               db.unexport_device('my/own/device')

        Parameters :
            - dev_name : (str) device name
        Return     : None
        """
    def unexport_event(self, event: str) -> None:
        """unexport_event(self, event) -> None

            Un-export an event from the database.

        Parameters :
            - event : (str) event
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

        New in PyTango 7.0.0
        """
    def unexport_server(self, server: str) -> None:
        """unexport_server(self, server) -> None

            Mark all devices exported for this server as unexported.

        Parameters :
            - server : (str) name of the server to be unexported with
                       format: <server name>/<instance>
        Return     : None

        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)
        """
    def unregister_service(self, serv_name: str, inst_name: str) -> None:
        """unregister_service(self, serv_name, inst_name) -> None

            Unregister the specified service from the database.

        Parameters :
            - serv_name : (str) service name
            - inst_name : (str) instance name
        Return     : None

        New in PyTango 3.0.4
        """
    def write_filedatabase(self) -> None:
        """write_filedatabase(self) -> None

            Force a write to the file if using a file based database.

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
        """

class DbData:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DbDatum) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DbData) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DbData:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DbDatum: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DbData) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DbDatum]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: DbData) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: DbDatum) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DbData) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: DbDatum) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DbDatum) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DbData) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DbDatum) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DbDatum:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DbDatum:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DbDatum) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DbDatum:
    """A single database value which has a name, type, address and value
    and methods for inserting and extracting C++ native types. This is
    the fundamental type for specifying database properties. Every
    property has a name and has one or more values associated with it.
    A status flag indicates if there is data in the DbDatum object or
    not. An additional flag allows the user to activate exceptions.

    Note: DbDatum is extended to support the python sequence API.
          This way the DbDatum behaves like a sequence of strings.
          This allows the user to work with a DbDatum as if it was
          working with the old list of strings.

    New in PyTango 7.0.0
    """

    name: str
    value_string: StdStringVector
    def __add__(self, seq): ...
    def __contains__(self, v): ...
    def __delitem__(self, k): ...
    def __getitem__(self, k): ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, name: str) -> None: ...
    @typing.overload
    def __init__(self, db_datum: DbDatum) -> None: ...
    def __iter__(self): ...
    def __len__(self): ...
    def __mul__(self, n): ...
    def __repr__(self):
        """repr method for struct"""
    def __setitem__(self, k, v): ...
    def __str__(self):
        """str method for struct"""
    def append(self, v): ...
    def extend(self, v): ...
    def is_empty(self) -> bool:
        """is_empty(self) -> bool

            Returns True or False depending on whether the
            DbDatum object contains data or not. It can be used to test
            whether a property is defined in the database or not.

        Parameters : None
        Return     : (bool) True if no data or False otherwise.

        New in PyTango 7.0.0
        """
    def size(self) -> int:
        """size(self) -> int

            Returns the number of separate elements in the value.

        Parameters : None
        Return     : the number of separate elements in the value.

        New in PyTango 7.0.0
        """

class DbDevExportInfo:
    """A structure containing export info for a device (should be
    retrieved from the database) with the following members:

        - name : (str) device name
        - ior : (str) CORBA reference of the device
        - host : name of the computer hosting the server
        - version : (str) version
        - pid : process identifier
    """

    host: str
    ior: str
    name: str
    version: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def pid(self) -> int: ...
    @pid.setter
    def pid(self, arg0: typing.SupportsInt) -> None: ...

class DbDevExportInfos:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DbDevExportInfo) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DbDevExportInfos) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DbDevExportInfos:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DbDevExportInfo: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DbDevExportInfos) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DbDevExportInfo]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: DbDevExportInfos) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: DbDevExportInfo) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DbDevExportInfos) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: DbDevExportInfo) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DbDevExportInfo) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DbDevExportInfos) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DbDevExportInfo) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DbDevExportInfo:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DbDevExportInfo:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DbDevExportInfo) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DbDevFullInfo(DbDevImportInfo):
    @property
    def class_name(self) -> str: ...
    @property
    def ds_full_name(self) -> str: ...
    @property
    def host(self) -> str: ...
    @property
    def pid(self) -> int: ...
    @property
    def started_date(self) -> str: ...
    @property
    def stopped_date(self) -> str: ...

class DbDevImportInfo:
    """A structure containing import info for a device (should be
    retrieved from the database) with the following members:

        - name : (str) device name
        - exported : 1 if device is running, 0 else
        - ior : (str)CORBA reference of the device
        - version : (str) version
    """
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def exported(self) -> int: ...
    @property
    def ior(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def version(self) -> str: ...

class DbDevImportInfos:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DbDevImportInfo) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DbDevImportInfos) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DbDevImportInfos:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DbDevImportInfo: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DbDevImportInfos) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DbDevImportInfo]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: DbDevImportInfos) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: DbDevImportInfo) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DbDevImportInfos) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: DbDevImportInfo) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DbDevImportInfo) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DbDevImportInfos) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DbDevImportInfo) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DbDevImportInfo:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DbDevImportInfo:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DbDevImportInfo) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DbDevInfo:
    """A structure containing available information for a device with
    the following members:

        - name : (str) name
        - _class : (str) device class
        - server : (str) server
    """

    _class: str
    klass: str
    name: str
    server: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""

class DbDevInfos:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DbDevInfo) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DbDevInfos) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DbDevInfos:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DbDevInfo: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DbDevInfos) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DbDevInfo]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: DbDevInfos) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: DbDevInfo) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DbDevInfos) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: DbDevInfo) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DbDevInfo) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DbDevInfos) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DbDevInfo) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DbDevInfo:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DbDevInfo:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DbDevInfo) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DbHistory:
    """A structure containing the modifications of a property. No public members."""
    @typing.overload
    def __init__(self, arg0: str, arg1: str, arg2: StdStringVector) -> None: ...
    @typing.overload
    def __init__(
        self, arg0: str, arg1: str, arg2: str, arg3: StdStringVector
    ) -> None: ...
    def get_attribute_name(self) -> str:
        """get_attribute_name(self) -> str

            Returns the attribute name (empty for object properties or device properties)

        Parameters : None
        Return     : (str) attribute name
        """
    def get_date(self) -> str:
        """get_date(self) -> str

            Returns the update date

        Parameters : None
        Return     : (str) update date
        """
    def get_name(self) -> str:
        """get_name(self) -> str

            Returns the property name.

        Parameters : None
        Return     : (str) property name
        """
    def get_value(self) -> DbDatum:
        """get_value(self) -> DbDatum

            Returns a COPY of the property value

        Parameters : None
        Return     : (DbDatum) a COPY of the property value
        """
    def is_deleted(self) -> bool:
        """is_deleted(self) -> bool

            Returns True if the property has been deleted or False otherwise

        Parameters : None
        Return     : (bool) True if the property has been deleted or False otherwise
        """

class DbHistoryList:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DbHistory) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DbHistoryList) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DbHistoryList:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DbHistory: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DbHistoryList) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DbHistory]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: DbHistoryList) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: DbHistory) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DbHistoryList) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: DbHistory) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DbHistory) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DbHistoryList) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DbHistory) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DbHistory:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DbHistory:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DbHistory) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DbServerData:
    """A structure used for moving DS from one tango host to another.
    Create a new instance by: DbServerData(<server name>, <server instance>)
    """
    def __init__(self, arg0: str, arg1: str) -> None: ...
    def already_exist(self, tg_host: str) -> bool:
        """already_exist(self, tg_host) -> bool

            Check if any of the device server process device(s) is already
            defined in the database specified by the tango host given as input arg

        Parameters :
            - tg_host : (str) The tango host for the new database
        Return     : (str) True in case any of the device is already known. False otherwise
        """
    def get_name(self) -> str:
        """get_name(self) -> str

            Returns the full server name

        Parameters : None
        Return     : (str) the full server name
        """
    def put_in_database(self, tg_host: str) -> None:
        """put_in_database(self, tg_host) -> None

            Store all the data related to the device server process in the
            database specified by the input arg.

        Parameters :
            - tg_host : (str) The tango host for the new database
        Return     : None
        """
    @typing.overload
    def remove(self) -> None:
        """remove(self) -> None

            Remove device server process from a database.

        Parameters :
            - tg_host : (str) The tango host for the new database
        Return     : None
        """
    @typing.overload
    def remove(self, tg_host: str) -> None:
        """remove(self, tg_host) -> None

            Remove device server process from a database.

        Parameters :
            - tg_host : (str) The tango host for the new database
        Return     : None
        """

class DbServerInfo:
    """A structure containing available information for a device server with
    the following members:

        - name : (str) name
        - host : (str) host
        - mode : (str) mode
        - level : (str) level
    """

    host: str
    name: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def level(self) -> int: ...
    @level.setter
    def level(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def mode(self) -> int: ...
    @mode.setter
    def mode(self, arg0: typing.SupportsInt) -> None: ...

class DevCommandInfo:
    """A device command info with the following members:

        - cmd_name : (str) command name
        - cmd_tag : command as binary value (for TACO)
        - in_type : (CmdArgType) input type
        - out_type : (CmdArgType) output type
        - in_type_desc : (str) description of input type
        - out_type_desc : (str) description of output type

    New in PyTango 7.0.0
    """
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def cmd_name(self) -> str: ...
    @property
    def cmd_tag(self) -> int: ...
    @property
    def in_type(self) -> CmdArgType: ...
    @property
    def in_type_desc(self) -> str: ...
    @property
    def out_type(self) -> CmdArgType: ...
    @property
    def out_type_desc(self) -> str: ...

class DevError:
    """Structure describing any error resulting from a command execution,
    or an attribute query, with following members:

        - reason : (str) reason
        - severity : (ErrSeverity) error severity (WARN, ERR, PANIC)
        - desc : (str) error description
        - origin : (str) Tango server method in which the error happened

    """

    desc: str
    origin: str
    reason: str
    severity: ErrSeverity
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self): ...

class DevFailed(Exception):
    def __repr__(self): ...
    def __str__(self): ...

class DevIntrChangeEventData:
    """This class is used to pass data to the callback method when a
    device interface changed event (:obj:`tango.EventType.INTERFACE_CHANGE_EVENT`)
    is sent to the client. It contains the
    following public fields:

        - device : (DeviceProxy) The DeviceProxy object on which the call was executed
        - event : (str) The event type name
        - event_reason : (EventReason) The reason for the event
        - device_name : (str) Tango device name
        - dev_started : (bool) True when event sent due to device being (re)started and with only
          a possible, but not certain, interface change
        - att_list : (AttributeInfoListEx) List of attribute details (only available in callback)
        - cmd_list : (CommandInfoList) List of command details (only available in callback)
        - err : (bool) A boolean flag set to true if the request failed. False
          otherwise
        - errors : (sequence<DevError>) The error stack
        - reception_date: (TimeVal)
    """

    dev_started: bool
    device: DeviceProxy
    device_name: str
    err: bool
    event: str
    event_reason: EventReason
    reception_date: TimeVal
    @typing.overload
    def __init__(self, arg0: DevIntrChangeEventData) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal

            Returns the timestamp of the event.

        :returns: the timestamp of the event
        :rtype: TimeVal
        """
    @property
    def errors(self) -> list[DevError]: ...
    @errors.setter
    def errors(self, arg1: typing.Any) -> None: ...

class DevSource(enum.IntEnum):
    """An enumeration representing the device source for data"""

    CACHE: typing.ClassVar[DevSource]  # value = <DevSource.CACHE: 1>
    CACHE_DEV: typing.ClassVar[DevSource]  # value = <DevSource.CACHE_DEV: 2>
    DEV: typing.ClassVar[DevSource]  # value = <DevSource.DEV: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class DevState(enum.IntEnum):
    """An enumeration representing the device state"""

    ALARM: typing.ClassVar[DevState]  # value = <DevState.ALARM: 11>
    CLOSE: typing.ClassVar[DevState]  # value = <DevState.CLOSE: 2>
    DISABLE: typing.ClassVar[DevState]  # value = <DevState.DISABLE: 12>
    EXTRACT: typing.ClassVar[DevState]  # value = <DevState.EXTRACT: 5>
    FAULT: typing.ClassVar[DevState]  # value = <DevState.FAULT: 8>
    INIT: typing.ClassVar[DevState]  # value = <DevState.INIT: 9>
    INSERT: typing.ClassVar[DevState]  # value = <DevState.INSERT: 4>
    MOVING: typing.ClassVar[DevState]  # value = <DevState.MOVING: 6>
    OFF: typing.ClassVar[DevState]  # value = <DevState.OFF: 1>
    ON: typing.ClassVar[DevState]  # value = <DevState.ON: 0>
    OPEN: typing.ClassVar[DevState]  # value = <DevState.OPEN: 3>
    RUNNING: typing.ClassVar[DevState]  # value = <DevState.RUNNING: 10>
    STANDBY: typing.ClassVar[DevState]  # value = <DevState.STANDBY: 7>
    UNKNOWN: typing.ClassVar[DevState]  # value = <DevState.UNKNOWN: 13>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class DeviceAttribute:
    """This is the fundamental type for RECEIVING data from device attributes.

    It contains several fields. The most important ones depend on the
    ExtractAs method used to get the value. Normally they are:

        - value   : Normal scalar value or numpy array of values.
        - w_value : The write part of the attribute.

    See other ExtractAs for different possibilities. There are some more
    fields, these really fixed:

        - name        : (str)
        - data_format : (AttrDataFormat) Attribute format
        - quality     : (AttrQuality)
        - time        : (TimeVal)
        - dim_x       : (int) attribute dimension x
        - dim_y       : (int) attribute dimension y
        - w_dim_x     : (int) attribute written dimension x
        - w_dim_y     : (int) attribute written dimension y
        - r_dimension : (tuple<int,int>) Attribute read dimensions.
        - w_dimension : (tuple<int,int>) Attribute written dimensions.
        - nb_read     : (int) attribute read total length
        - nb_written  : (int) attribute written total length


    And two methods:
        - get_date
        - get_err_stack
    """
    class ExtractAs(enum.IntEnum):
        """Defines what will go into value field of DeviceAttribute,
        or what will Attribute.get_write_value() return.
        Not all the possible values are valid in all the cases
        """

        ByteArray: typing.ClassVar[ExtractAs]  # value = <ExtractAs.ByteArray: 1>
        Bytes: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Bytes: 2>
        List: typing.ClassVar[ExtractAs]  # value = <ExtractAs.List: 4>
        Nothing: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Nothing: 7>
        Numpy: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Numpy: 0>
        String: typing.ClassVar[ExtractAs]  # value = <ExtractAs.String: 5>
        Tuple: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Tuple: 3>
        @staticmethod
        def __str__(*args, **kwargs):
            """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
        @classmethod
        def __new__(cls, value): ...
        def __format__(self, format_spec):
            """Convert to a string according to format_spec."""

    class except_flags(enum.IntEnum):
        failed_flag: typing.ClassVar[
            DeviceAttribute.except_flags
        ]  # value = <except_flags.failed_flag: 2>
        isempty_flag: typing.ClassVar[
            DeviceAttribute.except_flags
        ]  # value = <except_flags.isempty_flag: 0>
        numFlags: typing.ClassVar[
            DeviceAttribute.except_flags
        ]  # value = <except_flags.numFlags: 4>
        wrongtype_flag: typing.ClassVar[
            DeviceAttribute.except_flags
        ]  # value = <except_flags.wrongtype_flag: 1>
        @staticmethod
        def __str__(*args, **kwargs):
            """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
        @classmethod
        def __new__(cls, value): ...
        def __format__(self, format_spec):
            """Convert to a string according to format_spec."""

    name: str
    quality: AttrQuality
    time: TimeVal
    @staticmethod
    def __init_orig(*args, **kwargs):
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: tango._tango.DeviceAttribute) -> None

        2. __init__(self: tango._tango.DeviceAttribute, arg0: tango._tango.DeviceAttribute) -> None
        """
    def __init__(self, da=None): ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal

            Get the time at which the attribute was read by the server.

            Note: It's the same as reading the "time" attribute.

        Parameters : None
        Return     : (TimeVal) The attribute read timestamp.
        """
    def get_err_stack(self) -> list[DevError]:
        """get_err_stack(self) -> sequence<DevError>

            Returns the error stack reported by the server when the
            attribute was read.

        Parameters : None
        Return     : (sequence<DevError>)
        """
    def set_w_dim_x(self, val: typing.SupportsInt) -> None:
        """set_w_dim_x(self, val) -> None

            Sets the write value dim x.

        Parameters :
            - val : (int) new write dim x

        Return     : None

        New in PyTango 8.0.0
        """
    def set_w_dim_y(self, val: typing.SupportsInt) -> None:
        """set_w_dim_y(self, val) -> None

            Sets the write value dim y.

        Parameters :
            - val : (int) new write dim y

        Return     : None

        New in PyTango 8.0.0
        """
    @property
    def data_format(self) -> AttrDataFormat: ...
    @property
    def dim_x(self) -> int: ...
    @property
    def dim_y(self) -> int: ...
    @property
    def nb_read(self) -> int: ...
    @property
    def nb_written(self) -> int: ...
    @property
    def r_dimension(self) -> AttributeDimension: ...
    @property
    def w_dim_x(self) -> int: ...
    @property
    def w_dim_y(self) -> int: ...
    @property
    def w_dimension(self) -> AttributeDimension: ...

class DeviceAttributeConfig:
    """A base structure containing available information for an attribute
    with the following members:

        - name : (str) attribute name
        - writable : (AttrWriteType) write type (R, W, RW, R with W)
        - data_format : (AttrDataFormat) data format (SCALAR, SPECTRUM, IMAGE)
        - data_type : (int) attribute type (float, string,..)
        - max_dim_x : (int) first dimension of attribute (spectrum or image attributes)
        - max_dim_y : (int) second dimension of attribute(image attribute)
        - description : (int) attribute description
        - label : (str) attribute label (Voltage, time, ...)
        - unit : (str) attribute unit (V, ms, ...)
        - standard_unit : (str) standard unit
        - display_unit : (str) display unit
        - format : (str) how to display the attribute value (ex: for floats could be '%6.2f')
        - min_value : (str) minimum allowed value
        - max_value : (str) maximum allowed value
        - min_alarm : (str) low alarm level
        - max_alarm : (str) high alarm level
        - writable_attr_name : (str) name of the writable attribute
        - extensions : (StdStringVector) extensions (currently not used)
    """

    data_format: AttrDataFormat
    description: str
    display_unit: str
    extensions: StdStringVector
    format: str
    label: str
    max_alarm: str
    max_value: str
    min_alarm: str
    min_value: str
    name: str
    standard_unit: str
    unit: str
    writable: AttrWriteType
    writable_attr_name: str
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceAttributeConfig) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""
    @property
    def data_type(self) -> int: ...
    @data_type.setter
    def data_type(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_x(self) -> int: ...
    @max_dim_x.setter
    def max_dim_x(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def max_dim_y(self) -> int: ...
    @max_dim_y.setter
    def max_dim_y(self, arg0: typing.SupportsInt) -> None: ...

class DeviceAttributeHistory(DeviceAttribute):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceAttributeHistory) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def has_failed(self) -> bool: ...

class DeviceClass:
    """Base class for all TANGO device-class class.
    A TANGO device-class class is a class where is stored all
    data/method common to all devices of a TANGO device class
    """

    attr_list: typing.ClassVar[dict] = {}
    class_property_list: typing.ClassVar[dict] = {}
    cmd_list: typing.ClassVar[dict] = {}
    device_property_list: typing.ClassVar[dict] = {}
    @staticmethod
    def __init_orig__(*args, **kwargs):
        """__init__(self: tango._tango.DeviceClass, arg0: str) -> None"""
    def __init__(self, name): ...
    def __repr__(self): ...
    def __str__(self): ...
    def _add_device(self, device: ...) -> None: ...
    def _attribute_factory(self, attr_list_wrapper):
        """for internal usage only!!!

        Note: attempts to do anything with attr_list_wrapper here are
        not 100% save and may result either in crash or memory leak !!!
        """
    def _command_factory(self):
        """for internal usage only"""
    def _create_attribute(
        self,
        arg0: ...,
        arg1: str,
        arg2: CmdArgType,
        arg3: AttrDataFormat,
        arg4: AttrWriteType,
        arg5: typing.SupportsInt,
        arg6: typing.SupportsInt,
        arg7: DispLevel,
        arg8: typing.SupportsInt,
        arg9: bool,
        arg10: bool,
        arg11: bool,
        arg12: bool,
        arg13: bool,
        arg14: bool,
        arg15: bool,
        arg16: bool,
        arg17: bool,
        arg18: str,
        arg19: str,
        arg20: str,
        arg21: UserDefaultAttrProp,
    ) -> None: ...
    def _create_command(
        self,
        arg0: str,
        arg1: CmdArgType,
        arg2: CmdArgType,
        arg3: str,
        arg4: str,
        arg5: DispLevel,
        arg6: bool,
        arg7: typing.SupportsInt,
        arg8: str,
    ) -> None: ...
    def _create_fwd_attribute(
        self, arg0: ..., arg1: str, arg2: UserDefaultFwdAttrProp
    ) -> None: ...
    def _create_user_default_attr_prop(self, attr_name, extra_info):
        """for internal usage only"""
    def _device_destroyer(self, arg0: str) -> None: ...
    def _new_device(self, klass, dev_class, dev_name): ...
    @typing.overload
    def add_wiz_class_prop(self, name: str, desc: str) -> None:
        """add_wiz_class_prop(self, name, desc) -> None

            For internal usage only

        :param str name: class property name
        :param str desc: class property description

        :return: None
        """
    @typing.overload
    def add_wiz_class_prop(self, name: str, desc: str, default: str) -> None:
        """add_wiz_class_prop(self, name, desc, default) -> None

            For internal usage only

        :param str name: class property name
        :param str desc: class property description
        :param str default: class property default value

        :return: None
        """
    @typing.overload
    def add_wiz_dev_prop(self, name: str, desc: str) -> None:
        """add_wiz_dev_prop(self, name, desc) -> None

            For internal usage only

        :param str name: device property name
        :param str desc: device property description

        :return: None
        """
    @typing.overload
    def add_wiz_dev_prop(self, name: str, desc: str, default: str) -> None:
        """add_wiz_dev_prop(self, name, desc, default) -> None

            For internal usage only

        :param str name: device property name
        :param str desc: device property description
        :param str default: device property default value

        :return: None
        """
    def create_device(self, device_name, alias=None, cb=None):
        """create_device(self, device_name, alias=None, cb=None) -> None

            Creates a new device of the given class in the database, creates a new
            DeviceImpl for it and calls init_device (just like it is done for
            existing devices when the DS starts up)

            An optional parameter callback is called AFTER the device is
            registered in the database and BEFORE the init_device for the
            newly created device is called

        Throws tango.DevFailed:
            - the device name exists already or
            - the given class is not registered for this DS.
            - the cb is not a callable

        New in PyTango 7.1.2

        Parameters :
            - device_name : (str) the device name
            - alias : (str) optional alias. Default value is None meaning do not create device alias
            - cb : (callable) a callback that is called AFTER the device is registered
                   in the database and BEFORE the init_device for the newly created
                   device is called. Typically you may want to put device and/or attribute
                   properties in the database here. The callback must receive a parameter
                   device_name (str). Default value is None meaning no callback

        Return     : None
        """
    def delete_device(self, device_name):
        """delete_device(self, klass_name, device_name) -> None

            Deletes an existing device from the database and from this running
            server

            Throws tango.DevFailed:
                - the device name doesn't exist in the database
                - the device name doesn't exist in this DS.

        New in PyTango 7.1.2

        Parameters :
            - klass_name : (str) the device class name
            - device_name : (str) the device name

        Return     : None
        """
    def device_destroyer(self, name):
        """for internal usage only"""
    def device_factory(self, device_list):
        """for internal usage only"""
    def device_name_factory(self, dev_name_list):
        """device_name_factory(self, dev_name_list) ->  None

            Create device(s) name list (for no database device server).
            This method can be re-defined in DeviceClass sub-class for
            device server started without database. Its rule is to
            initialise class device name. The default method does nothing.

        Parameters :
            - dev_name_list : (seq<str>) sequence of devices to be filled

        Return     : None
        """
    def dyn_attr(self, device_list):
        """dyn_attr(self,device_list) -> None

            Default implementation does not do anything
            Overwrite in order to provide dynamic attributes

        Parameters :
            - device_list : (seq<DeviceImpl>) sequence of devices of this class

        Return     : None
        """
    def export_device(self, dev: ..., corba_dev_name: str = "Unused") -> None:
        """export_device(self, dev, corba_dev_name = 'Unused') -> None

            For internal usage only

        Parameters :
            - dev : (DeviceImpl) device object
            - corba_dev_name : (str) CORBA device name. Default value is 'Unused'

        Return     : None
        """
    def get_class_attr(self) -> ...:
        """get_class_attr(self) -> None

            Returns the instance of the :class:`tango.MultiClassAttribute` for the class

        :param: None

        :returns: the instance of the :class:`tango.MultiClassAttribute` for the class
        :rtype: :class:`tango.MultiClassAttribute`
        """
    def get_cmd_by_name(self, cmd_name: str) -> ...:
        """get_cmd_by_name(self, (str)cmd_name) -> tango.Command

            Get a reference to a command object.

        Parameters :
            - cmd_name : (str) command name
        Return     : (tango.Command) tango.Command object

        New in PyTango 8.0.0
        """
    def get_command_list(self) -> typing.Any:
        """get_command_list(self) -> sequence<tango.Command>

            Gets the list of tango.Command objects for this class

        Parameters : None
        Return     : (sequence<tango.Command>) list of tango.Command objects for this class

        New in PyTango 8.0.0
        """
    def get_cvs_location(self) -> str:
        """get_cvs_location(self) -> None

            Gets the cvs localtion

        Parameters : None
        Return     : (str) cvs location
        """
    def get_cvs_tag(self) -> str:
        """get_cvs_tag(self) -> str

            Gets the cvs tag

        Parameters : None
        Return     : (str) cvs tag
        """
    def get_device_list(self) -> typing.Any:
        """get_device_list(self) -> sequence<tango.DeviceImpl>

            Gets the list of tango.DeviceImpl objects for this class

        Parameters : None
        Return     : (sequence<tango.DeviceImpl>) list of tango.DeviceImpl objects for this class
        """
    def get_doc_url(self) -> str:
        """get_doc_url(self) -> str

            Get the TANGO device class documentation URL.

        Parameters : None
        Return     : (str) the TANGO device type name
        """
    def get_name(self) -> str:
        """get_name(self) -> str

            Get the TANGO device class name.

        Parameters : None
        Return     : (str) the TANGO device class name.
        """
    def get_type(self) -> str:
        """get_type(self) -> str

            Gets the TANGO device type name.

        Parameters : None
        Return     : (str) the TANGO device type name
        """
    @typing.overload
    def register_signal(self, signo: typing.SupportsInt) -> None:
        """register_signal(self, signo) -> None

            Register a signal.
            Register this class as class to be informed when signal signo
            is sent to to the device server process.
            The second version of the method is available only under Linux.

        Throws tango.DevFailed:
            - if the signal number is out of range
            - if the operating system failed to register a signal for the process.

        Parameters :
            - signo : (int) signal identifier

        Return     : None
        """
    @typing.overload
    def register_signal(self, signo: typing.SupportsInt, own_handler: bool) -> None:
        """register_signal(self, signo, own_handler) -> None

            Register a signal.
            Register this class as class to be informed when signal signo
            is sent to to the device server process.
            The second version of the method is available only under Linux.

        Throws tango.DevFailed:
            - if the signal number is out of range
            - if the operating system failed to register a signal for the process.

        Parameters :
            - signo : (int) signal identifier
            - own_handler : (bool) true if you want the device signal handler
                            to be executed in its own handler instead of being
                            executed by the signal thread. If this parameter
                            is set to true, care should be taken on how the
                            handler is written. A default false value is provided

        Return     : None
        """
    def set_type(self, dev_type: str) -> None:
        """set_type(self, dev_type) -> None

            Set the TANGO device type name.

        Parameters :
            - dev_type : (str) the new TANGO device type name
        Return     : None
        """
    def signal_handler(self, signo: typing.SupportsInt) -> None:
        """signal_handler(self, signo) -> None

            Signal handler.

            The method executed when the signal arrived in the device server process.
            This method is defined as virtual and then, can be redefined following
            device class needs.

        Parameters :
            - signo : (int) signal identifier
        Return     : None
        """
    def unregister_signal(self, signo: typing.SupportsInt) -> None:
        """unregister_signal(self, signo) -> None

            Unregister a signal.
            Unregister this class as class to be informed when signal signo
            is sent to to the device server process

        Parameters :
            - signo : (int) signal identifier
        Return     : None
        """

class DeviceData:
    """This is the fundamental type for sending and receiving data from
    device commands. The values can be inserted and extracted using the
    insert() and extract() methods.
    """
    class except_flags(enum.IntEnum):
        isempty_flag: typing.ClassVar[
            DeviceData.except_flags
        ]  # value = <except_flags.isempty_flag: 0>
        numFlags: typing.ClassVar[
            DeviceData.except_flags
        ]  # value = <except_flags.numFlags: 2>
        wrongtype_flag: typing.ClassVar[
            DeviceData.except_flags
        ]  # value = <except_flags.wrongtype_flag: 1>
        @staticmethod
        def __str__(*args, **kwargs):
            """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
        @classmethod
        def __new__(cls, value): ...
        def __format__(self, format_spec):
            """Convert to a string according to format_spec."""

    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceData) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def extract(self, extract_as: ExtractAs = ...) -> typing.Any:
        """extract(self) -> any

            Get the actual value stored in the DeviceData.

        Parameters : None
        Return     : Whatever is stored there, or None.
        """
    def get_type(self) -> CmdArgType:
        """get_type(self) -> CmdArgType

            This method returns the Tango data type of the data inside the
            DeviceData object.

        Parameters : None
        Return     : The content arg type.
        """
    def insert(self, data_type: typing.SupportsInt, value: typing.Any) -> None:
        """insert(self, data_type, value) -> None

            Inserts a value in the DeviceData.

        Parameters :
                - data_type :
                - value     : (any) The value to insert
        Return     : Whatever is stored there, or None.
        """
    def is_empty(self) -> bool:
        """is_empty(self) -> bool

            It can be used to test whether the DeviceData object has been
            initialized or not.

        Parameters : None
        Return     : True or False depending on whether the DeviceData object
                    contains data or not.
        """

class DeviceDataHistory(DeviceData):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceDataHistory) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal
            Get record polling date

        :returns: the date when the device server polling thread has executed the command
        :rtype: TimeVal
        """
    def get_err_stack(self) -> list[DevError]:
        """get_err_stack(self) -> DevErrorList

            Get record error stack

        :returns: the error stack recorded by the device server polling thread in case of the command failed when it was invoked
        :rtype: DevErrorList
        """
    def has_failed(self) -> bool:
        """has_failed(self) -> bool

            Check if the record was a failure

        :returns: a boolean set to true if the record in the polling buffer was a failure
        :rtype: bool
        """

class DeviceDataHistoryList:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DeviceDataHistory) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DeviceDataHistoryList) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DeviceDataHistoryList:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DeviceDataHistory: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceDataHistoryList) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DeviceDataHistory]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: DeviceDataHistoryList) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(
        self, arg0: typing.SupportsInt, arg1: DeviceDataHistory
    ) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DeviceDataHistoryList) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: DeviceDataHistory) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DeviceDataHistory) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DeviceDataHistoryList) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DeviceDataHistory) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DeviceDataHistory:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DeviceDataHistory:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DeviceDataHistory) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DeviceDataList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: DeviceData) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: DeviceDataList) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> DeviceDataList:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> DeviceData: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: DeviceDataList) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[DeviceData]: ...
    def __len__(self) -> int: ...
    def __ne__(self, arg0: DeviceDataList) -> bool: ...
    def __repr__(self) -> str:
        """Return the canonical string representation of this list."""
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: DeviceData) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: DeviceDataList) -> None:
        """Assign list elements using a slice object"""
    def append(self, x: DeviceData) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: DeviceData) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: DeviceDataList) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: DeviceData) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> DeviceData:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> DeviceData:
        """Remove and return the item at index ``i``"""
    def remove(self, x: DeviceData) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class DeviceImpl:
    """Base class for all TANGO device.

    This class inherits from CORBA classes where all the network layer is implemented.
    """

    _device_class_instance = None
    def __debug_stream(
        self, file: str, lineno: typing.SupportsInt, msg: str
    ) -> None: ...
    def __error_stream(
        self, file: str, lineno: typing.SupportsInt, msg: str
    ) -> None: ...
    def __fatal_stream(
        self, file: str, lineno: typing.SupportsInt, msg: str
    ) -> None: ...
    @typing.overload
    def __generic_push_event(self, attr_name: str, event_type: EventType) -> None: ...
    @typing.overload
    def __generic_push_event(
        self, attr_name: str, event_type: EventType, data: typing.Any
    ) -> None: ...
    @typing.overload
    def __generic_push_event(
        self,
        attr_name: str,
        event_type: EventType,
        data: typing.Any,
        time: typing.SupportsFloat,
        quality: AttrQuality,
    ) -> None: ...
    @typing.overload
    def __generic_push_event(
        self,
        attr_name: str,
        event_type: EventType,
        encoding: typing.Any,
        data: typing.Any,
    ) -> None: ...
    @typing.overload
    def __generic_push_event(
        self,
        attr_name: str,
        event_type: EventType,
        encoding: typing.Any,
        data: typing.Any,
        time: typing.SupportsFloat,
        quality: AttrQuality,
    ) -> None: ...
    def __info_stream(
        self, file: str, lineno: typing.SupportsInt, msg: str
    ) -> None: ...
    def __init__(
        self,
        klass: DeviceClass,
        name: str,
        description: str = "A Tango device",
        state: DevState = tango.DevState.UNKNOWN,
        status: str = "Not initialised",
    ) -> None: ...
    @typing.overload
    def __push_event(
        self, attr_name: str, filt_names: typing.Any, filt_vals: typing.Any
    ) -> None: ...
    @typing.overload
    def __push_event(
        self,
        attr_name: str,
        filt_names: typing.Any,
        filt_vals: typing.Any,
        data: typing.Any,
    ) -> None: ...
    @typing.overload
    def __push_event(
        self,
        attr_name: str,
        filt_names: typing.Any,
        filt_vals: typing.Any,
        encoding: typing.Any,
        data: typing.Any,
    ) -> None: ...
    @typing.overload
    def __push_event(
        self,
        attr_name: str,
        filt_names: typing.Any,
        filt_vals: typing.Any,
        data: typing.Any,
        time: typing.SupportsFloat,
        quality: AttrQuality,
    ) -> None: ...
    @typing.overload
    def __push_event(
        self,
        attr_name: str,
        filt_names: typing.Any,
        filt_vals: typing.Any,
        encoding: typing.Any,
        data: typing.Any,
        time: typing.SupportsFloat,
        quality: AttrQuality,
    ) -> None: ...
    def __repr__(self): ...
    def __str__(self): ...
    def __warn_stream(
        self, file: str, lineno: typing.SupportsInt, msg: str
    ) -> None: ...
    def _add_attribute(
        self,
        attr: Attr,
        read_meth_name: typing.Any,
        write_meth_name: typing.Any,
        is_allowed_meth_name: typing.Any,
    ) -> None: ...
    def _add_command(
        self,
        arg0: typing.Any,
        arg1: typing.Any,
        arg2: typing.Any,
        arg3: typing.Any,
        arg4: bool,
    ) -> None: ...
    def _disable_kernel_traces(self) -> None: ...
    def _disable_telemetry(self) -> None: ...
    def _enable_kernel_traces(self) -> None: ...
    def _enable_telemetry(self) -> None: ...
    def _get_attribute_config(self, arg0: list[str]) -> list[AttributeConfig]: ...
    def _remove_attribute(
        self, rem_attr_name: str, free_it: bool = False, clean_db: bool = True
    ) -> None: ...
    def _remove_command(
        self, rem_attr_name: str, free_it: bool = False, clean_db: bool = True
    ) -> None: ...
    def add_attribute(self, attr, r_meth=None, w_meth=None, is_allo_meth=None):
        """add_attribute(self, attr, r_meth=None, w_meth=None, is_allo_meth=None) -> Attr

        Add a new attribute to the device attribute list.

        Please, note that if you add
        an attribute to a device at device creation time, this attribute will be added
        to the device class attribute list. Therefore, all devices belonging to the
        same class created after this attribute addition will also have this attribute.

        If you pass a reference to unbound method for read, write or is_allowed method
        (e.g. DeviceClass.read_function or self.__class__.read_function),
        during execution the corresponding bound method (self.read_function) will be used.

        Note: Calling the synchronous add_attribute method from a coroutine function in
        an asyncio server may cause a deadlock.
        Use ``await`` :meth:`async_add_attribute` instead.
        However, if overriding the synchronous method ``initialize_dynamic_attributes``,
        then the synchronous add_attribute method must be used, even in asyncio servers.

        :param attr: the new attribute to be added to the list.
        :type attr: server.attribute or Attr or AttrData
        :param r_meth: the read method to be called on a read request
                       (if attr is of type server.attribute, then use the
                       fget field in the attr object instead)
        :type r_meth: callable
        :param w_meth: the write method to be called on a write request
                       (if attr is writable)
                       (if attr is of type server.attribute, then use the
                       fset field in the attr object instead)
        :type w_meth: callable
        :param is_allo_meth: the method that is called to check if it
                             is possible to access the attribute or not
                             (if attr is of type server.attribute, then use the
                             fisallowed field in the attr object instead)
        :type is_allo_meth: callable

        :returns: the newly created attribute.
        :rtype: Attr

        :raises DevFailed:
        """
    def add_command(self, cmd, device_level=True):
        """add_command(self, cmd, device_level=True) -> cmd

        Add a new command to the device command list.

        :param cmd: the new command to be added to the list
        :param device_level: Set this flag to true if the command must be added
                             for only this device

        :returns: The command to add
        :rtype: Command

        :raises DevFailed:
        """
    def add_version_info(self, key: str, value: str) -> None:
        """add_version_info(self, key, value) -> dict

            Method to add information about the module version a device is using

        :param key: Module name
        :type key: str

        :param value: Module version, or other relevant information.
        :type value: str

        .. versionadded:: 10.0.0
        """
    def append_status(self, status: str, new_line: bool = False) -> None:
        """append_status(self, status, new_line=False)

            Appends a string to the device status.

        :param status: the string to be appended to the device status
        :type status: str
        :param new_line: If true, appends a new line character before the string. Default is False
        :type new_line: bool
        """
    def async_add_attribute(self, attr, r_meth=None, w_meth=None, is_allo_meth=None):
        """async_add_attribute(self, attr, r_meth=None, w_meth=None, is_allo_meth=None) -> Attr

        Add a new attribute to the device attribute list.

        Please, note that if you add
        an attribute to a device at device creation time, this attribute will be added
        to the device class attribute list. Therefore, all devices belonging to the
        same class created after this attribute addition will also have this attribute.

        If you pass a reference to unbound method for read, write or is_allowed method
        (e.g. DeviceClass.read_function or self.__class__.read_function),
        during execution the corresponding bound method (self.read_function) will be used.

        :param attr: the new attribute to be added to the list.
        :type attr: server.attribute or Attr or AttrData
        :param r_meth: the read method to be called on a read request
                       (if attr is of type server.attribute, then use the
                       fget field in the attr object instead)
        :type r_meth: callable
        :param w_meth: the write method to be called on a write request
                       (if attr is writable)
                       (if attr is of type server.attribute, then use the
                       fset field in the attr object instead)
        :type w_meth: callable
        :param is_allo_meth: the method that is called to check if it
                             is possible to access the attribute or not
                             (if attr is of type server.attribute, then use the
                             fisallowed field in the attr object instead)
        :type is_allo_meth: callable

        :returns: the newly created attribute.
        :rtype: Attr

        :raises DevFailed:

        .. versionadded:: 10.0.0
        """
    def async_remove_attribute(self, attr_name, free_it=False, clean_db=True):
        """async_remove_attribute(self, attr_name, free_it=False, clean_db=True)

        Remove one attribute from the device attribute list.

        :param attr_name: attribute name
        :type attr_name: str

        :param free_it: free Attr object flag. Default False
        :type free_it: bool

        :param clean_db: clean attribute related info in db. Default True
        :type clean_db: bool

        :raises DevFailed:

        .. versionadded:: 10.0.0

        """
    def check_command_exists(self, cmd_name: str) -> None:
        """check_command_exists(self, cmd_name)

            Check that a command is supported by the device and
            does not need input value.

            The method throws an exception if the
            command is not defined or needs an input value.

        :param cmd_name: the command name
        :type cmd_name: str

        :raises DevFailed:
        :raises API_IncompatibleCmdArgumentType:
        :raises API_CommandNotFound:
        """
    def debug_stream(self, msg, *args, source=None):
        """debug_stream(self, msg, *args, source=None)

        Sends the given message to the tango debug stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_debug)

        :param msg: the message to be sent to the debug stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
        """
    def dev_state(self) -> DevState:
        """dev_state(self) -> DevState

            Get device state.

            Default method to get device state. The behaviour of this method depends
            on the device state. If the device state is ON or ALARM, it reads the
            attribute(s) with an alarm level defined, check if the read value is
            above/below the alarm and eventually change the state to ALARM, return
            the device state. For all th other device state, this method simply
            returns the state This method can be redefined in sub-classes in case
            of the default behaviour does not fullfill the needs.

        :returns: the device state
        :rtype: DevState

        :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading
        """
    def dev_status(self) -> str:
        """dev_status(self) -> str

            Get device status.

            Default method to get device status. It returns the contents of the device
            dev_status field. If the device state is ALARM, alarm messages are added
            to the device status. This method can be redefined in sub-classes in case
            of the default behaviour does not fullfill the needs.

        :returns: the device status
        :rtype: str

        :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading
        """
    def error_stream(self, msg, *args, source=None):
        """error_stream(self, msg, *args, source=None)

        Sends the given message to the tango error stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_error)

        :param msg: the message to be sent to the error stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
        """
    def fatal_stream(self, msg, *args, source=None):
        """fatal_stream(self, msg, *args, source=None)

        Sends the given message to the tango fatal stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_fatal)

        :param msg: the message to be sent to the fatal stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
        """
    def fill_attr_polling_buffer(self, attribute_name, attr_history_stack):
        """fill_attr_polling_buffer(self, attribute_name, attr_history_stack) -> None

            Fill attribute polling buffer with your own data. E.g.:

            .. code-block:: python

                def fill_history(self):
                    # note is such case quality will ATTR_VALID, and time_stamp will be time.time()
                    self.fill_attr_polling_buffer(attribute_name, TimedAttrData(my_new_value))

            or:

            .. code-block:: python

                def fill_history(self):
                    data = TimedAttrData(value=my_new_value,
                                         quality=AttrQuality.ATTR_WARNING,
                                         w_value=my_new_w_value,
                                         time_stamp=my_time)

                    self.fill_attr_polling_buffer(attribute_name, data)

            or:

            .. code-block:: python

                def fill_history(self):
                    data = [TimedAttrData(my_new_value),
                            TimedAttrData(error=RuntimeError("Cannot read value")]

                    self.fill_attr_polling_buffer(attribute_name, data)

        :param attribute_name: name of the attribute to fill polling buffer
        :type attribute_name: :obj:`str`

        :param attr_history_stack: data to be inserted.
        :type attr_history_stack: :obj:`tango.TimedAttrData` or list[:obj:`tango.TimedAttrData`]

        :return: None

        :raises: :obj:`tango.DevFailed`

        .. versionadded:: 10.1.0
        """
    def fill_cmd_polling_buffer(self, command_name, cmd_history_stack):
        """fill_cmd_polling_buffer(self, device, command_name, cmd_history_stack) -> None

            Fill command polling buffer with your own data. E.g.:


            .. code-block:: python

                def fill_history(self):
                    # note is such case time_stamp will be set to time.time()
                    self.fill_cmd_polling_buffer(command_name, TimedCmdData(my_new_value))

            or:

            .. code-block:: python

                def fill_history(self):
                    data = TimedCmdData(value=my_new_value,
                                         time_stamp=my_time)

                    self.fill_cmd_polling_buffer(command_name, data)

            or:

            .. code-block:: python

                def fill_history(self):
                    data = [TimedCmdData(my_new_value),
                            TimedCmdData(error=RuntimeError("Cannot read value")]

                    self.fill_cmd_polling_buffer(command_name, data)


        :param command_name: name of the command to fill polling buffer
        :type command_name: :obj:`str`

        :param cmd_history_stack: data to be inserted
        :type cmd_history_stack: :obj:`tango.TimedCmdData` or list[:obj:`tango.TimedCmdData`]

        :return: None

        :raises: :obj:`tango.DevFailed`

        .. versionadded:: 10.1.0
        """
    def get_attr_min_poll_period(self) -> StdStringVector:
        """get_attr_min_poll_period(self) -> Sequence[str]

            Returns the min attribute poll period in milliseconds

        :returns: the min attribute poll period in ms
        :rtype: Sequence[str]

        New in PyTango 7.2.0
        """
    def get_attr_poll_ring_depth(self, attr_name: str) -> int:
        """get_attr_poll_ring_depth(self, attr_name) -> int

            Returns the attribute poll ring depth.

        :param attr_name: the attribute name
        :type attr_name: str

        :returns: the attribute poll ring depth
        :rtype: int

        New in PyTango 7.1.2
        """
    def get_attribute_config(self, attr_names) -> list[tango._tango.AttributeConfig]:
        """Returns the list of :obj:`tango.AttributeConfig` for the requested names

        :param attr_names: sequence of str with attribute names, or single attribute name
        :type attr_names: list[str] | str

        :returns: :class:`tango.AttributeConfig` for each requested attribute name
        :rtype: list[:class:`tango.AttributeConfig`]

        """
    def get_attribute_poll_period(self, attr_name: str) -> int:
        """get_attribute_poll_period(self, attr_name) -> int

            Returns the attribute polling period (milliseconds) or 0 if the attribute
            is not polled.

        :param attr_name: attribute name
        :type attr_name: str

        :returns: attribute polling period (ms) or 0 if it is not polled
        :rtype: int

        New in PyTango 8.0.0
        """
    def get_client_ident(self) -> ClientAddr:
        """get_client_ident(self) -> ClientAddr | None

            Get client identification.

            This method is only useful while handling a command or
            attribute read/write. I.e., when a method has been invoked
            by a client. It will return `None` if the method was not
            invoked in the context of a client call.  E.g., called on startup,
            or called internally (e.g., from the polling loop).

            It can only be used with :obj:`tango.GreenMode.Synchronous` device
            servers. Other device servers will not have the correct context active
            at the time the attribute/command handler is running.  E.g., for an
            asyncio device server, the handler is running in the asyncio event loop
            thread.

        :returns: client identification structure
        :rtype: ClientAddr | None
        """
    def get_cmd_min_poll_period(self) -> StdStringVector:
        """get_cmd_min_poll_period(self) -> Sequence[str]

            Returns the min command poll period in milliseconds.

        :returns: the min command poll period in ms
        :rtype: Sequence[str]

        New in PyTango 7.2.0
        """
    def get_cmd_poll_ring_depth(self, cmd_name: str) -> int:
        """get_cmd_poll_ring_depth(self, cmd_name) -> int

            Returns the command poll ring depth.

        :param cmd_name: the command name
        :type cmd_name: str

        :returns: the command poll ring depth
        :rtype: int

        New in PyTango 7.1.2
        """
    def get_command_poll_period(self, cmd_name: str) -> int:
        """get_command_poll_period(self, cmd_name) -> int

            Returns the command polling period (milliseconds) or 0 if the command
            is not polled.

        :param cmd_name: command name
        :type cmd_name: str

        :returns: command polling period (ms) or 0 if it is not polled
        :rtype: int

        New in PyTango 8.0.0
        """
    def get_dev_idl_version(self) -> int:
        """get_dev_idl_version(self) -> int

            Returns the IDL version.

        :returns: the IDL version
        :rtype: int

        New in PyTango 7.1.2
        """
    def get_device_attr(self) -> MultiAttribute:
        """get_device_attr(self) -> MultiAttribute

            Get device multi attribute object.

        :returns: the device's MultiAttribute object
        :rtype: MultiAttribute
        """
    def get_device_class(self):
        """get_device_class(self)

        Get device class singleton.

        :returns: the device class singleton (device_class field)
        :rtype: DeviceClass

        """
    def get_device_properties(self, ds_class=None):
        """get_device_properties(self, ds_class = None)

        Utility method that fetches all the device properties from the database
        and converts them into members of this DeviceImpl.

        :param ds_class: the DeviceClass object. Optional. Default value is
                         None meaning that the corresponding DeviceClass object for this
                         DeviceImpl will be used
        :type ds_class: DeviceClass

        :raises DevFailed:
        """
    def get_exported_flag(self) -> bool:
        """get_exported_flag(self) -> bool

            Returns the state of the exported flag

        :returns: the state of the exported flag
        :rtype: bool

        New in PyTango 7.1.2
        """
    def get_logger(self) -> Logger:
        """get_logger(self) -> Logger

            Returns the Logger object for this device

        :returns: the Logger object for this device
        :rtype: Logger
        """
    def get_min_poll_period(self) -> int:
        """get_min_poll_period(self) -> int

            Returns the min poll period in milliseconds.

        :returns: the min poll period in ms
        :rtype: int

        New in PyTango 7.2.0
        """
    def get_name(self) -> str:
        """get_name(self) -> (str)

            Get a COPY of the device name.

        :returns: the device name
        :rtype: str
        """
    def get_non_auto_polled_attr(self) -> StdStringVector:
        """get_non_auto_polled_attr(self) -> Sequence[str]

            Returns a COPY of the list of non automatic polled attributes

        :returns: a COPY of the list of non automatic polled attributes
        :rtype: Sequence[str]

        New in PyTango 7.1.2
        """
    def get_non_auto_polled_cmd(self) -> StdStringVector:
        """get_non_auto_polled_cmd(self) -> Sequence[str]

            Returns a COPY of the list of non automatic polled commands

        :returns: a COPY of the list of non automatic polled commands
        :rtype: Sequence[str]

        New in PyTango 7.1.2
        """
    def get_poll_old_factor(self) -> int:
        """get_poll_old_factor(self) -> int

            Returns the poll old factor

        :returns: the poll old factor
        :rtype: int

        New in PyTango 7.1.2
        """
    def get_poll_ring_depth(self) -> int:
        """get_poll_ring_depth(self) -> int

            Returns the poll ring depth

        :returns: the poll ring depth
        :rtype: int

        New in PyTango 7.1.2
        """
    def get_polled_attr(self) -> StdStringVector:
        """get_polled_attr(self) -> Sequence[str]

            Returns a COPY of the list of polled attributes

        :returns: a COPY of the list of polled attributes
        :rtype: Sequence[str]

        New in PyTango 7.1.2
        """
    def get_polled_cmd(self) -> StdStringVector:
        """get_polled_cmd(self) -> Sequence[str]

            Returns a COPY of the list of polled commands

        :returns: a COPY of the list of polled commands
        :rtype: Sequence[str]

        New in PyTango 7.1.2
        """
    def get_prev_state(self) -> DevState:
        """get_prev_state(self) -> DevState

            Get a COPY of the device's previous state.

        :returns: the device's previous state
        :rtype: DevState
        """
    def get_state(self) -> DevState:
        """get_state(self) -> DevState

            Get a COPY of the device state.

        :returns: Current device state
        :rtype: DevState
        """
    def get_status(self) -> str:
        """get_status(self) -> str

            Get a COPY of the device status.

        :returns: the device status
        :rtype: str
        """
    def get_version_info(self) -> dict:
        """get_version_info(self) -> dict

            Returns a dict with versioning of different modules related to the
            pytango device.

            Example:
                {
                    "Build.PyTango.NumPy": "1.26.4",
                    "Build.PyTango.Pybind11": "3.0.1",
                    "Build.PyTango.Python": "3.12.2",
                    "Build.PyTango.cppTango":"10.0.0",
                    "NumPy": "1.26.4",
                    "PyTango": "10.0.0.dev0",
                    "Python": "3.12.2",
                    "cppTango": "10.0.0",
                    "omniORB": "4.3.2",
                    "zmq": "4.3.5"
                }


        :returns: modules version dict
        :rtype: dict

        .. versionadded:: 10.0.0
        """
    def info_stream(self, msg, *args, source=None):
        """info_stream(self, msg, *args, source=None)

        Sends the given message to the tango info stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_info)

        :param msg: the message to be sent to the info stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
        """
    def init_device(self) -> None:
        """init_device(self)

        Initialize the device.
        """
    def init_logger(self) -> None:
        """init_logger(self) -> None

        Setups logger for the device.  Called automatically when device starts.
        """
    def is_attribute_polled(self, attr_name: str) -> bool:
        """is_attribute_polled(self, attr_name) -> bool

            True if the attribute is polled.

        :param attr_name: attribute name
        :type attr_name: str

        :return: True if the attribute is polled
        :rtype: bool
        """
    def is_command_polled(self, cmd_name: str) -> bool:
        """is_command_polled(self, cmd_name) -> bool

            True if the command is polled.

        :param cmd_name: attribute name
        :type cmd_name: str

        :return: True if the command is polled
        :rtype: bool
        """
    def is_device_locked(self) -> bool:
        """is_device_locked(self) -> bool

            Returns if this device is locked by a client.

        :returns: True if it is locked or False otherwise
        :rtype: bool

        New in PyTango 7.1.2
        """
    def is_kernel_tracing_enabled(self) -> bool:
        """is_kernel_tracing_enabled(self) -> bool

            Indicates if telemetry tracing of the cppTango kernel API is enabled.

            Always False if telemetry support isn't compiled into cppTango.

        :returns: if kernel tracing is enabled
        :rtype: bool

        .. versionadded:: 10.0.0
        """
    def is_polled(self) -> bool:
        """is_polled(self) -> bool

            Returns if it is polled

        :returns: True if it is polled or False otherwise
        :rtype: bool

        New in PyTango 7.1.2
        """
    def is_telemetry_enabled(self) -> bool:
        """is_telemetry_enabled(self) -> bool

            Indicates if telemetry tracing is enabled for the device.

            Always False if telemetry support isn't compiled into cppTango.

        :returns: if device telemetry tracing is enabled
        :rtype: bool

        .. versionadded:: 10.0.0
        """
    def is_there_subscriber(self, attr_name: str, event_type: EventType) -> bool:
        """is_there_subscriber(self, attr_name, event_type) -> bool

            Check if there is subscriber(s) listening for the event.

            This method returns a boolean set to true if there are some
            subscriber(s) listening on the event specified by the two method
            arguments. Be aware that there is some delay (up to 600 sec)
            between this method returning false and the last subscriber
            unsubscription or crash...

            The device interface change event is not supported by this method.

        :param attr_name: the attribute name
        :type attr_name: str
        :param event_type: the event type
        :type event_type: EventType

        :returns: True if there is at least one listener or False otherwise
        :rtype: bool
        """
    def poll_attribute(self, attr_name: str, period_ms: typing.SupportsInt) -> None:
        """poll_attribute(self, attr_name, period_ms) -> None

            Add an attribute to the list of polled attributes.

        :param attr_name: attribute name
        :type attr_name: str

        :param period_ms: polling period in milliseconds
        :type period_ms: int

        :return: None
        :rtype: None
        """
    def poll_command(self, cmd_name: str, period_ms: typing.SupportsInt) -> None:
        """poll_command(self, cmd_name, period_ms) -> None

            Add a command to the list of polled commands.

        :param cmd_name: command name
        :type cmd_name: str

        :param period_ms: polling period in milliseconds
        :type period_ms: int

        :return: None
        :rtype: None
        """
    def push_alarm_event(self, attr_name, *args, **kwargs):
        """.. function:: push_alarm_event(self, attr_name, except)
                      push_alarm_event(self, attr_name, data)
                      push_alarm_event(self, attr_name, data, time_stamp, quality)
                      push_alarm_event(self, attr_name, str_data, data)
                      push_alarm_event(self, attr_name, str_data, data, time_stamp, quality)
            :noindex:

        Push an alarm event for the given attribute name.

        :param attr_name: attribute name
        :type attr_name: str
        :param data: the data to be sent as attribute event data. Data must be compatible with the
                     attribute type and format.
                     for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                     compatible with the attribute type
        :param str_data: special variation for DevEncoded data type. In this case 'data' must
                         be a str or an object with the buffer interface.
        :type str_data: str
        :param except: Instead of data, you may want to send an exception.
        :type except: DevFailed
        :param time_stamp: the time stamp
        :type time_stamp: double
        :param quality: the attribute quality factor
        :type quality: AttrQuality

        :raises DevFailed: If the attribute data type is not coherent.

         .. versionchanged:: 10.1.0
            Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
            determined from the data.
        """
    def push_archive_event(self, attr_name, *args, **kwargs):
        """.. function:: push_archive_event(self, attr_name, except)
                      push_archive_event(self, attr_name, data)
                      push_archive_event(self, attr_name, data, time_stamp, quality)
                      push_archive_event(self, attr_name, str_data, data)
                      push_archive_event(self, attr_name, str_data, data, time_stamp, quality)
            :noindex:

        Push an archive event for the given attribute name.

        :param attr_name: attribute name
        :type attr_name: str
        :param data: the data to be sent as attribute event data. Data must be compatible with the
                     attribute type and format.
                     for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                     compatible with the attribute type
        :param str_data: special variation for DevEncoded data type. In this case 'data' must
                         be a str or an object with the buffer interface.
        :type str_data: str
        :param except: Instead of data, you may want to send an exception.
        :type except: DevFailed
        :param time_stamp: the time stamp
        :type time_stamp: double
        :param quality: the attribute quality factor
        :type quality: AttrQuality

        :raises DevFailed: If the attribute data type is not coherent.

         .. versionchanged:: 10.1.0
            Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
            determined from the data.
        """
    def push_att_conf_event(self, attr: Attribute) -> None:
        """push_att_conf_event(self, attr)

            Push an attribute configuration event.

        :param attr: the attribute for which the configuration event
                     will be sent.
        :type attr: Attribute

        New in PyTango 7.2.1
        """
    def push_change_event(self, attr_name, *args, **kwargs):
        """.. function:: push_change_event(self, attr_name, except)
                      push_change_event(self, attr_name, data)
                      push_change_event(self, attr_name, data, time_stamp, quality)
                      push_change_event(self, attr_name, str_data, data)
                      push_change_event(self, attr_name, str_data, data, time_stamp, quality)
            :noindex:

        Push a change event for the given attribute name.

        :param attr_name: attribute name
        :type attr_name: str
        :param data: the data to be sent as attribute event data. Data must be compatible with the
                     attribute type and format.
                     for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                     compatible with the attribute type
        :param str_data: special variation for DevEncoded data type. In this case 'data' must
                         be a str or an object with the buffer interface.
        :type str_data: str
        :param except: Instead of data, you may want to send an exception.
        :type except: DevFailed
        :param time_stamp: the time stamp
        :type time_stamp: double
        :param quality: the attribute quality factor
        :type quality: AttrQuality

        :raises DevFailed: If the attribute data type is not coherent.

         .. versionchanged:: 10.1.0
            Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
            determined from the data.
        """
    def push_data_ready_event(
        self, attr_name: str, counter: typing.SupportsInt
    ) -> None:
        """push_data_ready_event(self, attr_name, counter)

            Push a data ready event for the given attribute name.

            The method needs the attribute name and a
            "counter" which will be passed within the event

        :param attr_name: attribute name
        :type attr_name: str
        :param counter: the user counter
        :type counter: int

        :raises DevFailed: If the attribute name is unknown.
        """
    def push_event(self, attr_name, filt_names, filt_vals, *args, **kwargs):
        """.. function:: push_event(self, attr_name, filt_names, filt_vals, except)
                      push_event(self, attr_name, filt_names, filt_vals, data)
                      push_event(self, attr_name, filt_names, filt_vals, str_data, data)
                      push_event(self, attr_name, filt_names, filt_vals, data, time_stamp, quality)
                      push_event(self, attr_name, filt_names, filt_vals, str_data, data, time_stamp, quality)
            :noindex:

        Push a user event for the given attribute name.

        :param attr_name: attribute name
        :type attr_name: str
        :param filt_names: unused (kept for backwards compatibility) - pass an empty list.
        :type filt_names: Sequence[str]
        :param filt_vals: unused (kept for backwards compatibility) - pass an empty list.
        :type filt_vals: Sequence[double]
        :param data: the data to be sent as attribute event data. Data must be compatible with the
                     attribute type and format.
                     for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                     compatible with the attribute type
        :param str_data: special variation for DevEncoded data type. In this case 'data' must
                         be a str or an object with the buffer interface.
        :type str_data: str
        :param except: Instead of data, you may want to send an exception.
        :type except: DevFailed
        :param time_stamp: the time stamp
        :type time_stamp: double
        :param quality: the attribute quality factor
        :type quality: AttrQuality

        :raises DevFailed: If the attribute data type is not coherent.

         .. versionchanged:: 10.1.0
            Removed optional 'dim_x' and 'dim_y' arguments. The dimensions are automatically
            determined from the data.
        """
    def register_signal(self, signo: typing.SupportsInt, own_handler: bool) -> None:
        """register_signal(self, signo, own_handler)

            Register this device as device to be informed when signal signo
            is sent to to the device server process

        :param signo: signal identifier
        :type signo: int

        :param own_handler: true if you want the device signal handler
                            to be executed in its own handler instead of being
                            executed by the signal thread. If this parameter
                            is set to true, care should be taken on how the
                            handler is written. A default false value is provided
        :type own_handler: bool
        """
    def remove_attribute(self, attr_name, free_it=False, clean_db=True):
        """remove_attribute(self, attr_name)

        Remove one attribute from the device attribute list.

        Note: Call of synchronous remove_attribute method from a coroutine function in
        an asyncio server may cause a deadlock.
        Use ``await`` :meth:`async_remove_attribute` instead.
        However, if overriding the synchronous method ``initialize_dynamic_attributes``,
        then the synchronous remove_attribute method must be used, even in asyncio servers.

        :param attr_name: attribute name
        :type attr_name: str

        :param free_it: free Attr object flag. Default False
        :type free_it: bool

        :param clean_db: clean attribute related info in db. Default True
        :type clean_db: bool

        :raises DevFailed:

        .. versionadded:: 9.5.0
            *free_it* parameter.
            *clean_db* parameter.

        """
    def remove_command(self, cmd_name, free_it=False, clean_db=True):
        """remove_command(self, cmd_name, free_it=False, clean_db=True)

        Remove one command from the device command list.

        :param cmd_name: command name to be removed from the list
        :type cmd_name: str
        :param free_it: set to true if the command object must be freed.
        :type free_it: bool
        :param clean_db: Clean command related information (included polling info
                         if the command is polled) from database.

        :raises DevFailed:
        """
    def set_alarm_event(
        self, attr_name: str, implemented: bool, detect: bool = True
    ) -> None:
        """set_alarm_event(self, attr_name, implemented, detect=True)

            Set an implemented flag for the attribute to indicate that the server fires
            alarm events manually, without the polling to be started.

            If the detect parameter is set to true, the criteria specified for the
            alarm event (rel_change and abs_change) are verified and
            the event is only pushed if a least one of them are fulfilled
            (change in value compared to previous event exceeds a threshold).
            If detect is set to false the event is fired without any value checking!

        :param attr_name: attribute name
        :type attr_name: str
        :param implemented: True when the server fires alarm events manually.
        :type implemented: bool
        :param detect: Triggers the verification of the alarm event properties
                       when set to true. Default value is true.
        :type detect: bool

        .. versionadded:: 10.0.0
        """
    def set_archive_event(
        self, attr_name: str, implemented: bool, detect: bool = True
    ) -> None:
        """set_alarm_event(self, attr_name, implemented, detect)

            Set an implemented flag for the attribute to indicate that the server fires
            archive events manually, without the polling to be started.

            If the detect parameter is set to true, the criteria specified for the
            archive event (rel_change and abs_change) are verified and
            the event is only pushed if a least one of them are fulfilled
            (change in value compared to previous event exceeds a threshold).
            If detect is set to false the event is fired without any value checking!

        :param attr_name: attribute name
        :type attr_name: str
        :param implemented: True when the server fires change events manually.
        :type implemented: bool
        :param detect: Triggers the verification of the change event properties
                        when set to true. Default value is true.
        :type detect: bool
        """
    def set_attribute_config(self, new_conf: list[AttributeConfig]) -> None:
        """set_attribute_config(self, new_conf) -> None

            Sets attribute configuration locally and in the Tango database

        :param new_conf: The new attribute(s) configuration. One AttributeConfig structure is needed for each attribute to update
        :type new_conf: list[:class:`tango.AttributeConfig`]

        :returns: None
        :rtype: None

        .. versionadded:: 10.0.0
        """
    def set_change_event(
        self, attr_name: str, implemented: bool, detect: bool = True
    ) -> None:
        """set_change_event(self, attr_name, implemented, detect=True)

            Set an implemented flag for the attribute to indicate that the server fires
            change events manually, without the polling to be started.

            If the detect parameter is set to true, the criteria specified for the
            change event (rel_change and abs_change) are verified and
            the event is only pushed if a least one of them are fulfilled
            (change in value compared to previous event exceeds a threshold).
            If detect is set to false the event is fired without any value checking!

        :param attr_name: attribute name
        :type attr_name: str
        :param implemented: True when the server fires change events manually.
        :type implemented: bool
        :param detect: Triggers the verification of the change event properties
                        when set to true. Default value is true.
        :type detect: bool
        """
    def set_data_ready_event(self, attr_name: str, implemented: bool) -> None:
        """set_alarm_event(self, attr_name, implemented)

            Set an implemented flag for the attribute to indicate that the server fires
            data ready events manually.

        :param attr_name: attribute name
        :type attr_name: str
        :param implemented: True when the server fires change events manually.
        :type implemented: bool
        """
    def set_kernel_tracing_enabled(self, enabled: bool):
        """set_kernel_tracing_enabled(self, enabled) -> None

        Enable or disable telemetry tracing of cppTango kernel methods, and
        for high-level PyTango devices, tracing of the PyTango kernel (BaseDevice)
        methods.

        This is a no-op if telemetry support isn't compiled into cppTango.

        :param enabled: True to enable kernel tracing
        :type enabled: bool

        .. versionadded:: 10.0.0
        """
    def set_state(self, new_state: DevState) -> None:
        """set_state(self, new_state)

        Set device state.

        :param new_state: the new device state
        :type new_state: DevState
        """
    def set_status(self, new_status: str) -> None:
        """set_status(self, new_status)

            Set device status.

        :param new_status: the new device status
        :type new_status: str
        """
    def set_telemetry_enabled(self, enabled: bool):
        """set_telemetry_enabled(self, enabled) -> None

        Enable or disable the device's telemetry interface.

        This is a no-op if telemetry support isn't compiled into cppTango.

        :param enabled: True to enable telemetry tracing
        :type enabled: bool

        .. versionadded:: 10.0.0
        """
    def start_logging(self) -> None:
        """start_logging(self) -> None

        Starts logging
        """
    def stop_logging(self) -> None:
        """stop_logging(self) -> None

        Stops logging
        """
    def stop_poll_attribute(self, attr_name: str) -> None:
        """stop_poll_attribute(self, attr_name) -> None

            Remove an attribute from the list of polled attributes.

        :param attr_name: attribute name
        :type attr_name: str

        :return: None
        :rtype: None
        """
    def stop_poll_command(self, cmd_name: str) -> None:
        """stop_poll_command(self, cmd_name) -> None

            Remove a command from the list of polled commands.

        :param cmd_name: cmd_name name
        :type cmd_name: str

        :return: None
        :rtype: None
        """
    @typing.overload
    def stop_polling(self) -> None:
        """stop_polling(self)

            Stop all polling for a device. if the device is polled, call this
            method before deleting it.

        New in PyTango 7.1.2
        """
    @typing.overload
    def stop_polling(self, with_db_upd: bool) -> None:
        """stop_polling(self, with_db_upd)(self)

            Stop all polling for a device. if the device is polled, call this
            method before deleting it.

        :param with_db_upd: Is it necessary to update db?
        :type with_db_upd: bool

        New in PyTango 7.1.2
        """
    def unregister_signal(self, signo: typing.SupportsInt) -> None:
        """unregister_signal(self, signo)

            Unregister this device as device to be informed when signal signo
            is sent to to the device server process

        :param signo: signal identifier
        :type signo: int
        """
    def warn_stream(self, msg, *args, source=None):
        """warn_stream(self, msg, *args, source=None)

        Sends the given message to the tango warn stream.

        Since PyTango 7.1.3, the same can be achieved with::

            print(msg, file=self.log_warn)

        :param msg: the message to be sent to the warn stream
        :type msg: str

        :param \\*args: Arguments to format a message string.

        :param source: Function that will be inspected for filename and lineno in the log message.
        :type source: Callable

        .. versionadded:: 9.4.2
            added *source* parameter
        """
    @property
    def log_debug(self): ...
    @property
    def log_error(self): ...
    @property
    def log_fatal(self): ...
    @property
    def log_info(self): ...
    @property
    def log_warn(self): ...

class DeviceInfo:
    """A structure containing available information for a device with the"
    following members:

        - dev_class : (str) device class
        - server_id : (str) server ID
        - server_host : (str) host name
        - server_version : (str) server version
        - doc_url : (str) document url
        - version_info : (dict<str, str>) version info dict

    .. versionchanged:: 10.0.0
        Added `version_info` field
    """
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def dev_class(self) -> str: ...
    @property
    def dev_type(self) -> str: ...
    @property
    def doc_url(self) -> str: ...
    @property
    def server_host(self) -> str: ...
    @property
    def server_id(self) -> str: ...
    @property
    def server_version(self) -> int: ...
    @property
    def version_info(self) -> dict: ...

class DeviceProxy(Connection):
    """DeviceProxy is the high level Tango object which provides the client with
    an easy-to-use interface to TANGO devices. DeviceProxy provides interfaces
    to all TANGO Device interfaces.The DeviceProxy manages timeouts, stateless
    connections and reconnection if the device server is restarted. To create
    a DeviceProxy, a Tango Device name must be set in the object constructor.

    Example :
       dev = tango.DeviceProxy("sys/tg_test/1")

    DeviceProxy(dev_name, green_mode=None, wait=True, timeout=True) -> DeviceProxy
    DeviceProxy(self, dev_name, need_check_acc, green_mode=None, wait=True, timeout=True) -> DeviceProxy

    Creates a new :class:`~tango.DeviceProxy`.

    :param dev_name: the device name or alias
    :type dev_name: str
    :param need_check_acc: in first version of the function it defaults to True.
                           Determines if at creation time of DeviceProxy it should check
                           for channel access (rarely used)
    :type need_check_acc: bool
    :param green_mode: determines the mode of execution of the device (including.
                      the way it is created). Defaults to the current global
                      green_mode (check :func:`~tango.get_green_mode` and
                      :func:`~tango.set_green_mode`)
    :type green_mode: :obj:`~tango.GreenMode`
    :param wait: whether or not to wait for result. If green_mode
                 Ignored when green_mode is Synchronous (always waits).
    :type wait: bool
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float
    :returns:
        if green_mode is Synchronous or wait is True:
            :class:`~tango.DeviceProxy`
        elif green_mode is Futures:
            :class:`concurrent.futures.Future`
        elif green_mode is Gevent:
            :class:`gevent.event.AsynchResult`
        elif green_mode is Asyncio:
            :class:`asyncio.Future`
    :throws:
        * :class:`~tango.DevFailed` if green_mode is Synchronous or wait is True
          and there is an error creating the device.
        * :class:`concurrent.futures.TimeoutError` if green_mode is Futures,
          wait is False, timeout is not None and the time to create the device
          has expired.
        * :class:`gevent.timeout.Timeout` if green_mode is Gevent, wait is False,
          timeout is not None and the time to create the device has expired.
        * :class:`asyncio.TimeoutError`` if green_mode is Asyncio,
          wait is False, timeout is not None and the time to create the device
          has expired.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
    """
    @staticmethod
    def __init_orig__(*args, **kwargs):
        """__init__(*args, **kwargs)
        Overloaded function.

        1. __init__(self: tango._tango.DeviceProxy) -> None

        2. __init__(self: tango._tango.DeviceProxy, name: str) -> None

        3. __init__(self: tango._tango.DeviceProxy, name: str, ch_acc: bool) -> None

        4. __init__(self: tango._tango.DeviceProxy, device: tango._tango.DeviceProxy) -> None
        """
    def __contains__(self, *args, **kwargs): ...
    def __get_attr_cache(self): ...
    def __get_attr_conf_events(self, event_id: typing.SupportsInt) -> typing.Any: ...
    def __get_callback_events(
        self,
        event_id: typing.SupportsInt,
        callback: PyEventCallBack,
        extract_as: ExtractAs = ...,
    ) -> None: ...
    def __get_cmd_cache(self): ...
    def __get_data_events(
        self, event_id: typing.SupportsInt, extract_as: ExtractAs = ...
    ) -> typing.Any: ...
    def __get_data_ready_events(self, event_id: typing.SupportsInt) -> typing.Any: ...
    def __get_devintr_change_events(
        self, event_id: typing.SupportsInt, extract_as: ExtractAs = ...
    ) -> typing.Any: ...
    def __get_event_map(self):
        """Internal helper method"""
    def __get_event_map_lock(self):
        """Internal helper method"""
    def __getattr__(self, *args, **kwargs): ...
    def __getitem__(self, *args, **kwargs): ...
    def __getstate__(self) -> tuple: ...
    def __init__(
        self,
        *args,
        green_mode=None,
        executor=None,
        threadpool=None,
        asyncio_executor=None,
    ): ...
    @typing.overload
    def __read_attributes_asynch(self, arg0: StdStringVector) -> int: ...
    @typing.overload
    def __read_attributes_asynch(
        self, attr_names: typing.Any, callback: typing.Any, extract_as: ExtractAs = ...
    ) -> None: ...
    @typing.overload
    def __read_attributes_reply(
        self, id: typing.SupportsInt, extract_as: ExtractAs = ...
    ) -> typing.Any: ...
    @typing.overload
    def __read_attributes_reply(
        self,
        id: typing.SupportsInt,
        timeout: typing.SupportsInt,
        extract_as: ExtractAs = ...,
    ) -> typing.Any: ...
    def __refresh_attr_cache(self): ...
    def __refresh_cmd_cache(self): ...
    def __repr__(self): ...
    def __setattr__(self, *args, **kwargs): ...
    def __setitem__(self, *args, **kwargs): ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self): ...
    def __subscribe_event_attrib_with_stateless_flag(
        self,
        attr_name: str,
        event: EventType,
        cb_or_queuesize: typing.Any,
        stateless: bool,
        extract_as: ExtractAs,
        filters: typing.Any,
    ) -> int: ...
    def __subscribe_event_attrib_with_sub_mode(
        self,
        attr_name: str,
        event: EventType,
        cb_or_queuesize: typing.Any,
        event_sub_mode: EventSubMode,
        extract_as: ExtractAs,
    ) -> int: ...
    def __subscribe_event_global_with_stateless_flag(
        self, event: EventType, cb: typing.Any, stateless: bool
    ) -> int: ...
    def __subscribe_event_global_with_sub_mode(
        self, event: EventType, cb: typing.Any, event_sub_mode: EventSubMode
    ) -> int: ...
    def __unsubscribe_event(self, event_id: typing.SupportsInt) -> None: ...
    def __unsubscribe_event_all(self): ...
    @typing.overload
    def __write_attributes_asynch(self, values: typing.Any) -> int: ...
    @typing.overload
    def __write_attributes_asynch(
        self, values: typing.Any, callback: typing.Any
    ) -> None: ...
    @typing.overload
    def __write_attributes_reply(self, id: typing.SupportsInt) -> None: ...
    @typing.overload
    def __write_attributes_reply(
        self, id: typing.SupportsInt, timeout: typing.SupportsInt
    ) -> None: ...
    def _delete_property(self, propname: DbData) -> None: ...
    @typing.overload
    def _get_attribute_config(
        self, attr_names: StdStringVector
    ) -> AttributeInfoList: ...
    @typing.overload
    def _get_attribute_config(self, attr_name: str) -> AttributeInfoEx: ...
    def _get_attribute_config_ex(
        self, attr_names: StdStringVector
    ) -> AttributeInfoListEx: ...
    @typing.overload
    def _get_command_config(self, attr_names: StdStringVector) -> CommandInfoList: ...
    @typing.overload
    def _get_command_config(self, attr_name: str) -> CommandInfo: ...
    def _get_info_(self):
        """Protected method that gets device info once and stores it in cache"""
    @typing.overload
    def _get_property(self, propname: str, propdata: DbData) -> None: ...
    @typing.overload
    def _get_property(self, propnames: StdStringVector, propdata: DbData) -> None: ...
    @typing.overload
    def _get_property(self, propdata: DbData) -> None: ...
    def _get_property_list(self, filter: str, array: StdStringVector) -> None: ...
    def _ping(self) -> int: ...
    def _put_property(self, propdata: DbData) -> None: ...
    def _read_attribute(
        self, attr_name: str, extract_as: ExtractAs = ...
    ) -> typing.Any: ...
    def _read_attributes(
        self, attr_names: typing.Any, extract_as: ExtractAs = ...
    ) -> typing.Any: ...
    @typing.overload
    def _set_attribute_config(self, seq: AttributeInfoList) -> None: ...
    @typing.overload
    def _set_attribute_config(self, seq: AttributeInfoListEx) -> None: ...
    def _state(self) -> DevState: ...
    def _status(self) -> str: ...
    @typing.overload
    def _write_attribute(self, attr_name: str, value: typing.Any) -> None: ...
    @typing.overload
    def _write_attribute(self, attr_info: AttributeInfo, value: typing.Any) -> None: ...
    def _write_attributes(self, name_val: typing.Any) -> None: ...
    def _write_read_attribute(
        self, attr_name: str, value: typing.Any, extract_as: ExtractAs = ...
    ) -> typing.Any: ...
    def _write_read_attributes(
        self,
        attr_in: typing.Any,
        attr_read_names: typing.Any,
        extract_as: ExtractAs = ...,
    ) -> typing.Any: ...
    def add_logging_target(self, target_type_target_name: str) -> None:
        """add_logging_target(self, target_type_target_name) -> None

            Adds a new logging target to the device.

            The target_type_target_name input parameter must follow the
            format: target_type::target_name. Supported target types are:
            console, file and device. For a device target, the target_name
            part of the target_type_target_name parameter must contain the
            name of a log consumer device (as defined in A.8). For a file
            target, target_name is the full path to the file to log to. If
            omitted, the device's name is used to build the file name
            (which is something like domain_family_member.log). Finally, the
            target_name part of the target_type_target_name input parameter
            is ignored in case of a console target and can be omitted.

        Parameters :
            - target_type_target_name : (str) logging target
        Return     : None

        Throws     : DevFailed from device

        New in PyTango 7.0.0
        """
    def adm_name(self) -> str:
        """adm_name(self) -> str

            Return the name of the corresponding administrator device. This is
            useful if you need to send an administration command to the device
            server, e.g restart it

        New in PyTango 3.0.4
        """
    def alias(self) -> str:
        """alias(self) -> str

            Return the device alias if one is defined.
            Otherwise, throws exception.

        Return: (str) device alias
        """
    def attribute_history(
        self, attr_name: str, depth: typing.SupportsInt, extract_as: ExtractAs = ...
    ) -> typing.Any:
        """attribute_history(self, attr_name, depth, extract_as=ExtractAs.Numpy) -> sequence<DeviceAttributeHistory>

            Retrieve attribute history from the attribute polling buffer. See
            chapter on Advanced Feature for all details regarding polling

        Parameters :
           - attr_name  : (str) Attribute name.
           - depth      : (int) The wanted history depth.
           - extract_as : (ExtractAs)

        Return     : This method returns a vector of DeviceAttributeHistory types.

        Throws     : NonSupportedFeature, ConnectionFailed,
                     CommunicationFailed, DevFailed from device
        """
    def attribute_list_query(self) -> AttributeInfoList:
        """attribute_list_query(self) -> sequence<AttributeInfo>

            Query the device for info on all attributes. This method returns
            a sequence of tango.AttributeInfo.

        Parameters : None
        Return     : (sequence<AttributeInfo>) containing the
                     attributes configuration

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
        """
    def attribute_list_query_ex(self) -> AttributeInfoListEx:
        """attribute_list_query_ex(self) -> sequence<AttributeInfoEx>

            Query the device for info on all attributes. This method returns
            a sequence of tango.AttributeInfoEx.

        Parameters : None
        Return     : (sequence<AttributeInfoEx>) containing the
                     attributes configuration

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
        """
    def attribute_query(self, attr_name: str) -> AttributeInfoEx:
        """attribute_query(self, attr_name) -> AttributeInfoEx

            Query the device for information about a single attribute.

        Parameters :
                - attr_name :(str) the attribute name
        Return     : (AttributeInfoEx) containing the attribute
                     configuration

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
        """
    def black_box(self, n: typing.SupportsInt) -> StdStringVector:
        """black_box(self, n) -> sequence<str>

            Get the last commands executed on the device server

        Parameters :
            - n : n number of commands to get
        Return     : (sequence<str>) sequence of strings containing the date, time,
                     command and from which client computer the command
                     was executed
        Example :
                print(black_box(4))
        """
    def command_history(self, cmd_name: str, depth: typing.SupportsInt) -> typing.Any:
        """command_history(self, cmd_name, depth) -> sequence<DeviceDataHistory>

            Retrieve command history from the command polling buffer. See
            chapter on Advanced Feature for all details regarding polling

        Parameters :
           - cmd_name  : (str) Command name.
           - depth     : (int) The wanted history depth.
        Return     : This method returns a vector of DeviceDataHistory types.

        Throws     : NonSupportedFeature, ConnectionFailed,
                     CommunicationFailed, DevFailed from device
        """
    def command_list_query(self) -> CommandInfoList:
        """command_list_query(self) -> sequence<CommandInfo>

            Query the device for information on all commands.

        Parameters : None
        Return     : (CommandInfoList) Sequence of CommandInfo objects
        """
    def command_query(self, command: str) -> CommandInfo:
        """command_query(self, command) -> CommandInfo

            Query the device for information about a single command.

        Parameters :
                - command : (str) command name
        Return     : (CommandInfo) object
        Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
        Example :
                com_info = dev.command_query("DevString")
                print(com_info.cmd_name)
                print(com_info.cmd_tag)
                print(com_info.in_type)
                print(com_info.out_type)
                print(com_info.in_type_desc)
                print(com_info.out_type_desc)
                print(com_info.disp_level)

        See CommandInfo documentation string form more detail
        """
    def delete_property(
        self,
        value: str
        | DbDatum
        | DbData
        | list[str | bytes | DbDatum]
        | dict[str, DbDatum]
        | dict[str, list[str]]
        | dict[str, typing.Any],
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> None:
        """Delete a the given of properties for this attribute.
        :param value: Can be one of the following:

                        1. :py:obj:`str` [in] - Single property data to be deleted.

                        2. :py:obj:`~tango.DbDatum` [in] - Single property data to be deleted.

                        3. :py:obj:`~tango.DbData` [in] - Several property data to be deleted.

                        4. :py:obj:`list`\\[:py:obj:`str`] [in] - Several property data to be deleted.

                        5. :py:obj:`list`\\[:py:obj:`tango.DbDatum`] [in] - Several property data to be deleted.

                        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                           to be deleted (values are ignored).

                        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                           property names to be deleted (keys are ignored).


        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :throws:
            :py:obj:`TypeError`: Raised in case of value has the wrong type.

            :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error.

            :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database.

            :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database.

            :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        """
    def description(self) -> str:
        """description(self) -> str

            Get device description.

        Parameters : None
        Return     : (str) describing the device
        """
    def dev_name(self) -> str: ...
    def event_queue_size(self, event_id: typing.SupportsInt) -> int:
        """event_queue_size(self, event_id) -> int

            Returns the number of stored events in the event reception
            buffer. After every call to DeviceProxy.get_events(), the event
            queue size is 0. During event subscription the client must have
            chosen the 'pull model' for this event. event_id is the event
            identifier returned by the DeviceProxy.subscribe_event() method.

        Parameters :
            - event_id : (int) event identifier
        Return     : an integer with the queue size

        Throws     : EventSystemFailed

        New in PyTango 7.0.0
        """
    def freeze_dynamic_interface(self):
        """Prevent unknown attributes to be set on this DeviceProxy instance.

        An exception will be raised if the Python attribute set on this DeviceProxy
        instance does not already exist.  This prevents accidentally writing to
        a non-existent Tango attribute when using the high-level API.

        This is the default behaviour since PyTango 9.3.4.

        See also :meth:`tango.DeviceProxy.unfreeze_dynamic_interface`.

        .. versionadded:: 9.4.0
        """
    def get_attribute_config(
        self, value, *, green_mode: None = None, wait: None = None, timeout: None = None
    ) -> AttributeInfoEx | AttributeInfoList:
        """get_attribute_config(self, name, green_mode=None, wait=True, timeout=None) -> AttributeInfoEx
        get_attribute_config(self, names, green_mode=None, wait=True, timeout=None) -> AttributeInfoList

            Return the attribute configuration for a single or a list of attribute(s). To get all the
            attributes pass a sequence containing the constant :obj:`tango.constants.AllAttr`

            Deprecated: use get_attribute_config_ex instead

        :param name: Attribute name.
        :type name: str

        :param names: Attribute names.
        :type names: sequence<str>

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: An `AttributeInfoEx` or `AttributeInfoList` object containing the attribute(s) information.
        :rtype: Union[:obj:`tango.AttributeInfoEx`, :obj:`tango.AttributeInfoList`]

        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: TypeError: Raised in case of an incorrect type of input arguments.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
        """
    def get_attribute_config_ex(
        self, value, *, green_mode: None = None, wait: None = None, timeout: None = None
    ) -> AttributeInfoListEx:
        """get_attribute_config_ex(self, name or sequence(names), green_mode=None, wait=True, timeout=None) -> AttributeInfoListEx :

            Return the extended attribute configuration for a single attribute or for the list of
            specified attributes. To get all the attributes pass a sequence
            containing the constant tango.constants.AllAttr.

        :param name: Attribute name or attribute names. Can be a single string (for one attribute) or a sequence of strings (for multiple attributes).
        :type name: str or sequence(str)

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: An `AttributeInfoListEx` object containing the attribute information.
        :rtype: :obj:`tango.AttributeInfoListEx`

        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
        """
    def get_attribute_list(self) -> StdStringVector:
        """get_attribute_list(self) -> sequence<str>

            Return the names of all attributes implemented for this device.

        Parameters : None
        Return     : sequence<str>

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
        """
    def get_attribute_poll_period(self, attr_name: str) -> int:
        """get_attribute_poll_period(self, attr_name) -> int

            Return the attribute polling period.

        Parameters :
            - attr_name : (str) attribute name
        Return     : polling period in milliseconds
        """
    def get_command_config(
        self,
        value=("All commands"),
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> CommandInfoList | CommandInfo:
        """get_command_config(self, green_mode=None, wait=True, timeout=None) -> CommandInfoList
        get_command_config(self, name, green_mode=None, wait=True, timeout=None) -> CommandInfo
        get_command_config(self, names, green_mode=None, wait=True, timeout=None) -> CommandInfoList

            Return the command configuration for single/list/all command(s).

        :param name: Command name. Used when querying information for a single command.
        :type name: str, optional

        :param names: Command names. Used when querying information for multiple commands. This parameter should not be used simultaneously with 'name'.
        :type names: sequence<str>, optional

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: A `CommandInfoList` object containing the commands information if multiple command names are provided, or a `CommandInfo` object if a single command name is provided.
        :rtype: :obj:`tango.CommandInfoList` or :obj:`tango.CommandInfo`

        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: TypeError: Raised in case of an incorrect type of input arguments.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
        """
    def get_command_list(self) -> StdStringVector:
        """get_command_list(self) -> sequence<str>

            Return the names of all commands implemented for this device.

        Parameters : None
        Return     : sequence<str>

        Throws     : ConnectionFailed, CommunicationFailed,
                     DevFailed from device
        """
    def get_command_poll_period(self, cmd_name: str) -> int:
        """get_command_poll_period(self, cmd_name) -> int

            Return the command polling period.

        Parameters :
            - cmd_name : (str) command name
        Return     : polling period in milliseconds
        """
    def get_device_db(self) -> Database:
        """get_device_db(self) -> Database

            Returns the internal database reference

        Parameters : None
        Return     : (Database) object

        New in PyTango 7.0.0
        """
    def get_events(self, event_id, callback=None, extract_as=...):
        """get_events(self, event_id, callback=None, extract_as=Numpy) -> None

            The method extracts all waiting events from the event reception buffer.

            If callback is not None, it is executed for every event. During event
            subscription the client must have chosen the pull model for this event.
            The callback will receive a parameter of type EventData,
            AttrConfEventData or DataReadyEventData depending on the type of the
            event (event_type parameter of subscribe_event).

            If callback is None, the method extracts all waiting events from the
            event reception buffer. The returned event_list is a vector of
            EventData, AttrConfEventData or DataReadyEventData pointers, just
            the same data the callback would have received.

        :param event_id: The event identifier returned by the `DeviceProxy.subscribe_event()` method.
        :type event_id: int
        :param callback: Any callable object or any object with a "push_event" method.
        :type callback: callable
        :param extract_as: (Description Needed)
        :type extract_as: :obj:`tango.ExtractAs`

        :returns: None

        :throws: :obj:`tango.EventSystemFailed`: Raised in case of a failure in the event system.
        :throws: TypeError: Raised in case of an incorrect type of input arguments.
        :throws: ValueError: Raised in case of an invalid value.

        :see also: :meth:`~tango.DeviceProxy.subscribe_event`

        """
    def get_green_mode(self):
        """Returns the green mode in use by this DeviceProxy.

        :returns: the green mode in use by this DeviceProxy.
        :rtype: GreenMode

        .. seealso::
            :func:`tango.get_green_mode`
            :func:`tango.set_green_mode`

        New in PyTango 8.1.0
        """
    def get_last_event_date(self, event_id: typing.SupportsInt) -> TimeVal:
        """get_last_event_date(self, event_id) -> TimeVal

            Returns the arrival time of the last event stored in the event
            reception buffer. After every call to DeviceProxy:get_events(),
            the event reception buffer is empty. In this case an exception
            will be returned. During event subscription the client must have
            chosen the 'pull model' for this event. event_id is the event
            identifier returned by the DeviceProxy.subscribe_event() method.

        Parameters :
            - event_id : (int) event identifier
        Return     : (tango.TimeVal) representing the arrival time

        Throws     : EventSystemFailed

        New in PyTango 7.0.0
        """
    def get_locker(self, lockinfo: LockerInfo) -> bool:
        """get_locker(self, lockinfo) -> bool

            If the device is locked, this method returns True an set some
            locker process informations in the structure passed as argument.
            If the device is not locked, the method returns False.

        Parameters :
            - lockinfo [out] : (tango.LockInfo) object that will be filled
                                with lock information
        Return     : (bool) True if the device is locked by us.
                     Otherwise, False

        New in PyTango 7.0.0
        """
    def get_logging_level(self) -> int:
        """get_logging_level(self) -> int

            Returns the current device's logging level, where:
                - 0=OFF
                - 1=FATAL
                - 2=ERROR
                - 3=WARNING
                - 4=INFO
                - 5=DEBUG

        Parameters :None
        Return     : (int) representing the current logging level

        New in PyTango 7.0.0
        """
    def get_logging_target(self) -> StdStringVector:
        """get_logging_target(self) -> sequence<str>

            Returns a sequence of string containing the current device's
            logging targets. Each vector element has the following format:
            target_type::target_name. An empty sequence is returned is the
            device has no logging targets.

        Parameters : None
        Return     : a sequence<str> with the logging targets

        New in PyTango 7.0.0
        """
    def get_property(
        self,
        propname: str
        | DbDatum
        | DbData
        | list[str | bytes | DbDatum]
        | dict[str, DbDatum]
        | dict[str, list[str]]
        | dict[str, typing.Any],
        value=None,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> dict[str, list[str]]:
        """Get a (list) property(ies) for an attribute.

        :param propname: Can be one of the following:

                        1. :py:obj:`str` [in] - Single property data to be fetched.

                        2. :py:obj:`~tango.DbDatum` [in] - Single property data to be fetched.

                        3. :py:obj:`~tango.DbData` [in] - Several property data to be fetched.

                        4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` ] [in] - Several property data to be fetched.

                        5. :py:obj:`list`\\[:py:obj:`tango.DbDatum`] [in] - Several property data to be fetched.

                        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                           to be fetched (values are ignored).

                        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                           property names to be fetched (keys are ignored).


        :param value: Optional. For propname overloads with :py:obj:`str` and :py:obj:`list`\\[:py:obj:`str`] will be filed with the property values, if provided.
        :type value: :obj:`tango.DbData`, optional

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: A :obj:`dict` object, which keys are the property names the value
                  associated with each key being a sequence of strings being the
                  property value.

        :throws:
            :py:obj:`TypeError`: Raised in case of propname has the wrong type.

            :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error.

            :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database.

            :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database.

            :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 10.1.0: overloads with :obj:`dict` as propname parameter

        .. versionchanged:: 10.1.0: raises if propname has an invalid type instead of returning None
        """
    def get_property_list(
        self,
        filter,
        array=None,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> list[str]:
        """get_property_list(self, filter, array=None, green_mode=None, wait=True, timeout=None) -> obj

                Get the list of property names for the device. The parameter
                filter allows the user to filter the returned name list. The
                wildcard character is '*'. Only one wildcard character is
                allowed in the filter parameter.

        :param filter: The filter wildcard.
        :type filter: str

        :param array: Optional. An array to be filled with the property names. If `None`, a new list will be created internally with the values. Defaults to `None`.
        :type array: sequence obj or None, optional

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: The given array filled with the property names, or a new list if `array` is `None`.
        :rtype: sequence obj

        :throws: :obj:`tango.NonDbDevice`: Raised in case of a non-database device error.
        :throws: :obj:`tango.WrongNameSyntax`: Raised in case of incorrect syntax in the name.
        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure with the database.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure with the database.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure from the database device.
        :throws: TypeError: Raised in case of an incorrect type of input arguments.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        :versionadded:: 7.0.0
        """
    def get_tango_lib_version(self) -> int:
        """get_tango_lib_version(self) -> int

            Returns the Tango lib version number used by the remote device
            Otherwise, throws exception.

        Return     : (int) The device Tango lib version as a 3 or 4 digits number.
                     Possible return value are: 100,200,500,520,700,800,810,...

        New in PyTango 8.1.0
        """
    def import_info(self) -> DbDevImportInfo:
        """import_info(self) -> DbDevImportInfo

            Query the device for import info from the database.

        Parameters : None
        Return     : (DbDevImportInfo)
        Example :
                dev_import = dev.import_info()
                print(dev_import.name)
                print(dev_import.exported)
                print(dev_ior.ior)
                print(dev_version.version)

        All DbDevImportInfo fields are strings except for exported which
        is an integer"
        """
    def info(self) -> DeviceInfo:
        """info(self) -> DeviceInfo

            A method which returns information on the device

        Parameters : None
        Return     : (DeviceInfo) object
        Example    :
                dev_info = dev.info()
                print(dev_info.dev_class)
                print(dev_info.server_id)
                print(dev_info.server_host)
                print(dev_info.server_version)
                print(dev_info.doc_url)
                print(dev_info.dev_type)
                print(dev_info.version_info)
        """
    def is_attribute_polled(self, attr_name: str) -> bool:
        """is_attribute_polled(self, attr_name) -> bool

        True if the attribute is polled.

        :param str attr_name: attribute name

        :returns: boolean value
        :rtype: bool
        """
    def is_command_polled(self, cmd_name: str) -> bool:
        """is_command_polled(self, cmd_name) -> bool

        True if the command is polled.

        :param str cmd_name: command name

        :returns: boolean value
        :rtype: bool
        """
    def is_dynamic_interface_frozen(self):
        """Indicates if the dynamic interface for this DeviceProxy instance is frozen.

        See also :meth:`tango.DeviceProxy.freeze_dynamic_interface` and
        :meth:`tango.DeviceProxy.unfreeze_dynamic_interface`.

            :returns: True if the dynamic interface this DeviceProxy is frozen.
            :rtype: bool

        .. versionadded:: 9.4.0
        """
    def is_event_queue_empty(self, event_id: typing.SupportsInt) -> bool:
        """is_event_queue_empty(self, event_id) -> bool

        Returns true when the event reception buffer is empty. During
        event subscription the client must have chosen the 'pull model'
        for this event. event_id is the event identifier returned by the
        DeviceProxy.subscribe_event() method.

        Parameters :
            - event_id : (int) event identifier
        Return     : (bool) True if queue is empty or False otherwise

        Throws     : EventSystemFailed

        New in PyTango 7.0.0
        """
    def is_locked(self) -> bool:
        """is_locked(self) -> bool

            Returns True if the device is locked. Otherwise, returns False.

        Parameters : None
        Return     : (bool) True if the device is locked. Otherwise, False

        New in PyTango 7.0.0
        """
    def is_locked_by_me(self) -> bool:
        """is_locked_by_me(self) -> bool

            Returns True if the device is locked by the caller. Otherwise,
            returns False (device not locked or locked by someone else)

        Parameters : None
        Return     : (bool) True if the device is locked by us.
                        Otherwise, False

        New in PyTango 7.0.0
        """
    def lock(self, lock_validity: typing.SupportsInt = 10) -> None:
        """lock(self, (int)lock_validity) -> None

            Lock a device. The lock_validity is the time (in seconds) the
            lock is kept valid after the previous lock call. A default value
            of 10 seconds is provided and should be fine in most cases. In
            case it is necessary to change the lock validity, it's not
            possible to ask for a validity less than a minimum value set to
            2 seconds. The library provided an automatic system to
            periodically re lock the device until an unlock call. No code is
            needed to start/stop this automatic re-locking system. The
            locking system is re-entrant. It is then allowed to call this
            method on a device already locked by the same process. The
            locking system has the following features:

              * It is impossible to lock the database device or any device
                server process admin device
              * Destroying a locked DeviceProxy unlocks the device
              * Restarting a locked device keeps the lock
              * It is impossible to restart a device locked by someone else
              * Restarting a server breaks the lock

            A locked device is protected against the following calls when
            executed by another client:

              * command_inout call except for device state and status
                requested via command and for the set of commands defined as
                allowed following the definition of allowed command in the
                Tango control access schema.
              * write_attribute call
              * write_read_attribute call
              * set_attribute_config call

        Parameters :
            - lock_validity : (int) lock validity time in seconds
                                (optional, default value is
                                tango.constants.DEFAULT_LOCK_VALIDITY)
        Return     : None

        New in PyTango 7.0.0
        """
    def locking_status(self) -> str:
        """locking_status(self) -> str

            This method returns a plain string describing the device locking
            status. This string can be:

              * 'Device <device name> is not locked' in case the device is
                not locked
              * 'Device <device name> is locked by CPP or Python client with
                PID <pid> from host <host name>' in case the device is
                locked by a CPP client
              * 'Device <device name> is locked by JAVA client class
                <main class> from host <host name>' in case the device is
                locked by a JAVA client

        Parameters : None
        Return     : a string representing the current locking status

        New in PyTango 7.0.0
        """
    def name(self) -> str:
        """name(self) -> str

            Return the device name from the device itself.

        Return: (str) device name
        """
    def pending_asynch_call(self, arg0: asyn_req_type) -> int:
        """pending_asynch_call(self) -> int

            Return number of device asynchronous pending requests"

        New in PyTango 7.0.0
        """
    def ping(
        self, *, green_mode: None = None, wait: None = None, timeout: None = None
    ) -> int:
        """ping(self, green_mode=None, wait=True, timeout=None) -> DevState

            A method which sends a ping to the device

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: time elapsed in microseconds
        :rtype: int

        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        """
    def poll_attribute(self, attr_name: str, period: typing.SupportsInt) -> None:
        """poll_attribute(self, attr_name, period) -> None

            Add an attribute to the list of polled attributes.

        Parameters :
            - attr_name : (str) attribute name
            - period    : (int) polling period in milliseconds
        Return     : None
        """
    def poll_command(self, cmd_name: str, period: typing.SupportsInt) -> None:
        """poll_command(self, cmd_name, period) -> None

            Add a command to the list of polled commands.

        Parameters :
            - cmd_name : (str) command name
            - period   : (int) polling period in milliseconds
        Return     : None
        """
    def polling_status(self) -> StdStringVector:
        """polling_status(self) -> sequence<str>

            Return the device polling status.

        Parameters : None
        Return     : (sequence<str>) One string for each polled command/attribute.
                     Each string is multi-line string with:

                        - attribute/command name
                        - attribute/command polling period in milliseconds
                        - attribute/command polling ring buffer
                        - time needed for last attribute/command execution in milliseconds
                        - time since data in the ring buffer has not been updated
                        - delta time between the last records in the ring buffer
                        - exception parameters in case of the last execution failed
        """
    def put_property(
        self,
        value: str
        | DbDatum
        | DbData
        | list[str | bytes | DbDatum]
        | dict[str, DbDatum]
        | dict[str, list[str]]
        | dict[str, typing.Any],
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> None:
        """Insert or update a list of properties for this attribute.

        :param value: Can be one of the following:

                        1. :py:obj:`str` - Single property data to be inserted.

                        2. :py:obj:`~tango.DbDatum` - Single property data to be inserted.

                        3. :py:obj:`~tango.DbData` - Several property data to be inserted.

                        4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` | :py:obj:`~tango.DbDatum`] - Several property data to be inserted.

                        5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`~tango.DbDatum`] -
                            DbDatum is property to be inserted (keys are ignored).

                        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] - Keys are property names,
                            and value has data to be inserted.

                        7. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] - Keys are property names, and `str(obj)` is property value.

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :throws:
            :py:obj:`TypeError`: Raised in case of value has the wrong type.

            :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error.

            :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database.

            :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database.

            :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
        """
    def read_attribute(
        self,
        value,
        extract_as=...,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> DeviceAttribute:
        """read_attribute(self, value, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> DeviceAttribute

            Read a single attribute.

        :param value: The name of the attribute to read.
        :type value: str

        :param extract_as: Defaults to numpy.
        :type extract_as: :obj:`tango.ExtractAs`

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :return: DeviceAttribute object with read attribute value.
        :rtype: :obj:`tango.DeviceAttribute`

        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionchanged:: 7.1.4
            For DevEncoded attributes, before it was returning a DeviceAttribute.value
            as a tuple **(format<str>, data<str>)** no matter what was the *extract_as*
            value was. Since 7.1.4, it returns a **(format<str>, data<buffer>)**
            unless *extract_as* is String, in which case it returns
            **(format<str>, data<str>)**.

        .. versionchanged:: 8.0.0
            For DevEncoded attributes, now returns a DeviceAttribute.value
            as a tuple **(format<str>, data<bytes>)** unless *extract_as* is String,
            in which case it returns **(format<str>, data<str>)**. Careful, if
            using python >= 3 data<str> is decoded using default python
            *utf-8* encoding. This means that PyTango assumes tango DS was written
            encapsulating string into *utf-8* which is the default python encoding.

        .. versionadded:: 8.1.0
            *green_mode* parameter.
            *wait* parameter.
            *timeout* parameter.

        .. versionchanged:: 9.4.0
            For spectrum and image attributes with an empty sequence, no longer
            returns DeviceAttribute.value and DeviceAttribute.w_value as
            :obj:`None`.  Instead, DevString and DevEnum types get an empty :obj:`tuple`,
            while other types get an empty :obj:`numpy.ndarray`.  Using *extract_as* can
            change the sequence type, but it still won't be :obj:`None`.
        """
    def read_attribute_asynch(
        self,
        attr_name,
        cb=None,
        extract_as=...,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> int | None:
        """read_attribute_asynch(self, attr_name, green_mode=None, wait=True, timeout=None) -> int
        read_attribute_asynch(self, attr_name, cb, extract_as=Numpy, green_mode=None, wait=True, timeout=None) -> None

            Read asynchronously the specified attributes.

            New in PyTango 7.0.0

        .. important::
            by default, TANGO is initialized with the **polling** model. If you want
            to use the **push** model (the one with the callback parameter), you
            need to change the global TANGO model to PUSH_CALLBACK.
            You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

        :param attr_name: an attribute to read
        :type attr_name: str

        :param cb: push model: as soon as attributes read, core calls cb with read results.
            This callback object should be an instance of a user class with an attr_read() method.
            It can also be any callable object.
        :type cb: Optional[Callable]

        :param extract_as: Defaults to numpy.
        :type extract_as: ExtractAs

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: an asynchronous call identifier which is needed to get attribute value if poll model, None if push model
        :rtype: Union[int, None]

        :throws: :obj:`tango.ConnectionFailed`
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. important::
            Multiple asynchronous calls are not guaranteed to be executed by the device
            server in the same order they are invoked by the client.  E.g., a call
            to the method ``write_attribute_asynch("a", 1)`` followed immediately with
            a call to ``read_attribute_asynch("a")`` could result in the device reading the
            attribute ``a`` before writing to it.
        """
    def read_attribute_reply(
        self,
        *args,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
        **kwargs,
    ) -> DeviceAttribute:
        """read_attribute_reply(self, id, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> DeviceAttribute
        read_attribute_reply(self, id, poll_timeout, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> DeviceAttribute

        Get the answer of an asynchronous read_attribute call, if it has arrived (polling model).

        If the reply is ready, but the attribute raised an exception while reading, an
        exception will be raised by this function (DevFailed, with reason API_AttrValueNotSet).

        .. versionchanged:: 7.0.0 New in PyTango
        .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

            - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
            - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.


        :param id: the asynchronous call identifier
        :type id: int

        :param poll_timeout: cppTango core timeout in ms.
            If the reply has not yet arrived, the call will wait for the time specified (in ms).
            If after timeout, the reply is still not there, an exception is thrown.
            If timeout set to 0, the call waits until the reply arrives.
            If the argument is not provided, then there is no timeout check, and an
            exception is raised immediately if the reply is not ready.
        :type poll_timeout: Optional[int]

        :param extract_as: Defaults to numpy.
        :type extract_as: ExtractAs

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: If the reply is arrived and if it is a valid reply,
            it is returned to the caller in a list of DeviceAttribute.
            If the reply is an exception, it is re-thrown by this call.
            If the reply is not yet arrived, the call will wait (blocking the process)
            for the time specified in timeout. If after timeout milliseconds, the reply is still not there, an
            exception is thrown. If timeout is set to 0, the call waits
            until the reply arrived.
        :rtype: :obj:`tango.DeviceAttribute`

        :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]

        """
    def read_attributes(
        self,
        attr_names,
        extract_as=...,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> list[DeviceAttribute]:
        """read_attributes(self, attr_names, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> sequence<DeviceAttribute>

            Read the list of specified attributes.

        :param attr_names: A list of attributes to read.
        :type attr_names: sequence<str>

        :param extract_as: In which format to return the attribute values.
        :type extract_as: :obj:`tango.ExtractAs`

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: A list of DeviceAttribute objects.
        :rtype: sequence<:obj:`tango.DeviceAttribute`>

        :throws: :obj:`tango.ConnectionFailed`, :obj:`tango.CommunicationFailed`, :obj:`tango.DeviceUnlocked`:
        :throws: :obj:`tango.DevFailed`: from device
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 8.1.0
            *green_mode* parameter.
            *wait* parameter.
            *timeout* parameter.
        """
    def read_attributes_asynch(
        self,
        attr_names,
        cb=None,
        extract_as=...,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> int | None:
        """read_attributes_asynch(self, attr_names, green_mode=None, wait=True, timeout=None) -> int
        read_attributes_asynch(self, attr_names, cb, extract_as=Numpy, green_mode=None, wait=True, timeout=None) -> None

            Read asynchronously an attribute list.

            New in PyTango 7.0.0

        .. important::
            by default, TANGO is initialized with the **polling** model. If you want
            to use the **push** model (the one with the callback parameter), you
            need to change the global TANGO model to PUSH_CALLBACK.
            You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

        :param attr_names: A list of attributes to read. See read_attributes.
        :type attr_names: Sequence[str]

        :param cb: push model: as soon as attributes read, core calls cb with read results.
            This callback object should be an instance of a user class with an attr_read() method.
            It can also be any callable object.
        :type cb: Optional[Callable]

        :param extract_as: Defaults to numpy.
        :type extract_as: :obj:`tango.ExtractAs`

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: an asynchronous call identifier which is needed to get attributes value if poll model, None if push model
        :rtype: Union[int, None]

        :throws: :obj:`tango.ConnectionFailed`
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. important::
            Multiple asynchronous calls are not guaranteed to be executed by the device
            server in the same order they are invoked by the client.  E.g., a call
            to ``write_attributes_asynch([("a", 1)])`` followed immediately with a call to
            ``read_attributes_asynch(["a"])`` could result in the device reading the
            attribute ``a`` before writing to it.
        """
    def read_attributes_reply(
        self,
        *args,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
        **kwargs,
    ) -> list[DeviceAttribute]:
        """read_attributes_reply(self, id, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> [DeviceAttribute]
        read_attributes_reply(self, id, poll_timeout, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> [DeviceAttribute]

        Get the answer of an asynchronous read_attributes call, if it has arrived (polling model).

        If the reply is ready, but an attribute raised an exception while reading, it will
        still be included in the returned list.  However, the has_error field for that item
        will be set to True.

        .. versionchanged:: 7.0.0 New in PyTango
        .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

            - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
            - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.


        :param id: the asynchronous call identifier
        :type id: int

        :param poll_timeout: cppTango core timeout in ms.
            If the reply has not yet arrived, the call will wait for the time specified (in ms).
            If after timeout, the reply is still not there, an exception is thrown.
            If timeout set to 0, the call waits until the reply arrives.
            If the argument is not provided, then there is no timeout check, and an
            exception is raised immediately if the reply is not ready.
        :type poll_timeout: Optional[int]

        :param extract_as: Defaults to numpy.
        :type extract_as: ExtractAs

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: If the reply is arrived and if it is a valid reply,
            it is returned to the caller in a list of DeviceAttribute.
            If the reply is an exception, it is re-thrown by this call.
            If the reply is not yet arrived, the call will wait (blocking the process)
            for the time specified in timeout. If after timeout milliseconds, the reply is still not there, an
            exception is thrown. If timeout is set to 0, the call waits
            until the reply arrived.
        :rtype: Sequence[DeviceAttribute]

        :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
        """
    def remove_logging_target(self, target_type_target_name: str) -> None:
        """remove_logging_target(self, target_type_target_name) -> None

            Removes a logging target from the device's target list.

            The target_type_target_name input parameter must follow the
            format: target_type::target_name. Supported target types are:
            console, file and device. For a device target, the target_name
            part of the target_type_target_name parameter must contain the
            name of a log consumer device (as defined in ). For a file
            target, target_name is the full path to the file to remove.
            If omitted, the default log file is removed. Finally, the
            target_name part of the target_type_target_name input parameter
            is ignored in case of a console target and can be omitted.
            If target_name is set to '*', all targets of the specified
            target_type are removed.

        Parameters :
            - target_type_target_name : (str) logging target
        Return     : None

        New in PyTango 7.0.0
        """
    def set_attribute_config(
        self, value, *, green_mode: None = None, wait: None = None, timeout: None = None
    ) -> None:
        """set_attribute_config(self, attr_info, green_mode=None, wait=True, timeout=None) -> None
        set_attribute_config(self, attr_info_ex, green_mode=None, wait=True, timeout=None) -> None

            Change the attribute configuration/extended attribute configuration for the specified attribute(s)

        :param attr_info: Attribute information. This parameter is used when providing basic attribute(s) information.
        :type attr_info: Union[:obj:`tango.AttributeInfo`, Sequence[:obj:`tango.AttributeInfo`]], optional

        :param attr_info_ex: Extended attribute information. This parameter is used when providing extended attribute information. It should not be used simultaneously with 'attr_info'.
        :type attr_info_ex: Union[:obj:`tango.AttributeInfoEx`, Sequence[:obj:`tango.AttributeInfoEx`]], optional

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: None

        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: TypeError: Raised in case of an incorrect type of input arguments.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        """
    def set_green_mode(self, green_mode=None):
        """Sets the green mode to be used by this DeviceProxy
        Setting it to None means use the global PyTango green mode
        (see :func:`tango.get_green_mode`).

        :param green_mode: the new green mode
        :type green_mode: GreenMode

        New in PyTango 8.1.0
        """
    def set_logging_level(self, level: typing.SupportsInt) -> None:
        """set_logging_level(self, level) -> None

            Changes the device's logging level, where:
                - 0=OFF
                - 1=FATAL
                - 2=ERROR
                - 3=WARNING
                - 4=INFO
                - 5=DEBUG

        Parameters :
            - level : (int) logging level
        Return     : None

        New in PyTango 7.0.0
        """
    def state(
        self, *, green_mode: None = None, wait: None = None, timeout: None = None
    ) -> DevState:
        """state(self, green_mode=None, wait=True, timeout=None) -> DevState

            A method which returns the state of the device.

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: A `DevState` constant.
        :rtype: DevState

        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        """
    def status(
        self, *, green_mode: None = None, wait: None = None, timeout: None = None
    ) -> str:
        """status(self, green_mode=None, wait=True, timeout=None) -> str

            A method which returns the status of the device as a string.

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: string describing the device status
        :rtype: str

        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        """
    def stop_poll_attribute(self, attr_name: str) -> None:
        """stop_poll_attribute(self, attr_name) -> None

            Remove an attribute from the list of polled attributes.

        Parameters :
            - attr_name : (str) attribute name
        Return     : None
        """
    def stop_poll_command(self, cmd_name: str) -> None:
        """stop_poll_command(self, cmd_name) -> None

            Remove a command from the list of polled commands.

        Parameters :
            - cmd_name : (str) command name
        Return     : None
        """
    def subscribe_event(
        self,
        *args,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
        **kwargs,
    ) -> int:
        """subscribe_event(self, attr_name, event_type, cb, sub_mode=EventSubMode.SyncRead, extract_as=ExtractAs.Numpy, *, green_mode=None, wait=True, timeout=None) -> int
        subscribe_event(self, attr_name, event_type, queuesize, sub_mode=EventSubMode.SyncRead, extract_as=ExtractAs.Numpy, *, green_mode=None, wait=True, timeout=None) -> int
        subscribe_event(self, event_type, cb, sub_mode=EventSubMode.SyncRead, *, green_mode=None, wait=True, timeout=None) -> int

        .. note::
            This function is heavily overloaded, and includes three additional signatures that
            have been deprecated (see warning below).

        The client call to subscribe for event reception.  There are two main categories:

        * Subscribe to events for a specific attribute, like change events, providing
          either:

          * a callback function for immediate notification (*push* callback model), or
          * a queue length, allowing events to be processed later (*pull* callback model).

        * Subscribe to device-level events (not linked to a specific attribute), like
          interface-changed events. These require a callback function (*push* callback model).

        More details of the *push* and *pull* callback models are provided in the
        :external+tangodoc:ref:`cppTango Events API docs <events-tangoclient-api>`.

        :param attr_name: The device attribute name which will be sent as an event, e.g., "current".
        :type attr_name: str

        :param event_type: The event reason, which must be one of the enumerated values in `EventType`. This includes:

            * `EventType.CHANGE_EVENT`
            * `EventType.ALARM_EVENT`
            * `EventType.PERIODIC_EVENT`
            * `EventType.ARCHIVE_EVENT`
            * `EventType.USER_EVENT`
            * `EventType.DATA_READY_EVENT`
            * `EventType.ATTR_CONF_EVENT`
            * `EventType.INTERFACE_CHANGE_EVENT`
        :type event_type: :obj:`tango.EventType`

        :param cb:
            Any callable object or an object with a callable ``push_event`` method
            (i.e., use the *push* callback model).
            The callable has the signature ``def cb(event)`` (or ``async def cb(event)``
            for asyncio green mode DeviceProxy objects).  The ``event`` parameter's data
            type depends on the type of event subscribed to. In most cases it is
            :obj:`tango.EventData`.  Special cases are `EventType.DATA_READY`,
            `EventType.ATTR_CONF_EVENT`, and `EventType.INTERFACE_CHANGE_EVENT` -
            see :ref:`event-arrived-structures`.

        :type cb: callable

        :param queuesize:
            The size of the event reception buffer (i.e., use the *pull* callback model).
            The event reception buffer is implemented as a round-robin buffer.
            This way the client can set up different ways to receive events:

            * Event reception buffer size = 1 : The client is interested only in the value of the last event received. All other events that have been received since the last reading are discarded.
            * Event reception buffer size > 1 : The client has chosen to keep an event history of a given size. When more events arrive since the last reading, older events will be discarded.
            * Event reception buffer size = tango.constants.ALL_EVENTS : The client buffers all received events. The buffer size is unlimited and only restricted by the available memory for the client.
        :type queuesize: int

        :param sub_mode: The event subscription mode.
        :type sub_mode: :obj:`tango.EventSubMode`

        :param extract_as: In which format to return the attribute values. Default: ExtractAs.NumPy
        :type extract_as: ExtractAs

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: An event id which has to be specified when unsubscribing from this event.
        :rtype: int

        :throws: :obj:`tango.EventSystemFailed`: Raised in case of a failure in the event system.
        :throws: :obj:`tango.DevFailed`: Raised in case of general communication failures.
        :throws: :obj:`TypeError`: Raised in case of an incorrect type of input arguments.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. deprecated:: PyTango 10.1.0

            The following signatures, which use the ``filters`` and/or ``stateless``
            parameters, are deprecated. The version for removal has not been decided, but
            the earliest is version 11.0.0.

            * *subscribe_event(self, attr_name, event_type, cb, filters=[], stateless=False, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> int*
            * *subscribe_event(self, attr_name, event_type, queuesize, filters=[], stateless=False, extract_as=ExtractAs.Numpy, green_mode=None, wait=True, timeout=None) -> int*
            * *subscribe_event(self, event_type, cb, stateless=False, *, green_mode=None, wait=True, timeout=None) -> int*

            ``filters`` (*sequence<str>*)
                The filters apply to the original Notifd-based event system, not the
                current ZeroMQ-based event system (added in Tango 8). Notifd support is
                scheduled for removal in Tango 11.

                A variable length list of name-value pairs which define additional filters
                for events. Provide an empty list, if this feature is not needed
                (typically, for all Tango servers from version 8).

                Filters cannot be used with the `sub_mode` parameter.

            ``stateless`` (*bool*)
                Instead of setting ``stateless=True`` use ``sub_mode=EventSubMode.Stateless``.

                When this flag is set to false, an exception will be thrown if the event
                subscription encounters a problem. With the stateless flag set to true,
                the event subscription will not raise an exception, even if the corresponding
                device is not running, or the attribute doesn't exist.
                A keep-alive thread will attempt to subscribe for the specified event
                every 10 seconds, executing a callback with the corresponding exception at
                every retry.

                The ``stateless`` flag cannot be used with the `sub_mode` parameter.

        .. versionadded:: 10.1.0
            Three new signatures using the *sub_mode* parameter.

        .. versionchanged:: 10.1.0
            All parameters can now be passed as keyword arguments.
        """
    def unfreeze_dynamic_interface(self):
        """Allow new attributes to be set on this DeviceProxy instance.

        An exception will not be raised if the Python attribute set on this DeviceProxy
        instance does not exist.  Instead, the new Python attribute will be added to
        the DeviceProxy instance's dictionary of attributes.  This may be useful, but
        a user will not get an error if they accidentally write to a non-existent Tango
        attribute when using the high-level API.

        See also :meth:`tango.DeviceProxy.freeze_dynamic_interface`.

        .. versionadded:: 9.4.0
        """
    def unlock(self, force: bool = False) -> None:
        """unlock(self, (bool)force) -> None

            Unlock a device. If used, the method argument provides a back
            door on the locking system. If this argument is set to true,
            the device will be unlocked even if the caller is not the locker.
            This feature is provided for administration purpose and should
            be used very carefully. If this feature is used, the locker will
            receive a DeviceUnlocked during the next call which is normally
            protected by the locking Tango system.

        Parameters :
            - force : (bool) force unlocking even if we are not the
                      locker (optional, default value is False)
        Return     : None

        New in PyTango 7.0.0
        """
    def unsubscribe_event(
        self,
        event_id,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> None:
        """unsubscribe_event(self, event_id, green_mode=None, wait=True, timeout=None) -> None

            Unsubscribes a client from receiving the event specified by event_id.

        :param event_id: The event identifier returned by `DeviceProxy::subscribe_event()`. Unlike in TangoC++, this implementation checks that the `event_id` has been subscribed to in this `DeviceProxy`.
        :type event_id: int

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: None

        :throws: :obj:`tango.EventSystemFailed`: Raised in case of a failure in the event system.
        :throws: KeyError: Raised if the specified `event_id` is not found or not subscribed in this `DeviceProxy`.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.
        """
    def write_attribute(
        self,
        attr: str | AttributeInfoEx,
        value: typing.Any,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> None:
        """write_attribute(self, attr, value, green_mode=None, wait=True, timeout=None) -> None

        Write a single attribute.

        :param attr: The name or AttributeInfoEx structure of the attribute to write.
        :type attr: str | :obj:`tango.AttributeInfoEx`

        :param value: The value to write to the attribute.
        :type value: Any

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :throws: :obj:`tango.ConnectionFailed`, :obj:`tango.CommunicationFailed`, :obj:`tango.DeviceUnlocked`:
        :throws: :obj:`tango.DevFailed`: from device
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 8.1.0
            *green_mode* parameter.
            *wait* parameter.
            *timeout* parameter.

        .. versionchanged:: 10.1.0 attr_name parameter was renamed to attr

        """
    def write_attribute_asynch(
        self,
        attr: str | AttributeInfoEx,
        value: typing.Any,
        cb=None,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> int | None:
        """Write asynchronously the specified attribute.

        .. important::
            by default, TANGO is initialized with the **polling** model. If you want
            to use the **push** model (the one with the callback parameter), you
            need to change the global TANGO model to PUSH_CALLBACK.
            You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

        :param attr: an attribute name to write or AttributeInfoEx object (see Note below)
        :type attr: str | :obj:`~tango.AttributeInfoEx`

        :param value: value to write
        :type value: Any

        :param cb: push model: as soon as attribute written, core calls cb with write results.
            This callback object should be an instance of a user class with an attr_written() method.
            It can also be any callable object.
        :type cb: Optional[Callable]

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: an asynchronous call identifier which is needed to get the server reply if poll model, None if push model
        :rtype: Union[int, None]

        :throws: ConnectionFailed
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. important::
            Multiple asynchronous calls are not guaranteed to be executed by the device
            server in the same order they are invoked by the client.  E.g., a call
            to the method ``write_attribute_asynch("a", 1)`` followed immediately with
            a call to ``read_attribute_asynch("a")`` could result in the device reading the
            attribute ``a`` before writing to it.

        .. note::
            There are two possibilities for the attr parameter: if you give attribute name,
            then PyTango will do additional synchronous(!) IO to fetch AttributeInfoEx object from device server,
            since we must know to which c++ data type cast python value. If you would like to avoid this IO you
            can give AttributeInfoEx instead of attribute name.

        .. versionchanged:: 10.1.0

            - attr_name parameter was renamed to attr
            - added support for AttributeInfoEx for attr parameter

        """
    def write_attribute_reply(
        self,
        *args,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
        **kwargs,
    ) -> None:
        """write_attribute_reply(self, id, green_mode=None, wait=True, timeout=None) -> None
        write_attribute_reply(self, id, poll_timeout, green_mode=None, wait=True, timeout=None) -> None

            Check if the answer of an asynchronous write_attributes is arrived
            (polling model). If the reply is arrived and if it is a valid reply,
            the call returned. If the reply is an exception, it is re-thrown by
            this call. An exception is also thrown in case of the reply is not
            yet arrived.

        .. versionchanged:: 7.0.0 New in PyTango
        .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

            - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
            - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.

        :param id: the asynchronous call identifier
        :type id: int

        :param poll_timeout: cppTango core timeout in ms.
            If the reply has not yet arrived, the call will wait for the time specified (in ms).
            If after timeout, the reply is still not there, an exception is thrown.
            If timeout set to 0, the call waits until the reply arrives.
            If the argument is not provided, then there is no timeout check, and an
            exception is raised immediately if the reply is not ready.
        :type poll_timeout: Optional[int]

        :param extract_as: Defaults to numpy.
        :type extract_as: ExtractAs

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: None
        :rtype: None

        :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]
        """
    def write_attributes(
        self,
        attr_values,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> None:
        """write_attributes(self, name_val, green_mode=None, wait=True, timeout=None) -> None

            Write the specified attributes.

        :param attr_values: A list of pairs (attr, value). See write_attribute
        :type attr_values: Sequence<(str | AttributeInfoEx, Any)>

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :throws: :obj:`tango.ConnectionFailed`, :obj:`tango.CommunicationFailed`, :obj:`tango.DeviceUnlocked`:
        :throws: :obj:`tango.DevFailed`, :obj:`tango.NamedDevFailedList`: from device
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. versionadded:: 8.1.0
            *green_mode* parameter.
            *wait* parameter.
            *timeout* parameter.

        .. versionchanged:: 10.1.0

            - name_val parameter was renamed to attr_values
            - added support for AttributeInfoEx for attr_values parameter
        """
    def write_attributes_asynch(
        self,
        attr_values: list[tuple[str | AttributeInfoEx, typing.Any]],
        cb=None,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> int | None:
        """Write asynchronously the specified attributes.

        .. important::
            by default, TANGO is initialized with the **polling** model. If you want
            to use the **push** model (the one with the callback parameter), you
            need to change the global TANGO model to PUSH_CALLBACK.
            You can do this with the :meth:`tango.ApiUtil.set_asynch_cb_sub_model`

        :param attr_values: pairs of (attr_name, value) to write (see Note below)
        :type attr_values: Sequence[Sequence[str | :obj:`~tango.AttributeInfoEx`, Any]]

        :param cb: push model: as soon as attributes written, core calls cb with write results.
            This callback object should be an instance of a user class with an attr_written() method.
            It can also be any callable object.
        :type cb: Optional[Callable]

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: an asynchronous call identifier which is needed to get the server reply if poll model, None if push model
        :rtype: Union[int, None]

        :throws: :obj:`tango.ConnectionFailed`
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        .. important::
            Multiple asynchronous calls are not guaranteed to be executed by the device
            server in the same order they are invoked by the client.  E.g., a call
            to ``write_attributes_asynch([("a", 1)])`` followed immediately with a call to
            ``read_attributes_asynch(["a"])`` could result in the device reading the
            attribute ``a`` before writing to it.

        .. note::
            For each pair of values there are two possibilities for the
            attr parameter: if you give attribute name, then PyTango must
            fetch attribute info for this attribute from server by additional synchronous(!)
            IO, since we must know to which c++ data type cast each python value.
            If you would like to avoid this IO you must give AttributeInfoEx instead of
            attribute name for each(!) pair of values.

        .. versionchanged:: 10.1.0 Added support for AttributeInfoEx for attr_values parameter.

        """
    def write_attributes_reply(
        self,
        *args,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
        **kwargs,
    ) -> None:
        """write_attributes_reply(self, id, green_mode=None, wait=True, timeout=None) -> None
        write_attributes_reply(self, id, poll_timeout, green_mode=None, wait=True, timeout=None) -> None

            Check if the answer of an asynchronous write_attributes is arrived
            (polling model). If the reply is arrived and if it is a valid reply,
            the call returned. If the reply is an exception, it is re-thrown by
            this call. An exception is also thrown in case of the reply is not
            yet arrived.

        .. versionchanged:: 7.0.0 New in PyTango
        .. versionchanged:: 10.0.0 To eliminate confusion between different timeout parameters, the core (cppTango) timeout (previously the optional second positional argument) has been renamed to "poll_timeout". Conversely, the pyTango executor timeout remains as the keyword argument "timeout". These parameters have distinct meanings and units:

            - The cppTango "poll_timeout" is measured in milliseconds and blocks the call until a reply is received. If the reply is not received within the specified poll_timeout duration, an exception is thrown. Setting poll_timeout to 0 causes the call to wait indefinitely until a reply is received.
            - The pyTango "timeout" is measured in seconds and is applicable only in asynchronous GreenModes (Asyncio, Futures, Gevent), and only when "wait" is set to True. The specific behavior when a reply is not received within the specified timeout period varies depending on the GreenMode.

        :param id: the asynchronous call identifier
        :type id: int

        :param poll_timeout: cppTango core timeout in ms.
            If the reply has not yet arrived, the call will wait for the time specified (in ms).
            If after timeout, the reply is still not there, an exception is thrown.
            If timeout set to 0, the call waits until the reply arrives.
            If the argument is not provided, then there is no timeout check, and an
            exception is raised immediately if the reply is not ready.
        :type poll_timeout: Optional[int]

        :param extract_as: Defaults to numpy.
        :type extract_as: ExtractAs

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: None
        :rtype: None

        :throws: Union[AsynCall, AsynReplyNotArrived, ConnectionFailed, CommunicationFailed, DevFailed]
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        """
    def write_read_attribute(
        self,
        attr: str | AttributeInfoEx,
        value: typing.Any,
        extract_as: ExtractAs = ...,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> DeviceAttribute:
        """Write then read a single attribute in a single network call.
         By default (serialisation by device), the execution of this call in
         the server can't be interrupted by other clients.

         :param attr: The name or AttributeInfoEx structure of the attribute to write.
         :type attr: str | :obj:`~tango.AttributeInfoEx`

         :param value: The value to write to the attribute.
         :type value: Any

         :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
         :type green_mode: :obj:`tango.GreenMode`, optional

         :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
         :type wait: bool, optional

         :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
         :type timeout: float, optional

         :returns: A DeviceAttribute object with readout value.
         :rtype: :obj:`tango.DeviceAttribute`

         :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
         :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
         :throws: :obj:`tango.DeviceUnlocked`: Raised in case of an unlocked device.
         :throws: :obj:`tango.WrongData`: Raised in case of a wrong data format.
         :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
         :throws: TypeError: Raised in case of an incorrect type of input arguments.
         :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
         :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

         .. note::
             There are two possibilities for the attr parameter: if you give attribute name,
             then PyTango will do additional IO to fetch AttributeInfoEx object from device server,
             since we must know to which c++ data type cast python value. If you would like to avoid this IO you
             can give AttributeInfoEx instead of attribute name.

         .. versionadded:: 7.0.0

         .. versionadded:: 8.1.0
             *green_mode* parameter.
             *wait* parameter.
             *timeout* parameter.

        .. versionchanged:: 10.1.0

             - attr_name parameter was renamed to attr
             - added support for AttributeInfoEx for attr parameter

        """
    def write_read_attributes(
        self,
        attr_values: list[tuple[str | AttributeInfoEx, typing.Any]],
        attr_read_names: list[str],
        extract_as: ExtractAs = ...,
        *,
        green_mode: None = None,
        wait: None = None,
        timeout: None = None,
    ) -> DeviceAttribute:
        """Write then read attribute(s) in a single network call. By
        default (serialisation by device), the execution of this
        call in the server can't be interrupted by other clients.
        On the server side, attribute(s) are first written and
        if no exception has been thrown during the write phase,
        attributes will be read.

        :param attr_values: A list of pairs (attr, value). See write_attribute
        :type attr_values: sequence<(str | AttributeInfoEx, Any)>

        :param attr_read_names: A list of attributes to read.
        :type attr_read_names: sequence<str>

        :param extract_as: Defaults to numpy.
        :type extract_as: :obj:`tango.ExtractAs`

        :param green_mode: Defaults to the current tango GreenMode. Refer to :meth:`~tango.DeviceProxy.get_green_mode` and :meth:`~tango.DeviceProxy.set_green_mode` for more details.
        :type green_mode: :obj:`tango.GreenMode`, optional

        :param wait: Specifies whether to wait for the result. If `green_mode` is *Synchronous*, this parameter is ignored as the operation always waits for the result. This parameter is also ignored when `green_mode` is Synchronous.
        :type wait: bool, optional

        :param timeout: The number of seconds to wait for the result. If set to `None`, there is no limit on the wait time. This parameter is ignored when `green_mode` is Synchronous or when `wait` is False.
        :type timeout: float, optional

        :returns: A sequence DeviceAttribute object with readout values.
        :rtype: sequence<:obj:`tango.DeviceAttribute`>

        :throws: :obj:`tango.ConnectionFailed`: Raised in case of a connection failure.
        :throws: :obj:`tango.CommunicationFailed`: Raised in case of a communication failure.
        :throws: :obj:`tango.DeviceUnlocked`: Raised in case of an unlocked device.
        :throws: :obj:`tango.WrongData`: Raised in case of a wrong data format.
        :throws: :obj:`tango.DevFailed`: Raised in case of a device failure.
        :throws: TypeError: Raised in case of an incorrect type of input arguments.
        :throws: :obj:`TimeoutError`: (green_mode == Futures) If the future didn't finish executing before the given timeout.
        :throws: :obj:`Timeout`: (green_mode == Gevent) If the async result didn't finish executing before the given timeout.

        New in PyTango 9.2.0

        .. note::
            For each pair of values there are two possibilities for the
            attr parameter: if you give attribute name, then PyTango must
            fetch attribute info for this attribute from server by additional synchronous(!)
            IO, since we must know to which c++ data type cast each python value.
            If you would like to avoid this IO you must give AttributeInfoEx instead of
            attribute name for each(!) pair of values.

        .. versionchanged:: 10.1.0

            - name_val parameter was renamed to attr_values
            - added support for AttributeInfoEx for attr_values parameter.


        """

class DeviceUnlocked(DevFailed): ...

class Device_2Impl(DeviceImpl):
    def __init__(
        self,
        klass: DeviceClass,
        name: str,
        description: str = "A Tango device",
        state: DevState = tango.DevState.UNKNOWN,
        status: str = "Not initialised",
    ) -> None: ...
    def _get_attribute_config_2(self, arg0: list[str]) -> list[AttributeConfig_2]: ...
    def get_attribute_config_2(
        self, attr_names
    ) -> list[tango._tango.AttributeConfig_2]:
        """Returns the list of :obj:`tango.AttributeConfig_2` for the requested names

        :param attr_names: sequence of str with attribute names, or single attribute name
        :type attr_names: list[str] | str

        :returns: :class:`tango.AttributeConfig_2` for each requested attribute name
        :rtype: list[:class:`tango.AttributeConfig_2`]
        """

class Device_3Impl(Device_2Impl):
    def __init__(
        self,
        klass: DeviceClass,
        name: str,
        description: str = "A Tango device",
        state: DevState = tango.DevState.UNKNOWN,
        status: str = "Not initialised",
    ) -> None: ...
    def _get_attribute_config_3(self, arg0: list[str]) -> list[AttributeConfig_3]: ...
    def always_executed_hook(self) -> None:
        """always_executed_hook(self)

            Hook method.

            Default method to implement an action necessary on a device before
            any command is executed. This method can be redefined in sub-classes
            in case of the default behaviour does not fullfill the needs

        :raises DevFailed: This method does not throw exception but a redefined method can.
        """
    def delete_device(self) -> None:
        """delete_device(self)

        Delete the device.
        """
    def dev_state(self) -> DevState:
        """dev_state(self) -> DevState

            Get device state.

            Default method to get device state. The behaviour of this method depends
            on the device state. If the device state is ON or ALARM, it reads the
            attribute(s) with an alarm level defined, check if the read value is
            above/below the alarm and eventually change the state to ALARM, return
            the device state. For all th other device state, this method simply
            returns the state This method can be redefined in sub-classes in case
            of the default behaviour does not fullfill the needs.

        :returns: the device state
        :rtype: DevState

        :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading
        """
    def dev_status(self) -> str:
        """dev_status(self) -> str

            Get device status.

            Default method to get device status. It returns the contents of the device
            dev_status field. If the device state is ALARM, alarm messages are added
            to the device status. This method can be redefined in sub-classes in case
            of the default behaviour does not fullfill the needs.

        :returns: the device status
        :rtype: str

        :raises DevFailed: If it is necessary to read attribute(s) and a problem occurs during the reading
        """
    def get_attribute_config_3(
        self, attr_names
    ) -> list[tango._tango.AttributeConfig_3]:
        """Returns the list of :obj:`tango.AttributeConfig_3` for the requested names

        :param attr_names: sequence of str with attribute names, or single attribute name
        :type attr_names: list[str] | str

        :returns: :class:`tango.AttributeConfig_3` for each requested attribute name
        :rtype: list[:class:`tango.AttributeConfig_3`]
        """
    def init_device(self) -> None: ...
    def read_attr_hardware(self, attr_list: StdLongVector) -> None:
        """read_attr_hardware(self, attr_list)

            Read the hardware to return attribute value(s).

            Default method to implement an action necessary on a device to read
            the hardware involved in a read attribute CORBA call. This method
            must be redefined in sub-classes in order to support attribute reading

        :param attr_list: list of indices in the device object attribute vector
                          of an attribute to be read.
        :type attr_list: Sequence[int]

        :raises DevFailed: This method does not throw exception but a redefined method can.
        """
    def server_init_hook(self) -> None:
        """server_init_hook(self)

            Hook method.

            This method is called once the device server admin device is exported.
            This allows for instance for the different devices to subscribe
            to events at server startup on attributes from other devices
            of the same device server with stateless parameter set to false.

            This method can be redefined in sub-classes in case of the default
            behaviour does not fullfill the needs

        .. versionadded:: 9.4.2
        """
    def set_attribute_config_3(self, new_conf: list[AttributeConfig_3]) -> None:
        """set_attribute_config_3(self, new_conf) -> None

            Sets attribute configuration locally and in the Tango database

        :param new_conf: The new attribute(s) configuration. One AttributeConfig structure is needed for each attribute to update
        :type new_conf: list[:class:`tango.AttributeConfig_3`]

        :returns: None
        :rtype: None
        """
    def signal_handler(self, signo: typing.SupportsInt) -> None:
        """signal_handler(self, signo)

            Signal handler.

            The method executed when the signal arrived in the device server process.
            This method is defined as virtual and then, can be redefined following
            device needs.

        :param signo: the signal number
        :type signo: int

        :raises DevFailed: This method does not throw exception but a redefined method can.
        """
    def write_attr_hardware(self, attr_list: StdLongVector) -> None:
        """write_attr_hardware(self, attr_list)

            Write the hardware for attributes.

            Default method to implement an action necessary on a device to write
            the hardware involved in a write attribute. This method must be
            redefined in sub-classes in order to support writable attribute

        :param attr_list: list of indices in the device object attribute vector
                          of an attribute to be written.
        :type attr_list: Sequence[int]

        :raises DevFailed: This method does not throw exception but a redefined method can.
        """

class Device_4Impl(Device_3Impl):
    def __init__(
        self,
        klass: DeviceClass,
        name: str,
        description: str = "A Tango device",
        state: DevState = tango.DevState.UNKNOWN,
        status: str = "Not initialised",
    ) -> None: ...
    def always_executed_hook(self) -> None: ...
    def delete_device(self) -> None: ...
    def dev_state(self) -> DevState: ...
    def dev_status(self) -> str: ...
    def init_device(self) -> None: ...
    def read_attr_hardware(self, arg0: StdLongVector) -> None: ...
    def server_init_hook(self) -> None: ...
    def write_attr_hardware(self, arg0: StdLongVector) -> None: ...

class Device_5Impl(Device_4Impl):
    def __init__(
        self,
        klass: DeviceClass,
        name: str,
        description: str = "A Tango device",
        state: DevState = tango.DevState.UNKNOWN,
        status: str = "Not initialised",
    ) -> None: ...
    def always_executed_hook(self) -> None: ...
    def delete_device(self) -> None: ...
    def dev_state(self) -> DevState: ...
    def dev_status(self) -> str: ...
    def init_device(self) -> None: ...
    def read_attr_hardware(self, arg0: StdLongVector) -> None: ...
    def server_init_hook(self) -> None: ...
    def write_attr_hardware(self, arg0: StdLongVector) -> None: ...

class Device_6Impl(Device_5Impl):
    def __init__(
        self,
        klass: DeviceClass,
        name: str,
        description: str = "A Tango device",
        state: DevState = tango.DevState.UNKNOWN,
        status: str = "Not initialised",
    ) -> None: ...
    def always_executed_hook(self) -> None: ...
    def delete_device(self) -> None: ...
    def dev_state(self) -> DevState: ...
    def dev_status(self) -> str: ...
    def init_device(self) -> None: ...
    def read_attr_hardware(self, arg0: StdLongVector) -> None: ...
    def server_init_hook(self) -> None: ...
    def write_attr_hardware(self, arg0: StdLongVector) -> None: ...

class DispLevel(enum.IntEnum):
    """An enumeration representing the display level"""

    DL_UNKNOWN: typing.ClassVar[DispLevel]  # value = <DispLevel.DL_UNKNOWN: 2>
    EXPERT: typing.ClassVar[DispLevel]  # value = <DispLevel.EXPERT: 1>
    OPERATOR: typing.ClassVar[DispLevel]  # value = <DispLevel.OPERATOR: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class EncodedAttribute:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self, buf_pool_size: typing.SupportsInt, serialization: bool = False
    ) -> None: ...
    def _decode_gray16(self, arg0: DeviceAttribute, arg1: ExtractAs) -> typing.Any: ...
    def _decode_gray8(self, arg0: DeviceAttribute, arg1: ExtractAs) -> typing.Any: ...
    def _decode_rgb32(self, arg0: DeviceAttribute, arg1: ExtractAs) -> typing.Any: ...
    def _encode_gray16(
        self, arg0: typing.Any, arg1: typing.SupportsInt, arg2: typing.SupportsInt
    ) -> None: ...
    def _encode_gray8(
        self, arg0: typing.Any, arg1: typing.SupportsInt, arg2: typing.SupportsInt
    ) -> None: ...
    def _encode_jpeg_gray8(
        self,
        arg0: typing.Any,
        arg1: typing.SupportsInt,
        arg2: typing.SupportsInt,
        arg3: typing.SupportsFloat,
    ) -> None: ...
    def _encode_jpeg_rgb24(
        self,
        arg0: typing.Any,
        arg1: typing.SupportsInt,
        arg2: typing.SupportsInt,
        arg3: typing.SupportsFloat,
    ) -> None: ...
    def _encode_jpeg_rgb32(
        self,
        arg0: typing.Any,
        arg1: typing.SupportsInt,
        arg2: typing.SupportsInt,
        arg3: typing.SupportsFloat,
    ) -> None: ...
    def _encode_rgb24(
        self, arg0: typing.Any, arg1: typing.SupportsInt, arg2: typing.SupportsInt
    ) -> None: ...
    def _generic_encode_gray8(self, gray8, width=0, height=0, quality=0, format=...):
        """Internal usage only"""
    def _generic_encode_rgb24(self, rgb24, width=0, height=0, quality=0, format=...):
        """Internal usage only"""
    def decode_gray16(self, da, extract_as=...):
        """Decode a 16 bits grayscale image (GRAY16) and returns a 16 bits gray scale image.

         :param da: :class:`DeviceAttribute` that contains the image
         :type da: :class:`DeviceAttribute`
         :param extract_as: defaults to ExtractAs.Numpy
         :type extract_as: ExtractAs
         :return: the decoded data

         - In case String string is choosen as extract method, a tuple is returned:
             width<int>, height<int>, buffer<str>
         - In case Numpy is choosen as extract method, a :class:`numpy.ndarray` is
           returned with ndim=2, shape=(height, width) and dtype=numpy.uint16.
         - In case Tuple or List are choosen, a tuple<tuple<int>> or list<list<int>>
           is returned.

        .. warning::
            The PyTango calls that return a :class:`DeviceAttribute`
            (like :meth:`DeviceProxy.read_attribute` or :meth:`DeviceProxy.command_inout`)
            automatically extract the contents by default. This method requires
            that the given :class:`DeviceAttribute` is obtained from a
            call which **DOESN'T** extract the contents. Example::

                dev = tango.DeviceProxy("a/b/c")
                da = dev.read_attribute("my_attr", extract_as=tango.ExtractAs.Nothing)
                enc = tango.EncodedAttribute()
                data = enc.decode_gray16(da)
        """
    def decode_gray8(self, da, extract_as=...):
        """Decode a 8 bits grayscale image (JPEG_GRAY8 or GRAY8) and returns a 8 bits gray scale image.

         :param da: :class:`DeviceAttribute` that contains the image
         :type da: :class:`DeviceAttribute`
         :param extract_as: defaults to ExtractAs.Numpy
         :type extract_as: ExtractAs
         :return: the decoded data

         - In case String string is choosen as extract method, a tuple is returned:
             width<int>, height<int>, buffer<str>
         - In case Numpy is choosen as extract method, a :class:`numpy.ndarray` is
           returned with ndim=2, shape=(height, width) and dtype=numpy.uint8.
         - In case Tuple or List are choosen, a tuple<tuple<int>> or list<list<int>>
           is returned.

        .. warning::
            The PyTango calls that return a :class:`DeviceAttribute`
            (like :meth:`DeviceProxy.read_attribute` or :meth:`DeviceProxy.command_inout`)
            automatically extract the contents by default. This method requires
            that the given :class:`DeviceAttribute` is obtained from a
            call which **DOESN'T** extract the contents. Example::

                dev = tango.DeviceProxy("a/b/c")
                da = dev.read_attribute("my_attr", extract_as=tango.ExtractAs.Nothing)
                enc = tango.EncodedAttribute()
                data = enc.decode_gray8(da)
        """
    def decode_rgb32(self, da, extract_as=...):
        """Decode a color image (JPEG_RGB or RGB24) and returns a 32 bits RGB image.

         :param da: :class:`DeviceAttribute` that contains the image
         :type da: :class:`DeviceAttribute`
         :param extract_as: defaults to ExtractAs.Numpy
         :type extract_as: ExtractAs
         :return: the decoded data

         - In case String string is choosen as extract method, a tuple is returned:
             width<int>, height<int>, buffer<str>
         - In case Numpy is choosen as extract method, a :class:`numpy.ndarray` is
           returned with ndim=2, shape=(height, width) and dtype=numpy.uint32.
         - In case Tuple or List are choosen, a tuple<tuple<int>> or list<list<int>>
           is returned.

        .. warning::
            The PyTango calls that return a :class:`DeviceAttribute`
            (like :meth:`DeviceProxy.read_attribute` or :meth:`DeviceProxy.command_inout`)
            automatically extract the contents by default. This method requires
            that the given :class:`DeviceAttribute` is obtained from a
            call which **DOESN'T** extract the contents. Example::

                dev = tango.DeviceProxy("a/b/c")
                da = dev.read_attribute("my_attr", extract_as=tango.ExtractAs.Nothing)
                enc = tango.EncodedAttribute()
                data = enc.decode_rgb32(da)
        """
    def encode_gray16(self, gray16, width=0, height=0):
        """Encode a 16 bit grayscale image (no compression)

            :param gray16: an object containning image information
            :type gray16: :py:obj:`str` or :py:obj:`buffer` or :class:`numpy.ndarray` or seq< seq<element> >
            :param width: image width. **MUST** be given if gray16 is a string or
                          if it is a :class:`numpy.ndarray` with ndims != 2.
                          Otherwise it is calculated internally.
            :type width: :py:obj:`int`
            :param height: image height. **MUST** be given if gray16 is a string
                           or if it is a :class:`numpy.ndarray` with ndims != 2.
                           Otherwise it is calculated internally.
            :type height: :py:obj:`int`

        .. note::
            When :class:`numpy.ndarray` is given:

                - gray16 **MUST** be CONTIGUOUS, ALIGNED
                - if gray16.ndims != 2, width and height **MUST** be given and
                  gray16.nbytes/2 **MUST** match width*height
                - if gray16.ndims == 2, gray16.itemsize **MUST** be 2 (typically,
                  gray16.dtype is one of `numpy.dtype.int16`, `numpy.dtype.uint16`,
                  `numpy.dtype.short` or `numpy.dtype.ushort`)

        Example::

            def read_myattr(self):
                enc = tango.EncodedAttribute()
                data = numpy.arange(100, dtype=numpy.int16)
                data = numpy.array((data,data,data))
                enc.encode_gray16(data)
                return enc
        """
    def encode_gray8(self, gray8, width=0, height=0):
        """Encode a 8 bit grayscale image (no compression)

            :param gray8: an object containning image information
            :type gray8: :py:obj:`str` or :class:`numpy.ndarray` or seq< seq<element> >
            :param width: image width. **MUST** be given if gray8 is a string or
                          if it is a :class:`numpy.ndarray` with ndims != 2.
                          Otherwise it is calculated internally.
            :type width: :py:obj:`int`
            :param height: image height. **MUST** be given if gray8 is a string
                           or if it is a :class:`numpy.ndarray` with ndims != 2.
                           Otherwise it is calculated internally.
            :type height: :py:obj:`int`

        .. note::
            When :class:`numpy.ndarray` is given:

                - gray8 **MUST** be CONTIGUOUS, ALIGNED
                - if gray8.ndims != 2, width and height **MUST** be given and
                  gray8.nbytes **MUST** match width*height
                - if gray8.ndims == 2, gray8.itemsize **MUST** be 1 (typically,
                  gray8.dtype is one of `numpy.dtype.byte`, `numpy.dtype.ubyte`,
                  `numpy.dtype.int8` or `numpy.dtype.uint8`)

        Example::

            def read_myattr(self):
                enc = tango.EncodedAttribute()
                data = numpy.arange(100, dtype=numpy.byte)
                data = numpy.array((data,data,data))
                enc.encode_gray8(data)
                return enc
        """
    def encode_jpeg_gray8(self, gray8, width=0, height=0, quality=100.0):
        """Encode a 8 bit grayscale image as JPEG format

            :param gray8: an object containning image information
            :type gray8: :py:obj:`str` or :class:`numpy.ndarray` or seq< seq<element> >
            :param width: image width. **MUST** be given if gray8 is a string or
                          if it is a :class:`numpy.ndarray` with ndims != 2.
                          Otherwise it is calculated internally.
            :type width: :py:obj:`int`
            :param height: image height. **MUST** be given if gray8 is a string
                           or if it is a :class:`numpy.ndarray` with ndims != 2.
                           Otherwise it is calculated internally.
            :type height: :py:obj:`int`
            :param quality: Quality of JPEG (0=poor quality 100=max quality) (default is 100.0)
            :type quality: :py:obj:`float`

        .. note::
            When :class:`numpy.ndarray` is given:

                - gray8 **MUST** be CONTIGUOUS, ALIGNED
                - if gray8.ndims != 2, width and height **MUST** be given and
                  gray8.nbytes **MUST** match width*height
                - if gray8.ndims == 2, gray8.itemsize **MUST** be 1 (typically,
                  gray8.dtype is one of `numpy.dtype.byte`, `numpy.dtype.ubyte`,
                  `numpy.dtype.int8` or `numpy.dtype.uint8`)

        Example::

            def read_myattr(self):
                enc = tango.EncodedAttribute()
                data = numpy.arange(100, dtype=numpy.byte)
                data = numpy.array((data,data,data))
                enc.encode_jpeg_gray8(data)
                return enc
        """
    def encode_jpeg_rgb24(self, rgb24, width=0, height=0, quality=100.0):
        """Encode a 24 bit rgb color image as JPEG format.

            :param rgb24: an object containning image information
            :type rgb24: :py:obj:`str` or :class:`numpy.ndarray` or seq< seq<element> >
            :param width: image width. **MUST** be given if rgb24 is a string or
                          if it is a :class:`numpy.ndarray` with ndims != 3.
                          Otherwise it is calculated internally.
            :type width: :py:obj:`int`
            :param height: image height. **MUST** be given if rgb24 is a string
                           or if it is a :class:`numpy.ndarray` with ndims != 3.
                           Otherwise it is calculated internally.
            :type height: :py:obj:`int`
            :param quality: Quality of JPEG (0=poor quality 100=max quality) (default is 100.0)
            :type quality: :py:obj:`float`

        .. note::
            When :class:`numpy.ndarray` is given:

                - rgb24 **MUST** be CONTIGUOUS, ALIGNED
                - if rgb24.ndims != 3, width and height **MUST** be given and
                  rgb24.nbytes/3 **MUST** match width*height
                - if rgb24.ndims == 3, rgb24.itemsize **MUST** be 1 (typically,
                  rgb24.dtype is one of `numpy.dtype.byte`, `numpy.dtype.ubyte`,
                  `numpy.dtype.int8` or `numpy.dtype.uint8`) and shape **MUST** be
                  (height, width, 3)

        Example::

            def read_myattr(self):
                enc = tango.EncodedAttribute()
                # create an 'image' where each pixel is R=0x01, G=0x01, B=0x01
                arr = numpy.ones((10,10,3), dtype=numpy.uint8)
                enc.encode_jpeg_rgb24(data)
                return enc
        """
    def encode_jpeg_rgb32(self, rgb32, width=0, height=0, quality=100.0):
        """Encode a 32 bit rgb color image as JPEG format.

            :param rgb32: an object containning image information
            :type rgb32: :py:obj:`str` or :class:`numpy.ndarray` or seq< seq<element> >
            :param width: image width. **MUST** be given if rgb32 is a string or
                          if it is a :class:`numpy.ndarray` with ndims != 2.
                          Otherwise it is calculated internally.
            :type width: :py:obj:`int`
            :param height: image height. **MUST** be given if rgb32 is a string
                           or if it is a :class:`numpy.ndarray` with ndims != 2.
                           Otherwise it is calculated internally.
            :type height: :py:obj:`int`

        .. note::
            When :class:`numpy.ndarray` is given:

                - rgb32 **MUST** be CONTIGUOUS, ALIGNED
                - if rgb32.ndims != 2, width and height **MUST** be given and
                  rgb32.nbytes/4 **MUST** match width*height
                - if rgb32.ndims == 2, rgb32.itemsize **MUST** be 4 (typically,
                  rgb32.dtype is one of `numpy.dtype.int32`, `numpy.dtype.uint32`)

        .. note::

            Encoding with transparency information required cppTango built with `TANGO_USE_JPEG` options
            see installation instructions of cppTango

        Example::

            def read_myattr(self):
                enc = tango.EncodedAttribute()
                data = numpy.arange(100, dtype=numpy.int32)
                data = numpy.array((data,data,data))
                enc.encode_jpeg_rgb32(data)
                return enc
        """
    def encode_rgb24(self, rgb24, width=0, height=0):
        """Encode a 24 bit color image (no compression)

            :param rgb24: an object containning image information
            :type rgb24: :py:obj:`str` or :class:`numpy.ndarray` or seq< seq<element> >
            :param width: image width. **MUST** be given if rgb24 is a string or
                          if it is a :class:`numpy.ndarray` with ndims != 3.
                          Otherwise it is calculated internally.
            :type width: :py:obj:`int`
            :param height: image height. **MUST** be given if rgb24 is a string
                           or if it is a :class:`numpy.ndarray` with ndims != 3.
                           Otherwise it is calculated internally.
            :type height: :py:obj:`int`

        .. note::
            When :class:`numpy.ndarray` is given:

                - rgb24 **MUST** be CONTIGUOUS, ALIGNED
                - if rgb24.ndims != 3, width and height **MUST** be given and
                  rgb24.nbytes/3 **MUST** match width*height
                - if rgb24.ndims == 3, rgb24.itemsize **MUST** be 1 (typically,
                  rgb24.dtype is one of `numpy.dtype.byte`, `numpy.dtype.ubyte`,
                  `numpy.dtype.int8` or `numpy.dtype.uint8`) and shape **MUST** be
                  (height, width, 3)

        Example::

            def read_myattr(self):
                enc = tango.EncodedAttribute()
                # create an 'image' where each pixel is R=0x01, G=0x01, B=0x01
                arr = numpy.ones((10,10,3), dtype=numpy.uint8)
                enc.encode_rgb24(data)
                return enc
        """

class EnsureOmniThread:
    """Tango servers and clients that start their own additional threads
    that will interact with Tango must guard these threads within this
    Python context.  This is especially important when working with
    event subscriptions, and pushing events.

    This context handler class ensures a non-omniORB thread will still
    get a dummy omniORB thread ID - cppTango requires threads to
    be identifiable in this way.  It should only be acquired once for
    the lifetime of the thread, and must be released before the thread
    is cleaned up.

    Here is an example::

        import tango
        from threading import Thread
        from time import sleep


        def my_thread_run():
            with tango.EnsureOmniThread():
                eid = dp.subscribe_event(
                    "double_scalar", tango.EventType.PERIODIC_EVENT, cb)
                while running:
                    print(f"num events stored {len(cb.get_events())}")
                    sleep(1)
                dp.unsubscribe_event(eid)


        cb = tango.utils.EventCallback()  # print events to stdout
        dp = tango.DeviceProxy("sys/tg_test/1")
        dp.poll_attribute("double_scalar", 1000)
        thread = Thread(target=my_thread_run)
        running = True
        thread.start()
        sleep(5)
        running = False
        thread.join()

    .. versionadded:: 9.3.2
    """
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_value, traceback): ...
    def __init__(self) -> None: ...
    def _acquire(self) -> None: ...
    def _release(self) -> None: ...

class ErrSeverity(enum.IntEnum):
    """An enumeration representing the error severity"""

    ERR: typing.ClassVar[ErrSeverity]  # value = <ErrSeverity.ERR: 1>
    PANIC: typing.ClassVar[ErrSeverity]  # value = <ErrSeverity.PANIC: 2>
    WARN: typing.ClassVar[ErrSeverity]  # value = <ErrSeverity.WARN: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class EventData:
    """This class is used to pass data to the callback method when an event
    related to attribute data is sent to the client. It contains the following public fields:

         - device : (DeviceProxy) The DeviceProxy object on which the call was
           executed.
         - attr_name : (str) The attribute name
         - event : (str) The event type name
         - event_reason : (EventReason) The reason for the event
         - attr_value : (DeviceAttribute) The attribute data
         - err : (bool) A boolean flag set to true if the request failed. False
           otherwise
         - errors : (sequence<DevError>) The error stack
         - reception_date: (TimeVal)

    .. note::
        The ``attr_value`` field may be ``None``.  E.g., if ``err`` is True, or when subscribing in
        ``EventSubMode.Async`` mode and the initial callback is received with ``EventReason.SubSuccess``.
    """

    attr_value = None
    attr_name: str
    device: ...
    err: bool
    event: str
    event_reason: EventReason
    reception_date: TimeVal
    @typing.overload
    def __init__(self, arg0: EventData) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    def get_date(self) -> TimeVal:
        """get_date(self) -> TimeVal

            Returns the timestamp of the event.

        :returns: the timestamp of the event
        :rtype: TimeVal

        New in PyTango 7.0.0
        """
    @property
    def errors(self) -> list[DevError]: ...
    @errors.setter
    def errors(self, arg1: typing.Any) -> None: ...

class EventDataList:
    __hash__: typing.ClassVar[None] = None
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: EventData) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: EventDataList) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> EventDataList:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> EventData: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: EventDataList) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[EventData]: ...
    def __len__(self) -> int: ...
    def __ne__(self, arg0: EventDataList) -> bool: ...
    def __repr__(self) -> str:
        """Return the canonical string representation of this list."""
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: EventData) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: EventDataList) -> None:
        """Assign list elements using a slice object"""
    def append(self, x: EventData) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: EventData) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: EventDataList) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: EventData) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> EventData:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> EventData:
        """Remove and return the item at index ``i``"""
    def remove(self, x: EventData) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class EventProperties:
    arch_event: ArchiveEventProp
    ch_event: ChangeEventProp
    per_event: PeriodicEventProp
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""

class EventReason(enum.IntEnum):
    """An enumeration representing the reason for an event.

    * ``EventReason.SubSuccess`` - initial subscription was successful.  Note: Event data will not have a value for `EventSubMode.Async` subscription.  Not emitted for `EventSubMode.Sync`.
    * ``EventReason.Update`` -  new event available. Device has pushed a new event, or re-subscription after loosing connection to device (e.g., after restart).
    * ``EventReason.SubFail`` - initial asynchronous subscription failed, or event system down ("Event channel is not responding anymore").
    * ``EventReason.Unknown`` - unexpected - probably a bug in cppTango or PyTango.

    See :class:`tango.EventSubMode`.

    .. versionadded:: 10.1.0
    """

    SubFail: typing.ClassVar[EventReason]  # value = <EventReason.SubFail: 1>
    SubSuccess: typing.ClassVar[EventReason]  # value = <EventReason.SubSuccess: 2>
    Unknown: typing.ClassVar[EventReason]  # value = <EventReason.Unknown: 0>
    Update: typing.ClassVar[EventReason]  # value = <EventReason.Update: 3>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class EventSubMode(enum.IntEnum):
    """An enumeration representing the sub mode used when subscribing to events.

    * ``EventSubMode.SyncRead`` - synchronous subscription including attribute read (raises exception on failure), first callback immediately with current value.
    * ``EventSubMode.AsyncRead`` - asynchronous subscription and asynchronous attribute read (no exception on failure, retries automatically), first callback "soon" after read with current value.
    * ``EventSubMode.Sync`` - synchronous subscription without reading attribute (raises exception on failure), no callback on subscription (only on next event).
    * ``EventSubMode.Async`` - asynchronous subscription without reading attribute (no exception on failure, retries automatically), first callback with no value when subscription completed.
    * ``EventSubMode.Stateless`` - synchronous subscription including attribute read (no exception on failure, retries automatically) - equivalent to old stateless=True option, first callback immediately with current value.  Consider ``AsyncRead`` instead.

    The table below summarises this:

    .. list-table:: Event Subscription Modes
       :header-rows: 1

       * - EventSubMode
         - Tries subscription before returning
         - Raises on subscription failure
         - Reads entity
         - First callback
       * - SyncRead
         - Yes
         - Yes
         - Yes, during subscription
         - Immediately, with data
       * - AsyncRead
         - No
         - No
         - Yes, after subscription
         - After read, with data
       * - Sync
         - Yes
         - Yes
         - No
         - Only on next event
       * - Async
         - No
         - No
         - No
         - After subscription, no data
       * - Stateless
         - Yes
         - No
         - Yes, during subscription
         - Immediately, with data

    See :meth:`tango.DeviceProxy.subscribe_event`.

    .. versionadded:: 10.1.0
    """

    Async: typing.ClassVar[EventSubMode]  # value = <EventSubMode.Async: 3>
    AsyncRead: typing.ClassVar[EventSubMode]  # value = <EventSubMode.AsyncRead: 4>
    Stateless: typing.ClassVar[EventSubMode]  # value = <EventSubMode.Stateless: 5>
    Sync: typing.ClassVar[EventSubMode]  # value = <EventSubMode.Sync: 1>
    SyncRead: typing.ClassVar[EventSubMode]  # value = <EventSubMode.SyncRead: 2>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class EventSystemFailed(DevFailed): ...

class EventType(enum.IntEnum):
    """An enumeration representing event type

    .. versionchanged:: 7.0.0 Added DATA_READY_EVENT
    .. versionchanged:: 9.2.2 Added INTERFACE_CHANGE_EVENT\\n
    .. versionchanged:: 10.0.0 Added ALARM_EVENT
    .. versionchanged:: 10.0.0 Removed QUALITY_EVENT
    .. versionchanged:: 10.1.0 Removed PIPE_EVENT
    """

    ALARM_EVENT: typing.ClassVar[EventType]  # value = <EventType.ALARM_EVENT: 9>
    ARCHIVE_EVENT: typing.ClassVar[EventType]  # value = <EventType.ARCHIVE_EVENT: 3>
    ATTR_CONF_EVENT: typing.ClassVar[
        EventType
    ]  # value = <EventType.ATTR_CONF_EVENT: 5>
    CHANGE_EVENT: typing.ClassVar[EventType]  # value = <EventType.CHANGE_EVENT: 0>
    DATA_READY_EVENT: typing.ClassVar[
        EventType
    ]  # value = <EventType.DATA_READY_EVENT: 6>
    INTERFACE_CHANGE_EVENT: typing.ClassVar[
        EventType
    ]  # value = <EventType.INTERFACE_CHANGE_EVENT: 7>
    PERIODIC_EVENT: typing.ClassVar[EventType]  # value = <EventType.PERIODIC_EVENT: 2>
    USER_EVENT: typing.ClassVar[EventType]  # value = <EventType.USER_EVENT: 4>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class Except:
    """A container for the static methods:

    - throw_exception
    - re_throw_exception
    - print_exception
    - compare_exception

    """
    @staticmethod
    def compare_exception(arg0: DevFailed, arg1: DevFailed) -> bool: ...
    @staticmethod
    def print_error_stack(arg0: list[DevError]) -> None:
        """print_error_stack(ex) -> None

        Print all the details of a TANGO error stack.

        Parameters :
        - ex     : (tango.DevErrorList) The error stack reference)
        """
    @staticmethod
    def re_throw_exception(
        exception: DevFailed,
        reason: str,
        description: str,
        origin: str,
        severity: ErrSeverity = tango.ErrSeverity.ERR,
    ) -> None:
        """re_throw_exception(ex, reason, desc, origin, sever=tango.ErrSeverity.ERR) -> None

            Re-throw a TANGO :class:`~tango.DevFailed` exception with one more error.
            The exception is re-thrown with one more :class:`~tango.DevError` object.
            A default value *tango.ErrSeverity.ERR* is defined for the new
            :class:`~tango.DevError` severity field.

        Parameters :
            - ex       : (tango.DevFailed) The :class:`~tango.DevFailed` exception
            - reason   : (str) The exception :class:`~tango.DevError` object reason field
            - desc     : (str) The exception :class:`~tango.DevError` object desc field
            - origin   : (str) The exception :class:`~tango.DevError` object origin field
            - severity : (tango.ErrSeverity) The exception DevError object severity field

        Throws     : DevFailed
        """
    @staticmethod
    def throw_exception(
        reason: str,
        description: str,
        origin: str,
        severity: ErrSeverity = tango.ErrSeverity.ERR,
    ) -> None:
        """throw_exception(reason, desc, origin, sever=tango.ErrSeverity.ERR) -> None

            Generate and throw a TANGO DevFailed exception.
            The exception is created with a single :class:`~tango.DevError`
            object. A default value *tango.ErrSeverity.ERR* is defined for
            the :class:`~tango.DevError` severity field.

        Parameters :
            - reason   : (str) The exception :class:`~tango.DevError` object reason field
            - desc     : (str) The exception :class:`~tango.DevError` object desc field
            - origin   : (str) The exception :class:`~tango.DevError` object origin field
            - severity : (tango.ErrSeverity) The exception DevError object severity field

        Throws : DevFailed
        """
    @staticmethod
    def throw_python_exception(
        type: typing.Any = None, value: typing.Any = None, traceback: typing.Any = None
    ) -> None:
        """throw_python_exception(type, value, traceback) -> None

            Generate and throw a TANGO DevFailed exception.
            The exception is created with a single :class:`~tango.DevError`
            object. A default value *tango.ErrSeverity.ERR* is defined for
            the :class:`~tango.DevError` severity field.

            The parameters are the same as the ones generates by a call to
            :func:`sys.exc_info`.

        Parameters :
            - type : (class)  the exception type of the exception being handled
            - value : (object) exception parameter (its associated value or the
                      second argument to raise, which is always a class instance
                      if the exception type is a class object)
            - traceback : (traceback) traceback object

        Throws     : DevFailed

        New in PyTango 7.2.1
        """
    @staticmethod
    def to_dev_failed(
        type: typing.Any = None, value: typing.Any = None, traceback: typing.Any = None
    ) -> DevFailed: ...

class ExtractAs(enum.IntEnum):
    """Defines what will go into value field of DeviceAttribute,
    or what will Attribute.get_write_value() return.
    Not all the possible values are valid in all the cases
    """

    ByteArray: typing.ClassVar[ExtractAs]  # value = <ExtractAs.ByteArray: 1>
    Bytes: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Bytes: 2>
    List: typing.ClassVar[ExtractAs]  # value = <ExtractAs.List: 4>
    Nothing: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Nothing: 7>
    Numpy: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Numpy: 0>
    String: typing.ClassVar[ExtractAs]  # value = <ExtractAs.String: 5>
    Tuple: typing.ClassVar[ExtractAs]  # value = <ExtractAs.Tuple: 3>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class FwdAttr:
    def __init__(self, arg0: str, arg1: str) -> None: ...
    def set_default_properties(self, prop: UserDefaultFwdAttrProp) -> None:
        """set_default_properties(self, prop: UserDefaultAttrProp) -> None

            Set default attribute properties

        :param prop: The user default property class
        :type prop: UserDefaultAttrProp
        """

class GreenMode(enum.IntEnum):
    """An enumeration representing the GreenMode

    .. versionadded:: 8.1.0
    .. versionchanged:: 8.1.9 Added Asyncio
    """

    Asyncio: typing.ClassVar[GreenMode]  # value = <GreenMode.Asyncio: 3>
    Futures: typing.ClassVar[GreenMode]  # value = <GreenMode.Futures: 1>
    Gevent: typing.ClassVar[GreenMode]  # value = <GreenMode.Gevent: 2>
    Synchronous: typing.ClassVar[GreenMode]  # value = <GreenMode.Synchronous: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class GroupAttrReply(GroupReply):
    def __repr__(self):
        """repr method for struct"""
    def __str__(self): ...
    def get_data(self, extract_as: ExtractAs = ...) -> typing.Any:
        """Get the DeviceAttribute.

        Parameters :
            - extract_as : (ExtractAs)

        Return     : (DeviceAttribute) Whatever is stored there, or None.
        """

class GroupAttrReplyList:
    def __getitem__(self, arg0: typing.SupportsInt) -> GroupAttrReply: ...
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __repr__(self): ...
    def __str__(self): ...
    def has_failed(self) -> bool: ...
    def push_back(self, arg0: GroupAttrReply) -> None: ...
    def reset(self) -> None: ...

class GroupCmdReply(GroupReply):
    def __repr__(self):
        """repr method for struct"""
    def __str__(self): ...
    def get_data(self):
        """get_data(self) -> any

            Get the actual value stored in the GroupCmdRply, the command
            output value.
            It's the same as self.get_data_raw().extract()

        Parameters : None
        Return     : (any) Whatever is stored there, or None.
        """
    def get_data_raw(self) -> DeviceData:
        """get_data_raw(self) -> any

            Get the DeviceData containing the output parameter
            of the command.

        Parameters : None
        Return     : (DeviceData) Whatever is stored there, or None.
        """

class GroupCmdReplyList:
    def __getitem__(self, arg0: typing.SupportsInt) -> GroupCmdReply: ...
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __repr__(self): ...
    def __str__(self): ...
    def has_failed(self) -> bool: ...
    def push_back(self, arg0: GroupCmdReply) -> None: ...
    def reset(self) -> None: ...

class GroupReply:
    """This is the base class for the result of an operation on a
    PyTangoGroup, being it a write attribute, read attribute, or
    command inout operation.

    It has some trivial common operations:

        - has_failed(self) -> bool
        - group_element_enabled(self) ->bool
        - dev_name(self) -> str
        - obj_name(self) -> str
        - get_err_stack(self) -> DevErrorList
    """
    def __init__(self, arg0: GroupReply) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self): ...
    def dev_name(self) -> str:
        """dev_name(self) -> str

            Returns the device name for the group element

        :return: The device name
        :rtype: str
        """
    def get_err_stack(self) -> list[DevError]:
        """get_err_stack(self) -> DevErrorList

            Get error stack

        :return: The error stack
        :rtype: DevErrorList
        """
    def group_element_enabled(self) -> bool:
        """group_element_enabled(self) -> bool

            Check if the group element corresponding to this reply is enabled.

        :return: true if corresponding element is enabled, false otherwise
        :rtype: bool
        """
    def has_failed(self) -> bool: ...
    def obj_name(self) -> str:
        """obj_name(self) -> str

            The object name

        :return: The device name
        :rtype: str
        """

class GroupReplyList:
    def __getitem__(self, arg0: typing.SupportsInt) -> GroupReply: ...
    def __init__(self) -> None: ...
    def __len__(self) -> int: ...
    def __repr__(self): ...
    def __str__(self): ...
    def has_failed(self) -> bool: ...
    def push_back(self, arg0: GroupReply) -> None: ...
    def reset(self) -> None: ...

class ImageAttr(SpectrumAttr):
    def __init__(
        self,
        arg0: str,
        arg1: typing.SupportsInt,
        arg2: AttrWriteType,
        arg3: typing.SupportsInt,
        arg4: typing.SupportsInt,
    ) -> None: ...

class Interceptors:
    def __init__(self) -> None: ...
    def create_thread(self) -> None: ...
    def delete_thread(self) -> None: ...

class KeepAliveCmdCode(enum.IntEnum):
    """An enumeration representing the KeepAliveCmdCode

    New in PyTango 7.1.0
    """

    EXIT_TH: typing.ClassVar[KeepAliveCmdCode]  # value = <KeepAliveCmdCode.EXIT_TH: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class Level:
    @staticmethod
    def get_name(arg0: typing.SupportsInt) -> str: ...
    @staticmethod
    def get_value(arg0: str) -> int: ...

class LevelLevel(enum.IntEnum):
    DEBUG: typing.ClassVar[LevelLevel]  # value = <LevelLevel.DEBUG: 600>
    ERROR: typing.ClassVar[LevelLevel]  # value = <LevelLevel.ERROR: 300>
    FATAL: typing.ClassVar[LevelLevel]  # value = <LevelLevel.FATAL: 200>
    INFO: typing.ClassVar[LevelLevel]  # value = <LevelLevel.INFO: 500>
    OFF: typing.ClassVar[LevelLevel]  # value = <LevelLevel.OFF: 100>
    WARN: typing.ClassVar[LevelLevel]  # value = <LevelLevel.WARN: 400>
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class LockCmdCode(enum.IntEnum):
    """An enumeration representing the LockCmdCode

    New in PyTango 7.0.0
    """

    LOCK_ADD_DEV: typing.ClassVar[LockCmdCode]  # value = <LockCmdCode.LOCK_ADD_DEV: 0>
    LOCK_EXIT: typing.ClassVar[LockCmdCode]  # value = <LockCmdCode.LOCK_EXIT: 3>
    LOCK_REM_DEV: typing.ClassVar[LockCmdCode]  # value = <LockCmdCode.LOCK_REM_DEV: 1>
    LOCK_UNLOCK_ALL_EXIT: typing.ClassVar[
        LockCmdCode
    ]  # value = <LockCmdCode.LOCK_UNLOCK_ALL_EXIT: 2>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class LockerInfo:
    """A structure with information about the locker with the following members:

    - ll : (tango.LockerLanguage) the locker language
    - li : (pid_t / UUID) the locker id
    - locker_host : (str) the host
    - locker_class : (str) the class

    pid_t should be an int, UUID should be a tuple of four numbers.

    New in PyTango 7.0.0
    """
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""
    @property
    def li(self) -> typing.Any: ...
    @property
    def ll(self) -> LockerLanguage: ...
    @property
    def locker_class(self) -> str: ...
    @property
    def locker_host(self) -> str: ...

class LockerLanguage(enum.IntEnum):
    """An enumeration representing the programming language in which the client application who locked is written.

    New in PyTango 7.0.0
    """

    CPP: typing.ClassVar[LockerLanguage]  # value = <LockerLanguage.CPP: 0>
    CPP_6: typing.ClassVar[LockerLanguage]  # value = <LockerLanguage.CPP_6: 2>
    JAVA: typing.ClassVar[LockerLanguage]  # value = <LockerLanguage.JAVA: 1>
    JAVA_6: typing.ClassVar[LockerLanguage]  # value = <LockerLanguage.JAVA_6: 3>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class LogLevel(enum.IntEnum):
    """An enumeration representing the LogLevel

    New in PyTango 7.0.0
    """

    LOG_DEBUG: typing.ClassVar[LogLevel]  # value = <LogLevel.LOG_DEBUG: 5>
    LOG_ERROR: typing.ClassVar[LogLevel]  # value = <LogLevel.LOG_ERROR: 2>
    LOG_FATAL: typing.ClassVar[LogLevel]  # value = <LogLevel.LOG_FATAL: 1>
    LOG_INFO: typing.ClassVar[LogLevel]  # value = <LogLevel.LOG_INFO: 4>
    LOG_OFF: typing.ClassVar[LogLevel]  # value = <LogLevel.LOG_OFF: 0>
    LOG_WARN: typing.ClassVar[LogLevel]  # value = <LogLevel.LOG_WARN: 3>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class LogTarget(enum.IntEnum):
    """An enumeration representing the LogTarget

    New in PyTango 7.0.0
    """

    LOG_CONSOLE: typing.ClassVar[LogTarget]  # value = <LogTarget.LOG_CONSOLE: 0>
    LOG_DEVICE: typing.ClassVar[LogTarget]  # value = <LogTarget.LOG_DEVICE: 2>
    LOG_FILE: typing.ClassVar[LogTarget]  # value = <LogTarget.LOG_FILE: 1>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class Logger:
    def __debug(self, arg0: str, arg1: typing.SupportsInt, arg2: str) -> None: ...
    def __error(self, arg0: str, arg1: typing.SupportsInt, arg2: str) -> None: ...
    def __fatal(self, arg0: str, arg1: typing.SupportsInt, arg2: str) -> None: ...
    def __info(self, arg0: str, arg1: typing.SupportsInt, arg2: str) -> None: ...
    def __init__(self, name: str, level: typing.SupportsInt = ...) -> None: ...
    def __log(
        self, arg0: str, arg1: typing.SupportsInt, arg2: typing.SupportsInt, arg3: str
    ) -> None: ...
    def __log_unconditionally(
        self, arg0: str, arg1: typing.SupportsInt, arg2: typing.SupportsInt, arg3: str
    ) -> None: ...
    def __warn(self, arg0: str, arg1: typing.SupportsInt, arg2: str) -> None: ...
    def debug(self, msg, *args):
        """debug(self, msg, *args)

        Sends the given message to the tango debug stream.

        :param msg: the message to be sent to the debug stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def error(self, msg, *args):
        """error(self, msg, *args)

        Sends the given message to the tango error stream.

        :param msg: the message to be sent to the error stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def fatal(self, msg, *args):
        """fatal(self, msg, *args)

        Sends the given message to the tango fatal stream.

        :param msg: the message to be sent to the fatal stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def get_level(self) -> int: ...
    def get_name(self) -> str: ...
    def info(self, msg, *args):
        """info(self, msg, *args)

        Sends the given message to the tango info stream.

        :param msg: the message to be sent to the info stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def is_debug_enabled(self) -> bool: ...
    def is_error_enabled(self) -> bool: ...
    def is_fatal_enabled(self) -> bool: ...
    def is_info_enabled(self) -> bool: ...
    def is_level_enabled(self, arg0: typing.SupportsInt) -> bool: ...
    def is_warn_enabled(self) -> bool: ...
    def log(self, level, msg, *args):
        """log(self, level, msg, *args)

        Sends the given message to the tango the selected stream.

        :param level: Log level
        :type level: Level.LevelLevel
        :param msg: the message to be sent to the stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def log_unconditionally(self, level, msg, *args):
        """log_unconditionally(self, level, msg, *args)

        Sends the given message to the tango the selected stream,
        without checking the level.

        :param level: Log level
        :type level: Level.LevelLevel
        :param msg: the message to be sent to the stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def set_level(self, arg0: typing.SupportsInt) -> None: ...
    def warn(self, msg, *args):
        """warn(self, msg, *args)

        Sends the given message to the tango warn stream.

        :param msg: the message to be sent to the warn stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """
    def warning(self, msg, *args):
        """warn(self, msg, *args)

        Sends the given message to the tango warn stream.

        :param msg: the message to be sent to the warn stream
        :type msg: str
        :param args: list of optional message arguments
        :type args: Sequence[str]
        """

class Logging:
    @staticmethod
    def add_logging_target(arg0: typing.Any) -> None: ...
    @staticmethod
    def get_core_logger() -> Logger: ...
    @staticmethod
    def remove_logging_target(arg0: typing.Any) -> None: ...
    @staticmethod
    def start_logging() -> None: ...
    @staticmethod
    def stop_logging() -> None: ...

class MessBoxType(enum.IntEnum):
    """An enumeration representing the MessBoxType

    New in PyTango 7.0.0
    """

    INFO: typing.ClassVar[MessBoxType]  # value = <MessBoxType.INFO: 1>
    STOP: typing.ClassVar[MessBoxType]  # value = <MessBoxType.STOP: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class MultiAttribute:
    """ """
    @typing.overload
    def check_alarm(self) -> bool:
        """check_alarm(self) -> bool

            Checks an alarm on all attribute(s) with an alarm defined.

        :returns: True if at least one attribute is in alarm condition
        :rtype: bool

        :raises DevFailed: If at least one attribute does not have any alarm level defined

        New in PyTango 7.0.0
        """
    @typing.overload
    def check_alarm(self, ind: typing.SupportsInt) -> bool:
        """check_alarm(self, ind) -> bool

            Checks an alarm for one attribute from its index in the main attributes vector.

        :param ind: the attribute index
        :type ind: int

        :returns: True if attribute is in alarm condition
        :rtype: bool

        :raises DevFailed: If at least one attribute does not have any alarm level defined

        New in PyTango 7.0.0
        """
    @typing.overload
    def check_alarm(self, attr_name: str) -> bool:
        """check_alarm(self, attr_name) -> bool

            Checks an alarm for one attribute with a given name.
            - The 3rd version of the method checks alarm for one attribute from its index in the main attributes vector.

        :param attr_name: attribute name
        :type attr_name: str

        :returns: True if attribute is in alarm condition
        :rtype: bool

        :raises DevFailed: If at least one attribute does not have any alarm level defined

        New in PyTango 7.0.0
        """
    def get_alarm_list(self) -> StdLongVector:
        """get_alarm_list(self) -> list[int]

            Get list of attribute with an alarm level defined

        :returns: A vector of int data. Each object is the index in the main attribute vector of attribute with alarm level defined
        :rtype: list[int]
        """
    def get_attr_by_ind(self, ind: typing.SupportsInt) -> Attribute:
        """get_attr_by_ind(self, ind) -> Attribute

            Get :class:`~tango.Attribute` object from its index.

            This method returns an :class:`~tango.Attribute` object from the
            index in the main attribute vector.

        :param ind: the attribute index
        :type ind: int

        :returns: the attribute object
        :rtype: Attribute
        """
    def get_attr_by_name(self, attr_name: str) -> Attribute:
        """get_attr_by_name(self, attr_name) -> Attribute

            Get :class:`~tango.Attribute` object from its name.

            This method returns an :class:`~tango.Attribute` object with a
            name passed as parameter. The equality on attribute name is case
            independent.

        :param attr_name: attribute name
        :type attr_name: str

        :returns: the attribute object
        :rtype: Attribute

        :raises DevFailed: If the attribute is not defined.
        """
    def get_attr_ind_by_name(self, attr_name: str) -> int:
        """get_attr_ind_by_name(self, attr_name) -> int

            Get Attribute index into the main attribute vector from its name.

            This method returns the index in the Attribute vector (stored in the
            :class:`~tango.MultiAttribute` object) of an attribute with a
            given name. The name equality is case independent.

        :param attr_name: attribute name
        :type attr_name: str

        :returns: the attribute index
        :rtype: int

        :raises DevFailed: If the attribute is not found in the vector.

        New in PyTango 7.0.0
        """
    def get_attr_nb(self) -> int:
        """get_attr_nb(self) -> int

            Get the number of attributes.

        :returns: the number of attributes
        :rtype: int

        New in PyTango 7.0.0
        """
    def get_attribute_list(self) -> tuple[Attribute]:
        """get_attribute_list(self) -> tuple[Attribute]

            Get the tuple of :class:`~tango.Attribute` objects.

        :returns: attribute objects tuple.
        :rtype: tuple[Attribute]

        .. versionchanged:: 10.1.0
           The return type was changed from ``AttributeList`` (now removed) to ``tuple[Attribute]``.

        New in PyTango 7.2.1
        """
    def get_w_attr_by_ind(self, ind: typing.SupportsInt) -> WAttribute:
        """get_w_attr_by_ind(self, ind) -> WAttribute

            Get a writable attribute object from its index.

            This method returns an :class:`~tango.WAttribute` object from the
            index in the main attribute vector.

        :param ind: the attribute index
        :type ind: int

        :returns: the attribute object
        :rtype: WAttribute
        """
    def get_w_attr_by_name(self, attr_name: str) -> WAttribute:
        """get_w_attr_by_name(self, attr_name) -> WAttribute

            Get a writable attribute object from its name.

            This method returns an :class:`~tango.WAttribute` object with a
            name passed as parameter. The equality on attribute name is case
            independent.

        :param attr_name: attribute name
        :type attr_name: str

        :returns: the attribute object
        :rtype: WAttribute

        :raises DevFailed: If the attribute is not defined.
        """
    def read_alarm(self, status: str) -> None:
        """read_alarm(self, status)

            Add alarm message to device status.

            This method add alarm message to the string passed as parameter.
            A message is added for each attribute which is in alarm condition

        :param status: a string (should be the device status)
        :type status: str

        New in PyTango 7.0.0
        """

class MultiClassAttribute:
    """There is one instance of this class for each device class.

    This class is mainly an aggregate of :class:`~tango.Attr` objects.
    It eases management of multiple attributes

    New in PyTango 7.2.1
    """
    def get_attr(self, attr_name: str) -> Attr:
        """get_attr(self, attr_name) -> Attr

            Get the :class:`~tango.Attr` object for the attribute with
            name passed as parameter.

        :param attr_name: attribute name
        :type attr_name: str

        :returns: the attribute object
        :rtype: Attr

        :raises DevFailed: If the attribute is not defined.

        New in PyTango 7.2.1
        """
    def get_attr_list(self) -> tuple[Attr]:
        """get_attr_list(self) -> tuple[Attr]

            Get the tuple of :class:`~tango.Attr` for this device class.

        :returns: attr objects tuple
        :rtype: tuple[Attr]

        .. versionchanged:: 10.1.0
           The return type was changed from ``AttrList`` (now removed) to ``tuple[Attr]``.

        New in PyTango 7.2.1
        """
    def remove_attr(self, attr_name: str, cl_name: str) -> None:
        """remove_attr(self, attr_name, cl_name)

            Remove the :class:`~tango.Attr` object for the attribute with
            name passed as parameter.

            Does nothing if the attribute does not exist.

        :param attr_name: attribute name
        :type attr_name: str
        :param cl_name: the attribute class name
        :type cl_name: str

        New in PyTango 7.2.1
        """

class NamedDevFailed:
    @property
    def err_stack(self) -> list[DevError]: ...
    @property
    def idx_in_call(self) -> int: ...
    @property
    def name(self) -> str: ...

class NamedDevFailedList:
    def call_failed(self) -> bool: ...
    def get_faulty_attr_nb(self) -> int: ...
    @property
    def err_list(self) -> ...: ...

class NonDbDevice(DevFailed): ...
class NonSupportedFeature(DevFailed): ...
class NotAllowed(DevFailed): ...

class PeriodicEventInfo:
    """A structure containing available periodic event information for an attribute
    with the following members:

        - period : (str) event period
        - extensions : (StdStringVector) extensions (currently not used)
    """

    extensions: StdStringVector
    period: str
    def __getstate__(self) -> tuple: ...
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __setstate__(self, arg0: tuple) -> None: ...
    def __str__(self):
        """str method for struct"""

class PeriodicEventProp:
    extensions: list[str]
    period: str
    def __init__(self) -> None: ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """str method for struct"""

class PollCmdCode(enum.IntEnum):
    """An enumeration representing the PollCmdCode

    New in PyTango 7.0.0
    """

    POLL_ADD_HEARTBEAT: typing.ClassVar[
        PollCmdCode
    ]  # value = <PollCmdCode.POLL_ADD_HEARTBEAT: 8>
    POLL_ADD_OBJ: typing.ClassVar[PollCmdCode]  # value = <PollCmdCode.POLL_ADD_OBJ: 0>
    POLL_EXIT: typing.ClassVar[PollCmdCode]  # value = <PollCmdCode.POLL_EXIT: 6>
    POLL_REM_DEV: typing.ClassVar[PollCmdCode]  # value = <PollCmdCode.POLL_REM_DEV: 5>
    POLL_REM_EXT_TRIG_OBJ: typing.ClassVar[
        PollCmdCode
    ]  # value = <PollCmdCode.POLL_REM_EXT_TRIG_OBJ: 7>
    POLL_REM_HEARTBEAT: typing.ClassVar[
        PollCmdCode
    ]  # value = <PollCmdCode.POLL_REM_HEARTBEAT: 9>
    POLL_REM_OBJ: typing.ClassVar[PollCmdCode]  # value = <PollCmdCode.POLL_REM_OBJ: 1>
    POLL_START: typing.ClassVar[PollCmdCode]  # value = <PollCmdCode.POLL_START: 2>
    POLL_STOP: typing.ClassVar[PollCmdCode]  # value = <PollCmdCode.POLL_STOP: 3>
    POLL_UPD_PERIOD: typing.ClassVar[
        PollCmdCode
    ]  # value = <PollCmdCode.POLL_UPD_PERIOD: 4>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class PollDevice:
    """A structure containing PollDevice information with the following members:

    - dev_name : (str) device name
    - ind_list : (sequence<int>) index list

    New in PyTango 7.0.0
    """

    dev_name: str
    ind_list: StdLongVector

class PollObjType(enum.IntEnum):
    """An enumeration representing the PollObjType

    New in PyTango 7.0.0
    """

    EVENT_HEARTBEAT: typing.ClassVar[
        PollObjType
    ]  # value = <PollObjType.EVENT_HEARTBEAT: 2>
    POLL_ATTR: typing.ClassVar[PollObjType]  # value = <PollObjType.POLL_ATTR: 1>
    POLL_CMD: typing.ClassVar[PollObjType]  # value = <PollObjType.POLL_CMD: 0>
    STORE_SUBDEV: typing.ClassVar[PollObjType]  # value = <PollObjType.STORE_SUBDEV: 3>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class SerialModel(enum.IntEnum):
    """An enumeration representing the type of serialization performed by the device server"""

    BY_CLASS: typing.ClassVar[SerialModel]  # value = <SerialModel.BY_CLASS: 1>
    BY_DEVICE: typing.ClassVar[SerialModel]  # value = <SerialModel.BY_DEVICE: 0>
    BY_PROCESS: typing.ClassVar[SerialModel]  # value = <SerialModel.BY_PROCESS: 2>
    NO_SYNC: typing.ClassVar[SerialModel]  # value = <SerialModel.NO_SYNC: 3>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class SpectrumAttr(Attr):
    def __init__(
        self,
        arg0: str,
        arg1: typing.SupportsInt,
        arg2: AttrWriteType,
        arg3: typing.SupportsInt,
    ) -> None: ...

class StdDoubleVector:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: typing.SupportsFloat) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: StdDoubleVector) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> StdDoubleVector:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> float: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: StdDoubleVector) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[float]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: StdDoubleVector) -> bool: ...
    def __repr__(self) -> str:
        """Return the canonical string representation of this list."""
    @typing.overload
    def __setitem__(
        self, arg0: typing.SupportsInt, arg1: typing.SupportsFloat
    ) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StdDoubleVector) -> None:
        """Assign list elements using a slice object"""
    def append(self, x: typing.SupportsFloat) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: typing.SupportsFloat) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: StdDoubleVector) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: typing.SupportsFloat) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> float:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> float:
        """Remove and return the item at index ``i``"""
    def remove(self, x: typing.SupportsFloat) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class StdLongVector:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: typing.SupportsInt) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: StdLongVector) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> StdLongVector:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> int: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: StdLongVector) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[int]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: StdLongVector) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(
        self, arg0: typing.SupportsInt, arg1: typing.SupportsInt
    ) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StdLongVector) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: typing.SupportsInt) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: typing.SupportsInt) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: StdLongVector) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: typing.SupportsInt) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> int:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> int:
        """Remove and return the item at index ``i``"""
    def remove(self, x: typing.SupportsInt) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class StdNamedDevFailedVector:
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    @typing.overload
    def __getitem__(self, s: slice) -> StdNamedDevFailedVector:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> NamedDevFailed: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: StdNamedDevFailedVector) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[NamedDevFailed]: ...
    def __len__(self) -> int: ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: NamedDevFailed) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StdNamedDevFailedVector) -> None:
        """Assign list elements using a slice object"""
    def append(self, x: NamedDevFailed) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    @typing.overload
    def extend(self, L: StdNamedDevFailedVector) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: NamedDevFailed) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> NamedDevFailed:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> NamedDevFailed:
        """Remove and return the item at index ``i``"""

class StdStringVector:
    __hash__: typing.ClassVar[None] = None
    def __add__(self, seq): ...
    def __bool__(self) -> bool:
        """Check whether the list is nonempty"""
    def __contains__(self, x: str) -> bool:
        """Return true the container contains ``x``"""
    @typing.overload
    def __delitem__(self, arg0: typing.SupportsInt) -> None:
        """Delete the list elements at index ``i``"""
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """Delete list elements using a slice object"""
    def __eq__(self, arg0: StdStringVector) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> StdStringVector:
        """Retrieve list elements using a slice object"""
    @typing.overload
    def __getitem__(self, arg0: typing.SupportsInt) -> str: ...
    def __imul__(self, n): ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: StdStringVector) -> None:
        """Copy constructor"""
    @typing.overload
    def __init__(self, arg0: collections.abc.Iterable) -> None: ...
    def __iter__(self) -> collections.abc.Iterator[str]: ...
    def __len__(self) -> int: ...
    def __mul__(self, n): ...
    def __ne__(self, arg0: StdStringVector) -> bool: ...
    def __repr__(self): ...
    @typing.overload
    def __setitem__(self, arg0: typing.SupportsInt, arg1: str) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: StdStringVector) -> None:
        """Assign list elements using a slice object"""
    def __str__(self): ...
    def append(self, x: str) -> None:
        """Add an item to the end of the list"""
    def clear(self) -> None:
        """Clear the contents"""
    def count(self, x: str) -> int:
        """Return the number of times ``x`` appears in the list"""
    @typing.overload
    def extend(self, L: StdStringVector) -> None:
        """Extend the list by appending all the items in the given list"""
    @typing.overload
    def extend(self, L: collections.abc.Iterable) -> None:
        """Extend the list by appending all the items in the given list"""
    def insert(self, i: typing.SupportsInt, x: str) -> None:
        """Insert an item at a given position."""
    @typing.overload
    def pop(self) -> str:
        """Remove and return the last item"""
    @typing.overload
    def pop(self, i: typing.SupportsInt) -> str:
        """Remove and return the item at index ``i``"""
    def remove(self, x: str) -> None:
        """Remove the first item from the list whose value is x. It is an error if there is no such item."""

class SubDevDiag:
    def get_associated_device(self) -> str:
        """Get the device name that is associated with the current thread of the device server"""
    def get_sub_devices(self) -> list[str]:
        """Read the list of sub devices for the device server
        The returned strings are formated as:

        'device_name sub_device_name'

         or

         sub_device_name

         when no associated device could be identified
        """
    def get_sub_devices_from_cache(self) -> None:
        """Read the list of sub devices from the database cache.
        The cache is filled at server sart-up
        """
    def register_sub_device(self, dev_name: str, sub_dev_name: str) -> None:
        """Register a sub device for an associated device in the list of sub devices of the device server"""
    @typing.overload
    def remove_sub_devices(self) -> None:
        """Remove all sub devices"""
    @typing.overload
    def remove_sub_devices(self, dev_name: str) -> None:
        """Remove all sub devices for a device of the server"""
    def set_associated_device(self, dev_name: str) -> None:
        """Set the device name that should be associated to a thread in the device server"""
    def store_sub_devices(self) -> None:
        """Store the list of sub devices for the devices of the server.
        The sub device names are stored as a string array
        under the device property "sub_devices".
        Sub device names without an associated device,
        will be stored under the name of the administration device.

        Database access will only happen when the list of
        sub devices was modified and when the list is different
        from the list read into the db_cache during the server
        startup
        """

class TimeVal:
    """Time value structure with the following members:

    - tv_sec : seconds
    - tv_usec : microseconds
    - tv_nsec : nanoseconds
    """
    @staticmethod
    def __init_original(*args, **kwargs):
        """__init__(self: tango._tango.TimeVal) -> None"""
    @staticmethod
    def fromdatetime(dt):
        """fromdatetime(dt) -> TimeVal

            A static method returning a :class:`tango.TimeVal` object representing
            the given :class:`datetime.datetime`

            Parameters :
                - dt : (datetime.datetime) a datetime object
            Return     : (TimeVal) representing the given timestamp

        .. versionadded:: 7.1.0

        .. versionadded:: 7.1.2
            Documented
        """
    @staticmethod
    def fromtimestamp(ts):
        """fromtimestamp(ts) -> TimeVal

            A static method returning a :class:`tango.TimeVal` object representing
            the given timestamp

            Parameters :
                - ts : (float) a timestamp
            Return     : (TimeVal) representing the given timestamp

        .. versionadded:: 7.1.0
        """
    @staticmethod
    def now():
        """now() -> TimeVal

            A static method returning a :class:`tango.TimeVal` object representing
            the current time

            Parameters : None
            Return     : (TimeVal) representing the current time

        .. versionadded:: 7.1.0

        .. versionadded:: 7.1.2
            Documented
        """
    def __init__(self, a=None, b=None, c=None): ...
    def __repr__(self):
        """repr method for struct"""
    def __str__(self):
        """__str__(self) -> str

            Returns a string representation of TimeVal

            Parameters : None
            Return     : (str) a string representing the time (same as :class:`datetime.datetime`)

        .. versionadded:: 7.1.0

        .. versionadded:: 7.1.2
            Documented
        """
    def isoformat(self, sep="T"):
        """isoformat(self, sep='T') -> str

            Returns a string in ISO 8601 format, YYYY-MM-DDTHH:MM:SS[.mmmmmm][+HH:MM]

            Parameters :
                sep : (str) sep is used to separate the year from the time, and defaults to 'T'
            Return     : (str) a string representing the time according to a format specification.

        .. versionadded:: 7.1.0

        .. versionadded:: 7.1.2
            Documented

        .. versionchanged:: 7.1.2
            The `sep` parameter is not mandatory anymore and defaults to 'T' (same as :meth:`datetime.datetime.isoformat`)
        """
    def strftime(self, format):
        """strftime(self, format) -> str

            Convert a time value to a string according to a format specification.

            Parameters :
                format : (str) See the python library reference manual for formatting codes
            Return     : (str) a string representing the time according to a format specification.

        .. versionadded:: 7.1.0

        .. versionadded:: 7.1.2
            Documented
        """
    def todatetime(self):
        """todatetime(self) -> datetime.datetime

            Returns a :class:`datetime.datetime` object representing
            the same time value

            Parameters : None
            Return     : (datetime.datetime) the time value in datetime format

        .. versionadded:: 7.1.0
        """
    def totime(self):
        """totime(self) -> float

            Returns a float representing this time value

            Parameters : None
            Return     : a float representing the time value

        .. versionadded:: 7.1.0
        """
    @property
    def tv_nsec(self) -> int: ...
    @tv_nsec.setter
    def tv_nsec(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def tv_sec(self) -> int: ...
    @tv_sec.setter
    def tv_sec(self, arg0: typing.SupportsInt) -> None: ...
    @property
    def tv_usec(self) -> int: ...
    @tv_usec.setter
    def tv_usec(self, arg0: typing.SupportsInt) -> None: ...

class UserDefaultAttrProp:
    """User class to set attribute default properties.

    This class is used to set attribute default properties.
    Three levels of attributes properties setting are implemented within Tango.
    The highest property setting level is the database.
    Then the user default (set using this UserDefaultAttrProp class) and finally
    a Tango library default value.
    """

    abs_change: str
    archive_abs_change: str
    archive_period: str
    archive_rel_change: str
    delta_t: str
    delta_val: str
    description: str
    display_unit: str
    enum_labels: str
    format: str
    label: str
    max_alarm: str
    max_value: str
    max_warning: str
    min_alarm: str
    min_value: str
    min_warning: str
    period: str
    rel_change: str
    standard_unit: str
    unit: str
    @staticmethod
    def set_label(*args, **kwargs) -> None:
        """set_label(self, def_label)

            Set default label property.

        :param def_label: the user default label property
        :type def_label: str
        """
    def __init__(self) -> None: ...
    def _set_enum_labels(self, arg0: StdStringVector) -> None: ...
    def set_abs_change(self, arg0: str) -> None:
        """set_abs_change(self, def_abs_change) <= DEPRECATED

        Set default change event abs_change property.

        :param def_abs_change: the user default change event abs_change property
        :type def_abs_change: str

        Deprecated since PyTango 8.0. Please use set_event_abs_change instead.
        """
    def set_archive_abs_change(self, arg0: str) -> None:
        """set_archive_abs_change(self, def_archive_abs_change) <= DEPRECATED

        Set default archive event abs_change property.

        :param def_archive_abs_change: the user default archive event abs_change property
        :type def_archive_abs_change: str

        Deprecated since PyTango 8.0. Please use set_archive_event_abs_change instead.
        """
    def set_archive_event_abs_change(self, arg0: str) -> None:
        """set_archive_event_abs_change(self, def_archive_abs_change)

        Set default archive event abs_change property.

        :param def_archive_abs_change: the user default archive event abs_change property
        :type def_archive_abs_change: str

        New in PyTango 8.0
        """
    def set_archive_event_period(self, arg0: str) -> None:
        """set_archive_event_period(self, def_archive_period)

        Set default archive event period property.

        :param def_archive_period: t
        :type def_archive_period: str

        New in PyTango 8.0
        """
    def set_archive_event_rel_change(self, arg0: str) -> None:
        """set_archive_event_rel_change(self, def_archive_rel_change)

        Set default archive event rel_change property.

        :param def_archive_rel_change: the user default archive event rel_change property
        :type def_archive_rel_change: str

        New in PyTango 8.0
        """
    def set_archive_period(self, arg0: str) -> None:
        """set_archive_period(self, def_archive_period) <= DEPRECATED

        Set default archive event period property.

        :param def_archive_period: t
        :type def_archive_period: str

        Deprecated since PyTango 8.0. Please use set_archive_event_period instead.
        """
    def set_archive_rel_change(self, arg0: str) -> None:
        """set_archive_rel_change(self, def_archive_rel_change) <= DEPRECATED

        Set default archive event rel_change property.

        :param def_archive_rel_change: the user default archive event rel_change property
        :type def_archive_rel_change: str

        Deprecated since PyTango 8.0. Please use set_archive_event_rel_change instead.
        """
    def set_delta_t(self, arg0: str) -> None:
        """set_delta_t(self, def_delta_t)

        Set default RDS alarm delta_t property.

        :param def_delta_t: the user default RDS alarm delta_t property
        :type def_delta_t: str
        """
    def set_delta_val(self, arg0: str) -> None:
        """set_delta_val(self, def_delta_val)

        Set default RDS alarm delta_val property.

        :param def_delta_val: the user default RDS alarm delta_val property
        :type def_delta_val: str
        """
    def set_description(self, def_description: str) -> None:
        """set_description(self, def_description: str)

            Set default description property.

        :param def_description: the user default description property
        :type def_description: str
        """
    def set_display_unit(self, arg0: str) -> None:
        """set_display_unit(self, def_display_unit)

        Set default display unit property.

        :param def_display_unit: the user default display unit property
        :type def_display_unit: str
        """
    def set_enum_labels(self, enum_labels):
        """set_enum_labels(self, enum_labels)

        Set default enumeration labels.

        :param enum_labels: list of enumeration labels
        :type enum_labels: Sequence[str]

        New in PyTango 9.2.0
        """
    def set_event_abs_change(self, arg0: str) -> None:
        """set_event_abs_change(self, def_abs_change)

        Set default change event abs_change property.

        :param def_abs_change: the user default change event abs_change property
        :type def_abs_change: str

        New in PyTango 8.0
        """
    def set_event_period(self, arg0: str) -> None:
        """set_event_period(self, def_period)

        Set default periodic event period property.

        :param def_period: the user default periodic event period property
        :type def_period: str

        New in PyTango 8.0
        """
    def set_event_rel_change(self, arg0: str) -> None:
        """set_event_rel_change(self, def_rel_change)

        Set default change event rel_change property.

        :param def_rel_change: the user default change event rel_change property
        :type def_rel_change: str

        New in PyTango 8.0
        """
    def set_format(self, arg0: str) -> None:
        """set_format(self, def_format)

        Set default format property.

        :param def_format: the user default format property
        :type def_format: str
        """
    def set_max_alarm(self, arg0: str) -> None:
        """set_max_alarm(self, def_max_alarm)

        Set default max_alarm property.

        :param def_max_alarm: the user default max_alarm property
        :type def_max_alarm: str
        """
    def set_max_value(self, arg0: str) -> None:
        """set_max_value(self, def_max_value)

        Set default max_value property.

        :param def_max_value: the user default max_value property
        :type def_max_value: str
        """
    def set_max_warning(self, arg0: str) -> None:
        """set_max_warning(self, def_max_warning)

        Set default max_warning property.

        :param def_max_warning: the user default max_warning property
        :type def_max_warning: str
        """
    def set_min_alarm(self, arg0: str) -> None:
        """set_min_alarm(self, def_min_alarm)

        Set default min_alarm property.

        :param def_min_alarm: the user default min_alarm property
        :type def_min_alarm: str
        """
    def set_min_value(self, arg0: str) -> None:
        """set_min_value(self, def_min_value)

        Set default min_value property.

        :param def_min_value: the user default min_value property
        :type def_min_value: str
        """
    def set_min_warning(self, arg0: str) -> None:
        """set_min_warning(self, def_min_warning)

        Set default min_warning property.

        :param def_min_warning: the user default min_warning property
        :type def_min_warning: str
        """
    def set_period(self, arg0: str) -> None:
        """set_period(self, def_period) <= DEPRECATED

        Set default periodic event period property.

        :param def_period: the user default periodic event period property
        :type def_period: str

        Deprecated since PyTango 8.0. Please use set_event_period instead.
        """
    def set_rel_change(self, arg0: str) -> None:
        """set_rel_change(self, def_rel_change) <= DEPRECATED

        Set default change event rel_change property.

        :param def_rel_change: the user default change event rel_change property
        :type def_rel_change: str

        Deprecated since PyTango 8.0. Please use set_event_rel_change instead.
        """
    def set_standard_unit(self, arg0: str) -> None:
        """set_standard_unit(self, def_standard_unit)

        Set default standard unit property.

        :param def_standard_unit: the user default standard unit property
        :type def_standard_unit: str
        """
    def set_unit(self, arg0: str) -> None:
        """set_unit(self, def_unit)

        Set default unit property.

        :param def_unit: te user default unit property
        :type def_unit: str
        """

class UserDefaultFwdAttrProp:
    def __init__(self) -> None: ...
    def set_label(self, def_label: str) -> None:
        """set_label(self, def_label: str) -> None

            Set default label property

        :param def_label: The user default label property
        :type def_label: str
        """

class Util:
    """This class is a used to store TANGO device server process data and to
    provide the user with a set of utilities method.

    This class is implemented using the singleton design pattern.
    Therefore a device server process can have only one instance of this
    class and its constructor is not public. Example::

        util = tango.Util.instance()
            print(util.get_host_name())
    """

    _FileDb: typing.ClassVar[bool] = False
    _UseDb: typing.ClassVar[bool] = True
    @staticmethod
    def __init_orig(*args, **kwargs):
        """init(arg0: object) -> tango._tango.Util


        init(*args) -> Util

           Static method that creates and gets the singleton object reference.
           This method returns a reference to the object of the Util class.
           If the class singleton object has not been created, it will be instantiated

           :param str \\\\*args: the process commandline arguments

           :return: :class:`Util` the tango Util object
           :rtype: :class:`Util`
        """
    @staticmethod
    def __init_orig__(*args, **kwargs):
        """__init__(self: tango._tango.Util, arg0: object) -> None"""
    @staticmethod
    def init(args): ...
    @staticmethod
    @typing.overload
    def instance() -> Util:
        """instance() -> Util

            Static method that gets the singleton object reference.
            If the class has not been initialised with it's init method,
            this method prints a message and aborts the device server process.

        :returns: the tango :class:`Util` object
        :rtype: :class:`Util`

        :raises: :class:`DevFailed` instead of aborting if exit is set to False
        """
    @staticmethod
    @typing.overload
    def instance(exit: bool) -> Util:
        """instance(exit = True) -> Util

            Static method that gets the singleton object reference.
            If the class has not been initialised with it's init method,
            this method prints a message and aborts the device server process.

        :param exit: exit or throw DevFailed
        :type exit: bool

        :returns: the tango :class:`Util` object
        :rtype: :class:`Util`

        :raises: :class:`DevFailed` instead of aborting if exit is set to False
        """
    @staticmethod
    def set_use_db(arg0: bool) -> None:
        """set_use_db(self) -> None

        Set the database use Tango::Util::_UseDb flag.
        Implemented for device server started without database usage.

        Use with extreme care!
        """
    def __init__(self, args): ...
    def _fill_attr_polling_buffer(
        self, dev: DeviceImpl, att_name: str, data: collections.abc.Sequence
    ) -> None: ...
    def _fill_cmd_polling_buffer(
        self, dev: DeviceImpl, cmd_name: str, data: collections.abc.Sequence
    ) -> None: ...
    def add_Cpp_TgClass(self, device_class_name, tango_device_class_name):
        """Register a new C++ tango class.

        If there is a shared library file called MotorClass.so which
        contains a MotorClass class and a _create_MotorClass_class method. Example::

            util.add_Cpp_TgClass('MotorClass', 'Motor')

        .. note:: the parameter 'device_class_name' must match the shared
                  library name.

        .. deprecated:: 7.1.2
            Use :meth:`tango.Util.add_class` instead.
        """
    def add_TgClass(self, klass_device_class, klass_device, device_class_name=None):
        """Register a new python tango class. Example::

            util.add_TgClass(MotorClass, Motor)
            util.add_TgClass(MotorClass, Motor, 'Motor') # equivalent to previous line

        .. deprecated:: 7.1.2
            Use :meth:`tango.Util.add_class` instead.
        """
    def add_class(self, *args, **kwargs):
        """add_class(self, class<DeviceClass>, class<DeviceImpl>, language="python") -> None

            Register a new tango class ('python' or 'c++').

            If language is 'python' then args must be the same as
            :meth:`tango.Util.add_TgClass`. Otherwise, args should be the ones
            in :meth:`tango.Util.add_Cpp_TgClass`. Example::

                util.add_class(MotorClass, Motor)
                util.add_class('CounterClass', 'Counter', language='c++')

        New in PyTango 7.1.2
        """
    def connect_db(self) -> None:
        """connect_db(self) -> None

            Connect the process to the TANGO database.
            If the connection to the database failed, a message is
            displayed on the screen and the process is aborted

        Parameters : None
        Return     : None
        """
    def create_device(self, klass_name, device_name, alias=None, cb=None):
        """create_device(self, klass_name, device_name, alias=None, cb=None) -> None

            Creates a new device of the given class in the database, creates a new
            DeviceImpl for it and calls init_device (just like it is done for
            existing devices when the DS starts up)

            An optional parameter callback is called AFTER the device is
            registered in the database and BEFORE the init_device for the
            newly created device is called

            Throws tango.DevFailed:
                - the device name exists already or
                - the given class is not registered for this DS.
                - the cb is not a callable

        New in PyTango 7.1.2

        Parameters :
            - klass_name : (str) the device class name
            - device_name : (str) the device name
            - alias : (str) optional alias. Default value is None meaning do not create device alias
            - cb : (callable) a callback that is called AFTER the device is registered
                   in the database and BEFORE the init_device for the newly created
                   device is called. Typically you may want to put device and/or attribute
                   properties in the database here. The callback must receive a parameter
                   device_name (str). Default value is None meaning no callback

        Return     : None
        """
    def delete_device(self, klass_name, device_name):
        """delete_device(self, klass_name, device_name) -> None

            Deletes an existing device from the database and from this running
            server

            Throws tango.DevFailed:
                - the device name doesn't exist in the database
                - the device name doesn't exist in this DS.

        New in PyTango 7.1.2

        Parameters :
            - klass_name : (str) the device class name
            - device_name : (str) the device name

        Return     : None
        """
    def fill_attr_polling_buffer(self, device, attribute_name, attr_history_stack):
        """fill_attr_polling_buffer(self, device, attribute_name, attr_history_stack) -> None

            Fill attribute polling buffer with your own data. E.g.:

            .. code-block:: python

                def fill_history():
                    util = Util.instance(False)
                    # note is such case quality will ATTR_VALID, and time_stamp will be time.time()
                    util.fill_attr_polling_buffer(device, attribute_name, TimedAttrData(my_new_value))

            or:

            .. code-block:: python

                def fill_history():
                    util = Util.instance(False)

                    data = TimedAttrData(value=my_new_value,
                                         quality=AttrQuality.ATTR_WARNING,
                                         w_value=my_new_w_value,
                                         time_stamp=my_time)

                    util.fill_attr_polling_buffer(device, attribute_name, data)

            or:

            .. code-block:: python

                def fill_history():
                    util = Util.instance(False)
                    data = [TimedAttrData(my_new_value),
                            TimedAttrData(error=RuntimeError("Cannot read value")]

                    util.fill_attr_polling_buffer(device, attribute_name, data)

        :param device: the device to fill attribute polling buffer
        :type device: :obj:`tango.DeviceImpl`

        :param attribute_name: name of the attribute to fill polling buffer
        :type attribute_name: :obj:`str`

        :param attr_history_stack: data to be inserted.
        :type attr_history_stack: :obj:`tango.TimedAttrData` or list[:obj:`tango.TimedAttrData`]

        :return: None

        :raises: :obj:`tango.DevFailed`

        .. versionadded:: 10.1.0
        """
    def fill_cmd_polling_buffer(self, device, command_name, cmd_history_stack):
        """fill_cmd_polling_buffer(self, device, command_name, attr_history_stack) -> None

            Fill attribute polling buffer with your own data. E.g.:


            .. code-block:: python

                def fill_history():
                    util = Util.instance(False)
                    # note is such time_stamp will be set to time.time()
                    util.fill_cmd_polling_buffer(device, command_name, TimedCmdData(my_new_value))

            or:

            .. code-block:: python

                def fill_history():
                    util = Util.instance(False)

                    data = TimedCmdData(value=my_new_value,
                                         time_stamp=my_time)

                    util.fill_cmd_polling_buffer(device, command_name, data)

            or:

            .. code-block:: python

                def fill_history():
                    util = Util.instance(False)
                    data = [TimedCmdData(my_new_value),
                            TimedCmdData(error=RuntimeError("Cannot read value")]

                    util.fill_cmd_polling_buffer(device, command_name, data)


        :param device: the device to fill command polling buffer
        :type device: :obj:`tango.DeviceImpl`

        :param command_name: name of the command to fill polling buffer
        :type command_name: :obj:`str`

        :param cmd_history_stack: data to be inserted
        :type cmd_history_stack: :obj:`tango.TimedCmdData` or list[:obj:`tango.TimedCmdData`]

        :return: None

        :raises: :obj:`tango.DevFailed`

        .. versionadded:: 10.1.0
        """
    def get_class_list(self):
        """get_class_list(self) -> seq<DeviceClass>

            Returns a list of objects of inheriting from DeviceClass

        Parameters : None

        Return     : (seq<DeviceClass>) a list of objects of inheriting from DeviceClass
        """
    def get_database(self) -> Database:
        """get_database(self) -> Database

            Get a reference to the TANGO database object

        Parameters : None
        Return     : (Database) the database

        New in PyTango 7.0.0
        """
    def get_device_by_name(self, dev_name: str) -> typing.Any:
        """get_device_by_name(self, dev_name) -> DeviceImpl

            Get a device reference from its name

        Parameters :
            - dev_name : (str) The TANGO device name
        Return     : (DeviceImpl) The device reference

        New in PyTango 7.0.0
        """
    def get_device_ior(self, device: DeviceImpl) -> str:
        """get_device_ior(self, device) -> str

        Get the CORBA Interoperable Object Reference (IOR) associated with the device

        :param device: :class:`tango.LatestDeviceImpl` device object
        :type device: :class:`tango.LatestDeviceImpl`

        :return: the associated CORBA object reference
        :rtype: str
        """
    def get_device_list(self, arg0: str) -> list:
        """get_device_list(self) -> sequence<DeviceImpl>

            Get device list from name.
            It is possible to use a wild card ('*') in the name parameter
            (e.g. "*", "/tango/tangotest/n*", ...)

        Parameters : None
        Return     : (sequence<DeviceImpl>) the list of device objects

        New in PyTango 7.0.0
        """
    def get_device_list_by_class(self, class_name: str) -> typing.Any:
        """get_device_list_by_class(self, class_name) -> sequence<DeviceImpl>

            Get the list of device references for a given TANGO class.
            Return the list of references for all devices served by one implementation
            of the TANGO device pattern implemented in the process.

        Parameters :
            - class_name : (str) The TANGO device class name

        Return     : (sequence<DeviceImpl>) The device reference list

        New in PyTango 7.0.0
        """
    def get_ds_exec_name(self) -> str:
        """get_ds_exec_name(self) -> str

            Get a COPY of the device server executable name.

        Parameters : None
        Return     : (str) a COPY of the device server executable name.

        New in PyTango 3.0.4
        """
    def get_ds_inst_name(self) -> str:
        """get_ds_inst_name(self) -> str

            Get a COPY of the device server instance name.

        Parameters : None
        Return     : (str) a COPY of the device server instance name.

        New in PyTango 3.0.4
        """
    def get_ds_name(self) -> str:
        """get_ds_name(self) -> str

            Get the device server name.
            The device server name is the <device server executable name>/<the device server instance name>

        Parameters : None
        Return     : (str) device server name

        New in PyTango 3.0.4
        """
    def get_dserver_device(self) -> DServer:
        """get_dserver_device(self) -> DServer

            Get a reference to the dserver device attached to the device server process.

        Parameters : None
        Return     : (DServer) the dserver device attached to the device server process

        New in PyTango 7.0.0
        """
    def get_dserver_ior(self, device_server: DServer) -> str:
        """get_dserver_ior(self, device_server) -> str

        Get the CORBA Interoperable Object Reference (IOR) associated with the device server

        :param device_server: :class:`DServer` device object
        :type device_server: :class:`DServer`

        :return: the associated CORBA object reference
        :rtype: str
        """
    def get_host_name(self) -> str:
        """get_host_name(self) -> str

            Get the host name where the device server process is running.

        Parameters : None
        Return     : (str) the host name where the device server process is running

        New in PyTango 3.0.4
        """
    def get_pid(self) -> int:
        """get_pid(self) -> TangoSys_Pid

            Get the device server process identifier.

        Parameters : None
        Return     : (int) the device server process identifier
        """
    def get_pid_str(self) -> str:
        """get_pid_str(self) -> str

            Get the device server process identifier as a string.

        Parameters : None
        Return     : (str) the device server process identifier as a string

        New in PyTango 3.0.4
        """
    def get_polling_threads_pool_size(self) -> int:
        """get_polling_threads_pool_size(self) -> int

            Get the polling threads pool size.

        Parameters : None
        Return     : (int) the maximum number of threads in the polling threads pool
        """
    def get_serial_model(self) -> SerialModel:
        """get_serial_model(self) ->SerialModel

            Get the serialization model.

        Parameters : None
        Return     : (SerialModel) the serialization model
        """
    def get_server_version(self) -> str:
        """get_server_version(self) -> str

            Get the device server version.

        Parameters : None
        Return     : (str) the device server version.
        """
    def get_sub_dev_diag(self) -> SubDevDiag:
        """get_sub_dev_diag(self) -> SubDevDiag

            Get the internal sub device manager

        Parameters : None
        Return     : (SubDevDiag) the sub device manager

        New in PyTango 7.0.0
        """
    def get_tango_lib_release(self) -> int:
        """get_tango_lib_release(self) -> int

            Get the TANGO library version number.

        Parameters : None
        Return     : (int) The Tango library release number coded in
                     3 digits (for instance 550,551,552,600,....)
        """
    def get_trace_level(self) -> int:
        """get_trace_level(self) -> int

            Get the process trace level.

        Parameters : None
        Return     : (int) the process trace level.
        """
    def get_version_str(self) -> str:
        """get_version_str(self) -> str

            Get the IDL TANGO version.

        Parameters : None
        Return     : (str) the IDL TANGO version.

        New in PyTango 3.0.4
        """
    def is_auto_alarm_on_change_event(self) -> bool:
        """is_auto_alarm_on_change_event(self) -> bool

        Returns True if alarm events are automatically pushed to subscribers when a device
        pushes a change event, and the attribute quality has changed to or from alarm.

        Can be configured in two ways:

          - via the ``CtrlSystem`` free Tango database property
            ``AutoAlarmOnChangeEvent`` (set to true or false),
          - by calling the :meth:`tango.Util.set_auto_alarm_on_change_event`.

        :return: True if alarm events are automatically pushed to subscribers when a device
            pushes a change event
        :rtype: bool

        .. versionadded:: 10.0.0
        """
    def is_device_restarting(self, dev_name: str) -> bool:
        """is_device_restarting(self, dev_name) -> bool

            Check if the device is actually restarted by the device server
            process admin device with its DevRestart command

        Parameters :
            dev_name : (str) device name
        Return     : (bool) True if the device is restarting.

        New in PyTango 8.0.0
        """
    def is_svr_shutting_down(self) -> bool:
        """is_svr_shutting_down(self) -> bool

            Check if the device server process is in its shutting down sequence

        Parameters : None
        Return     : (bool) True if the server is in its shutting down phase.

        New in PyTango 8.0.0
        """
    def is_svr_starting(self) -> bool:
        """is_svr_starting(self) -> bool

            Check if the device server process is in its starting phase

        Parameters : None
        Return     : (bool) True if the server is in its starting phase

        New in PyTango 8.0.0
        """
    def orb_run(self) -> None:
        """orb_run(self) -> None

            Run the CORBA event loop directly (EXPERT FEATURE!)

            This method runs the CORBA event loop.  It may be useful if the
            Util.server_run method needs to be bypassed.  Normally, that method
            runs the CORBA event loop.

        :return: None
        :rtype: None
        """
    def reset_filedatabase(self) -> None:
        """reset_filedatabase(self) -> None

            Reread the file database.

        Parameters : None
        Return     : None
        """
    def server_cleanup(self) -> None:
        """server_cleanup(self) -> None

        Release device server resources (EXPERT FEATURE!)

        This method cleans up the Tango device server and relinquishes
        all computer resources before the process exits.  It is
        unnecessary to call this, unless Util.server_run has been bypassed.
        """
    def server_init(self, with_window: bool = False) -> None:
        """server_init(self, with_window = False) -> None

            Initialize all the device server pattern(s) embedded in a device server process.

        Parameters :
            - with_window : (bool) default value is False
        Return     : None

        Throws     : DevFailed If the device pattern initialistaion failed
        """
    def server_run(self) -> None:
        """server_run(self) -> None

            Run the CORBA event loop.
            This method runs the CORBA event loop. For UNIX or Linux operating system,
            this method does not return. For Windows in a non-console mode, this method
            start a thread which enter the CORBA event loop.

        Parameters : None
        Return     : None
        """
    def server_set_event_loop(self, event_loop: typing.Any) -> None:
        """server_set_event_loop(self, event_loop) -> None

        This method registers an event loop function in a Tango server.
        This function will be called by the process main thread in an infinite loop
        The process will not use the classical ORB blocking event loop.
        It is the user responsibility to code this function in a way that it implements
        some kind of blocking in order not to load the computer CPU. The following
        piece of code is an example of how you can use this feature::

            _LOOP_NB = 1
            def looping():
                global _LOOP_NB
                print "looping", _LOOP_NB
                time.sleep(0.1)
                _LOOP_NB += 1
                return _LOOP_NB > 100

            def main():
                util = tango.Util(sys.argv)

                # ...

                U = tango.Util.instance()
                U.server_set_event_loop(looping)
                U.server_init()
                U.server_run()

        Parameters : None
        Return     : None

        New in PyTango 8.1.0
        """
    def set_auto_alarm_on_change_event(self, value: bool) -> None:
        """set_auto_alarm_on_change_event(self, enabled) -> None

        Toggles if alarm events are automatically pushed - see
        :meth:`tango.Util.is_auto_alarm_on_change_event`.

        This method takes priority over the value of the free property in the Tango database.

        :param enabled: if True - the alarm event will be emitted with change event, if there is quality change to or from alarm
        :type enabled: bool

        :return: None
        :rtype: None

        .. versionadded:: 10.0.0
        """
    def set_interceptors(self, interceptors: Interceptors) -> None: ...
    def set_polling_threads_pool_size(self, thread_nb: typing.SupportsInt) -> None:
        """set_polling_threads_pool_size(self, thread_nb) -> None

            Set the polling threads pool size.

        Parameters :
            - thread_nb : (int) the maximun number of threads in the polling threads pool
        Return     : None

        New in PyTango 7.0.0
        """
    def set_serial_model(self, ser: SerialModel) -> None:
        """set_serial_model(self, ser) -> None

            Set the serialization model.

        Parameters :
            - ser : (SerialModel) the new serialization model. The serialization model must
                    be one of BY_DEVICE, BY_CLASS, BY_PROCESS or NO_SYNC
        Return     : None
        """
    def set_server_version(self, vers: str) -> None:
        """set_server_version(self, vers) -> None

            Set the device server version.

        Parameters :
            - vers : (str) the device server version
        Return     : None
        """
    def set_trace_level(self, level: typing.SupportsInt) -> None:
        """set_trace_level(self, level) -> None

            Set the process trace level.

        Parameters :
            - level : (int) the new process level
        Return     : None
        """
    def trigger_attr_polling(self, dev: DeviceImpl, name: str) -> None:
        """trigger_attr_polling(self, dev, name) -> None

            Trigger polling for polled attribute.
            This method send the order to the polling thread to poll one object registered
            with an update period defined as "externally triggerred"

        Parameters :
            - dev : (DeviceImpl) the TANGO device
            - name : (str) the attribute name which must be polled
        Return     : None
        """
    def trigger_cmd_polling(self, dev: DeviceImpl, name: str) -> None:
        """trigger_cmd_polling(self, dev, name) -> None

            Trigger polling for polled command.
            This method send the order to the polling thread to poll one object registered
            with an update period defined as "externally triggerred"

        Parameters :
            - dev : (DeviceImpl) the TANGO device
            - name : (str) the command name which must be polled
        Return     : None

        Throws     : DevFailed If the call failed
        """
    def unregister_server(self) -> None:
        """unregister_server(self) -> None

            Unregister a device server process from the TANGO database.
            If the database call fails, a message is displayed on the screen
            and the process is aborted

        Parameters : None
        Return     : None

        New in PyTango 7.0.0
        """

class WAttribute(Attribute):
    """This class represents a Tango writable attribute"""
    def get_max_value(self) -> typing.Any:
        """get_max_value(self) -> obj

            Get attribute maximum value or throws an exception if the
            attribute does not have a maximum value.

        :returns: an object with the python maximum value
        :rtype: obj
        """
    def get_min_value(self) -> typing.Any:
        """get_min_value(self) -> obj

            Get attribute minimum value or throws an exception if the
            attribute does not have a minimum value.

        :returns: an object with the python minimum value
        :rtype: obj
        """
    def get_write_value(self, extract_as: ExtractAs = ...) -> typing.Any:
        """get_write_value(self, extract_as=ExtractAs.Numpy) -> obj

            Retrieve the new value for writable attribute.

        :param extract_as: defaults to ExtractAs.Numpy
        :type extract_as: ExtractAs

        :returns: the attribute write value.
        :rtype: obj
        """
    def get_write_value_length(self) -> int:
        """get_write_value_length(self) -> int

            Retrieve the new value length (data number) for writable attribute.

        :returns: the new value data length
        :rtype: int
        """
    def is_max_value(self) -> bool:
        """is_max_value(self) -> bool

            Check if the attribute has a maximum value.

        :returns: true if the attribute has a maximum value defined
        :rtype: bool
        """
    def is_min_value(self) -> bool:
        """is_min_value(self) -> bool

            Check if the attribute has a minimum value.

        :returns: true if the attribute has a minimum value defined
        :rtype: bool
        """
    def set_max_value(self, value: typing.Any) -> None:
        """set_max_value(self, value)

            Set attribute maximum value.

        :param value: the attribute maximum value. python data type must be compatible
                      with the attribute data format and type.
        """
    def set_min_value(self, value: typing.Any) -> None:
        """set_min_value(self, value)

        Set attribute minimum value.

        :param value: the attribute minimum value. python data type must be compatible
                      with the attribute data format and type.
        """
    def set_write_value(self, value: typing.Any) -> None:
        """set_write_value(self, value)

           Set the writable attribute value.

           :param value: the data to be set. Data must be compatible with the attribute type and format.
                         for SPECTRUM and IMAGE attributes, data can be any type of sequence of elements
                         compatible with the attribute type

        .. versionchanged:: 10.1.0
            The dim_x and dim_y parameters were removed.
        """

class WrongData(DevFailed): ...
class WrongNameSyntax(DevFailed): ...

class _ImageFormat(enum.IntEnum):
    JpegImage: typing.ClassVar[_ImageFormat]  # value = <_ImageFormat.JpegImage: 1>
    RawImage: typing.ClassVar[_ImageFormat]  # value = <_ImageFormat.RawImage: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class __AttributeProxy:
    def __getstate__(self) -> tuple: ...
    @typing.overload
    def __init__(self, attribute_proxy: __AttributeProxy) -> None: ...
    @typing.overload
    def __init__(self, name: str) -> None: ...
    @typing.overload
    def __init__(self, device_proxy: DeviceProxy, name: str) -> None: ...
    def __setstate__(self, arg0: tuple) -> None: ...
    def _delete_property(self, propdata: DbData) -> None: ...
    @typing.overload
    def _get_property(self, propname: str, propdata: DbData) -> None: ...
    @typing.overload
    def _get_property(self, propnames: StdStringVector, propdata: DbData) -> None: ...
    @typing.overload
    def _get_property(self, propdata: DbData) -> None: ...
    def _put_property(self, propdata: DbData) -> None: ...
    def delete_property(
        self,
        value: str
        | tango._tango.DbDatum
        | tango._tango.DbData
        | list[str | bytes | tango._tango.DbDatum]
        | dict[str, tango._tango.DbDatum]
        | dict[str, list[str]]
        | dict[str, object],
    ) -> None:
        """Delete a the given of properties for this attribute.
        :param value: Can be one of the following:

                        1. :py:obj:`str` [in] - Single property data to be deleted.

                        2. :py:obj:`~tango.DbDatum` [in] - Single property data to be deleted.

                        3. :py:obj:`~tango.DbData` [in] - Several property data to be deleted.

                        4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` | :py:obj:`~tango.DbDatum`] [in] - Several property data to be deleted.

                        5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                           to be deleted (values are ignored).

                        6. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                           property names to be deleted (keys are ignored).


        :throws:
            :py:obj:`TypeError`: Raised in case of value has the wrong type.

            :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error.

            :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database.

            :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database.

            :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`
        """
    def get_device_proxy(self) -> DeviceProxy:
        """get_device_proxy(self) -> DeviceProxy

            Get associated DeviceProxy instance

        :return: the DeviceProxy instance used to communicate with the device to which the attributes belongs
        :rtype: DeviceProxy
        """
    def get_property(
        self,
        propname: str
        | tango._tango.DbDatum
        | tango._tango.DbData
        | list[str | bytes | tango._tango.DbDatum]
        | dict[str, tango._tango.DbDatum]
        | dict[str, list[str]]
        | dict[str, object],
        value=None,
    ) -> dict[str, list[str]]:
        """Get a (list) property(ies) for an attribute.

        :param propname: Can be one of the following:

                        1. :py:obj:`str` [in] - Single property data to be fetched.

                        2. :py:obj:`~tango.DbDatum` [in] - Single property data to be fetched.

                        3. :py:obj:`~tango.DbData` [in] - Several property data to be fetched.

                        4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes`] [in] - Several property data to be fetched.

                        5. :py:obj:`list`\\[:py:obj:`tango.DbDatum`] [in] - Several property data to be fetched.

                        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] [in] - Keys are property names
                           to be fetched (values are ignored).

                        7. :py:obj:`dict`\\[:py:obj:`str`, :obj:`tango.DbDatum`] [in] - Several `DbDatum.name` are
                           property names to be fetched (keys are ignored).


        :param value: Optional. For propname overloads with :py:obj:`str` and :py:obj:`list`\\[:py:obj:`str`] will be filed with the property values, if provided.
        :type value: :obj:`tango.DbData`, optional

        :returns: A :obj:`dict` object, which keys are the property names the value
                  associated with each key being a sequence of strings being the
                  property value.

        :throws:
            :py:obj:`TypeError`: Raised in case of propname has the wrong type.

            :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error.

            :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database.

            :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database.

            :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`

        .. versionadded:: 10.1.0: overloads with :obj:`dict` as propname parameter

        .. versionchanged:: 10.1.0: raises if propname has an invalid type instead of returning None
        """
    def name(self) -> str:
        """name(self) -> str

            Get attribute name

        :return: the attribute name
        :rtype: str
        """
    def put_property(
        self,
        value: str
        | tango._tango.DbDatum
        | tango._tango.DbData
        | list[str | bytes | tango._tango.DbDatum]
        | dict[str, tango._tango.DbDatum]
        | dict[str, list[str]]
        | dict[str, object],
    ) -> None:
        """Insert or update a list of properties for this attribute.

        :param value: Can be one of the following:

                        1. :py:obj:`str` - Single property data to be inserted.

                        2. :py:obj:`~tango.DbDatum` - Single property data to be inserted.

                        3. :py:obj:`~tango.DbData` - Several property data to be inserted.

                        4. :py:obj:`list`\\[:py:obj:`str` | :py:obj:`bytes` | :py:obj:`~tango.DbDatum`] - Several property data to be inserted.

                        5. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`~tango.DbDatum`] -
                            DbDatum is property to be inserted (keys are ignored).

                        6. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`list`\\[:py:obj:`str`]] - Keys are property names,
                            and value has data to be inserted.

                        7. :py:obj:`dict`\\[:py:obj:`str`, :py:obj:`object`] - Keys are property names, and `str(obj)` is property value.

        :throws:
            :py:obj:`TypeError`: Raised in case of value has the wrong type.

            :py:obj:`tango.NonDbDevice`: Raised in case of a non-database device error.

            :py:obj:`tango.ConnectionFailed`: Raised on connection failure with the database.

            :py:obj:`tango.CommunicationFailed`: Raised on communication failure with the database.

            :py:obj:`tango.DevFailed`: Raised on a device failure from the database device.`
        """

class __CallBackAutoDie:
    """INTERNAL CLASS - DO NOT USE IT"""
    def __init__(self, arg0: typing.SupportsInt) -> None: ...
    def attr_read(self, arg0: ...) -> None: ...
    def attr_written(self, arg0: ...) -> None: ...
    def cmd_ended(self, arg0: ...) -> None: ...

class __EventCallBack:
    """INTERNAL CLASS - DO NOT USE IT"""
    def __init__(self) -> None: ...
    @typing.overload
    def push_event(self, arg0: EventData) -> None: ...
    @typing.overload
    def push_event(self, arg0: AttrConfEventData) -> None: ...
    @typing.overload
    def push_event(self, arg0: DataReadyEventData) -> None: ...
    @typing.overload
    def push_event(self, arg0: DevIntrChangeEventData) -> None: ...

class __Group:
    def __init__(self, arg0: str) -> None: ...
    @typing.overload
    def _add(self, pattern: str, timeout_ms: typing.SupportsInt = -1) -> None: ...
    @typing.overload
    def _add(
        self, patterns: StdStringVector, timeout_ms: typing.SupportsInt = -1
    ) -> None: ...
    @typing.overload
    def _add(self, group: __Group, timeout_ms: typing.SupportsInt = -1) -> None: ...
    @typing.overload
    def _remove(self, pattern: str, forward: bool = True) -> None: ...
    @typing.overload
    def _remove(self, patterns: StdStringVector, forward: bool = True) -> None: ...
    @typing.overload
    def command_inout_asynch(
        self, cmd_name: str, forget: bool = False, forward: bool = True
    ) -> int:
        """command_inout_asynch(self, cmd_name, forget=False, forward=True) -> int

            Executes a Tango command on each device in the group asynchronously.
            The method sends the request to all devices and returns immediately.
            Pass the returned request id to Group.command_inout_reply() to obtain
            the results.

        Parameters :
            - cmd_name   : (str) Command name
            - forget     : (bool) Fire and forget flag. If set to true, it means that
                           no reply is expected (i.e. the caller does not care
                           about it and will not even try to get it)
            - forward    : (bool) If it is set to true (the default) request is
                            forwarded to subgroups. Otherwise, it is only applied
                            to the local set of devices.

        Return     : (int) request id. Pass the returned request id to
                    Group.command_inout_reply() to obtain the results.

        Throws     :
        """
    @typing.overload
    def command_inout_asynch(
        self,
        cmd_name: str,
        param: DeviceData,
        forget: bool = False,
        forward: bool = True,
    ) -> int:
        """command_inout_asynch(self, cmd_name, param, forget=False, forward=True) -> int

            Executes a Tango command on each device in the group asynchronously.
            The method sends the request to all devices and returns immediately.
            Pass the returned request id to Group.command_inout_reply() to obtain
            the results.

        Parameters :
            - cmd_name   : (str) Command name
            - param      : (any) parameter value
            - forget     : (bool) Fire and forget flag. If set to true, it means that
                           no reply is expected (i.e. the caller does not care
                           about it and will not even try to get it)
            - forward    : (bool) If it is set to true (the default) request is
                            forwarded to subgroups. Otherwise, it is only applied
                            to the local set of devices.

        Return     : (int) request id. Pass the returned request id to
                    Group.command_inout_reply() to obtain the results.

        Throws     :
        """
    @typing.overload
    def command_inout_asynch(
        self,
        cmd_name: str,
        param: DeviceDataList,
        forget: bool = False,
        forward: bool = True,
    ) -> int:
        """command_inout_asynch(self, cmd_name, param_list, forget=False, forward=True) -> int

            Executes a Tango command on each device in the group asynchronously.
            The method sends the request to all devices and returns immediately.
            Pass the returned request id to Group.command_inout_reply() to obtain
            the results.

        Parameters :
            - cmd_name   : (str) Command name
            - param_list : (tango.DeviceDataList) sequence of parameters.
                           When given, it's length must match the group size.
            - forget     : (bool) Fire and forget flag. If set to true, it means that
                           no reply is expected (i.e. the caller does not care
                           about it and will not even try to get it)
            - forward    : (bool) If it is set to true (the default) request is
                            forwarded to subgroups. Otherwise, it is only applied
                            to the local set of devices.

        Return     : (int) request id. Pass the returned request id to
                    Group.command_inout_reply() to obtain the results.

        Throws     :
        """
    def command_inout_reply(
        self, req_id: typing.SupportsInt, timeout_ms: typing.SupportsInt = 0
    ) -> GroupCmdReplyList:
        """command_inout_reply(self, req_id, timeout_ms=0) -> sequence<GroupCmdReply>

            Returns the results of an asynchronous command.

        Parameters :
            - req_id     : (int) Is a request identifier previously returned by one
                            of the command_inout_asynch methods
            - timeout_ms : (int) For each device in the hierarchy, if the command
                            result is not yet available, command_inout_reply
                            wait timeout_ms milliseconds before throwing an
                            exception. This exception will be part of the
                            global reply. If timeout_ms is set to 0,
                            command_inout_reply waits "indefinitely".

        Return     : (sequence<GroupCmdReply>)

        Throws     :
        """
    def contains(self, pattern: str, forward: bool = True) -> bool:
        """contains(self, pattern, forward=True) -> bool

        Parameters :
            - pattern    : (str) The pattern can be a fully qualified or simple
                            group name, a device name or a device name pattern.
            - forward    : (bool) If fwd is set to true (the default), the remove
                            request is also forwarded to subgroups. Otherwise,
                            it is only applied to the local set of elements.

        Return     : (bool) Returns true if the hierarchy contains groups and/or
                     devices which name matches the specified pattern. Returns
                     false otherwise.

        Throws     :
        """
    @typing.overload
    def disable(self) -> None: ...
    @typing.overload
    def disable(self, dev_name: str, forward: bool = True) -> None:
        """disable(self, dev_name, forward=True) -> None

            Disables group element. The element will be excluded from all group operations.

        :param dev_name: device_name name of the element, can contain wildcards (*). If more than one device matches the pattern, only the first one will be disabled.
        :type dev_name: str

        :param forward: flag to perform recursive search for the element in all sub-groups
        :type forward: bool
        """
    @typing.overload
    def enable(self) -> None: ...
    @typing.overload
    def enable(self, dev_name: str, forward: bool = True) -> None:
        """enable(self, dev_name, forward=True) -> None

            Enables group element. The element will participate in all group operations.

        :param dev_name: device_name name of the element, can contain wildcards (*). If more than one device matches the pattern, only the first one will be enabled.
        :type dev_name: str

        :param forward: flag to perform recursive search for the element in all sub-groups
        :type forward: bool
        """
    @typing.overload
    def get_device(self, dev_name: str) -> DeviceProxy:
        """get_device(self, dev_name) -> DeviceProxy

            Returns a reference to the specified device or None if there is no
            device by that name in the group. Or, returns a reference to the
            "idx-th" device in the hierarchy or NULL if the hierarchy contains
            less than "idx" devices.

            This method may throw an exception in case the specified device belongs
            to the group but can't be reached (not registered, down...). See example
            below:

            ::

                try:
                    dp = g.get_device("my/device/01")
                    if dp is None:
                        # my/device/01 does not belong to the group
                        pass
                except DevFailed, f:
                    # my/device/01 belongs to the group but can't be reached
                    pass

            The request is systematically forwarded to subgroups (i.e. if no device
            named device_name could be found in the local set of devices, the
            request is forwarded to subgroups).

        Parameters :
            - dev_name    : (str) Device name.

        Return     : DeviceProxy

        Throws     : DevFailed
        """
    @typing.overload
    def get_device(self, idx: typing.SupportsInt) -> DeviceProxy:
        """get_device(self, idx) -> DeviceProxy

            Returns a reference to the specified device or None if there is no
            device by that name in the group. Or, returns a reference to the
            "idx-th" device in the hierarchy or NULL if the hierarchy contains
            less than "idx" devices.

            This method may throw an exception in case the specified device belongs
            to the group but can't be reached (not registered, down...). See example
            below:

            ::

                try:
                    dp = g.get_device("my/device/01")
                    if dp is None:
                        # my/device/01 does not belong to the group
                        pass
                except DevFailed, f:
                    # my/device/01 belongs to the group but can't be reached
                    pass

            The request is systematically forwarded to subgroups (i.e. if no device
            named device_name could be found in the local set of devices, the
            request is forwarded to subgroups).

        Parameters :
            - idx         : (int) Device number.

        Return     : DeviceProxy

        Throws     : DevFailed
        """
    def get_device_list(self, forward: bool = True) -> StdStringVector:
        """get_device_list(self, forward=True) -> sequence<str>

            Considering the following hierarchy:

            ::

                g2.add("my/device/04")
                g2.add("my/device/05")

                g4.add("my/device/08")
                g4.add("my/device/09")

                g3.add("my/device/06")
                g3.add(g4)
                g3.add("my/device/07")

                g1.add("my/device/01")
                g1.add(g2)
                g1.add("my/device/03")
                g1.add(g3)
                g1.add("my/device/02")

            The returned vector content depends on the value of the forward option.
            If set to true, the results will be organized as follows:

            ::

                    dl = g1.get_device_list(True)

                dl[0] contains "my/device/01" which belongs to g1
                dl[1] contains "my/device/04" which belongs to g1.g2
                dl[2] contains "my/device/05" which belongs to g1.g2
                dl[3] contains "my/device/03" which belongs to g1
                dl[4] contains "my/device/06" which belongs to g1.g3
                dl[5] contains "my/device/08" which belongs to g1.g3.g4
                dl[6] contains "my/device/09" which belongs to g1.g3.g4
                dl[7] contains "my/device/07" which belongs to g1.g3
                dl[8] contains "my/device/02" which belongs to g1

            If the forward option is set to false, the results are:

            ::

                    dl = g1.get_device_list(False);

                dl[0] contains "my/device/01" which belongs to g1
                dl[1] contains "my/device/03" which belongs to g1
                dl[2] contains "my/device/02" which belongs to g1


        Parameters :
            - forward : (bool) If it is set to true (the default), the request
                        is forwarded to sub-groups. Otherwise, it is only
                        applied to the local set of devices.

        Return     : (sequence<str>) The list of devices currently in the hierarchy.

        Throws     :
        """
    def get_fully_qualified_name(self) -> str:
        """Get the complete (dpt-separated) name of the group. This takes into consideration the name of the group and its parents"""
    def get_group(self, group_name: str) -> __Group:
        """get_group(self, group_name ) -> Group

            Returns a reference to the specified group or None if there is no group
            by that name. The group_name can be a fully qualified name.

            Considering the following group:

            ::

                -> gauges
                    |-> cell-01
                    |    |-> penning
                    |    |    |-> ...
                    |    |-> pirani
                    |    |-> ...
                    |-> cell-02
                    |    |-> penning
                    |    |    |-> ...
                    |    |-> pirani
                    |    |-> ...
                    | -> cell-03
                    |    |-> ...
                    |
                    | -> ...

            A call to gauges.get_group("penning") returns the first group named
            "penning" in the hierarchy (i.e. gauges.cell-01.penning) while
            gauges.get_group("gauges.cell-02.penning'') returns the specified group.

            The request is systematically forwarded to subgroups (i.e. if no group
            named group_name could be found in the local set of elements, the request
            is forwarded to subgroups).

        Parameters :
            - group_name : (str)

        Return     : (Group)

        Throws     :

        New in PyTango 7.0.0
        """
    def get_name(self) -> str:
        """Get the name of the group. Eg: Group('name').get_name() == 'name'"""
    def get_parent(self) -> __Group: ...
    def get_size(self, forward: bool = True) -> int:
        """get_size(self, forward=True) -> int

        Parameters :
            - forward : (bool) If it is set to true (the default), the request is
                        forwarded to sub-groups.

        Return     : (int) The number of the devices in the hierarchy

        Throws     :
        """
    def is_enabled(self, device_name: str, forward: bool = True) -> bool:
        """is_enabled(self, device_name, forward) -> bool

            Check if a device is enabled

        :param dev_name: device_name name of the element. If more than one device matches the pattern, only the first one will be checked.
        :type dev_name: str

        :param forward: flag to perform recursive search for the element in all sub-groups
        :type forward: bool

        New in PyTango 7.0.0
        """
    def name_equals(self, name: str) -> bool:
        """name_equals(name) -> bool

        New in PyTango 7.0.0
        """
    def name_matches(self, name: str) -> bool:
        """name_equals(name) -> bool

        New in PyTango 7.0.0
        """
    def ping(self, forward: bool = True) -> bool:
        """ping(self, forward=True) -> bool

            Ping all devices in a group.

        Parameters :
            - forward    : (bool) If fwd is set to true (the default), the request
                            is also forwarded to subgroups. Otherwise, it is
                            only applied to the local set of devices.

        Return     : (bool) This method returns true if all devices in
                     the group are alive, false otherwise.

        Throws     :
        """
    def read_attribute_asynch(self, attr_name: str, forward: bool = True) -> int:
        """read_attribute_asynch(self, attr_name, forward=True,) -> int

            Reads an attribute on each device in the group asynchronously.
            The method sends the request to all devices and returns immediately.

        Parameters :
            - attr_name : (str) Name of the attribute to read.
            - forward   : (bool) If it is set to true (the default) request is
                            forwarded to subgroups. Otherwise, it is only applied
                            to the local set of devices.

        Return     : (int) request id. Pass the returned request id to
                    Group.read_attribute_reply() to obtain the results.

        Throws     :
        """
    def read_attribute_reply(
        self, req_id: typing.SupportsInt, timeout_ms: typing.SupportsInt = 0
    ) -> GroupAttrReplyList:
        """read_attribute_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupAttrReply>

            Returns the results of an asynchronous attribute reading.

        Parameters :
            - req_id     : (int) a request identifier previously returned by read_attribute_asynch.
            - timeout_ms : (int) For each device in the hierarchy, if the attribute
                            value is not yet available, read_attribute_reply
                            wait timeout_ms milliseconds before throwing an
                            exception. This exception will be part of the
                            global reply. If timeout_ms is set to 0,
                            read_attribute_reply waits "indefinitely".

        Return     : (sequence<GroupAttrReply>)

        Throws     :
        """
    def read_attributes_asynch(
        self, attr_names: StdStringVector, forward: bool = True
    ) -> int:
        """read_attributes_asynch(self, attr_names, forward=True) -> int

            Reads the attributes on each device in the group asynchronously.
            The method sends the request to all devices and returns immediately.

        Parameters :
            - attr_names : (sequence<str>) Name of the attributes to read.
            - forward    : (bool) If it is set to true (the default) request is
                            forwarded to subgroups. Otherwise, it is only applied
                            to the local set of devices.

        Return     : (int) request id. Pass the returned request id to
                    Group.read_attributes_reply() to obtain the results.

        Throws     :
        """
    def read_attributes_reply(
        self, req_id: typing.SupportsInt, timeout_ms: typing.SupportsInt = 0
    ) -> GroupAttrReplyList:
        """read_attributes_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupAttrReply>

            Returns the results of an asynchronous attribute reading.

        Parameters :
            - req_id     : (int) a request identifier previously returned by read_attribute_asynch.
            - timeout_ms : (int) For each device in the hierarchy, if the attribute
                           value is not yet available, read_attribute_reply
                           ait timeout_ms milliseconds before throwing an
                           exception. This exception will be part of the
                           global reply. If timeout_ms is set to 0,
                           read_attributes_reply waits "indefinitely".

        Return     : (sequence<GroupAttrReply>)

        Throws     :
        """
    def remove_all(self) -> None:
        """remove_all(self) -> None

        Removes all elements in the _RealGroup. After such a call, the _RealGroup is empty.
        """
    def set_timeout_millis(self, timeout_ms: typing.SupportsInt) -> None:
        """set_timeout_millis(self, timeout_ms) -> bool

            Set client side timeout for all devices composing the group in
            milliseconds. Any method which takes longer than this time to execute
            will throw an exception.

        Parameters :
            - timeout_ms : (int)

        Return     : None

        Throws     : (errors are ignored)

        New in PyTango 7.0.0
        """
    def write_attribute_asynch(
        self,
        attr: typing.Any,
        value: typing.Any,
        forward: bool = True,
        multi: bool = False,
    ) -> int:
        """Writes an attribute on each device in the group asynchronously.
        The method sends the request to all devices and returns immediately.

        Parameters :
            - attr : (str | AttributeInfoEx) Name or AttributeInfoEx of the attribute to write.
            - value     : (any) Value to write. See DeviceProxy.write_attribute
            - forward   : (bool) If it is set to true (the default) request is
                          forwarded to subgroups. Otherwise, it is only applied
                          to the local set of devices.
            - multi     : (bool) If it is set to false (the default), the same
                          value is applied to all devices in the group.
                          Otherwise the value is interpreted as a sequence of
                          values, and each value is applied to the corresponding
                          device in the group. In this case len(value) must be
                          equal to group.get_size()!

        Return     : (int) request id. Pass the returned request id to
                    Group.write_attribute_reply() to obtain the acknowledgements.

        Throws     :

        .. versionchanged:: 10.1.0 attr_name parameter was renamed to attr and
                            added support for AttributeInfoEx for attr_values parameter
        """
    def write_attribute_reply(
        self, req_id: typing.SupportsInt, timeout_ms: typing.SupportsInt = 0
    ) -> GroupReplyList:
        """write_attribute_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupReply>

            Returns the acknowledgements of an asynchronous attribute writing.

        Parameters :
            - req_id     : (int) a request identifier previously returned by write_attribute_asynch.
            - timeout_ms : (int) For each device in the hierarchy, if the acknowledgment
                            is not yet available, write_attribute_reply
                            wait timeout_ms milliseconds before throwing an
                            exception. This exception will be part of the
                            global reply. If timeout_ms is set to 0,
                            write_attribute_reply waits "indefinitely".

        Return     : (sequence<GroupReply>)

        Throws     :
        """

class alarm_flags(enum.IntEnum):
    max_level: typing.ClassVar[alarm_flags]  # value = <alarm_flags.max_level: 1>
    max_warn: typing.ClassVar[alarm_flags]  # value = <alarm_flags.max_warn: 4>
    min_level: typing.ClassVar[alarm_flags]  # value = <alarm_flags.min_level: 0>
    min_warn: typing.ClassVar[alarm_flags]  # value = <alarm_flags.min_warn: 3>
    numFlags: typing.ClassVar[alarm_flags]  # value = <alarm_flags.numFlags: 5>
    rds: typing.ClassVar[alarm_flags]  # value = <alarm_flags.rds: 2>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class asyn_req_type(enum.IntEnum):
    """An enumeration representing the asynchronous request type"""

    ALL_ASYNCH: typing.ClassVar[asyn_req_type]  # value = <asyn_req_type.ALL_ASYNCH: 2>
    CALLBACK: typing.ClassVar[asyn_req_type]  # value = <asyn_req_type.CALLBACK: 1>
    POLLING: typing.ClassVar[asyn_req_type]  # value = <asyn_req_type.POLLING: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

class cb_sub_model(enum.IntEnum):
    """An enumeration representing callback sub model"""

    PULL_CALLBACK: typing.ClassVar[
        cb_sub_model
    ]  # value = <cb_sub_model.PULL_CALLBACK: 1>
    PUSH_CALLBACK: typing.ClassVar[
        cb_sub_model
    ]  # value = <cb_sub_model.PUSH_CALLBACK: 0>
    @staticmethod
    def __str__(*args, **kwargs):
        """(self: object) -> detail::accessor<detail::accessor_policies::str_attr>"""
    @classmethod
    def __new__(cls, value): ...
    def __format__(self, format_spec):
        """Convert to a string according to format_spec."""

def _dump_cpp_coverage() -> None: ...
def _get_tango_lib_release() -> int: ...
def is_omni_thread() -> bool:
    """Determines if the calling thread is (or looks like) an omniORB thread.
    This includes user threads that have a dummy omniORB thread ID, such
    as that provided by EnsureOmniThread.

        Parameters : None

        Return     : (bool) True if the calling thread is an omnithread.

    New in PyTango 9.3.2
    """

def raise_asynch_exception(arg0: typing.SupportsInt, arg1: typing.Any) -> int: ...

ConstDevString: CmdArgType  # value = <CmdArgType.ConstDevString: 20>
DevBoolean: CmdArgType  # value = <CmdArgType.DevBoolean: 1>
DevDouble: CmdArgType  # value = <CmdArgType.DevDouble: 5>
DevEncoded: CmdArgType  # value = <CmdArgType.DevEncoded: 28>
DevEnum: CmdArgType  # value = <CmdArgType.DevEnum: 29>
DevFloat: CmdArgType  # value = <CmdArgType.DevFloat: 4>
DevLong: CmdArgType  # value = <CmdArgType.DevLong: 3>
DevLong64: CmdArgType  # value = <CmdArgType.DevLong64: 23>
DevShort: CmdArgType  # value = <CmdArgType.DevShort: 2>
DevString: CmdArgType  # value = <CmdArgType.DevString: 8>
DevUChar: CmdArgType  # value = <CmdArgType.DevUChar: 22>
DevULong: CmdArgType  # value = <CmdArgType.DevULong: 7>
DevULong64: CmdArgType  # value = <CmdArgType.DevULong64: 24>
DevUShort: CmdArgType  # value = <CmdArgType.DevUShort: 6>
DevVarBooleanArray: CmdArgType  # value = <CmdArgType.DevVarBooleanArray: 21>
DevVarCharArray: CmdArgType  # value = <CmdArgType.DevVarCharArray: 9>
DevVarDoubleArray: CmdArgType  # value = <CmdArgType.DevVarDoubleArray: 13>
DevVarDoubleStringArray: CmdArgType  # value = <CmdArgType.DevVarDoubleStringArray: 18>
DevVarEncodedArray: CmdArgType  # value = <CmdArgType.DevVarEncodedArray: 32>
DevVarFloatArray: CmdArgType  # value = <CmdArgType.DevVarFloatArray: 12>
DevVarLong64Array: CmdArgType  # value = <CmdArgType.DevVarLong64Array: 25>
DevVarLongArray: CmdArgType  # value = <CmdArgType.DevVarLongArray: 11>
DevVarLongStringArray: CmdArgType  # value = <CmdArgType.DevVarLongStringArray: 17>
DevVarShortArray: CmdArgType  # value = <CmdArgType.DevVarShortArray: 10>
DevVarStateArray: CmdArgType  # value = <CmdArgType.DevVarStateArray: 31>
DevVarStringArray: CmdArgType  # value = <CmdArgType.DevVarStringArray: 16>
DevVarULong64Array: CmdArgType  # value = <CmdArgType.DevVarULong64Array: 26>
DevVarULongArray: CmdArgType  # value = <CmdArgType.DevVarULongArray: 15>
DevVarUShortArray: CmdArgType  # value = <CmdArgType.DevVarUShortArray: 14>
DevVoid: CmdArgType  # value = <CmdArgType.DevVoid: 0>
FMT_UNKNOWN: AttrDataFormat  # value = <AttrDataFormat.FMT_UNKNOWN: 3>
IMAGE: AttrDataFormat  # value = <AttrDataFormat.IMAGE: 2>
READ: AttrWriteType  # value = <AttrWriteType.READ: 0>
READ_WITH_WRITE: AttrWriteType  # value = <AttrWriteType.READ_WITH_WRITE: 1>
READ_WRITE: AttrWriteType  # value = <AttrWriteType.READ_WRITE: 3>
SCALAR: AttrDataFormat  # value = <AttrDataFormat.SCALAR: 0>
SPECTRUM: AttrDataFormat  # value = <AttrDataFormat.SPECTRUM: 1>
Unknown: CmdArgType  # value = <CmdArgType.Unknown: 100>
WRITE: AttrWriteType  # value = <AttrWriteType.WRITE: 2>
WT_UNKNOWN: AttrWriteType  # value = <AttrWriteType.WT_UNKNOWN: 4>
__tangolib_version__: str = "10.1.1"
