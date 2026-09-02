import pytest

from novita_sandbox.core import AsyncVolume, Novita, Volume


def test_volume_create_is_disabled():
    with pytest.raises(
        NotImplementedError,
        match="Volume.create is deprecated and disabled",
    ):
        Volume.create("my-volume")


@pytest.mark.asyncio
async def test_async_volume_create_is_disabled():
    with pytest.raises(
        NotImplementedError,
        match="AsyncVolume.create is deprecated and disabled",
    ):
        await AsyncVolume.create("my-volume")


def test_novita_volume_create_is_disabled():
    novita = Novita(api_key="test-key")

    with pytest.raises(
        NotImplementedError,
        match="Volume.create is deprecated and disabled",
    ):
        novita.volume.create("my-volume")
