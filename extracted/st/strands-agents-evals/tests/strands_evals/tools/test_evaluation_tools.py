from strands_evals.tools.evaluation_tools import (
    any_order_match_scorer,
    exact_match_scorer,
    in_order_match_scorer,
)


def test_exact_match_scorer_perfect_match():
    """Test exact match with perfect match"""
    actual = ["step1", "step2", "step3"]
    expected = ["step1", "step2", "step3"]
    assert exact_match_scorer(actual, expected) == 1.0


def test_exact_match_scorer_no_match():
    """Test exact match with no match"""
    actual = ["step1", "step2", "step3"]
    expected = ["step4", "step5", "step6"]
    assert exact_match_scorer(actual, expected) == 0.0


def test_exact_match_scorer_partial_match():
    """Test exact match with partial match"""
    actual = ["step1", "step2", "wrong"]
    expected = ["step1", "step2", "step3"]
    assert exact_match_scorer(actual, expected) == 2 / 3


def test_exact_match_scorer_uneven_match_1():
    """Test exact match with uneven match"""
    actual = ["step2", "wrong"]
    expected = ["step1", "step2", "step3"]
    assert exact_match_scorer(actual, expected) == 0.0


def test_exact_match_scorer_uneven_match_2():
    """Test exact match with uneven match"""
    actual = ["step2", "step1", "step3", "step4"]
    expected = ["step1", "step2", "step3"]
    assert exact_match_scorer(actual, expected) == 1 / 3


def test_in_order_match_scorer_perfect_order():
    """Test in-order match with perfect order"""
    actual = ["step1", "step2", "step3"]
    expected = ["step1", "step2", "step3"]
    assert in_order_match_scorer(actual, expected) == 1.0


def test_in_order_match_scorer_with_extras():
    """Test in-order match with extra actions"""
    actual = ["step1", "extra", "step2", "step3"]
    expected = ["step1", "step2", "step3"]
    assert in_order_match_scorer(actual, expected) == 1.0


def test_in_order_match_scorer_partial_order():
    """Test in-order match with partial order"""
    actual = ["step1", "step2"]
    expected = ["step1", "step2", "step3"]
    assert in_order_match_scorer(actual, expected) == 2 / 3


def test_in_order_match_scorer_wrong_order():
    """Test in-order match with wrong order"""
    actual = ["step2", "step1", "step3"]
    expected = ["step1", "step2", "step3"]
    assert in_order_match_scorer(actual, expected) == 1 / 3  # Only step3 matches in order


def test_in_order_match_scorer_empty_actual():
    """Test in-order match with empty actual"""
    actual = []
    expected = ["step1", "step2", "step3"]
    assert in_order_match_scorer(actual, expected) == 0


def test_in_order_match_scorer_empty_expected():
    """Test in-order match with empty expected"""
    actual = ["step1", "step2", "step3"]
    expected = []
    assert in_order_match_scorer(actual, expected) == 1


def test_any_order_match_scorer_perfect_match():
    """Test any-order match with all actions present"""
    actual = ["step3", "step1", "step2"]
    expected = ["step1", "step2", "step3"]
    assert any_order_match_scorer(actual, expected) == 1.0


def test_any_order_match_scorer_with_extras():
    """Test any-order match with extra actions"""
    actual = ["step3", "extra", "step1", "step2"]
    expected = ["step1", "step2", "step3"]
    assert any_order_match_scorer(actual, expected) == 1.0


def test_any_order_match_scorer_partial_match():
    """Test any-order match with partial match"""
    actual = ["step1", "step2"]
    expected = ["step1", "step2", "step3"]
    assert any_order_match_scorer(actual, expected) == 2 / 3


def test_any_order_match_scorer_empty_actual():
    """Test any-order match with empty actual"""
    actual = []
    expected = ["step1", "step2", "step3"]
    assert any_order_match_scorer(actual, expected) == 0


def test_any_order_match_scorer_empty_expected():
    """Test any-order match with empty expected"""
    actual = ["step1", "step2", "step3"]
    expected = []
    assert any_order_match_scorer(actual, expected) == 1
