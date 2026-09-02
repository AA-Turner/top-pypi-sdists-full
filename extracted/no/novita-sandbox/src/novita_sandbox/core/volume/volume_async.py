from typing import List, Optional

from typing_extensions import Unpack

from novita_sandbox.core.api import handle_api_exception
from novita_sandbox.core.api.client.api.volumes import (
    get_volumes,
    get_volumes_volume_id,
    delete_volumes_volume_id,
)
from novita_sandbox.core.api.client.models import Error
from novita_sandbox.core.api.client_async import get_api_client as get_core_api_client
from novita_sandbox.core.compat import raise_if_legacy
from novita_sandbox.core.connection_config import (
    ApiParams,
    ConnectionConfig,
    validate_domain,
)
from novita_sandbox.core.exceptions import NotFoundException, VolumeException
from novita_sandbox.core.volume.types import (
    VolumeAndToken,
    VolumeInfo,
)


def _api_field(obj, attr_name: str, json_name: str, default=0):
    value = getattr(obj, attr_name, None)
    if value is not None:
        return value

    return getattr(obj, "additional_properties", {}).get(json_name, default) or default


class AsyncVolume:
    """Novita AI sandbox Volume for persistent storage that can be mounted to sandboxes (async)."""

    def __init__(
        self,
        volume_id: str,
        name: str,
        token: Optional[str] = None,
        domain: Optional[str] = None,
        debug: Optional[bool] = None,
    ):
        if domain is not None:
            validate_domain(domain)
        self._volume_id = volume_id
        self._name = name
        self._token = token
        self._domain = domain
        self._debug = debug

    @property
    def volume_id(self) -> str:
        return self._volume_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def token(self) -> Optional[str]:
        return self._token

    @classmethod
    async def create(cls, name: str, quota_size_gib: Optional[int] = None, quota_inodes: Optional[int] = None, **opts: Unpack[ApiParams]) -> "AsyncVolume":
        """
        Create a new volume.

        Deprecated: volume creation is disabled.

        :param name: Name of the volume
        :param quota_size_gib: Capacity quota in GiB
        :param quota_inodes: Inode quota

        :return: An AsyncVolume instance for the new volume
        """
        raise NotImplementedError(
            "AsyncVolume.create is deprecated and disabled. Use an existing volume instead."
        )

    @classmethod
    async def connect(cls, volume_id: str, **opts: Unpack[ApiParams]) -> "AsyncVolume":
        """
        Connect to an existing volume by ID.

        :param volume_id: Volume ID

        :return: An AsyncVolume instance for the existing volume
        """
        info = await cls.get_info(volume_id, **opts)
        config = ConnectionConfig(**opts)
        return cls(
            volume_id=volume_id,
            name=info.name,
            token=info.token,
            domain=config.domain,
            debug=config.debug,
        )

    @staticmethod
    async def get_info(volume_id: str, **opts: Unpack[ApiParams]) -> VolumeAndToken:
        """
        Get information about a volume.

        :param volume_id: Volume ID

        :return: Volume info
        """
        raise_if_legacy(opts, "AsyncVolume.get_info")

        config = ConnectionConfig(**opts)

        api_client = get_core_api_client(config)
        res = await get_volumes_volume_id.asyncio_detailed(
            volume_id,
            client=api_client,
        )

        if res.status_code == 404:
            raise NotFoundException(f"Volume {volume_id} not found")

        if res.status_code >= 300:
            raise handle_api_exception(res, VolumeException)

        if res.parsed is None:
            raise Exception("Body of the request is None")

        if isinstance(res.parsed, Error):
            raise Exception(f"{res.parsed.message}: Request failed")

        return VolumeAndToken(
            volume_id=res.parsed.volume_id,
            name=res.parsed.name,
            token=res.parsed.token,
            quota_size_gib=_api_field(res.parsed, "quota_size_gib", "quotaSizeGiB"),
            quota_inodes=_api_field(res.parsed, "quota_inodes", "quotaInodes"),
            used_size_bytes=_api_field(res.parsed, "used_size_bytes", "usedSizeBytes"),
            used_inodes=_api_field(res.parsed, "used_inodes", "usedInodes"),
        )

    @staticmethod
    async def list(**opts: Unpack[ApiParams]) -> List[VolumeInfo]:
        """
        List all volumes.

        :return: List of volumes
        """
        raise_if_legacy(opts, "AsyncVolume.list")

        config = ConnectionConfig(**opts)
        api_client = get_core_api_client(config)
        res = await get_volumes.asyncio_detailed(
            client=api_client,
        )

        if res.status_code >= 300:
            raise handle_api_exception(res, VolumeException)

        if res.parsed is None:
            return []

        if isinstance(res.parsed, Error):
            raise Exception(f"{res.parsed.message}: Request failed")

        return [
            VolumeInfo(
                volume_id=v.volume_id,
                name=v.name,
                quota_size_gib=_api_field(v, "quota_size_gib", "quotaSizeGiB"),
                quota_inodes=_api_field(v, "quota_inodes", "quotaInodes"),
                used_size_bytes=_api_field(v, "used_size_bytes", "usedSizeBytes"),
                used_inodes=_api_field(v, "used_inodes", "usedInodes"),
            )
            for v in res.parsed
        ]

    @staticmethod
    async def update_quota(volume_id: str, quota_size_gib: Optional[int] = None, quota_inodes: Optional[int] = None, **opts: Unpack[ApiParams]) -> VolumeAndToken:
        """
        Update volume quota.

        :param volume_id: Volume ID
        :param quota_size_gib: Capacity quota in GiB
        :param quota_inodes: Inode quota

        :return: Updated volume information
        """
        raise_if_legacy(opts, "AsyncVolume.update_quota")

        config = ConnectionConfig(**opts)
        api_client = get_core_api_client(config)
        body = {}
        if quota_size_gib is not None:
            body["quotaSizeGiB"] = quota_size_gib
        if quota_inodes is not None:
            body["quotaInodes"] = quota_inodes

        async_client = api_client.get_async_httpx_client()
        res = await async_client.patch(
            f"{config.api_url}/volumes/{volume_id}",
            json=body,
            headers=config.sandbox_headers,
        )

        if res.status_code == 404:
            raise NotFoundException(f"Volume {volume_id} not found")

        if res.status_code >= 300:
            raise VolumeException(f"{res.status_code}: {await res.aread()}")

        data = res.json()
        return VolumeAndToken(
            volume_id=data["volumeID"],
            name=data["name"],
            token=data.get("token", ""),
            quota_size_gib=data.get("quotaSizeGiB", 0) or 0,
            quota_inodes=data.get("quotaInodes", 0) or 0,
            used_size_bytes=data.get("usedSizeBytes", 0) or 0,
            used_inodes=data.get("usedInodes", 0) or 0,
        )

    @staticmethod
    async def destroy(volume_id: str, **opts: Unpack[ApiParams]) -> bool:
        """
        Destroy a volume.

        :param volume_id: Volume ID
        """
        raise_if_legacy(opts, "AsyncVolume.destroy")

        config = ConnectionConfig(**opts)

        api_client = get_core_api_client(config)
        res = await delete_volumes_volume_id.asyncio_detailed(
            volume_id,
            client=api_client,
        )

        if res.status_code == 404:
            return False

        if res.status_code >= 300:
            raise handle_api_exception(res, VolumeException)

        return True
