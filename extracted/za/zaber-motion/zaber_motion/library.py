# ===== THIS FILE IS GENERATED FROM A TEMPLATE ===== #
# ============== DO NOT EDIT DIRECTLY ============== #

from typing import Optional
from .call import call, call_async, call_sync
from .dto import requests as dto
from .dto.log_output_mode import LogOutputMode
from .dto.device_db_source_type import DeviceDbSourceType


class Library:
    """
    Access class to general library information and configuration.
    """

    @staticmethod
    def set_log_output(
            mode: LogOutputMode,
            file_path: Optional[str] = None
    ) -> None:
        """
        Sets library logging output.

        Args:
            mode: Logging output mode.
            file_path: Path of the file to open.
        """
        request = dto.SetLogOutputRequest(
            mode=mode,
            file_path=file_path,
        )
        call_sync("logging/set_output", request)

    @staticmethod
    def set_device_db_source(
            source_type: DeviceDbSourceType,
            url_or_file_path: Optional[str] = None
    ) -> None:
        """
        Sets source of Device DB data. Allows selection of a web service or a local file.

        Args:
            source_type: Source type.
            url_or_file_path: URL of the web service or path to the local file.
                Leave empty for the default URL of Zaber web service.
        """
        request = dto.SetDeviceDbSourceRequest(
            source_type=source_type,
            url_or_file_path=url_or_file_path,
        )
        call_sync("device_db/set_source", request)

    @staticmethod
    def enable_device_db_store(
            store_location: Optional[str] = None
    ) -> None:
        """
        Enables Device DB store.
        The store uses filesystem to save information obtained from the Device DB.
        The stored data are later used instead of the Device DB.

        Args:
            store_location: Specifies relative or absolute path of the folder used by the store.
                If left empty defaults to a folder in user home directory.
                Must be accessible by the process.
        """
        request = dto.ToggleDeviceDbStoreRequest(
            toggle_on=True,
            store_location=store_location,
        )
        call_sync("device_db/toggle_store", request)

    @staticmethod
    def disable_device_db_store() -> None:
        """
        Disables Device DB store.
        """
        request = dto.ToggleDeviceDbStoreRequest(
        )
        call_sync("device_db/toggle_store", request)

    @staticmethod
    def is_device_db_store_enabled() -> bool:
        """
        Checks if the Device DB store is currently enabled.

        Returns:
            True if the Device DB store is enabled.
        """
        request = dto.EmptyRequest(
        )
        response = call_sync(
            "device_db/check_store",
            request,
            dto.BoolResponse.from_binary)
        return response.value

    @staticmethod
    def clear_device_db_store() -> None:
        """
        Clears the Device DB store on the local filesystem.
        Note: If the device DB was enabled with a custom store location, store files will be removed in that location.
        """
        request = dto.EmptyRequest(
        )
        call("device_db/clear_store", request)

    @staticmethod
    async def clear_device_db_store_async() -> None:
        """
        Clears the Device DB store on the local filesystem.
        Note: If the device DB was enabled with a custom store location, store files will be removed in that location.
        """
        request = dto.EmptyRequest(
        )
        await call_async("device_db/clear_store", request)

    @staticmethod
    def set_internal_mode(
            mode: bool
    ) -> None:
        """
        Disables certain customer checks (like FF flag).

        Args:
            mode: Whether to turn internal mode on or off.
        """
        request = dto.SetInternalModeRequest(
            mode=mode,
        )
        call_sync("library/set_internal_mode", request)

    @staticmethod
    def set_idle_polling_period(
            period: int
    ) -> None:
        """
        Sets the period between polling for IDLE during movements.
        Caution: Setting the period too low may cause performance issues.

        Args:
            period: Period in milliseconds.
                Negative value restores the default period.
        """
        request = dto.IntRequest(
            value=period,
        )
        call_sync("library/set_idle_polling_period", request)

    @staticmethod
    def check_version() -> None:
        """
        Throws an error if the version of the loaded shared library does not match the caller's version.
        """
        request = dto.CheckVersionRequest(
            host="py",
            version="7.9.1",
        )
        call_sync("library/check_version", request)


Library.check_version()
