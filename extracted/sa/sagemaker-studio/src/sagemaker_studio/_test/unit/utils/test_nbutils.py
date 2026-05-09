import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import sagemaker_studio.utils
from sagemaker_studio.utils.nbutils import (
    SMUS_NOTEBOOK_PARAM_PREFIX,
    NotebookParameters,
    _DataZoneNotebookClient,
    _extract_parameters_from_notebook_file,
    _NotebookMetadataReader,
    _parse_parameter_assignments,
    _parse_parameters,
)

MOCK_METADATA_PATH = "test_nb_metadata.json"
MOCK_METADATA_CONTENT = {
    "AppType": "JupyterLab",
    "DomainId": "test-domain-id",
    "NotebookId": "test-notebook-id",
    "NotebookRunId": "test-run-id",
    "AdditionalMetadata": {
        "DataZoneDomainId": "test-domain-id",
        "DataZoneDomainRegion": "us-east-1",
    },
}

MOCK_METADATA_NO_RUN_ID = {
    "DomainId": "test-domain-id",
    "NotebookId": "test-notebook-id",
}


class TestNotebookMetadataReader(unittest.TestCase):
    def setUp(self):
        self.reader = _NotebookMetadataReader()

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_notebook_id(self):
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(MOCK_METADATA_CONTENT, f)
        try:
            self.assertEqual(self.reader.get_notebook_id(), "test-notebook-id")
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_notebook_run_id(self):
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(MOCK_METADATA_CONTENT, f)
        try:
            self.assertEqual(self.reader.get_notebook_run_id(), "test-run-id")
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_notebook_run_id_none_when_missing(self):
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(MOCK_METADATA_NO_RUN_ID, f)
        try:
            self.assertIsNone(self.reader.get_notebook_run_id())
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", "/nonexistent/path.json")
    def test_returns_none_when_no_metadata_file(self):
        self.assertIsNone(self.reader.get_notebook_id())
        self.assertIsNone(self.reader.get_notebook_run_id())
        self.assertIsNone(self.reader.get_domain_id())

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_domain_id(self):
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(MOCK_METADATA_CONTENT, f)
        try:
            self.assertEqual(self.reader.get_domain_id(), "test-domain-id")
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_reads_from_additional_metadata(self):
        metadata = {
            "AdditionalMetadata": {
                "NotebookId": "additional-nb-id",
                "DataZoneDomainId": "additional-domain-id",
            }
        }
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(metadata, f)
        try:
            self.assertEqual(self.reader.get_notebook_id(), "additional-nb-id")
            self.assertEqual(self.reader.get_domain_id(), "additional-domain-id")
        finally:
            os.remove(MOCK_METADATA_PATH)


class TestParseParameters(unittest.TestCase):
    def test_dict_input(self):
        self.assertEqual(_parse_parameters({"a": "1", "b": 2}), {"a": "1", "b": "2"})

    def test_json_string_input(self):
        self.assertEqual(_parse_parameters(json.dumps({"x": "y"})), {"x": "y"})

    def test_invalid_string(self):
        self.assertEqual(_parse_parameters("not json"), {})

    def test_empty(self):
        self.assertEqual(_parse_parameters({}), {})
        self.assertEqual(_parse_parameters(""), {})


class TestParseParameterAssignments(unittest.TestCase):
    def test_simple_assignments(self):
        source = 'my_param = "hello"\nnum = 10\nrate = 0.01'
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"my_param": "hello", "num": "10", "rate": "0.01"})

    def test_single_quoted(self):
        result = _parse_parameter_assignments("name = 'world'")
        self.assertEqual(result, {"name": "world"})

    def test_skips_comments_and_blanks(self):
        source = "# comment\n\nx = 5"
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"x": "5"})

    def test_skips_non_identifier_keys(self):
        source = "123bad = 'nope'\ngood = 'yes'"
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"good": "yes"})

    def test_inline_comment_unquoted(self):
        source = "lr = 0.01  # learning rate"
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"lr": "0.01"})

    def test_inline_comment_quoted(self):
        source = 'name = "hello"  # greeting'
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"name": "hello"})

    def test_inline_comment_single_quoted(self):
        source = "name = 'hello'  # greeting"
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"name": "hello"})

    def test_type_annotated_assignment(self):
        source = "learning_rate: float = 0.01\nepochs: int = 10"
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"learning_rate": "0.01", "epochs": "10"})

    def test_type_annotated_with_inline_comment(self):
        source = "lr: float = 0.01  # learning rate"
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"lr": "0.01"})

    def test_type_annotated_string(self):
        source = 'name: str = "hello"'
        result = _parse_parameter_assignments(source)
        self.assertEqual(result, {"name": "hello"})


