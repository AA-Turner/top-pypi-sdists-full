"""Tests for dataset tools."""

from datetime import datetime
from unittest.mock import Mock

import pytest

from langsmith_mcp_server.services.tools.datasets import (
    _parse_as_of_parameter,
    list_datasets_tool,
    list_examples_tool,
    read_dataset_tool,
    read_example_tool,
)


class MockDataset:
    """Mock dataset object to simulate LangSmith dataset responses."""

    def __init__(
        self,
        id: str,
        name: str,
        description: str = None,
        data_type: str = "kv",
        created_at: datetime = None,
        modified_at: datetime = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.data_type = data_type
        self.created_at = created_at or datetime(2024, 1, 1, 12, 0, 0)
        self.modified_at = modified_at or datetime(2024, 1, 2, 12, 0, 0)


class MockExample:
    """Mock example object to simulate LangSmith example responses."""

    def __init__(
        self,
        id: str,
        dataset_id: str,
        inputs: dict = None,
        outputs: dict = None,
        metadata: dict = None,
        created_at: datetime = None,
        modified_at: datetime = None,
        runs: list = None,
        source_run_id: str = None,
        attachments: dict = None,
    ):
        self.id = id
        self.dataset_id = dataset_id
        self.inputs = inputs or {"question": "What is 2+2?"}
        self.outputs = outputs or {"answer": "4"}
        self.metadata = metadata or {}
        self.created_at = created_at or datetime(2024, 1, 1, 12, 0, 0)
        self.modified_at = modified_at or datetime(2024, 1, 2, 12, 0, 0)
        self.runs = runs or []
        self.source_run_id = source_run_id
        self.attachments = attachments or {}


@pytest.fixture
def mock_client():
    """Create a mock LangSmith client."""
    client = Mock()
    return client


@pytest.fixture
def sample_datasets():
    """Create sample dataset objects for testing."""
    return [
        MockDataset(
            id="dataset-1",
            name="Test Dataset 1",
            description="First test dataset",
            data_type="kv",
        ),
        MockDataset(
            id="dataset-2",
            name="Chat Dataset",
            description="Dataset for chat conversations",
            data_type="chat",
        ),
        MockDataset(
            id="dataset-3",
            name="Empty Dataset",
            description=None,
            data_type="kv",
        ),
    ]


@pytest.fixture
def sample_examples():
    """Create sample example objects for testing."""
    return [
        MockExample(
            id="example-1",
            dataset_id="dataset-1",
            inputs={"question": "What is 2+2?"},
            outputs={"answer": "4"},
            metadata={"difficulty": "easy"},
            source_run_id="run-123",
        ),
        MockExample(
            id="example-2",
            dataset_id="dataset-1",
            inputs={"question": "What is the capital of France?"},
            outputs={"answer": "Paris"},
            metadata={"difficulty": "medium", "topic": "geography"},
            source_run_id="run-456",
        ),
        MockExample(
            id="example-3",
            dataset_id="dataset-2",
            inputs={"prompt": "Explain quantum physics"},
            outputs={"explanation": "Quantum physics is..."},
            metadata={"difficulty": "hard", "topic": "science"},
        ),
    ]


class TestListDatasetsTool:
    """Test cases for list_datasets_tool function."""

    def test_list_datasets_success_no_filters(self, mock_client, sample_datasets):
        """Test successful dataset listing without filters."""
        mock_client.list_datasets.return_value = iter(sample_datasets)

        result = list_datasets_tool(mock_client)

        assert "datasets" in result
        assert "total_count" in result
        assert result["total_count"] == 3
        assert len(result["datasets"]) == 3

        # Check first dataset structure
        first_dataset = result["datasets"][0]
        expected_attrs = [
            "id",
            "name",
            "description",
            "data_type",
            "created_at",
            "modified_at",
        ]
        for attr in expected_attrs:
            assert attr in first_dataset

        # Verify data
        assert first_dataset["id"] == "dataset-1"
        assert first_dataset["name"] == "Test Dataset 1"
        assert first_dataset["data_type"] == "kv"
        assert first_dataset["created_at"] == "2024-01-01T12:00:00"
        assert first_dataset["modified_at"] == "2024-01-02T12:00:00"

        # Verify client was called with no filters
        mock_client.list_datasets.assert_called_once_with(limit=20)

    def test_list_datasets_with_dataset_ids_filter(self, mock_client, sample_datasets):
        """Test dataset listing with dataset_ids filter."""
        filtered_datasets = [sample_datasets[0]]
        mock_client.list_datasets.return_value = iter(filtered_datasets)

        dataset_ids = ["dataset-1"]
        result = list_datasets_tool(mock_client, dataset_ids=dataset_ids)

        assert result["total_count"] == 1
        assert result["datasets"][0]["id"] == "dataset-1"

        mock_client.list_datasets.assert_called_once_with(dataset_ids=dataset_ids, limit=20)

    def test_list_datasets_with_data_type_filter(self, mock_client, sample_datasets):
        """Test dataset listing with data_type filter."""
        chat_datasets = [sample_datasets[1]]  # Only the chat dataset
        mock_client.list_datasets.return_value = iter(chat_datasets)

        result = list_datasets_tool(mock_client, data_type="chat")

        assert result["total_count"] == 1
        assert result["datasets"][0]["data_type"] == "chat"

        mock_client.list_datasets.assert_called_once_with(data_type="chat", limit=20)

    def test_list_datasets_with_name_filter(self, mock_client, sample_datasets):
        """Test dataset listing with dataset_name filter."""
        filtered_datasets = [sample_datasets[0]]
        mock_client.list_datasets.return_value = iter(filtered_datasets)

        result = list_datasets_tool(mock_client, dataset_name="Test Dataset 1")

        assert result["total_count"] == 1
        assert result["datasets"][0]["name"] == "Test Dataset 1"

        mock_client.list_datasets.assert_called_once_with(dataset_name="Test Dataset 1", limit=20)

    def test_list_datasets_with_name_contains_filter(self, mock_client, sample_datasets):
        """Test dataset listing with dataset_name_contains filter."""
        filtered_datasets = [sample_datasets[1]]
        mock_client.list_datasets.return_value = iter(filtered_datasets)

        result = list_datasets_tool(mock_client, dataset_name_contains="Chat")

        assert result["total_count"] == 1
        assert result["datasets"][0]["name"] == "Chat Dataset"

        mock_client.list_datasets.assert_called_once_with(dataset_name_contains="Chat", limit=20)

    def test_list_datasets_with_metadata_filter(self, mock_client, sample_datasets):
        """Test dataset listing with metadata filter."""
        filtered_datasets = [sample_datasets[0]]
        mock_client.list_datasets.return_value = iter(filtered_datasets)

        metadata_filter = {"version": "1.0"}
        result = list_datasets_tool(mock_client, metadata=metadata_filter)

        assert result["total_count"] == 1
        # Note: metadata is not returned in the output, it's only used for filtering
        assert result["datasets"][0]["id"] == "dataset-1"

        mock_client.list_datasets.assert_called_once_with(metadata=metadata_filter, limit=20)

    def test_list_datasets_with_custom_limit(self, mock_client, sample_datasets):
        """Test dataset listing with custom limit."""
        mock_client.list_datasets.return_value = iter(sample_datasets[:2])

        result = list_datasets_tool(mock_client, limit=2)

        assert result["total_count"] == 2

        mock_client.list_datasets.assert_called_once_with(limit=2)

    def test_list_datasets_with_all_filters(self, mock_client, sample_datasets):
        """Test dataset listing with all filters applied."""
        filtered_datasets = [sample_datasets[0]]
        mock_client.list_datasets.return_value = iter(filtered_datasets)

        result = list_datasets_tool(
            mock_client,
            dataset_ids=["dataset-1"],
            data_type="kv",
            dataset_name="Test Dataset 1",
            dataset_name_contains="Test",
            metadata={"version": "1.0"},
            limit=10,
        )

        assert result["total_count"] == 1

        mock_client.list_datasets.assert_called_once_with(
            dataset_ids=["dataset-1"],
            data_type="kv",
            dataset_name="Test Dataset 1",
            dataset_name_contains="Test",
            metadata={"version": "1.0"},
            limit=10,
        )

    def test_list_datasets_empty_result(self, mock_client):
        """Test dataset listing when no datasets are found."""
        mock_client.list_datasets.return_value = iter([])

        result = list_datasets_tool(mock_client)

        assert result["total_count"] == 0
        assert result["datasets"] == []

    def test_list_datasets_with_none_values(self, mock_client, sample_datasets):
        """Test that None values are properly handled and not passed to client."""
        mock_client.list_datasets.return_value = iter(sample_datasets)

        result = list_datasets_tool(
            mock_client,
            dataset_ids=None,
            data_type=None,
            dataset_name=None,
            dataset_name_contains=None,
            metadata=None,
            limit=None,
        )

        assert result["total_count"] == 3

        # Should not pass any parameters since all are None (including limit)
        mock_client.list_datasets.assert_called_once_with()

    def test_list_datasets_handles_missing_attributes(self, mock_client):
        """Test handling of datasets with missing attributes."""
        # Create a mock dataset with missing attributes
        incomplete_dataset = Mock()
        incomplete_dataset.id = "incomplete-1"
        incomplete_dataset.name = "Incomplete Dataset"
        # Configure missing attributes to return None when accessed via getattr
        incomplete_dataset.configure_mock(
            **{
                "description": None,
                "data_type": None,
                "created_at": None,
                "modified_at": None,
            }
        )

        mock_client.list_datasets.return_value = iter([incomplete_dataset])

        result = list_datasets_tool(mock_client)

        assert result["total_count"] == 1
        dataset = result["datasets"][0]
        assert dataset["id"] == "incomplete-1"
        assert dataset["name"] == "Incomplete Dataset"
        # Missing attributes should be None
        assert dataset["description"] is None
        assert dataset["data_type"] is None

    def test_list_datasets_client_exception(self, mock_client):
        """Test error handling when client raises an exception."""
        mock_client.list_datasets.side_effect = Exception("API Error")

        result = list_datasets_tool(mock_client)

        assert "error" in result
        assert "Error fetching datasets: API Error" in result["error"]


class TestListExamplesTool:
    """Test cases for list_examples_tool function."""

    def test_list_examples_success_with_dataset_id(self, mock_client, sample_examples):
        """Test successful examples listing with dataset_id."""
        mock_client.list_examples.return_value = iter(sample_examples[:2])

        result = list_examples_tool(mock_client, dataset_id="dataset-1")

        assert "examples" in result
        assert "total_count" in result
        assert result["total_count"] == 2
        assert len(result["examples"]) == 2

        # Check first example structure
        first_example = result["examples"][0]
        expected_attrs = [
            "id",
            "dataset_id",
            "inputs",
            "outputs",
            "metadata",
            "created_at",
            "modified_at",
            "runs",
            "source_run_id",
            "attachments",
        ]
        for attr in expected_attrs:
            assert attr in first_example

        # Verify data and serialization
        assert first_example["id"] == "example-1"
        assert first_example["dataset_id"] == "dataset-1"
        assert first_example["inputs"] == {"question": "What is 2+2?"}
        assert first_example["outputs"] == {"answer": "4"}
        assert first_example["metadata"] == {"difficulty": "easy"}
        assert first_example["created_at"] == "2024-01-01T12:00:00"
        assert first_example["modified_at"] == "2024-01-02T12:00:00"
        assert first_example["source_run_id"] == "run-123"

        mock_client.list_examples.assert_called_once_with(dataset_id="dataset-1")

    def test_list_examples_success_with_dataset_name(self, mock_client, sample_examples):
        """Test successful examples listing with dataset_name."""
        mock_client.list_examples.return_value = iter(sample_examples[:1])

        result = list_examples_tool(mock_client, dataset_name="my-dataset")

        assert result["total_count"] == 1
        assert result["examples"][0]["id"] == "example-1"

        mock_client.list_examples.assert_called_once_with(dataset_name="my-dataset")

    def test_list_examples_with_example_ids(self, mock_client, sample_examples):
        """Test examples listing with specific example_ids."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        example_ids = ["example-1"]
        result = list_examples_tool(mock_client, example_ids=example_ids)

        assert result["total_count"] == 1
        assert result["examples"][0]["id"] == "example-1"

        mock_client.list_examples.assert_called_once_with(example_ids=example_ids)

    def test_list_examples_with_pagination(self, mock_client, sample_examples):
        """Test examples listing with limit and offset."""
        mock_client.list_examples.return_value = iter(sample_examples[:2])

        result = list_examples_tool(mock_client, dataset_id="dataset-1", limit=2, offset=5)

        assert result["total_count"] == 2

        mock_client.list_examples.assert_called_once_with(dataset_id="dataset-1", limit=2, offset=5)

    def test_list_examples_with_filter(self, mock_client, sample_examples):
        """Test examples listing with filter string."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        filter_str = 'has(metadata, {"difficulty": "easy"})'
        result = list_examples_tool(mock_client, dataset_id="dataset-1", filter=filter_str)

        assert result["total_count"] == 1

        mock_client.list_examples.assert_called_once_with(dataset_id="dataset-1", filter=filter_str)

    def test_list_examples_with_metadata_filter(self, mock_client, sample_examples):
        """Test examples listing with metadata filter."""
        mock_client.list_examples.return_value = iter([sample_examples[1]])

        metadata_filter = {"topic": "geography"}
        result = list_examples_tool(mock_client, dataset_id="dataset-1", metadata=metadata_filter)

        assert result["total_count"] == 1

        mock_client.list_examples.assert_called_once_with(
            dataset_id="dataset-1", metadata=metadata_filter
        )

    def test_list_examples_with_splits(self, mock_client, sample_examples):
        """Test examples listing with splits filter."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        splits = ["train", "test"]
        result = list_examples_tool(mock_client, dataset_id="dataset-1", splits=splits)

        assert result["total_count"] == 1

        mock_client.list_examples.assert_called_once_with(dataset_id="dataset-1", splits=splits)

    def test_list_examples_with_attachment_options(self, mock_client, sample_examples):
        """Test examples listing with attachment and S3 URL options."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        result = list_examples_tool(
            mock_client,
            dataset_id="dataset-1",
            inline_s3_urls=False,
            include_attachments=True,
        )

        assert result["total_count"] == 1

        mock_client.list_examples.assert_called_once_with(
            dataset_id="dataset-1", inline_s3_urls=False, include_attachments=True
        )

    def test_list_examples_with_as_of_timestamp(self, mock_client, sample_examples):
        """Test examples listing with as_of timestamp (should convert to datetime)."""
        from datetime import datetime

        mock_client.list_examples.return_value = iter([sample_examples[0]])

        as_of_str = "2024-01-15T10:00:00Z"
        result = list_examples_tool(mock_client, dataset_id="dataset-1", as_of=as_of_str)

        assert result["total_count"] == 1

        # Verify that the timestamp was converted to datetime
        call_args = mock_client.list_examples.call_args[1]
        assert "as_of" in call_args
        assert isinstance(call_args["as_of"], datetime)
        assert call_args["as_of"].isoformat() == "2024-01-15T10:00:00+00:00"

    def test_list_examples_with_as_of_version_tag(self, mock_client, sample_examples):
        """Test examples listing with as_of version tag (should remain string)."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        as_of_tag = "v1.0"
        result = list_examples_tool(mock_client, dataset_id="dataset-1", as_of=as_of_tag)

        assert result["total_count"] == 1

        # Verify that the version tag remained as string
        call_args = mock_client.list_examples.call_args[1]
        assert "as_of" in call_args
        assert call_args["as_of"] == "v1.0"

    def test_list_examples_with_all_parameters(self, mock_client, sample_examples):
        """Test examples listing with all parameters."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        result = list_examples_tool(
            mock_client,
            dataset_id="dataset-1",
            dataset_name="my-dataset",
            example_ids=["example-1"],
            limit=10,
            offset=0,
            filter='has(metadata, {"difficulty": "easy"})',
            metadata={"topic": "math"},
            splits=["train"],
            inline_s3_urls=True,
            include_attachments=False,
            as_of="v1.0",
        )

        assert result["total_count"] == 1

        mock_client.list_examples.assert_called_once_with(
            dataset_id="dataset-1",
            dataset_name="my-dataset",
            example_ids=["example-1"],
            limit=10,
            offset=0,
            filter='has(metadata, {"difficulty": "easy"})',
            metadata={"topic": "math"},
            splits=["train"],
            inline_s3_urls=True,
            include_attachments=False,
            as_of="v1.0",
        )

    def test_list_examples_empty_result(self, mock_client):
        """Test examples listing when no examples are found."""
        mock_client.list_examples.return_value = iter([])

        result = list_examples_tool(mock_client, dataset_id="dataset-1")

        assert result["total_count"] == 0
        assert result["examples"] == []

    def test_list_examples_with_none_values(self, mock_client, sample_examples):
        """Test that None values are properly handled and not passed to client."""
        mock_client.list_examples.return_value = iter(sample_examples)

        result = list_examples_tool(
            mock_client,
            dataset_id=None,
            dataset_name=None,
            example_ids=None,
            limit=None,
            offset=None,
            filter=None,
            metadata=None,
            splits=None,
            inline_s3_urls=None,
            include_attachments=None,
            as_of=None,
        )

        assert result["total_count"] == 3

        # Should not pass any parameters since all are None
        mock_client.list_examples.assert_called_once_with()

    def test_list_examples_handles_missing_attributes(self, mock_client):
        """Test handling of examples with missing attributes."""
        # Create a mock example with missing attributes
        incomplete_example = Mock()
        incomplete_example.id = "incomplete-1"
        incomplete_example.dataset_id = "dataset-1"
        incomplete_example.inputs = {"question": "Test?"}
        # Configure missing attributes to return None
        incomplete_example.configure_mock(
            **{
                "outputs": None,
                "metadata": None,
                "created_at": None,
                "modified_at": None,
                "runs": None,
                "source_run_id": None,
                "attachments": None,
            }
        )

        mock_client.list_examples.return_value = iter([incomplete_example])

        result = list_examples_tool(mock_client, dataset_id="dataset-1")

        assert result["total_count"] == 1
        example = result["examples"][0]
        assert example["id"] == "incomplete-1"
        assert example["dataset_id"] == "dataset-1"
        assert example["inputs"] == {"question": "Test?"}
        # Missing attributes should be None
        assert example["outputs"] is None
        assert example["metadata"] is None

    def test_list_examples_client_exception(self, mock_client):
        """Test error handling when client raises an exception."""
        mock_client.list_examples.side_effect = Exception("API Error")

        result = list_examples_tool(mock_client, dataset_id="dataset-1")

        assert "error" in result
        assert "Error fetching examples: API Error" in result["error"]

    def test_list_examples_as_of_invalid_datetime_fallback(self, mock_client, sample_examples):
        """Test that invalid datetime strings fall back to being treated as version tags."""
        mock_client.list_examples.return_value = iter([sample_examples[0]])

        # This looks like a timestamp but is invalid
        invalid_timestamp = "2024-13-45T25:99:99Z"
        result = list_examples_tool(mock_client, dataset_id="dataset-1", as_of=invalid_timestamp)

        assert result["total_count"] == 1

        # Should pass the invalid timestamp as a string (version tag)
        call_args = mock_client.list_examples.call_args[1]
        assert call_args["as_of"] == invalid_timestamp


