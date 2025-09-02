from enum import IntEnum


class ControlType(IntEnum):
    """
    The control type is an identifier for control commands. These are documented in docs/PROTOCOL.md on
    the bluenet github repository.
    """
    SETUP                            = 0
    FACTORY_RESET                    = 1
    GET_STATE                        = 2
    SET_STATE                        = 3
    GET_BOOTLOADER_VERSION           = 4
    GET_UICR_DATA                    = 5
    SET_IBEACON_CONFIG_ID            = 6
    RESET                            = 10
    GOTO_DFU                         = 11
    NO_OPERATION                     = 12
    DISCONNECT                       = 13
    SWITCH                           = 20
    MULTISWITCH                      = 21
    PWM                              = 22
    RELAY                            = 23
    SET_TIME                         = 30
    SET_TX                           = 31
    RESET_ERRORS                     = 32
    MESH_COMMAND                     = 33
    SET_SUN_TIME                     = 34
    RESET_RSSI_BETWEEN_STONES        = 36
    ALLOW_DIMMING                    = 40
    LOCK_SWITCH                      = 41
    UART_MESSAGE                     = 50
    SAVE_BEHAVIOUR                   = 60
    REPLACE_BEHAVIOUR                = 61
    REMOVE_BEHAVIOUR                 = 62
    GET_BEHAVIOUR                    = 63
    GET_BEHAVIOUR_INDICES            = 64
    BEHAVIOUR_HANDLER_SETTINGS       = 65
    GET_BEHAVIOUR_DEBUG              = 69
    REGISTER_TRACKED_DEVICE          = 70
    TRACKED_DEVICE_HEARTBEAT         = 71
    GET_UPTIME                       = 80
    GET_ADC_RESTARTS                 = 81
    GET_SWITCH_HISTORY               = 82
    GET_POWER_SAMPLES                = 83
    GET_MIN_SCHEDULER_FREE           = 84
    GET_LAST_RESET_REASON            = 85
    GET_GPREGRET                     = 86
    GET_ADC_CHANNEL_SWAPS            = 87
    GET_RAM_STATS                    = 88
    MICROAPP_GET_INFO                = 90
    MICROAPP_UPLOAD                  = 91
    MICROAPP_VALIDATE                = 92
    MICROAPP_REMOVE                  = 93
    MICROAPP_ENABLE                  = 94
    MICROAPP_DISABLE                 = 95
    MICROAPP_MESSAGE                 = 96
    ASSET_FILTER_UPLOAD              = 110
    ASSET_FILTER_REMOVE              = 111
    ASSET_FILTER_COMMIT_CHANGES      = 112
    ASSET_FILTER_GET_SUMMARIES       = 113


    UNSPECIFIED                = 65535

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class StateType(IntEnum):
    UNKNOWN                                = 0
    PWM_PERIOD                             = 5
    IBEACON_MAJOR                          = 6
    IBEACON_MINOR                          = 7
    IBEACON_UUID                           = 8
    IBEACON_TX_POWER                       = 9
    WIFI_SETTINGS                          = 10
    TX_POWER                               = 11
    ADVERTISEMENT_INTERVAL                 = 12
    PASSKEY                                = 13
    MIN_ENV_TEMP                           = 14
    MAX_ENV_TEMP                           = 15
    SCAN_DURATION                          = 16
    SCAN_SEND_DELAY                        = 17
    SCAN_BREAK_DURATION                    = 18
    BOOT_DELAY                             = 19
    MAX_CHIP_TEMP                          = 20
    SCAN_FILTER                            = 21
    SCAN_FILTER_FRACTION                   = 22
    CURRENT_LIMIT                          = 23
    MESH_ENABLED                           = 24
    ENCRYPTION_ENABLED                     = 25
    IBEACON_ENABLED                        = 26
    SCANNER_ENABLED                        = 27
    CONTINUOUS_POWER_MEASUREMENT_ENABLED   = 28
    TRACKER_ENABLED                        = 29
    ADC_SAMPLE_RATE                        = 30
    POWER_SAMPLE_BURST_INTERVAL            = 31
    POWER_SAMPLE_CONTINUOUS_INTERVAL       = 32
    POWER_SAMPLE_CONTINUOUS_NUMBER_SAMPLES = 33
    CROWNSTONE_IDENTIFIER                  = 34
    ADMIN_ENCRYPTION_KEY                   = 35
    MEMBER_ENCRYPTION_KEY                  = 36
    GUEST_ENCRYPTION_KEY                   = 37
    DEFAULT_ON                             = 38
    SCAN_INTERVAL                          = 39
    SCAN_WINDOW                            = 40
    RELAY_HIGH_DURATION                    = 41
    LOW_TX_POWER                           = 42
    VOLTAGE_MULTIPLIER                     = 43
    CURRENT_MULITPLIER                     = 44
    VOLTAGE_ZERO                           = 45
    CURRENT_ZERO                           = 46
    POWER_ZERO                             = 47
    POWER_AVERAGE_WINDOW                   = 48
    MESH_ACCESS_ADDRESS                    = 49
    CURRENT_CONSUMPTION_THRESHOLD          = 50
    CURRENT_CONSUMPTION_THRESHOLD_DIMMER   = 51
    DIMMER_TEMP_UP_VOLTAGE                 = 52
    DIMMER_TEMP_DOWN_VOLTAGE               = 53
    PWM_ALLOWED                            = 54
    SWITCH_LOCKED                          = 55
    SWITCHCRAFT_ENABLED                    = 56
    SWITCHCRAFT_THRESHOLD                  = 57
    MESH_CHANNEL                           = 58
    UART_ENABLED                           = 59
    DEVICE_NAME                            = 60
    SERVICE_DATA_KEY                       = 61
    MESH_DEVICE_KEY                        = 62
    MESH_APPLICATION_KEY                   = 63
    MESH_NETWORK_KEY                       = 64
    LOCALIZATION_KEY                       = 65
    START_DIMMER_ON_ZERO_CROSSING          = 66
    TAP_TO_TOGGLE_ENABLED                  = 67
    TAP_TO_TOGGLE_RSSI_THRESHOLD_OFFSET    = 68
    BEHAVIOUR_RULE                         = 69
    TWILIGHT_RULE                          = 70
    EXTENDED_BEHAVIOUR_RULE                = 71

    RESET_COUNTER                          = 128
    SWITCH_STATE                           = 129
    ACCUMULATED_ENERGY                     = 130
    POWER_USAGE                            = 131
    TRACKED_DEVICES                        = 132
    SCHEDULE                               = 133
    OPERATION_MODE                         = 134
    TEMPERATURE                            = 135
    TIME                                   = 136
    ERROR_BITMASK                          = 139
    SUNTIMES                               = 149
    BEHAVIOUR_SETTINGS                     = 150

    MESH_IV_INDEX                          = 151
    MESH_SEQ_NUMBER                        = 152
    SOFT_ON_SPEED                          = 156
    HUB_MODE                               = 157
    UART_KEY                               = 158

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

