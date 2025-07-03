from __future__ import annotations

import csv
import enum
import os
from dataclasses import dataclass
from typing import List, Optional, Any, TypeVar, Union

from bigeye_sdk.bigconfig_validation.yaml_model_base import (
    YamlModelWithValidatorContext,
)
from bigeye_sdk.exceptions.exceptions import FileLoadException, FileNotFoundException, InvalidConfigurationException
from bigeye_sdk.generated.com.bigeye.models.generated import Table, TableColumn, DataNodeType
from bigeye_sdk.model.protobuf_enum_facade import SimpleDataNodeType
from bigeye_sdk.serializable import File
from bigeye_sdk.log import get_logger

log = get_logger(__file__)

LINEAGE_CONFIGURATION_FILE = TypeVar(
    "LINEAGE_CONFIGURATION_FILE", bound="LineageConfigurationFile"
)

ICONS_BUCKET = "https://lineage-plus-icons.s3.us-west-2.amazonaws.com"

class SimpleCustomIconType(enum.Enum):
    CUSTOM_ICON_TYPE_FIVETRAN = f"{ICONS_BUCKET}/fivetran.svg"
    CUSTOM_ICON_TYPE_GOOGLE_SHEETS = f"{ICONS_BUCKET}/gsheets.svg"
    CUSTOM_ICON_TYPE_SHOPIFY = f"{ICONS_BUCKET}/shopify.svg"
    CUSTOM_ICON_TYPE_ADOBE_ANALYTICS = f"{ICONS_BUCKET}/adobe_analytics.svg"
    CUSTOM_ICON_TYPE_ADP = f"{ICONS_BUCKET}/adp_workforce.svg"
    CUSTOM_ICON_TYPE_AMAZON = f"{ICONS_BUCKET}/amazon.svg"
    CUSTOM_ICON_TYPE_GITHUB = f"{ICONS_BUCKET}/github.svg"
    CUSTOM_ICON_TYPE_QUICKBOOKS = f"{ICONS_BUCKET}/quickbooks.svg"
    CUSTOM_ICON_TYPE_WORKDAY = f"{ICONS_BUCKET}/workday.svg"
    CUSTOM_ICON_TYPE_YOUTUBE_ANALYTICS = f"{ICONS_BUCKET}/youtube_analytics.svg"
    CUSTOM_ICON_TYPE_MICROSOFT_ADVERTISING = f"{ICONS_BUCKET}/microsoft_advertising.svg"
    CUSTOM_ICON_TYPE_MICROSOFT_D365 = f"{ICONS_BUCKET}/microsoft_d365.svg"
    CUSTOM_ICON_TYPE_MICROSOFT_ONEDRIVE = f"{ICONS_BUCKET}/microsoft_onedrive.svg"
    CUSTOM_ICON_TYPE_MICROSOFT_TEAMS = f"{ICONS_BUCKET}/microsoft_teams.svg"
    CUSTOM_ICON_TYPE_PAYPAL = f"{ICONS_BUCKET}/paypal.svg"
    CUSTOM_ICON_TYPE_SALESFORCE = f"{ICONS_BUCKET}/salesforce.svg"
    CUSTOM_ICON_TYPE_SFTP = f"{ICONS_BUCKET}/sftp.svg"
    CUSTOM_ICON_TYPE_SHAREPOINT = f"{ICONS_BUCKET}/sharepoint.svg"
    CUSTOM_ICON_TYPE_GOOGLE = f"{ICONS_BUCKET}/google.svg"
    CUSTOM_ICON_TYPE_GOOGLE_DRIVE = f"{ICONS_BUCKET}/google_drive.svg"
    CUSTOM_ICON_TYPE_GOOGLE_SEARCH_ADS = f"{ICONS_BUCKET}/google_search_ads.svg"
    CUSTOM_ICON_TYPE_HUBSPOT = f"{ICONS_BUCKET}/hubspot.svg"
    CUSTOM_ICON_TYPE_INSTAGRAM = f"{ICONS_BUCKET}/instagram.svg"
    CUSTOM_ICON_TYPE_INTERCOM = f"{ICONS_BUCKET}/intercom.svg"
    CUSTOM_ICON_TYPE_LINKEDIN = f"{ICONS_BUCKET}/linkedin.svg"
    CUSTOM_ICON_TYPE_JIRA = f"{ICONS_BUCKET}/atlassian_jira.svg"
    CUSTOM_ICON_TYPE_AZURE = f"{ICONS_BUCKET}/azure.svg"
    CUSTOM_ICON_TYPE_AZURE_STORAGE = f"{ICONS_BUCKET}/azure_storage.svg"
    CUSTOM_ICON_TYPE_BOX = f"{ICONS_BUCKET}/box.svg"
    CUSTOM_ICON_TYPE_DATADOG = f"{ICONS_BUCKET}/datadog.svg"
    CUSTOM_ICON_TYPE_FTP = f"{ICONS_BUCKET}/ftp.svg"
    CUSTOM_ICON_TYPE_GOOGLE_ADS = f"{ICONS_BUCKET}/google_ads.svg"
    CUSTOM_ICON_TYPE_GOOGLE_ANALYTICS = f"{ICONS_BUCKET}/google_analytics.svg"


