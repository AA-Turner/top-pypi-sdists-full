
class DevTopics:
    newServiceData = "newServiceData"  # data is dictionary: {
                                       #                        "id": int
                                       #                        "opCode": int
                                       #                        "dataType": int
                                       #                        "switchState": int
                                       #                        "flagBitmask": int
                                       #                        "temperature": int
                                       #                        "powerFactor": int
                                       #                        "powerUsageReal": int
                                       #                        "energyUsed": int
                                       #                        "partialTimestamp": int
                                       #                        "validation": int
                                       #                     }
    newCurrentData = "newCurrentData"  # data is dictionary: { id: int, type: 'current', data: [(time, data point)] }
    newVoltageData = "newVoltageData"  # data is dictionary: { id: int, type: 'voltage', data: [(time, data point)] }
    newFilteredCurrentData = "newFilteredCurrentData"  # data is dictionary: { id: int, type: 'current', data: [(time, data point)] }
    newFilteredVoltageData = "newFilteredVoltageData"  # data is dictionary: { id: int, type: 'voltage', data: [(time, data point)] }
    newCalculatedPowerData = "newCalculatedPowerData"  # data is dictionary: {
                                                       #                         "id": int,
                                                       #                         "currentRmsMA": int,
                                                       #                         "currentRmsMedianMA": int,
                                                       #                         "filteredCurrentRmsMA": int,
                                                       #                         "filteredCurrentRmsMedianMA": int,
                                                       #                         "avgZeroVoltage": int,
                                                       #                         "avgZeroCurrent": int,
                                                       #                         "powerMilliWattApparent": int,
                                                       #                         "powerMilliWattReal": int,
                                                       #                         "avgPowerMilliWattReal": int
                                                       #                     }
    newAdcConfigPacket = 'newAdcConfigPacket'
    adcRestarted = 'adcRestarted'
    ownMacAddress = 'ownMacAddress'
    ownCrownstoneId = 'ownCrownstoneId'
