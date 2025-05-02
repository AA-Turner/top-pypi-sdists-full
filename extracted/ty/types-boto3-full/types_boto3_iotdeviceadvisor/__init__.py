"""
Main interface for iotdeviceadvisor service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iotdeviceadvisor/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iotdeviceadvisor import (
        Client,
        IoTDeviceAdvisorClient,
    )

    session = Session()
    client: IoTDeviceAdvisorClient = session.client("iotdeviceadvisor")
    ```
"""

from .client import IoTDeviceAdvisorClient

Client = IoTDeviceAdvisorClient


__all__ = ("Client", "IoTDeviceAdvisorClient")