class TestExtractParametersFromNotebookFile(unittest.TestCase):
    def _write_notebook(self, cells):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
        nb = {"cells": cells}
        json.dump(nb, f)
        f.close()
        return f.name

    def test_extracts_from_tagged_cell(self):
        path = self._write_notebook(
            [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ["lr = 0.01\n", "epochs = 10"],
                }
            ]
        )
        try:
            result = _extract_parameters_from_notebook_file(path)
            self.assertEqual(result, {"lr": "0.01", "epochs": "10"})
        finally:
            os.remove(path)

    def test_injected_parameters_override_defaults(self):
        path = self._write_notebook(
            [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ["lr = 0.01\n", "epochs = 10"],
                },
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["injected-parameters"]},
                    "source": ["lr = 0.05"],
                },
            ]
        )
        try:
            result = _extract_parameters_from_notebook_file(path)
            self.assertEqual(result, {"lr": "0.05", "epochs": "10"})
        finally:
            os.remove(path)

    def test_returns_empty_when_no_parameters_cell(self):
        path = self._write_notebook([{"cell_type": "code", "metadata": {}, "source": ["x = 1"]}])
        try:
            self.assertEqual(_extract_parameters_from_notebook_file(path), {})
        finally:
            os.remove(path)

    def test_returns_empty_for_nonexistent_file(self):
        self.assertEqual(_extract_parameters_from_notebook_file("/no/such/file.ipynb"), {})

    def test_ignores_non_code_cells(self):
        path = self._write_notebook(
            [
                {
                    "cell_type": "markdown",
                    "metadata": {"tags": ["parameters"]},
                    "source": ["lr = 0.01"],
                }
            ]
        )
        try:
            self.assertEqual(_extract_parameters_from_notebook_file(path), {})
        finally:
            os.remove(path)


class TestNotebookParametersGet(unittest.TestCase):
    def setUp(self):
        self.params = NotebookParameters()
        self._cleanup_env_vars()

    def tearDown(self):
        self._cleanup_env_vars()

    def _cleanup_env_vars(self):
        keys_to_remove = [k for k in os.environ if k.startswith(SMUS_NOTEBOOK_PARAM_PREFIX)]
        for k in keys_to_remove:
            del os.environ[k]

    def test_step1_env_var(self):
        """Step 1: env var found, returns immediately."""
        os.environ[f"{SMUS_NOTEBOOK_PARAM_PREFIX}my_param"] = "env_value"
        result = self.params.get("my_param")
        self.assertEqual(result, "env_value")

    def test_step2_run_id_path(self):
        """Step 2: metadata has notebook ID + run ID, uses run parameters."""
        with patch.object(
            self.params._metadata_reader, "get_domain_id", return_value="d-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value="nb-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value="run-1"
        ), patch.object(
            self.params._dz_client,
            "get_notebook_run_parameters",
            return_value={"p": "run_val"},
        ) as mock_run:
            result = self.params.get("p")
            self.assertEqual(result, "run_val")
            mock_run.assert_called_once_with(domain_id="d-1", run_id="run-1")
            # Verify env var is NOT set (SDK should never set env vars)
            self.assertNotIn(f"{SMUS_NOTEBOOK_PARAM_PREFIX}p", os.environ)

    def test_step3_notebook_id_only(self):
        """Step 3: metadata has notebook ID but no run ID."""
        with patch.object(
            self.params._metadata_reader, "get_domain_id", return_value="d-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value="nb-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value=None
        ), patch.object(
            self.params._dz_client,
            "get_notebook_parameters",
            return_value={"q": "nb_val"},
        ) as mock_nb:
            result = self.params.get("q")
            self.assertEqual(result, "nb_val")
            mock_nb.assert_called_once_with(domain_id="d-1", notebook_id="nb-1")

    def test_step4_parameters_cell_fallback(self):
        """Step 4: no metadata, falls back to parameters cell in .ipynb."""
        nb_file = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ['fallback_param = "from_cell"'],
                }
            ]
        }
        json.dump(nb, nb_file)
        nb_file.close()

        params = NotebookParameters(notebook_path=nb_file.name)
        try:
            with patch.object(
                params._metadata_reader, "get_notebook_id", return_value=None
            ), patch.object(
                params._metadata_reader, "get_domain_id", return_value=None
            ), patch.object(
                params._metadata_reader, "get_notebook_run_id", return_value=None
            ):
                result = params.get("fallback_param")
                self.assertEqual(result, "from_cell")
        finally:
            os.remove(nb_file.name)

    def test_step5_returns_default(self):
        """Step 5: nothing found, returns default."""
        with patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value=None
        ), patch.object(
            self.params._metadata_reader, "get_domain_id", return_value=None
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value=None
        ):
            self.assertIsNone(self.params.get("missing"))
            self.assertEqual(self.params.get("missing", "fallback"), "fallback")

    def test_env_var_takes_precedence_over_api(self):
        os.environ[f"{SMUS_NOTEBOOK_PARAM_PREFIX}x"] = "env_wins"
        with patch.object(
            self.params._dz_client,
            "get_notebook_parameters",
            return_value={"x": "api_loses"},
        ):
            self.assertEqual(self.params.get("x"), "env_wins")


