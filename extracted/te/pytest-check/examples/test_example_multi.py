from pytest_check import check

check.set_max_fail(9)
check.set_max_report(9)
check.call_on_fail(lambda message: print(f'FROM CALL ON FAIL: "{message}"'))


def test_foo():
    check.is_true(False, msg="check #1")
    check.is_true(False, msg="check #2")
    check.is_true(False, msg="check #3")
