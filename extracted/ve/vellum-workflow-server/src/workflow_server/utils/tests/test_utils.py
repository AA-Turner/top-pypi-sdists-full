import pytest

from vellum import (
    ChatMessage,
    FunctionCall,
    SearchResult,
    SearchResultDocument,
    StringVellumValue,
    VellumAudio,
    VellumError,
    VellumImage,
)
from workflow_server.utils.utils import (
    convert_json_inputs_to_vellum,
    to_python_safe_snake_case,
    to_valid_python_identifier,
)


@pytest.mark.parametrize(
    ["input", "expected"],
    [
        ({"type": "STRING", "name": "test", "value": "<example-string-value>"}, {"test": "<example-string-value>"}),
        ({"type": "NUMBER", "name": "test2", "value": 5}, {"test2": 5}),
        (
            {"type": "JSON", "name": "test3", "value": {"example-key": "example-value"}},
            {"test3": {"example-key": "example-value"}},
        ),
        (
            {
                "type": "CHAT_HISTORY",
                "name": "chat_history",
                "value": [{"role": "USER", "text": "<example-user-text>"}],
            },
            {"chat_history": [ChatMessage(text="<example-user-text>", role="USER")]},
        ),
        (
            {
                "type": "FUNCTION_CALL",
                "name": "function_call",
                "value": {"name": "example-function-name", "arguments": {"foo": "bar"}},
            },
            {"function_call": FunctionCall(name="example-function-name", arguments={"foo": "bar"})},
        ),
        (
            {"type": "IMAGE", "name": "image", "value": {"src": "https://example.com/image.png"}},
            {"image": VellumImage(src="https://example.com/image.png")},
        ),
        (
            {"type": "AUDIO", "name": "audio", "value": {"src": "https://example.com/audio.mp3"}},
            {"audio": VellumAudio(src="https://example.com/audio.mp3")},
        ),
        (
            {
                "type": "SEARCH_RESULTS",
                "name": "search_results",
                "value": [
                    {
                        "text": "example-search-result",
                        "score": 0.99,
                        "keywords": ["foo", "bar"],
                        "document": {
                            "id": "example-document-id",
                            "label": "example-document-label",
                            "external_id": "example-external-id",
                            "metadata": {"foo": "bar"},
                        },
                    }
                ],
            },
            {
                "search_results": [
                    SearchResult(
                        text="example-search-result",
                        score=0.99,
                        keywords=["foo", "bar"],
                        document=SearchResultDocument(
                            id="example-document-id",
                            label="example-document-label",
                            external_id="example-external-id",
                            metadata={"foo": "bar"},
                        ),
                    )
                ]
            },
        ),
        (
            {
                "type": "ERROR",
                "name": "error",
                "value": {"message": "example-error-message", "code": "USER_DEFINED_ERROR"},
            },
            {"error": VellumError(message="example-error-message", code="USER_DEFINED_ERROR")},
        ),
        (
            {"type": "ARRAY", "name": "array", "value": [{"type": "STRING", "value": "<example-string-value>"}]},
            {"array": [StringVellumValue(value="<example-string-value>")]},
        ),
        (
            {"type": "NUMBER", "name": "123", "value": 123},
            {"input_123": 123},
        ),
        (
            {"type": "STRING", "name": "_a", "value": "example-string-value"},
            {"input_a": "example-string-value"},
        ),
        (
            {"type": "NUMBER", "name": "_123", "value": 123},
            {"input_123": 123},
        ),
    ],
    ids=[
        "string",
        "number",
        "json",
        "chat_history",
        "function_call",
        "image",
        "audio",
        "search_results",
        "error",
        "array",
        "number_prefixed_input",
        "underscore_prefixed_alpha_input",
        "underscore_prefixed_number_input",
    ],
)
def test_convert_json_inputs_to_vellum__happy_path(input, expected):
    actual = convert_json_inputs_to_vellum([input])

    assert expected == actual


def test_input_variables_with_uppercase_gets_sanitized():
    inputs = [
        {"type": "STRING", "name": "Foo", "value": "<example-string-value>"},
        {"type": "STRING", "name": "Foo-Var", "value": "<another-example-string-value>"},
    ]

    expected = {
        "Foo": "<example-string-value>",
        "foo_var": "<another-example-string-value>",
    }

    actual = convert_json_inputs_to_vellum(inputs)

    assert expected == actual


@pytest.mark.parametrize(
    ["input_string", "safety_prefix", "expected"],
    [
        ("Foo", "input", "Foo"),
        ("test", "input", "test"),
        ("myVariable", "input", "myVariable"),
        ("validName123", "input", "validName123"),
        ("Foo-Var", "input", "foo_var"),
        ("My Variable", "input", "my_variable"),
        ("test-case", "input", "test_case"),
        ("CamelCase", "input", "CamelCase"),
        ("123", "input", "input_123"),
        ("_a", "input", "input_a"),
        ("_123", "input", "input_123"),
        ("test@#$", "input", "test"),
        ("@#$test", "input", "test"),
        ("123", "_", "_123"),
        ("123", "var", "var_123"),
        ("123", "var_", "var_123"),
    ],
)
def test_to_valid_python_identifier(input_string, safety_prefix, expected):
    actual = to_valid_python_identifier(input_string, safety_prefix)
    assert expected == actual


@pytest.mark.parametrize(
    ["input_string", "safety_prefix", "expected"],
    [
        ("Foo", "input", "foo"),
        ("Foo-Var", "input", "foo_var"),
        ("CamelCase", "input", "camel_case"),
        ("test", "input", "test"),
        ("My Variable", "input", "my_variable"),
        ("123", "input", "input_123"),
        ("_a", "input", "input_a"),
        ("_123", "input", "input_123"),
        ("123", "_", "_123"),
        ("123", "var", "var_123"),
        ("123", "var_", "var_123"),
    ],
)
def test_to_python_safe_snake_case(input_string, safety_prefix, expected):
    actual = to_python_safe_snake_case(input_string, safety_prefix)
    assert expected == actual
