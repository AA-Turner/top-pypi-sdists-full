"""
Type annotations for nimble service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_nimble.client import NimbleStudioClient
    from types_aiobotocore_nimble.waiter import (
        LaunchProfileDeletedWaiter,
        LaunchProfileReadyWaiter,
        StreamingImageDeletedWaiter,
        StreamingImageReadyWaiter,
        StreamingSessionDeletedWaiter,
        StreamingSessionReadyWaiter,
        StreamingSessionStoppedWaiter,
        StreamingSessionStreamReadyWaiter,
        StudioComponentDeletedWaiter,
        StudioComponentReadyWaiter,
        StudioDeletedWaiter,
        StudioReadyWaiter,
    )

    session = get_session()
    async with session.create_client("nimble") as client:
        client: NimbleStudioClient

        launch_profile_deleted_waiter: LaunchProfileDeletedWaiter = client.get_waiter("launch_profile_deleted")
        launch_profile_ready_waiter: LaunchProfileReadyWaiter = client.get_waiter("launch_profile_ready")
        streaming_image_deleted_waiter: StreamingImageDeletedWaiter = client.get_waiter("streaming_image_deleted")
        streaming_image_ready_waiter: StreamingImageReadyWaiter = client.get_waiter("streaming_image_ready")
        streaming_session_deleted_waiter: StreamingSessionDeletedWaiter = client.get_waiter("streaming_session_deleted")
        streaming_session_ready_waiter: StreamingSessionReadyWaiter = client.get_waiter("streaming_session_ready")
        streaming_session_stopped_waiter: StreamingSessionStoppedWaiter = client.get_waiter("streaming_session_stopped")
        streaming_session_stream_ready_waiter: StreamingSessionStreamReadyWaiter = client.get_waiter("streaming_session_stream_ready")
        studio_component_deleted_waiter: StudioComponentDeletedWaiter = client.get_waiter("studio_component_deleted")
        studio_component_ready_waiter: StudioComponentReadyWaiter = client.get_waiter("studio_component_ready")
        studio_deleted_waiter: StudioDeletedWaiter = client.get_waiter("studio_deleted")
        studio_ready_waiter: StudioReadyWaiter = client.get_waiter("studio_ready")
    ```
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef,
    GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef,
    GetStreamingImageRequestStreamingImageDeletedWaitTypeDef,
    GetStreamingImageRequestStreamingImageReadyWaitTypeDef,
    GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef,
    GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef,
    GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef,
    GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef,
    GetStudioComponentRequestStudioComponentDeletedWaitTypeDef,
    GetStudioComponentRequestStudioComponentReadyWaitTypeDef,
    GetStudioRequestStudioDeletedWaitTypeDef,
    GetStudioRequestStudioReadyWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "LaunchProfileDeletedWaiter",
    "LaunchProfileReadyWaiter",
    "StreamingImageDeletedWaiter",
    "StreamingImageReadyWaiter",
    "StreamingSessionDeletedWaiter",
    "StreamingSessionReadyWaiter",
    "StreamingSessionStoppedWaiter",
    "StreamingSessionStreamReadyWaiter",
    "StudioComponentDeletedWaiter",
    "StudioComponentReadyWaiter",
    "StudioDeletedWaiter",
    "StudioReadyWaiter",
)

class LaunchProfileDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#launchprofiledeletedwaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetLaunchProfileRequestLaunchProfileDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#launchprofiledeletedwaiter)
        """

class LaunchProfileReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#launchprofilereadywaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetLaunchProfileRequestLaunchProfileReadyWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.LaunchProfileReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#launchprofilereadywaiter)
        """

class StreamingImageDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingimagedeletedwaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStreamingImageRequestStreamingImageDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingimagedeletedwaiter)
        """

class StreamingImageReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingimagereadywaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStreamingImageRequestStreamingImageReadyWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingImageReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingimagereadywaiter)
        """

class StreamingSessionDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessiondeletedwaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStreamingSessionRequestStreamingSessionDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessiondeletedwaiter)
        """

class StreamingSessionReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessionreadywaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStreamingSessionRequestStreamingSessionReadyWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessionreadywaiter)
        """

class StreamingSessionStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessionstoppedwaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStreamingSessionRequestStreamingSessionStoppedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessionstoppedwaiter)
        """

class StreamingSessionStreamReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStreamReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessionstreamreadywaiter)
    """
    async def wait(
        self,
        **kwargs: Unpack[GetStreamingSessionStreamRequestStreamingSessionStreamReadyWaitTypeDef],
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StreamingSessionStreamReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#streamingsessionstreamreadywaiter)
        """

class StudioComponentDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studiocomponentdeletedwaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStudioComponentRequestStudioComponentDeletedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studiocomponentdeletedwaiter)
        """

class StudioComponentReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studiocomponentreadywaiter)
    """
    async def wait(
        self, **kwargs: Unpack[GetStudioComponentRequestStudioComponentReadyWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioComponentReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studiocomponentreadywaiter)
        """

class StudioDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studiodeletedwaiter)
    """
    async def wait(self, **kwargs: Unpack[GetStudioRequestStudioDeletedWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studiodeletedwaiter)
        """

class StudioReadyWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioReady)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studioreadywaiter)
    """
    async def wait(self, **kwargs: Unpack[GetStudioRequestStudioReadyWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nimble.html#NimbleStudio.Waiter.StudioReady.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nimble/waiters/#studioreadywaiter)
        """
