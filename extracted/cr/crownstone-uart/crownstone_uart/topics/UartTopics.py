
class UartTopics:

    newDataAvailable = "UART_newDataAvailable"

    uartMessage = "UART_Message" # data is dictionary: {"string": str, "data": [uint8, uint8, ...] }

    hello = "UART_hello" # Data is: UartCrownstoneHelloPacket

    log = "UART_log" # Data is UartLogPacket
    logArray = "UART_logArray" # Data is UartLogArrayPacket

    assetIdReport = "assetIdReport" # Data is an AssetIdReport class instance.
    assetTrackingReport = "assetTrackingReport" # Data is an AssetMacReport class instance.

    rssiBetweenStones = "rssiBetweenStones" # Data is RssiBetweenStonesPacket

    microappMessage = "Microapp_message" # Data is MicroappMessagePacket