class OpCode(IntEnum):
    READ                       = 0
    WRITE                      = 1
    NOTIFY                     = 2


class DeviceType(IntEnum):
    UNDEFINED                  = 0
    PLUG                       = 1
    GUIDESTONE                 = 2
    BUILTIN                    = 3
    CROWNSTONE_USB             = 4
    BUILTIN_ONE                = 5
    PLUG_ONE                   = 6
    HUB                        = 7

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class ResultValue(IntEnum):
    SUCCESS                    = 0      # Completed successfully.
    WAIT_FOR_SUCCESS           = 1      # Command is successful so far, but you need to wait for SUCCESS.
    SUCCESS_NO_CHANGE          = 2      # Completed successfully, but nothing changed.
    BUFFER_UNASSIGNED          = 16     # No buffer was assigned for the command.
    BUFFER_LOCKED              = 17     # Buffer is locked, failed queue command.
    BUFFER_TO_SMALL            = 18
    NOT_ALIGNED                = 19     # Buffer is not aligned.
    WRONG_PAYLOAD_LENGTH       = 32     # Wrong payload length provided.
    WRONG_PARAMETER            = 33     # Wrong parameter provided.
    INVALID_MESSAGE            = 34     # invalid message provided.
    UNKNOWN_OP_CODE            = 35     # Unknown operation code provided.
    UNKNOWN_TYPE               = 36     # Unknown type provided.
    NOT_FOUND                  = 37     # The thing you were looking for was not found.
    NO_SPACE                   = 38
    BUSY                       = 39
    ERR_WRONG_STATE            = 40     # The crownstone is in a wrong state.
    ERR_ALREADY_EXISTS         = 41     # Item already exists.
    ERR_TIMEOUT                = 42     # Operation timed out.
    ERR_CANCELED               = 43     # Operation was canceled.
    ERR_PROTOCOL_UNSUPPORTED   = 44     # The protocol is not supported.
    MISMATCH                   = 45     # There is a mismatch, usually in CRC/checksum/hash.
    NO_ACCESS                  = 48     # Invalid access for this command.
    ERR_UNSAFE                 = 49     # Invalid access for this command.
    NOT_AVAILABLE              = 64     # Command currently not available.
    NOT_IMPLEMENTED            = 65     # Command not implemented (not yet or not anymore).
    NOT_INITIALIZED            = 67     # Something must first be initialized.
    ERR_NOT_STARTED            = 68     # Something must first be started.
    WRITE_DISABLED             = 80     # Write is disabled for given type.
    ERR_WRITE_NOT_ALLOWED      = 81     # Direct write is not allowed for this type, use command instead.
    READ_FAILED                = 82     # Failed to read.
    ADC_INVALID_CHANNEL        = 96     # Invalid adc input channel selected.
    ERR_EVENT_UNHANDLED        = 112    # The event or command was not handled.
    UNSPECIFIED                = 65535

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)


