from aws_packages import sum_as_string


def test_sum_as_string():
    result = sum_as_string(1, 2)
    assert result == "3"
