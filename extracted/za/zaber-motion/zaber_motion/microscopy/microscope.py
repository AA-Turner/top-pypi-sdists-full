# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import Optional
from ..call import call, call_async, call_sync
from ..dto import requests as dto
from ..ascii import Connection, Device, Axis, AxisGroup
from .illuminator import Illuminator
from .filter_changer import FilterChanger
from .objective_changer import ObjectiveChanger
from .autofocus import Autofocus
from .camera_trigger import CameraTrigger
from ..dto.microscopy.microscope_config import MicroscopeConfig
from ..dto.microscopy.third_party_components import ThirdPartyComponents


class Microscope:
    """
    Represent a microscope.
    Parts of the microscope may or may not be instantiated depending on the configuration.
    Requires at least Firmware 7.34.
    """

    @property
    def connection(self) -> Connection:
        """
        Connection of the microscope.
        """
        return self._connection

    @property
    def illuminator(self) -> Optional[Illuminator]:
        """
        The illuminator.
        """
        return self._illuminator

    @property
    def focus_axis(self) -> Optional[Axis]:
        """
        The focus axis.
        """
        return self._focus_axis

    @property
    def x_axis(self) -> Optional[Axis]:
        """
        The X axis.
        """
        return self._x_axis

    @property
    def y_axis(self) -> Optional[Axis]:
        """
        The Y axis.
        """
        return self._y_axis

    @property
    def plate(self) -> Optional[AxisGroup]:
        """
        Axis group consisting of X and Y axes representing the plate of the microscope.
        """
        return self._plate

    @property
    def objective_changer(self) -> Optional[ObjectiveChanger]:
        """
        The objective changer.
        """
        return self._objective_changer

    @property
    def filter_changer(self) -> Optional[FilterChanger]:
        """
        The filter changer.
        """
        return self._filter_changer

    @property
    def autofocus(self) -> Optional[Autofocus]:
        """
        The autofocus feature.
        """
        return self._autofocus

    @property
    def camera_trigger(self) -> Optional[CameraTrigger]:
        """
        The camera trigger.
        """
        return self._camera_trigger

    def __init__(self, connection: Connection, config: MicroscopeConfig):
        """
        Creates instance of `Microscope` from the given config.
        Parts are instantiated depending on device addresses in the config.
        """
        self._connection: Connection = connection
        self._config: MicroscopeConfig = MicroscopeConfig.from_binary(MicroscopeConfig.to_binary(config))
        self._illuminator: Optional[Illuminator] = Illuminator(Device(connection, config.illuminator))\
            if config.illuminator else None
        self._focus_axis: Optional[Axis] = Axis(Device(connection, config.focus_axis.device), config.focus_axis.axis)\
            if config.focus_axis and config.focus_axis.device else None
        self._x_axis: Optional[Axis] = Axis(Device(connection, config.x_axis.device), config.x_axis.axis)\
            if config.x_axis and config.x_axis.device else None
        self._y_axis: Optional[Axis] = Axis(Device(connection, config.y_axis.device), config.y_axis.axis)\
            if config.y_axis and config.y_axis.device else None
        self._plate: Optional[AxisGroup] = AxisGroup([self._x_axis, self._y_axis])\
            if self._x_axis is not None and self._y_axis is not None else None
        self._objective_changer: Optional[ObjectiveChanger] = ObjectiveChanger(
            Device(connection, config.objective_changer),
            self._focus_axis)\
            if config.objective_changer and self._focus_axis else None
        self._filter_changer: Optional[FilterChanger] = FilterChanger(Device(connection, config.filter_changer))\
            if config.filter_changer else None
        self._autofocus: Optional[Autofocus] = Autofocus(
            config.autofocus,
            self._focus_axis,
            self._objective_changer.turret if self._objective_changer else None)\
            if config.autofocus and self._focus_axis else None
        self._camera_trigger: Optional[CameraTrigger] = CameraTrigger(
            Device(connection, config.camera_trigger.device),
            config.camera_trigger.channel)\
            if config.camera_trigger and config.camera_trigger.device else None

    @staticmethod
    def find(
            connection: Connection,
            third_party_components: Optional[ThirdPartyComponents] = None
    ) -> 'Microscope':
        """
        Finds a microscope on a connection.

        Args:
            connection: Connection on which to detect the microscope.
            third_party_components: Third party components of the microscope that cannot be found on the connection.

        Returns:
            New instance of microscope.
        """
        request = dto.MicroscopeFindRequest(
            interface_id=connection.interface_id,
            third_party=third_party_components,
        )
        response = call(
            "microscope/detect",
            request,
            dto.MicroscopeConfigResponse.from_binary)
        return Microscope(connection, response.config)

    @staticmethod
    async def find_async(
            connection: Connection,
            third_party_components: Optional[ThirdPartyComponents] = None
    ) -> 'Microscope':
        """
        Finds a microscope on a connection.

        Args:
            connection: Connection on which to detect the microscope.
            third_party_components: Third party components of the microscope that cannot be found on the connection.

        Returns:
            New instance of microscope.
        """
        request = dto.MicroscopeFindRequest(
            interface_id=connection.interface_id,
            third_party=third_party_components,
        )
        response = await call_async(
            "microscope/detect",
            request,
            dto.MicroscopeConfigResponse.from_binary)
        return Microscope(connection, response.config)

    def initialize(
            self,
            force: bool = False
    ) -> None:
        """
        Initializes the microscope.
        Homes all axes, filter changer, and objective changer if they require it.

        Args:
            force: Forces all devices to home even when not required.
        """
        request = dto.MicroscopeInitRequest(
            interface_id=self.connection.interface_id,
            config=self._config,
            force=force,
        )
        call("microscope/initialize", request)

    async def initialize_async(
            self,
            force: bool = False
    ) -> None:
        """
        Initializes the microscope.
        Homes all axes, filter changer, and objective changer if they require it.

        Args:
            force: Forces all devices to home even when not required.
        """
        request = dto.MicroscopeInitRequest(
            interface_id=self.connection.interface_id,
            config=self._config,
            force=force,
        )
        await call_async("microscope/initialize", request)

    def is_initialized(
            self
    ) -> bool:
        """
        Checks whether the microscope is initialized.

        Returns:
            True, when the microscope is initialized. False, otherwise.
        """
        request = dto.MicroscopeEmptyRequest(
            interface_id=self.connection.interface_id,
            config=self._config,
        )
        response = call(
            "microscope/is_initialized",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    async def is_initialized_async(
            self
    ) -> bool:
        """
        Checks whether the microscope is initialized.

        Returns:
            True, when the microscope is initialized. False, otherwise.
        """
        request = dto.MicroscopeEmptyRequest(
            interface_id=self.connection.interface_id,
            config=self._config,
        )
        response = await call_async(
            "microscope/is_initialized",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    def __repr__(
            self
    ) -> str:
        """
        Returns a string that represents the microscope.

        Returns:
            A string that represents the microscope.
        """
        request = dto.MicroscopeEmptyRequest(
            interface_id=self.connection.interface_id,
            config=self._config,
        )
        response = call_sync(
            "microscope/to_string",
            request,
            dto.StringResponse.from_binary)
        return response.value
