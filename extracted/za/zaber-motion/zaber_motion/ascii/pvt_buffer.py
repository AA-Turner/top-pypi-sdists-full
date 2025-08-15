# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List
from ..dto import requests as dto
from ..call import call, call_async

if TYPE_CHECKING:
    from .device import Device


class PvtBuffer:
    """
    Represents a PVT buffer with this number on a device.
    A PVT buffer is a place to store a queue of PVT actions.
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
        Gets the buffer contents as an array of strings.

        Returns:
            A string array containing all the PVT commands stored in the buffer.
        """
        request = dto.StreamBufferGetContentRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
            pvt=True,
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
        Gets the buffer contents as an array of strings.

        Returns:
            A string array containing all the PVT commands stored in the buffer.
        """
        request = dto.StreamBufferGetContentRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
            pvt=True,
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
        Erases the contents of the buffer.
        This method fails if there is a PVT sequence writing to the buffer.
        """
        request = dto.StreamBufferEraseRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
            pvt=True,
        )
        call("device/stream_buffer_erase", request)

    async def erase_async(
            self
    ) -> None:
        """
        Erases the contents of the buffer.
        This method fails if there is a PVT sequence writing to the buffer.
        """
        request = dto.StreamBufferEraseRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            buffer_id=self.buffer_id,
            pvt=True,
        )
        await call_async("device/stream_buffer_erase", request)