class SimpleCustomNode(YamlModelWithValidatorContext):
    name: str
    container_name: str = "Python"
    data_node_id: Optional[int] = None
    container_node_id: Optional[int] = None
    node_type: DataNodeType = DataNodeType.DATA_NODE_TYPE_CUSTOM
    node_icon: Optional[Union[str, SimpleCustomIconType]] = None
    metadata: Optional[dict] = None

    @property
    def node_icon_url(self):
        if isinstance(self.node_icon, SimpleCustomIconType):
            return self.node_icon.value
        elif self.node_icon is not None :
            return self.node_icon
        else:
            return None

@dataclass
class SimpleLineageEdgeRequest:
    upstream: Union[Table, TableColumn, SimpleCustomNode]
    downstream: Union[Table, TableColumn, SimpleCustomNode]
    node_type: DataNodeType
    etl_task: Optional[SimpleCustomNode] = None


@dataclass
class SimpleLineageNodeRequest:
    name: str
    container_name: str
    node_type: DataNodeType


class LineageConfigurationFile(File):
    pass


class LineageColumnOverride(YamlModelWithValidatorContext):
    upstream_column_name: str
    downstream_column_name: str


class LineageTableOverride(YamlModelWithValidatorContext):
    upstream_table_name: str
    downstream_table_name: str
    column_overrides: Optional[List[LineageColumnOverride]] = None
    column_name_exclusions: Optional[List[str]] = None
    etl_task: Optional[SimpleCustomNode] = None


class LineageConfiguration(YamlModelWithValidatorContext):
    """
    The Simple Lineage Configuration is a Yaml serializable configuration file used to configure and version lineage as
    a file.

    Attributes:
        upstream_schema_name: The fq schema name of upstream entity.
        downstream_schema_name: The fq schema name of downstream entity.
        upstream_type: The upstream entity type.
        downstream_type: The downstream entity type.
        table_overrides: Optional list of tables where names do not match and will need to be mapped.
        etl_task: Optional custom ETL task to be used for the lineage.
    """
    upstream_schema_name: str
    downstream_schema_name: str
    upstream_type: Optional[SimpleDataNodeType] = None
    downstream_type: Optional[SimpleDataNodeType] = None
    upstream_metadata: Optional[dict] = None
    downstream_metadata: Optional[dict] = None
    upstream_icon_url: Optional[str] = None
    downstream_icon_url: Optional[str] = None
    table_overrides: Optional[List[LineageTableOverride]] = None
    etl_task: Optional[SimpleCustomNode] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.__verify_config()

    def __verify_config(self):
        if not self.has_custom_upstream and self.upstream_icon_url:
            raise InvalidConfigurationException(f"Upstream node of type {self.upstream_type} cannot be configured with an icon url.")
        if not self.has_custom_downstream and self.downstream_icon_url:
            raise InvalidConfigurationException(f"Downstream node of type {self.downstream_type} cannot be configured with an icon url.")

        return

    @property
    def has_custom_upstream(self):
        return (self.upstream_type == SimpleDataNodeType.CUSTOM
                or self.upstream_type == SimpleDataNodeType.CUSTOM_ENTRY)

    @property
    def has_custom_downstream(self):
        return (self.downstream_type == SimpleDataNodeType.CUSTOM
                or self.downstream_type == SimpleDataNodeType.CUSTOM_ENTRY)

    @property
    def has_custom(self):
        return self.has_custom_upstream or self.has_custom_downstream

