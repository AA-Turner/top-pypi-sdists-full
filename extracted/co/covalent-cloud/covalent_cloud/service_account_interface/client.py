# Copyright 2023 Agnostiq Inc.

from typing import Optional

from covalent_cloud.shared.classes.api import DeploymentAPI, DispatcherAPI
from covalent_cloud.shared.classes.settings import Settings, settings


def get_client(settings: Optional[Settings] = settings) -> DispatcherAPI:
    """
    A factory / getter method for the Dispatcher API client.

    Args:
        settings: An instance of `Settings` class. Default is `settings`.

    Returns:
        An instance of `DispatcherAPI` client.

    """

    return DispatcherAPI(settings=settings)


def get_deployment_client(settings: Optional[Settings] = settings) -> DeploymentAPI:
    """
    A factory / getter method for the Deployment API client.

    Args:
        settings: An instance of `Settings` class. Default is `settings`.

    Returns:
        An instance of `DeploymentAPI` client.

    """

    return DeploymentAPI(settings=settings)
