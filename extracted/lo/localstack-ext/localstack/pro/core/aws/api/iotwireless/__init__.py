from collections.abc import Iterable
from datetime import datetime
from enum import StrEnum
from typing import IO, TypedDict

from localstack.aws.api import RequestContext, ServiceException, ServiceRequest, handler

AccountLinked = bool
AckModeRetryDurationSecs = int
AddGwMetadata = bool
AmazonId = str
AmazonResourceName = str
ApId = str
AppEui = str
AppKey = str
AppSKey = str
AppServerPrivateKey = str
ApplicationServerPublicKey = str
AutoCreateTasks = bool
Avg = float
BCCH = int
BSIC = int
BaseLat = float
BaseLng = float
BaseStationId = int
BeaconingDataRate = int
BeaconingFrequency = int
CaptureTimeAccuracy = float
CdmaChannel = int
CellParams = int
CertificatePEM = str
CertificateValue = str
ChannelMask = str
ClassBTimeout = int
ClassCTimeout = int
ClientRequestToken = str
Coordinate = float
DakCertificateId = str
Description = str
DestinationArn = str
DestinationName = str
DevAddr = str
DevEui = str
DevStatusReqFreq = int
DeviceCreationFile = str
DeviceName = str
DeviceProfileArn = str
DeviceProfileId = str
DeviceProfileName = str
DeviceTypeId = str
DimensionValue = str
DlAllowed = bool
DlBucketSize = int
DlDr = int
DlFreq = int
DlRate = int
DlRatePolicy = str
Double = float
DownlinkFrequency = int
DrMax = int
DrMaxBox = int
DrMin = int
DrMinBox = int
EARFCN = int
EndPoint = str
EutranCid = int
Expression = str
FCntStart = int
FNwkSIntKey = str
FPort = int
FactorySupport = bool
FileDescriptor = str
Fingerprint = str
FirmwareUpdateImage = str
FirmwareUpdateRole = str
FragmentIntervalMS = int
FragmentSizeBytes = int
FuotaTaskArn = str
FuotaTaskId = str
FuotaTaskName = str
GPST = float
GatewayEui = str
GatewayMaxEirp = float
GenAppKey = str
GeranCid = int
GnssNav = str
GsmTimingAdvance = int
HorizontalAccuracy = float
HrAllowed = bool
IPAddress = str
ISODateTimeString = str
Id = str
Identifier = str
ImportTaskArn = str
ImportTaskId = str
Integer = int
IotCertificateId = str
JoinEui = str
LAC = int
LteTimingAdvance = int
MCC = int
MNC = int
MacAddress = str
MacVersion = str
Max = float
MaxAllowedSignature = int
MaxDutyCycle = int
MaxEirp = int
MaxResults = int
McGroupId = int
Message = str
MessageId = str
MetricQueryError = str
MetricQueryId = str
MetricUnit = str
Min = float
MinGwDiversity = int
Model = str
MulticastDeviceStatus = str
MulticastGroupArn = str
MulticastGroupId = str
MulticastGroupMessageId = str
MulticastGroupName = str
MulticastGroupStatus = str
NRCapable = bool
NbTransMax = int
NbTransMin = int
NetId = str
NetworkAnalyzerConfigurationArn = str
NetworkAnalyzerConfigurationName = str
NetworkId = int
NextToken = str
NumberOfDevicesInGroup = int
NumberOfDevicesRequested = int
NwkGeoLoc = bool
NwkKey = str
NwkSEncKey = str
NwkSKey = str
OnboardStatusReason = str
P90 = float
PCI = int
PSC = int
PackageVersion = str
PartnerAccountArn = str
PartnerAccountId = str
PathLoss = int
PayloadData = str
PilotPower = int
PingSlotDr = int
PingSlotFreq = int
PingSlotPeriod = int
PnOffset = int
PositionCoordinateValue = float
PositionResourceIdentifier = str
PositionSolverVersion = str
PrAllowed = bool
PresetFreq = int
ProviderNetId = str
QualificationStatus = bool
QueryString = str
RSCP = int
RSRP = int
RSRQ = float
RSS = int
RaAllowed = bool
RedundancyPercent = int
RegParamsRevision = str
RegistrationZone = int
ReportDevStatusBattery = bool
ReportDevStatusMargin = bool
ResourceId = str
ResourceIdentifier = str
ResourceType = str
Result = str
RfRegion = str
Role = str
RoleArn = str
RxDataRate2 = int
RxDelay1 = int
RxDrOffset1 = int
RxFreq2 = int
RxLevel = int
SNwkSIntKey = str
Seq = int
ServiceProfileArn = str
ServiceProfileId = str
ServiceProfileName = str
SessionTimeout = int
SidewalkId = str
SidewalkManufacturingSn = str
Station = str
StatusReason = str
Std = float
SubBand = int
Sum = float
Supports32BitFCnt = bool
SupportsClassB = bool
SupportsClassC = bool
SupportsJoin = bool
SystemId = int
TAC = int
TagKey = str
TagValue = str
TargetPer = int
TdscdmaTimingAdvance = int
ThingArn = str
ThingName = str
TransmissionInterval = int
TransmissionIntervalMulticast = int
TransmitMode = int
TxPowerIndexMax = int
TxPowerIndexMin = int
UARFCN = int
UARFCNDL = int
UlBucketSize = int
UlRate = int
UlRatePolicy = str
UpdateDataSource = str
UpdateSignature = str
Use2DSolver = bool
UtranCid = int
VerticalAccuracy = float
WirelessDeviceArn = str
WirelessDeviceId = str
WirelessDeviceName = str
WirelessGatewayArn = str
WirelessGatewayId = str
WirelessGatewayName = str
WirelessGatewayTaskDefinitionArn = str
WirelessGatewayTaskDefinitionId = str
WirelessGatewayTaskName = str


class AggregationPeriod(StrEnum):
    OneHour = "OneHour"
    OneDay = "OneDay"
    OneWeek = "OneWeek"


class ApplicationConfigType(StrEnum):
    SemtechGeolocation = "SemtechGeolocation"


class BatteryLevel(StrEnum):
    normal = "normal"
    low = "low"
    critical = "critical"


class ConnectionStatus(StrEnum):
    Connected = "Connected"
    Disconnected = "Disconnected"


class DeviceProfileType(StrEnum):
    Sidewalk = "Sidewalk"
    LoRaWAN = "LoRaWAN"


class DeviceState(StrEnum):
    Provisioned = "Provisioned"
    RegisteredNotSeen = "RegisteredNotSeen"
    RegisteredReachable = "RegisteredReachable"
    RegisteredUnreachable = "RegisteredUnreachable"


class DimensionName(StrEnum):
    DeviceId = "DeviceId"
    GatewayId = "GatewayId"


class DlClass(StrEnum):
    ClassB = "ClassB"
    ClassC = "ClassC"


class DownlinkMode(StrEnum):
    SEQUENTIAL = "SEQUENTIAL"
    CONCURRENT = "CONCURRENT"
    USING_UPLINK_GATEWAY = "USING_UPLINK_GATEWAY"


class Event(StrEnum):
    discovered = "discovered"
    lost = "lost"
    ack = "ack"
    nack = "nack"
    passthrough = "passthrough"


class EventNotificationPartnerType(StrEnum):
    Sidewalk = "Sidewalk"


class EventNotificationResourceType(StrEnum):
    SidewalkAccount = "SidewalkAccount"
    WirelessDevice = "WirelessDevice"
    WirelessGateway = "WirelessGateway"


class EventNotificationTopicStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class ExpressionType(StrEnum):
    RuleName = "RuleName"
    MqttTopic = "MqttTopic"


class FuotaDeviceStatus(StrEnum):
    Initial = "Initial"
    Package_Not_Supported = "Package_Not_Supported"
    FragAlgo_unsupported = "FragAlgo_unsupported"
    Not_enough_memory = "Not_enough_memory"
    FragIndex_unsupported = "FragIndex_unsupported"
    Wrong_descriptor = "Wrong_descriptor"
    SessionCnt_replay = "SessionCnt_replay"
    MissingFrag = "MissingFrag"
    MemoryError = "MemoryError"
    MICError = "MICError"
    Successful = "Successful"
    Device_exist_in_conflict_fuota_task = "Device_exist_in_conflict_fuota_task"


class FuotaTaskEvent(StrEnum):
    Fuota = "Fuota"


class FuotaTaskStatus(StrEnum):
    Pending = "Pending"
    FuotaSession_Waiting = "FuotaSession_Waiting"
    In_FuotaSession = "In_FuotaSession"
    FuotaDone = "FuotaDone"
    Delete_Waiting = "Delete_Waiting"


class FuotaTaskType(StrEnum):
    LoRaWAN = "LoRaWAN"


class IdentifierType(StrEnum):
    PartnerAccountId = "PartnerAccountId"
    DevEui = "DevEui"
    GatewayEui = "GatewayEui"
    WirelessDeviceId = "WirelessDeviceId"
    WirelessGatewayId = "WirelessGatewayId"


class ImportTaskStatus(StrEnum):
    INITIALIZING = "INITIALIZING"
    INITIALIZED = "INITIALIZED"
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    DELETING = "DELETING"


class LogLevel(StrEnum):
    INFO = "INFO"
    ERROR = "ERROR"
    DISABLED = "DISABLED"


class MessageType(StrEnum):
    CUSTOM_COMMAND_ID_NOTIFY = "CUSTOM_COMMAND_ID_NOTIFY"
    CUSTOM_COMMAND_ID_GET = "CUSTOM_COMMAND_ID_GET"
    CUSTOM_COMMAND_ID_SET = "CUSTOM_COMMAND_ID_SET"
    CUSTOM_COMMAND_ID_RESP = "CUSTOM_COMMAND_ID_RESP"


class MetricName(StrEnum):
    DeviceRSSI = "DeviceRSSI"
    DeviceSNR = "DeviceSNR"
    DeviceRoamingRSSI = "DeviceRoamingRSSI"
    DeviceRoamingSNR = "DeviceRoamingSNR"
    DeviceUplinkCount = "DeviceUplinkCount"
    DeviceDownlinkCount = "DeviceDownlinkCount"
    DeviceUplinkLostCount = "DeviceUplinkLostCount"
    DeviceUplinkLostRate = "DeviceUplinkLostRate"
    DeviceJoinRequestCount = "DeviceJoinRequestCount"
    DeviceJoinAcceptCount = "DeviceJoinAcceptCount"
    DeviceRoamingUplinkCount = "DeviceRoamingUplinkCount"
    DeviceRoamingDownlinkCount = "DeviceRoamingDownlinkCount"
    GatewayUpTime = "GatewayUpTime"
    GatewayDownTime = "GatewayDownTime"
    GatewayRSSI = "GatewayRSSI"
    GatewaySNR = "GatewaySNR"
    GatewayUplinkCount = "GatewayUplinkCount"
    GatewayDownlinkCount = "GatewayDownlinkCount"
    GatewayJoinRequestCount = "GatewayJoinRequestCount"
    GatewayJoinAcceptCount = "GatewayJoinAcceptCount"
    AwsAccountUplinkCount = "AwsAccountUplinkCount"
    AwsAccountDownlinkCount = "AwsAccountDownlinkCount"
    AwsAccountUplinkLostCount = "AwsAccountUplinkLostCount"
    AwsAccountUplinkLostRate = "AwsAccountUplinkLostRate"
    AwsAccountJoinRequestCount = "AwsAccountJoinRequestCount"
    AwsAccountJoinAcceptCount = "AwsAccountJoinAcceptCount"
    AwsAccountRoamingUplinkCount = "AwsAccountRoamingUplinkCount"
    AwsAccountRoamingDownlinkCount = "AwsAccountRoamingDownlinkCount"
    AwsAccountDeviceCount = "AwsAccountDeviceCount"
    AwsAccountGatewayCount = "AwsAccountGatewayCount"
    AwsAccountActiveDeviceCount = "AwsAccountActiveDeviceCount"
    AwsAccountActiveGatewayCount = "AwsAccountActiveGatewayCount"


class MetricQueryStatus(StrEnum):
    Succeeded = "Succeeded"
    Failed = "Failed"


