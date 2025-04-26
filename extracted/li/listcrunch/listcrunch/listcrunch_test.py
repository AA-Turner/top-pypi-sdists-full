from listcrunch import crunch, uncrunch


def test_basic_crunch():
    assert crunch([1, 2, 3]) == "1:0;2:1;3:2"


def test_basic_uncrunch():
    assert uncrunch("1:0;2:1;3:2") == ["1", "2", "3"]


def test_basic_run():
    assert crunch([1, 1, 1]) == "1:0-2"


def test_basic_run_uncrunch():
    assert uncrunch("1:0-2") == ["1", "1", "1"]


def test_basic_broken_run():
    assert crunch([1, 2, 1]) == "1:0,2;2:1"


def test_basic_broken_run_uncrunch():
    assert uncrunch("1:0,2;2:1") == ["1", "2", "1"]


def test_order():
    assert crunch([2, 1]) == "2:0;1:1"


def test_order_uncrunch():
    assert uncrunch("2:0;1:1") == ["2", "1"]


def test_advanced():
    assert crunch([50, 50, 3, 50, 50, 3, 60, 70, 70]) == "50:0-1,3-4;3:2,5;60:6;70:7-8"


def test_advanced_uncrunch():
    assert uncrunch("50:0-1,3-4;3:2,5;60:6;70:7-8") == [
        "50",
        "50",
        "3",
        "50",
        "50",
        "3",
        "60",
        "70",
        "70",
    ]


def test_empty_crunch():
    assert crunch([]) == ""


def test_empty_uncrunch():
    assert uncrunch("") == []


def test_single_item_crunch():
    assert crunch([77]) == "77:0"


def test_single_item_uncrunch():
    assert uncrunch("77:0") == ["77"]
