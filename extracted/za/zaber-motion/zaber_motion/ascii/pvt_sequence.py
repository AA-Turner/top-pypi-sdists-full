# pylint: disable=too-many-arguments, too-many-lines

# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #
from typing import TYPE_CHECKING, List, Optional
from ..dto import requests as dto
from ..call import call, call_async, call_sync
from ..dto.measurement import Measurement
from .pvt_buffer import PvtBuffer
from ..dto.ascii.pvt_mode import PvtMode
from ..dto.ascii.pvt_axis_definition import PvtAxisDefinition
from ..dto.ascii.pvt_sequence_data import PvtSequenceData
from ..dto.ascii.pvt_csv_data import PvtCsvData
from ..dto.ascii.measurement_sequence import MeasurementSequence
from ..dto.ascii.optional_measurement_sequence import OptionalMeasurementSequence

from .pvt_io import PvtIo
from ..dto.ascii.digital_output_action import DigitalOutputAction

if TYPE_CHECKING:
    from .device import Device


class PvtSequence:
    """
    A handle for a PVT sequence with this number on the device.
    PVT sequences provide a way execute or store trajectory
    consisting of points with defined position, velocity, and time.
    PVT sequence methods append actions to a queue which executes
    or stores actions in a first in, first out order.
    """

    @property
    def device(self) -> 'Device':
        """
        Device that controls this PVT sequence.
        """
        return self._device

    @property
    def pvt_id(self) -> int:
        """
        The number that identifies the PVT sequence on the device.
        """
        return self._pvt_id

    @property
    def mode(self) -> PvtMode:
        """
        Current mode of the PVT sequence.
        """
        return self.__retrieve_mode()

    @property
    def axes(self) -> List[PvtAxisDefinition]:
        """
        An array of axes definitions the PVT sequence is set up to control.
        """
        return self.__retrieve_axes()

    @property
    def io(self) -> PvtIo:
        """
        Gets an object that provides access to I/O for this sequence.
        """
        return self._io

    def __init__(self, device: 'Device', pvt_id: int):
        self._device: 'Device' = device
        self._pvt_id: int = pvt_id
        self._io: PvtIo = PvtIo(device, pvt_id)

    def setup_live_composite(
            self,
            *pvt_axes: PvtAxisDefinition
    ) -> None:
        """
        Setup the PVT sequence to control the specified axes and to queue actions on the device.
        Allows use of lockstep axes in a PVT sequence.

        Args:
            pvt_axes: Definition of the PVT sequence axes.
        """
        request = dto.StreamSetupLiveCompositeRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_axes=list(pvt_axes),
        )
        call("device/stream_setup_live_composite", request)

    async def setup_live_composite_async(
            self,
            *pvt_axes: PvtAxisDefinition
    ) -> None:
        """
        Setup the PVT sequence to control the specified axes and to queue actions on the device.
        Allows use of lockstep axes in a PVT sequence.

        Args:
            pvt_axes: Definition of the PVT sequence axes.
        """
        request = dto.StreamSetupLiveCompositeRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_axes=list(pvt_axes),
        )
        await call_async("device/stream_setup_live_composite", request)

    def setup_live(
            self,
            *axes: int
    ) -> None:
        """
        Setup the PVT sequence to control the specified axes and to queue actions on the device.

        Args:
            axes: Numbers of physical axes to setup the PVT sequence on.
        """
        request = dto.StreamSetupLiveRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            axes=list(axes),
        )
        call("device/stream_setup_live", request)

    async def setup_live_async(
            self,
            *axes: int
    ) -> None:
        """
        Setup the PVT sequence to control the specified axes and to queue actions on the device.

        Args:
            axes: Numbers of physical axes to setup the PVT sequence on.
        """
        request = dto.StreamSetupLiveRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            axes=list(axes),
        )
        await call_async("device/stream_setup_live", request)

    def setup_store_composite(
            self,
            pvt_buffer: PvtBuffer,
            *pvt_axes: PvtAxisDefinition
    ) -> None:
        """
        Setup the PVT sequence to use the specified axes and queue actions into a PVT buffer.
        Allows use of lockstep axes in a PVT sequence.

        Args:
            pvt_buffer: The PVT buffer to queue actions in.
            pvt_axes: Definition of the PVT sequence axes.
        """
        request = dto.StreamSetupStoreCompositeRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_buffer=pvt_buffer.buffer_id,
            pvt_axes=list(pvt_axes),
        )
        call("device/stream_setup_store_composite", request)

    async def setup_store_composite_async(
            self,
            pvt_buffer: PvtBuffer,
            *pvt_axes: PvtAxisDefinition
    ) -> None:
        """
        Setup the PVT sequence to use the specified axes and queue actions into a PVT buffer.
        Allows use of lockstep axes in a PVT sequence.

        Args:
            pvt_buffer: The PVT buffer to queue actions in.
            pvt_axes: Definition of the PVT sequence axes.
        """
        request = dto.StreamSetupStoreCompositeRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_buffer=pvt_buffer.buffer_id,
            pvt_axes=list(pvt_axes),
        )
        await call_async("device/stream_setup_store_composite", request)

    def setup_store(
            self,
            pvt_buffer: PvtBuffer,
            *axes: int
    ) -> None:
        """
        Setup the PVT sequence to use the specified axes and queue actions into a PVT buffer.

        Args:
            pvt_buffer: The PVT buffer to queue actions in.
            axes: Numbers of physical axes to setup the PVT sequence on.
        """
        request = dto.StreamSetupStoreRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_buffer=pvt_buffer.buffer_id,
            axes=list(axes),
        )
        call("device/stream_setup_store", request)

    async def setup_store_async(
            self,
            pvt_buffer: PvtBuffer,
            *axes: int
    ) -> None:
        """
        Setup the PVT sequence to use the specified axes and queue actions into a PVT buffer.

        Args:
            pvt_buffer: The PVT buffer to queue actions in.
            axes: Numbers of physical axes to setup the PVT sequence on.
        """
        request = dto.StreamSetupStoreRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_buffer=pvt_buffer.buffer_id,
            axes=list(axes),
        )
        await call_async("device/stream_setup_store", request)

    def call(
            self,
            pvt_buffer: PvtBuffer
    ) -> None:
        """
        Append the actions in a PVT buffer to the sequence's queue.

        Args:
            pvt_buffer: The PVT buffer to call.
        """
        request = dto.StreamCallRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_buffer=pvt_buffer.buffer_id,
        )
        call("device/stream_call", request)

    async def call_async(
            self,
            pvt_buffer: PvtBuffer
    ) -> None:
        """
        Append the actions in a PVT buffer to the sequence's queue.

        Args:
            pvt_buffer: The PVT buffer to call.
        """
        request = dto.StreamCallRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            pvt_buffer=pvt_buffer.buffer_id,
        )
        await call_async("device/stream_call", request)

    def point(
            self,
            positions: List[Measurement],
            velocities: List[Optional[Measurement]],
            time: Measurement
    ) -> None:
        """
        Queues a point with absolute coordinates in the PVT sequence.
        If some or all velocities are not provided, the sequence calculates the velocities
        from surrounding points using finite difference.
        The last point of the sequence must have defined velocity (likely zero).

        Args:
            positions: Positions for the axes to move through, relative to their home positions.
            velocities: The axes velocities at the given point.
                Specify an empty array or null for specific axes to make the sequence calculate the velocity.
            time: The duration between the previous point in the sequence and this one.
        """
        request = dto.PvtPointRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.ABS,
            positions=positions,
            velocities=velocities,
            time=time,
        )
        call("device/stream_point", request)

    async def point_async(
            self,
            positions: List[Measurement],
            velocities: List[Optional[Measurement]],
            time: Measurement
    ) -> None:
        """
        Queues a point with absolute coordinates in the PVT sequence.
        If some or all velocities are not provided, the sequence calculates the velocities
        from surrounding points using finite difference.
        The last point of the sequence must have defined velocity (likely zero).

        Args:
            positions: Positions for the axes to move through, relative to their home positions.
            velocities: The axes velocities at the given point.
                Specify an empty array or null for specific axes to make the sequence calculate the velocity.
            time: The duration between the previous point in the sequence and this one.
        """
        request = dto.PvtPointRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.ABS,
            positions=positions,
            velocities=velocities,
            time=time,
        )
        await call_async("device/stream_point", request)

    def points(
            self,
            positions: List[MeasurementSequence],
            velocities: List[MeasurementSequence],
            times: MeasurementSequence
    ) -> None:
        """
        Queues points with absolute coordinates in the PVT sequence.

        Args:
            positions: Per-axis sequences of positions.
            velocities: Per-axis sequences of velocities.
                For velocities [v0, v1, ...] and positions [p0, p1, ...], v1 is the target velocity at point p1.
            times: Segment times from one point to another.
                For times [t0, t1, ...] and positions [p0, p1, ...], t1 is the time it takes to move from p0 to p1.
        """
        request = dto.PvtPointsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.ABS,
            positions=positions,
            velocities=velocities,
            times=times,
        )
        call("device/stream_points", request)

    async def points_async(
            self,
            positions: List[MeasurementSequence],
            velocities: List[MeasurementSequence],
            times: MeasurementSequence
    ) -> None:
        """
        Queues points with absolute coordinates in the PVT sequence.

        Args:
            positions: Per-axis sequences of positions.
            velocities: Per-axis sequences of velocities.
                For velocities [v0, v1, ...] and positions [p0, p1, ...], v1 is the target velocity at point p1.
            times: Segment times from one point to another.
                For times [t0, t1, ...] and positions [p0, p1, ...], t1 is the time it takes to move from p0 to p1.
        """
        request = dto.PvtPointsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.ABS,
            positions=positions,
            velocities=velocities,
            times=times,
        )
        await call_async("device/stream_points", request)

    def point_relative(
            self,
            positions: List[Measurement],
            velocities: List[Optional[Measurement]],
            time: Measurement
    ) -> None:
        """
        Queues a point with coordinates relative to the previous point in the PVT sequence.
        If some or all velocities are not provided, the sequence calculates the velocities
        from surrounding points using finite difference.
        The last point of the sequence must have defined velocity (likely zero).

        Args:
            positions: Positions for the axes to move through, relative to the previous point.
            velocities: The axes velocities at the given point.
                Specify an empty array or null for specific axes to make the sequence calculate the velocity.
            time: The duration between the previous point in the sequence and this one.
        """
        request = dto.PvtPointRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.REL,
            positions=positions,
            velocities=velocities,
            time=time,
        )
        call("device/stream_point", request)

    async def point_relative_async(
            self,
            positions: List[Measurement],
            velocities: List[Optional[Measurement]],
            time: Measurement
    ) -> None:
        """
        Queues a point with coordinates relative to the previous point in the PVT sequence.
        If some or all velocities are not provided, the sequence calculates the velocities
        from surrounding points using finite difference.
        The last point of the sequence must have defined velocity (likely zero).

        Args:
            positions: Positions for the axes to move through, relative to the previous point.
            velocities: The axes velocities at the given point.
                Specify an empty array or null for specific axes to make the sequence calculate the velocity.
            time: The duration between the previous point in the sequence and this one.
        """
        request = dto.PvtPointRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.REL,
            positions=positions,
            velocities=velocities,
            time=time,
        )
        await call_async("device/stream_point", request)

    def points_relative(
            self,
            positions: List[MeasurementSequence],
            velocities: List[MeasurementSequence],
            times: MeasurementSequence
    ) -> None:
        """
        Queues points with coordinates relative to the previous point in the PVT sequence.

        Args:
            positions: Per-axis sequences of positions.
            velocities: Per-axis sequences of velocities.
                For velocities [v0, v1, ...] and positions [p0, p1, ...], v1 is the target velocity at point p1.
            times: Segment times from one point to another.
                For times [t0, t1, ...] and positions [p0, p1, ...], t1 is the time it takes to move from p0 to p1.
        """
        request = dto.PvtPointsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.REL,
            positions=positions,
            velocities=velocities,
            times=times,
        )
        call("device/stream_points", request)

    async def points_relative_async(
            self,
            positions: List[MeasurementSequence],
            velocities: List[MeasurementSequence],
            times: MeasurementSequence
    ) -> None:
        """
        Queues points with coordinates relative to the previous point in the PVT sequence.

        Args:
            positions: Per-axis sequences of positions.
            velocities: Per-axis sequences of velocities.
                For velocities [v0, v1, ...] and positions [p0, p1, ...], v1 is the target velocity at point p1.
            times: Segment times from one point to another.
                For times [t0, t1, ...] and positions [p0, p1, ...], t1 is the time it takes to move from p0 to p1.
        """
        request = dto.PvtPointsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            type=dto.StreamSegmentType.REL,
            positions=positions,
            velocities=velocities,
            times=times,
        )
        await call_async("device/stream_points", request)

    @staticmethod
    def generate_velocities(
            positions: List[MeasurementSequence],
            times: MeasurementSequence,
            velocities: Optional[List[OptionalMeasurementSequence]] = None,
            times_relative: bool = True
    ) -> PvtSequenceData:
        """
        Generates velocities for a sequence of positions and times, and (optionally) a partially defined sequence
        of velocities. Note that if some velocities are defined, the solver will NOT modify them in any way.
        If all velocities are defined, the solver will simply return the same velocities.
        This function calculates velocities by enforcing that acceleration be continuous at each segment transition.

        Also note that if generating a path for multiple axes, the user must provide a position measurement sequence
        per axis, And the values arrays for each sequence must be equal in length to each other and also to the
        times sequence.

        Args:
            positions: Positions for the axes to move through, relative to their home positions.
                Each MeasurementSequence represents a sequence of positions along a particular dimension.
                For example, a 2D path sequence would contain two MeasurementSequence objects,
                one representing positions along X and one for those along Y.
            times: The relative or absolute time of each position in the PVT sequence.
            velocities: Optional velocities corresponding to each point in the position sequences.
            times_relative: If true, the times sequence values are interpreted as relative. Otherwise,
                they are interpreted as absolute. Note that the values of the returned time
                sequence are ALWAYS relative. This is because the PVT sequence API expects
                points to have relative times.

        Returns:
            Object containing the generated PVT sequence. Note that returned time sequence is always relative.
        """
        request = dto.PvtGenerateVelocitiesRequest(
            positions=positions,
            times=times,
            velocities=velocities,
            times_relative=times_relative,
        )
        response = call(
            "device/pvt_generate_velocities",
            request,
            PvtSequenceData.from_binary)
        return response

    @staticmethod
    async def generate_velocities_async(
            positions: List[MeasurementSequence],
            times: MeasurementSequence,
            velocities: Optional[List[OptionalMeasurementSequence]] = None,
            times_relative: bool = True
    ) -> PvtSequenceData:
        """
        Generates velocities for a sequence of positions and times, and (optionally) a partially defined sequence
        of velocities. Note that if some velocities are defined, the solver will NOT modify them in any way.
        If all velocities are defined, the solver will simply return the same velocities.
        This function calculates velocities by enforcing that acceleration be continuous at each segment transition.

        Also note that if generating a path for multiple axes, the user must provide a position measurement sequence
        per axis, And the values arrays for each sequence must be equal in length to each other and also to the
        times sequence.

        Args:
            positions: Positions for the axes to move through, relative to their home positions.
                Each MeasurementSequence represents a sequence of positions along a particular dimension.
                For example, a 2D path sequence would contain two MeasurementSequence objects,
                one representing positions along X and one for those along Y.
            times: The relative or absolute time of each position in the PVT sequence.
            velocities: Optional velocities corresponding to each point in the position sequences.
            times_relative: If true, the times sequence values are interpreted as relative. Otherwise,
                they are interpreted as absolute. Note that the values of the returned time
                sequence are ALWAYS relative. This is because the PVT sequence API expects
                points to have relative times.

        Returns:
            Object containing the generated PVT sequence. Note that returned time sequence is always relative.
        """
        request = dto.PvtGenerateVelocitiesRequest(
            positions=positions,
            times=times,
            velocities=velocities,
            times_relative=times_relative,
        )
        response = await call_async(
            "device/pvt_generate_velocities",
            request,
            PvtSequenceData.from_binary)
        return response

    @staticmethod
    def generate_positions(
            velocities: List[MeasurementSequence],
            times: MeasurementSequence,
            times_relative: bool = True
    ) -> PvtSequenceData:
        """
        Generates positions for a sequence of velocities and times. This function calculates
        positions by enforcing that acceleration be continuous at each segment transition.

        Note that if generating a path for multiple axes, the user must provide a
        velocity measurement sequence per axis, and the values arrays for each sequence
        must be equal in length to each other and also to the times sequence.

        Args:
            velocities: The sequence of velocities for each axis.
                Each MeasurementSequence represents a sequence of velocities along particular dimension.
            times: The relative or absolute time of each position in the PVT sequence.
            times_relative: If true, the times sequence values are interpreted as relative. Otherwise,
                they are interpreted as absolute. Note that the values of the returned time
                sequence are ALWAYS relative. This is because the PVT sequence API expects
                points to have relative times.

        Returns:
            Object containing the generated PVT sequence. Note that returned time sequence is always relative.
        """
        request = dto.PvtGeneratePositionsRequest(
            velocities=velocities,
            times=times,
            times_relative=times_relative,
        )
        response = call(
            "device/pvt_generate_positions",
            request,
            PvtSequenceData.from_binary)
        return response

    @staticmethod
    async def generate_positions_async(
            velocities: List[MeasurementSequence],
            times: MeasurementSequence,
            times_relative: bool = True
    ) -> PvtSequenceData:
        """
        Generates positions for a sequence of velocities and times. This function calculates
        positions by enforcing that acceleration be continuous at each segment transition.

        Note that if generating a path for multiple axes, the user must provide a
        velocity measurement sequence per axis, and the values arrays for each sequence
        must be equal in length to each other and also to the times sequence.

        Args:
            velocities: The sequence of velocities for each axis.
                Each MeasurementSequence represents a sequence of velocities along particular dimension.
            times: The relative or absolute time of each position in the PVT sequence.
            times_relative: If true, the times sequence values are interpreted as relative. Otherwise,
                they are interpreted as absolute. Note that the values of the returned time
                sequence are ALWAYS relative. This is because the PVT sequence API expects
                points to have relative times.

        Returns:
            Object containing the generated PVT sequence. Note that returned time sequence is always relative.
        """
        request = dto.PvtGeneratePositionsRequest(
            velocities=velocities,
            times=times,
            times_relative=times_relative,
        )
        response = await call_async(
            "device/pvt_generate_positions",
            request,
            PvtSequenceData.from_binary)
        return response

    def wait_until_idle(
            self,
            throw_error_on_fault: bool = True
    ) -> None:
        """
        Waits until the live PVT sequence executes all queued actions.

        Args:
            throw_error_on_fault: Determines whether to throw error when fault is observed.
        """
        request = dto.StreamWaitUntilIdleRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            throw_error_on_fault=throw_error_on_fault,
        )
        call("device/stream_wait_until_idle", request)

    async def wait_until_idle_async(
            self,
            throw_error_on_fault: bool = True
    ) -> None:
        """
        Waits until the live PVT sequence executes all queued actions.

        Args:
            throw_error_on_fault: Determines whether to throw error when fault is observed.
        """
        request = dto.StreamWaitUntilIdleRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            throw_error_on_fault=throw_error_on_fault,
        )
        await call_async("device/stream_wait_until_idle", request)

    def cork(
            self
    ) -> None:
        """
        Cork the front of the PVT sequences's action queue, blocking execution.
        Execution resumes upon uncorking the queue, or when the number of queued actions reaches its limit.
        Corking eliminates discontinuities in motion due to subsequent PVT commands reaching the device late.
        You can only cork an idle live PVT sequence.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        call("device/stream_cork", request)

    async def cork_async(
            self
    ) -> None:
        """
        Cork the front of the PVT sequences's action queue, blocking execution.
        Execution resumes upon uncorking the queue, or when the number of queued actions reaches its limit.
        Corking eliminates discontinuities in motion due to subsequent PVT commands reaching the device late.
        You can only cork an idle live PVT sequence.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        await call_async("device/stream_cork", request)

    def uncork(
            self
    ) -> None:
        """
        Uncork the front of the queue, unblocking command execution.
        You can only uncork an idle live PVT sequence that is corked.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        call("device/stream_uncork", request)

    async def uncork_async(
            self
    ) -> None:
        """
        Uncork the front of the queue, unblocking command execution.
        You can only uncork an idle live PVT sequence that is corked.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        await call_async("device/stream_uncork", request)

    def is_busy(
            self
    ) -> bool:
        """
        Returns a boolean value indicating whether the live PVT sequence is executing a queued action.

        Returns:
            True if the PVT sequence is executing a queued action.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = call(
            "device/stream_is_busy",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    async def is_busy_async(
            self
    ) -> bool:
        """
        Returns a boolean value indicating whether the live PVT sequence is executing a queued action.

        Returns:
            True if the PVT sequence is executing a queued action.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = await call_async(
            "device/stream_is_busy",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def __repr__(
            self
    ) -> str:
        """
        Returns a string which represents the PVT sequence.

        Returns:
            String which represents the PVT sequence.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = call_sync(
            "device/stream_to_string",
            request,
            dto.StringResponse.from_binary)
        return response.value

    def disable(
            self
    ) -> None:
        """
        Disables the PVT sequence.
        If the PVT sequence is not setup, this command does nothing.
        Once disabled, the PVT sequence will no longer accept PVT commands.
        The PVT sequence will process the rest of the commands in the queue until it is empty.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        call("device/stream_disable", request)

    async def disable_async(
            self
    ) -> None:
        """
        Disables the PVT sequence.
        If the PVT sequence is not setup, this command does nothing.
        Once disabled, the PVT sequence will no longer accept PVT commands.
        The PVT sequence will process the rest of the commands in the queue until it is empty.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        await call_async("device/stream_disable", request)

    def generic_command(
            self,
            command: str
    ) -> None:
        """
        Sends a generic ASCII command to the PVT sequence.
        Keeps resending the command while the device rejects with AGAIN reason.

        Args:
            command: Command and its parameters.
        """
        request = dto.StreamGenericCommandRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            command=command,
        )
        call("device/stream_generic_command", request)

    async def generic_command_async(
            self,
            command: str
    ) -> None:
        """
        Sends a generic ASCII command to the PVT sequence.
        Keeps resending the command while the device rejects with AGAIN reason.

        Args:
            command: Command and its parameters.
        """
        request = dto.StreamGenericCommandRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            command=command,
        )
        await call_async("device/stream_generic_command", request)

    def generic_command_batch(
            self,
            batch: List[str]
    ) -> None:
        """
        Sends a batch of generic ASCII commands to the PVT sequence.
        Keeps resending command while the device rejects with AGAIN reason.
        The batch is atomic in terms of thread safety.

        Args:
            batch: Array of commands.
        """
        request = dto.StreamGenericCommandBatchRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            batch=batch,
        )
        call("device/stream_generic_command_batch", request)

    async def generic_command_batch_async(
            self,
            batch: List[str]
    ) -> None:
        """
        Sends a batch of generic ASCII commands to the PVT sequence.
        Keeps resending command while the device rejects with AGAIN reason.
        The batch is atomic in terms of thread safety.

        Args:
            batch: Array of commands.
        """
        request = dto.StreamGenericCommandBatchRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            batch=batch,
        )
        await call_async("device/stream_generic_command_batch", request)

    def check_disabled(
            self
    ) -> bool:
        """
        Queries the PVT sequence status from the device
        and returns boolean indicating whether the PVT sequence is disabled.
        Useful to determine if execution was interrupted by other movements.

        Returns:
            True if the PVT sequence is disabled.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = call(
            "device/stream_check_disabled",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    async def check_disabled_async(
            self
    ) -> bool:
        """
        Queries the PVT sequence status from the device
        and returns boolean indicating whether the PVT sequence is disabled.
        Useful to determine if execution was interrupted by other movements.

        Returns:
            True if the PVT sequence is disabled.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = await call_async(
            "device/stream_check_disabled",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def treat_discontinuities_as_error(
            self
    ) -> None:
        """
        Makes the PVT sequence throw PvtDiscontinuityException when it encounters discontinuities (ND warning flag).
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        call_sync("device/stream_treat_discontinuities", request)

    def ignore_current_discontinuity(
            self
    ) -> None:
        """
        Prevents PvtDiscontinuityException as a result of expected discontinuity when resuming the sequence.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        call_sync("device/stream_ignore_discontinuity", request)

    def __retrieve_axes(
            self
    ) -> List[PvtAxisDefinition]:
        """
        Gets the axes of the PVT sequence.

        Returns:
            An array of axis numbers of the axes the PVT sequence is set up to control.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = call_sync(
            "device/stream_get_axes",
            request,
            dto.StreamGetAxesResponse.from_binary)
        return response.pvt_axes

    def __retrieve_mode(
            self
    ) -> PvtMode:
        """
        Get the mode of the PVT sequence.

        Returns:
            Mode of the PVT sequence.
        """
        request = dto.StreamEmptyRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
        )
        response = call_sync(
            "device/stream_get_mode",
            request,
            dto.StreamModeResponse.from_binary)
        return response.pvt_mode

    @staticmethod
    def save_sequence_data(
            sequence_data: PvtSequenceData,
            path: str,
            dimension_names: Optional[List[str]] = None
    ) -> None:
        """
        Saves PvtSequenceData object as csv file.
        Save format is compatible with Zaber Launcher PVT Editor App.

        Throws InvalidArgumentException if fields are undefined or inconsistent.
        For example, position and velocity arrays must have the same dimensions.
        Sequence lengths must be consistent for positions, velocities and times.

        Args:
            sequence_data: The PVT sequence data to save.
            path: The path to save the file to.
            dimension_names: Optional csv column names for each series.
                If not provided, the default names will be used: Series 1, Series 2, etc..
                Length of this array must be equal to number of dimensions in sequence data.
        """
        request = dto.PvtSaveCsvRequest(
            sequence_data=sequence_data,
            path=path,
            dimension_names=dimension_names,
        )
        call("device/stream_pvt_save_csv", request)

    @staticmethod
    async def save_sequence_data_async(
            sequence_data: PvtSequenceData,
            path: str,
            dimension_names: Optional[List[str]] = None
    ) -> None:
        """
        Saves PvtSequenceData object as csv file.
        Save format is compatible with Zaber Launcher PVT Editor App.

        Throws InvalidArgumentException if fields are undefined or inconsistent.
        For example, position and velocity arrays must have the same dimensions.
        Sequence lengths must be consistent for positions, velocities and times.

        Args:
            sequence_data: The PVT sequence data to save.
            path: The path to save the file to.
            dimension_names: Optional csv column names for each series.
                If not provided, the default names will be used: Series 1, Series 2, etc..
                Length of this array must be equal to number of dimensions in sequence data.
        """
        request = dto.PvtSaveCsvRequest(
            sequence_data=sequence_data,
            path=path,
            dimension_names=dimension_names,
        )
        await call_async("device/stream_pvt_save_csv", request)

    @staticmethod
    def load_sequence_data(
            path: str
    ) -> PvtCsvData:
        """
        Load PVT Sequence data from CSV file.
        The CSV data can include a header (recommended).
        There are two possible header formats:

        1. A time column with named position and velocity columns.
        For example, "Time (ms),X Position (cm),X Velocity (cm/s),...".
        In this case, position, velocity and time columns are all optional.
        Also, order does not matter, but position and velocity names must be consistent.
        This is our recommended CSV format.

        2. A time column with alternating position and velocity columns.
        For example, "Time (ms),Position (cm),Velocity (cm/s),...".
        In this case, only the time column is optional and order does matter.

        Units must be wrapped in parens or square braces: ie. (µm/s), [µm/s].
        Additionally, native units are the default if no units are specified.
        Time values default to milliseconds if no units are provided.
        If no header is included, then column order is assumed to be "T,P1,V1,P2,V2,...".
        In this case the number of columns must be odd.

        Args:
            path: The path to the csv file to load.

        Returns:
            The PVT csv data loaded from the file.
        """
        request = dto.PvtLoadCsvRequest(
            path=path,
        )
        response = call(
            "device/stream_pvt_load_csv",
            request,
            PvtCsvData.from_binary)
        return response

    @staticmethod
    async def load_sequence_data_async(
            path: str
    ) -> PvtCsvData:
        """
        Load PVT Sequence data from CSV file.
        The CSV data can include a header (recommended).
        There are two possible header formats:

        1. A time column with named position and velocity columns.
        For example, "Time (ms),X Position (cm),X Velocity (cm/s),...".
        In this case, position, velocity and time columns are all optional.
        Also, order does not matter, but position and velocity names must be consistent.
        This is our recommended CSV format.

        2. A time column with alternating position and velocity columns.
        For example, "Time (ms),Position (cm),Velocity (cm/s),...".
        In this case, only the time column is optional and order does matter.

        Units must be wrapped in parens or square braces: ie. (µm/s), [µm/s].
        Additionally, native units are the default if no units are specified.
        Time values default to milliseconds if no units are provided.
        If no header is included, then column order is assumed to be "T,P1,V1,P2,V2,...".
        In this case the number of columns must be odd.

        Args:
            path: The path to the csv file to load.

        Returns:
            The PVT csv data loaded from the file.
        """
        request = dto.PvtLoadCsvRequest(
            path=path,
        )
        response = await call_async(
            "device/stream_pvt_load_csv",
            request,
            PvtCsvData.from_binary)
        return response

    def set_digital_output(
            self,
            channel_number: int,
            value: DigitalOutputAction
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetDigitalOutput instead.

        Sets value for the specified digital output channel.

        Args:
            channel_number: Channel number starting at 1.
            value: The type of action to perform on the channel.
        """
        request = dto.StreamSetDigitalOutputRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            channel_number=channel_number,
            value=value,
        )
        call("device/stream_set_digital_output", request)

    async def set_digital_output_async(
            self,
            channel_number: int,
            value: DigitalOutputAction
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetDigitalOutput instead.

        Sets value for the specified digital output channel.

        Args:
            channel_number: Channel number starting at 1.
            value: The type of action to perform on the channel.
        """
        request = dto.StreamSetDigitalOutputRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            channel_number=channel_number,
            value=value,
        )
        await call_async("device/stream_set_digital_output", request)

    def set_all_digital_outputs(
            self,
            values: List[DigitalOutputAction]
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetAllDigitalOutputs instead.

        Sets values for all digital output channels.

        Args:
            values: The type of action to perform on the channel.
        """
        request = dto.StreamSetAllDigitalOutputsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            values=values,
        )
        call("device/stream_set_all_digital_outputs", request)

    async def set_all_digital_outputs_async(
            self,
            values: List[DigitalOutputAction]
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetAllDigitalOutputs instead.

        Sets values for all digital output channels.

        Args:
            values: The type of action to perform on the channel.
        """
        request = dto.StreamSetAllDigitalOutputsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            values=values,
        )
        await call_async("device/stream_set_all_digital_outputs", request)

    def set_analog_output(
            self,
            channel_number: int,
            value: float
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetAnalogOutput instead.

        Sets value for the specified analog output channel.

        Args:
            channel_number: Channel number starting at 1.
            value: Value to set the output channel voltage to.
        """
        request = dto.StreamSetAnalogOutputRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            channel_number=channel_number,
            value=value,
        )
        call("device/stream_set_analog_output", request)

    async def set_analog_output_async(
            self,
            channel_number: int,
            value: float
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetAnalogOutput instead.

        Sets value for the specified analog output channel.

        Args:
            channel_number: Channel number starting at 1.
            value: Value to set the output channel voltage to.
        """
        request = dto.StreamSetAnalogOutputRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            channel_number=channel_number,
            value=value,
        )
        await call_async("device/stream_set_analog_output", request)

    def set_all_analog_outputs(
            self,
            values: List[float]
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetAllAnalogOutputs instead.

        Sets values for all analog output channels.

        Args:
            values: Voltage values to set the output channels to.
        """
        request = dto.StreamSetAllAnalogOutputsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            values=values,
        )
        call("device/stream_set_all_analog_outputs", request)

    async def set_all_analog_outputs_async(
            self,
            values: List[float]
    ) -> None:
        """
        Deprecated: Use PvtSequence.Io.SetAllAnalogOutputs instead.

        Sets values for all analog output channels.

        Args:
            values: Voltage values to set the output channels to.
        """
        request = dto.StreamSetAllAnalogOutputsRequest(
            interface_id=self.device.connection.interface_id,
            device=self.device.device_address,
            stream_id=self.pvt_id,
            pvt=True,
            values=values,
        )
        await call_async("device/stream_set_all_analog_outputs", request)
