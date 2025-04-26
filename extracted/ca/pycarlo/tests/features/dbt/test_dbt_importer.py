import pathlib
from typing import Any
from unittest import TestCase
from unittest.mock import Mock, call, patch
from uuid import uuid4

from box import Box

from pycarlo.common.files import BytesFileReader, JsonFileReader
from pycarlo.features.dbt import DbtImporter
from pycarlo.features.dbt.queries import (
    GET_DBT_UPLOAD_URL,
    SEND_DBT_ARTIFACTS_EVENT,
)
from pycarlo.features.pii import PiiFilterer
from pycarlo.features.user import Resource


class DbtImportServiceTest(TestCase):
    manifest_path = f"{pathlib.Path(__file__).parent}/sample_manifest.json"
    run_results_path = f"{pathlib.Path(__file__).parent}/sample_run_results.json"
    logs_path = f"{pathlib.Path(__file__).parent}/sample_logs.txt"

    def setUp(self) -> None:
        self._mock_pii_service = Mock()
        self._mock_pii_service.get_pii_filters_config.return_value = None

    @patch("pycarlo.features.dbt.dbt_importer.http")
    def test_import_run(self, mock_http: Mock):
        # given
        resource = Resource(id=uuid4(), name="Snowflake", type="snowflake")
        mock_user_service = Mock()
        mock_user_service.get_resource.return_value = resource

        def mock_client_responses(**kwargs: Any):
            query = kwargs["query"]
            if query == GET_DBT_UPLOAD_URL:
                return Box({"get_dbt_upload_url": f"https://{kwargs['variables']['fileName']}"})

        mock_client = Mock(side_effect=mock_client_responses)

        importer = DbtImporter(
            mc_client=mock_client,
            user_service=mock_user_service,
            pii_service=self._mock_pii_service,
        )

        # when
        importer.import_run(
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=resource.id,
        )

        # verify expected call to user service
        mock_user_service.get_resource.assert_called_once_with(resource.id)

        # verify expected calls to upload artifacts to S3
        self.assertEqual(3, mock_http.upload.call_count)
        mock_http.upload.assert_has_calls(
            [
                call(
                    method="put",
                    url="https://sample_manifest.json",
                    content=JsonFileReader(self.manifest_path).read(),
                ),
                call(
                    method="put",
                    url="https://sample_run_results.json",
                    content=JsonFileReader(self.run_results_path).read(),
                ),
                call(
                    method="put",
                    url="https://sample_logs.txt",
                    content=BytesFileReader(self.logs_path).read(),
                ),
            ]
        )

        # verify expected MC client calls
        self.assertEqual(4, mock_client.call_count)
        mock_client.assert_has_calls(
            [
                call(
                    query=GET_DBT_UPLOAD_URL,
                    variables=dict(
                        projectName="default-project",
                        invocationId="3b44f6e7-0a4a-4c81-8859-468b2d15075e",
                        fileName="sample_manifest.json",
                    ),
                    additional_headers={
                        "x-mcd-telemetry-reason": "service",
                        "x-mcd-telemetry-service": "dbt_importer",
                    },
                ),
                call(
                    query=GET_DBT_UPLOAD_URL,
                    variables=dict(
                        projectName="default-project",
                        invocationId="3b44f6e7-0a4a-4c81-8859-468b2d15075e",
                        fileName="sample_run_results.json",
                    ),
                    additional_headers={
                        "x-mcd-telemetry-reason": "service",
                        "x-mcd-telemetry-service": "dbt_importer",
                    },
                ),
                call(
                    query=GET_DBT_UPLOAD_URL,
                    variables=dict(
                        projectName="default-project",
                        invocationId="3b44f6e7-0a4a-4c81-8859-468b2d15075e",
                        fileName="sample_logs.txt",
                    ),
                    additional_headers={
                        "x-mcd-telemetry-reason": "service",
                        "x-mcd-telemetry-service": "dbt_importer",
                    },
                ),
                call(
                    query=SEND_DBT_ARTIFACTS_EVENT,
                    variables=dict(
                        projectName="default-project",
                        jobName="default-job",
                        invocationId="3b44f6e7-0a4a-4c81-8859-468b2d15075e",
                        artifacts=dict(
                            manifest="sample_manifest.json",
                            runResults="sample_run_results.json",
                            logs="sample_logs.txt",
                        ),
                        resourceId=str(resource.id),
                    ),
                    additional_headers={
                        "x-mcd-telemetry-reason": "service",
                        "x-mcd-telemetry-service": "dbt_importer",
                    },
                ),
            ]
        )

    @patch("pycarlo.features.dbt.dbt_importer.http")
    @patch("pycarlo.features.dbt.DbtImporter._init_pii_filterer")
    def test_import_run_filtered(self, mock_init_filterer: Mock, mock_http: Mock):
        resource = Resource(id=uuid4(), name="Snowflake", type="snowflake")
        mock_user_service = Mock()
        mock_user_service.get_resource.return_value = resource

        mock_init_filterer.return_value = PiiFilterer(
            filters_config={"active": [{"name": "thread-id", "pattern": r"Thread-\d{2}"}]},
            include_metrics=False,
        )

        def mock_client_responses(**kwargs: Any):
            query = kwargs["query"]
            if query == GET_DBT_UPLOAD_URL:
                return Box({"get_dbt_upload_url": f"https://{kwargs['variables']['fileName']}"})

        mock_client = Mock(side_effect=mock_client_responses)

        importer = DbtImporter(
            mc_client=mock_client,
            user_service=mock_user_service,
            pii_service=self._mock_pii_service,
        )

        # when
        importer.import_run(
            manifest_path=self.manifest_path,
            run_results_path=self.run_results_path,
            logs_path=self.logs_path,
            resource_id=resource.id,
        )

        expected_run_results = JsonFileReader(self.run_results_path).read()
        for r in expected_run_results["results"]:
            r["thread_id"] = "<filtered:thread-id>"

        # verify call was properly filtered, we know there are thread ids in sample run results
        mock_http.upload.assert_has_calls(
            [
                call(
                    method="put",
                    url="https://sample_run_results.json",
                    content=expected_run_results,
                ),
            ]
        )