class ProcessType(IntEnum):
    CONTINUE                   = 0
    FINISHED                   = 1
    ABORT_ERROR                = 2


class BroadcastTypes(IntEnum):
    NO_OP                      = 0
    MULTI_SWITCH               = 1
    SET_TIME                   = 2
    BEHAVIOUR_SETTINGS         = 3


class GetPersistenceMode(IntEnum):
    CURRENT = 0
    STORED = 1
    FIRMWARE_DEFAULT = 2

class SetPersistenceMode(IntEnum):
    TEMPORARY = 0
    STORED = 1

class PowerSamplesType(IntEnum):
    SWITCHCRAFT                = 0
    SWITCHCRAFT_NON_TRIGGERED  = 1
    NOW_FILTERED               = 2
    NOW_UNFILTERED             = 3
    SOFT_FUSE                  = 4
    SWITCH                     = 5
    UNSPECIFIED                = 255

class CommandSourceType(IntEnum):
    ENUM                       = 0
    BEHAVIOUR                  = 1
    BROADCAST                  = 3
    UNSPECIFIED                = 255

class CommandSourceId(IntEnum):
    NONE                       = 0
    INTERNAL                   = 2
    UART                       = 3
    CONNECTION                 = 4
    SWITCHCRAFT                = 5
    TAP_TO_TOGGLE              = 6
    UNSPECIFIED                = 255

class MicroappOpcode(IntEnum):
    UPLOAD                     = 1
    VALIDATE                   = 2
    ENABLE                     = 3
    DISABLE                    = 4
    REQUEST                    = 5
    UNSPECIFIED                = 255

class SwitchValSpecial(IntEnum):
    TOGGLE                     = 253 # Switch OFF when currently on, switch to SMART_ON when currently off.
    BEHAVIOUR                  = 254 # Switch to the value according to behaviour rules.
    SMART_ON                   = 255 # Switch on, the value will be determined by behaviour rules.