class TestNotebookParametersShow(unittest.TestCase):
    def setUp(self):
        self.params = NotebookParameters()
        self._cleanup_env_vars()

    def tearDown(self):
        self._cleanup_env_vars()

    def _cleanup_env_vars(self):
        keys_to_remove = [k for k in os.environ if k.startswith(SMUS_NOTEBOOK_PARAM_PREFIX)]
        for k in keys_to_remove:
            del os.environ[k]

    def test_show_env_vars_only(self):
        os.environ[f"{SMUS_NOTEBOOK_PARAM_PREFIX}a"] = "1"
        with patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value=None
        ), patch.object(
            self.params._metadata_reader, "get_domain_id", return_value=None
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value=None
        ):
            self.assertEqual(self.params.show(), {"a": "1"})

    def test_show_merges_all_sources(self):
        """env vars > API > cell, with correct precedence."""
        nb_file = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ['cell_only = "c"\nshared = "from_cell"'],
                }
            ]
        }
        json.dump(nb, nb_file)
        nb_file.close()

        os.environ[f"{SMUS_NOTEBOOK_PARAM_PREFIX}shared"] = "from_env"
        params = NotebookParameters(notebook_path=nb_file.name)
        try:
            with patch.object(
                params._metadata_reader, "get_domain_id", return_value="d-1"
            ), patch.object(
                params._metadata_reader, "get_notebook_id", return_value="nb-1"
            ), patch.object(
                params._metadata_reader, "get_notebook_run_id", return_value=None
            ), patch.object(
                params._dz_client,
                "get_notebook_parameters",
                return_value={"api_only": "a", "shared": "from_api"},
            ):
                result = params.show()
                self.assertEqual(result["cell_only"], "c")
                self.assertEqual(result["api_only"], "a")
                # env var wins
                self.assertEqual(result["shared"], "from_env")
        finally:
            os.remove(nb_file.name)

    def test_show_empty(self):
        with patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value=None
        ), patch.object(
            self.params._metadata_reader, "get_domain_id", return_value=None
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value=None
        ):
            self.assertEqual(self.params.show(), {})

    def test_show_uses_run_id_when_available(self):
        with patch.object(
            self.params._metadata_reader, "get_domain_id", return_value="d-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value="nb-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value="run-1"
        ), patch.object(
            self.params._dz_client,
            "get_notebook_run_parameters",
            return_value={"x": "1"},
        ) as mock_run:
            result = self.params.show()
            self.assertEqual(result, {"x": "1"})
            mock_run.assert_called_once()


