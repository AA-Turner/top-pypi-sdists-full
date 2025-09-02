class UartCommandHelloPacket:
    """
    UART command hello packet:
    1B flags
    """
    def __init__(self, encryptionRequired: bool = False, hasBeenSetUp: bool = False, hasInternet: bool = False, hasError: bool = False):
        self.encryptionRequired = encryptionRequired
        self.hasBeenSetUp = hasBeenSetUp
        self.hasInternet = hasInternet
        self.hasError = hasError

    def serialize(self):
        flags = 0 # Uint 8
        if self.encryptionRequired: flags = flags | (1 << 0)
        if self.hasBeenSetUp:       flags = flags | (1 << 1)
        if self.hasInternet:        flags = flags | (1 << 2)
        if self.hasError:           flags = flags | (1 << 3)
        return [flags]
