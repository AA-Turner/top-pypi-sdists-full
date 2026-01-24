import os
from pathlib import Path
from typing import Optional

from qwak.inner.const import QwakConstants
from qwak.inner.di_configuration import QwakContainer
from qwak.inner.tool.grpc.grpc_tools import validate_grpc_address
from qwak.tools.logger import get_qwak_logger


logger = get_qwak_logger()

__DEFAULT_CONFIG_FILE_PATH: Path = Path(__file__).parent / "config.yml"


def wire_dependencies():
    container = QwakContainer()

    container.config.from_yaml(__DEFAULT_CONFIG_FILE_PATH)
    control_plane_grpc_address_override: Optional[str] = os.getenv(
        QwakConstants.CONTROL_PLANE_GRPC_ADDRESS_ENVAR_NAME
    )

    if control_plane_grpc_address_override:
        validate_grpc_address(control_plane_grpc_address_override)
        __override_control_plane_grpc_address(
            container, control_plane_grpc_address_override
        )

    from qwak.clients import (
        administration,
        alert_management,
        alerts_registry,
        analytics,
        audience,
        automation_management,
        autoscaling,
        batch_job_management,
        build_orchestrator,
        data_versioning,
        deployment,
        feature_store,
        file_versioning,
        instance_template,
        integration_management,
        kube_deployment_captain,
        logging_client,
        model_management,
        project,
        prompt_manager,
        system_secret,
        user_application_instance,
        vector_store,
        workspace_manager,
    )

    container.wire(
        packages=[
            administration,
            alert_management,
            audience,
            automation_management,
            autoscaling,
            analytics,
            batch_job_management,
            build_orchestrator,
            data_versioning,
            deployment,
            file_versioning,
            instance_template,
            kube_deployment_captain,
            logging_client,
            model_management,
            project,
            feature_store,
            user_application_instance,
            alerts_registry,
            workspace_manager,
            vector_store,
            integration_management,
            system_secret,
            prompt_manager,
        ]
    )

    return container


def __override_control_plane_grpc_address(
    container: "QwakContainer", control_plane_grpc_address_override: str
):
    logger.debug(
        "Overriding control plane gRPC address from environment variable to %s.",
        control_plane_grpc_address_override,
    )
    container.config.grpc.core.address.from_value(
        control_plane_grpc_address_override.strip()
    )