class TestReadDatasetTool:
    """Test cases for read_dataset_tool function."""

    def test_read_dataset_success_with_id(self, mock_client, sample_datasets):
        """Test successful dataset reading with dataset_id."""
        mock_client.read_dataset.return_value = sample_datasets[0]

        result = read_dataset_tool(mock_client, dataset_id="dataset-1")

        assert "dataset" in result
        assert "error" not in result

        dataset = result["dataset"]
        assert dataset["id"] == "dataset-1"
        assert dataset["name"] == "Test Dataset 1"
        assert dataset["data_type"] == "kv"
        assert dataset["created_at"] == "2024-01-01T12:00:00"

        mock_client.read_dataset.assert_called_once_with(dataset_id="dataset-1")

    def test_read_dataset_success_with_name(self, mock_client, sample_datasets):
        """Test successful dataset reading with dataset_name."""
        mock_client.read_dataset.return_value = sample_datasets[1]

        result = read_dataset_tool(mock_client, dataset_name="Chat Dataset")

        assert "dataset" in result
        dataset = result["dataset"]
        assert dataset["name"] == "Chat Dataset"
        assert dataset["data_type"] == "chat"

        mock_client.read_dataset.assert_called_once_with(dataset_name="Chat Dataset")

    def test_read_dataset_with_both_params(self, mock_client, sample_datasets):
        """Test dataset reading with both dataset_id and dataset_name."""
        mock_client.read_dataset.return_value = sample_datasets[0]

        result = read_dataset_tool(
            mock_client, dataset_id="dataset-1", dataset_name="Test Dataset 1"
        )

        assert "dataset" in result
        # Both parameters should be passed to client
        mock_client.read_dataset.assert_called_once_with(
            dataset_id="dataset-1", dataset_name="Test Dataset 1"
        )

    def test_read_dataset_client_exception(self, mock_client):
        """Test error handling when client raises an exception."""
        mock_client.read_dataset.side_effect = Exception("Dataset not found")

        result = read_dataset_tool(mock_client, dataset_id="nonexistent")

        assert "error" in result
        assert "Error reading dataset: Dataset not found" in result["error"]

    def test_read_dataset_with_none_values(self, mock_client, sample_datasets):
        """Test that None values are properly handled."""
        mock_client.read_dataset.return_value = sample_datasets[0]

        result = read_dataset_tool(mock_client, dataset_id=None, dataset_name=None)

        assert "dataset" in result
        # Should not pass any parameters since all are None
        mock_client.read_dataset.assert_called_once_with()


