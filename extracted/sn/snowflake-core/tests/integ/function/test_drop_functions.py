import pytest

from tests.utils import random_string

from .utils import create_service_function


@pytest.mark.flaky
def test_drop_functions(temp_service_for_function, functions):
    funcs = []
    func_objects = []

    function_name_prefix = random_string(5, "test_func_")
    for i in range(5):
        function_name = f"{function_name_prefix}_foofunc_{str(i)}"
        function_name_with_args = f"{function_name}(REAL)"
        endpoint = "ep1"

        func_objects.append(create_service_function(
            function_name, ["REAL"], "REAL", endpoint,
            temp_service_for_function.name, functions
        ))

        funcs.append(function_name_with_args)

    ct = len([func.name for func in functions.iter()])

    for i in range(5):
        if i % 2 == 0:
            func_objects[i].drop()
        else:
            functions[funcs[i]].drop()
        functions["dummy_______()"].drop(if_exists=True)
        assert len([f.name for f in functions.iter()]) == ct - 1 - i
