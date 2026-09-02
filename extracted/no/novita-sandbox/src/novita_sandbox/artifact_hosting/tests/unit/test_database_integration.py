"""Unit tests for TiDB Cloud database integration models and deploy flow."""

from unittest.mock import MagicMock

import pytest

from novita_sandbox.artifact_hosting.client import DeploymentClient
from novita_sandbox.artifact_hosting.models.deployment import Deployment
from novita_sandbox.artifact_hosting.models.nested import (
    DatabaseInfo,
    DeploymentMetadata,
)
from novita_sandbox.artifact_hosting.models.project import Project


class TestDatabaseInfoFromDict:
    def test_from_dict_full_data(self):
        data = {
            "status": "ACTIVE",
            "provider": "tidb_cloud",
            "host": "gateway01.us-east-1.prod.aws.tidbcloud.com",
            "port": 4000,
            "databaseName": "app_data",
            "databaseUrl": "mysql+pymysql://user:***@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/app_data",
            "createdAt": "2026-03-25T10:00:00Z",
        }

        info = DatabaseInfo.from_dict(data)

        assert info.status == "ACTIVE"
        assert info.provider == "tidb_cloud"
        assert info.host == "gateway01.us-east-1.prod.aws.tidbcloud.com"
        assert info.port == 4000
        assert info.database_name == "app_data"
        assert info.database_url == "mysql+pymysql://user:***@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/app_data"
        assert info.created_at == "2026-03-25T10:00:00Z"

    def test_from_dict_minimal_data(self):
        info = DatabaseInfo.from_dict({"status": "PROVISIONING"})

        assert info.status == "PROVISIONING"
        assert info.provider == "tidb_cloud"
        assert info.host is None
        assert info.port is None
        assert info.database_name is None
        assert info.database_url is None
        assert info.created_at is None


class TestDatabaseInfoToDict:
    def test_to_dict_roundtrip(self):
        original = {
            "status": "ACTIVE",
            "provider": "tidb_cloud",
            "host": "gateway01.us-east-1.prod.aws.tidbcloud.com",
            "port": 4000,
            "databaseName": "app_data",
            "databaseUrl": "mysql+pymysql://user:***@host:4000/app_data",
            "createdAt": "2026-03-25T10:00:00Z",
        }

        assert DatabaseInfo.from_dict(original).to_dict() == original


class TestDeploymentMetadataDatabase:
    def test_from_dict_with_database_true(self):
        metadata = DeploymentMetadata.from_dict(
            {
                "environmentVariables": {"NODE_ENV": "production"},
                "httpPort": 3000,
                "database": True,
                "replicaSpec": {
                    "cpu": "1",
                    "memory": "1Gi",
                    "maxReplicas": 1,
                    "minReplicas": 0,
                },
            }
        )

        assert metadata.database is True
        assert metadata.http_port == 3000
        assert metadata.environment_variables == {"NODE_ENV": "production"}

    def test_to_dict_with_database_true(self):
        result = DeploymentMetadata(database=True).to_dict()

        assert result["database"] is True
        assert result["httpPort"] == 3000

    def test_to_dict_with_database_false(self):
        result = DeploymentMetadata(database=False).to_dict()

        assert "database" not in result


class TestProjectWithDatabaseInfo:
    def test_from_dict_with_database_info(self, sample_project_data):
        mock_client = MagicMock(spec=DeploymentClient)
        data = sample_project_data.copy()
        data["databaseInfo"] = {
            "status": "ACTIVE",
            "provider": "tidb_cloud",
            "host": "gateway01.us-east-1.prod.aws.tidbcloud.com",
            "port": 4000,
            "databaseName": "app_data",
            "databaseUrl": "mysql+pymysql://user:***@gateway01.us-east-1.prod.aws.tidbcloud.com:4000/app_data",
            "createdAt": "2026-03-25T10:00:00Z",
        }

        project = Project.from_dict(data, mock_client)

        assert project.database_info is not None
        assert isinstance(project.database_info, DatabaseInfo)
        assert project.database_info.status == "ACTIVE"
        assert project.database_info.database_name == "app_data"

    def test_from_dict_without_database_info(self, sample_project_data):
        project = Project.from_dict(sample_project_data, MagicMock(spec=DeploymentClient))

        assert project.database_info is None

    def test_ensure_database_updates_project_database_info(self, sample_project_data):
        mock_client = MagicMock(spec=DeploymentClient)
        expected_database_info = DatabaseInfo(
            status="ACTIVE",
            database_url="mysql+pymysql://user:password@host:4000/app_data",
        )
        mock_client.ensure_project_database.return_value = expected_database_info

        project = Project.from_dict(sample_project_data, mock_client)
        database_info = project.ensure_database()

        mock_client.ensure_project_database.assert_called_once_with("proj_xxx")
        assert database_info is expected_database_info
        assert project.database_info is expected_database_info


class TestDeployWithDatabase:
    @pytest.fixture
    def mock_project(self, sample_project_data, sample_deployment_data):
        mock_client = MagicMock(spec=DeploymentClient)
        mock_client._http = MagicMock()
        mock_client._http.post.return_value = sample_deployment_data
        return Project.from_dict(sample_project_data, mock_client)

    def test_deploy_with_database_true(self, mock_project):
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            database=True,
            wait=False,
        )

        payload = mock_project._client._http.post.call_args[1]["json"]
        assert payload["metadata"]["database"] is True

    def test_deploy_with_migrations(self, mock_project):
        migrations = ["python manage.py migrate"]

        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            database=True,
            migrations=migrations,
            wait=False,
        )

        payload = mock_project._client._http.post.call_args[1]["json"]
        assert payload["metadata"]["database"] is True
        assert payload["metadata"]["migrations"] == migrations

    def test_deploy_without_database(self, mock_project):
        mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            wait=False,
        )

        payload = mock_project._client._http.post.call_args[1]["json"]
        assert "database" not in payload["metadata"]
        assert "migrations" not in payload["metadata"]

    def test_deploy_with_database_returns_deployment(self, mock_project):
        deployment = mock_project.deploy(
            sandbox_id="sbx-123",
            arti_dir="/app/source",
            database=True,
            wait=False,
        )

        assert isinstance(deployment, Deployment)
        assert deployment.id == "dep_xxx"


class TestEnsureProjectDatabase:
    def test_ensure_project_database(self):
        client = DeploymentClient(api_key="test-key")
        client._http = MagicMock()
        client._http.post.return_value = {
            "databaseInfo": {
                "status": "ACTIVE",
                "provider": "tidb_cloud",
                "databaseName": "app_data",
                "databaseUrl": "mysql+pymysql://user:password@host:4000/app_data",
            }
        }

        database_info = client.ensure_project_database("proj_xxx")

        assert isinstance(database_info, DatabaseInfo)
        assert database_info.status == "ACTIVE"
        assert database_info.database_name == "app_data"
        client._http.post.assert_called_once_with(
            "/projects/proj_xxx/database",
            json={"projectId": "proj_xxx"},
            context="Ensure project database",
        )
