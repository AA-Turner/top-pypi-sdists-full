import pytest

from tests.utils import random_string

from .utils import create_service_function


TRANSLATE_DATA_TYPE_TO_BIND = {"INT": "FIXED"}


@pytest.mark.usefixtures("qa_mode_enabled")
def test_execute_function(temp_service_for_function, functions, setup_with_connector_execution):
    types = [["REAL"], ["INT"], ["BOOLEAN"], ["REAL", "INT"]]
    inputs = [[12.3], [12], [True], [12, 1]]
    outputs = [12.3, 12, True, 12.0]

    alter_prefix = "alter session "
    with setup_with_connector_execution(
        [
            alter_prefix + "set QA_MODE_MOCK_EXTERNAL_FUNCTION_REMOTE_CALLS = true",
            alter_prefix + """set snowservices_mock_server_endpoints =
                  '{"ep1":["mockhost1", "mockhost2"],"end-point-2":["mockhost3"]}';
            """,
        ],
        [
            alter_prefix + "unset QA_MODE_MOCK_EXTERNAL_FUNCTION_REMOTE_CALLS",
            alter_prefix + "unset snowservices_mock_server_endpoints",
        ],
    ):
        for i in range(len(inputs)):
            t = types[i]
            function_name = random_string(5, "test_func_")
            function_name_with_args = f'{function_name}({",".join(t)})'
            endpoint = 'end-point-2' if t == "INT" else "ep1"
            try:
                f = create_service_function(
                    function_name, t, t[0], endpoint,
                    temp_service_for_function.name, functions
                )
                assert f.execute(inputs[i]) == outputs[i]
            finally:
                functions[function_name_with_args].drop()
