"""
Main interface for iot-jobs-data service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iot_jobs_data/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iot_jobs_data import (
        Client,
        IoTJobsDataPlaneClient,
    )

    session = Session()
    client: IoTJobsDataPlaneClient = session.client("iot-jobs-data")
    ```
"""

from .client import IoTJobsDataPlaneClient

Client = IoTJobsDataPlaneClient


__all__ = ("Client", "IoTJobsDataPlaneClient")
