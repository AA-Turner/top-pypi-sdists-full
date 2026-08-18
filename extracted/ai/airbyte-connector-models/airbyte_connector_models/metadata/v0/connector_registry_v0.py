# Copyright (c) 2025 Airbyte, Inc., all rights reserved.


from __future__ import annotations

from datetime import date
from enum import Enum
from typing import Annotated, Any, Literal
from uuid import UUID

from pydantic import AnyUrl, AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class AllowedHosts(BaseModel):
    """
    A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    hosts: Annotated[
        list[str] | None,
        Field(
            description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted."
        ),
    ] = None


class StreamBreakingChangeScope(BaseModel):
    """
    A scope that can be used to limit the impact of a breaking change to specific streams.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    scope_type: Annotated[Literal["stream"], Field(alias="scopeType")]
    impacted_scopes: Annotated[
        list[str],
        Field(
            alias="impactedScopes",
            description="List of streams that are impacted by the breaking change.",
            min_length=1,
        ),
    ]


class BreakingChangeScope(RootModel[StreamBreakingChangeScope]):
    root: Annotated[
        StreamBreakingChangeScope,
        Field(description="A scope that can be used to limit the impact of a breaking change."),
    ]


class ConnectorRegistryV0(BaseModel):
    """
    describes the collection of connectors retrieved from a registry
    """

    destinations: list[ConnectorRegistryV0ConnectorRegistryDestinationDefinition]
    sources: list[ConnectorRegistryV0ConnectorRegistrySourceDefinition]


class ResourceRequirements(BaseModel):
    """
    generic configuration for pod source requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    cpu_request: str | None = None
    cpu_limit: str | None = None
    memory_request: str | None = None
    memory_limit: str | None = None


class ConnectorRegistryV0ActorDefinitionResourceRequirements(BaseModel):
    """
    actor definition specific resource requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    default: Annotated[
        ResourceRequirements | None,
        Field(
            description="if set, these are the requirements that should be set for ALL jobs run for this actor definition."
        ),
    ] = None
    job_specific: Annotated[list[JobTypeResourceLimit] | None, Field(alias="jobSpecific")] = None


class ConnectorRegistryV0AirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorRegistryV0AirbyteInternalSl | None = None
    ql: ConnectorRegistryV0AirbyteInternalQl | None = None
    is_enterprise: Annotated[bool | None, Field(alias="isEnterprise")] = False
    require_version_increments_in_pull_requests: Annotated[
        bool | None,
        Field(
            alias="requireVersionIncrementsInPullRequests",
            description="When false, version increment checks will be skipped for this connector",
        ),
    ] = True


class ConnectorRegistryV0AirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorRegistryV0AirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorRegistryV0ConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None


class ConnectorRegistryV0ConnectorRegistryDestinationDefinition(BaseModel):
    """
    describes a destination
    """

    model_config = ConfigDict(
        extra="allow",
    )
    destination_definition_id: Annotated[UUID, Field(alias="destinationDefinitionId")]
    name: str
    docker_repository: Annotated[str, Field(alias="dockerRepository")]
    docker_image_tag: Annotated[str, Field(alias="dockerImageTag")]
    documentation_url: Annotated[str, Field(alias="documentationUrl")]
    icon: str | None = None
    icon_url: Annotated[str | None, Field(alias="iconUrl")] = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    release_stage: Annotated[ReleaseStage | None, Field(alias="releaseStage")] = None
    support_level: Annotated[SupportLevel | None, Field(alias="supportLevel")] = None
    release_date: Annotated[
        date | None,
        Field(
            alias="releaseDate",
            description="The date when this connector was first released, in yyyy-mm-dd format.",
        ),
    ] = None
    tags: Annotated[
        list[str] | None,
        Field(
            description="An array of tags that describe the connector. E.g: language:python, keyword:rds, etc."
        ),
    ] = None
    resource_requirements: Annotated[
        ConnectorRegistryV0ActorDefinitionResourceRequirements | None,
        Field(alias="resourceRequirements"),
    ] = None
    protocol_version: Annotated[
        str | None,
        Field(
            alias="protocolVersion",
            description="the Airbyte Protocol version supported by the connector",
        ),
    ] = None
    normalization_config: Annotated[
        ConnectorRegistryV0ConnectorRegistryDestinationDefinitionNormalizationDestinationDefinitionConfig
        | None,
        Field(
            alias="normalizationConfig",
            description="describes a normalization config for destination definition",
            title="NormalizationDestinationDefinitionConfig",
        ),
    ] = None
    supports_dbt: Annotated[
        bool | None,
        Field(
            alias="supportsDbt",
            description="an optional flag indicating whether DBT is used in the normalization. If the flag value is NULL - DBT is not used.",
        ),
    ] = None
    allowed_hosts: Annotated[AllowedHosts | None, Field(alias="allowedHosts")] = None
    releases: ConnectorRegistryV0ConnectorRegistryReleases | None = None
    ab_internal: ConnectorRegistryV0AirbyteInternal | None = None
    supports_refreshes: Annotated[bool | None, Field(alias="supportsRefreshes")] = False
    supports_file_transfer: Annotated[bool | None, Field(alias="supportsFileTransfer")] = False
    supports_data_activation: Annotated[bool | None, Field(alias="supportsDataActivation")] = False
    generated: ConnectorRegistryV0GeneratedFields | None = None
    package_info: Annotated[
        ConnectorRegistryV0ConnectorPackageInfo | None, Field(alias="packageInfo")
    ] = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None


