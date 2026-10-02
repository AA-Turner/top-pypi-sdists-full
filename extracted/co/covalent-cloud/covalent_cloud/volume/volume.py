# Copyright 2023 Agnostiq Inc.


from typing import Optional

from covalent_cloud.service_account_interface.client import get_client
from covalent_cloud.shared.classes.exceptions import handle_error
from covalent_cloud.shared.classes.settings import Settings, settings
from covalent_cloud.shared.schemas.volume import BaseVolume, Volume


def volume(
    name: str, vtype: Optional[str] = "OBJECT_STORAGE", settings: Optional[Settings] = settings
) -> Volume:
    """
    Creates or retrieves a persistent storage volume in Covalent Cloud. This function is used to manage volumes that provide persistent storage to workflow tasks, allowing them to read and write data across multiple workflow executions.

    The volumes are user-specific and remain available indefinitely until explicitly deleted. They are especially useful for workflows that require access to large datasets or need to maintain state between different executions.

    Args:
        name (str): The name of the volume. This name is used to create a new volume or retrieve an existing one.
        settings (Settings, optional): Configuration settings for connecting to the Covalent Cloud. Defaults to None, which uses the default settings.

    Returns:
        Volume: An object representing the created or retrieved volume.

    Examples:
        .. highlight:: python
        .. code-block:: python

            import covalent_cloud as cc
            import covalent as ct
            from covalent_cloud import volume

            # Creating a new volume
            my_volume = cc.volume("/mydata") # This will create a new volume named "/mydata" if it does not already exist.

            # Using the volume in a workflow

            # Define the workflow (here it is a single task workflow)
            @ct.lattice
            @ct.electron
            def my_workflow(x, y):
                # Workflow logic here to use "./mydata" volume
                pass

            # Dispatch the workflow with the volume
            run_id = cc.dispatch(my_workflow, volume=my_volume)(x=1, y=2)
            # The workflow now has access to the "/mydata" volume for persistent storage.
    """

    try:
        # will check if name is valid else throw error
        volume = BaseVolume(name=name)

        # should be valid name without any slashes since the validator cleaned it
        volume_name = volume.name

        client = get_client(settings)
        response = client.post(
            "/api/v2/volumes", request_options={"json": {"name": volume_name, "vtype": vtype}}
        )

        data = response.json()
        volume = Volume(**data)
        return volume
    except Exception as e:
        handle_error(e)
