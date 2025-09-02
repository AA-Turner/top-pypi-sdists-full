from typing import Union, Any

from pydantic import BaseModel, Field, AliasChoices, ConfigDict, AliasGenerator

from ipfabric.models.jobs import Job


class ExportConfig(BaseModel):
    model_config = ConfigDict(
        alias_generator=AliasGenerator(
            serialization_alias=lambda field_name: field_name.replace("_", "-"),
        )
    )
    device_attributes: bool = Field(True, validation_alias=AliasChoices("device-attributes", "device_attributes"))
    jumphost: bool = True
    oui: bool = True
    discovery: bool = True
    discovery_seeds: bool = Field(True, validation_alias=AliasChoices("discovery-seeds", "discovery_seeds"))
    device_credentials: bool = Field(True, validation_alias=AliasChoices("device-credentials", "device_credentials"))
    assurance_engine: bool = Field(True, validation_alias=AliasChoices("assurance-engine", "assurance_engine"))
    discovery_tasks: bool = Field(True, validation_alias=AliasChoices("discovery-tasks", "discovery_tasks"))
    vendors_api: bool = Field(True, validation_alias=AliasChoices("vendors-api", "vendors_api"))
    site_separation: bool = Field(True, validation_alias=AliasChoices("site-separation", "site_separation"))
    cli_settings: bool = Field(True, validation_alias=AliasChoices("cli-settings", "cli_settings"))
    bgp_routing: bool = Field(True, validation_alias=AliasChoices("bgp-routing", "bgp_routing"))
    snapshot_retention: bool = Field(True, validation_alias=AliasChoices("snapshot-retention", "snapshot_retention"))
    configuration_management: bool = Field(
        True, validation_alias=AliasChoices("configuration-management", "configuration_management")
    )
    api_tokens: bool = Field(True, validation_alias=AliasChoices("api-tokens", "api_tokens"))
    webhooks: bool = True
    snmp: bool = True
    certificates: bool = True
    local_users: bool = Field(True, validation_alias=AliasChoices("local-users", "local_users"))
    ldap: bool = True
    roles: bool = True
    policies: bool = True
    intent_checks: bool = Field(True, validation_alias=AliasChoices("intent_checks", "intent_checks"))
    dashboards_and_widgets: bool = Field(
        True, validation_alias=AliasChoices("dashboards-and-widgets", "dashboards_and_widgets")
    )

    def export(self) -> dict[str, Any]:
        return {
            "configurationOptions": [k for k, v in self.model_dump(by_alias=True).items() if v is True],
        }


class ImportJob(BaseModel):
    job: Job

    @property
    def job_completed(self):
        return self.job.isDone is True and self.job.status == "done"


class ExportJob(ImportJob, BaseModel):
    config: Union[dict, None] = None