class ConnectorRegistryV0ConnectorRegistryDestinationDefinition1(BaseModel):
    """
    describes a destination
    """

    model_config = ConfigDict(
        extra="allow",
    )
    destination_definition_id: Annotated[UUID, Field(alias="destinationDefinitionId")]
    name: str
    docker_repository: Annotated[str, Field(alias="dockerRepository")]
    docker_image_tag: Annotated[str, Field(alias="dockerImageTag")]
    documentation_url: Annotated[str, Field(alias="documentationUrl")]
    icon: str | None = None
    icon_url: Annotated[str | None, Field(alias="iconUrl")] = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    release_stage: Annotated[ReleaseStage | None, Field(alias="releaseStage")] = None
    support_level: Annotated[SupportLevel | None, Field(alias="supportLevel")] = None
    release_date: Annotated[
        date | None,
        Field(
            alias="releaseDate",
            description="The date when this connector was first released, in yyyy-mm-dd format.",
        ),
    ] = None
    tags: Annotated[
        list[str] | None,
        Field(
            description="An array of tags that describe the connector. E.g: language:python, keyword:rds, etc."
        ),
    ] = None
    resource_requirements: Annotated[
        ConnectorRegistryV0ActorDefinitionResourceRequirements | None,
        Field(alias="resourceRequirements"),
    ] = None
    protocol_version: Annotated[
        str | None,
        Field(
            alias="protocolVersion",
            description="the Airbyte Protocol version supported by the connector",
        ),
    ] = None
    normalization_config: Annotated[
        ConnectorRegistryV0ConnectorRegistryDestinationDefinition1NormalizationDestinationDefinitionConfig
        | None,
        Field(
            alias="normalizationConfig",
            description="describes a normalization config for destination definition",
            title="NormalizationDestinationDefinitionConfig",
        ),
    ] = None
    supports_dbt: Annotated[
        bool | None,
        Field(
            alias="supportsDbt",
            description="an optional flag indicating whether DBT is used in the normalization. If the flag value is NULL - DBT is not used.",
        ),
    ] = None
    allowed_hosts: Annotated[AllowedHosts | None, Field(alias="allowedHosts")] = None
    releases: ConnectorRegistryV0ConnectorRegistryReleases | None = None
    ab_internal: ConnectorRegistryV0AirbyteInternal | None = None
    supports_refreshes: Annotated[bool | None, Field(alias="supportsRefreshes")] = False
    supports_file_transfer: Annotated[bool | None, Field(alias="supportsFileTransfer")] = False
    supports_data_activation: Annotated[bool | None, Field(alias="supportsDataActivation")] = False
    generated: ConnectorRegistryV0GeneratedFields | None = None
    package_info: Annotated[
        ConnectorRegistryV0ConnectorPackageInfo | None, Field(alias="packageInfo")
    ] = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None


class ConnectorRegistryV0ConnectorRegistryDestinationDefinition1NormalizationDestinationDefinitionConfig(
    BaseModel
):
    """
    describes a normalization config for destination definition
    """

    model_config = ConfigDict(
        extra="allow",
    )
    normalization_repository: Annotated[
        str,
        Field(
            alias="normalizationRepository",
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used.",
        ),
    ]
    normalization_tag: Annotated[
        str,
        Field(
            alias="normalizationTag",
            description="a field indicating the tag of the docker repository to be used for normalization.",
        ),
    ]
    normalization_integration_type: Annotated[
        str,
        Field(
            alias="normalizationIntegrationType",
            description="a field indicating the type of integration dialect to use for normalization.",
        ),
    ]


class ConnectorRegistryV0ConnectorRegistryDestinationDefinitionNormalizationDestinationDefinitionConfig(
    BaseModel
):
    """
    describes a normalization config for destination definition
    """

    model_config = ConfigDict(
        extra="allow",
    )
    normalization_repository: Annotated[
        str,
        Field(
            alias="normalizationRepository",
            description="a field indicating the name of the repository to be used for normalization. If the value of the flag is NULL - normalization is not used.",
        ),
    ]
    normalization_tag: Annotated[
        str,
        Field(
            alias="normalizationTag",
            description="a field indicating the tag of the docker repository to be used for normalization.",
        ),
    ]
    normalization_integration_type: Annotated[
        str,
        Field(
            alias="normalizationIntegrationType",
            description="a field indicating the type of integration dialect to use for normalization.",
        ),
    ]


