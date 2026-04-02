import pytest
import apyds


@pytest.fixture
def chain() -> apyds.Chain:
    return apyds.Chain(100, 1000)


def test_reset_parameters(chain: apyds.Chain) -> None:
    chain.set_limit_size(50)
    chain.set_buffer_size(500)
    chain.reset()


def test_add_rule_and_fact(chain: apyds.Chain) -> None:
    assert chain.add("test rule")
    assert chain.add("fact")


def test_add_fail(chain: apyds.Chain) -> None:
    chain.set_limit_size(10)
    assert not chain.add("a-long-facts-that-exceeds-limit")


def test_execute_single_premise(chain: apyds.Chain) -> None:
    chain.add("p q")
    chain.add("p")
    target = apyds.Rule("q")
    success = False

    def callback(rule: apyds.Rule) -> bool:
        nonlocal success
        if rule == target:
            success = True
            return True
        return False

    count = chain.execute(callback)
    assert count == 1
    assert success


def test_execute_multiple_premises_chain(chain: apyds.Chain) -> None:
    chain.add("p q r")
    chain.add("p")
    chain.add("q")
    target = apyds.Rule("r")
    success = False

    def callback(rule: apyds.Rule) -> bool:
        nonlocal success
        if rule == target:
            success = True
        return False

    count = chain.execute(callback)
    assert count == 2
    assert success


def test_execute_multiple_premises_partial(chain: apyds.Chain) -> None:
    chain.add("p q r")
    chain.add("p")
    count = chain.execute(lambda rule: False)
    assert count == 1


def test_execute_three_premises(chain: apyds.Chain) -> None:
    chain.add("p q r s")
    chain.add("p")
    chain.add("q")
    chain.add("r")
    target = apyds.Rule("s")
    success = False

    def callback(rule: apyds.Rule) -> bool:
        nonlocal success
        if rule == target:
            success = True
        return False

    count = chain.execute(callback)
    assert count == 3
    assert success


def test_execute_duplicated_fact(chain: apyds.Chain) -> None:
    chain.add("p r")
    chain.add("q r")
    chain.add("p")
    chain.add("q")
    count = chain.execute(lambda rule: False)
    assert count == 1


def test_execute_exceed(chain: apyds.Chain) -> None:
    chain.set_limit_size(100)
    assert chain.add("(2 `x) (`x `x`)")
    assert chain.add("(2 a-very-long-fact-that-exceeds-half-of-the-limit-size)")
    count = chain.execute(lambda rule: False)
    assert count == 0


def test_dont_generate_duplicated_fact(chain: apyds.Chain) -> None:
    assert chain.add("aaaaa bbbbb")
    assert chain.add("aaaaa")
    assert chain.execute(lambda rule: False) == 1
    assert chain.execute(lambda rule: False) == 0


def test_execute_exceed_by_too_many_premises() -> None:
    chain = apyds.Chain(100, 1000)
    assert chain.add("aaaaa bbbbb ccccc ddddd eeeee fffff")
    assert chain.add("aaaaa")
    assert chain.add("bbbbb")
    assert chain.add("ccccc")
    assert chain.add("ddddd")
    assert chain.add("eeeee")
    assert chain.execute(lambda rule: False) == 5

    chain.reset()
    chain.set_limit_size(100)
    chain.set_buffer_size(1000)
    assert chain.add("aaaaa bbbbb ccccc ddddd eeeee fffff")
    assert chain.add("aaaaa")
    assert chain.add("bbbbb")
    assert chain.add("ccccc")
    assert chain.add("ddddd")
    assert chain.add("eeeee")
    assert chain.execute(lambda rule: False) == 5

    chain.reset()
    chain.set_limit_size(100)
    chain.set_buffer_size(100)
    assert chain.add("aaaaa bbbbb ccccc ddddd eeeee fffff")
    assert chain.add("aaaaa")
    assert chain.add("bbbbb")
    assert chain.add("ccccc")
    assert chain.add("ddddd")
    assert chain.add("eeeee")
    assert chain.execute(lambda rule: False) == 1


def test_iterator(chain: apyds.Chain) -> None:
    chain.add("a")
    chain.add("b")
    chain.add("a b c")
    expected = ["b\n----\nc\n", "----\nc\n"]
    count = 0
    for rule in chain:
        assert count < len(expected)
        assert str(rule) == expected[count]
        count += 1
    assert count == len(expected)
