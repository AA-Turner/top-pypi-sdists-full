from typing import Dict, Optional

from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort


class AirflowService:
    def __init__(
        self,
        config: Config,
        command_name: str,
        user_service: Optional[UserService] = None,
    ):
        self._command_name = command_name
        self._user_service = user_service or UserService(
            config=config,
            command_name=self._command_name,
        )

    def get_airflow_resource_uuid(self, name: Optional[str] = None) -> Optional[str]:
        etl_containers = self._user_service.etl_containers or []
        airflow_containers = [
            container for container in etl_containers if self._is_airflow_container(container, name)
        ]
        if not airflow_containers:
            if name:
                complain_and_abort(f"No Airflow connection found with name {name}")
            else:
                complain_and_abort("No Airflow connection found")
            return None
        elif len(airflow_containers) > 1:
            if name:
                complain_and_abort(f"Multiple Airflow connections found with name {name}")
            else:
                complain_and_abort("Multiple Airflow connections found, use --name to disambiguate")
            return None
        return airflow_containers[0].get("uuid")

    @staticmethod
    def _is_airflow_container(container: Dict, name: Optional[str]) -> bool:
        if name and name != container["name"]:
            return False
        connections = container.get("connections", [])
        return any(connection for connection in connections if connection["type"] == "AIRFLOW")
