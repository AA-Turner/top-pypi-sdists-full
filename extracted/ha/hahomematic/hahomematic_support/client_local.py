"""The local client-object and its methods."""

from __future__ import annotations

from _collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
import importlib.resources
import logging
import os
from typing import Any, Final, cast

import orjson

from hahomematic.client import _LOGGER, Client, _ClientConfig
from hahomematic.const import (
    ADDRESS_SEPARATOR,
    DP_KEY_VALUE,
    UTF_8,
    WAIT_FOR_CALLBACK,
    CallSource,
    CommandRxMode,
    DescriptionMarker,
    DeviceDescription,
    Interface,
    ParameterData,
    ParamsetKey,
    ProductGroup,
    ProgramData,
    ProxyInitState,
    SystemInformation,
    SystemVariableData,
)
from hahomematic.decorators import inspector
from hahomematic.support import is_channel_address

LOCAL_SERIAL: Final = "0815_4711"
BACKEND_LOCAL: Final = "Local CCU"


class ClientLocal(Client):  # pragma: no cover
    """Local client object to provide access to locally stored files."""

    def __init__(self, client_config: _ClientConfig, local_resources: LocalRessources) -> None:
        """Initialize the Client."""
        super().__init__(client_config=client_config)
        self._local_resources = local_resources
        self._paramset_descriptions_cache: dict[str, dict[ParamsetKey, dict[str, ParameterData]]] = defaultdict(
            lambda: defaultdict(dict)
        )

    async def init_client(self) -> None:
        """Init the client."""
        self._system_information = await self._get_system_information()

    @property
    def available(self) -> bool:
        """Return the availability of the client."""
        return True

    @property
    def model(self) -> str:
        """Return the model of the backend."""
        return BACKEND_LOCAL

    def get_product_group(self, model: str) -> ProductGroup:
        """Return the product group."""
        l_model = model.lower()
        if l_model.startswith("hmipw"):
            return ProductGroup.HMIPW
        if l_model.startswith("hmip"):
            return ProductGroup.HMIP
        if l_model.startswith("hmw"):
            return ProductGroup.HMW
        if l_model.startswith("hm"):
            return ProductGroup.HM
        return ProductGroup.UNKNOWN

    @property
    def supports_ping_pong(self) -> bool:
        """Return the supports_ping_pong info of the backend."""
        return True

    @property
    def supports_push_updates(self) -> bool:
        """Return the client supports push update."""
        return True

    async def initialize_proxy(self) -> ProxyInitState:
        """Init the proxy has to tell the CCU / Homegear where to send the events."""
        return ProxyInitState.INIT_SUCCESS

    async def deinitialize_proxy(self) -> ProxyInitState:
        """De-init to stop CCU from sending events for this remote."""
        return ProxyInitState.DE_INIT_SUCCESS

    async def stop(self) -> None:
        """Stop depending services."""

    @inspector(re_raise=False, measure_performance=True)
    async def fetch_all_device_data(self) -> None:
        """Fetch all device data from CCU."""

    @inspector(re_raise=False, measure_performance=True)
    async def fetch_device_details(self) -> None:
        """Fetch names from backend."""

    @inspector(re_raise=False, no_raise_return=False)
    async def is_connected(self) -> bool:
        """
        Perform actions required for connectivity check.

        Connection is not connected, if three consecutive checks fail.
        Return connectivity state.
        """
        return True

    def is_callback_alive(self) -> bool:
        """Return if XmlRPC-Server is alive based on received events for this client."""
        return True

    @inspector(re_raise=False, no_raise_return=False)
    async def check_connection_availability(self, handle_ping_pong: bool) -> bool:
        """Send ping to CCU to generate PONG event."""
        if handle_ping_pong and self.supports_ping_pong:
            self._ping_pong_cache.handle_send_ping(ping_ts=datetime.now())
        return True

    @inspector()
    async def execute_program(self, pid: str) -> bool:
        """Execute a program on CCU / Homegear."""
        return True

    @inspector()
    async def set_program_state(self, pid: str, state: bool) -> bool:
        """Set the program state on CCU / Homegear."""
        return True

    @inspector(measure_performance=True)
    async def set_system_variable(self, legacy_name: str, value: Any) -> bool:
        """Set a system variable on CCU / Homegear."""
        return True

    @inspector()
    async def delete_system_variable(self, name: str) -> bool:
        """Delete a system variable from CCU / Homegear."""
        return True

    @inspector()
    async def get_system_variable(self, name: str) -> str:
        """Get single system variable from CCU / Homegear."""
        return "Empty"

    @inspector(re_raise=False)
    async def get_all_system_variables(
        self, markers: tuple[DescriptionMarker | str, ...]
    ) -> tuple[SystemVariableData, ...]:
        """Get all system variables from CCU / Homegear."""
        return ()

    @inspector(re_raise=False)
    async def get_all_programs(self, markers: tuple[DescriptionMarker | str, ...]) -> tuple[ProgramData, ...]:
        """Get all programs, if available."""
        return ()

    @inspector(re_raise=False, no_raise_return={})
    async def get_all_rooms(self) -> dict[str, set[str]]:
        """Get all rooms, if available."""
        return {}

    @inspector(re_raise=False, no_raise_return={})
    async def get_all_functions(self) -> dict[str, set[str]]:
        """Get all functions, if available."""
        return {}

    async def _get_system_information(self) -> SystemInformation:
        """Get system information of the backend."""
        return SystemInformation(available_interfaces=(Interface.BIDCOS_RF,), serial=LOCAL_SERIAL)

    @inspector(re_raise=False, measure_performance=True)
    async def list_devices(self) -> tuple[DeviceDescription, ...] | None:
        """Get device descriptions from CCU / Homegear."""
        if not self._local_resources:
            _LOGGER.warning(
                "LIST_DEVICES: missing local_resources in config for %s",
                self.central.name,
            )
            return None
        device_descriptions: list[DeviceDescription] = []
        if local_device_descriptions := cast(
            list[Any],
            await self._load_all_json_files(
                anchor=self._local_resources.anchor,
                resource=self._local_resources.device_description_dir,
                include_list=list(self._local_resources.address_device_translation.values()),
                exclude_list=self._local_resources.ignore_devices_on_create,
            ),
        ):
            for device_description in local_device_descriptions:
                device_descriptions.extend(device_description)
        return tuple(device_descriptions)

    @inspector(log_level=logging.NOTSET)
    async def get_value(
        self,
        channel_address: str,
        paramset_key: ParamsetKey,
        parameter: str,
        call_source: CallSource = CallSource.MANUAL_OR_SCHEDULED,
    ) -> Any:
        """Return a value from CCU."""
        return

    @inspector(re_raise=False, no_raise_return=set())
    async def set_value(
        self,
        channel_address: str,
        paramset_key: ParamsetKey,
        parameter: str,
        value: Any,
        wait_for_callback: int | None = WAIT_FOR_CALLBACK,
        rx_mode: CommandRxMode | None = None,
        check_against_pd: bool = False,
    ) -> set[DP_KEY_VALUE]:
        """Set single value on paramset VALUES."""
        # store the send value in the last_value_send_cache
        result = self._last_value_send_cache.add_set_value(
            channel_address=channel_address, parameter=parameter, value=value
        )
        # fire an event to fake the state change for a simple parameter
        await self.central.data_point_event(self.interface_id, channel_address, parameter, value)
        return result

    @inspector()
    async def get_paramset(
        self,
        address: str,
        paramset_key: ParamsetKey | str,
        call_source: CallSource = CallSource.MANUAL_OR_SCHEDULED,
    ) -> Any:
        """
        Return a paramset from CCU.

        Address is usually the channel_address,
        but for bidcos devices there is a master paramset at the device.
        """
        return {}

    async def _get_paramset_description(
        self, address: str, paramset_key: ParamsetKey
    ) -> dict[str, ParameterData] | None:
        """Get paramset description from CCU."""
        if not self._local_resources:
            _LOGGER.warning(
                "GET_PARAMSET_DESCRIPTION: missing local_resources in config for %s",
                self.central.name,
            )
            return None

        if (
            address not in self._paramset_descriptions_cache
            and (file_name := self._local_resources.address_device_translation.get(address.split(ADDRESS_SEPARATOR)[0]))
            and (
                data := await self._load_json_file(
                    anchor=self._local_resources.anchor,
                    resource=self._local_resources.paramset_description_dir,
                    filename=file_name,
                )
            )
        ):
            self._paramset_descriptions_cache.update(data)

        return self._paramset_descriptions_cache[address].get(paramset_key)

    @inspector(measure_performance=True)
    async def put_paramset(
        self,
        channel_address: str,
        paramset_key_or_link_address: ParamsetKey | str,
        values: Any,
        wait_for_callback: int | None = WAIT_FOR_CALLBACK,
        rx_mode: CommandRxMode | None = None,
        check_against_pd: bool = False,
    ) -> set[DP_KEY_VALUE]:
        """
        Set paramsets manually.

        Address is usually the channel_address,
        but for bidcos devices there is a master paramset at the device.
        """
        # store the send value in the last_value_send_cache
        if isinstance(paramset_key_or_link_address, str) and is_channel_address(address=paramset_key_or_link_address):
            result = set()
        else:
            result = self._last_value_send_cache.add_put_paramset(
                channel_address=channel_address,
                paramset_key=ParamsetKey(paramset_key_or_link_address),
                values=values,
            )

        # fire an event to fake the state change for the content of a paramset
        for parameter in values:
            await self.central.data_point_event(self.interface_id, channel_address, parameter, values[parameter])
        return result

    async def _load_all_json_files(
        self,
        anchor: str,
        resource: str,
        include_list: list[str] | None = None,
        exclude_list: list[str] | None = None,
    ) -> list[Any] | None:
        """Load all json files from disk into dict."""
        if not include_list:
            return []
        if not exclude_list:
            exclude_list = []
        result: list[Any] = []
        resource_path = os.path.join(str(importlib.resources.files(anchor)), resource)
        for filename in os.listdir(resource_path):
            if filename not in include_list or filename in exclude_list:
                continue
            if file_content := await self._load_json_file(anchor=anchor, resource=resource, filename=filename):
                result.append(file_content)
        return result

    async def _load_json_file(self, anchor: str, resource: str, filename: str) -> Any | None:
        """Load json file from disk into dict."""
        package_path = str(importlib.resources.files(anchor))

        def _perform_load() -> Any | None:
            with open(
                file=os.path.join(package_path, resource, filename),
                encoding=UTF_8,
            ) as fptr:
                return orjson.loads(fptr.read())

        return await self.central.looper.async_add_executor_job(_perform_load, name="load-json-file")


@dataclass(frozen=True, kw_only=True, slots=True)
class LocalRessources:
    """Dataclass with information for local client."""

    address_device_translation: dict[str, str]
    ignore_devices_on_create: list[str]
    anchor: str = "pydevccu"
    device_description_dir: str = "device_descriptions"
    paramset_description_dir: str = "paramset_descriptions"
