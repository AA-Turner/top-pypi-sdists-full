import re


def test_max_tb_line_uses_inner_line_for_with_check(pytester):
    pytester.copy_example("examples/test_example_traceback.py")
    result = pytester.runpytest(
        "--check-max-tb=0",
        "--check-max-tb-line=1",
        "test_example_traceback.py::test_tb_ctx",
    )
    result.assert_outcomes(failed=1)
    result.stdout.fnmatch_lines(
        [
            "*FAILURE: assert message*",
            '*test_example_traceback.py:* in helper2_ctx() -> assert 1 == 2, "assert message"',
        ],
    )
    result.stdout.no_fnmatch_line('*-> with check("check message"):*')


def test_max_tb_line_includes_line_and_exception_summary(pytester):
    pytester.copy_example("examples/test_example_multi_check_raises.py")
    result = pytester.runpytest("--check-max-tb=1", "--check-max-tb-line=4")
    result.assert_outcomes(failed=1)
    output = str(result.stdout)
    assert re.search(
        r"FAILURE: list index out of range, "
        r"test_example_multi_check_raises\.py:\d+ in test_multi_check_raises\(\) "
        r'-> assert lst_1\[-1\] == "Fail 2": IndexError: list index out of range',
        output,
    )