class TestDataZoneNotebookClientIntegration(unittest.TestCase):
    def setUp(self):
        self.client = _DataZoneNotebookClient()
        self.mock_dz = MagicMock()
        self.client._datazone_api = self.mock_dz

    def test_get_notebook_parameters(self):
        self.mock_dz.get_notebook_wip.return_value = {
            "id": "nb-1",
            "parameters": {"lr": "0.01", "epochs": "10"},
        }
        result = self.client.get_notebook_parameters("d-1", "nb-1")
        self.assertEqual(result, {"lr": "0.01", "epochs": "10"})
        self.mock_dz.get_notebook_wip.assert_called_once_with(
            domainIdentifier="d-1", identifier="nb-1"
        )

    def test_get_notebook_parameters_no_params_key(self):
        self.mock_dz.get_notebook_wip.return_value = {
            "id": "nb-1",
        }
        self.assertEqual(self.client.get_notebook_parameters("d-1", "nb-1"), {})

    def test_get_notebook_parameters_no_metadata(self):
        self.mock_dz.get_notebook_wip.return_value = {"id": "nb-1"}
        self.assertEqual(self.client.get_notebook_parameters("d-1", "nb-1"), {})

    def test_get_notebook_parameters_api_error(self):
        self.mock_dz.get_notebook_wip.side_effect = Exception("API error")
        self.assertEqual(self.client.get_notebook_parameters("d-1", "nb-1"), {})

    def test_get_notebook_run_parameters(self):
        self.mock_dz.get_notebook_run.return_value = {
            "id": "run-1",
            "parameters": {"batch": "32"},
        }
        result = self.client.get_notebook_run_parameters("d-1", "run-1")
        self.assertEqual(result, {"batch": "32"})
        self.mock_dz.get_notebook_run.assert_called_once_with(
            domainIdentifier="d-1", identifier="run-1"
        )

    def test_get_notebook_run_parameters_api_error(self):
        self.mock_dz.get_notebook_run.side_effect = Exception("API error")
        self.assertEqual(self.client.get_notebook_run_parameters("d-1", "run-1"), {})

    def test_ensure_client_failure(self):
        client = _DataZoneNotebookClient()
        with patch(
            "sagemaker_studio.sagemaker_studio_api.SageMakerStudioAPI",
            side_effect=Exception("init failed"),
        ):
            self.assertIsNone(client._ensure_client())

    def test_get_notebook_parameters_client_none(self):
        """When _ensure_client returns None, should return empty dict."""
        client = _DataZoneNotebookClient()
        with patch.object(client, "_ensure_client", return_value=None):
            result = client.get_notebook_parameters("d-1", "nb-1")
            self.assertEqual(result, {})

    def test_get_notebook_run_parameters_client_none(self):
        """When _ensure_client returns None, should return empty dict."""
        client = _DataZoneNotebookClient()
        with patch.object(client, "_ensure_client", return_value=None):
            result = client.get_notebook_run_parameters("d-1", "run-1")
            self.assertEqual(result, {})


class TestNotebookMetadataReaderCorruptFile(unittest.TestCase):
    def test_corrupt_metadata_file_returns_none(self):
        """When metadata file exists but contains invalid JSON, returns None."""
        reader = _NotebookMetadataReader()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("not valid json{{{")
            path = f.name
        try:
            with patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", path):
                self.assertIsNone(reader.get_notebook_id())
        finally:
            os.remove(path)