class SimpleLineageConfigurationFile(
    LineageConfigurationFile, type="LINEAGE_CONFIGURATION_FILE"
):
    relations: Optional[List[LineageConfiguration]] = None

    @classmethod
    def load_from_csv(cls, input_file: str) -> 'SimpleLineageConfigurationFile':
        """
        Load LineageConfiguration objects from a CSV file.
        Args:
            input_file (str): Path to the CSV file
        Returns:
            SimpleLineageConfigurationFile: Instance with loaded configurations
        """
        if not os.path.exists(input_file):
            raise FileNotFoundException(f"CSV file not found: {input_file}")

        configurations = []

        try:
            with open(input_file, mode='r', encoding='utf-8-sig') as csv_file:
                reader = csv.DictReader(csv_file)

                # Group rows by combined schema pairs (database.schema)
                schema_groups = {}
                for row in reader:
                    # Create fully qualified schema names by combining database and schema
                    upstream_fq_schema = f"{row.get('upstream_database_name', '')}.{row.get('upstream_schema_name', '')}"
                    downstream_fq_schema = f"{row.get('downstream_database_name', '')}.{row.get('downstream_schema_name', '')}"

                    # Remove leading/trailing dots if database or schema is missing
                    upstream_fq_schema = upstream_fq_schema.strip('.')
                    downstream_fq_schema = downstream_fq_schema.strip('.')

                    # Create a key based on fully qualified upstream and downstream schema
                    key = (upstream_fq_schema, downstream_fq_schema)

                    if key not in schema_groups:
                        schema_groups[key] = []

                    schema_groups[key].append(row)

                # Create LineageConfiguration for each schema pair
                for (upstream_schema, downstream_schema), rows in schema_groups.items():
                    if not upstream_schema:
                        log.warning(f"Skipping row with empty upstream schema")
                        continue

                    # Get the types from the first row (assuming consistent for the schema pair)
                    first_row = rows[0]
                    upstream_type = None
                    downstream_type = None
                    try:
                        if first_row.get('upstream_type', None):
                            upstream_type = SimpleDataNodeType(first_row['upstream_type'])
                    except ValueError:
                        raise ValueError(f"Invalid upstream_type: {first_row['upstream_type']}")

                    try:
                        if first_row.get('downstream_type', None):
                            downstream_type = SimpleDataNodeType(first_row['downstream_type'])
                    except ValueError:
                        raise ValueError(f"Invalid downstream_type: {first_row['downstream_type']}")

                    # Collect table overrides
                    table_overrides = {}
                    for row in rows:
                        if row.get('upstream_table_name', None) and row.get('downstream_table_name', None):
                            table_key = (row['upstream_table_name'], row['downstream_table_name'])

                            if table_key not in table_overrides:
                                table_overrides[table_key] = {
                                    'override': LineageTableOverride(
                                        upstream_table_name=row['upstream_table_name'],
                                        downstream_table_name=row['downstream_table_name'],
                                        column_overrides=[],
                                    )
                                }

                            # Add column override if both column names are provided
                            if row.get('upstream_column_name', None) and row.get('downstream_column_name', None):
                                table_overrides[table_key]['override'].column_overrides.append(
                                    LineageColumnOverride(
                                        upstream_column_name=row['upstream_column_name'],
                                        downstream_column_name=row['downstream_column_name']
                                    )
                                )

                    # Create LineageConfiguration
                    config = LineageConfiguration(
                        upstream_schema_name=upstream_schema,
                        downstream_schema_name=downstream_schema,
                        upstream_type=upstream_type,
                        downstream_type=downstream_type,
                        table_overrides=[override['override'] for override in
                                         table_overrides.values()] if table_overrides else []
                    )
                    configurations.append(config)

            # Create and return an instance with the loaded configurations
            instance = cls(type="LINEAGE_CONFIGURATION_FILE")
            instance.relations = configurations
            return instance
        except Exception as e:
            raise FileLoadException(f"Error loading CSV file: {input_file}, Error: {e}")
