import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Any, Union

from pydantic import BaseModel, Field

from ipfabric.models.config_export import ExportConfig, ExportJob, ImportJob
from ipfabric.tools.shared import raise_for_status

logger = logging.getLogger("ipfabric")

CONFIG_OPTIONS = {
    "device-attributes",
    "jumphost",
    "oui",
    "discovery",
    "discovery-seeds",
    "device-credentials",
    "assurance-engine",
    "discovery-tasks",
    "vendors-api",
    "site-separation",
    "cli-settings",
    "bgp-routing",
    "snapshot-retention",
    "configuration-management",
    "api-tokens",
    "webhooks",
    "snmp",
    "certificates",
    "local-users",
    "ldap",
    "roles",
    "policies",
    "intent-checks",
    "dashboards-and-widgets",
}
CONFIG_ITEMS = set(sorted(CONFIG_OPTIONS.union({_.replace("-", "_") for _ in CONFIG_OPTIONS})))


class ApplianceConfiguration(BaseModel):
    client: Any = Field(description="IPFClient", exclude=True)

    @staticmethod
    def _create_options(
        passphrase: str,
        config_options: Union[ExportConfig, list[str], None],
        disable_options: Union[list[str], None] = None,
    ) -> ExportConfig:
        if len(passphrase) < 8:
            raise ValueError("Passphrase must be at least 8 characters long")
        if isinstance(config_options, list):
            if not all(item not in CONFIG_ITEMS for item in config_options):
                raise ValueError(f"Invalid configuration options: {set(config_options) - CONFIG_ITEMS}")
            config_options = ExportConfig(**{k: k in config_options for k in CONFIG_ITEMS})
        if config_options is None:
            config_options = ExportConfig()
        if disable_options is not None:
            if not all(item not in CONFIG_ITEMS for item in disable_options):
                raise ValueError(f"Invalid disabled configuration options: {set(disable_options) - CONFIG_ITEMS}")
            for k, v in ExportConfig(**{k: k not in disable_options for k in CONFIG_ITEMS}).model_dump().items():
                if v is False:
                    setattr(config_options, k, False)
        return config_options

    def export_config(
        self,
        passphrase: str,
        config_options: Union[ExportConfig, list[str], None] = None,
        disable_options: Union[list[str], None] = None,
        wait_for_export: bool = True,
        retry: int = 5,
        timeout: int = 5,
    ) -> Union[ExportJob, None]:
        """
        Export the current appliance configuration.

        Args:
            passphrase: str: 8 characters or longer string to encrypt the configuration.
            config_options: list: List of configuration options to export; None: export all; or ExportConfig object.
            disable_options: list: List of configuration options to disable export; None: export all
            wait_for_export: bool: Wait for the job to complete before returning
            timeout: int: How long in seconds to wait before retry
            retry: int: How many retries to use when looking for a job, increase for large downloads

        Returns: ExportJob: Job object with configuration data; None if an error occurred.
        """
        config_options = self._create_options(passphrase, config_options, disable_options)
        payload = {"passphrase": passphrase, **config_options.export()}
        started = round((datetime.now(timezone.utc) - timedelta(seconds=10)).timestamp() * 1000)
        raise_for_status(self.client.post("appliance-configuration/export", json=payload))
        # TODO: NIM-18675 v7.5
        job = self.client.jobs.find_job(started=started, action="export")
        if not job:
            return None
        if wait_for_export and (_ := self.client.jobs.return_job_when_done(job, retry=retry, timeout=timeout)):
            config = raise_for_status(self.client.get(f"jobs/{job.id}/download"))
            return ExportJob(job=_, config=config.json())
        return ExportJob(job=job, config=None)

    def import_config(
        self,
        passphrase: str,
        config: Union[dict, str, bytes],
        config_options: Union[ExportConfig, list[str], None] = None,
        disable_options: Union[list[str], None] = None,
        wait_for_import: bool = True,
        retry: int = 5,
        timeout: int = 5,
    ) -> Union[ImportJob, None]:
        """
        Export the current appliance configuration.

        Args:
            passphrase: str: 8 characters or longer string to encrypt the configuration.
            config: dict: Configuration data to import.
            config_options: list: List of configuration options to export; None: export all; or ExportConfig object.
            disable_options: list: List of configuration options to disable export; None: export all
            wait_for_import: bool: Wait for the job to complete before returning
            timeout: int: How long in seconds to wait before retry
            retry: int: How many retries to use when looking for a job, increase for large downloads

        Returns: ImportJob: Job object with configuration data; None if an error occurred.
        """
        config_options = self._create_options(passphrase, config_options, disable_options).export()[
            "configurationOptions"
        ]
        valid_options = set(config_options).intersection(set(config.keys()))
        if not valid_options:
            raise ValueError("No valid configuration options to be imported.")
        if valid_options != set(config_options):
            logger.warning(
                "The following settings were not in the configuration and will not be imported:\n"
                f"{json.dumps(list(set(config_options) - valid_options))}"
            )

        if isinstance(config, dict):
            config = json.dumps(config).encode("utf-8")
        config = config if isinstance(config, bytes) else config.encode("utf-8")
        files = [
            ("file", ("configurationExport.json", config, "application/json")),
            ("passphrase", (None, passphrase)),
            *[("configurationOptions[]", (None, v)) for v in valid_options],
        ]
        started = round((datetime.now(timezone.utc) - timedelta(seconds=10)).timestamp() * 1000)
        raise_for_status(self.client.post("appliance-configuration/import", files=files))
        # TODO: NIM-18675 v8.0
        job = self.client.jobs.find_job(started=started, action="import")
        if not job:
            return None
        if wait_for_import:
            _ = self.client.jobs.return_job_when_done(job, retry=retry, timeout=timeout)
            job = _ or self.client.jobs.get_job_by_id(job.id)
        return ImportJob(job=job)
