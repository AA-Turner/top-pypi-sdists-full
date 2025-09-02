from enum import Enum


class UartError(Enum):
    """Error types for Uart exceptions."""
    NO_CROWNSTONE_UART_DEVICE_AVAILABLE = "NO_CROWNSTONE_UART_DEVICE_AVAILABLE"


class UartBridgeError(Enum):
    """Error types for Uart Bridge exceptions."""
    CANNOT_OPEN_SERIAL_CONTROLLER       = "CANNOT_OPEN_SERIAL_CONTROLLER"

    def __str__(self) -> str:
        """Return value of the error."""
        return self.value


class UartException(Exception):
    """Raised on errors in the Uart Manager."""
