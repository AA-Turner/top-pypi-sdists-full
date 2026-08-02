from enum import IntEnum

class UartMessageType(IntEnum):
    UART_MESSAGE =                     0
    ENCRYPTED_UART_MESSAGE =           128

class UartTxType(IntEnum):
    HELLO =                            0
    SESSION_NONCE =                    1
    HEARTBEAT =                        2
    STATUS =                           3
    GET_MAC_ADDRESS =                  4
    CONTROL =                          10
    HUB_DATA_REPLY =                   11

    ENABLE_ADVERTISEMENT =             50000
    ENABLE_MESH =                      50001
    GET_CROWNSTONE_ID =                50002

    ADC_CONFIG_INC_RANGE_CURRENT =     50103
    ADC_CONFIG_DEC_RANGE_CURRENT =     50104
    ADC_CONFIG_INC_RANGE_VOLTAGE =     50105
    ADC_CONFIG_DEC_RANGE_VOLTAGE =     50106
    ADC_CONFIG_DIFFERENTIAL_CURRENT =  50108
    ADC_CONFIG_DIFFERENTIAL_VOLTAGE =  50109
    ADC_CONFIG_VOLTAGE_PIN =           50110

    POWER_LOG_CURRENT =                50200
    POWER_LOG_VOLTAGE =                50201
    POWER_LOG_FILTERED_CURRENT =       50202
    POWER_LOG_CALCULATED_POWER =       50204

    MOCK_INTERNAL_EVT =                60000
    UNKNOWN =                          65535

class UartRxType(IntEnum):
    HELLO =                            0
    SESSION_NONCE =                    1
    HEARTBEAT =                        2
    STATUS =                           3
    MAC_ADDRESS =                      4
    RESULT_PACKET =                    10

    ERR_REPLY_PARSING_FAILED =         9900
    ERR_REPLY_STATUS =                 9901
    ERR_REPLY_SESSION_NONCE_MISSING =  9902
    ERR_REPLY_DECRYPTION_FAILED =      9903

    UART_MESSAGE =                     10000
    SESSION_NONCE_MISSING =            10001
    OWN_SERVICE_DATA =                 10002
    PRESENCE_CHANGE =                  10004
    FACTORY_RESET =                    10005
    BOOTED =                           10006
    HUB_DATA =                         10007
    MICROAPP_DATA =                    10008

    MESH_SERVICE_DATA =                10102
    EXTERNAL_STATE_PART_0 =			   10103
    EXTERNAL_STATE_PART_1 =			   10104
    MESH_RESULT = 					   10105
    MESH_ACK_ALL_RESULT = 		       10106
    RSSI_PING_MESSAGE =                10107

    ASSET_MAC_RSSI_REPORT =            10108

    NEIGHBOUR_RSSI =                   10111
    ASSET_ID_RSSI_REPORT =             10112

    LOG =                              10200
    LOG_ARRAY =                        10201

    INTERNAL_EVENT =                   40000

    MESH_CMD_TIME =                    40103
    MESH_PROFILE_LOCATION =            40110
    MESH_SET_BEHAVIOUR_SETTINGS =      40111
    MESH_TRACKED_DEVICE_REGISTER =     40112
    MESH_TRACKED_DEVICE_TOKEN =        40113
    MESH_SYNC_REQUEST =                40114
    MESH_TRACKED_DEVICE_HEARTBEAT =    40120

    ADVERTISING_ENABLED =              50000
    MESH_ENABLED =                     50001
    CROWNSTONE_ID =                    50002

    ADC_CONFIG =                       50100
    ADC_RESTART =                      50101

    POWER_LOG_CURRENT =                50200
    POWER_LOG_VOLTAGE =                50201
    POWER_LOG_FILTERED_CURRENT =       50202
    POWER_LOG_FILTERED_VOLTAGE =       50203
    POWER_LOG_POWER =                  50204

    ASCII_LOG =               		   60000
    FIRMWARESTATE =                    60001