class ConnectorRegistryV0ConnectorRegistryReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    release_candidates: Annotated[
        ConnectorReleaseCandidates | None, Field(alias="releaseCandidates")
    ] = None
    rollout_configuration: Annotated[
        ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfiguration | None,
        Field(
            alias="rolloutConfiguration",
            description="configuration for the rollout of a connector",
            title="RolloutConfiguration",
        ),
    ] = None
    breaking_changes: Annotated[
        dict[str, VersionBreakingChange] | None,
        Field(
            alias="breakingChanges",
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ] = None
    unsafe_downgrades: Annotated[UnsafeDowngrades | None, Field(alias="unsafeDowngrades")] = None
    migration_documentation_url: Annotated[
        AnyUrl | None,
        Field(
            alias="migrationDocumentationUrl",
            description="URL to documentation on how to migrate from the previous version to the current version. Defaults to ${documentationUrl}-migrations",
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode(Enum):
    """
    Controls how rollouts are initiated and advanced for this connector. "manual" (the default) means a human must start the rollout and approve each advancement step. "autopilot" means the AutoPilot system automatically starts the rollout when a new release candidate is published and advances it based on health signals and the configured schedule in autopilotConfig.
    """

    manual = "manual"
    autopilot = "autopilot"


class ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfiguration(BaseModel):
    """
    configuration for the rollout of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enable_progressive_rollout: Annotated[
        bool | None,
        Field(
            alias="enableProgressiveRollout",
            description="Whether to enable progressive rollout for the connector.",
        ),
    ] = False
    default_rollout_mode: Annotated[
        ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode | None,
        Field(
            alias="defaultRolloutMode",
            description='Controls how rollouts are initiated and advanced for this connector. "manual" (the default) means a human must start the rollout and approve each advancement step. "autopilot" means the AutoPilot system automatically starts the rollout when a new release candidate is published and advances it based on health signals and the configured schedule in autopilotConfig.',
        ),
    ] = ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode.manual
    autopilot_config: Annotated[
        ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig | None,
        Field(
            alias="autopilotConfig",
            description='Configuration for the AutoPilot rollout system. These settings only take effect when defaultRolloutMode is set to "autopilot".',
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy(Enum):
    """
    Controls the speed and caution level of the AutoPilot rollout. See progressive rollout docs for details on each mode.
    """

    fast = "fast"
    slow = "slow"
    default = "default"


class ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig(BaseModel):
    """
    Configuration for the AutoPilot rollout system. These settings only take effect when defaultRolloutMode is set to "autopilot".
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    auto_start: Annotated[
        bool | None,
        Field(
            alias="autoStart",
            description="Whether the AutoPilot system automatically starts a rollout when a new release candidate is published. When true (the default), AutoPilot calls the start_connector_rollout API on behalf of the operator. When false, a human must explicitly start the rollout even though advancement will be handled by AutoPilot.",
        ),
    ] = True
    auto_promote_stages: Annotated[
        bool | None,
        Field(
            alias="autoPromoteStages",
            description="Whether the AutoPilot system automatically promotes the rollout through stages (customer tiers and final GA acceptance). When true (the default), AutoPilot advances across tiers and promotes to GA based on health signals. When false, stage promotion requires human approval.",
        ),
    ] = True
    strategy: Annotated[
        ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy
        | None,
        Field(
            description="Controls the speed and caution level of the AutoPilot rollout. See progressive rollout docs for details on each mode."
        ),
    ] = ConnectorRegistryV0ConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy.default


class ConnectorRegistryV0ConnectorRegistrySourceDefinition(BaseModel):
    """
    describes a source
    """

    model_config = ConfigDict(
        extra="allow",
    )
    source_definition_id: Annotated[UUID, Field(alias="sourceDefinitionId")]
    name: str
    docker_repository: Annotated[str, Field(alias="dockerRepository")]
    docker_image_tag: Annotated[str, Field(alias="dockerImageTag")]
    documentation_url: Annotated[str, Field(alias="documentationUrl")]
    icon: str | None = None
    icon_url: Annotated[str | None, Field(alias="iconUrl")] = None
    source_type: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionSourceType | None,
        Field(alias="sourceType"),
    ] = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    release_stage: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionReleaseStage | None,
        Field(
            alias="releaseStage",
            description="enum that describes a connector's release stage",
            title="ReleaseStage",
        ),
    ] = None
    support_level: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionSupportLevel | None,
        Field(
            alias="supportLevel",
            description="enum that describes a connector's release stage",
            title="SupportLevel",
        ),
    ] = None
    release_date: Annotated[
        date | None,
        Field(
            alias="releaseDate",
            description="The date when this connector was first released, in yyyy-mm-dd format.",
        ),
    ] = None
    resource_requirements: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionActorDefinitionResourceRequirements
        | None,
        Field(
            alias="resourceRequirements",
            description="actor definition specific resource requirements",
            title="ActorDefinitionResourceRequirements",
        ),
    ] = None
    protocol_version: Annotated[
        str | None,
        Field(
            alias="protocolVersion",
            description="the Airbyte Protocol version supported by the connector",
        ),
    ] = None
    allowed_hosts: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionAllowedHosts | None,
        Field(
            alias="allowedHosts",
            description="A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.",
            title="AllowedHosts",
        ),
    ] = None
    suggested_streams: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionSuggestedStreams | None,
        Field(
            alias="suggestedStreams",
            description="A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.",
            title="SuggestedStreams",
        ),
    ] = None
    max_seconds_between_messages: Annotated[
        int | None,
        Field(
            alias="maxSecondsBetweenMessages",
            description="Number of seconds allowed between 2 airbyte protocol messages. The source will timeout if this delay is reach",
        ),
    ] = None
    erd_url: Annotated[
        str | None,
        Field(alias="erdUrl", description="The URL where you can visualize the ERD"),
    ] = None
    releases: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleases | None,
        Field(
            description="Contains information about different types of releases for a connector.",
            title="ConnectorRegistryReleases",
        ),
    ] = None
    ab_internal: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternal | None,
        Field(description="Fields for internal use only", title="AirbyteInternal"),
    ] = None
    generated: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFields | None,
        Field(
            description="Optional schema for fields generated at metadata upload time",
            title="GeneratedFields",
        ),
    ] = None
    package_info: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorPackageInfo | None,
        Field(
            alias="packageInfo",
            description="Information about the contents of the connector image",
            title="ConnectorPackageInfo",
        ),
    ] = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None
    supports_file_transfer: Annotated[bool | None, Field(alias="supportsFileTransfer")] = False
    supports_data_activation: Annotated[bool | None, Field(alias="supportsDataActivation")] = False


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1(BaseModel):
    """
    describes a source
    """

    model_config = ConfigDict(
        extra="allow",
    )
    source_definition_id: Annotated[UUID, Field(alias="sourceDefinitionId")]
    name: str
    docker_repository: Annotated[str, Field(alias="dockerRepository")]
    docker_image_tag: Annotated[str, Field(alias="dockerImageTag")]
    documentation_url: Annotated[str, Field(alias="documentationUrl")]
    icon: str | None = None
    icon_url: Annotated[str | None, Field(alias="iconUrl")] = None
    source_type: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1SourceType | None,
        Field(alias="sourceType"),
    ] = None
    spec: dict[str, Any]
    tombstone: Annotated[
        bool | None,
        Field(
            description="if false, the configuration is active. if true, then this configuration is permanently off."
        ),
    ] = False
    public: Annotated[
        bool | None,
        Field(description="true if this connector definition is available to all workspaces"),
    ] = False
    custom: Annotated[
        bool | None, Field(description="whether this is a custom connector definition")
    ] = False
    release_stage: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ReleaseStage | None,
        Field(
            alias="releaseStage",
            description="enum that describes a connector's release stage",
            title="ReleaseStage",
        ),
    ] = None
    support_level: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1SupportLevel | None,
        Field(
            alias="supportLevel",
            description="enum that describes a connector's release stage",
            title="SupportLevel",
        ),
    ] = None
    release_date: Annotated[
        date | None,
        Field(
            alias="releaseDate",
            description="The date when this connector was first released, in yyyy-mm-dd format.",
        ),
    ] = None
    resource_requirements: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ActorDefinitionResourceRequirements
        | None,
        Field(
            alias="resourceRequirements",
            description="actor definition specific resource requirements",
            title="ActorDefinitionResourceRequirements",
        ),
    ] = None
    protocol_version: Annotated[
        str | None,
        Field(
            alias="protocolVersion",
            description="the Airbyte Protocol version supported by the connector",
        ),
    ] = None
    allowed_hosts: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1AllowedHosts | None,
        Field(
            alias="allowedHosts",
            description="A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.",
            title="AllowedHosts",
        ),
    ] = None
    suggested_streams: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1SuggestedStreams | None,
        Field(
            alias="suggestedStreams",
            description="A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.",
            title="SuggestedStreams",
        ),
    ] = None
    max_seconds_between_messages: Annotated[
        int | None,
        Field(
            alias="maxSecondsBetweenMessages",
            description="Number of seconds allowed between 2 airbyte protocol messages. The source will timeout if this delay is reach",
        ),
    ] = None
    erd_url: Annotated[
        str | None,
        Field(alias="erdUrl", description="The URL where you can visualize the ERD"),
    ] = None
    releases: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleases | None,
        Field(
            description="Contains information about different types of releases for a connector.",
            title="ConnectorRegistryReleases",
        ),
    ] = None
    ab_internal: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternal | None,
        Field(description="Fields for internal use only", title="AirbyteInternal"),
    ] = None
    generated: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFields | None,
        Field(
            description="Optional schema for fields generated at metadata upload time",
            title="GeneratedFields",
        ),
    ] = None
    package_info: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorPackageInfo | None,
        Field(
            alias="packageInfo",
            description="Information about the contents of the connector image",
            title="ConnectorPackageInfo",
        ),
    ] = None
    language: Annotated[
        str | None, Field(description="The language the connector is written in")
    ] = None
    supports_file_transfer: Annotated[bool | None, Field(alias="supportsFileTransfer")] = False
    supports_data_activation: Annotated[bool | None, Field(alias="supportsDataActivation")] = False


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ActorDefinitionResourceRequirements(
    BaseModel
):
    """
    actor definition specific resource requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    default: Annotated[
        ResourceRequirements | None,
        Field(
            description="if set, these are the requirements that should be set for ALL jobs run for this actor definition."
        ),
    ] = None
    job_specific: Annotated[list[JobTypeResourceLimit] | None, Field(alias="jobSpecific")] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalSl | None = None
    ql: ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalQl | None = None
    is_enterprise: Annotated[bool | None, Field(alias="isEnterprise")] = False
    require_version_increments_in_pull_requests: Annotated[
        bool | None,
        Field(
            alias="requireVersionIncrementsInPullRequests",
            description="When false, version increment checks will be skipped for this connector",
        ),
    ] = True


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1AllowedHosts(BaseModel):
    """
    A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    hosts: Annotated[
        list[str] | None,
        Field(
            description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted."
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    release_candidates: Annotated[
        ConnectorReleaseCandidates | None, Field(alias="releaseCandidates")
    ] = None
    rollout_configuration: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfiguration
        | None,
        Field(
            alias="rolloutConfiguration",
            description="configuration for the rollout of a connector",
            title="RolloutConfiguration",
        ),
    ] = None
    breaking_changes: Annotated[
        dict[str, VersionBreakingChange] | None,
        Field(
            alias="breakingChanges",
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ] = None
    unsafe_downgrades: Annotated[UnsafeDowngrades | None, Field(alias="unsafeDowngrades")] = None
    migration_documentation_url: Annotated[
        AnyUrl | None,
        Field(
            alias="migrationDocumentationUrl",
            description="URL to documentation on how to migrate from the previous version to the current version. Defaults to ${documentationUrl}-migrations",
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode(
    Enum
):
    """
    Controls how rollouts are initiated and advanced for this connector. "manual" (the default) means a human must start the rollout and approve each advancement step. "autopilot" means the AutoPilot system automatically starts the rollout when a new release candidate is published and advances it based on health signals and the configured schedule in autopilotConfig.
    """

    manual = "manual"
    autopilot = "autopilot"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfiguration(
    BaseModel
):
    """
    configuration for the rollout of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enable_progressive_rollout: Annotated[
        bool | None,
        Field(
            alias="enableProgressiveRollout",
            description="Whether to enable progressive rollout for the connector.",
        ),
    ] = False
    default_rollout_mode: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode
        | None,
        Field(
            alias="defaultRolloutMode",
            description='Controls how rollouts are initiated and advanced for this connector. "manual" (the default) means a human must start the rollout and approve each advancement step. "autopilot" means the AutoPilot system automatically starts the rollout when a new release candidate is published and advances it based on health signals and the configured schedule in autopilotConfig.',
        ),
    ] = ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode.manual
    autopilot_config: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig
        | None,
        Field(
            alias="autopilotConfig",
            description='Configuration for the AutoPilot rollout system. These settings only take effect when defaultRolloutMode is set to "autopilot".',
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy(
    Enum
):
    """
    Controls the speed and caution level of the AutoPilot rollout. See progressive rollout docs for details on each mode.
    """

    fast = "fast"
    slow = "slow"
    default = "default"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationAutopilotConfig(
    BaseModel
):
    """
    Configuration for the AutoPilot rollout system. These settings only take effect when defaultRolloutMode is set to "autopilot".
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    auto_start: Annotated[
        bool | None,
        Field(
            alias="autoStart",
            description="Whether the AutoPilot system automatically starts a rollout when a new release candidate is published. When true (the default), AutoPilot calls the start_connector_rollout API on behalf of the operator. When false, a human must explicitly start the rollout even though advancement will be handled by AutoPilot.",
        ),
    ] = True
    auto_promote_stages: Annotated[
        bool | None,
        Field(
            alias="autoPromoteStages",
            description="Whether the AutoPilot system automatically promotes the rollout through stages (customer tiers and final GA acceptance). When true (the default), AutoPilot advances across tiers and promotes to GA based on health signals. When false, stage promotion requires human approval.",
        ),
    ] = True
    strategy: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy
        | None,
        Field(
            description="Controls the speed and caution level of the AutoPilot rollout. See progressive rollout docs for details on each mode."
        ),
    ] = ConnectorRegistryV0ConnectorRegistrySourceDefinition1ConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy.default


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    release: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfo | None,
        Field(
            description="Attribution for the pull request and author that released this connector version. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="ReleaseInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbom_url: Annotated[str | None, Field(alias="sbomUrl", description="URL to the SBOM file")] = (
        None
    )


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsConnectorMetrics(
    BaseModel
):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsGitInfo(BaseModel):
    """
    Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    commit_sha: Annotated[
        str | None,
        Field(description="The git commit sha of the last commit that modified this file."),
    ] = None
    commit_timestamp: Annotated[
        AwareDatetime | None,
        Field(description="The git commit timestamp of the last commit that modified this file."),
    ] = None
    commit_author: Annotated[
        str | None,
        Field(description="The git commit author of the last commit that modified this file."),
    ] = None
    commit_author_email: Annotated[
        str | None,
        Field(
            description="The git commit author email of the last commit that modified this file."
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfo(BaseModel):
    """
    Attribution for the pull request and author that released this connector version. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    pr_number: Annotated[
        int | None,
        Field(description="The number of the pull request that released this version."),
    ] = None
    pr_url: Annotated[
        str | None,
        Field(description="The URL of the pull request that released this version."),
    ] = None
    pr_author_id: Annotated[
        int | None,
        Field(description="The GitHub account ID of the pull request author."),
    ] = None
    pr_author_login: Annotated[
        str | None, Field(description="The GitHub login of the pull request author.")
    ] = None
    pr_author_type: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoPrAuthorType
        | None,
        Field(
            description="Whether the pull request author is a human user, a bot, or unknown, as reported by GitHub. This is raw author metadata, not an ownership verdict: read attributed_to_kind to learn who is accountable for the release. Unknown means that the author could not be determined."
        ),
    ] = None
    pr_author_association: Annotated[
        str | None,
        Field(
            description="The GitHub author association of the pull request author, such as MEMBER, OWNER, COLLABORATOR, or CONTRIBUTOR. MEMBER, OWNER, and COLLABORATOR identify an Airbyte maintainer; CONTRIBUTOR identifies a community author who is not accountable for the release."
        ),
    ] = None
    pr_merged_by_login: Annotated[
        str | None,
        Field(
            description="The GitHub login of the account that merged the releasing pull request. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    pr_merged_by_type: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoPrMergedByType
        | None,
        Field(
            description="Whether the account that merged the pull request is a human user, a bot, or unknown, as reported by GitHub. A human merger is a maintainer by construction, since merging into airbytehq/airbyte requires write access."
        ),
    ] = None
    attributed_to: Annotated[
        str | None,
        Field(
            description="The identity accountable for this release, which may differ from the pull request author. Never a community contributor: a community-authored release is attributed to the maintainer who merged it, or to nobody. Null whenever attributed_to_kind is `other`, and non-null for `maintainer` and `bot` -- `other` is precisely the case where no identity may be named, so the two fields always agree."
        ),
    ] = None
    attributed_to_kind: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoAttributedToKind
        | None,
        Field(
            description="What kind of identity attributed_to holds, and the field to route escalations on. `maintainer` is a human with write access to airbytehq/airbyte and is the only kind that may be contacted as the owner of the release. `bot` names an automated account for the record but must never be contacted. `other` covers community-authored and unattributable releases, which have no named owner and belong to the oncall rotation, and always carries a null attributed_to."
        ),
    ] = None
    merge_commit_sha: Annotated[
        str | None,
        Field(
            description="The sha of the commit that merged the releasing pull request. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    merged_at: Annotated[
        AwareDatetime | None,
        Field(
            description="The timestamp at which the releasing pull request was merged. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    released_at: Annotated[
        AwareDatetime | None,
        Field(description="The best available timestamp for when this version was released."),
    ] = None
    source: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoSource,
        Field(description="How the attribution was determined."),
    ]


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoAttributedToKind(
    Enum
):
    """
    What kind of identity attributed_to holds, and the field to route escalations on. `maintainer` is a human with write access to airbytehq/airbyte and is the only kind that may be contacted as the owner of the release. `bot` names an automated account for the record but must never be contacted. `other` covers community-authored and unattributable releases, which have no named owner and belong to the oncall rotation, and always carries a null attributed_to.
    """

    maintainer = "maintainer"
    bot = "bot"
    other = "other"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoPrAuthorType(
    Enum
):
    """
    Whether the pull request author is a human user, a bot, or unknown, as reported by GitHub. This is raw author metadata, not an ownership verdict: read attributed_to_kind to learn who is accountable for the release. Unknown means that the author could not be determined.
    """

    user = "User"
    bot = "Bot"
    unknown = "Unknown"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoPrMergedByType(
    Enum
):
    """
    Whether the account that merged the pull request is a human user, a bot, or unknown, as reported by GitHub. A human merger is a maintainer by construction, since merging into airbytehq/airbyte requires write access.
    """

    user = "User"
    bot = "Bot"
    unknown = "Unknown"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsReleaseInfoSource(Enum):
    """
    How the attribution was determined.
    """

    publish = "publish"
    git_backfill = "git-backfill"
    prerelease = "prerelease"
    changelog = "changelog"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1GeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class ReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1ReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1SourceType(Enum):
    api = "api"
    file = "file"
    database = "database"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1SuggestedStreams(BaseModel):
    """
    A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    streams: Annotated[
        list[str] | None,
        Field(
            description="An array of streams that this connector suggests the average user will want.  SuggestedStreams not being present for the source means that all streams are suggested.  An empty list here means that no streams are suggested."
        ),
    ] = None


class SupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


class ConnectorRegistryV0ConnectorRegistrySourceDefinition1SupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionActorDefinitionResourceRequirements(
    BaseModel
):
    """
    actor definition specific resource requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    default: Annotated[
        ResourceRequirements | None,
        Field(
            description="if set, these are the requirements that should be set for ALL jobs run for this actor definition."
        ),
    ] = None
    job_specific: Annotated[list[JobTypeResourceLimit] | None, Field(alias="jobSpecific")] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternal(BaseModel):
    """
    Fields for internal use only
    """

    model_config = ConfigDict(
        extra="allow",
    )
    sl: ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalSl | None = None
    ql: ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalQl | None = None
    is_enterprise: Annotated[bool | None, Field(alias="isEnterprise")] = False
    require_version_increments_in_pull_requests: Annotated[
        bool | None,
        Field(
            alias="requireVersionIncrementsInPullRequests",
            description="When false, version increment checks will be skipped for this connector",
        ),
    ] = True


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalQl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300
    integer_400 = 400
    integer_500 = 500
    integer_600 = 600


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAirbyteInternalSl(Enum):
    integer_0 = 0
    integer_100 = 100
    integer_200 = 200
    integer_300 = 300


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionAllowedHosts(BaseModel):
    """
    A connector's allowed hosts.  If present, the platform will limit communication to only hosts which are listed in `AllowedHosts.hosts`.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    hosts: Annotated[
        list[str] | None,
        Field(
            description="An array of hosts that this connector can connect to.  AllowedHosts not being present for the source or destination means that access to all hosts is allowed.  An empty list here means that no network access is granted."
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorPackageInfo(BaseModel):
    """
    Information about the contents of the connector image
    """

    cdk_version: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleases(BaseModel):
    """
    Contains information about different types of releases for a connector.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    release_candidates: Annotated[
        ConnectorReleaseCandidates | None, Field(alias="releaseCandidates")
    ] = None
    rollout_configuration: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfiguration
        | None,
        Field(
            alias="rolloutConfiguration",
            description="configuration for the rollout of a connector",
            title="RolloutConfiguration",
        ),
    ] = None
    breaking_changes: Annotated[
        dict[str, VersionBreakingChange] | None,
        Field(
            alias="breakingChanges",
            description="Each entry denotes a breaking change in a specific version of a connector that requires user action to upgrade.",
            title="ConnectorBreakingChanges",
        ),
    ] = None
    unsafe_downgrades: Annotated[UnsafeDowngrades | None, Field(alias="unsafeDowngrades")] = None
    migration_documentation_url: Annotated[
        AnyUrl | None,
        Field(
            alias="migrationDocumentationUrl",
            description="URL to documentation on how to migrate from the previous version to the current version. Defaults to ${documentationUrl}-migrations",
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode(
    Enum
):
    """
    Controls how rollouts are initiated and advanced for this connector. "manual" (the default) means a human must start the rollout and approve each advancement step. "autopilot" means the AutoPilot system automatically starts the rollout when a new release candidate is published and advances it based on health signals and the configured schedule in autopilotConfig.
    """

    manual = "manual"
    autopilot = "autopilot"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfiguration(
    BaseModel
):
    """
    configuration for the rollout of a connector
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    enable_progressive_rollout: Annotated[
        bool | None,
        Field(
            alias="enableProgressiveRollout",
            description="Whether to enable progressive rollout for the connector.",
        ),
    ] = False
    default_rollout_mode: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode
        | None,
        Field(
            alias="defaultRolloutMode",
            description='Controls how rollouts are initiated and advanced for this connector. "manual" (the default) means a human must start the rollout and approve each advancement step. "autopilot" means the AutoPilot system automatically starts the rollout when a new release candidate is published and advances it based on health signals and the configured schedule in autopilotConfig.',
        ),
    ] = ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationDefaultRolloutMode.manual
    autopilot_config: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationAutopilotConfig
        | None,
        Field(
            alias="autopilotConfig",
            description='Configuration for the AutoPilot rollout system. These settings only take effect when defaultRolloutMode is set to "autopilot".',
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy(
    Enum
):
    """
    Controls the speed and caution level of the AutoPilot rollout. See progressive rollout docs for details on each mode.
    """

    fast = "fast"
    slow = "slow"
    default = "default"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationAutopilotConfig(
    BaseModel
):
    """
    Configuration for the AutoPilot rollout system. These settings only take effect when defaultRolloutMode is set to "autopilot".
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    auto_start: Annotated[
        bool | None,
        Field(
            alias="autoStart",
            description="Whether the AutoPilot system automatically starts a rollout when a new release candidate is published. When true (the default), AutoPilot calls the start_connector_rollout API on behalf of the operator. When false, a human must explicitly start the rollout even though advancement will be handled by AutoPilot.",
        ),
    ] = True
    auto_promote_stages: Annotated[
        bool | None,
        Field(
            alias="autoPromoteStages",
            description="Whether the AutoPilot system automatically promotes the rollout through stages (customer tiers and final GA acceptance). When true (the default), AutoPilot advances across tiers and promotes to GA based on health signals. When false, stage promotion requires human approval.",
        ),
    ] = True
    strategy: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy
        | None,
        Field(
            description="Controls the speed and caution level of the AutoPilot rollout. See progressive rollout docs for details on each mode."
        ),
    ] = ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleasesRolloutConfigurationAutopilotConfigStrategy.default


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    release: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfo | None,
        Field(
            description="Attribution for the pull request and author that released this connector version. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="ReleaseInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbom_url: Annotated[str | None, Field(alias="sbomUrl", description="URL to the SBOM file")] = (
        None
    )


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsConnectorMetrics(
    BaseModel
):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsGitInfo(BaseModel):
    """
    Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    commit_sha: Annotated[
        str | None,
        Field(description="The git commit sha of the last commit that modified this file."),
    ] = None
    commit_timestamp: Annotated[
        AwareDatetime | None,
        Field(description="The git commit timestamp of the last commit that modified this file."),
    ] = None
    commit_author: Annotated[
        str | None,
        Field(description="The git commit author of the last commit that modified this file."),
    ] = None
    commit_author_email: Annotated[
        str | None,
        Field(
            description="The git commit author email of the last commit that modified this file."
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfo(BaseModel):
    """
    Attribution for the pull request and author that released this connector version. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    pr_number: Annotated[
        int | None,
        Field(description="The number of the pull request that released this version."),
    ] = None
    pr_url: Annotated[
        str | None,
        Field(description="The URL of the pull request that released this version."),
    ] = None
    pr_author_id: Annotated[
        int | None,
        Field(description="The GitHub account ID of the pull request author."),
    ] = None
    pr_author_login: Annotated[
        str | None, Field(description="The GitHub login of the pull request author.")
    ] = None
    pr_author_type: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoPrAuthorType
        | None,
        Field(
            description="Whether the pull request author is a human user, a bot, or unknown, as reported by GitHub. This is raw author metadata, not an ownership verdict: read attributed_to_kind to learn who is accountable for the release. Unknown means that the author could not be determined."
        ),
    ] = None
    pr_author_association: Annotated[
        str | None,
        Field(
            description="The GitHub author association of the pull request author, such as MEMBER, OWNER, COLLABORATOR, or CONTRIBUTOR. MEMBER, OWNER, and COLLABORATOR identify an Airbyte maintainer; CONTRIBUTOR identifies a community author who is not accountable for the release."
        ),
    ] = None
    pr_merged_by_login: Annotated[
        str | None,
        Field(
            description="The GitHub login of the account that merged the releasing pull request. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    pr_merged_by_type: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoPrMergedByType
        | None,
        Field(
            description="Whether the account that merged the pull request is a human user, a bot, or unknown, as reported by GitHub. A human merger is a maintainer by construction, since merging into airbytehq/airbyte requires write access."
        ),
    ] = None
    attributed_to: Annotated[
        str | None,
        Field(
            description="The identity accountable for this release, which may differ from the pull request author. Never a community contributor: a community-authored release is attributed to the maintainer who merged it, or to nobody. Null whenever attributed_to_kind is `other`, and non-null for `maintainer` and `bot` -- `other` is precisely the case where no identity may be named, so the two fields always agree."
        ),
    ] = None
    attributed_to_kind: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoAttributedToKind
        | None,
        Field(
            description="What kind of identity attributed_to holds, and the field to route escalations on. `maintainer` is a human with write access to airbytehq/airbyte and is the only kind that may be contacted as the owner of the release. `bot` names an automated account for the record but must never be contacted. `other` covers community-authored and unattributable releases, which have no named owner and belong to the oncall rotation, and always carries a null attributed_to."
        ),
    ] = None
    merge_commit_sha: Annotated[
        str | None,
        Field(
            description="The sha of the commit that merged the releasing pull request. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    merged_at: Annotated[
        AwareDatetime | None,
        Field(
            description="The timestamp at which the releasing pull request was merged. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    released_at: Annotated[
        AwareDatetime | None,
        Field(description="The best available timestamp for when this version was released."),
    ] = None
    source: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoSource,
        Field(description="How the attribution was determined."),
    ]


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoAttributedToKind(
    Enum
):
    """
    What kind of identity attributed_to holds, and the field to route escalations on. `maintainer` is a human with write access to airbytehq/airbyte and is the only kind that may be contacted as the owner of the release. `bot` names an automated account for the record but must never be contacted. `other` covers community-authored and unattributable releases, which have no named owner and belong to the oncall rotation, and always carries a null attributed_to.
    """

    maintainer = "maintainer"
    bot = "bot"
    other = "other"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoPrAuthorType(
    Enum
):
    """
    Whether the pull request author is a human user, a bot, or unknown, as reported by GitHub. This is raw author metadata, not an ownership verdict: read attributed_to_kind to learn who is accountable for the release. Unknown means that the author could not be determined.
    """

    user = "User"
    bot = "Bot"
    unknown = "Unknown"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoPrMergedByType(
    Enum
):
    """
    Whether the account that merged the pull request is a human user, a bot, or unknown, as reported by GitHub. A human merger is a maintainer by construction, since merging into airbytehq/airbyte requires write access.
    """

    user = "User"
    bot = "Bot"
    unknown = "Unknown"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsReleaseInfoSource(Enum):
    """
    How the attribution was determined.
    """

    publish = "publish"
    git_backfill = "git-backfill"
    prerelease = "prerelease"
    changelog = "changelog"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionGeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionReleaseStage(Enum):
    """
    enum that describes a connector's release stage
    """

    alpha = "alpha"
    beta = "beta"
    generally_available = "generally_available"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionSourceType(Enum):
    api = "api"
    file = "file"
    database = "database"
    custom = "custom"


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionSuggestedStreams(BaseModel):
    """
    A source's suggested streams.  These will be suggested by default for new connections using this source.  Otherwise, all streams will be selected.  This is useful for when your source has a lot of streams, but the average user will only want a subset of them synced.
    """

    model_config = ConfigDict(
        extra="allow",
    )
    streams: Annotated[
        list[str] | None,
        Field(
            description="An array of streams that this connector suggests the average user will want.  SuggestedStreams not being present for the source means that all streams are suggested.  An empty list here means that no streams are suggested."
        ),
    ] = None


class ConnectorRegistryV0ConnectorRegistrySourceDefinitionSupportLevel(Enum):
    """
    enum that describes a connector's release stage
    """

    community = "community"
    certified = "certified"
    archived = "archived"


class ConnectorRegistryV0GeneratedFields(BaseModel):
    """
    Optional schema for fields generated at metadata upload time
    """

    git: Annotated[
        ConnectorRegistryV0GeneratedFieldsGitInfo | None,
        Field(
            description="Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="GitInfo",
        ),
    ] = None
    release: Annotated[
        ConnectorRegistryV0GeneratedFieldsReleaseInfo | None,
        Field(
            description="Attribution for the pull request and author that released this connector version. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.",
            title="ReleaseInfo",
        ),
    ] = None
    source_file_info: Annotated[
        ConnectorRegistryV0GeneratedFieldsSourceFileInfo | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="SourceFileInfo",
        ),
    ] = None
    metrics: Annotated[
        ConnectorRegistryV0GeneratedFieldsConnectorMetrics | None,
        Field(
            description="Information about the source file that generated the registry entry",
            title="ConnectorMetrics",
        ),
    ] = None
    sbom_url: Annotated[str | None, Field(alias="sbomUrl", description="URL to the SBOM file")] = (
        None
    )


class ConnectorRegistryV0GeneratedFieldsConnectorMetrics(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    all: Any | None = None
    cloud: Any | None = None
    oss: Any | None = None


class ConnectorRegistryV0GeneratedFieldsGitInfo(BaseModel):
    """
    Information about the author of the last commit that modified this file. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    commit_sha: Annotated[
        str | None,
        Field(description="The git commit sha of the last commit that modified this file."),
    ] = None
    commit_timestamp: Annotated[
        AwareDatetime | None,
        Field(description="The git commit timestamp of the last commit that modified this file."),
    ] = None
    commit_author: Annotated[
        str | None,
        Field(description="The git commit author of the last commit that modified this file."),
    ] = None
    commit_author_email: Annotated[
        str | None,
        Field(
            description="The git commit author email of the last commit that modified this file."
        ),
    ] = None


class ConnectorRegistryV0GeneratedFieldsReleaseInfo(BaseModel):
    """
    Attribution for the pull request and author that released this connector version. DO NOT DEFINE THIS FIELD MANUALLY. It will be overwritten by the CI.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    pr_number: Annotated[
        int | None,
        Field(description="The number of the pull request that released this version."),
    ] = None
    pr_url: Annotated[
        str | None,
        Field(description="The URL of the pull request that released this version."),
    ] = None
    pr_author_id: Annotated[
        int | None,
        Field(description="The GitHub account ID of the pull request author."),
    ] = None
    pr_author_login: Annotated[
        str | None, Field(description="The GitHub login of the pull request author.")
    ] = None
    pr_author_type: Annotated[
        ConnectorRegistryV0GeneratedFieldsReleaseInfoPrAuthorType | None,
        Field(
            description="Whether the pull request author is a human user, a bot, or unknown, as reported by GitHub. This is raw author metadata, not an ownership verdict: read attributed_to_kind to learn who is accountable for the release. Unknown means that the author could not be determined."
        ),
    ] = None
    pr_author_association: Annotated[
        str | None,
        Field(
            description="The GitHub author association of the pull request author, such as MEMBER, OWNER, COLLABORATOR, or CONTRIBUTOR. MEMBER, OWNER, and COLLABORATOR identify an Airbyte maintainer; CONTRIBUTOR identifies a community author who is not accountable for the release."
        ),
    ] = None
    pr_merged_by_login: Annotated[
        str | None,
        Field(
            description="The GitHub login of the account that merged the releasing pull request. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    pr_merged_by_type: Annotated[
        ConnectorRegistryV0GeneratedFieldsReleaseInfoPrMergedByType | None,
        Field(
            description="Whether the account that merged the pull request is a human user, a bot, or unknown, as reported by GitHub. A human merger is a maintainer by construction, since merging into airbytehq/airbyte requires write access."
        ),
    ] = None
    attributed_to: Annotated[
        str | None,
        Field(
            description="The identity accountable for this release, which may differ from the pull request author. Never a community contributor: a community-authored release is attributed to the maintainer who merged it, or to nobody. Null whenever attributed_to_kind is `other`, and non-null for `maintainer` and `bot` -- `other` is precisely the case where no identity may be named, so the two fields always agree."
        ),
    ] = None
    attributed_to_kind: Annotated[
        ConnectorRegistryV0GeneratedFieldsReleaseInfoAttributedToKind | None,
        Field(
            description="What kind of identity attributed_to holds, and the field to route escalations on. `maintainer` is a human with write access to airbytehq/airbyte and is the only kind that may be contacted as the owner of the release. `bot` names an automated account for the record but must never be contacted. `other` covers community-authored and unattributable releases, which have no named owner and belong to the oncall rotation, and always carries a null attributed_to."
        ),
    ] = None
    merge_commit_sha: Annotated[
        str | None,
        Field(
            description="The sha of the commit that merged the releasing pull request. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    merged_at: Annotated[
        AwareDatetime | None,
        Field(
            description="The timestamp at which the releasing pull request was merged. Null for prereleases, which are published from an unmerged branch."
        ),
    ] = None
    released_at: Annotated[
        AwareDatetime | None,
        Field(description="The best available timestamp for when this version was released."),
    ] = None
    source: Annotated[
        ConnectorRegistryV0GeneratedFieldsReleaseInfoSource,
        Field(description="How the attribution was determined."),
    ]


class ConnectorRegistryV0GeneratedFieldsReleaseInfoAttributedToKind(Enum):
    """
    What kind of identity attributed_to holds, and the field to route escalations on. `maintainer` is a human with write access to airbytehq/airbyte and is the only kind that may be contacted as the owner of the release. `bot` names an automated account for the record but must never be contacted. `other` covers community-authored and unattributable releases, which have no named owner and belong to the oncall rotation, and always carries a null attributed_to.
    """

    maintainer = "maintainer"
    bot = "bot"
    other = "other"


class ConnectorRegistryV0GeneratedFieldsReleaseInfoPrAuthorType(Enum):
    """
    Whether the pull request author is a human user, a bot, or unknown, as reported by GitHub. This is raw author metadata, not an ownership verdict: read attributed_to_kind to learn who is accountable for the release. Unknown means that the author could not be determined.
    """

    user = "User"
    bot = "Bot"
    unknown = "Unknown"


class ConnectorRegistryV0GeneratedFieldsReleaseInfoPrMergedByType(Enum):
    """
    Whether the account that merged the pull request is a human user, a bot, or unknown, as reported by GitHub. A human merger is a maintainer by construction, since merging into airbytehq/airbyte requires write access.
    """

    user = "User"
    bot = "Bot"
    unknown = "Unknown"


class ConnectorRegistryV0GeneratedFieldsReleaseInfoSource(Enum):
    """
    How the attribution was determined.
    """

    publish = "publish"
    git_backfill = "git-backfill"
    prerelease = "prerelease"
    changelog = "changelog"


class ConnectorRegistryV0GeneratedFieldsSourceFileInfo(BaseModel):
    """
    Information about the source file that generated the registry entry
    """

    metadata_etag: str | None = None
    metadata_file_path: str | None = None
    metadata_bucket_name: str | None = None
    metadata_last_modified: str | None = None
    registry_entry_generated_at: str | None = None


class VersionReleaseCandidate(
    RootModel[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1
        | ConnectorRegistryV0ConnectorRegistryDestinationDefinition1
    ]
):
    root: Annotated[
        ConnectorRegistryV0ConnectorRegistrySourceDefinition1
        | ConnectorRegistryV0ConnectorRegistryDestinationDefinition1,
        Field(description="Contains information about a release candidate version of a connector."),
    ]


class ConnectorReleaseCandidates(RootModel[dict[str, VersionReleaseCandidate]]):
    root: Annotated[
        dict[str, VersionReleaseCandidate],
        Field(description="Each entry denotes a release candidate version of a connector."),
    ]


class JobTypeResourceLimit(BaseModel):
    """
    sets resource requirements for a specific job type for an actor definition. these values override the default, if both are set.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    job_type: Annotated[
        JobTypeResourceLimitJobType,
        Field(
            alias="jobType",
            description="enum that describes the different types of jobs that the platform runs.",
            title="JobType",
        ),
    ]
    resource_requirements: Annotated[
        JobTypeResourceLimitResourceRequirements,
        Field(
            alias="resourceRequirements",
            description="generic configuration for pod source requirements",
            title="ResourceRequirements",
        ),
    ]


class JobTypeResourceLimitJobType(Enum):
    """
    enum that describes the different types of jobs that the platform runs.
    """

    get_spec = "get_spec"
    check_connection = "check_connection"
    discover_schema = "discover_schema"
    sync = "sync"
    reset_connection = "reset_connection"
    connection_updater = "connection_updater"
    replicate = "replicate"


class JobTypeResourceLimitResourceRequirements(BaseModel):
    """
    generic configuration for pod source requirements
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    cpu_request: str | None = None
    cpu_limit: str | None = None
    memory_request: str | None = None
    memory_limit: str | None = None


class UnsafeDowngradeEntry(BaseModel):
    """
    Information about why downgrading past a specific version is unsafe.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    message: Annotated[
        str,
        Field(description="Explanation of why downgrading past this version is unsafe."),
    ]


class UnsafeDowngrades(RootModel[dict[str, UnsafeDowngradeEntry]]):
    root: Annotated[
        dict[str, UnsafeDowngradeEntry],
        Field(
            description="Map of connector versions that are unsafe to downgrade past. Each entry contains a message explaining why downgrading past that version is unsafe. In the compiled registry output, this is the union of explicitly declared unsafeDowngrades and breakingChanges entries where safeToDowngrade is false (or omitted)."
        ),
    ]


class VersionBreakingChange(BaseModel):
    """
    Contains information about a breaking change, including the deadline to upgrade and a message detailing the change.
    """

    model_config = ConfigDict(
        extra="forbid",
    )
    upgrade_deadline: Annotated[
        date,
        Field(
            alias="upgradeDeadline",
            description="The deadline by which to upgrade before the breaking change takes effect.",
        ),
    ]
    message: Annotated[str, Field(description="Descriptive message detailing the breaking change.")]
    deadline_action: Annotated[
        VersionBreakingChangeDeadlineAction | None,
        Field(
            alias="deadlineAction",
            description="The action the platform takes when the upgrade deadline is reached: `auto_upgrade` automatically migrates connections to the new version; `disable` pauses syncs until the user manually upgrades.",
        ),
    ] = None
    migration_documentation_url: Annotated[
        AnyUrl | None,
        Field(
            alias="migrationDocumentationUrl",
            description="URL to documentation on how to migrate to the current version. Defaults to ${documentationUrl}-migrations#${version}",
        ),
    ] = None
    is_breaking: Annotated[
        bool | None,
        Field(
            alias="isBreaking",
            description="Whether this entry represents an actual breaking change that requires user action (version pinning, upgrade notifications, deadline enforcement). Defaults to true for backward compatibility. Set to false for entries that only annotate a version (e.g. to mark it as unsafe to downgrade past) without triggering breaking-change platform behavior.",
        ),
    ] = True
    safe_to_downgrade: Annotated[
        bool | None,
        Field(
            alias="safeToDowngrade",
            description="Whether it is safe to downgrade (roll back) past this version. Defaults to false, meaning rolling back past this version is unsafe and the system should prevent it. Set to true only when the changes in this version are fully reversible and a downgrade would not cause data loss or corruption.",
        ),
    ] = False
    scoped_impact: Annotated[
        list[BreakingChangeScope] | None,
        Field(
            alias="scopedImpact",
            description="List of scopes that are impacted by the breaking change. If not specified, the breaking change cannot be scoped to reduce impact via the supported scope types.",
            min_length=1,
        ),
    ] = None


class VersionBreakingChangeDeadlineAction(Enum):
    """
    The action the platform takes when the upgrade deadline is reached: `auto_upgrade` automatically migrates connections to the new version; `disable` pauses syncs until the user manually upgrades.
    """

    auto_upgrade = "auto_upgrade"
    disable = "disable"


ConnectorRegistryV0ConnectorRegistryDestinationDefinition.model_rebuild()
ConnectorRegistryV0ConnectorRegistryReleases.model_rebuild()
ConnectorRegistryV0ConnectorRegistrySourceDefinitionConnectorRegistryReleases.model_rebuild()
ConnectorReleaseCandidates.model_rebuild()
VersionReleaseCandidate.model_rebuild()
