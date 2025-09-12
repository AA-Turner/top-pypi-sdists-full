import json
import os
import pathlib
import shutil
from unittest import TestCase
from unittest.mock import ANY, Mock, call, patch

import click
import responses
from box import Box, BoxList
from click.testing import CliRunner
from freezegun import freeze_time
from parameterized import parameterized
from pycarlo.core import Client

from montecarlodata.common.data import MonolithResponse
from montecarlodata.iac.commands import compile as compile_config
from montecarlodata.iac.commands import (
    convert_to_mac,
    convert_to_ui,
    export,
    export_as_latest,
    export_migrated_dt,
    get_template,
)
from montecarlodata.iac.mc_config_service import MonteCarloConfigService
from montecarlodata.queries.iac import (
    CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
    GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
)
from montecarlodata.utils import GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG


class MonteCarloConfigServiceTest(TestCase):
    maxDiff = None

    @patch("os.getcwd")
    def setUp(self, getcwd) -> None:
        self._request_wrapper_mock = Mock(spec=GqlWrapper)
        self._pycarlo_client = Mock(spec=Client)
        self._print_func = Mock(spec=click.echo)
        self.project_dir = self._get_project_dir("standalone_configs")
        getcwd.return_value = self.project_dir
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            print_func=self._print_func,
        )

    def test_standalone_configs(self):
        namespace = "test"
        files, template, _ = self.service.compile(namespace)
        self.assertEqual(len(files), 4)
        self.assertEqual(
            json.loads(json.dumps(template)),
            self._get_standalone_config_compiled_template(namespace),
        )

    def test_namespace_override(self):
        project_dir = self._get_project_dir("namespace_override")
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=project_dir,
            pycarlo_client=self._pycarlo_client,
        )
        files, template, _ = self.service.compile("test")

        self.assertEqual(len(files), 3)
        self.assertEqual(
            json.loads(json.dumps(template)),
            {
                "custom_namespace": {
                    "field_health": [
                        {
                            "table": "analytics:prod_lineage.lineage_nodes",
                            "timestamp_field": "created",
                        },
                        {"table": "analytics:prod.abc"},
                    ],
                    "freshness": [
                        {
                            "freshness_threshold": 30,
                            "schedule": {
                                "interval_minutes": 30,
                                "start_time": "2021-07-27T19:51:00",
                                "type": "fixed",
                            },
                            "table": "analytics:prod.abc",
                        }
                    ],
                },
                "infra": {
                    "dimension_tracking": [
                        {
                            "field": "account_id",
                            "table": "analytics:prod.customer_360",
                            "yaml_file_name": f"{project_dir}/monitors.yaml",
                            "yaml_line": 5,
                        }
                    ]
                },
                "test": {
                    "dimension_tracking": [
                        {
                            "field": "account_id",
                            "table": "analytics:prod.customer_360",
                            "yaml_file_name": f"{project_dir}/monitors_other.yml",
                            "yaml_line": 3,
                        }
                    ]
                },
            },
        )

    @parameterized.expand(
        [
            ("namespace_override", "montecarlo.yml"),
            ("namespace_override_yaml", "montecarlo.yaml"),
        ]
    )
    def test_namespace_override_no_default_namesapce(self, project_dir_name, config_file_name):
        project_dir = self._get_project_dir(project_dir_name)
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=project_dir,
            pycarlo_client=self._pycarlo_client,
        )
        files, template, errors = self.service.compile(None, abort_on_error=False)

        self.assertEqual(len(files), 3)
        self.assertEqual(
            json.loads(json.dumps(template)),
            {
                "custom_namespace": {
                    "field_health": [
                        {
                            "table": "analytics:prod_lineage.lineage_nodes",
                            "timestamp_field": "created",
                        },
                        {"table": "analytics:prod.abc"},
                    ],
                    "freshness": [
                        {
                            "freshness_threshold": 30,
                            "schedule": {
                                "interval_minutes": 30,
                                "start_time": "2021-07-27T19:51:00",
                                "type": "fixed",
                            },
                            "table": "analytics:prod.abc",
                        }
                    ],
                },
                "infra": {
                    "dimension_tracking": [
                        {
                            "field": "account_id",
                            "table": "analytics:prod.customer_360",
                            "yaml_file_name": f"{project_dir}/monitors.yaml",
                            "yaml_line": 5,
                        }
                    ]
                },
            },
        )
        self.assertEqual(len(errors), 1)
        file_name = next(iter(errors))
        self.assertTrue(
            f"tests/iac/test_resources/{project_dir_name}/monitors_other.yml" in file_name
        )
        self.assertTrue(
            "A default namespace need to be passed through command line --namespace "
            f"or set default namespace in {config_file_name} or an override namespace needs to be set in file"
            in errors[file_name][0]
        )

    def test_namespace_override_default_namespace_montecarlo_yaml(self):
        project_dir = self._get_project_dir("namespace_override_montecarlo")
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=project_dir,
            pycarlo_client=self._pycarlo_client,
        )

        files, template, errors = self.service.compile(None, abort_on_error=False)

        self.assertEqual(len(files), 3)
        self.assertEqual(
            json.loads(json.dumps(template)),
            {
                "custom_namespace": {
                    "field_health": [
                        {
                            "table": "analytics:prod_lineage.lineage_nodes",
                            "timestamp_field": "created",
                        },
                        {"table": "analytics:prod.abc"},
                    ],
                    "freshness": [
                        {
                            "freshness_threshold": 30,
                            "schedule": {
                                "interval_minutes": 30,
                                "start_time": "2021-07-27T19:51:00",
                                "type": "fixed",
                            },
                            "table": "analytics:prod.abc",
                        }
                    ],
                },
                "infra": {
                    "dimension_tracking": [
                        {
                            "field": "account_id",
                            "table": "analytics:prod.customer_360",
                            "yaml_file_name": f"{project_dir}/monitors.yml",
                            "yaml_line": 5,
                        }
                    ]
                },
                "test_montecarlo": {
                    "dimension_tracking": [
                        {
                            "field": "account_id",
                            "table": "analytics:prod.customer_360",
                            "yaml_file_name": f"{project_dir}/monitors_other.yml",
                            "yaml_line": 3,
                        }
                    ]
                },
            },
        )
        self.assertEqual(len(errors), 0)

    def test_embedded_dbt_configs(self):
        project_dir = self._get_project_dir("embedded_dbt_configs")
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=project_dir,
            pycarlo_client=self._pycarlo_client,
        )
        files, template, _ = self.service.compile("test")

        self.assertEqual(len(files), 4)
        self.assertEqual(
            json.loads(json.dumps(template)),
            {
                "test": {
                    "field_health": [
                        {
                            "table": "analytics:prod_lineage.lineage_nodes",
                            "timestamp_field": "created",
                        },
                        {"table": "analytics:prod.abc"},
                        {
                            "table": "analytics:prod.client_hub",
                            "fields": ["account_id"],
                            "yaml_line": 3,
                            "yaml_file_name": f"{project_dir}/dir1/dir2/monitors.yml",
                        },
                    ],
                    "freshness": [
                        {
                            "table": "analytics:prod.abc",
                            "freshness_threshold": 30,
                            "schedule": {
                                "type": "fixed",
                                "interval_minutes": 30,
                                "start_time": "2021-07-27T19:51:00",
                            },
                        }
                    ],
                    "dimension_tracking": [
                        {
                            "table": "analytics:prod.customer_360",
                            "field": "account_id",
                            "yaml_line": 3,
                            "yaml_file_name": f"{project_dir}/dir1/monitors.yml",
                        }
                    ],
                },
            },
        )

    def test_embedded_dbt_configs_with_refs(self):
        project_dir = self._get_project_dir("embedded_dbt_configs_with_refs")
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=project_dir,
            pycarlo_client=self._pycarlo_client,
            dbt_manifest_path=f"{project_dir}/manifest.json",
        )
        files, template, _ = self.service.compile("test")

        self.assertEqual(len(files), 4)
        self.assertEqual(
            json.loads(json.dumps(template)),
            {
                "test": {
                    "custom_sql": [
                        {
                            "notes": "{{query_result:link, connection_type}}",
                            "sampling_sql": "select * from analytics.prod.customer_360",
                            "sql": "select * from analytics.prod.def a join "
                            "analytics.prod.client_hub b on a.id = b.id",
                            "variables": {"foo": ["bar analytics.prod.def"]},
                        }
                    ],
                    "dimension_tracking": [
                        {
                            "field": "account_id",
                            "table": "analytics:prod.customer_360",
                            "yaml_file_name": f"{project_dir}/dir1/monitors.yml",
                            "yaml_line": 3,
                        }
                    ],
                    "field_health": [
                        {
                            "table": "analytics:prod_lineage.lineage_nodes",
                            "timestamp_field": "created",
                        },
                        {"table": "analytics:prod.def"},
                        {
                            "fields": ["account_id"],
                            "name": "a analytics:prod.client_hub or analytics:prod.def",
                            "table": "analytics:prod.client_hub",
                            "yaml_file_name": f"{project_dir}/dir1/dir2/monitors.yml",
                            "yaml_line": 3,
                        },
                    ],
                    "freshness": [
                        {
                            "freshness_threshold": 30,
                            "schedule": {
                                "interval_minutes": 30,
                                "start_time": "2021-07-27T19:51:00",
                                "type": "fixed",
                            },
                            "tables": [
                                "analytics:prod.def",
                                "analytics:prod.client_hub",
                            ],
                        }
                    ],
                }
            },
        )

    def test_invalid_configs(self):
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=self._get_project_dir("invalid_configs"),
            pycarlo_client=self._pycarlo_client,
        )
        self.service._abort_on_error = False

        files, template, errors_by_file = self.service.compile("test", abort_on_error=False)
        errors = sorted(list(errors_by_file.items()), key=lambda x: x[0])

        self.assertEqual(len(errors), 3)
        file, error = errors[0]
        self.assertTrue(file.endswith("dir1/dir2/monitors.yml"))
        self.assertEqual(error, ['"custom_sql" property should be a list.'])
        file, error = errors[1]
        self.assertTrue(file.endswith("dir1/monitors.yml"))
        self.assertEqual(error, ['"field_health" property should be a list.'])
        file, error = errors[2]
        self.assertTrue(file.endswith("dir1/repeated_key.yml"))
        self.assertEqual(
            error, ['Failed to parse YAML: Duplicate "dimension_tracking" key found in YAML.']
        )

    def test_yaml_references(self):
        project_dir = self._get_project_dir("yaml_references")
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            project_dir=self._get_project_dir("yaml_references"),
            pycarlo_client=self._pycarlo_client,
        )
        self.service._abort_on_error = False

        files, template, errors_by_file = self.service.compile("test", abort_on_error=False)
        self.assertEqual(
            template,
            {
                "test": {
                    "dimension_tracking": BoxList(
                        [
                            {
                                "lookback_days": 2,
                                "name": "dt-1-mac",
                                "yaml_line": 8,
                                "yaml_file_name": f"{project_dir}/dir1/repeated_key_references.yml",
                            },
                            {
                                "labels": ["Common (product)"],
                                "name": "dt-2-mac",
                                "yaml_line": 8,
                                "yaml_file_name": f"{project_dir}/dir1/yaml_references.yml",
                            },
                        ]
                    )
                }
            },
        )
        errors = sorted(list(errors_by_file.items()), key=lambda x: x[0])

        self.assertEqual(len(errors), 0)

    def test_apply(self):
        namespace = "foo"
        update_uuid = "eeeeeeee-58fd-44d0-8b2d-eeeeeeeeeeee"
        update_response = MonolithResponse(
            data={
                "response": {
                    "updateUuid": update_uuid,
                    "errorsAsJson": "{}",
                    "warningsAsJson": "{}",
                }
            }
        )
        poll_response = MonolithResponse(
            data={
                "state": "APPLIED",
                "resourceModifications": [
                    {
                        "type": "ResourceModificationType.UPDATE",
                        "description": "Monitor: type=stats, table=analytics:prod.client_hub",
                        "resourceAsJson": json.dumps(
                            {
                                "uuid": "ed4d07c3-58fd-44d0-8b2d-c1b020f45a69",
                                "resource": None,
                                "name": (
                                    "monitor|type=stats|table=analytics:prod.client_hub|"
                                    "timestamp_field=<<NULL>>|where_condition=<<NULL>>"
                                ),
                                "table": "analytics:prod.customer_360",
                                "type": "stats",
                                "fields": [],
                                "timestamp_field": None,
                                "where_condition": None,
                            }
                        ),
                    },
                    {
                        "type": "ResourceModificationType.UPDATE",
                        "description": "Monitor: type=categories, table=analytics:prod.customer_360",
                        "resourceAsJson": json.dumps(
                            {
                                "uuid": "ec3b0a80-d088-4dbe-acf5-150caf041574",
                                "resource": None,
                                "name": (
                                    "monitor|type=categories|table=analytics:prod.customer_360|"
                                    "timestamp_field=<<NULL>>|where_condition=<<NULL>>|fields=account_id"
                                ),
                                "table": "analytics:prod.customer_360",
                                "type": "categories",
                                "fields": ["account_id"],
                                "timestamp_field": None,
                                "where_condition": None,
                            }
                        ),
                    },
                ],
                "changesApplied": True,
                "errorsAsJson": "{}",
                "warningsAsJson": "{}",
            }
        )
        self._request_wrapper_mock.make_request_v2.side_effect = [
            update_response,
            poll_response,
            update_response,
            poll_response,
        ]

        responses = self.service.apply(namespace, skip_confirmation=True)

        compiled_template = self._get_standalone_config_compiled_template(namespace)

        self.assertEqual(
            [
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=json.dumps(compiled_template[namespace]),
                        dryRun=True,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=json.dumps(compiled_template[namespace]),
                        dryRun=False,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
            ],
            self._request_wrapper_mock.make_request_v2.mock_calls,
        )

        self.assertEqual(responses[0].errors, {})
        self.assertEqual(len(responses[0].resource_modifications), 2)

    def test_apply_dry_run(self):
        namespace = "foo"
        update_uuid = "eeeeeeee-58fd-44d0-8b2d-eeeeeeeeeeee"
        update_response = MonolithResponse(
            data={
                "response": {
                    "updateUuid": update_uuid,
                    "errorsAsJson": "{}",
                    "warningsAsJson": "{}",
                }
            }
        )
        poll_response = MonolithResponse(
            data={
                "state": "APPLIED",
                "resourceModifications": [
                    {
                        "type": "ResourceModificationType.UPDATE",
                        "description": "Monitor: type=stats, table=analytics:prod.client_hub",
                        "resourceAsJson": '{"uuid": "ed4d07c3-58fd-44d0-8b2d-c1b020f45a69", "resource": null, "name": "monitor|type=stats|table=analytics:prod.client_hub|timestamp_field=<<NULL>>|where_condition=<<NULL>>", "table": "analytics:prod.customer_360", "type": "stats", "fields": [], "timestamp_field": null, "where_condition": null}',
                    },
                    {
                        "type": "ResourceModificationType.UPDATE",
                        "description": "Monitor: type=categories, table=analytics:prod.customer_360",
                        "resourceAsJson": '{"uuid": "ec3b0a80-d088-4dbe-acf5-150caf041574", "resource": null, "name": "monitor|type=categories|table=analytics:prod.customer_360|timestamp_field=<<NULL>>|where_condition=<<NULL>>|fields=account_id", "table": "analytics:prod.customer_360", "type": "categories", "fields": ["account_id"], "timestamp_field": null, "where_condition": null}',
                    },
                ],
                "changesApplied": True,
                "errorsAsJson": "{}",
                "warningsAsJson": "{}",
            }
        )
        self._request_wrapper_mock.make_request_v2.side_effect = [
            update_response,
            poll_response,
        ]

        responses = self.service.apply(namespace, dry_run=True)

        compiled_template = self._get_standalone_config_compiled_template(namespace)

        self._request_wrapper_mock.make_request_v2.assert_has_calls(
            [
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=json.dumps(compiled_template[namespace]),
                        dryRun=True,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
            ]
        )

        self.assertEqual(responses[0].errors, {})
        self.assertEqual(len(responses[0].resource_modifications), 2)

    def test_apply_with_errors(self):
        namespace = "foo"
        update_uuid = "eeeeeeee-58fd-44d0-8b2d-eeeeeeeeeeee"
        self._request_wrapper_mock.make_request_v2.return_value = MonolithResponse(
            data={
                "response": {
                    "updateUuid": update_uuid,
                    "errorsAsJson": '{"validation_errors": {"monitors": {"0": {"type": ["Unknown field."]}}}}',
                    "warningsAsJson": "{}",
                }
            }
        )

        responses = self.service.apply(namespace, abort_on_error=False)
        compiled_template = self._get_standalone_config_compiled_template(namespace)

        self._request_wrapper_mock.make_request_v2.assert_called_once_with(
            query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
            operation="createOrUpdateMonteCarloConfigTemplateAsync",
            service="iac_service",
            variables=dict(
                namespace=namespace,
                configTemplateJson=json.dumps(compiled_template[namespace]),
                dryRun=True,
                misconfiguredAsWarning=True,
                resource=None,
                createNonIngestedTables=False,
            ),
        )

        self.assertEqual(
            responses[0].errors,
            {"validation_errors": {"monitors": {"0": {"type": ["Unknown field."]}}}},
        )
        self.assertEqual(len(responses[0].resource_modifications), 0)

    @parameterized.expand(
        [
            (
                "Failed to apply changes.",
                {"system_error": "Problem applying template resource: ..."},
                "FAILED",
                '{"system_error": "Problem applying template resource: ..."}',
            ),
            ("Update skipped in favor of more recent update.", {}, "SKIPPED", "{}"),
        ]
    )
    def test_apply_with_resource_apply_errors(
        self,
        expected_msg: str,
        expected_errors: dict,
        result_state: str,
        result_errors: str,
    ):
        namespace = "foo"
        update_uuid = "eeeeeeee-58fd-44d0-8b2d-eeeeeeeeeeee"
        update_response = MonolithResponse(
            data={
                "response": {
                    "updateUuid": update_uuid,
                    "errorsAsJson": "{}",
                }
            }
        )
        dry_run_poll_response = MonolithResponse(
            data={
                "state": "APPLIED",
                "resourceModifications": [
                    {
                        "type": "ResourceModificationType.UPDATE",
                        "description": "Monitor: type=stats, table=analytics:prod.client_hub",
                        "resourceAsJson": '{"uuid": "ed4d07c3-58fd-44d0-8b2d-c1b020f45a69", "resource": null, "name": "monitor|type=stats|table=analytics:prod.client_hub|timestamp_field=<<NULL>>|where_condition=<<NULL>>", "table": "analytics:prod.customer_360", "type": "stats", "fields": [], "timestamp_field": null, "where_condition": null}',
                    },
                    {
                        "type": "ResourceModificationType.UPDATE",
                        "description": "Monitor: type=categories, table=analytics:prod.customer_360",
                        "resourceAsJson": '{"uuid": "ec3b0a80-d088-4dbe-acf5-150caf041574", "resource": null, "name": "monitor|type=categories|table=analytics:prod.customer_360|timestamp_field=<<NULL>>|where_condition=<<NULL>>|fields=account_id", "table": "analytics:prod.customer_360", "type": "categories", "fields": ["account_id"], "timestamp_field": null, "where_condition": null}',
                    },
                ],
                "changesApplied": False,
                "errorsAsJson": "{}",
                "warningsAsJson": "{}",
            }
        )
        wet_poll_response = MonolithResponse(
            data={
                "state": result_state,
                "resourceModifications": [],
                "changesApplied": False,
                "errorsAsJson": result_errors,
            }
        )
        self._request_wrapper_mock.make_request_v2.side_effect = [
            update_response,
            dry_run_poll_response,
            update_response,
            wet_poll_response,
        ]

        responses = self.service.apply(
            namespace,
            skip_confirmation=True,
            abort_on_error=False,
        )

        compiled_template = self._get_standalone_config_compiled_template(namespace)

        self._request_wrapper_mock.make_request_v2.assert_has_calls(
            [
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=json.dumps(compiled_template[namespace]),
                        dryRun=True,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=json.dumps(compiled_template[namespace]),
                        dryRun=False,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
            ]
        )

        self.assertEqual(responses[0].errors, expected_errors)
        self.assertEqual(len(responses[0].resource_modifications), 0)
        self._print_func.assert_has_calls([call(expected_msg)])

    def test_misconfigured_warnings(self):
        namespace = "foo"
        update_uuid = "eeeeeeee-58fd-44d0-8b2d-eeeeeeeeeeee"
        update_response = MonolithResponse(
            data={
                "response": {
                    "updateUuid": update_uuid,
                    "errorsAsJson": "{}",
                    "warningsAsJson": "{}",
                }
            }
        )
        poll_response = MonolithResponse(
            data={
                "state": "APPLIED",
                "resourceModifications": [
                    {
                        "type": "ResourceModificationType.CREATE",
                        "description": (
                            "Freshness SLO: "
                            "tables=['analytics:prod.client_hub', 'analytics:prod.client_warehouses'] "
                            "freshness_threshold=1"
                        ),
                        "resourceAsJson": json.dumps(
                            {
                                "uuid": None,
                                "resource": None,
                                "name": "freshnessrule|tables=(multiple)",
                                "description": None,
                                "notes": None,
                                "labels": [],
                                "schedule": {
                                    "type": "fixed",
                                    "interval_minutes": 1,
                                    "interval_crontab": None,
                                    "start_time": "2021-07-27T19:00:00",
                                },
                                "table": None,
                                "tables": [
                                    "analytics:prod.client_hub",
                                    "analytics:prod.client_warehouses",
                                ],
                                "freshness_threshold": 1,
                            }
                        ),
                    }
                ],
                "changesApplied": False,
                "errorsAsJson": "{}",
                "warningsAsJson": json.dumps(
                    {
                        "misconfigured_warnings": [
                            {
                                "title": "High breaching Freshness SLOs are defined, adjust freshness_threshold in",
                                "items": [
                                    (
                                        "analytics:prod.client_hub: "
                                        "freshness_threshold is 1, the expected minimum threshold is 464"
                                    ),
                                    (
                                        "analytics:prod.client_warehouses: "
                                        "freshness_threshold is 1, the expected minimum threshold is 1440"
                                    ),
                                ],
                            }
                        ]
                    }
                ),
            }
        )
        self._request_wrapper_mock.make_request_v2.side_effect = [
            update_response,
            poll_response,
            update_response,
            poll_response,
        ]

        responses = self.service.apply(namespace, abort_on_error=False, skip_confirmation=True)

        self._request_wrapper_mock.make_request_v2.assert_has_calls(
            [
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=ANY,
                        dryRun=True,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
                call(
                    query=CREATE_OR_UPDATE_MONTE_CARLO_CONFIG_TEMPLATE_ASYNC,
                    operation="createOrUpdateMonteCarloConfigTemplateAsync",
                    service="iac_service",
                    variables=dict(
                        namespace=namespace,
                        configTemplateJson=ANY,
                        dryRun=False,
                        misconfiguredAsWarning=True,
                        resource=None,
                        createNonIngestedTables=False,
                    ),
                ),
                call(
                    query=GET_MONTE_CARLO_CONFIG_TEMPLATE_UPDATE_STATE,
                    operation="getMonteCarloConfigTemplateUpdateState",
                    service="iac_service",
                    variables=dict(updateUuid=update_uuid),
                ),
            ]
        )

        self.assertEqual(
            responses[0].warnings,
            {
                "misconfigured_warnings": [
                    {
                        "items": [
                            (
                                "analytics:prod.client_hub: freshness_threshold is 1, the expected "
                                "minimum threshold is 464"
                            ),
                            (
                                "analytics:prod.client_warehouses: freshness_threshold is 1, the expected "
                                "minimum threshold is 1440"
                            ),
                        ],
                        "title": "High breaching Freshness SLOs are defined, adjust freshness_threshold in",
                    }
                ]
            },
        )
        self.assertEqual(len(responses[0].resource_modifications), 1)
        self._print_func.assert_has_calls([call("Changes successfully applied.")])

    def test_list_namespaces(self):
        self._pycarlo_client.return_value = self._mc_config_templates_response(self.LIMIT)
        self.service.list_namespaces(self.LIMIT)
        self._print_func.assert_called_once_with(self.NAMESPACES_TABLE)

    def test_list_namespaces_with_more_available(self):
        self._pycarlo_client.return_value = self._mc_config_templates_response(self.LIMIT + 1)
        self.service.list_namespaces(self.LIMIT)
        expected_calls = [
            call(self.NAMESPACES_TABLE),
            call(self.service.MORE_NS_MESSAGE),
        ]
        self._print_func.assert_has_calls(expected_calls)

    def test_compile_command_no_namespace(self):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        dir = self._get_project_dir("namespace_override")
        result = runner.invoke(
            compile_config,
            obj={"config": ctx},
            args=["--project-dir", dir, "--namespace", None],
        )

        self.assertEqual(
            result.output,
            (
                "\n"
                "Gathering monitor configuration files.\n"
                " - "
                f"{dir}/dbt_models/schema.yml "
                "- Embedded monitor configuration found.\n"
                " - "
                f"{dir}/monitors.yaml "
                "- Monitor configuration found.\n"
                "\n"
                "Configuration validation errors:\n"
                " - File: "
                f"{dir}/monitors_other.yml\n"
                "    - A default namespace need to be passed through command line --namespace "
                "or set default namespace in montecarlo.yml or an override namespace needs to "
                "be set in file: "
                f"{dir}/monitors_other.yml\n"
                "\n"
                "Error - Errors encountered, exiting.\n"
                "Aborted!\n"
            ),
        )

    def test_compile_command_ns_config(self):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        dir = self._get_project_dir("namespace_override_montecarlo")
        result = runner.invoke(
            compile_config,
            obj={"config": ctx},
            args=["--project-dir", dir, "--namespace", None],
        )

        self.assertEqual(
            result.output,
            (
                "\n"
                "Gathering monitor configuration files.\n"
                "namespace: test_montecarlo found in montecarlo.yml ignoring value passed "
                "with --namespace=None\n"
                " - "
                f"{dir}/dbt_models/schema.yml "
                "- Embedded monitor configuration found.\n"
                " - "
                f"{dir}/monitors.yml "
                "- Monitor configuration found.\n"
                " - "
                f"{dir}/monitors_other.yml "
                "- Monitor configuration found.\n"
            ),
        )

    def test_compile_command_ns_param(self):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        dir = self._get_project_dir("namespace_override")
        result = runner.invoke(
            compile_config,
            obj={"config": ctx},
            args=["--project-dir", dir, "--namespace", "test-mont"],
        )

        self.assertEqual(
            result.output,
            (
                "\n"
                "Gathering monitor configuration files.\n"
                " - "
                f"{dir}/dbt_models/schema.yml "
                "- Embedded monitor configuration found.\n"
                " - "
                f"{dir}/monitors.yaml "
                "- Monitor configuration found.\n"
                " - "
                f"{dir}/monitors_other.yml "
                "- Monitor configuration found.\n"
            ),
        )

    def test_compile_command_ns_config_param(self):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        dir = self._get_project_dir("namespace_override_montecarlo")
        result = runner.invoke(
            compile_config,
            obj={"config": ctx},
            args=["--project-dir", dir, "--namespace", "test-namespace"],
        )

        self.assertEqual(
            result.output,
            (
                "\n"
                "Gathering monitor configuration files.\n"
                "namespace: test_montecarlo found in montecarlo.yml ignoring value passed "
                "with --namespace=test-namespace\n"
                " - "
                f"{dir}/dbt_models/schema.yml "
                "- Embedded monitor configuration found.\n"
                " - "
                f"{dir}/monitors.yml "
                "- Monitor configuration found.\n"
                " - "
                f"{dir}/monitors_other.yml "
                "- Monitor configuration found.\n"
            ),
        )

    @freeze_time("2020-01-01")
    def test_generate_from_dbt_tests(self):
        project_dir = self._get_project_dir("import_dbt_tests")
        output_path = f"{project_dir}/dbt.yml"
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            dbt_manifest_path=f"{project_dir}/manifest.json",
        )
        self.service.generate_from_dbt_tests(output_path)

        with open(f"{project_dir}/expected.yml", "r") as f:
            expected_yaml = f.read()

        with open(output_path, "r") as f:
            output_yaml = f.read()

        self.assertEqual(expected_yaml, output_yaml)

    @freeze_time("2020-01-01")
    def test_generate_from_dbt_tests_when_filtered_and_labeled(self):
        project_dir = self._get_project_dir("import_dbt_tests")
        output_path = f"{project_dir}/dbt.yml"
        self.service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            dbt_manifest_path=f"{project_dir}/manifest.json",
        )
        self.service.generate_from_dbt_tests(
            output_path,
            test_types=["SINGULAR", "unique"],
            labels=["foo", "bar"],
        )

        with open(output_path, "r") as f:
            output_yaml = f.read()

        self.assertEqual(
            """\
montecarlo:
  custom_sql:
  - name: test.analytics.assert_not_null_recent_metrics_resource_id
    description: test.analytics.assert_not_null_recent_metrics_resource_id
    sql: |
      SELECT
          *
      FROM
          personal.dbt_bneville.recent_metrics
      WHERE
          resource_id IS NULL AND
          metric != 'total_views'
    schedule:
      type: fixed
      start_time: '2020-01-01T00:00:00+00:00'
      interval_minutes: 720
    comparisons:
    - type: threshold
      operator: GT
      threshold_value: 0
    labels:
    - bar
    - foo
  - name: test.analytics.unique_table_field_metrics_multi_key.14e928c2e4
    description: test.analytics.unique_table_field_metrics_multi_key.14e928c2e4
    sql: |
      select
          multi_key as unique_field,
          count(*) as n_records

      from personal.dbt_bneville.table_field_metrics
      where multi_key is not null
      group by multi_key
      having count(*) > 1
    schedule:
      type: fixed
      start_time: '2020-01-01T00:00:00+00:00'
      interval_minutes: 720
    comparisons:
    - type: threshold
      operator: GT
      threshold_value: 0
    labels:
    - bar
    - foo\n""",
            output_yaml,
        )

    def _get_project_dir(self, dir_name: str):
        return os.path.join(pathlib.Path(__file__).parent.resolve(), "test_resources", dir_name)

    def _get_temp_dir(self, dir_name: str):
        return os.path.join(
            pathlib.Path(__file__).parent.resolve(), "test_resources", "temp", dir_name
        )

    LIMIT = 2
    NAMESPACES_TABLE = """\
╒═════════════╤══════════════════════════════════╕
│ Namespace   │ Last Update Time                 │
╞═════════════╪══════════════════════════════════╡
│ namespace_1 │ 2000-01-01 00:00:00.000000+00:00 │
├─────────────┼──────────────────────────────────┤
│ namespace_2 │ 2000-01-01 00:00:00.000000+00:00 │
╘═════════════╧══════════════════════════════════╛"""

    @responses.activate
    def test_convert_to_ui(self):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "convertConfigTemplateToUiMonitors": {
                        "response": {
                            "monitors": [
                                {"uuid": "uuid1", "name": "test1"},
                                {"uuid": "uuid2", "name": "test2"},
                            ],
                        }
                    }
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            convert_to_ui,
            obj={"config": ctx},
            args=["--namespace", "test-namespace", "--dry-run"],
        )
        self.assertEqual(
            result.output,
            """Exported the following monitors to UI:
* uuid1: test1
* uuid2: test2
""",
        )

    @patch("os.getcwd")
    @responses.activate
    def test_convert_to_mac(self, getcwd):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "convertUiMonitorsToConfigTemplate": {
                        "response": {
                            "configTemplateAsDict": json.dumps({"foo": "bar"}),
                            "errors": [],
                            "warnings": [],
                        },
                    },
                }
            },
        )

        dir = self._get_temp_dir("convert_to_mac")
        shutil.rmtree(dir, ignore_errors=True)

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            convert_to_mac,
            obj={"config": ctx},
            args=["--namespace", "test-namespace", "--project-dir", dir, "--dry-run"],
        )
        self.assertEqual(result.output, f"Wrote monitor config to {dir}.\n")

        getcwd.return_value = dir
        service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            print_func=self._print_func,
        )

        files, template, _ = service.compile("test")

        self.assertEqual(len(files), 1)
        self.assertEqual(json.loads(json.dumps(template)), {"test-namespace": {"foo": "bar"}})

    @patch("os.getcwd")
    @responses.activate
    def test_convert_to_mac_with_monitors_file(self, getcwd):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "convertUiMonitorsToConfigTemplate": {
                        "response": {
                            "configTemplateAsDict": json.dumps({"foo": "bar"}),
                            "errors": [],
                            "warnings": [],
                        },
                    },
                }
            },
        )

        dir = self._get_temp_dir("convert_to_mac")
        monitors_file = os.path.join(self._get_project_dir("convert_to_mac"), "monitors_uuids")
        shutil.rmtree(dir, ignore_errors=True)

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            convert_to_mac,
            obj={"config": ctx},
            args=[
                "--namespace",
                "test-namespace",
                "--project-dir",
                dir,
                "--dry-run",
                "--monitors-file",
                monitors_file,
            ],
        )
        self.assertEqual(result.output, f"Wrote monitor config to {dir}.\n")

        getcwd.return_value = dir
        service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            print_func=self._print_func,
        )

        files, template, _ = service.compile("test")

        self.assertEqual(len(files), 1)
        self.assertEqual(json.loads(json.dumps(template)), {"test-namespace": {"foo": "bar"}})

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            json.loads(responses.calls[0].request.body)["variables"],
            {
                "allMonitors": False,
                "dryRun": True,
                "monitorUuids": [
                    "2eb76621-3344-421a-bf8c-835173ef2d70",
                    "807cb339-1d9c-4234-a945-1e85de54513b",
                ],
                "namespace": "test-namespace",
            },
        )

    @patch("os.getcwd")
    @responses.activate
    def test_export_as_latest_with_monitors_file(self, getcwd):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "exportLatestVersionMonitorReplacementTemplates": {
                        "configTemplateAsYaml": "foo: bar",
                        "errors": [],
                    },
                }
            },
        )

        monitors_file = os.path.join(self._get_project_dir("export_as_latest"), "monitors_uuids")

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            export_as_latest,
            obj={"config": ctx},
            args=[
                "--namespace",
                "test-namespace",
                "--monitors-file",
                monitors_file,
            ],
        )
        self.assertEqual(result.output, "foo: bar\n")

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            json.loads(responses.calls[0].request.body)["variables"],
            {
                "namespace": "test-namespace",
                "monitorUuids": [
                    "2eb76621-3344-421a-bf8c-835173ef2d70",
                    "807cb339-1d9c-4234-a945-1e85de54513b",
                ],
            },
        )

    @patch("os.getcwd")
    @responses.activate
    def test_get_template(self, getcwd):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "getMonteCarloConfigTemplates": {
                        "edges": [
                            {
                                "node": {
                                    "template": json.dumps({"foo": "bar"}),
                                }
                            }
                        ],
                    },
                }
            },
        )

        dir = self._get_temp_dir("get_template")
        shutil.rmtree(dir, ignore_errors=True)

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            get_template,
            obj={"config": ctx},
            args=["--namespace", "test-namespace", "--project-dir", dir],
        )
        self.assertEqual(result.output, f"Wrote monitor config to {dir}.\n")

        getcwd.return_value = dir
        service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            print_func=self._print_func,
        )

        files, template, _ = service.compile("test")

        self.assertEqual(len(files), 1)
        self.assertEqual(json.loads(json.dumps(template)), {"test-namespace": {"foo": "bar"}})

    @staticmethod
    def _mc_config_templates_response(namespace_count):
        return Box(
            {
                "get_monte_carlo_config_templates": {
                    "edges": [
                        {
                            "node": {
                                "namespace": f"namespace_{i}",
                                "last_update_time": "2000-01-01 00:00:00.000000+00:00",
                            }
                        }
                        for i in range(1, namespace_count + 1)
                    ]
                }
            }
        )

    def _get_standalone_config_compiled_template(self, namespace):
        return {
            namespace: {
                "field_health": [
                    {
                        "table": "analytics:prod.client_hub",
                        "fields": ["account_id"],
                        "yaml_line": 3,
                        "yaml_file_name": f"{self.project_dir}/dir1/dir2/monitors.yml",
                    },
                    {
                        "table": "analytics:prod.client_hub_2",
                        "fields": ["account_id"],
                        "yaml_line": 3,
                        "yaml_file_name": f"{self.project_dir}/dir1/dir2/monitors_additional.yml",
                    },
                ],
                "notifications": {
                    "email": [
                        {
                            "name": "email2",
                            "emails": ["foo2@bar.com"],
                            "audiences": ["audience2"],
                            "yaml_line": 8,
                            "yaml_file_name": f"{self.project_dir}/dir1/dir2/monitors.yml",
                        },
                        {
                            "name": "email3",
                            "emails": ["foo3@bar.com"],
                            "audiences": ["audience3"],
                            "yaml_line": 11,
                            "yaml_file_name": f"{self.project_dir}/dir1/dir2/monitors_additional.yml",
                        },
                        {
                            "name": "email1",
                            "emails": ["foo@bar.com"],
                            "audiences": ["audience1"],
                            "yaml_line": 7,
                            "yaml_file_name": f"{self.project_dir}/dir1/monitors.yml",
                        },
                    ],
                    "yaml_line": 6,
                    "yaml_file_name": f"{self.project_dir}/dir1/monitors.yml",
                    "slack": [
                        {
                            "name": "slack1",
                            "channel": "channel1",
                            "audiences": ["audience2"],
                            "yaml_line": 11,
                            "yaml_file_name": f"{self.project_dir}/dir1/monitors.yml",
                        }
                    ],
                },
                "dimension_tracking": [
                    {
                        "table": "analytics:prod.customer_360_2",
                        "field": "account_id",
                        "yaml_line": 7,
                        "yaml_file_name": f"{self.project_dir}/dir1/dir2/monitors_additional.yml",
                    },
                    {
                        "table": "analytics:prod.customer_360",
                        "field": "account_id",
                        "yaml_line": 3,
                        "yaml_file_name": f"{self.project_dir}/dir1/monitors.yml",
                    },
                ],
            },
        }

    @patch("os.getcwd")
    @responses.activate
    def test_export_migrated_dt(self, getcwd: Mock):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "exportDimensionTrackingMonitorMigrationTemplates": {
                        "configTemplateAsYaml": "foo: bar",
                        "errors": [],
                    },
                }
            },
        )

        result = runner.invoke(
            export_migrated_dt,
            obj={"config": ctx},
            args=["--namespace", "ui"],
        )

        assert result.output == "foo: bar\n"

    @patch("os.getcwd")
    @responses.activate
    def test_convert_to_mac_with_monitor_uuids(self, getcwd):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "convertUiMonitorsToConfigTemplate": {
                        "response": {
                            "configTemplateAsDict": json.dumps({"foo": "bar"}),
                            "errors": [],
                            "warnings": [],
                        },
                    },
                }
            },
        )

        dir = self._get_temp_dir("convert_to_mac")
        shutil.rmtree(dir, ignore_errors=True)

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            convert_to_mac,
            obj={"config": ctx},
            args=[
                "--namespace",
                "test-namespace",
                "--project-dir",
                dir,
                "--dry-run",
                "--monitor-uuids",
                "2eb76621-3344-421a-bf8c-835173ef2d70,807cb339-1d9c-4234-a945-1e85de54513b",
            ],
        )
        self.assertEqual(result.output, f"Wrote monitor config to {dir}.\n")

        getcwd.return_value = dir
        service = MonteCarloConfigService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper_mock,
            pycarlo_client=self._pycarlo_client,
            print_func=self._print_func,
        )

        files, template, _ = service.compile("test")

        self.assertEqual(len(files), 1)
        self.assertEqual(json.loads(json.dumps(template)), {"test-namespace": {"foo": "bar"}})

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            json.loads(responses.calls[0].request.body)["variables"],
            {
                "allMonitors": False,
                "dryRun": True,
                "monitorUuids": [
                    "2eb76621-3344-421a-bf8c-835173ef2d70",
                    "807cb339-1d9c-4234-a945-1e85de54513b",
                ],
                "namespace": "test-namespace",
            },
        )

    @responses.activate
    def test_export_with_monitor_uuids(self):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "exportMonteCarloConfigTemplates": {
                        "configTemplateAsYaml": "foo: bar",
                        "errors": [],
                    },
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            export,
            obj={"config": ctx},
            args=[
                "--monitor-uuids",
                "2eb76621-3344-421a-bf8c-835173ef2d70,807cb339-1d9c-4234-a945-1e85de54513b",
            ],
        )
        self.assertEqual(result.output, "foo: bar\n")

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            json.loads(responses.calls[0].request.body)["variables"],
            {
                "exportName": True,
                "monitorUuids": [
                    "2eb76621-3344-421a-bf8c-835173ef2d70",
                    "807cb339-1d9c-4234-a945-1e85de54513b",
                ],
            },
        )

    @responses.activate
    def test_export_with_monitors_file(self):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "exportMonteCarloConfigTemplates": {
                        "configTemplateAsYaml": "foo: bar",
                        "errors": [],
                    },
                }
            },
        )

        monitors_file = os.path.join(self._get_project_dir("export_as_latest"), "monitors_uuids")

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            export,
            obj={"config": ctx},
            args=[
                "--monitors-file",
                monitors_file,
            ],
        )
        self.assertEqual(result.output, "foo: bar\n")

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            json.loads(responses.calls[0].request.body)["variables"],
            {
                "exportName": True,
                "monitorUuids": [
                    "2eb76621-3344-421a-bf8c-835173ef2d70",
                    "807cb339-1d9c-4234-a945-1e85de54513b",
                ],
            },
        )

    @responses.activate
    def test_export_with_export_name_false(self):
        responses.post(
            _SAMPLE_CONFIG.mcd_api_endpoint,
            json={
                "data": {
                    "exportMonteCarloConfigTemplates": {
                        "configTemplateAsYaml": "foo: bar",
                        "errors": [],
                    },
                }
            },
        )

        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            export,
            obj={"config": ctx},
            args=[
                "--monitor-uuids",
                "2eb76621-3344-421a-bf8c-835173ef2d70",
                "--export-name",
                "false",
            ],
        )
        self.assertEqual(result.output, "foo: bar\n")

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            json.loads(responses.calls[0].request.body)["variables"],
            {
                "exportName": False,
                "monitorUuids": [
                    "2eb76621-3344-421a-bf8c-835173ef2d70",
                ],
            },
        )

    def test_export_with_both_params(self):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            export,
            obj={"config": ctx},
            args=[
                "--monitor-uuids",
                "2eb76621-3344-421a-bf8c-835173ef2d70",
                "--monitors-file",
                "some_file.txt",
            ],
        )
        self.assertIn("Cannot use both --monitor-uuids and --monitors-file", result.output)
        self.assertNotEqual(result.exit_code, 0)

    def test_export_with_no_params(self):
        ctx = _SAMPLE_CONFIG
        runner = CliRunner()
        result = runner.invoke(
            export,
            obj={"config": ctx},
            args=[],
        )
        self.assertIn("You must provide either --monitor-uuids or --monitors-file", result.output)
        self.assertNotEqual(result.exit_code, 0)