class TestReadExampleTool:
    """Test cases for read_example_tool function."""

    def test_read_example_success(self, mock_client, sample_examples):
        """Test successful example reading."""
        mock_client.read_example.return_value = sample_examples[0]

        result = read_example_tool(mock_client, example_id="example-1")

        assert "example" in result
        assert "error" not in result

        example = result["example"]
        assert example["id"] == "example-1"
        assert example["dataset_id"] == "dataset-1"
        assert example["inputs"] == {"question": "What is 2+2?"}
        assert example["outputs"] == {"answer": "4"}
        assert example["created_at"] == "2024-01-01T12:00:00"
        assert example["source_run_id"] == "run-123"

        mock_client.read_example.assert_called_once_with(example_id="example-1")

    def test_read_example_with_as_of_timestamp(self, mock_client, sample_examples):
        """Test example reading with as_of timestamp (should convert to datetime)."""
        from datetime import datetime

        mock_client.read_example.return_value = sample_examples[0]

        as_of_str = "2024-01-15T10:00:00Z"
        result = read_example_tool(mock_client, example_id="example-1", as_of=as_of_str)

        assert "example" in result

        # Verify that the timestamp was converted to datetime
        call_args = mock_client.read_example.call_args[1]
        assert "as_of" in call_args
        assert isinstance(call_args["as_of"], datetime)
        assert call_args["as_of"].isoformat() == "2024-01-15T10:00:00+00:00"

    def test_read_example_with_as_of_version_tag(self, mock_client, sample_examples):
        """Test example reading with as_of version tag (should remain string)."""
        mock_client.read_example.return_value = sample_examples[0]

        as_of_tag = "v1.0"
        result = read_example_tool(mock_client, example_id="example-1", as_of=as_of_tag)

        assert "example" in result

        # Verify that the version tag remained as string
        call_args = mock_client.read_example.call_args[1]
        assert "as_of" in call_args
        assert call_args["as_of"] == "v1.0"

    def test_read_example_client_exception(self, mock_client):
        """Test error handling when client raises an exception."""
        mock_client.read_example.side_effect = Exception("Example not found")

        result = read_example_tool(mock_client, example_id="nonexistent")

        assert "error" in result
        assert "Error reading example: Example not found" in result["error"]

    def test_read_example_handles_missing_attributes(self, mock_client):
        """Test handling of examples with missing attributes."""
        # Create a mock example with missing attributes
        incomplete_example = Mock()
        incomplete_example.id = "incomplete-1"
        incomplete_example.dataset_id = "dataset-1"
        incomplete_example.inputs = {"question": "Test?"}
        incomplete_example.configure_mock(
            **{
                "outputs": None,
                "metadata": None,
                "created_at": None,
                "modified_at": None,
                "runs": None,
                "source_run_id": None,
                "attachments": None,
            }
        )

        mock_client.read_example.return_value = incomplete_example

        result = read_example_tool(mock_client, example_id="incomplete-1")

        assert "example" in result
        example = result["example"]
        assert example["id"] == "incomplete-1"
        assert example["dataset_id"] == "dataset-1"
        assert example["inputs"] == {"question": "Test?"}
        # Missing attributes should be None
        assert example["outputs"] is None
        assert example["metadata"] is None

    def test_read_example_as_of_invalid_datetime_fallback(self, mock_client, sample_examples):
        """Test that invalid datetime strings fall back to being treated as version tags."""
        mock_client.read_example.return_value = sample_examples[0]

        # This looks like a timestamp but is invalid
        invalid_timestamp = "2024-13-45T25:99:99Z"
        result = read_example_tool(mock_client, example_id="example-1", as_of=invalid_timestamp)

        assert "example" in result

        # Should pass the invalid timestamp as a string (version tag)
        call_args = mock_client.read_example.call_args[1]
        assert call_args["as_of"] == invalid_timestamp


