"""
Main interface for iot-jobs-data service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_jobs_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iot_jobs_data import (
        Client,
        IoTJobsDataPlaneClient,
    )

    session = get_session()
    async with session.create_client("iot-jobs-data") as client:
        client: IoTJobsDataPlaneClient
        ...

    ```
"""

from .client import IoTJobsDataPlaneClient

Client = IoTJobsDataPlaneClient


__all__ = ("Client", "IoTJobsDataPlaneClient")
