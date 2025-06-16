"""
Main interface for ec2-instance-connect service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ec2_instance_connect/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ec2_instance_connect import (
        Client,
        EC2InstanceConnectClient,
    )

    session = get_session()
    async with session.create_client("ec2-instance-connect") as client:
        client: EC2InstanceConnectClient
        ...

    ```
"""

from .client import EC2InstanceConnectClient

Client = EC2InstanceConnectClient

__all__ = ("Client", "EC2InstanceConnectClient")
