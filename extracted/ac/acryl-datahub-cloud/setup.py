import json
import pathlib

from setuptools import setup

_here = pathlib.Path(__file__).parent

_codegen_config_file = pathlib.Path("./src/acryl_datahub_cloud/_codegen_config.json")
_codegen_config: dict = json.loads(_codegen_config_file.read_text())

acryl_datahub = [
    # 1.5.0.8: acryl-datahub exposes redshift-slim (Wolfi executor venv; no sql_common / GE / urllib3 1.x stack).
    # Needs to stay pinned to prevent breaking changes
    "acryl-datahub==1.6.0.15"
]

# Note: We are using the croniter library for cron parsing which is different from executor, which uses apscheduler, so there is a risk of mismatch here.
# croniter is now maintained at: https://github.com/pallets-eco/croniter
base_requirements = [
    *acryl_datahub,
    "croniter",
    "pytz",
    "types-croniter",
    "tzlocal",
    "boto3",
    "botocore!=1.23.0",
]

stats_common = {"pandas", "pyarrow", "duckdb"}
aws_common = {"boto3"}
open_search_common = {"opensearch-py==2.4.2"}

plugins = {
    "datahub-lineage-features": stats_common | open_search_common | {"tenacity"},
    "datahub-reporting-forms": stats_common
    | aws_common
    | {
        "termcolor==2.5.0",
    },
    "datahub-reporting-extract-graph": stats_common | aws_common | open_search_common,
    "datahub-reporting-extract-sql": stats_common | aws_common,
    # Unpinned pyarrow via stats_common; bundled images apply constraints.txt (e.g. pyarrow>=23 for CVE fixes).
    "datahub-usage-reporting": stats_common
    | aws_common
    | {
        "opensearch-py==2.4.2",
        "polars==1.34.0",
        "elasticsearch==7.13.4",
        "numpy<2",
        "scipy<=1.14.1",
        "termcolor==2.5.0",
    },
    "datahub-metadata-sharing": {"tenacity"},
    "datahub-action-request-owner": {"tenacity"},
    "acryl-cs-issues": {"zenpy", "openai", "jinja2", "slack-sdk"},
    "datahub-forms-notifications": {"tenacity"},
    "datahub-periodic-analytics": stats_common | aws_common | {"polars==1.34.0"},
}

dev_requirements = {
    # acryl-datahub[dev] pulls in more things than are strictly necessary, but it's fine.
    "acryl-datahub[dev]",
    # flatdict 4.0.1 has a broken setup.py that doesn't declare pkg_resources as a build dependency
    "flatdict!=4.0.1",
    # Type stubs for external libraries
    "pyarrow-stubs",
    "scipy-stubs",
    "pandas-stubs",
    *list(
        dependency
        for plugin in [
            "datahub-reporting-forms",
            "datahub-reporting-extract-graph",
            "datahub-reporting-extract-sql",
            "datahub-action-request-owner",
            "datahub-lineage-features",
            "datahub-usage-reporting",
            "datahub-metadata-sharing",
            "acryl-cs-issues",
            "datahub-forms-notifications",
            "datahub-periodic-analytics",
        ]
        for dependency in plugins[plugin]
    ),
}

setup(
    **{
        **_codegen_config,
        "description": "Extend DataHub with DataHub Cloud features: usage reporting, lineage enrichment, metadata sharing, and more.",
        "long_description": (_here / "README.md").read_text(),
        "long_description_content_type": "text/markdown",
        "url": "https://datahub.com/",
        "project_urls": {
            "Documentation": "https://docs.datahub.com",
            "Source": "https://github.com/acryldata/datahub-fork",
            "Changelog": "https://github.com/acryldata/datahub-fork/releases",
            "Releases": "https://github.com/acryldata/datahub-fork/releases",
        },
        "license": "Proprietary",
        "python_requires": ">=3.10",
        "classifiers": [
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Intended Audience :: Information Technology",
            "License :: Other/Proprietary License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Database",
        ],
        "install_requires": [
            *_codegen_config["install_requires"],
            *base_requirements,
        ],
        "entry_points": {
            **_codegen_config["entry_points"],
            "console_scripts": [
                "acryl-datahub-cloud = acryl_datahub_cloud.cli:main",
            ],
            "datahub.ingestion.source.plugins": [
                "datahub-reporting-forms = acryl_datahub_cloud.datahub_reporting.forms:DataHubReportingFormsSource",
                "datahub-reporting-extract-graph = acryl_datahub_cloud.datahub_reporting.extract_graph:DataHubReportingExtractGraphSource",
                "datahub-reporting-extract-sql = acryl_datahub_cloud.datahub_reporting.extract_sql:DataHubReportingExtractSQLSource",
                "datahub-lineage-features = acryl_datahub_cloud.lineage_features.source:DataHubLineageFeaturesSource",
                "datahub-usage-reporting = acryl_datahub_cloud.datahub_usage_reporting.usage_feature_reporter:DataHubUsageFeatureReportingSource",
                "datahub-metadata-sharing = acryl_datahub_cloud.datahub_metadata_sharing.metadata_sharing_source:DataHubMetadataSharingSource",
                "acryl-cs-issues = acryl_datahub_cloud.acryl_cs_issues.source:AcrylCSIssuesSource",
                "datahub-restore = acryl_datahub_cloud.datahub_restore.source:DataHubRestoreSource",
                "datahub-action-request-owner = acryl_datahub_cloud.action_request.action_request_owner_source:ActionRequestOwnerSource",
                "datahub-forms-notifications = acryl_datahub_cloud.datahub_forms_notifications.forms_notifications_source:DataHubFormsNotificationsSource",
                "datahub-user-entity-resolution = acryl_datahub_cloud.user_entity_resolution.source:UserEntityResolutionSource",
                "github-documents-cloud = acryl_datahub_cloud.github_documents_cloud.source:GitHubDocumentsCloudSource",
                "datahub-periodic-analytics-rollup = acryl_datahub_cloud.periodic_analytics.rollup_source:DataHubPeriodicAnalyticsRollupSource",
                "datahub-periodic-analytics-billing-sync = acryl_datahub_cloud.periodic_analytics.billing_sync_source:DataHubPeriodicAnalyticsBillingSyncSource",
            ],
        },
        "include_package_data": True,
        "package_data": {
            "acryl_datahub_cloud": [
                "*.json",
                "metadata/*.avsc",
                "metadata/schemas/*.avsc",
            ],
            "acryl_datahub_cloud.datahub_metadata_sharing": [
                "scroll_shared_entities.gql",
                "share_entity.gql",
            ],
            "acryl_datahub_cloud.datahub_forms_notifications": [
                "get_search_results_total.gql",
                "scroll_forms_for_notification.gql",
                "send_form_notification_request.gql",
                "get_feature_flag.gql",
            ],
            "acryl_datahub_cloud.periodic_analytics.registries": ["*.yaml"],
        },
    },
    extras_require={
        **{plugin: list(dependencies) for (plugin, dependencies) in plugins.items()},
        "all": list(
            set().union(*[requirements for _plugin, requirements in plugins.items()])
        ),
        "dev": list(dev_requirements),
    },
)
