# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List
from ..dto import requests as dto
from ..call import call, call_async

if TYPE_CHECKING:
    from .device import Device


class StreamBuffer:
    """
    Represents a stream buffer with this number on a device.
    A stream buffer is a place to store a queue of stream actions.
    """

    @property
    def device(self) -> 'Device':
        """
        The Device this buffer exists on.
        """
        return self._device

    @property
    def buffer_id(self) -> int:
        """
        The number identifying the buffer on the device.
        """
        return self._buffer_id

    def __init__(self, device: 'Device', buffer_id: int):
        self._device: 'Device' = device
        self._buffer_id: int = buffer_id

    def get_content(
            self
    ) -> List[str]:
        """
        Get the buffer contents as an array of strings.

        Returns:
            A string array containing all the stream commands stored in the buffer.
        """
        request = dto.StreamBufferGetContentRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
        )
        response = call(
            "device/stream_buffer_get_content",
            request,
            dto.StreamBufferGetContentResponse.from_binary)
        return response.buffer_lines

    async def get_content_async(
            self
    ) -> List[str]:
        """
        Get the buffer contents as an array of strings.

        Returns:
            A string array containing all the stream commands stored in the buffer.
        """
        request = dto.StreamBufferGetContentRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
        )
        response = await call_async(
            "device/stream_buffer_get_content",
            request,
            dto.StreamBufferGetContentResponse.from_binary)
        return response.buffer_lines

    def erase(
            self
    ) -> None:
        """
        Erase the contents of the buffer.
        This method fails if there is a stream writing to the buffer.
        """
        request = dto.StreamBufferEraseRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
        )
        call("device/stream_buffer_erase", request)

    async def erase_async(
            self
    ) -> None:
        """
        Erase the contents of the buffer.
        This method fails if there is a stream writing to the buffer.
        """
        request = dto.StreamBufferEraseRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
        )
        await call_async("device/stream_buffer_erase", request)
