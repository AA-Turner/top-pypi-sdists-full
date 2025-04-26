import pytest

from tests.utils import random_string

from .utils import create_service_function


@pytest.mark.flaky
def test_iter_functions(temp_service_for_function, functions):
    funcs = []

    try:
        function_name_prefix = random_string(5, "test_func_")
        for i in range(5):
            function_name = f"{function_name_prefix}_iter_foofunc_{str(i)}"
            function_name_with_args = f"{function_name}(REAL)"
            endpoint = "ep1"

            create_service_function(
                function_name, ["REAL"], "REAL", endpoint,
                temp_service_for_function.name, functions
            )

            funcs.append(function_name_with_args)

        for i in range(3):
            function_name = f"{function_name_prefix}_iter_woofunc_{str(i)}"
            function_name_with_args = f"{function_name}(REAL)"
            endpoint = "end-point-2"

            create_service_function(
                function_name, ["REAL"], "REAL", endpoint,
                temp_service_for_function.name, functions
            )

            funcs.append(function_name_with_args)

        assert len([func.name for func in functions.iter()]) >= 8
        assert len([func.name for func in functions.iter(like=r"%%\_iter\_foofunc\_%%")]) == 5
        assert len([func.name for func in functions.iter(like=r"%%\_iter\_woofunc\_%%")]) == 3

    finally:
        for i in funcs:
            functions[i].drop()