class TestParseAsOfParameter:
    """Test cases for _parse_as_of_parameter helper function."""

    def test_parse_iso_timestamp_with_z(self):
        """Test parsing ISO timestamp with Z suffix."""
        from datetime import datetime

        result = _parse_as_of_parameter("2024-01-15T10:00:00Z")

        assert isinstance(result, datetime)
        assert result.isoformat() == "2024-01-15T10:00:00+00:00"

    def test_parse_iso_timestamp_with_offset(self):
        """Test parsing ISO timestamp with timezone offset."""
        from datetime import datetime

        result = _parse_as_of_parameter("2024-01-15T10:00:00+05:00")

        assert isinstance(result, datetime)
        assert result.isoformat() == "2024-01-15T10:00:00+05:00"

    def test_parse_iso_timestamp_without_timezone(self):
        """Test parsing ISO timestamp without timezone."""
        from datetime import datetime

        result = _parse_as_of_parameter("2024-01-15T10:00:00")

        assert isinstance(result, datetime)
        assert result.isoformat() == "2024-01-15T10:00:00"

    def test_parse_version_tag(self):
        """Test that version tags are returned as strings."""
        version_tags = ["v1.0", "production", "latest", "baseline"]

        for tag in version_tags:
            result = _parse_as_of_parameter(tag)
            assert isinstance(result, str)
            assert result == tag

    def test_parse_invalid_timestamp_fallback(self):
        """Test that invalid timestamps fall back to string."""
        invalid_timestamps = [
            "2024-13-45T25:99:99Z",  # Invalid date/time values
            "not-a-timestamp",  # Not a timestamp at all
            "invalid-date-format",  # Invalid format
        ]

        for invalid in invalid_timestamps:
            result = _parse_as_of_parameter(invalid)
            assert isinstance(result, str)
            assert result == invalid

    def test_parse_date_only_valid(self):
        """Test that date-only strings are parsed as datetime."""
        from datetime import datetime

        result = _parse_as_of_parameter("2024-01-15")

        assert isinstance(result, datetime)
        assert result.date().isoformat() == "2024-01-15"

    def test_parse_empty_string(self):
        """Test parsing empty string."""
        result = _parse_as_of_parameter("")

        assert isinstance(result, str)
        assert result == ""