class TestExtractParametersCorruptNotebook(unittest.TestCase):
    def test_corrupt_notebook_file_returns_empty(self):
        """When notebook file exists but contains invalid JSON, returns empty dict."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False) as f:
            f.write("{bad json")
            path = f.name
        try:
            self.assertEqual(_extract_parameters_from_notebook_file(path), {})
        finally:
            os.remove(path)

    def test_empty_path_returns_empty(self):
        """When notebook_path is empty string, returns empty dict."""
        self.assertEqual(_extract_parameters_from_notebook_file(""), {})


class TestTryParseJson(unittest.TestCase):
    def test_non_string_passthrough(self):
        """Non-string values are returned as-is."""
        params = NotebookParameters()
        self.assertEqual(params._try_parse_json(42), 42)
        self.assertEqual(params._try_parse_json([1, 2]), [1, 2])
        self.assertEqual(params._try_parse_json({"a": 1}), {"a": 1})

    def test_json_string_parsed(self):
        """JSON-encoded strings are parsed into Python objects."""
        params = NotebookParameters()
        self.assertEqual(params._try_parse_json('{"key": "val"}'), {"key": "val"})
        self.assertEqual(params._try_parse_json("[1, 2, 3]"), [1, 2, 3])

    def test_plain_string_returned_as_is(self):
        """Non-JSON strings are returned unchanged."""
        params = NotebookParameters()
        self.assertEqual(params._try_parse_json("hello"), "hello")

    def test_single_quoted_json_parsed(self):
        """JSON wrapped in single quotes from API is parsed."""
        params = NotebookParameters()
        result = params._try_parse_json('\'{"learning_rate": 0.01, "epochs": 10}\'')
        self.assertEqual(result, {"learning_rate": 0.01, "epochs": 10})

    def test_double_quoted_json_parsed(self):
        """JSON wrapped in double quotes from API is parsed."""
        params = NotebookParameters()
        result = params._try_parse_json('"[1, 2, 3]"')
        self.assertEqual(result, [1, 2, 3])

    def test_recursive_dict_deserialization(self):
        """String values inside a dict are recursively deserialized."""
        params = NotebookParameters()
        input_dict = {
            "name": "John Doe",
            "age": "42",
            "is_active": "true",
            "departments": '["Engineering", "Data Science"]',
            "config": '{"epochs": 100}',
            "nothing": "null",
            "s3_uri": "s3://my-bucket/path",
        }
        result = params._try_parse_json(input_dict)
        self.assertEqual(result["name"], "John Doe")
        self.assertEqual(result["age"], 42)
        self.assertIs(result["is_active"], True)
        self.assertEqual(result["departments"], ["Engineering", "Data Science"])
        self.assertEqual(result["config"], {"epochs": 100})
        self.assertIsNone(result["nothing"])
        self.assertEqual(result["s3_uri"], "s3://my-bucket/path")

    def test_recursive_list_deserialization(self):
        """String values inside a list are recursively deserialized."""
        params = NotebookParameters()
        result = params._try_parse_json(["42", "true", "hello", "[1, 2]"])
        self.assertEqual(result, [42, True, "hello", [1, 2]])


class TestGetFallthroughPaths(unittest.TestCase):
    """Cover branch paths where API returns params but the requested key is missing."""

    def setUp(self):
        self.params = NotebookParameters()
        keys_to_remove = [k for k in os.environ if k.startswith(SMUS_NOTEBOOK_PARAM_PREFIX)]
        for k in keys_to_remove:
            del os.environ[k]

    def test_run_id_path_key_missing_falls_to_default(self):
        """Step 2 has params but not the requested key, falls through to default."""
        with patch.object(
            self.params._metadata_reader, "get_domain_id", return_value="d-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value="nb-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value="run-1"
        ), patch.object(
            self.params._dz_client,
            "get_notebook_run_parameters",
            return_value={"other": "val"},
        ):
            self.assertEqual(self.params.get("missing_key", "default"), "default")

    def test_notebook_id_path_key_missing_falls_to_default(self):
        """Step 3 has params but not the requested key, falls through to default."""
        with patch.object(
            self.params._metadata_reader, "get_domain_id", return_value="d-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_id", return_value="nb-1"
        ), patch.object(
            self.params._metadata_reader, "get_notebook_run_id", return_value=None
        ), patch.object(
            self.params._dz_client,
            "get_notebook_parameters",
            return_value={"other": "val"},
        ):
            self.assertEqual(self.params.get("missing_key", "default"), "default")

    def test_get_json_env_var_parsed(self):
        """Env var containing JSON is auto-parsed."""
        os.environ[f"{SMUS_NOTEBOOK_PARAM_PREFIX}config"] = '{"lr": 0.01}'
        try:
            result = self.params.get("config")
            self.assertEqual(result, {"lr": 0.01})
        finally:
            del os.environ[f"{SMUS_NOTEBOOK_PARAM_PREFIX}config"]


class TestNotebookMetadataReaderGetNotebookPath(unittest.TestCase):
    """Tests for _NotebookMetadataReader.get_notebook_path()."""

    def setUp(self):
        self.reader = _NotebookMetadataReader()

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_notebook_path_from_top_level(self):
        metadata = {**MOCK_METADATA_CONTENT, "InputNotebookPath": "/opt/ml/input/notebook.ipynb"}
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(metadata, f)
        try:
            self.assertEqual(self.reader.get_notebook_path(), "/opt/ml/input/notebook.ipynb")
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_notebook_path_from_additional_metadata(self):
        metadata = {
            "AdditionalMetadata": {
                "InputNotebookPath": "/opt/ml/input/nb.ipynb",
            }
        }
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(metadata, f)
        try:
            reader = _NotebookMetadataReader()
            self.assertEqual(reader.get_notebook_path(), "/opt/ml/input/nb.ipynb")
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", MOCK_METADATA_PATH)
    def test_get_notebook_path_returns_none_when_missing(self):
        with open(MOCK_METADATA_PATH, "w") as f:
            json.dump(MOCK_METADATA_CONTENT, f)
        try:
            self.assertIsNone(self.reader.get_notebook_path())
        finally:
            os.remove(MOCK_METADATA_PATH)

    @patch.object(sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", "/nonexistent/path.json")
    def test_get_notebook_path_returns_none_when_no_file(self):
        self.assertIsNone(self.reader.get_notebook_path())


class TestNotebookParametersAutoDetectPath(unittest.TestCase):
    """Tests that NotebookParameters auto-detects notebook_path from metadata."""

    def test_auto_detects_path_from_metadata(self):
        """Singleton-style construction picks up InputNotebookPath from metadata."""
        nb_file = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ['auto_param = "detected"'],
                }
            ]
        }
        json.dump(nb, nb_file)
        nb_file.close()

        metadata = {"InputNotebookPath": nb_file.name}
        metadata_file = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(metadata, metadata_file)
        metadata_file.close()

        try:
            with patch.object(
                sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", metadata_file.name
            ):
                params = NotebookParameters()  # No explicit notebook_path
                self.assertEqual(params._notebook_path, nb_file.name)
                result = params.get("auto_param")
                self.assertEqual(result, "detected")
        finally:
            os.remove(nb_file.name)
            os.remove(metadata_file.name)

    def test_explicit_path_takes_precedence_over_metadata(self):
        """Explicitly provided notebook_path is used even if metadata has one."""
        explicit_nb = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ['source = "explicit"'],
                }
            ]
        }
        json.dump(nb, explicit_nb)
        explicit_nb.close()

        metadata = {"InputNotebookPath": "/some/other/notebook.ipynb"}
        metadata_file = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(metadata, metadata_file)
        metadata_file.close()

        try:
            with patch.object(
                sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", metadata_file.name
            ):
                params = NotebookParameters(notebook_path=explicit_nb.name)
                self.assertEqual(params._notebook_path, explicit_nb.name)
                result = params.get("source")
                self.assertEqual(result, "explicit")
        finally:
            os.remove(explicit_nb.name)
            os.remove(metadata_file.name)

    def test_no_metadata_file_leaves_path_none(self):
        """Without metadata file, notebook_path stays None (graceful degradation)."""
        with patch.object(
            sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", "/nonexistent/path.json"
        ):
            params = NotebookParameters()
            self.assertIsNone(params._notebook_path)

    def test_show_uses_auto_detected_path(self):
        """show() includes parameters from auto-detected notebook file."""
        nb_file = tempfile.NamedTemporaryFile(mode="w", suffix=".ipynb", delete=False)
        nb = {
            "cells": [
                {
                    "cell_type": "code",
                    "metadata": {"tags": ["parameters"]},
                    "source": ['x = "from_cell"\ny = "also_cell"'],
                }
            ]
        }
        json.dump(nb, nb_file)
        nb_file.close()

        metadata = {"InputNotebookPath": nb_file.name}
        metadata_file = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(metadata, metadata_file)
        metadata_file.close()

        try:
            with patch.object(
                sagemaker_studio.utils, "SAGEMAKER_METADATA_JSON_PATH", metadata_file.name
            ):
                params = NotebookParameters()
                with patch.object(
                    params._metadata_reader, "get_notebook_id", return_value=None
                ), patch.object(
                    params._metadata_reader, "get_domain_id", return_value=None
                ), patch.object(
                    params._metadata_reader, "get_notebook_run_id", return_value=None
                ):
                    result = params.show()
                    self.assertEqual(result["x"], "from_cell")
                    self.assertEqual(result["y"], "also_cell")
        finally:
            os.remove(nb_file.name)
            os.remove(metadata_file.name)


if __name__ == "__main__":
    unittest.main()
