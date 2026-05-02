from __future__ import annotations

import os
import json
from typing import Any, Dict, List, cast

import httpx
import pytest
from respx import MockRouter
from respx.models import Call as RespxCall

from scale_gp_beta import SGPClient
from scale_gp_beta.lib.custom_function import CustomFunction, get_evaluation_columns, _extract_function_source

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


def sample_function(x: float, y: float) -> float:
    return x + y


def function_with_math(x: float) -> float:
    import math

    return math.sqrt(x)


class TestExtractFunctionSource:
    def test_basic_function(self) -> None:
        source = _extract_function_source(sample_function)
        assert "def sample_function" in source
        assert "return x + y" in source

    def test_includes_inline_imports(self) -> None:
        source = _extract_function_source(function_with_math)
        assert "import math" in source
        assert "def function_with_math" in source
        assert "math.sqrt" in source

    def test_lambda_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Cannot use a lambda"):
            _extract_function_source(lambda x: x)  # pyright: ignore[reportUnknownArgumentType, reportUnknownLambdaType]

    def test_builtin_raises_error(self) -> None:
        with pytest.raises(ValueError, match="Cannot extract source code"):
            _extract_function_source(len)


class TestCustomFunctionSerialize:
    def test_serialize_basic(self) -> None:
        cf = CustomFunction(func=sample_function)
        result = cf.serialize()

        assert result["task_type"] == "custom_function"  # pyright: ignore[reportTypedDictNotRequiredAccess]
        assert result["alias"] == "sample_function"  # pyright: ignore[reportTypedDictNotRequiredAccess]
        assert "function_source" in result["configuration"]
        assert "arg_mapping" not in result["configuration"]

    def test_serialize_with_arg_mapping(self) -> None:
        cf = CustomFunction(func=sample_function, arg_mapping={"x": "column_a", "y": "column_b"})
        result = cf.serialize()

        assert result["configuration"]["arg_mapping"] == {"x": "item.column_a", "y": "item.column_b"}  # pyright: ignore[reportTypedDictNotRequiredAccess]

    def test_serialize_with_arg_mapping_passthrough_locator(self) -> None:
        cf = CustomFunction(func=sample_function, arg_mapping={"x": "item.nested.field"})
        result = cf.serialize()

        assert result["configuration"]["arg_mapping"] == {"x": "item.nested.field"}  # pyright: ignore[reportTypedDictNotRequiredAccess]

    def test_serialize_with_arg_mapping_dotted_column_name(self) -> None:
        # column names containing dots should still get the item. prefix
        cf = CustomFunction(func=sample_function, arg_mapping={"x": "metrics.accuracy"})
        result = cf.serialize()

        assert result["configuration"]["arg_mapping"] == {"x": "item.metrics.accuracy"}  # pyright: ignore[reportTypedDictNotRequiredAccess]

    def test_serialize_with_alias(self) -> None:
        cf = CustomFunction(func=sample_function, alias="my_custom_name")
        result = cf.serialize()

        assert result["alias"] == "my_custom_name"  # pyright: ignore[reportTypedDictNotRequiredAccess]

    def test_serialize_includes_inline_imports(self) -> None:
        cf = CustomFunction(func=function_with_math)
        result = cf.serialize()

        source = result["configuration"]["function_source"]
        assert "import math" in source
        assert "def function_with_math" in source


class TestCustomFunctionDryRun:
    @pytest.fixture
    def mock_client(self, respx_mock: MockRouter) -> SGPClient:
        respx_mock.post("/v5/evaluations/tasks/dry-run").mock(
            return_value=httpx.Response(
                200,
                json={
                    "results": [{"output": 3.0}],
                    "status": "success",
                },
            )
        )
        client = SGPClient(base_url=base_url, api_key="test_key", account_id="test_account")
        return client

    def test_dry_run_calls_api(self, mock_client: SGPClient, respx_mock: MockRouter) -> None:
        cf = CustomFunction(func=sample_function)
        sample_data: List[Dict[str, Any]] = [{"x": 1.0, "y": 2.0}]

        result = cf.dry_run(client=mock_client, sample_data=sample_data)

        # Verify the response was returned
        assert result == {"results": [{"output": 3.0}], "status": "success"}

        # Verify the request was made correctly
        call = cast(RespxCall, respx_mock.calls[0])
        request = call.request
        assert request.url.path == "/v5/evaluations/tasks/dry-run"

        body = json.loads(request.content)
        assert body["task_type"] == "custom_function"
        assert body["configuration"]["function_source"] == cf.function_source
        assert body["sample_data"] == sample_data

    def test_dry_run_with_arg_mapping(self, mock_client: SGPClient, respx_mock: MockRouter) -> None:
        mapping = {"x": "col_a", "y": "col_b"}
        cf = CustomFunction(func=sample_function, arg_mapping=mapping)
        sample_data: List[Dict[str, Any]] = [{"col_a": 1.0, "col_b": 2.0}]

        cf.dry_run(client=mock_client, sample_data=sample_data)

        call = cast(RespxCall, respx_mock.calls[0])
        request = call.request
        body = json.loads(request.content)
        assert body["configuration"]["arg_mapping"] == {"x": "item.col_a", "y": "item.col_b"}

    def test_dry_run_omits_arg_mapping_when_none(self, mock_client: SGPClient, respx_mock: MockRouter) -> None:
        cf = CustomFunction(func=sample_function)
        sample_data: List[Dict[str, Any]] = [{"x": 1.0, "y": 2.0}]

        cf.dry_run(client=mock_client, sample_data=sample_data)

        call = cast(RespxCall, respx_mock.calls[0])
        request = call.request
        body = json.loads(request.content)
        assert "arg_mapping" not in body["configuration"]


class TestGetEvaluationColumns:
    @pytest.fixture
    def mock_client(self, respx_mock: MockRouter) -> SGPClient:
        respx_mock.get("/v5/evaluations/eval_123/schema").mock(
            return_value=httpx.Response(
                200,
                json={
                    "evaluation_id": "eval_123",
                    "total_items": 10,
                    "fields": [
                        {"field_name": "ground_truth", "data_type": "number", "item_count": 10, "source": "data"},
                        {"field_name": "model_output", "data_type": "number", "item_count": 10, "source": "data"},
                        {"field_name": "score", "data_type": "number", "item_count": 10, "source": "task_result_cache"},
                    ],
                },
            )
        )
        return SGPClient(base_url=base_url, api_key="test_key", account_id="test_account")

    def test_returns_only_data_fields(self, mock_client: SGPClient) -> None:
        columns = get_evaluation_columns(mock_client, "eval_123")

        assert len(columns) == 2
        assert all(f.source == "data" for f in columns)
        assert [f.field_name for f in columns] == ["ground_truth", "model_output"]