class MulticastFrameInfo(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class OnboardStatus(StrEnum):
    INITIALIZED = "INITIALIZED"
    PENDING = "PENDING"
    ONBOARDED = "ONBOARDED"
    FAILED = "FAILED"


class PartnerType(StrEnum):
    Sidewalk = "Sidewalk"


class PositionConfigurationFec(StrEnum):
    ROSE = "ROSE"
    NONE = "NONE"


class PositionConfigurationStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class PositionResourceType(StrEnum):
    WirelessDevice = "WirelessDevice"
    WirelessGateway = "WirelessGateway"


class PositionSolverProvider(StrEnum):
    Semtech = "Semtech"


class PositionSolverType(StrEnum):
    GNSS = "GNSS"


class PositioningConfigStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class SigningAlg(StrEnum):
    Ed25519 = "Ed25519"
    P256r1 = "P256r1"


class SummaryMetricConfigurationStatus(StrEnum):
    Enabled = "Enabled"
    Disabled = "Disabled"


class SupportedRfRegion(StrEnum):
    EU868 = "EU868"
    US915 = "US915"
    AU915 = "AU915"
    AS923_1 = "AS923-1"
    AS923_2 = "AS923-2"
    AS923_3 = "AS923-3"
    AS923_4 = "AS923-4"
    EU433 = "EU433"
    CN470 = "CN470"
    CN779 = "CN779"
    RU864 = "RU864"
    KR920 = "KR920"
    IN865 = "IN865"


class WirelessDeviceEvent(StrEnum):
    Join = "Join"
    Rejoin = "Rejoin"
    Uplink_Data = "Uplink_Data"
    Downlink_Data = "Downlink_Data"
    Registration = "Registration"


class WirelessDeviceFrameInfo(StrEnum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class WirelessDeviceIdType(StrEnum):
    WirelessDeviceId = "WirelessDeviceId"
    DevEui = "DevEui"
    ThingName = "ThingName"
    SidewalkManufacturingSn = "SidewalkManufacturingSn"


class WirelessDeviceSidewalkStatus(StrEnum):
    PROVISIONED = "PROVISIONED"
    REGISTERED = "REGISTERED"
    ACTIVATED = "ACTIVATED"
    UNKNOWN = "UNKNOWN"


class WirelessDeviceType(StrEnum):
    Sidewalk = "Sidewalk"
    LoRaWAN = "LoRaWAN"


class WirelessGatewayEvent(StrEnum):
    CUPS_Request = "CUPS_Request"
    Certificate = "Certificate"


class WirelessGatewayIdType(StrEnum):
    GatewayEui = "GatewayEui"
    WirelessGatewayId = "WirelessGatewayId"
    ThingName = "ThingName"


class WirelessGatewayServiceType(StrEnum):
    CUPS = "CUPS"
    LNS = "LNS"


class WirelessGatewayTaskDefinitionType(StrEnum):
    UPDATE = "UPDATE"


class WirelessGatewayTaskStatus(StrEnum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FIRST_RETRY = "FIRST_RETRY"
    SECOND_RETRY = "SECOND_RETRY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class WirelessGatewayType(StrEnum):
    LoRaWAN = "LoRaWAN"


class AccessDeniedException(ServiceException):
    """User does not have permission to perform this action."""

    code: str = "AccessDeniedException"
    sender_fault: bool = False
    status_code: int = 403


class ConflictException(ServiceException):
    """Adding, updating, or deleting the resource can cause an inconsistent
    state.
    """

    code: str = "ConflictException"
    sender_fault: bool = False
    status_code: int = 409
    ResourceId: ResourceId | None
    ResourceType: ResourceType | None


class InternalServerException(ServiceException):
    """An unexpected error occurred while processing a request."""

    code: str = "InternalServerException"
    sender_fault: bool = False
    status_code: int = 500


class ResourceNotFoundException(ServiceException):
    """Resource does not exist."""

    code: str = "ResourceNotFoundException"
    sender_fault: bool = False
    status_code: int = 404
    ResourceId: ResourceId | None
    ResourceType: ResourceType | None


class ThrottlingException(ServiceException):
    """The request was denied because it exceeded the allowed API request rate."""

    code: str = "ThrottlingException"
    sender_fault: bool = False
    status_code: int = 429


class TooManyTagsException(ServiceException):
    """The request was denied because the resource can't have any more tags."""

    code: str = "TooManyTagsException"
    sender_fault: bool = False
    status_code: int = 400
    ResourceName: AmazonResourceName | None


class ValidationException(ServiceException):
    """The input did not meet the specified constraints."""

    code: str = "ValidationException"
    sender_fault: bool = False
    status_code: int = 400


class SessionKeysAbpV1_0_x(TypedDict, total=False):
    """Session keys for ABP v1.1"""

    NwkSKey: NwkSKey | None
    AppSKey: AppSKey | None


class AbpV1_0_x(TypedDict, total=False):
    """ABP device object for LoRaWAN specification v1.0.x"""

    DevAddr: DevAddr | None
    SessionKeys: SessionKeysAbpV1_0_x | None
    FCntStart: FCntStart | None


class SessionKeysAbpV1_1(TypedDict, total=False):
    """Session keys for ABP v1.1"""

    FNwkSIntKey: FNwkSIntKey | None
    SNwkSIntKey: SNwkSIntKey | None
    NwkSEncKey: NwkSEncKey | None
    AppSKey: AppSKey | None


class AbpV1_1(TypedDict, total=False):
    """ABP device object for LoRaWAN specification v1.1"""

    DevAddr: DevAddr | None
    SessionKeys: SessionKeysAbpV1_1 | None
    FCntStart: FCntStart | None


class Accuracy(TypedDict, total=False):
    """The accuracy of the estimated position in meters. An empty value
    indicates that no position data is available. A value of ‘0.0’ value
    indicates that position data is available. This data corresponds to the
    position information that you specified instead of the position computed
    by solver.
    """

    HorizontalAccuracy: HorizontalAccuracy | None
    VerticalAccuracy: VerticalAccuracy | None


class ApplicationConfig(TypedDict, total=False):
    """LoRaWAN application configuration, which can be used to perform
    geolocation.
    """

    FPort: FPort | None
    Type: ApplicationConfigType | None
    DestinationName: DestinationName | None


Applications = list[ApplicationConfig]
AssistPosition = list[Coordinate]


class Tag(TypedDict, total=False):
    """A simple label consisting of a customer-defined key-value pair"""

    Key: TagKey
    Value: TagValue


TagList = list[Tag]


class SidewalkAccountInfo(TypedDict, total=False):
    """Information about a Sidewalk account."""

    AmazonId: AmazonId | None
    AppServerPrivateKey: AppServerPrivateKey | None


class AssociateAwsAccountWithPartnerAccountRequest(ServiceRequest):
    Sidewalk: SidewalkAccountInfo
    ClientRequestToken: ClientRequestToken | None
    Tags: TagList | None


class AssociateAwsAccountWithPartnerAccountResponse(TypedDict, total=False):
    Sidewalk: SidewalkAccountInfo | None
    Arn: PartnerAccountArn | None


class AssociateMulticastGroupWithFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    MulticastGroupId: MulticastGroupId


class AssociateMulticastGroupWithFuotaTaskResponse(TypedDict, total=False):
    pass


class AssociateWirelessDeviceWithFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    WirelessDeviceId: WirelessDeviceId


class AssociateWirelessDeviceWithFuotaTaskResponse(TypedDict, total=False):
    pass


class AssociateWirelessDeviceWithMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId
    WirelessDeviceId: WirelessDeviceId


class AssociateWirelessDeviceWithMulticastGroupResponse(TypedDict, total=False):
    pass


class AssociateWirelessDeviceWithThingRequest(ServiceRequest):
    Id: WirelessDeviceId
    ThingArn: ThingArn


class AssociateWirelessDeviceWithThingResponse(TypedDict, total=False):
    pass


class AssociateWirelessGatewayWithCertificateRequest(ServiceRequest):
    Id: WirelessGatewayId
    IotCertificateId: IotCertificateId


class AssociateWirelessGatewayWithCertificateResponse(TypedDict, total=False):
    IotCertificateId: IotCertificateId | None


class AssociateWirelessGatewayWithThingRequest(ServiceRequest):
    Id: WirelessGatewayId
    ThingArn: ThingArn


class AssociateWirelessGatewayWithThingResponse(TypedDict, total=False):
    pass


BeaconingFrequencies = list[BeaconingFrequency]


class Beaconing(TypedDict, total=False):
    """Beaconing parameters for configuring the wireless gateways."""

    DataRate: BeaconingDataRate | None
    Frequencies: BeaconingFrequencies | None


class CancelMulticastGroupSessionRequest(ServiceRequest):
    Id: MulticastGroupId


class CancelMulticastGroupSessionResponse(TypedDict, total=False):
    pass


class CdmaNmrObj(TypedDict, total=False):
    """CDMA object for network measurement reports."""

    PnOffset: PnOffset
    CdmaChannel: CdmaChannel
    PilotPower: PilotPower | None
    BaseStationId: BaseStationId | None


CdmaNmrList = list[CdmaNmrObj]


class CdmaLocalId(TypedDict, total=False):
    """CDMA local ID information, which corresponds to the local identification
    parameters of a CDMA cell.
    """

    PnOffset: PnOffset
    CdmaChannel: CdmaChannel


class CdmaObj(TypedDict, total=False):
    """CDMA (Code-division multiple access) object."""

    SystemId: SystemId
    NetworkId: NetworkId
    BaseStationId: BaseStationId
    RegistrationZone: RegistrationZone | None
    CdmaLocalId: CdmaLocalId | None
    PilotPower: PilotPower | None
    BaseLat: BaseLat | None
    BaseLng: BaseLng | None
    CdmaNmr: CdmaNmrList | None


CdmaList = list[CdmaObj]


class LteNmrObj(TypedDict, total=False):
    """LTE object for network measurement reports."""

    Pci: PCI
    Earfcn: EARFCN
    EutranCid: EutranCid | None
    Rsrp: RSRP | None
    Rsrq: RSRQ | None


LteNmrList = list[LteNmrObj]


class LteLocalId(TypedDict, total=False):
    """LTE local identification (local ID) information."""

    Pci: PCI
    Earfcn: EARFCN


class LteObj(TypedDict, total=False):
    """LTE object."""

    Mcc: MCC
    Mnc: MNC
    EutranCid: EutranCid
    Tac: TAC | None
    LteLocalId: LteLocalId | None
    LteTimingAdvance: LteTimingAdvance | None
    Rsrp: RSRP | None
    Rsrq: RSRQ | None
    NrCapable: NRCapable | None
    LteNmr: LteNmrList | None


LteList = list[LteObj]


class TdscdmaNmrObj(TypedDict, total=False):
    """TD-SCDMA object for network measurement reports."""

    Uarfcn: UARFCN
    CellParams: CellParams
    UtranCid: UtranCid | None
    Rscp: RSCP | None
    PathLoss: PathLoss | None


TdscdmaNmrList = list[TdscdmaNmrObj]


class TdscdmaLocalId(TypedDict, total=False):
    """TD-SCDMA local identification (local Id) information."""

    Uarfcn: UARFCN
    CellParams: CellParams


class TdscdmaObj(TypedDict, total=False):
    """TD-SCDMA object."""

    Mcc: MCC
    Mnc: MNC
    Lac: LAC | None
    UtranCid: UtranCid
    TdscdmaLocalId: TdscdmaLocalId | None
    TdscdmaTimingAdvance: TdscdmaTimingAdvance | None
    Rscp: RSCP | None
    PathLoss: PathLoss | None
    TdscdmaNmr: TdscdmaNmrList | None


TdscdmaList = list[TdscdmaObj]


class WcdmaNmrObj(TypedDict, total=False):
    """Network Measurement Reports."""

    Uarfcndl: UARFCNDL
    Psc: PSC
    UtranCid: UtranCid
    Rscp: RSCP | None
    PathLoss: PathLoss | None


WcdmaNmrList = list[WcdmaNmrObj]


class WcdmaLocalId(TypedDict, total=False):
    """WCDMA local identification (local ID) information."""

    Uarfcndl: UARFCNDL
    Psc: PSC


class WcdmaObj(TypedDict, total=False):
    """WCDMA."""

    Mcc: MCC
    Mnc: MNC
    Lac: LAC | None
    UtranCid: UtranCid
    WcdmaLocalId: WcdmaLocalId | None
    Rscp: RSCP | None
    PathLoss: PathLoss | None
    WcdmaNmr: WcdmaNmrList | None


WcdmaList = list[WcdmaObj]


class GlobalIdentity(TypedDict, total=False):
    """Global identity information."""

    Lac: LAC
    GeranCid: GeranCid


class GsmNmrObj(TypedDict, total=False):
    """GSM object for network measurement reports."""

    Bsic: BSIC
    Bcch: BCCH
    RxLevel: RxLevel | None
    GlobalIdentity: GlobalIdentity | None


GsmNmrList = list[GsmNmrObj]


class GsmLocalId(TypedDict, total=False):
    """GSM local ID information, which corresponds to the local identification
    parameters of a GSM cell.
    """

    Bsic: BSIC
    Bcch: BCCH


class GsmObj(TypedDict, total=False):
    """GSM object."""

    Mcc: MCC
    Mnc: MNC
    Lac: LAC
    GeranCid: GeranCid
    GsmLocalId: GsmLocalId | None
    GsmTimingAdvance: GsmTimingAdvance | None
    RxLevel: RxLevel | None
    GsmNmr: GsmNmrList | None


GsmList = list[GsmObj]


class CellTowers(TypedDict, total=False):
    """The cell towers that were used to perform the measurements."""

    Gsm: GsmList | None
    Wcdma: WcdmaList | None
    Tdscdma: TdscdmaList | None
    Lte: LteList | None
    Cdma: CdmaList | None


class CertificateList(TypedDict, total=False):
    """List of sidewalk certificates."""

    SigningAlg: SigningAlg
    Value: CertificateValue


class LoRaWANConnectionStatusEventNotificationConfigurations(TypedDict, total=False):
    """Object for LoRaWAN connection status resource type event configuration."""

    GatewayEuiEventTopic: EventNotificationTopicStatus | None


class ConnectionStatusEventConfiguration(TypedDict, total=False):
    """Connection status event configuration object for enabling or disabling
    topic.
    """

    LoRaWAN: LoRaWANConnectionStatusEventNotificationConfigurations | None
    WirelessGatewayIdEventTopic: EventNotificationTopicStatus | None


class LoRaWANConnectionStatusResourceTypeEventConfiguration(TypedDict, total=False):
    """Object for LoRaWAN connection status resource type event configuration."""

    WirelessGatewayEventTopic: EventNotificationTopicStatus | None


class ConnectionStatusResourceTypeEventConfiguration(TypedDict, total=False):
    """Connection status resource type event configuration object for enabling
    or disabling topic.
    """

    LoRaWAN: LoRaWANConnectionStatusResourceTypeEventConfiguration | None


Crc = int


class CreateDestinationRequest(ServiceRequest):
    Name: DestinationName
    ExpressionType: ExpressionType
    Expression: Expression
    Description: Description | None
    RoleArn: RoleArn
    Tags: TagList | None
    ClientRequestToken: ClientRequestToken | None


class CreateDestinationResponse(TypedDict, total=False):
    Arn: DestinationArn | None
    Name: DestinationName | None


class SidewalkCreateDeviceProfile(TypedDict, total=False):
    """Sidewalk object for creating a device profile."""

    pass


FactoryPresetFreqsList = list[PresetFreq]


class LoRaWANDeviceProfile(TypedDict, total=False):
    """LoRaWANDeviceProfile object."""

    SupportsClassB: SupportsClassB | None
    ClassBTimeout: ClassBTimeout | None
    PingSlotPeriod: PingSlotPeriod | None
    PingSlotDr: PingSlotDr | None
    PingSlotFreq: PingSlotFreq | None
    SupportsClassC: SupportsClassC | None
    ClassCTimeout: ClassCTimeout | None
    MacVersion: MacVersion | None
    RegParamsRevision: RegParamsRevision | None
    RxDelay1: RxDelay1 | None
    RxDrOffset1: RxDrOffset1 | None
    RxDataRate2: RxDataRate2 | None
    RxFreq2: RxFreq2 | None
    FactoryPresetFreqsList: FactoryPresetFreqsList | None
    MaxEirp: MaxEirp | None
    MaxDutyCycle: MaxDutyCycle | None
    RfRegion: RfRegion | None
    SupportsJoin: SupportsJoin | None
    Supports32BitFCnt: Supports32BitFCnt | None


class CreateDeviceProfileRequest(ServiceRequest):
    Name: DeviceProfileName | None
    LoRaWAN: LoRaWANDeviceProfile | None
    Tags: TagList | None
    ClientRequestToken: ClientRequestToken | None
    Sidewalk: SidewalkCreateDeviceProfile | None


class CreateDeviceProfileResponse(TypedDict, total=False):
    Arn: DeviceProfileArn | None
    Id: DeviceProfileId | None


class LoRaWANFuotaTask(TypedDict, total=False):
    """The LoRaWAN information used with a FUOTA task."""

    RfRegion: SupportedRfRegion | None


class CreateFuotaTaskRequest(ServiceRequest):
    Name: FuotaTaskName | None
    Description: Description | None
    ClientRequestToken: ClientRequestToken | None
    LoRaWAN: LoRaWANFuotaTask | None
    FirmwareUpdateImage: FirmwareUpdateImage
    FirmwareUpdateRole: FirmwareUpdateRole
    Tags: TagList | None
    RedundancyPercent: RedundancyPercent | None
    FragmentSizeBytes: FragmentSizeBytes | None
    FragmentIntervalMS: FragmentIntervalMS | None
    Descriptor: FileDescriptor | None


class CreateFuotaTaskResponse(TypedDict, total=False):
    Arn: FuotaTaskArn | None
    Id: FuotaTaskId | None


GatewayListMulticast = list[WirelessGatewayId]


class ParticipatingGatewaysMulticast(TypedDict, total=False):
    """Specify the list of gateways to which you want to send the multicast
    downlink messages. The multicast message will be sent to each gateway in
    the list, with the transmission interval as the time interval between
    each message.
    """

    GatewayList: GatewayListMulticast | None
    TransmissionInterval: TransmissionIntervalMulticast | None


class LoRaWANMulticast(TypedDict, total=False):
    """The LoRaWAN information that is to be used with the multicast group."""

    RfRegion: SupportedRfRegion | None
    DlClass: DlClass | None
    ParticipatingGateways: ParticipatingGatewaysMulticast | None


class CreateMulticastGroupRequest(ServiceRequest):
    Name: MulticastGroupName | None
    Description: Description | None
    ClientRequestToken: ClientRequestToken | None
    LoRaWAN: LoRaWANMulticast
    Tags: TagList | None


class CreateMulticastGroupResponse(TypedDict, total=False):
    Arn: MulticastGroupArn | None
    Id: MulticastGroupId | None


NetworkAnalyzerMulticastGroupList = list[MulticastGroupId]
WirelessGatewayList = list[WirelessGatewayId]
WirelessDeviceList = list[WirelessDeviceId]


class TraceContent(TypedDict, total=False):
    """Trace content for your wireless devices, gateways, and multicast groups."""

    WirelessDeviceFrameInfo: WirelessDeviceFrameInfo | None
    LogLevel: LogLevel | None
    MulticastFrameInfo: MulticastFrameInfo | None


class CreateNetworkAnalyzerConfigurationRequest(ServiceRequest):
    Name: NetworkAnalyzerConfigurationName
    TraceContent: TraceContent | None
    WirelessDevices: WirelessDeviceList | None
    WirelessGateways: WirelessGatewayList | None
    Description: Description | None
    Tags: TagList | None
    ClientRequestToken: ClientRequestToken | None
    MulticastGroups: NetworkAnalyzerMulticastGroupList | None


class CreateNetworkAnalyzerConfigurationResponse(TypedDict, total=False):
    Arn: NetworkAnalyzerConfigurationArn | None
    Name: NetworkAnalyzerConfigurationName | None


class LoRaWANServiceProfile(TypedDict, total=False):
    """LoRaWANServiceProfile object."""

    AddGwMetadata: AddGwMetadata | None
    DrMin: DrMinBox | None
    DrMax: DrMaxBox | None
    PrAllowed: PrAllowed | None
    RaAllowed: RaAllowed | None
    TxPowerIndexMin: TxPowerIndexMin | None
    TxPowerIndexMax: TxPowerIndexMax | None
    NbTransMin: NbTransMin | None
    NbTransMax: NbTransMax | None


class CreateServiceProfileRequest(ServiceRequest):
    Name: ServiceProfileName | None
    LoRaWAN: LoRaWANServiceProfile | None
    Tags: TagList | None
    ClientRequestToken: ClientRequestToken | None


class CreateServiceProfileResponse(TypedDict, total=False):
    Arn: ServiceProfileArn | None
    Id: ServiceProfileId | None


class SidewalkPositioning(TypedDict, total=False):
    """The Positioning object of the Sidewalk device."""

    DestinationName: DestinationName | None


class SidewalkCreateWirelessDevice(TypedDict, total=False):
    """Sidewalk object for creating a wireless device."""

    DeviceProfileId: DeviceProfileId | None
    Positioning: SidewalkPositioning | None
    SidewalkManufacturingSn: SidewalkManufacturingSn | None


class Positioning(TypedDict, total=False):
    """The FPorts for the position information."""

    ClockSync: FPort | None
    Stream: FPort | None
    Gnss: FPort | None


class FPorts(TypedDict, total=False):
    """List of FPort assigned for different LoRaWAN application packages to use"""

    Fuota: FPort | None
    Multicast: FPort | None
    ClockSync: FPort | None
    Positioning: Positioning | None
    Applications: Applications | None


class OtaaV1_0_x(TypedDict, total=False):
    """OTAA device object for v1.0.x"""

    AppKey: AppKey | None
    AppEui: AppEui | None
    JoinEui: JoinEui | None
    GenAppKey: GenAppKey | None


class OtaaV1_1(TypedDict, total=False):
    """OTAA device object for v1.1"""

    AppKey: AppKey | None
    NwkKey: NwkKey | None
    JoinEui: JoinEui | None


class LoRaWANDevice(TypedDict, total=False):
    """LoRaWAN object for create functions."""

    DevEui: DevEui | None
    DeviceProfileId: DeviceProfileId | None
    ServiceProfileId: ServiceProfileId | None
    OtaaV1_1: OtaaV1_1 | None
    OtaaV1_0_x: OtaaV1_0_x | None
    AbpV1_1: AbpV1_1 | None
    AbpV1_0_x: AbpV1_0_x | None
    FPorts: FPorts | None


class CreateWirelessDeviceRequest(ServiceRequest):
    Type: WirelessDeviceType
    Name: WirelessDeviceName | None
    Description: Description | None
    DestinationName: DestinationName
    ClientRequestToken: ClientRequestToken | None
    LoRaWAN: LoRaWANDevice | None
    Tags: TagList | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkCreateWirelessDevice | None


class CreateWirelessDeviceResponse(TypedDict, total=False):
    Arn: WirelessDeviceArn | None
    Id: WirelessDeviceId | None


SubBands = list[SubBand]
NetIdFilters = list[NetId]
JoinEuiRange = list[JoinEui]
JoinEuiFilters = list[JoinEuiRange]


class LoRaWANGateway(TypedDict, total=False):
    """LoRaWANGateway object."""

    GatewayEui: GatewayEui | None
    RfRegion: RfRegion | None
    JoinEuiFilters: JoinEuiFilters | None
    NetIdFilters: NetIdFilters | None
    SubBands: SubBands | None
    Beaconing: Beaconing | None
    MaxEirp: GatewayMaxEirp | None


class CreateWirelessGatewayRequest(ServiceRequest):
    Name: WirelessGatewayName | None
    Description: Description | None
    LoRaWAN: LoRaWANGateway
    Tags: TagList | None
    ClientRequestToken: ClientRequestToken | None


class CreateWirelessGatewayResponse(TypedDict, total=False):
    Arn: WirelessGatewayArn | None
    Id: WirelessDeviceId | None


class LoRaWANGatewayVersion(TypedDict, total=False):
    """LoRaWANGatewayVersion object."""

    PackageVersion: PackageVersion | None
    Model: Model | None
    Station: Station | None


class LoRaWANUpdateGatewayTaskCreate(TypedDict, total=False):
    """LoRaWANUpdateGatewayTaskCreate object."""

    UpdateSignature: UpdateSignature | None
    SigKeyCrc: Crc | None
    CurrentVersion: LoRaWANGatewayVersion | None
    UpdateVersion: LoRaWANGatewayVersion | None


class UpdateWirelessGatewayTaskCreate(TypedDict, total=False):
    """UpdateWirelessGatewayTaskCreate object."""

    UpdateDataSource: UpdateDataSource | None
    UpdateDataRole: UpdateDataSource | None
    LoRaWAN: LoRaWANUpdateGatewayTaskCreate | None


class CreateWirelessGatewayTaskDefinitionRequest(ServiceRequest):
    AutoCreateTasks: AutoCreateTasks
    Name: WirelessGatewayTaskName | None
    Update: UpdateWirelessGatewayTaskCreate | None
    ClientRequestToken: ClientRequestToken | None
    Tags: TagList | None


class CreateWirelessGatewayTaskDefinitionResponse(TypedDict, total=False):
    Id: WirelessGatewayTaskDefinitionId | None
    Arn: WirelessGatewayTaskDefinitionArn | None


class CreateWirelessGatewayTaskRequest(ServiceRequest):
    Id: WirelessGatewayId
    WirelessGatewayTaskDefinitionId: WirelessGatewayTaskDefinitionId


class CreateWirelessGatewayTaskResponse(TypedDict, total=False):
    WirelessGatewayTaskDefinitionId: WirelessGatewayTaskDefinitionId | None
    Status: WirelessGatewayTaskStatus | None


CreatedAt = datetime
CreationDate = datetime
CreationTime = datetime


class DakCertificateMetadata(TypedDict, total=False):
    """The device attestation key (DAK) information."""

    CertificateId: DakCertificateId
    MaxAllowedSignature: MaxAllowedSignature | None
    FactorySupport: FactorySupport | None
    ApId: ApId | None
    DeviceTypeId: DeviceTypeId | None


DakCertificateMetadataList = list[DakCertificateMetadata]


class DeleteDestinationRequest(ServiceRequest):
    Name: DestinationName


class DeleteDestinationResponse(TypedDict, total=False):
    pass


class DeleteDeviceProfileRequest(ServiceRequest):
    Id: DeviceProfileId


class DeleteDeviceProfileResponse(TypedDict, total=False):
    pass


class DeleteFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId


class DeleteFuotaTaskResponse(TypedDict, total=False):
    pass


class DeleteMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId


class DeleteMulticastGroupResponse(TypedDict, total=False):
    pass


class DeleteNetworkAnalyzerConfigurationRequest(ServiceRequest):
    ConfigurationName: NetworkAnalyzerConfigurationName


class DeleteNetworkAnalyzerConfigurationResponse(TypedDict, total=False):
    pass


class DeleteQueuedMessagesRequest(ServiceRequest):
    Id: WirelessDeviceId
    MessageId: MessageId
    WirelessDeviceType: WirelessDeviceType | None


class DeleteQueuedMessagesResponse(TypedDict, total=False):
    pass


class DeleteServiceProfileRequest(ServiceRequest):
    Id: ServiceProfileId


class DeleteServiceProfileResponse(TypedDict, total=False):
    pass


class DeleteWirelessDeviceImportTaskRequest(ServiceRequest):
    Id: ImportTaskId


class DeleteWirelessDeviceImportTaskResponse(TypedDict, total=False):
    pass


class DeleteWirelessDeviceRequest(ServiceRequest):
    Id: WirelessDeviceId


class DeleteWirelessDeviceResponse(TypedDict, total=False):
    pass


class DeleteWirelessGatewayRequest(ServiceRequest):
    Id: WirelessGatewayId


class DeleteWirelessGatewayResponse(TypedDict, total=False):
    pass


class DeleteWirelessGatewayTaskDefinitionRequest(ServiceRequest):
    Id: WirelessGatewayTaskDefinitionId


class DeleteWirelessGatewayTaskDefinitionResponse(TypedDict, total=False):
    pass


class DeleteWirelessGatewayTaskRequest(ServiceRequest):
    Id: WirelessGatewayId


class DeleteWirelessGatewayTaskResponse(TypedDict, total=False):
    pass


class DeregisterWirelessDeviceRequest(ServiceRequest):
    Identifier: Identifier
    WirelessDeviceType: WirelessDeviceType | None


class DeregisterWirelessDeviceResponse(TypedDict, total=False):
    pass


class Destinations(TypedDict, total=False):
    """Describes a destination."""

    Arn: DestinationArn | None
    Name: DestinationName | None
    ExpressionType: ExpressionType | None
    Expression: Expression | None
    Description: Description | None
    RoleArn: RoleArn | None


DestinationList = list[Destinations]
DeviceCertificateList = list[CertificateList]
DeviceCreationFileList = list[DeviceCreationFile]


class DeviceProfile(TypedDict, total=False):
    """Describes a device profile."""

    Arn: DeviceProfileArn | None
    Name: DeviceProfileName | None
    Id: DeviceProfileId | None


DeviceProfileList = list[DeviceProfile]


class SidewalkEventNotificationConfigurations(TypedDict, total=False):
    """``SidewalkEventNotificationConfigurations`` object, which is the event
    configuration object for Sidewalk-related event topics.
    """

    AmazonIdEventTopic: EventNotificationTopicStatus | None


class DeviceRegistrationStateEventConfiguration(TypedDict, total=False):
    """Device registration state event configuration object for enabling and
    disabling relevant topics.
    """

    Sidewalk: SidewalkEventNotificationConfigurations | None
    WirelessDeviceIdEventTopic: EventNotificationTopicStatus | None


class SidewalkResourceTypeEventConfiguration(TypedDict, total=False):
    """Sidewalk resource type event configuration object for enabling or
    disabling topic.
    """

    WirelessDeviceEventTopic: EventNotificationTopicStatus | None


class DeviceRegistrationStateResourceTypeEventConfiguration(TypedDict, total=False):
    """Device registration state resource type event configuration object for
    enabling or disabling topic.
    """

    Sidewalk: SidewalkResourceTypeEventConfiguration | None


class Dimension(TypedDict, total=False):
    """The required list of dimensions for the metric."""

    name: DimensionName | None
    value: DimensionValue | None


Dimensions = list[Dimension]


class DisassociateAwsAccountFromPartnerAccountRequest(ServiceRequest):
    PartnerAccountId: PartnerAccountId
    PartnerType: PartnerType


class DisassociateAwsAccountFromPartnerAccountResponse(TypedDict, total=False):
    pass


class DisassociateMulticastGroupFromFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    MulticastGroupId: MulticastGroupId


class DisassociateMulticastGroupFromFuotaTaskResponse(TypedDict, total=False):
    pass


class DisassociateWirelessDeviceFromFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    WirelessDeviceId: WirelessDeviceId


class DisassociateWirelessDeviceFromFuotaTaskResponse(TypedDict, total=False):
    pass


class DisassociateWirelessDeviceFromMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId
    WirelessDeviceId: WirelessDeviceId


class DisassociateWirelessDeviceFromMulticastGroupResponse(TypedDict, total=False):
    pass


class DisassociateWirelessDeviceFromThingRequest(ServiceRequest):
    Id: WirelessDeviceId


class DisassociateWirelessDeviceFromThingResponse(TypedDict, total=False):
    pass


class DisassociateWirelessGatewayFromCertificateRequest(ServiceRequest):
    Id: WirelessGatewayId


class DisassociateWirelessGatewayFromCertificateResponse(TypedDict, total=False):
    pass


class DisassociateWirelessGatewayFromThingRequest(ServiceRequest):
    Id: WirelessGatewayId


class DisassociateWirelessGatewayFromThingResponse(TypedDict, total=False):
    pass


class GatewayListItem(TypedDict, total=False):
    """Gateway list item object that specifies the frequency and list of
    gateways for which the downlink message should be sent.
    """

    GatewayId: WirelessGatewayId
    DownlinkFrequency: DownlinkFrequency


GatewayList = list[GatewayListItem]


class ParticipatingGateways(TypedDict, total=False):
    """Specify the list of gateways to which you want to send downlink data
    traffic when the wireless device is running in class B or class C mode.
    """

    DownlinkMode: DownlinkMode
    GatewayList: GatewayList
    TransmissionInterval: TransmissionInterval


class LoRaWANSendDataToDevice(TypedDict, total=False):
    """LoRaWAN router info."""

    FPort: FPort | None
    ParticipatingGateways: ParticipatingGateways | None


class DownlinkQueueMessage(TypedDict, total=False):
    """The message in the downlink queue."""

    MessageId: MessageId | None
    TransmitMode: TransmitMode | None
    ReceivedAt: ISODateTimeString | None
    LoRaWAN: LoRaWANSendDataToDevice | None


DownlinkQueueMessagesList = list[DownlinkQueueMessage]


class MessageDeliveryStatusEventConfiguration(TypedDict, total=False):
    """Message delivery status event configuration object for enabling and
    disabling relevant topics.
    """

    Sidewalk: SidewalkEventNotificationConfigurations | None
    WirelessDeviceIdEventTopic: EventNotificationTopicStatus | None


class LoRaWANJoinEventNotificationConfigurations(TypedDict, total=False):
    """Object for LoRaWAN join resource type event configuration."""

    DevEuiEventTopic: EventNotificationTopicStatus | None


class JoinEventConfiguration(TypedDict, total=False):
    """Join event configuration object for enabling or disabling topic."""

    LoRaWAN: LoRaWANJoinEventNotificationConfigurations | None
    WirelessDeviceIdEventTopic: EventNotificationTopicStatus | None


class ProximityEventConfiguration(TypedDict, total=False):
    """Proximity event configuration object for enabling and disabling relevant
    topics.
    """

    Sidewalk: SidewalkEventNotificationConfigurations | None
    WirelessDeviceIdEventTopic: EventNotificationTopicStatus | None


class EventNotificationItemConfigurations(TypedDict, total=False):
    """Object of all event configurations and the status of the event topics."""

    DeviceRegistrationState: DeviceRegistrationStateEventConfiguration | None
    Proximity: ProximityEventConfiguration | None
    Join: JoinEventConfiguration | None
    ConnectionStatus: ConnectionStatusEventConfiguration | None
    MessageDeliveryStatus: MessageDeliveryStatusEventConfiguration | None


class EventConfigurationItem(TypedDict, total=False):
    """Event configuration object for a single resource."""

    Identifier: Identifier | None
    IdentifierType: IdentifierType | None
    PartnerType: EventNotificationPartnerType | None
    Events: EventNotificationItemConfigurations | None


EventConfigurationsList = list[EventConfigurationItem]


class FuotaTask(TypedDict, total=False):
    """A FUOTA task."""

    Id: FuotaTaskId | None
    Arn: FuotaTaskArn | None
    Name: FuotaTaskName | None


class FuotaTaskEventLogOption(TypedDict, total=False):
    """The log options for a FUOTA task event and can be used to set log levels
    for a specific FUOTA task event.

    For a LoRaWAN FUOTA task, the only possible event for a log message is
    ``Fuota``.
    """

    Event: FuotaTaskEvent
    LogLevel: LogLevel


FuotaTaskEventLogOptionList = list[FuotaTaskEventLogOption]
FuotaTaskList = list[FuotaTask]


class FuotaTaskLogOption(TypedDict, total=False):
    """The log options for FUOTA tasks and can be used to set log levels for a
    specific type of FUOTA task.
    """

    Type: FuotaTaskType
    LogLevel: LogLevel
    Events: FuotaTaskEventLogOptionList | None


FuotaTaskLogOptionList = list[FuotaTaskLogOption]
GeoJsonPayload = bytes


class GetDestinationRequest(ServiceRequest):
    Name: DestinationName


class GetDestinationResponse(TypedDict, total=False):
    Arn: DestinationArn | None
    Name: DestinationName | None
    Expression: Expression | None
    ExpressionType: ExpressionType | None
    Description: Description | None
    RoleArn: RoleArn | None


class GetDeviceProfileRequest(ServiceRequest):
    Id: DeviceProfileId


class SidewalkGetDeviceProfile(TypedDict, total=False):
    """Gets information about a Sidewalk device profile."""

    ApplicationServerPublicKey: ApplicationServerPublicKey | None
    QualificationStatus: QualificationStatus | None
    DakCertificateMetadata: DakCertificateMetadataList | None


class GetDeviceProfileResponse(TypedDict, total=False):
    Arn: DeviceProfileArn | None
    Name: DeviceProfileName | None
    Id: DeviceProfileId | None
    LoRaWAN: LoRaWANDeviceProfile | None
    Sidewalk: SidewalkGetDeviceProfile | None


class GetEventConfigurationByResourceTypesRequest(ServiceRequest):
    pass


class MessageDeliveryStatusResourceTypeEventConfiguration(TypedDict, total=False):
    """Message delivery status resource type event configuration object for
    enabling or disabling relevant topic.
    """

    Sidewalk: SidewalkResourceTypeEventConfiguration | None


class LoRaWANJoinResourceTypeEventConfiguration(TypedDict, total=False):
    """Object for LoRaWAN join resource type event configuration."""

    WirelessDeviceEventTopic: EventNotificationTopicStatus | None


class JoinResourceTypeEventConfiguration(TypedDict, total=False):
    """Join resource type event configuration object for enabling or disabling
    topic.
    """

    LoRaWAN: LoRaWANJoinResourceTypeEventConfiguration | None


class ProximityResourceTypeEventConfiguration(TypedDict, total=False):
    """Proximity resource type event configuration object for enabling or
    disabling topic.
    """

    Sidewalk: SidewalkResourceTypeEventConfiguration | None


class GetEventConfigurationByResourceTypesResponse(TypedDict, total=False):
    DeviceRegistrationState: DeviceRegistrationStateResourceTypeEventConfiguration | None
    Proximity: ProximityResourceTypeEventConfiguration | None
    Join: JoinResourceTypeEventConfiguration | None
    ConnectionStatus: ConnectionStatusResourceTypeEventConfiguration | None
    MessageDeliveryStatus: MessageDeliveryStatusResourceTypeEventConfiguration | None


class GetFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId


StartTime = datetime


class LoRaWANFuotaTaskGetInfo(TypedDict, total=False):
    """The LoRaWAN information returned from getting a FUOTA task."""

    RfRegion: RfRegion | None
    StartTime: StartTime | None


class GetFuotaTaskResponse(TypedDict, total=False):
    Arn: FuotaTaskArn | None
    Id: FuotaTaskId | None
    Status: FuotaTaskStatus | None
    Name: FuotaTaskName | None
    Description: Description | None
    LoRaWAN: LoRaWANFuotaTaskGetInfo | None
    FirmwareUpdateImage: FirmwareUpdateImage | None
    FirmwareUpdateRole: FirmwareUpdateRole | None
    CreatedAt: CreatedAt | None
    RedundancyPercent: RedundancyPercent | None
    FragmentSizeBytes: FragmentSizeBytes | None
    FragmentIntervalMS: FragmentIntervalMS | None
    Descriptor: FileDescriptor | None


class GetLogLevelsByResourceTypesRequest(ServiceRequest):
    pass


class WirelessDeviceEventLogOption(TypedDict, total=False):
    """The log options for a wireless device event and can be used to set log
    levels for a specific wireless device event.

    For a LoRaWAN device, possible events for a log messsage are: ``Join``,
    ``Rejoin``, ``Downlink_Data``, and ``Uplink_Data``. For a Sidewalk
    device, possible events for a log message are ``Registration``,
    ``Downlink_Data``, and ``Uplink_Data``.
    """

    Event: WirelessDeviceEvent
    LogLevel: LogLevel


WirelessDeviceEventLogOptionList = list[WirelessDeviceEventLogOption]


class WirelessDeviceLogOption(TypedDict, total=False):
    """The log options for wireless devices and can be used to set log levels
    for a specific type of wireless device.
    """

    Type: WirelessDeviceType
    LogLevel: LogLevel
    Events: WirelessDeviceEventLogOptionList | None


WirelessDeviceLogOptionList = list[WirelessDeviceLogOption]


class WirelessGatewayEventLogOption(TypedDict, total=False):
    """The log options for a wireless gateway event and can be used to set log
    levels for a specific wireless gateway event.

    For a LoRaWAN gateway, possible events for a log message are
    ``CUPS_Request`` and ``Certificate``.
    """

    Event: WirelessGatewayEvent
    LogLevel: LogLevel


WirelessGatewayEventLogOptionList = list[WirelessGatewayEventLogOption]


class WirelessGatewayLogOption(TypedDict, total=False):
    """The log options for wireless gateways and can be used to set log levels
    for a specific type of wireless gateway.
    """

    Type: WirelessGatewayType
    LogLevel: LogLevel
    Events: WirelessGatewayEventLogOptionList | None


WirelessGatewayLogOptionList = list[WirelessGatewayLogOption]


class GetLogLevelsByResourceTypesResponse(TypedDict, total=False):
    DefaultLogLevel: LogLevel | None
    WirelessGatewayLogOptions: WirelessGatewayLogOptionList | None
    WirelessDeviceLogOptions: WirelessDeviceLogOptionList | None
    FuotaTaskLogOptions: FuotaTaskLogOptionList | None


class GetMetricConfigurationRequest(ServiceRequest):
    pass


class SummaryMetricConfiguration(TypedDict, total=False):
    """The configuration of summary metrics."""

    Status: SummaryMetricConfigurationStatus | None


class GetMetricConfigurationResponse(TypedDict, total=False):
    SummaryMetric: SummaryMetricConfiguration | None


MetricQueryEndTimestamp = datetime
MetricQueryStartTimestamp = datetime


class SummaryMetricQuery(TypedDict, total=False):
    """The summary metric query object."""

    QueryId: MetricQueryId | None
    MetricName: MetricName | None
    Dimensions: Dimensions | None
    AggregationPeriod: AggregationPeriod | None
    StartTimestamp: MetricQueryStartTimestamp | None
    EndTimestamp: MetricQueryEndTimestamp | None


SummaryMetricQueries = list[SummaryMetricQuery]


class GetMetricsRequest(ServiceRequest):
    SummaryMetricQueries: SummaryMetricQueries | None


class MetricQueryValue(TypedDict, total=False):
    """The aggregated values of the metric."""

    Min: Min | None
    Max: Max | None
    Sum: Sum | None
    Avg: Avg | None
    Std: Std | None
    P90: P90 | None


MetricQueryValues = list[MetricQueryValue]
MetricQueryTimestamp = datetime
MetricQueryTimestamps = list[MetricQueryTimestamp]


class SummaryMetricQueryResult(TypedDict, total=False):
    """The result of the summary metrics aggregation operation."""

    QueryId: MetricQueryId | None
    QueryStatus: MetricQueryStatus | None
    Error: MetricQueryError | None
    MetricName: MetricName | None
    Dimensions: Dimensions | None
    AggregationPeriod: AggregationPeriod | None
    StartTimestamp: MetricQueryStartTimestamp | None
    EndTimestamp: MetricQueryEndTimestamp | None
    Timestamps: MetricQueryTimestamps | None
    Values: MetricQueryValues | None
    Unit: MetricUnit | None


SummaryMetricQueryResults = list[SummaryMetricQueryResult]


class GetMetricsResponse(TypedDict, total=False):
    SummaryMetricQueryResults: SummaryMetricQueryResults | None


class GetMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId


class LoRaWANMulticastGet(TypedDict, total=False):
    """The LoRaWAN information that is to be returned from getting multicast
    group information.
    """

    RfRegion: SupportedRfRegion | None
    DlClass: DlClass | None
    NumberOfDevicesRequested: NumberOfDevicesRequested | None
    NumberOfDevicesInGroup: NumberOfDevicesInGroup | None
    ParticipatingGateways: ParticipatingGatewaysMulticast | None


class GetMulticastGroupResponse(TypedDict, total=False):
    Arn: MulticastGroupArn | None
    Id: MulticastGroupId | None
    Name: MulticastGroupName | None
    Description: Description | None
    Status: MulticastGroupStatus | None
    LoRaWAN: LoRaWANMulticastGet | None
    CreatedAt: CreatedAt | None


class GetMulticastGroupSessionRequest(ServiceRequest):
    Id: MulticastGroupId


SessionStartTimeTimestamp = datetime


class LoRaWANMulticastSession(TypedDict, total=False):
    """The LoRaWAN information used with the multicast session."""

    DlDr: DlDr | None
    DlFreq: DlFreq | None
    SessionStartTime: SessionStartTimeTimestamp | None
    SessionTimeout: SessionTimeout | None
    PingSlotPeriod: PingSlotPeriod | None


class GetMulticastGroupSessionResponse(TypedDict, total=False):
    LoRaWAN: LoRaWANMulticastSession | None


class GetNetworkAnalyzerConfigurationRequest(ServiceRequest):
    ConfigurationName: NetworkAnalyzerConfigurationName


class GetNetworkAnalyzerConfigurationResponse(TypedDict, total=False):
    TraceContent: TraceContent | None
    WirelessDevices: WirelessDeviceList | None
    WirelessGateways: WirelessGatewayList | None
    Description: Description | None
    Arn: NetworkAnalyzerConfigurationArn | None
    Name: NetworkAnalyzerConfigurationName | None
    MulticastGroups: NetworkAnalyzerMulticastGroupList | None


class GetPartnerAccountRequest(ServiceRequest):
    PartnerAccountId: PartnerAccountId
    PartnerType: PartnerType


class SidewalkAccountInfoWithFingerprint(TypedDict, total=False):
    """Information about a Sidewalk account."""

    AmazonId: AmazonId | None
    Fingerprint: Fingerprint | None
    Arn: PartnerAccountArn | None


class GetPartnerAccountResponse(TypedDict, total=False):
    Sidewalk: SidewalkAccountInfoWithFingerprint | None
    AccountLinked: AccountLinked | None


class GetPositionConfigurationRequest(ServiceRequest):
    ResourceIdentifier: PositionResourceIdentifier
    ResourceType: PositionResourceType


class SemtechGnssDetail(TypedDict, total=False):
    """Details of the Semtech GNSS solver object."""

    Provider: PositionSolverProvider | None
    Type: PositionSolverType | None
    Status: PositionConfigurationStatus | None
    Fec: PositionConfigurationFec | None


class PositionSolverDetails(TypedDict, total=False):
    """The wrapper for position solver details."""

    SemtechGnss: SemtechGnssDetail | None


class GetPositionConfigurationResponse(TypedDict, total=False):
    Solvers: PositionSolverDetails | None
    Destination: DestinationName | None


class Gnss(TypedDict, total=False):
    """Global navigation satellite system (GNSS) object used for positioning."""

    Payload: GnssNav
    CaptureTime: GPST | None
    CaptureTimeAccuracy: CaptureTimeAccuracy | None
    AssistPosition: AssistPosition | None
    AssistAltitude: Coordinate | None
    Use2DSolver: Use2DSolver | None


class Ip(TypedDict, total=False):
    """IP address used for resolving device location."""

    IpAddress: IPAddress


class WiFiAccessPoint(TypedDict, total=False):
    """Wi-Fi access point."""

    MacAddress: MacAddress
    Rss: RSS


WiFiAccessPoints = list[WiFiAccessPoint]


class GetPositionEstimateRequest(ServiceRequest):
    WiFiAccessPoints: WiFiAccessPoints | None
    CellTowers: CellTowers | None
    Ip: Ip | None
    Gnss: Gnss | None
    Timestamp: CreationDate | None


class GetPositionEstimateResponse(TypedDict, total=False):
    GeoJsonPayload: GeoJsonPayload | IO[GeoJsonPayload] | Iterable[GeoJsonPayload] | None


class GetPositionRequest(ServiceRequest):
    ResourceIdentifier: PositionResourceIdentifier
    ResourceType: PositionResourceType


PositionCoordinate = list[PositionCoordinateValue]


class GetPositionResponse(TypedDict, total=False):
    Position: PositionCoordinate | None
    Accuracy: Accuracy | None
    SolverType: PositionSolverType | None
    SolverProvider: PositionSolverProvider | None
    SolverVersion: PositionSolverVersion | None
    Timestamp: ISODateTimeString | None


class GetResourceEventConfigurationRequest(ServiceRequest):
    Identifier: Identifier
    IdentifierType: IdentifierType
    PartnerType: EventNotificationPartnerType | None


class GetResourceEventConfigurationResponse(TypedDict, total=False):
    DeviceRegistrationState: DeviceRegistrationStateEventConfiguration | None
    Proximity: ProximityEventConfiguration | None
    Join: JoinEventConfiguration | None
    ConnectionStatus: ConnectionStatusEventConfiguration | None
    MessageDeliveryStatus: MessageDeliveryStatusEventConfiguration | None


class GetResourceLogLevelRequest(ServiceRequest):
    ResourceIdentifier: ResourceIdentifier
    ResourceType: ResourceType


class GetResourceLogLevelResponse(TypedDict, total=False):
    LogLevel: LogLevel | None


class GetResourcePositionRequest(ServiceRequest):
    ResourceIdentifier: PositionResourceIdentifier
    ResourceType: PositionResourceType


class GetResourcePositionResponse(TypedDict, total=False):
    GeoJsonPayload: GeoJsonPayload | IO[GeoJsonPayload] | Iterable[GeoJsonPayload] | None


class GetServiceEndpointRequest(ServiceRequest):
    ServiceType: WirelessGatewayServiceType | None


class GetServiceEndpointResponse(TypedDict, total=False):
    ServiceType: WirelessGatewayServiceType | None
    ServiceEndpoint: EndPoint | None
    ServerTrust: CertificatePEM | None


class GetServiceProfileRequest(ServiceRequest):
    Id: ServiceProfileId


class LoRaWANGetServiceProfileInfo(TypedDict, total=False):
    """LoRaWANGetServiceProfileInfo object."""

    UlRate: UlRate | None
    UlBucketSize: UlBucketSize | None
    UlRatePolicy: UlRatePolicy | None
    DlRate: DlRate | None
    DlBucketSize: DlBucketSize | None
    DlRatePolicy: DlRatePolicy | None
    AddGwMetadata: AddGwMetadata | None
    DevStatusReqFreq: DevStatusReqFreq | None
    ReportDevStatusBattery: ReportDevStatusBattery | None
    ReportDevStatusMargin: ReportDevStatusMargin | None
    DrMin: DrMin | None
    DrMax: DrMax | None
    ChannelMask: ChannelMask | None
    PrAllowed: PrAllowed | None
    HrAllowed: HrAllowed | None
    RaAllowed: RaAllowed | None
    NwkGeoLoc: NwkGeoLoc | None
    TargetPer: TargetPer | None
    MinGwDiversity: MinGwDiversity | None
    TxPowerIndexMin: TxPowerIndexMin | None
    TxPowerIndexMax: TxPowerIndexMax | None
    NbTransMin: NbTransMin | None
    NbTransMax: NbTransMax | None


class GetServiceProfileResponse(TypedDict, total=False):
    Arn: ServiceProfileArn | None
    Name: ServiceProfileName | None
    Id: ServiceProfileId | None
    LoRaWAN: LoRaWANGetServiceProfileInfo | None


class GetWirelessDeviceImportTaskRequest(ServiceRequest):
    Id: ImportTaskId


ImportedWirelessDeviceCount = int


class SidewalkGetStartImportInfo(TypedDict, total=False):
    """Sidewalk-related information for devices in an import task that are
    being onboarded.
    """

    DeviceCreationFileList: DeviceCreationFileList | None
    Role: Role | None
    Positioning: SidewalkPositioning | None


class GetWirelessDeviceImportTaskResponse(TypedDict, total=False):
    Id: ImportTaskId | None
    Arn: ImportTaskArn | None
    DestinationName: DestinationName | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkGetStartImportInfo | None
    CreationTime: CreationTime | None
    Status: ImportTaskStatus | None
    StatusReason: StatusReason | None
    InitializedImportedDeviceCount: ImportedWirelessDeviceCount | None
    PendingImportedDeviceCount: ImportedWirelessDeviceCount | None
    OnboardedImportedDeviceCount: ImportedWirelessDeviceCount | None
    FailedImportedDeviceCount: ImportedWirelessDeviceCount | None


class GetWirelessDeviceRequest(ServiceRequest):
    Identifier: Identifier
    IdentifierType: WirelessDeviceIdType


PrivateKeysList = list[CertificateList]


class SidewalkDevice(TypedDict, total=False):
    """Sidewalk device object."""

    AmazonId: AmazonId | None
    SidewalkId: SidewalkId | None
    SidewalkManufacturingSn: SidewalkManufacturingSn | None
    DeviceCertificates: DeviceCertificateList | None
    PrivateKeys: PrivateKeysList | None
    DeviceProfileId: DeviceProfileId | None
    CertificateId: DakCertificateId | None
    Status: WirelessDeviceSidewalkStatus | None
    Positioning: SidewalkPositioning | None


class GetWirelessDeviceResponse(TypedDict, total=False):
    Type: WirelessDeviceType | None
    Name: WirelessDeviceName | None
    Description: Description | None
    DestinationName: DestinationName | None
    Id: WirelessDeviceId | None
    Arn: WirelessDeviceArn | None
    ThingName: ThingName | None
    ThingArn: ThingArn | None
    LoRaWAN: LoRaWANDevice | None
    Sidewalk: SidewalkDevice | None
    Positioning: PositioningConfigStatus | None


class GetWirelessDeviceStatisticsRequest(ServiceRequest):
    WirelessDeviceId: WirelessDeviceId


class SidewalkDeviceMetadata(TypedDict, total=False):
    """MetaData for Sidewalk device."""

    Rssi: Integer | None
    BatteryLevel: BatteryLevel | None
    Event: Event | None
    DeviceState: DeviceState | None


class LoRaWANPublicGatewayMetadata(TypedDict, total=False):
    """LoRaWAN public gateway metadata."""

    ProviderNetId: ProviderNetId | None
    Id: Id | None
    Rssi: Double | None
    Snr: Double | None
    RfRegion: RfRegion | None
    DlAllowed: DlAllowed | None


LoRaWANPublicGatewayMetadataList = list[LoRaWANPublicGatewayMetadata]


class LoRaWANGatewayMetadata(TypedDict, total=False):
    """LoRaWAN gateway metatdata."""

    GatewayEui: GatewayEui | None
    Snr: Double | None
    Rssi: Double | None


LoRaWANGatewayMetadataList = list[LoRaWANGatewayMetadata]


class LoRaWANDeviceMetadata(TypedDict, total=False):
    """LoRaWAN device metatdata."""

    DevEui: DevEui | None
    FPort: Integer | None
    DataRate: Integer | None
    Frequency: Integer | None
    Timestamp: ISODateTimeString | None
    Gateways: LoRaWANGatewayMetadataList | None
    PublicGateways: LoRaWANPublicGatewayMetadataList | None


class GetWirelessDeviceStatisticsResponse(TypedDict, total=False):
    WirelessDeviceId: WirelessDeviceId | None
    LastUplinkReceivedAt: ISODateTimeString | None
    LoRaWAN: LoRaWANDeviceMetadata | None
    Sidewalk: SidewalkDeviceMetadata | None


class GetWirelessGatewayCertificateRequest(ServiceRequest):
    Id: WirelessGatewayId


class GetWirelessGatewayCertificateResponse(TypedDict, total=False):
    IotCertificateId: IotCertificateId | None
    LoRaWANNetworkServerCertificateId: IotCertificateId | None


class GetWirelessGatewayFirmwareInformationRequest(ServiceRequest):
    Id: WirelessGatewayId


class LoRaWANGatewayCurrentVersion(TypedDict, total=False):
    """LoRaWANGatewayCurrentVersion object."""

    CurrentVersion: LoRaWANGatewayVersion | None


class GetWirelessGatewayFirmwareInformationResponse(TypedDict, total=False):
    LoRaWAN: LoRaWANGatewayCurrentVersion | None


class GetWirelessGatewayRequest(ServiceRequest):
    Identifier: Identifier
    IdentifierType: WirelessGatewayIdType


class GetWirelessGatewayResponse(TypedDict, total=False):
    Name: WirelessGatewayName | None
    Id: WirelessGatewayId | None
    Description: Description | None
    LoRaWAN: LoRaWANGateway | None
    Arn: WirelessGatewayArn | None
    ThingName: ThingName | None
    ThingArn: ThingArn | None


class GetWirelessGatewayStatisticsRequest(ServiceRequest):
    WirelessGatewayId: WirelessGatewayId


class GetWirelessGatewayStatisticsResponse(TypedDict, total=False):
    WirelessGatewayId: WirelessGatewayId | None
    LastUplinkReceivedAt: ISODateTimeString | None
    ConnectionStatus: ConnectionStatus | None


class GetWirelessGatewayTaskDefinitionRequest(ServiceRequest):
    Id: WirelessGatewayTaskDefinitionId


class GetWirelessGatewayTaskDefinitionResponse(TypedDict, total=False):
    AutoCreateTasks: AutoCreateTasks | None
    Name: WirelessGatewayTaskName | None
    Update: UpdateWirelessGatewayTaskCreate | None
    Arn: WirelessGatewayTaskDefinitionArn | None


class GetWirelessGatewayTaskRequest(ServiceRequest):
    Id: WirelessGatewayId


class GetWirelessGatewayTaskResponse(TypedDict, total=False):
    WirelessGatewayId: WirelessGatewayId | None
    WirelessGatewayTaskDefinitionId: WirelessGatewayTaskDefinitionId | None
    LastUplinkReceivedAt: ISODateTimeString | None
    TaskCreatedAt: ISODateTimeString | None
    Status: WirelessGatewayTaskStatus | None


LastUpdateTime = datetime


class ImportedSidewalkDevice(TypedDict, total=False):
    """Information about a Sidewalk device that has been added to an import
    task.
    """

    SidewalkManufacturingSn: SidewalkManufacturingSn | None
    OnboardingStatus: OnboardStatus | None
    OnboardingStatusReason: OnboardStatusReason | None
    LastUpdateTime: LastUpdateTime | None


class ImportedWirelessDevice(TypedDict, total=False):
    """Information about a wireless device that has been added to an import
    task.
    """

    Sidewalk: ImportedSidewalkDevice | None


ImportedWirelessDeviceList = list[ImportedWirelessDevice]


class ListDestinationsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListDestinationsResponse(TypedDict, total=False):
    NextToken: NextToken | None
    DestinationList: DestinationList | None


class ListDeviceProfilesRequest(ServiceRequest):
    NextToken: NextToken | None
    MaxResults: MaxResults | None
    DeviceProfileType: DeviceProfileType | None


class ListDeviceProfilesResponse(TypedDict, total=False):
    NextToken: NextToken | None
    DeviceProfileList: DeviceProfileList | None


class ListDevicesForWirelessDeviceImportTaskRequest(ServiceRequest):
    Id: ImportTaskId
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    Status: OnboardStatus | None


class SidewalkListDevicesForImportInfo(TypedDict, total=False):
    """The Sidewalk-related object containing positioning information used to
    configure Sidewalk devices during import.
    """

    Positioning: SidewalkPositioning | None


class ListDevicesForWirelessDeviceImportTaskResponse(TypedDict, total=False):
    NextToken: NextToken | None
    DestinationName: DestinationName | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkListDevicesForImportInfo | None
    ImportedWirelessDeviceList: ImportedWirelessDeviceList | None


class ListEventConfigurationsRequest(ServiceRequest):
    ResourceType: EventNotificationResourceType
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class ListEventConfigurationsResponse(TypedDict, total=False):
    NextToken: NextToken | None
    EventConfigurationsList: EventConfigurationsList | None


class ListFuotaTasksRequest(ServiceRequest):
    NextToken: NextToken | None
    MaxResults: MaxResults | None


class ListFuotaTasksResponse(TypedDict, total=False):
    NextToken: NextToken | None
    FuotaTaskList: FuotaTaskList | None


class ListMulticastGroupsByFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    NextToken: NextToken | None
    MaxResults: MaxResults | None


class MulticastGroupByFuotaTask(TypedDict, total=False):
    """A multicast group that is associated with a FUOTA task."""

    Id: MulticastGroupId | None


MulticastGroupListByFuotaTask = list[MulticastGroupByFuotaTask]


class ListMulticastGroupsByFuotaTaskResponse(TypedDict, total=False):
    NextToken: NextToken | None
    MulticastGroupList: MulticastGroupListByFuotaTask | None


class ListMulticastGroupsRequest(ServiceRequest):
    NextToken: NextToken | None
    MaxResults: MaxResults | None


class MulticastGroup(TypedDict, total=False):
    """A multicast group."""

    Id: MulticastGroupId | None
    Arn: MulticastGroupArn | None
    Name: MulticastGroupName | None


MulticastGroupList = list[MulticastGroup]


class ListMulticastGroupsResponse(TypedDict, total=False):
    NextToken: NextToken | None
    MulticastGroupList: MulticastGroupList | None


class ListNetworkAnalyzerConfigurationsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class NetworkAnalyzerConfigurations(TypedDict, total=False):
    """Network analyzer configurations."""

    Arn: NetworkAnalyzerConfigurationArn | None
    Name: NetworkAnalyzerConfigurationName | None


NetworkAnalyzerConfigurationList = list[NetworkAnalyzerConfigurations]


class ListNetworkAnalyzerConfigurationsResponse(TypedDict, total=False):
    NextToken: NextToken | None
    NetworkAnalyzerConfigurationList: NetworkAnalyzerConfigurationList | None


class ListPartnerAccountsRequest(ServiceRequest):
    NextToken: NextToken | None
    MaxResults: MaxResults | None


SidewalkAccountList = list[SidewalkAccountInfoWithFingerprint]


class ListPartnerAccountsResponse(TypedDict, total=False):
    NextToken: NextToken | None
    Sidewalk: SidewalkAccountList | None


class ListPositionConfigurationsRequest(ServiceRequest):
    ResourceType: PositionResourceType | None
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class PositionConfigurationItem(TypedDict, total=False):
    """The wrapper for a position configuration."""

    ResourceIdentifier: PositionResourceIdentifier | None
    ResourceType: PositionResourceType | None
    Solvers: PositionSolverDetails | None
    Destination: DestinationName | None


PositionConfigurationList = list[PositionConfigurationItem]


class ListPositionConfigurationsResponse(TypedDict, total=False):
    PositionConfigurationList: PositionConfigurationList | None
    NextToken: NextToken | None


class ListQueuedMessagesRequest(ServiceRequest):
    Id: WirelessDeviceId
    NextToken: NextToken | None
    MaxResults: MaxResults | None
    WirelessDeviceType: WirelessDeviceType | None


class ListQueuedMessagesResponse(TypedDict, total=False):
    NextToken: NextToken | None
    DownlinkQueueMessagesList: DownlinkQueueMessagesList | None


class ListServiceProfilesRequest(ServiceRequest):
    NextToken: NextToken | None
    MaxResults: MaxResults | None


class ServiceProfile(TypedDict, total=False):
    """Information about a service profile."""

    Arn: ServiceProfileArn | None
    Name: ServiceProfileName | None
    Id: ServiceProfileId | None


ServiceProfileList = list[ServiceProfile]


class ListServiceProfilesResponse(TypedDict, total=False):
    NextToken: NextToken | None
    ServiceProfileList: ServiceProfileList | None


class ListTagsForResourceRequest(ServiceRequest):
    ResourceArn: AmazonResourceName


class ListTagsForResourceResponse(TypedDict, total=False):
    Tags: TagList | None


class ListWirelessDeviceImportTasksRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None


class WirelessDeviceImportTask(TypedDict, total=False):
    """Information about an import task for wireless devices."""

    Id: ImportTaskId | None
    Arn: ImportTaskArn | None
    DestinationName: DestinationName | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkGetStartImportInfo | None
    CreationTime: CreationTime | None
    Status: ImportTaskStatus | None
    StatusReason: StatusReason | None
    InitializedImportedDeviceCount: ImportedWirelessDeviceCount | None
    PendingImportedDeviceCount: ImportedWirelessDeviceCount | None
    OnboardedImportedDeviceCount: ImportedWirelessDeviceCount | None
    FailedImportedDeviceCount: ImportedWirelessDeviceCount | None


WirelessDeviceImportTaskList = list[WirelessDeviceImportTask]


class ListWirelessDeviceImportTasksResponse(TypedDict, total=False):
    NextToken: NextToken | None
    WirelessDeviceImportTaskList: WirelessDeviceImportTaskList | None


class ListWirelessDevicesRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    DestinationName: DestinationName | None
    DeviceProfileId: DeviceProfileId | None
    ServiceProfileId: ServiceProfileId | None
    WirelessDeviceType: WirelessDeviceType | None
    FuotaTaskId: FuotaTaskId | None
    MulticastGroupId: MulticastGroupId | None


class SidewalkListDevice(TypedDict, total=False):
    """Sidewalk object used by list functions."""

    AmazonId: AmazonId | None
    SidewalkId: SidewalkId | None
    SidewalkManufacturingSn: SidewalkManufacturingSn | None
    DeviceCertificates: DeviceCertificateList | None
    DeviceProfileId: DeviceProfileId | None
    Status: WirelessDeviceSidewalkStatus | None
    Positioning: SidewalkPositioning | None


class LoRaWANListDevice(TypedDict, total=False):
    """LoRaWAN object for list functions."""

    DevEui: DevEui | None


class WirelessDeviceStatistics(TypedDict, total=False):
    """Information about a wireless device's operation."""

    Arn: WirelessDeviceArn | None
    Id: WirelessDeviceId | None
    Type: WirelessDeviceType | None
    Name: WirelessDeviceName | None
    DestinationName: DestinationName | None
    LastUplinkReceivedAt: ISODateTimeString | None
    LoRaWAN: LoRaWANListDevice | None
    Sidewalk: SidewalkListDevice | None
    FuotaDeviceStatus: FuotaDeviceStatus | None
    MulticastDeviceStatus: MulticastDeviceStatus | None
    McGroupId: McGroupId | None
    Positioning: PositioningConfigStatus | None


WirelessDeviceStatisticsList = list[WirelessDeviceStatistics]


class ListWirelessDevicesResponse(TypedDict, total=False):
    NextToken: NextToken | None
    WirelessDeviceList: WirelessDeviceStatisticsList | None


class ListWirelessGatewayTaskDefinitionsRequest(ServiceRequest):
    MaxResults: MaxResults | None
    NextToken: NextToken | None
    TaskDefinitionType: WirelessGatewayTaskDefinitionType | None


class LoRaWANUpdateGatewayTaskEntry(TypedDict, total=False):
    """LoRaWANUpdateGatewayTaskEntry object."""

    CurrentVersion: LoRaWANGatewayVersion | None
    UpdateVersion: LoRaWANGatewayVersion | None


class UpdateWirelessGatewayTaskEntry(TypedDict, total=False):
    """UpdateWirelessGatewayTaskEntry object."""

    Id: WirelessGatewayTaskDefinitionId | None
    LoRaWAN: LoRaWANUpdateGatewayTaskEntry | None
    Arn: WirelessGatewayTaskDefinitionArn | None


WirelessGatewayTaskDefinitionList = list[UpdateWirelessGatewayTaskEntry]


class ListWirelessGatewayTaskDefinitionsResponse(TypedDict, total=False):
    NextToken: NextToken | None
    TaskDefinitions: WirelessGatewayTaskDefinitionList | None


class ListWirelessGatewaysRequest(ServiceRequest):
    NextToken: NextToken | None
    MaxResults: MaxResults | None


class WirelessGatewayStatistics(TypedDict, total=False):
    """Information about a wireless gateway's operation."""

    Arn: WirelessGatewayArn | None
    Id: WirelessGatewayId | None
    Name: WirelessGatewayName | None
    Description: Description | None
    LoRaWAN: LoRaWANGateway | None
    LastUplinkReceivedAt: ISODateTimeString | None


WirelessGatewayStatisticsList = list[WirelessGatewayStatistics]


class ListWirelessGatewaysResponse(TypedDict, total=False):
    NextToken: NextToken | None
    WirelessGatewayList: WirelessGatewayStatisticsList | None


class LoRaWANMulticastMetadata(TypedDict, total=False):
    """The metadata information of the LoRaWAN multicast group."""

    FPort: FPort | None


class LoRaWANStartFuotaTask(TypedDict, total=False):
    """The LoRaWAN information used to start a FUOTA task."""

    StartTime: StartTime | None


class UpdateFPorts(TypedDict, total=False):
    """Object for updating the FPorts information."""

    Positioning: Positioning | None
    Applications: Applications | None


class UpdateAbpV1_0_x(TypedDict, total=False):
    """ABP device object for LoRaWAN specification v1.0.x"""

    FCntStart: FCntStart | None


class UpdateAbpV1_1(TypedDict, total=False):
    """ABP device object for LoRaWAN specification v1.1"""

    FCntStart: FCntStart | None


class LoRaWANUpdateDevice(TypedDict, total=False):
    """LoRaWAN object for update functions."""

    DeviceProfileId: DeviceProfileId | None
    ServiceProfileId: ServiceProfileId | None
    AbpV1_1: UpdateAbpV1_1 | None
    AbpV1_0_x: UpdateAbpV1_0_x | None
    FPorts: UpdateFPorts | None


class MulticastWirelessMetadata(TypedDict, total=False):
    """Wireless metadata that is to be sent to multicast group."""

    LoRaWAN: LoRaWANMulticastMetadata | None


class SemtechGnssConfiguration(TypedDict, total=False):
    """Information about the Semtech GNSS solver configuration."""

    Status: PositionConfigurationStatus
    Fec: PositionConfigurationFec


class PositionSolverConfigurations(TypedDict, total=False):
    """The wrapper for position solver configurations."""

    SemtechGnss: SemtechGnssConfiguration | None


class PutPositionConfigurationRequest(ServiceRequest):
    ResourceIdentifier: PositionResourceIdentifier
    ResourceType: PositionResourceType
    Solvers: PositionSolverConfigurations | None
    Destination: DestinationName | None


class PutPositionConfigurationResponse(TypedDict, total=False):
    pass


class PutResourceLogLevelRequest(ServiceRequest):
    ResourceIdentifier: ResourceIdentifier
    ResourceType: ResourceType
    LogLevel: LogLevel


class PutResourceLogLevelResponse(TypedDict, total=False):
    pass


class ResetAllResourceLogLevelsRequest(ServiceRequest):
    pass


class ResetAllResourceLogLevelsResponse(TypedDict, total=False):
    pass


class ResetResourceLogLevelRequest(ServiceRequest):
    ResourceIdentifier: ResourceIdentifier
    ResourceType: ResourceType


class ResetResourceLogLevelResponse(TypedDict, total=False):
    pass


class SendDataToMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId
    PayloadData: PayloadData
    WirelessMetadata: MulticastWirelessMetadata


class SendDataToMulticastGroupResponse(TypedDict, total=False):
    MessageId: MulticastGroupMessageId | None


class SidewalkSendDataToDevice(TypedDict, total=False):
    """Information about a Sidewalk router."""

    Seq: Seq | None
    MessageType: MessageType | None
    AckModeRetryDurationSecs: AckModeRetryDurationSecs | None


class WirelessMetadata(TypedDict, total=False):
    """WirelessMetadata object."""

    LoRaWAN: LoRaWANSendDataToDevice | None
    Sidewalk: SidewalkSendDataToDevice | None


class SendDataToWirelessDeviceRequest(ServiceRequest):
    Id: WirelessDeviceId
    TransmitMode: TransmitMode
    PayloadData: PayloadData
    WirelessMetadata: WirelessMetadata | None


class SendDataToWirelessDeviceResponse(TypedDict, total=False):
    MessageId: MessageId | None


class SidewalkSingleStartImportInfo(TypedDict, total=False):
    """Information about an import task created for an individual Sidewalk
    device.
    """

    SidewalkManufacturingSn: SidewalkManufacturingSn | None
    Positioning: SidewalkPositioning | None


class SidewalkStartImportInfo(TypedDict, total=False):
    """Information about an import task created for bulk provisioning."""

    DeviceCreationFile: DeviceCreationFile | None
    Role: Role | None
    Positioning: SidewalkPositioning | None


class SidewalkUpdateAccount(TypedDict, total=False):
    """Sidewalk update."""

    AppServerPrivateKey: AppServerPrivateKey | None


class SidewalkUpdateImportInfo(TypedDict, total=False):
    """Sidewalk object information for updating an import task."""

    DeviceCreationFile: DeviceCreationFile | None


class SidewalkUpdateWirelessDevice(TypedDict, total=False):
    """Sidewalk object for updating a wireless device."""

    Positioning: SidewalkPositioning | None


class StartBulkAssociateWirelessDeviceWithMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId
    QueryString: QueryString | None
    Tags: TagList | None


class StartBulkAssociateWirelessDeviceWithMulticastGroupResponse(TypedDict, total=False):
    pass


class StartBulkDisassociateWirelessDeviceFromMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId
    QueryString: QueryString | None
    Tags: TagList | None


class StartBulkDisassociateWirelessDeviceFromMulticastGroupResponse(TypedDict, total=False):
    pass


class StartFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    LoRaWAN: LoRaWANStartFuotaTask | None


class StartFuotaTaskResponse(TypedDict, total=False):
    pass


class StartMulticastGroupSessionRequest(ServiceRequest):
    Id: MulticastGroupId
    LoRaWAN: LoRaWANMulticastSession


class StartMulticastGroupSessionResponse(TypedDict, total=False):
    pass


class StartSingleWirelessDeviceImportTaskRequest(ServiceRequest):
    DestinationName: DestinationName
    ClientRequestToken: ClientRequestToken | None
    DeviceName: DeviceName | None
    Tags: TagList | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkSingleStartImportInfo


class StartSingleWirelessDeviceImportTaskResponse(TypedDict, total=False):
    Id: ImportTaskId | None
    Arn: ImportTaskArn | None


class StartWirelessDeviceImportTaskRequest(ServiceRequest):
    DestinationName: DestinationName
    ClientRequestToken: ClientRequestToken | None
    Tags: TagList | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkStartImportInfo


class StartWirelessDeviceImportTaskResponse(TypedDict, total=False):
    Id: ImportTaskId | None
    Arn: ImportTaskArn | None


TagKeyList = list[TagKey]


class TagResourceRequest(ServiceRequest):
    ResourceArn: AmazonResourceName
    Tags: TagList


class TagResourceResponse(TypedDict, total=False):
    pass


class TestWirelessDeviceRequest(ServiceRequest):
    Id: WirelessDeviceId


class TestWirelessDeviceResponse(TypedDict, total=False):
    Result: Result | None


class UntagResourceRequest(ServiceRequest):
    ResourceArn: AmazonResourceName
    TagKeys: TagKeyList


class UntagResourceResponse(TypedDict, total=False):
    pass


class UpdateDestinationRequest(ServiceRequest):
    Name: DestinationName
    ExpressionType: ExpressionType | None
    Expression: Expression | None
    Description: Description | None
    RoleArn: RoleArn | None


class UpdateDestinationResponse(TypedDict, total=False):
    pass


class UpdateEventConfigurationByResourceTypesRequest(ServiceRequest):
    DeviceRegistrationState: DeviceRegistrationStateResourceTypeEventConfiguration | None
    Proximity: ProximityResourceTypeEventConfiguration | None
    Join: JoinResourceTypeEventConfiguration | None
    ConnectionStatus: ConnectionStatusResourceTypeEventConfiguration | None
    MessageDeliveryStatus: MessageDeliveryStatusResourceTypeEventConfiguration | None


class UpdateEventConfigurationByResourceTypesResponse(TypedDict, total=False):
    pass


class UpdateFuotaTaskRequest(ServiceRequest):
    Id: FuotaTaskId
    Name: FuotaTaskName | None
    Description: Description | None
    LoRaWAN: LoRaWANFuotaTask | None
    FirmwareUpdateImage: FirmwareUpdateImage | None
    FirmwareUpdateRole: FirmwareUpdateRole | None
    RedundancyPercent: RedundancyPercent | None
    FragmentSizeBytes: FragmentSizeBytes | None
    FragmentIntervalMS: FragmentIntervalMS | None
    Descriptor: FileDescriptor | None


class UpdateFuotaTaskResponse(TypedDict, total=False):
    pass


class UpdateLogLevelsByResourceTypesRequest(ServiceRequest):
    DefaultLogLevel: LogLevel | None
    FuotaTaskLogOptions: FuotaTaskLogOptionList | None
    WirelessDeviceLogOptions: WirelessDeviceLogOptionList | None
    WirelessGatewayLogOptions: WirelessGatewayLogOptionList | None


class UpdateLogLevelsByResourceTypesResponse(TypedDict, total=False):
    pass


class UpdateMetricConfigurationRequest(ServiceRequest):
    SummaryMetric: SummaryMetricConfiguration | None


class UpdateMetricConfigurationResponse(TypedDict, total=False):
    pass


class UpdateMulticastGroupRequest(ServiceRequest):
    Id: MulticastGroupId
    Name: MulticastGroupName | None
    Description: Description | None
    LoRaWAN: LoRaWANMulticast | None


class UpdateMulticastGroupResponse(TypedDict, total=False):
    pass


class UpdateNetworkAnalyzerConfigurationRequest(ServiceRequest):
    ConfigurationName: NetworkAnalyzerConfigurationName
    TraceContent: TraceContent | None
    WirelessDevicesToAdd: WirelessDeviceList | None
    WirelessDevicesToRemove: WirelessDeviceList | None
    WirelessGatewaysToAdd: WirelessGatewayList | None
    WirelessGatewaysToRemove: WirelessGatewayList | None
    Description: Description | None
    MulticastGroupsToAdd: NetworkAnalyzerMulticastGroupList | None
    MulticastGroupsToRemove: NetworkAnalyzerMulticastGroupList | None


class UpdateNetworkAnalyzerConfigurationResponse(TypedDict, total=False):
    pass


class UpdatePartnerAccountRequest(ServiceRequest):
    Sidewalk: SidewalkUpdateAccount
    PartnerAccountId: PartnerAccountId
    PartnerType: PartnerType


class UpdatePartnerAccountResponse(TypedDict, total=False):
    pass


class UpdatePositionRequest(ServiceRequest):
    ResourceIdentifier: PositionResourceIdentifier
    ResourceType: PositionResourceType
    Position: PositionCoordinate


class UpdatePositionResponse(TypedDict, total=False):
    pass


class UpdateResourceEventConfigurationRequest(ServiceRequest):
    Identifier: Identifier
    IdentifierType: IdentifierType
    PartnerType: EventNotificationPartnerType | None
    DeviceRegistrationState: DeviceRegistrationStateEventConfiguration | None
    Proximity: ProximityEventConfiguration | None
    Join: JoinEventConfiguration | None
    ConnectionStatus: ConnectionStatusEventConfiguration | None
    MessageDeliveryStatus: MessageDeliveryStatusEventConfiguration | None


class UpdateResourceEventConfigurationResponse(TypedDict, total=False):
    pass


class UpdateResourcePositionRequest(ServiceRequest):
    GeoJsonPayload: IO[GeoJsonPayload] | None
    ResourceIdentifier: PositionResourceIdentifier
    ResourceType: PositionResourceType


class UpdateResourcePositionResponse(TypedDict, total=False):
    pass


class UpdateWirelessDeviceImportTaskRequest(ServiceRequest):
    Id: ImportTaskId
    Sidewalk: SidewalkUpdateImportInfo


class UpdateWirelessDeviceImportTaskResponse(TypedDict, total=False):
    pass


class UpdateWirelessDeviceRequest(ServiceRequest):
    Id: WirelessDeviceId
    DestinationName: DestinationName | None
    Name: WirelessDeviceName | None
    Description: Description | None
    LoRaWAN: LoRaWANUpdateDevice | None
    Positioning: PositioningConfigStatus | None
    Sidewalk: SidewalkUpdateWirelessDevice | None


class UpdateWirelessDeviceResponse(TypedDict, total=False):
    pass


class UpdateWirelessGatewayRequest(ServiceRequest):
    Id: WirelessGatewayId
    Name: WirelessGatewayName | None
    Description: Description | None
    JoinEuiFilters: JoinEuiFilters | None
    NetIdFilters: NetIdFilters | None
    MaxEirp: GatewayMaxEirp | None


class UpdateWirelessGatewayResponse(TypedDict, total=False):
    pass


class IotwirelessApi:
    service: str = "iotwireless"
    version: str = "2020-11-22"

    @handler("AssociateAwsAccountWithPartnerAccount")
    def associate_aws_account_with_partner_account(
        self,
        context: RequestContext,
        sidewalk: SidewalkAccountInfo,
        client_request_token: ClientRequestToken | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> AssociateAwsAccountWithPartnerAccountResponse:
        """Associates a partner account with your AWS account.

        :param sidewalk: The Sidewalk account credentials.
        :param client_request_token: Each resource must have a unique client request token.
        :param tags: The tags to attach to the specified resource.
        :returns: AssociateAwsAccountWithPartnerAccountResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises ConflictException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("AssociateMulticastGroupWithFuotaTask")
    def associate_multicast_group_with_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        multicast_group_id: MulticastGroupId,
        **kwargs,
    ) -> AssociateMulticastGroupWithFuotaTaskResponse:
        """Associate a multicast group with a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param multicast_group_id: The ID of the multicast group.
        :returns: AssociateMulticastGroupWithFuotaTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("AssociateWirelessDeviceWithFuotaTask")
    def associate_wireless_device_with_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        wireless_device_id: WirelessDeviceId,
        **kwargs,
    ) -> AssociateWirelessDeviceWithFuotaTaskResponse:
        """Associate a wireless device with a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param wireless_device_id: The ID of the wireless device.
        :returns: AssociateWirelessDeviceWithFuotaTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("AssociateWirelessDeviceWithMulticastGroup")
    def associate_wireless_device_with_multicast_group(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        wireless_device_id: WirelessDeviceId,
        **kwargs,
    ) -> AssociateWirelessDeviceWithMulticastGroupResponse:
        """Associates a wireless device with a multicast group.

        :param id: The ID of the multicast group.
        :param wireless_device_id: The ID of the wireless device.
        :returns: AssociateWirelessDeviceWithMulticastGroupResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("AssociateWirelessDeviceWithThing")
    def associate_wireless_device_with_thing(
        self, context: RequestContext, id: WirelessDeviceId, thing_arn: ThingArn, **kwargs
    ) -> AssociateWirelessDeviceWithThingResponse:
        """Associates a wireless device with a thing.

        :param id: The ID of the resource to update.
        :param thing_arn: The ARN of the thing to associate with the wireless device.
        :returns: AssociateWirelessDeviceWithThingResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("AssociateWirelessGatewayWithCertificate")
    def associate_wireless_gateway_with_certificate(
        self,
        context: RequestContext,
        id: WirelessGatewayId,
        iot_certificate_id: IotCertificateId,
        **kwargs,
    ) -> AssociateWirelessGatewayWithCertificateResponse:
        """Associates a wireless gateway with a certificate.

        :param id: The ID of the resource to update.
        :param iot_certificate_id: The ID of the certificate to associate with the wireless gateway.
        :returns: AssociateWirelessGatewayWithCertificateResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("AssociateWirelessGatewayWithThing")
    def associate_wireless_gateway_with_thing(
        self, context: RequestContext, id: WirelessGatewayId, thing_arn: ThingArn, **kwargs
    ) -> AssociateWirelessGatewayWithThingResponse:
        """Associates a wireless gateway with a thing.

        :param id: The ID of the resource to update.
        :param thing_arn: The ARN of the thing to associate with the wireless gateway.
        :returns: AssociateWirelessGatewayWithThingResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("CancelMulticastGroupSession")
    def cancel_multicast_group_session(
        self, context: RequestContext, id: MulticastGroupId, **kwargs
    ) -> CancelMulticastGroupSessionResponse:
        """Cancels an existing multicast group session.

        :param id: The ID of the multicast group.
        :returns: CancelMulticastGroupSessionResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateDestination")
    def create_destination(
        self,
        context: RequestContext,
        name: DestinationName,
        expression_type: ExpressionType,
        expression: Expression,
        role_arn: RoleArn,
        description: Description | None = None,
        tags: TagList | None = None,
        client_request_token: ClientRequestToken | None = None,
        **kwargs,
    ) -> CreateDestinationResponse:
        """Creates a new destination that maps a device message to an AWS IoT rule.

        :param name: The name of the new resource.
        :param expression_type: The type of value in ``Expression``.
        :param expression: The rule name or topic rule to send messages to.
        :param role_arn: The ARN of the IAM Role that authorizes the destination.
        :param description: The description of the new resource.
        :param tags: The tags to attach to the new destination.
        :param client_request_token: Each resource must have a unique client request token.
        :returns: CreateDestinationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateDeviceProfile")
    def create_device_profile(
        self,
        context: RequestContext,
        name: DeviceProfileName | None = None,
        lo_ra_wan: LoRaWANDeviceProfile | None = None,
        tags: TagList | None = None,
        client_request_token: ClientRequestToken | None = None,
        sidewalk: SidewalkCreateDeviceProfile | None = None,
        **kwargs,
    ) -> CreateDeviceProfileResponse:
        """Creates a new device profile.

        :param name: The name of the new resource.
        :param lo_ra_wan: The device profile information to use to create the device profile.
        :param tags: The tags to attach to the new device profile.
        :param client_request_token: Each resource must have a unique client request token.
        :param sidewalk: The Sidewalk-related information for creating the Sidewalk device
        profile.
        :returns: CreateDeviceProfileResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateFuotaTask")
    def create_fuota_task(
        self,
        context: RequestContext,
        firmware_update_image: FirmwareUpdateImage,
        firmware_update_role: FirmwareUpdateRole,
        name: FuotaTaskName | None = None,
        description: Description | None = None,
        client_request_token: ClientRequestToken | None = None,
        lo_ra_wan: LoRaWANFuotaTask | None = None,
        tags: TagList | None = None,
        redundancy_percent: RedundancyPercent | None = None,
        fragment_size_bytes: FragmentSizeBytes | None = None,
        fragment_interval_ms: FragmentIntervalMS | None = None,
        descriptor: FileDescriptor | None = None,
        **kwargs,
    ) -> CreateFuotaTaskResponse:
        """Creates a FUOTA task.

        :param firmware_update_image: The S3 URI points to a firmware update image that is to be used with a
        FUOTA task.
        :param firmware_update_role: The firmware update role that is to be used with a FUOTA task.
        :param name: The name of a FUOTA task.
        :param description: The description of the new resource.
        :param client_request_token: Each resource must have a unique client request token.
        :param lo_ra_wan: The LoRaWAN information used with a FUOTA task.
        :param tags: The tag to attach to the specified resource.
        :param redundancy_percent: The percentage of the added fragments that are redundant.
        :param fragment_size_bytes: The size of each fragment in bytes.
        :param fragment_interval_ms: The interval for sending fragments in milliseconds, rounded to the
        nearest second.
        :param descriptor: The descriptor is the metadata about the file that is transferred to the
        device using FUOTA, such as the software version.
        :returns: CreateFuotaTaskResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateMulticastGroup")
    def create_multicast_group(
        self,
        context: RequestContext,
        lo_ra_wan: LoRaWANMulticast,
        name: MulticastGroupName | None = None,
        description: Description | None = None,
        client_request_token: ClientRequestToken | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateMulticastGroupResponse:
        """Creates a multicast group.

        :param lo_ra_wan: The LoRaWAN information that is to be used with the multicast group.
        :param name: The name of the multicast group.
        :param description: The description of the multicast group.
        :param client_request_token: Each resource must have a unique client request token.
        :param tags: The tag to attach to the specified resource.
        :returns: CreateMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateNetworkAnalyzerConfiguration")
    def create_network_analyzer_configuration(
        self,
        context: RequestContext,
        name: NetworkAnalyzerConfigurationName,
        trace_content: TraceContent | None = None,
        wireless_devices: WirelessDeviceList | None = None,
        wireless_gateways: WirelessGatewayList | None = None,
        description: Description | None = None,
        tags: TagList | None = None,
        client_request_token: ClientRequestToken | None = None,
        multicast_groups: NetworkAnalyzerMulticastGroupList | None = None,
        **kwargs,
    ) -> CreateNetworkAnalyzerConfigurationResponse:
        """Creates a new network analyzer configuration.

        :param name: Name of the network analyzer configuration.
        :param trace_content: Trace content for your wireless devices, gateways, and multicast groups.
        :param wireless_devices: Wireless device resources to add to the network analyzer configuration.
        :param wireless_gateways: Wireless gateway resources to add to the network analyzer configuration.
        :param description: The description of the new resource.
        :param tags: The tag to attach to the specified resource.
        :param client_request_token: Each resource must have a unique client request token.
        :param multicast_groups: Multicast Group resources to add to the network analyzer configruation.
        :returns: CreateNetworkAnalyzerConfigurationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateServiceProfile")
    def create_service_profile(
        self,
        context: RequestContext,
        name: ServiceProfileName | None = None,
        lo_ra_wan: LoRaWANServiceProfile | None = None,
        tags: TagList | None = None,
        client_request_token: ClientRequestToken | None = None,
        **kwargs,
    ) -> CreateServiceProfileResponse:
        """Creates a new service profile.

        :param name: The name of the new resource.
        :param lo_ra_wan: The service profile information to use to create the service profile.
        :param tags: The tags to attach to the new service profile.
        :param client_request_token: Each resource must have a unique client request token.
        :returns: CreateServiceProfileResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateWirelessDevice", expand=False)
    def create_wireless_device(
        self, context: RequestContext, request: CreateWirelessDeviceRequest, **kwargs
    ) -> CreateWirelessDeviceResponse:
        """Provisions a wireless device.

        :param type: The wireless device type.
        :param destination_name: The name of the destination to assign to the new wireless device.
        :param name: The name of the new resource.
        :param description: The description of the new resource.
        :param client_request_token: Each resource must have a unique client request token.
        :param lo_ra_wan: The device configuration information to use to create the wireless
        device.
        :param tags: The tags to attach to the new wireless device.
        :param positioning: The integration status of the Device Location feature for LoRaWAN and
        Sidewalk devices.
        :param sidewalk: The device configuration information to use to create the Sidewalk
        device.
        :returns: CreateWirelessDeviceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateWirelessGateway")
    def create_wireless_gateway(
        self,
        context: RequestContext,
        lo_ra_wan: LoRaWANGateway,
        name: WirelessGatewayName | None = None,
        description: Description | None = None,
        tags: TagList | None = None,
        client_request_token: ClientRequestToken | None = None,
        **kwargs,
    ) -> CreateWirelessGatewayResponse:
        """Provisions a wireless gateway.

        When provisioning a wireless gateway, you might run into duplication
        errors for the following reasons.

        -  If you specify a ``GatewayEui`` value that already exists.

        -  If you used a ``ClientRequestToken`` with the same parameters within
           the last 10 minutes.

        To avoid this error, make sure that you use unique identifiers and
        parameters for each request within the specified time period.

        :param lo_ra_wan: The gateway configuration information to use to create the wireless
        gateway.
        :param name: The name of the new resource.
        :param description: The description of the new resource.
        :param tags: The tags to attach to the new wireless gateway.
        :param client_request_token: Each resource must have a unique client request token.
        :returns: CreateWirelessGatewayResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateWirelessGatewayTask")
    def create_wireless_gateway_task(
        self,
        context: RequestContext,
        id: WirelessGatewayId,
        wireless_gateway_task_definition_id: WirelessGatewayTaskDefinitionId,
        **kwargs,
    ) -> CreateWirelessGatewayTaskResponse:
        """Creates a task for a wireless gateway.

        :param id: The ID of the resource to update.
        :param wireless_gateway_task_definition_id: The ID of the WirelessGatewayTaskDefinition.
        :returns: CreateWirelessGatewayTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("CreateWirelessGatewayTaskDefinition")
    def create_wireless_gateway_task_definition(
        self,
        context: RequestContext,
        auto_create_tasks: AutoCreateTasks,
        name: WirelessGatewayTaskName | None = None,
        update: UpdateWirelessGatewayTaskCreate | None = None,
        client_request_token: ClientRequestToken | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> CreateWirelessGatewayTaskDefinitionResponse:
        """Creates a gateway task definition.

        :param auto_create_tasks: Whether to automatically create tasks using this task definition for all
        gateways with the specified current version.
        :param name: The name of the new resource.
        :param update: Information about the gateways to update.
        :param client_request_token: Each resource must have a unique client request token.
        :param tags: The tags to attach to the specified resource.
        :returns: CreateWirelessGatewayTaskDefinitionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteDestination")
    def delete_destination(
        self, context: RequestContext, name: DestinationName, **kwargs
    ) -> DeleteDestinationResponse:
        """Deletes a destination.

        :param name: The name of the resource to delete.
        :returns: DeleteDestinationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteDeviceProfile")
    def delete_device_profile(
        self, context: RequestContext, id: DeviceProfileId, **kwargs
    ) -> DeleteDeviceProfileResponse:
        """Deletes a device profile.

        :param id: The ID of the resource to delete.
        :returns: DeleteDeviceProfileResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteFuotaTask")
    def delete_fuota_task(
        self, context: RequestContext, id: FuotaTaskId, **kwargs
    ) -> DeleteFuotaTaskResponse:
        """Deletes a FUOTA task.

        :param id: The ID of a FUOTA task.
        :returns: DeleteFuotaTaskResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteMulticastGroup")
    def delete_multicast_group(
        self, context: RequestContext, id: MulticastGroupId, **kwargs
    ) -> DeleteMulticastGroupResponse:
        """Deletes a multicast group if it is not in use by a FUOTA task.

        :param id: The ID of the multicast group.
        :returns: DeleteMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteNetworkAnalyzerConfiguration")
    def delete_network_analyzer_configuration(
        self,
        context: RequestContext,
        configuration_name: NetworkAnalyzerConfigurationName,
        **kwargs,
    ) -> DeleteNetworkAnalyzerConfigurationResponse:
        """Deletes a network analyzer configuration.

        :param configuration_name: Name of the network analyzer configuration.
        :returns: DeleteNetworkAnalyzerConfigurationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteQueuedMessages")
    def delete_queued_messages(
        self,
        context: RequestContext,
        id: WirelessDeviceId,
        message_id: MessageId,
        wireless_device_type: WirelessDeviceType | None = None,
        **kwargs,
    ) -> DeleteQueuedMessagesResponse:
        """Remove queued messages from the downlink queue.

        :param id: The ID of a given wireless device for which downlink messages will be
        deleted.
        :param message_id: If message ID is ``"*"``, it cleares the entire downlink queue for a
        given device, specified by the wireless device ID.
        :param wireless_device_type: The wireless device type, which can be either Sidewalk or LoRaWAN.
        :returns: DeleteQueuedMessagesResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("DeleteServiceProfile")
    def delete_service_profile(
        self, context: RequestContext, id: ServiceProfileId, **kwargs
    ) -> DeleteServiceProfileResponse:
        """Deletes a service profile.

        :param id: The ID of the resource to delete.
        :returns: DeleteServiceProfileResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteWirelessDevice")
    def delete_wireless_device(
        self, context: RequestContext, id: WirelessDeviceId, **kwargs
    ) -> DeleteWirelessDeviceResponse:
        """Deletes a wireless device.

        :param id: The ID of the resource to delete.
        :returns: DeleteWirelessDeviceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteWirelessDeviceImportTask")
    def delete_wireless_device_import_task(
        self, context: RequestContext, id: ImportTaskId, **kwargs
    ) -> DeleteWirelessDeviceImportTaskResponse:
        """Delete an import task.

        :param id: The unique identifier of the import task to be deleted.
        :returns: DeleteWirelessDeviceImportTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteWirelessGateway")
    def delete_wireless_gateway(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> DeleteWirelessGatewayResponse:
        """Deletes a wireless gateway.

        When deleting a wireless gateway, you might run into duplication errors
        for the following reasons.

        -  If you specify a ``GatewayEui`` value that already exists.

        -  If you used a ``ClientRequestToken`` with the same parameters within
           the last 10 minutes.

        To avoid this error, make sure that you use unique identifiers and
        parameters for each request within the specified time period.

        :param id: The ID of the resource to delete.
        :returns: DeleteWirelessGatewayResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteWirelessGatewayTask")
    def delete_wireless_gateway_task(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> DeleteWirelessGatewayTaskResponse:
        """Deletes a wireless gateway task.

        :param id: The ID of the resource to delete.
        :returns: DeleteWirelessGatewayTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeleteWirelessGatewayTaskDefinition")
    def delete_wireless_gateway_task_definition(
        self, context: RequestContext, id: WirelessGatewayTaskDefinitionId, **kwargs
    ) -> DeleteWirelessGatewayTaskDefinitionResponse:
        """Deletes a wireless gateway task definition. Deleting this task
        definition does not affect tasks that are currently in progress.

        :param id: The ID of the resource to delete.
        :returns: DeleteWirelessGatewayTaskDefinitionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DeregisterWirelessDevice")
    def deregister_wireless_device(
        self,
        context: RequestContext,
        identifier: Identifier,
        wireless_device_type: WirelessDeviceType | None = None,
        **kwargs,
    ) -> DeregisterWirelessDeviceResponse:
        """Deregister a wireless device from AWS IoT Wireless.

        :param identifier: The identifier of the wireless device to deregister from AWS IoT
        Wireless.
        :param wireless_device_type: The type of wireless device to deregister from AWS IoT Wireless, which
        can be ``LoRaWAN`` or ``Sidewalk``.
        :returns: DeregisterWirelessDeviceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DisassociateAwsAccountFromPartnerAccount")
    def disassociate_aws_account_from_partner_account(
        self,
        context: RequestContext,
        partner_account_id: PartnerAccountId,
        partner_type: PartnerType,
        **kwargs,
    ) -> DisassociateAwsAccountFromPartnerAccountResponse:
        """Disassociates your AWS account from a partner account. If
        ``PartnerAccountId`` and ``PartnerType`` are ``null``, disassociates
        your AWS account from all partner accounts.

        :param partner_account_id: The partner account ID to disassociate from the AWS account.
        :param partner_type: The partner type.
        :returns: DisassociateAwsAccountFromPartnerAccountResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DisassociateMulticastGroupFromFuotaTask")
    def disassociate_multicast_group_from_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        multicast_group_id: MulticastGroupId,
        **kwargs,
    ) -> DisassociateMulticastGroupFromFuotaTaskResponse:
        """Disassociates a multicast group from a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param multicast_group_id: The ID of the multicast group.
        :returns: DisassociateMulticastGroupFromFuotaTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DisassociateWirelessDeviceFromFuotaTask")
    def disassociate_wireless_device_from_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        wireless_device_id: WirelessDeviceId,
        **kwargs,
    ) -> DisassociateWirelessDeviceFromFuotaTaskResponse:
        """Disassociates a wireless device from a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param wireless_device_id: The ID of the wireless device.
        :returns: DisassociateWirelessDeviceFromFuotaTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DisassociateWirelessDeviceFromMulticastGroup")
    def disassociate_wireless_device_from_multicast_group(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        wireless_device_id: WirelessDeviceId,
        **kwargs,
    ) -> DisassociateWirelessDeviceFromMulticastGroupResponse:
        """Disassociates a wireless device from a multicast group.

        :param id: The ID of the multicast group.
        :param wireless_device_id: The ID of the wireless device.
        :returns: DisassociateWirelessDeviceFromMulticastGroupResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DisassociateWirelessDeviceFromThing")
    def disassociate_wireless_device_from_thing(
        self, context: RequestContext, id: WirelessDeviceId, **kwargs
    ) -> DisassociateWirelessDeviceFromThingResponse:
        """Disassociates a wireless device from its currently associated thing.

        :param id: The ID of the resource to update.
        :returns: DisassociateWirelessDeviceFromThingResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("DisassociateWirelessGatewayFromCertificate")
    def disassociate_wireless_gateway_from_certificate(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> DisassociateWirelessGatewayFromCertificateResponse:
        """Disassociates a wireless gateway from its currently associated
        certificate.

        :param id: The ID of the resource to update.
        :returns: DisassociateWirelessGatewayFromCertificateResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("DisassociateWirelessGatewayFromThing")
    def disassociate_wireless_gateway_from_thing(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> DisassociateWirelessGatewayFromThingResponse:
        """Disassociates a wireless gateway from its currently associated thing.

        :param id: The ID of the resource to update.
        :returns: DisassociateWirelessGatewayFromThingResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetDestination")
    def get_destination(
        self, context: RequestContext, name: DestinationName, **kwargs
    ) -> GetDestinationResponse:
        """Gets information about a destination.

        :param name: The name of the resource to get.
        :returns: GetDestinationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetDeviceProfile")
    def get_device_profile(
        self, context: RequestContext, id: DeviceProfileId, **kwargs
    ) -> GetDeviceProfileResponse:
        """Gets information about a device profile.

        :param id: The ID of the resource to get.
        :returns: GetDeviceProfileResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetEventConfigurationByResourceTypes")
    def get_event_configuration_by_resource_types(
        self, context: RequestContext, **kwargs
    ) -> GetEventConfigurationByResourceTypesResponse:
        """Get the event configuration based on resource types.

        :returns: GetEventConfigurationByResourceTypesResponse
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetFuotaTask")
    def get_fuota_task(
        self, context: RequestContext, id: FuotaTaskId, **kwargs
    ) -> GetFuotaTaskResponse:
        """Gets information about a FUOTA task.

        :param id: The ID of a FUOTA task.
        :returns: GetFuotaTaskResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetLogLevelsByResourceTypes")
    def get_log_levels_by_resource_types(
        self, context: RequestContext, **kwargs
    ) -> GetLogLevelsByResourceTypesResponse:
        """Returns current default log levels or log levels by resource types.
        Based on the resource type, log levels can be returned for wireless
        device, wireless gateway, or FUOTA task log options.

        :returns: GetLogLevelsByResourceTypesResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetMetricConfiguration")
    def get_metric_configuration(
        self, context: RequestContext, **kwargs
    ) -> GetMetricConfigurationResponse:
        """Get the metric configuration status for this AWS account.

        :returns: GetMetricConfigurationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetMetrics")
    def get_metrics(
        self,
        context: RequestContext,
        summary_metric_queries: SummaryMetricQueries | None = None,
        **kwargs,
    ) -> GetMetricsResponse:
        """Get the summary metrics for this AWS account.

        :param summary_metric_queries: The list of queries to retrieve the summary metrics.
        :returns: GetMetricsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetMulticastGroup")
    def get_multicast_group(
        self, context: RequestContext, id: MulticastGroupId, **kwargs
    ) -> GetMulticastGroupResponse:
        """Gets information about a multicast group.

        :param id: The ID of the multicast group.
        :returns: GetMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetMulticastGroupSession")
    def get_multicast_group_session(
        self, context: RequestContext, id: MulticastGroupId, **kwargs
    ) -> GetMulticastGroupSessionResponse:
        """Gets information about a multicast group session.

        :param id: The ID of the multicast group.
        :returns: GetMulticastGroupSessionResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetNetworkAnalyzerConfiguration")
    def get_network_analyzer_configuration(
        self,
        context: RequestContext,
        configuration_name: NetworkAnalyzerConfigurationName,
        **kwargs,
    ) -> GetNetworkAnalyzerConfigurationResponse:
        """Get network analyzer configuration.

        :param configuration_name: Name of the network analyzer configuration.
        :returns: GetNetworkAnalyzerConfigurationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetPartnerAccount")
    def get_partner_account(
        self,
        context: RequestContext,
        partner_account_id: PartnerAccountId,
        partner_type: PartnerType,
        **kwargs,
    ) -> GetPartnerAccountResponse:
        """Gets information about a partner account. If ``PartnerAccountId`` and
        ``PartnerType`` are ``null``, returns all partner accounts.

        :param partner_account_id: The partner account ID to disassociate from the AWS account.
        :param partner_type: The partner type.
        :returns: GetPartnerAccountResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetPosition")
    def get_position(
        self,
        context: RequestContext,
        resource_identifier: PositionResourceIdentifier,
        resource_type: PositionResourceType,
        **kwargs,
    ) -> GetPositionResponse:
        """Get the position information for a given resource.

        This action is no longer supported. Calls to retrieve the position
        information should use the
        `GetResourcePosition <https://docs.aws.amazon.com/iot-wireless/latest/apireference/API_GetResourcePosition.html>`__
        API operation instead.

        :param resource_identifier: Resource identifier used to retrieve the position information.
        :param resource_type: Resource type of the resource for which position information is
        retrieved.
        :returns: GetPositionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetPositionConfiguration")
    def get_position_configuration(
        self,
        context: RequestContext,
        resource_identifier: PositionResourceIdentifier,
        resource_type: PositionResourceType,
        **kwargs,
    ) -> GetPositionConfigurationResponse:
        """Get position configuration for a given resource.

        This action is no longer supported. Calls to retrieve the position
        configuration should use the
        `GetResourcePosition <https://docs.aws.amazon.com/iot-wireless/latest/apireference/API_GetResourcePosition.html>`__
        API operation instead.

        :param resource_identifier: Resource identifier used in a position configuration.
        :param resource_type: Resource type of the resource for which position configuration is
        retrieved.
        :returns: GetPositionConfigurationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetPositionEstimate")
    def get_position_estimate(
        self,
        context: RequestContext,
        wi_fi_access_points: WiFiAccessPoints | None = None,
        cell_towers: CellTowers | None = None,
        ip: Ip | None = None,
        gnss: Gnss | None = None,
        timestamp: CreationDate | None = None,
        **kwargs,
    ) -> GetPositionEstimateResponse:
        """Get estimated position information as a payload in GeoJSON format. The
        payload measurement data is resolved using solvers that are provided by
        third-party vendors.

        :param wi_fi_access_points: Retrieves an estimated device position by resolving WLAN measurement
        data.
        :param cell_towers: Retrieves an estimated device position by resolving measurement data
        from cellular radio towers.
        :param ip: Retrieves an estimated device position by resolving the IP address
        information from the device.
        :param gnss: Retrieves an estimated device position by resolving the global
        navigation satellite system (GNSS) scan data.
        :param timestamp: Optional information that specifies the time when the position
        information will be resolved.
        :returns: GetPositionEstimateResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetResourceEventConfiguration")
    def get_resource_event_configuration(
        self,
        context: RequestContext,
        identifier: Identifier,
        identifier_type: IdentifierType,
        partner_type: EventNotificationPartnerType | None = None,
        **kwargs,
    ) -> GetResourceEventConfigurationResponse:
        """Get the event configuration for a particular resource identifier.

        :param identifier: Resource identifier to opt in for event messaging.
        :param identifier_type: Identifier type of the particular resource identifier for event
        configuration.
        :param partner_type: Partner type of the resource if the identifier type is
        ``PartnerAccountId``.
        :returns: GetResourceEventConfigurationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetResourceLogLevel")
    def get_resource_log_level(
        self,
        context: RequestContext,
        resource_identifier: ResourceIdentifier,
        resource_type: ResourceType,
        **kwargs,
    ) -> GetResourceLogLevelResponse:
        """Fetches the log-level override, if any, for a given resource ID and
        resource type..

        :param resource_identifier: The unique identifier of the resource, which can be the wireless gateway
        ID, the wireless device ID, or the FUOTA task ID.
        :param resource_type: The type of resource, which can be ``WirelessDevice``,
        ``WirelessGateway``, or ``FuotaTask``.
        :returns: GetResourceLogLevelResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("GetResourcePosition")
    def get_resource_position(
        self,
        context: RequestContext,
        resource_identifier: PositionResourceIdentifier,
        resource_type: PositionResourceType,
        **kwargs,
    ) -> GetResourcePositionResponse:
        """Get the position information for a given wireless device or a wireless
        gateway resource. The position information uses the `World Geodetic
        System
        (WGS84) <https://gisgeography.com/wgs84-world-geodetic-system/>`__.

        :param resource_identifier: The identifier of the resource for which position information is
        retrieved.
        :param resource_type: The type of resource for which position information is retrieved, which
        can be a wireless device or a wireless gateway.
        :returns: GetResourcePositionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("GetServiceEndpoint")
    def get_service_endpoint(
        self,
        context: RequestContext,
        service_type: WirelessGatewayServiceType | None = None,
        **kwargs,
    ) -> GetServiceEndpointResponse:
        """Gets the account-specific endpoint for Configuration and Update Server
        (CUPS) protocol or LoRaWAN Network Server (LNS) connections.

        :param service_type: The service type for which to get endpoint information about.
        :returns: GetServiceEndpointResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetServiceProfile")
    def get_service_profile(
        self, context: RequestContext, id: ServiceProfileId, **kwargs
    ) -> GetServiceProfileResponse:
        """Gets information about a service profile.

        :param id: The ID of the resource to get.
        :returns: GetServiceProfileResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessDevice")
    def get_wireless_device(
        self,
        context: RequestContext,
        identifier: Identifier,
        identifier_type: WirelessDeviceIdType,
        **kwargs,
    ) -> GetWirelessDeviceResponse:
        """Gets information about a wireless device.

        :param identifier: The identifier of the wireless device to get.
        :param identifier_type: The type of identifier used in ``identifier``.
        :returns: GetWirelessDeviceResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessDeviceImportTask")
    def get_wireless_device_import_task(
        self, context: RequestContext, id: ImportTaskId, **kwargs
    ) -> GetWirelessDeviceImportTaskResponse:
        """Get information about an import task and count of device onboarding
        summary information for the import task.

        :param id: The identifier of the import task for which information is requested.
        :returns: GetWirelessDeviceImportTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessDeviceStatistics")
    def get_wireless_device_statistics(
        self, context: RequestContext, wireless_device_id: WirelessDeviceId, **kwargs
    ) -> GetWirelessDeviceStatisticsResponse:
        """Gets operating information about a wireless device.

        :param wireless_device_id: The ID of the wireless device for which to get the data.
        :returns: GetWirelessDeviceStatisticsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessGateway")
    def get_wireless_gateway(
        self,
        context: RequestContext,
        identifier: Identifier,
        identifier_type: WirelessGatewayIdType,
        **kwargs,
    ) -> GetWirelessGatewayResponse:
        """Gets information about a wireless gateway.

        :param identifier: The identifier of the wireless gateway to get.
        :param identifier_type: The type of identifier used in ``identifier``.
        :returns: GetWirelessGatewayResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessGatewayCertificate")
    def get_wireless_gateway_certificate(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> GetWirelessGatewayCertificateResponse:
        """Gets the ID of the certificate that is currently associated with a
        wireless gateway.

        :param id: The ID of the resource to get.
        :returns: GetWirelessGatewayCertificateResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessGatewayFirmwareInformation")
    def get_wireless_gateway_firmware_information(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> GetWirelessGatewayFirmwareInformationResponse:
        """Gets the firmware version and other information about a wireless
        gateway.

        :param id: The ID of the resource to get.
        :returns: GetWirelessGatewayFirmwareInformationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessGatewayStatistics")
    def get_wireless_gateway_statistics(
        self, context: RequestContext, wireless_gateway_id: WirelessGatewayId, **kwargs
    ) -> GetWirelessGatewayStatisticsResponse:
        """Gets operating information about a wireless gateway.

        :param wireless_gateway_id: The ID of the wireless gateway for which to get the data.
        :returns: GetWirelessGatewayStatisticsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessGatewayTask")
    def get_wireless_gateway_task(
        self, context: RequestContext, id: WirelessGatewayId, **kwargs
    ) -> GetWirelessGatewayTaskResponse:
        """Gets information about a wireless gateway task.

        :param id: The ID of the resource to get.
        :returns: GetWirelessGatewayTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("GetWirelessGatewayTaskDefinition")
    def get_wireless_gateway_task_definition(
        self, context: RequestContext, id: WirelessGatewayTaskDefinitionId, **kwargs
    ) -> GetWirelessGatewayTaskDefinitionResponse:
        """Gets information about a wireless gateway task definition.

        :param id: The ID of the resource to get.
        :returns: GetWirelessGatewayTaskDefinitionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListDestinations")
    def list_destinations(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListDestinationsResponse:
        """Lists the destinations registered to your AWS account.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :returns: ListDestinationsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListDeviceProfiles")
    def list_device_profiles(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        device_profile_type: DeviceProfileType | None = None,
        **kwargs,
    ) -> ListDeviceProfilesResponse:
        """Lists the device profiles registered to your AWS account.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :param device_profile_type: A filter to list only device profiles that use this type, which can be
        ``LoRaWAN`` or ``Sidewalk``.
        :returns: ListDeviceProfilesResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListDevicesForWirelessDeviceImportTask")
    def list_devices_for_wireless_device_import_task(
        self,
        context: RequestContext,
        id: ImportTaskId,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        status: OnboardStatus | None = None,
        **kwargs,
    ) -> ListDevicesForWirelessDeviceImportTaskResponse:
        """List the Sidewalk devices in an import task and their onboarding status.

        :param id: The identifier of the import task for which wireless devices are listed.
        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise ``null`` to receive the first set of
        results.
        :param status: The status of the devices in the import task.
        :returns: ListDevicesForWirelessDeviceImportTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListEventConfigurations")
    def list_event_configurations(
        self,
        context: RequestContext,
        resource_type: EventNotificationResourceType,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListEventConfigurationsResponse:
        """List event configurations where at least one event topic has been
        enabled.

        :param resource_type: Resource type to filter event configurations.
        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :returns: ListEventConfigurationsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListFuotaTasks")
    def list_fuota_tasks(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListFuotaTasksResponse:
        """Lists the FUOTA tasks registered to your AWS account.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListFuotaTasksResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListMulticastGroups")
    def list_multicast_groups(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListMulticastGroupsResponse:
        """Lists the multicast groups registered to your AWS account.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListMulticastGroupsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListMulticastGroupsByFuotaTask")
    def list_multicast_groups_by_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListMulticastGroupsByFuotaTaskResponse:
        """List all multicast groups associated with a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListMulticastGroupsByFuotaTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListNetworkAnalyzerConfigurations")
    def list_network_analyzer_configurations(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListNetworkAnalyzerConfigurationsResponse:
        """Lists the network analyzer configurations.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :returns: ListNetworkAnalyzerConfigurationsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListPartnerAccounts")
    def list_partner_accounts(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListPartnerAccountsResponse:
        """Lists the partner accounts associated with your AWS account.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListPartnerAccountsResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListPositionConfigurations")
    def list_position_configurations(
        self,
        context: RequestContext,
        resource_type: PositionResourceType | None = None,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListPositionConfigurationsResponse:
        """List position configurations for a given resource, such as positioning
        solvers.

        This action is no longer supported. Calls to retrieve position
        information should use the
        `GetResourcePosition <https://docs.aws.amazon.com/iot-wireless/latest/apireference/API_GetResourcePosition.html>`__
        API operation instead.

        :param resource_type: Resource type for which position configurations are listed.
        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :returns: ListPositionConfigurationsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("ListQueuedMessages")
    def list_queued_messages(
        self,
        context: RequestContext,
        id: WirelessDeviceId,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        wireless_device_type: WirelessDeviceType | None = None,
        **kwargs,
    ) -> ListQueuedMessagesResponse:
        """List queued messages in the downlink queue.

        :param id: The ID of a given wireless device which the downlink message packets are
        being sent.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :param wireless_device_type: The wireless device type, whic can be either Sidewalk or LoRaWAN.
        :returns: ListQueuedMessagesResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListServiceProfiles")
    def list_service_profiles(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListServiceProfilesResponse:
        """Lists the service profiles registered to your AWS account.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListServiceProfilesResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListTagsForResource")
    def list_tags_for_resource(
        self, context: RequestContext, resource_arn: AmazonResourceName, **kwargs
    ) -> ListTagsForResourceResponse:
        """Lists the tags (metadata) you have assigned to the resource.

        :param resource_arn: The ARN of the resource for which you want to list tags.
        :returns: ListTagsForResourceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListWirelessDeviceImportTasks")
    def list_wireless_device_import_tasks(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        **kwargs,
    ) -> ListWirelessDeviceImportTasksResponse:
        """List of import tasks and summary information of onboarding status of
        devices in each import task.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise ``null`` to receive the first set of
        results.
        :returns: ListWirelessDeviceImportTasksResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListWirelessDevices")
    def list_wireless_devices(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        destination_name: DestinationName | None = None,
        device_profile_id: DeviceProfileId | None = None,
        service_profile_id: ServiceProfileId | None = None,
        wireless_device_type: WirelessDeviceType | None = None,
        fuota_task_id: FuotaTaskId | None = None,
        multicast_group_id: MulticastGroupId | None = None,
        **kwargs,
    ) -> ListWirelessDevicesResponse:
        """Lists the wireless devices registered to your AWS account.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param destination_name: A filter to list only the wireless devices that use as uplink
        destination.
        :param device_profile_id: A filter to list only the wireless devices that use this device profile.
        :param service_profile_id: A filter to list only the wireless devices that use this service
        profile.
        :param wireless_device_type: A filter to list only the wireless devices that use this wireless device
        type.
        :param fuota_task_id: The ID of a FUOTA task.
        :param multicast_group_id: The ID of the multicast group.
        :returns: ListWirelessDevicesResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("ListWirelessGatewayTaskDefinitions")
    def list_wireless_gateway_task_definitions(
        self,
        context: RequestContext,
        max_results: MaxResults | None = None,
        next_token: NextToken | None = None,
        task_definition_type: WirelessGatewayTaskDefinitionType | None = None,
        **kwargs,
    ) -> ListWirelessGatewayTaskDefinitionsResponse:
        """List the wireless gateway tasks definitions registered to your AWS
        account.

        :param max_results: The maximum number of results to return in this operation.
        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param task_definition_type: A filter to list only the wireless gateway task definitions that use
        this task definition type.
        :returns: ListWirelessGatewayTaskDefinitionsResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("ListWirelessGateways")
    def list_wireless_gateways(
        self,
        context: RequestContext,
        next_token: NextToken | None = None,
        max_results: MaxResults | None = None,
        **kwargs,
    ) -> ListWirelessGatewaysResponse:
        """Lists the wireless gateways registered to your AWS account.

        :param next_token: To retrieve the next set of results, the ``nextToken`` value from a
        previous response; otherwise **null** to receive the first set of
        results.
        :param max_results: The maximum number of results to return in this operation.
        :returns: ListWirelessGatewaysResponse
        :raises ValidationException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises AccessDeniedException:
        """
        raise NotImplementedError

    @handler("PutPositionConfiguration")
    def put_position_configuration(
        self,
        context: RequestContext,
        resource_identifier: PositionResourceIdentifier,
        resource_type: PositionResourceType,
        solvers: PositionSolverConfigurations | None = None,
        destination: DestinationName | None = None,
        **kwargs,
    ) -> PutPositionConfigurationResponse:
        """Put position configuration for a given resource.

        This action is no longer supported. Calls to update the position
        configuration should use the
        `UpdateResourcePosition <https://docs.aws.amazon.com/iot-wireless/latest/apireference/API_UpdateResourcePosition.html>`__
        API operation instead.

        :param resource_identifier: Resource identifier used to update the position configuration.
        :param resource_type: Resource type of the resource for which you want to update the position
        configuration.
        :param solvers: The positioning solvers used to update the position configuration of the
        resource.
        :param destination: The position data destination that describes the AWS IoT rule that
        processes the device's position data for use by AWS IoT Core for
        LoRaWAN.
        :returns: PutPositionConfigurationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("PutResourceLogLevel")
    def put_resource_log_level(
        self,
        context: RequestContext,
        resource_identifier: ResourceIdentifier,
        resource_type: ResourceType,
        log_level: LogLevel,
        **kwargs,
    ) -> PutResourceLogLevelResponse:
        """Sets the log-level override for a resource ID and resource type. A limit
        of 200 log level override can be set per account.

        :param resource_identifier: The unique identifier of the resource, which can be the wireless gateway
        ID, the wireless device ID, or the FUOTA task ID.
        :param resource_type: The type of resource, which can be ``WirelessDevice``,
        ``WirelessGateway``, or ``FuotaTask``.
        :param log_level: The log level for a log message.
        :returns: PutResourceLogLevelResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ResetAllResourceLogLevels")
    def reset_all_resource_log_levels(
        self, context: RequestContext, **kwargs
    ) -> ResetAllResourceLogLevelsResponse:
        """Removes the log-level overrides for all resources; wireless devices,
        wireless gateways, and FUOTA tasks.

        :returns: ResetAllResourceLogLevelsResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("ResetResourceLogLevel")
    def reset_resource_log_level(
        self,
        context: RequestContext,
        resource_identifier: ResourceIdentifier,
        resource_type: ResourceType,
        **kwargs,
    ) -> ResetResourceLogLevelResponse:
        """Removes the log-level override, if any, for a specific resource ID and
        resource type. It can be used for a wireless device, a wireless gateway,
        or a FUOTA task.

        :param resource_identifier: The unique identifier of the resource, which can be the wireless gateway
        ID, the wireless device ID, or the FUOTA task ID.
        :param resource_type: The type of resource, which can be ``WirelessDevice``,
        ``WirelessGateway``, or ``FuotaTask``.
        :returns: ResetResourceLogLevelResponse
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("SendDataToMulticastGroup")
    def send_data_to_multicast_group(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        payload_data: PayloadData,
        wireless_metadata: MulticastWirelessMetadata,
        **kwargs,
    ) -> SendDataToMulticastGroupResponse:
        """Sends the specified data to a multicast group.

        :param id: The ID of the multicast group.
        :param payload_data: The binary to be sent to the end device, encoded in base64.
        :param wireless_metadata: Wireless metadata that is to be sent to multicast group.
        :returns: SendDataToMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("SendDataToWirelessDevice")
    def send_data_to_wireless_device(
        self,
        context: RequestContext,
        id: WirelessDeviceId,
        transmit_mode: TransmitMode,
        payload_data: PayloadData,
        wireless_metadata: WirelessMetadata | None = None,
        **kwargs,
    ) -> SendDataToWirelessDeviceResponse:
        """Sends a decrypted application data frame to a device.

        :param id: The ID of the wireless device to receive the data.
        :param transmit_mode: The transmit mode to use to send data to the wireless device.
        :param payload_data: The binary to be sent to the end device, encoded in base64.
        :param wireless_metadata: Metadata about the message request.
        :returns: SendDataToWirelessDeviceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("StartBulkAssociateWirelessDeviceWithMulticastGroup")
    def start_bulk_associate_wireless_device_with_multicast_group(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        query_string: QueryString | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> StartBulkAssociateWirelessDeviceWithMulticastGroupResponse:
        """Starts a bulk association of all qualifying wireless devices with a
        multicast group.

        :param id: The ID of the multicast group.
        :param query_string: Query string used to search for wireless devices as part of the bulk
        associate and disassociate process.
        :param tags: The tag to attach to the specified resource.
        :returns: StartBulkAssociateWirelessDeviceWithMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StartBulkDisassociateWirelessDeviceFromMulticastGroup")
    def start_bulk_disassociate_wireless_device_from_multicast_group(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        query_string: QueryString | None = None,
        tags: TagList | None = None,
        **kwargs,
    ) -> StartBulkDisassociateWirelessDeviceFromMulticastGroupResponse:
        """Starts a bulk disassociatin of all qualifying wireless devices from a
        multicast group.

        :param id: The ID of the multicast group.
        :param query_string: Query string used to search for wireless devices as part of the bulk
        associate and disassociate process.
        :param tags: The tag to attach to the specified resource.
        :returns: StartBulkDisassociateWirelessDeviceFromMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StartFuotaTask")
    def start_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        lo_ra_wan: LoRaWANStartFuotaTask | None = None,
        **kwargs,
    ) -> StartFuotaTaskResponse:
        """Starts a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param lo_ra_wan: The LoRaWAN information used to start a FUOTA task.
        :returns: StartFuotaTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("StartMulticastGroupSession")
    def start_multicast_group_session(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        lo_ra_wan: LoRaWANMulticastSession,
        **kwargs,
    ) -> StartMulticastGroupSessionResponse:
        """Starts a multicast group session.

        :param id: The ID of the multicast group.
        :param lo_ra_wan: The LoRaWAN information used with the multicast session.
        :returns: StartMulticastGroupSessionResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StartSingleWirelessDeviceImportTask")
    def start_single_wireless_device_import_task(
        self,
        context: RequestContext,
        destination_name: DestinationName,
        sidewalk: SidewalkSingleStartImportInfo,
        client_request_token: ClientRequestToken | None = None,
        device_name: DeviceName | None = None,
        tags: TagList | None = None,
        positioning: PositioningConfigStatus | None = None,
        **kwargs,
    ) -> StartSingleWirelessDeviceImportTaskResponse:
        """Start import task for a single wireless device.

        :param destination_name: The name of the Sidewalk destination that describes the IoT rule to
        route messages from the device in the import task that will be onboarded
        to AWS IoT Wireless.
        :param sidewalk: The Sidewalk-related parameters for importing a single wireless device.
        :param client_request_token: Each resource must have a unique client request token.
        :param device_name: The name of the wireless device for which an import task is being
        started.
        :param tags: The tag to attach to the specified resource.
        :param positioning: The integration status of the Device Location feature for Sidewalk
        devices.
        :returns: StartSingleWirelessDeviceImportTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("StartWirelessDeviceImportTask")
    def start_wireless_device_import_task(
        self,
        context: RequestContext,
        destination_name: DestinationName,
        sidewalk: SidewalkStartImportInfo,
        client_request_token: ClientRequestToken | None = None,
        tags: TagList | None = None,
        positioning: PositioningConfigStatus | None = None,
        **kwargs,
    ) -> StartWirelessDeviceImportTaskResponse:
        """Start import task for provisioning Sidewalk devices in bulk using an S3
        CSV file.

        :param destination_name: The name of the Sidewalk destination that describes the IoT rule to
        route messages from the devices in the import task that are onboarded to
        AWS IoT Wireless.
        :param sidewalk: The Sidewalk-related parameters for importing wireless devices that need
        to be provisioned in bulk.
        :param client_request_token: Each resource must have a unique client request token.
        :param tags: The tag to attach to the specified resource.
        :param positioning: The integration status of the Device Location feature for Sidewalk
        devices.
        :returns: StartWirelessDeviceImportTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("TagResource")
    def tag_resource(
        self, context: RequestContext, resource_arn: AmazonResourceName, tags: TagList, **kwargs
    ) -> TagResourceResponse:
        """Adds a tag to a resource.

        :param resource_arn: The ARN of the resource to add tags to.
        :param tags: Adds to or modifies the tags of the given resource.
        :returns: TagResourceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        :raises TooManyTagsException:
        """
        raise NotImplementedError

    @handler("TestWirelessDevice")
    def test_wireless_device(
        self, context: RequestContext, id: WirelessDeviceId, **kwargs
    ) -> TestWirelessDeviceResponse:
        """Simulates a provisioned device by sending an uplink data payload of
        ``Hello``.

        :param id: The ID of the wireless device to test.
        :returns: TestWirelessDeviceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UntagResource")
    def untag_resource(
        self,
        context: RequestContext,
        resource_arn: AmazonResourceName,
        tag_keys: TagKeyList,
        **kwargs,
    ) -> UntagResourceResponse:
        """Removes one or more tags from a resource.

        :param resource_arn: The ARN of the resource to remove tags from.
        :param tag_keys: A list of the keys of the tags to remove from the resource.
        :returns: UntagResourceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateDestination")
    def update_destination(
        self,
        context: RequestContext,
        name: DestinationName,
        expression_type: ExpressionType | None = None,
        expression: Expression | None = None,
        description: Description | None = None,
        role_arn: RoleArn | None = None,
        **kwargs,
    ) -> UpdateDestinationResponse:
        """Updates properties of a destination.

        :param name: The new name of the resource.
        :param expression_type: The type of value in ``Expression``.
        :param expression: The new rule name or topic rule to send messages to.
        :param description: A new description of the resource.
        :param role_arn: The ARN of the IAM Role that authorizes the destination.
        :returns: UpdateDestinationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateEventConfigurationByResourceTypes")
    def update_event_configuration_by_resource_types(
        self,
        context: RequestContext,
        device_registration_state: DeviceRegistrationStateResourceTypeEventConfiguration
        | None = None,
        proximity: ProximityResourceTypeEventConfiguration | None = None,
        join: JoinResourceTypeEventConfiguration | None = None,
        connection_status: ConnectionStatusResourceTypeEventConfiguration | None = None,
        message_delivery_status: MessageDeliveryStatusResourceTypeEventConfiguration | None = None,
        **kwargs,
    ) -> UpdateEventConfigurationByResourceTypesResponse:
        """Update the event configuration based on resource types.

        :param device_registration_state: Device registration state resource type event configuration object for
        enabling and disabling wireless gateway topic.
        :param proximity: Proximity resource type event configuration object for enabling and
        disabling wireless gateway topic.
        :param join: Join resource type event configuration object for enabling and disabling
        wireless device topic.
        :param connection_status: Connection status resource type event configuration object for enabling
        and disabling wireless gateway topic.
        :param message_delivery_status: Message delivery status resource type event configuration object for
        enabling and disabling wireless device topic.
        :returns: UpdateEventConfigurationByResourceTypesResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateFuotaTask")
    def update_fuota_task(
        self,
        context: RequestContext,
        id: FuotaTaskId,
        name: FuotaTaskName | None = None,
        description: Description | None = None,
        lo_ra_wan: LoRaWANFuotaTask | None = None,
        firmware_update_image: FirmwareUpdateImage | None = None,
        firmware_update_role: FirmwareUpdateRole | None = None,
        redundancy_percent: RedundancyPercent | None = None,
        fragment_size_bytes: FragmentSizeBytes | None = None,
        fragment_interval_ms: FragmentIntervalMS | None = None,
        descriptor: FileDescriptor | None = None,
        **kwargs,
    ) -> UpdateFuotaTaskResponse:
        """Updates properties of a FUOTA task.

        :param id: The ID of a FUOTA task.
        :param name: The name of a FUOTA task.
        :param description: The description of the new resource.
        :param lo_ra_wan: The LoRaWAN information used with a FUOTA task.
        :param firmware_update_image: The S3 URI points to a firmware update image that is to be used with a
        FUOTA task.
        :param firmware_update_role: The firmware update role that is to be used with a FUOTA task.
        :param redundancy_percent: The percentage of the added fragments that are redundant.
        :param fragment_size_bytes: The size of each fragment in bytes.
        :param fragment_interval_ms: The interval for sending fragments in milliseconds, rounded to the
        nearest second.
        :param descriptor: The descriptor is the metadata about the file that is transferred to the
        device using FUOTA, such as the software version.
        :returns: UpdateFuotaTaskResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateLogLevelsByResourceTypes")
    def update_log_levels_by_resource_types(
        self,
        context: RequestContext,
        default_log_level: LogLevel | None = None,
        fuota_task_log_options: FuotaTaskLogOptionList | None = None,
        wireless_device_log_options: WirelessDeviceLogOptionList | None = None,
        wireless_gateway_log_options: WirelessGatewayLogOptionList | None = None,
        **kwargs,
    ) -> UpdateLogLevelsByResourceTypesResponse:
        """Set default log level, or log levels by resource types. This can be for
        wireless device, wireless gateway, or FUOTA task log options, and is
        used to control the log messages that'll be displayed in CloudWatch.

        :param default_log_level: The log level for a log message.
        :param fuota_task_log_options: The list of FUOTA task log options.
        :param wireless_device_log_options: The list of wireless device log options.
        :param wireless_gateway_log_options: The list of wireless gateway log options.
        :returns: UpdateLogLevelsByResourceTypesResponse
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises ValidationException:
        """
        raise NotImplementedError

    @handler("UpdateMetricConfiguration")
    def update_metric_configuration(
        self,
        context: RequestContext,
        summary_metric: SummaryMetricConfiguration | None = None,
        **kwargs,
    ) -> UpdateMetricConfigurationResponse:
        """Update the summary metric configuration.

        :param summary_metric: The value to be used to set summary metric configuration.
        :returns: UpdateMetricConfigurationResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateMulticastGroup")
    def update_multicast_group(
        self,
        context: RequestContext,
        id: MulticastGroupId,
        name: MulticastGroupName | None = None,
        description: Description | None = None,
        lo_ra_wan: LoRaWANMulticast | None = None,
        **kwargs,
    ) -> UpdateMulticastGroupResponse:
        """Updates properties of a multicast group session.

        :param id: The ID of the multicast group.
        :param name: The name of the multicast group.
        :param description: The description of the new resource.
        :param lo_ra_wan: The LoRaWAN information that is to be used with the multicast group.
        :returns: UpdateMulticastGroupResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateNetworkAnalyzerConfiguration")
    def update_network_analyzer_configuration(
        self,
        context: RequestContext,
        configuration_name: NetworkAnalyzerConfigurationName,
        trace_content: TraceContent | None = None,
        wireless_devices_to_add: WirelessDeviceList | None = None,
        wireless_devices_to_remove: WirelessDeviceList | None = None,
        wireless_gateways_to_add: WirelessGatewayList | None = None,
        wireless_gateways_to_remove: WirelessGatewayList | None = None,
        description: Description | None = None,
        multicast_groups_to_add: NetworkAnalyzerMulticastGroupList | None = None,
        multicast_groups_to_remove: NetworkAnalyzerMulticastGroupList | None = None,
        **kwargs,
    ) -> UpdateNetworkAnalyzerConfigurationResponse:
        """Update network analyzer configuration.

        :param configuration_name: Name of the network analyzer configuration.
        :param trace_content: Trace content for your wireless devices, gateways, and multicast groups.
        :param wireless_devices_to_add: Wireless device resources to add to the network analyzer configuration.
        :param wireless_devices_to_remove: Wireless device resources to remove from the network analyzer
        configuration.
        :param wireless_gateways_to_add: Wireless gateway resources to add to the network analyzer configuration.
        :param wireless_gateways_to_remove: Wireless gateway resources to remove from the network analyzer
        configuration.
        :param description: The description of the new resource.
        :param multicast_groups_to_add: Multicast group resources to add to the network analyzer configuration.
        :param multicast_groups_to_remove: Multicast group resources to remove from the network analyzer
        configuration.
        :returns: UpdateNetworkAnalyzerConfigurationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdatePartnerAccount")
    def update_partner_account(
        self,
        context: RequestContext,
        sidewalk: SidewalkUpdateAccount,
        partner_account_id: PartnerAccountId,
        partner_type: PartnerType,
        **kwargs,
    ) -> UpdatePartnerAccountResponse:
        """Updates properties of a partner account.

        :param sidewalk: The Sidewalk account credentials.
        :param partner_account_id: The ID of the partner account to update.
        :param partner_type: The partner type.
        :returns: UpdatePartnerAccountResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdatePosition")
    def update_position(
        self,
        context: RequestContext,
        resource_identifier: PositionResourceIdentifier,
        resource_type: PositionResourceType,
        position: PositionCoordinate,
        **kwargs,
    ) -> UpdatePositionResponse:
        """Update the position information of a resource.

        This action is no longer supported. Calls to update the position
        information should use the
        `UpdateResourcePosition <https://docs.aws.amazon.com/iot-wireless/latest/apireference/API_UpdateResourcePosition.html>`__
        API operation instead.

        :param resource_identifier: Resource identifier of the resource for which position is updated.
        :param resource_type: Resource type of the resource for which position is updated.
        :param position: The position information of the resource.
        :returns: UpdatePositionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateResourceEventConfiguration")
    def update_resource_event_configuration(
        self,
        context: RequestContext,
        identifier: Identifier,
        identifier_type: IdentifierType,
        partner_type: EventNotificationPartnerType | None = None,
        device_registration_state: DeviceRegistrationStateEventConfiguration | None = None,
        proximity: ProximityEventConfiguration | None = None,
        join: JoinEventConfiguration | None = None,
        connection_status: ConnectionStatusEventConfiguration | None = None,
        message_delivery_status: MessageDeliveryStatusEventConfiguration | None = None,
        **kwargs,
    ) -> UpdateResourceEventConfigurationResponse:
        """Update the event configuration for a particular resource identifier.

        :param identifier: Resource identifier to opt in for event messaging.
        :param identifier_type: Identifier type of the particular resource identifier for event
        configuration.
        :param partner_type: Partner type of the resource if the identifier type is
        ``PartnerAccountId``.
        :param device_registration_state: Event configuration for the device registration state event.
        :param proximity: Event configuration for the proximity event.
        :param join: Event configuration for the join event.
        :param connection_status: Event configuration for the connection status event.
        :param message_delivery_status: Event configuration for the message delivery status event.
        :returns: UpdateResourceEventConfigurationResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ConflictException:
        :raises ThrottlingException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateResourcePosition")
    def update_resource_position(
        self,
        context: RequestContext,
        resource_identifier: PositionResourceIdentifier,
        resource_type: PositionResourceType,
        geo_json_payload: IO[GeoJsonPayload] | None = None,
        **kwargs,
    ) -> UpdateResourcePositionResponse:
        """Update the position information of a given wireless device or a wireless
        gateway resource. The position coordinates are based on the `World
        Geodetic System
        (WGS84) <https://gisgeography.com/wgs84-world-geodetic-system/>`__.

        :param resource_identifier: The identifier of the resource for which position information is
        updated.
        :param resource_type: The type of resource for which position information is updated, which
        can be a wireless device or a wireless gateway.
        :param geo_json_payload: The position information of the resource, displayed as a JSON payload.
        :returns: UpdateResourcePositionResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises ThrottlingException:
        :raises InternalServerException:
        """
        raise NotImplementedError

    @handler("UpdateWirelessDevice")
    def update_wireless_device(
        self,
        context: RequestContext,
        id: WirelessDeviceId,
        destination_name: DestinationName | None = None,
        name: WirelessDeviceName | None = None,
        description: Description | None = None,
        lo_ra_wan: LoRaWANUpdateDevice | None = None,
        positioning: PositioningConfigStatus | None = None,
        sidewalk: SidewalkUpdateWirelessDevice | None = None,
        **kwargs,
    ) -> UpdateWirelessDeviceResponse:
        """Updates properties of a wireless device.

        :param id: The ID of the resource to update.
        :param destination_name: The name of the new destination for the device.
        :param name: The new name of the resource.
        :param description: A new description of the resource.
        :param lo_ra_wan: The updated wireless device's configuration.
        :param positioning: The integration status of the Device Location feature for LoRaWAN and
        Sidewalk devices.
        :param sidewalk: The updated sidewalk properties.
        :returns: UpdateWirelessDeviceResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateWirelessDeviceImportTask")
    def update_wireless_device_import_task(
        self,
        context: RequestContext,
        id: ImportTaskId,
        sidewalk: SidewalkUpdateImportInfo,
        **kwargs,
    ) -> UpdateWirelessDeviceImportTaskResponse:
        """Update an import task to add more devices to the task.

        :param id: The identifier of the import task to be updated.
        :param sidewalk: The Sidewalk-related parameters of the import task to be updated.
        :returns: UpdateWirelessDeviceImportTaskResponse
        :raises ValidationException:
        :raises AccessDeniedException:
        :raises ResourceNotFoundException:
        :raises InternalServerException:
        :raises ConflictException:
        :raises ThrottlingException:
        """
        raise NotImplementedError

    @handler("UpdateWirelessGateway")
    def update_wireless_gateway(
        self,
        context: RequestContext,
        id: WirelessGatewayId,
        name: WirelessGatewayName | None = None,
        description: Description | None = None,
        join_eui_filters: JoinEuiFilters | None = None,
        net_id_filters: NetIdFilters | None = None,
        max_eirp: GatewayMaxEirp | None = None,
        **kwargs,
    ) -> UpdateWirelessGatewayResponse:
        """Updates properties of a wireless gateway.

        :param id: The ID of the resource to update.
        :param name: The new name of the resource.
        :param description: A new description of the resource.
        :param join_eui_filters: A list of JoinEuiRange used by LoRa gateways to filter LoRa frames.
        :param net_id_filters: A list of NetId values that are used by LoRa gateways to filter the
        uplink frames.
        :param max_eirp: The MaxEIRP value.
        :returns: UpdateWirelessGatewayResponse
        :raises ValidationException:
        :raises ResourceNotFoundException:
        :raises AccessDeniedException:
        :raises InternalServerException:
        :raises ThrottlingException:
        """
        raise NotImplementedError
