from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class AlertChannelKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ALERT_CHANNEL_KIND_UNSPECIFIED: _ClassVar[AlertChannelKind]
    ALERT_CHANNEL_KIND_SLACK_CHANNEL: _ClassVar[AlertChannelKind]
    ALERT_CHANNEL_KIND_PAGERDUTY_SERVICE: _ClassVar[AlertChannelKind]
    ALERT_CHANNEL_KIND_INCIDENTIO_SERVICE: _ClassVar[AlertChannelKind]

ALERT_CHANNEL_KIND_UNSPECIFIED: AlertChannelKind
ALERT_CHANNEL_KIND_SLACK_CHANNEL: AlertChannelKind
ALERT_CHANNEL_KIND_PAGERDUTY_SERVICE: AlertChannelKind
ALERT_CHANNEL_KIND_INCIDENTIO_SERVICE: AlertChannelKind
