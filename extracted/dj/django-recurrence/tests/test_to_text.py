from django.utils import translation

from recurrence import Rule
import recurrence


def test_rule_to_text_simple():
    assert Rule(
        recurrence.WEEKLY
    ).to_text() == 'weekly'


def test_rule_to_text_interval():
    assert Rule(
        recurrence.WEEKLY,
        interval=3
    ).to_text() == 'every 3 weeks'


def test_rule_to_text_oneoff():
    assert Rule(
        recurrence.WEEKLY,
        count=1
    ).to_text() == 'weekly, occuring once'


def test_rule_to_text_multiple():
    assert Rule(
        recurrence.WEEKLY,
        count=5
    ).to_text() == 'weekly, occuring 5 times'


def test_rule_to_text_yearly_bymonth():
    assert Rule(
        recurrence.YEARLY,
        bymonth=[1, 3],
    ).to_text() == 'annually, each January, March'

    assert Rule(
        recurrence.YEARLY,
        bymonth=[1, 3],
    ).to_text(True) == 'annually, each Jan, Mar'


def test_rule_to_text_yearly_byday():
    assert Rule(
        recurrence.YEARLY,
        byday=[1, 3],
    ).to_text() == 'annually, on the Tuesday, Thursday'

    assert Rule(
        recurrence.YEARLY,
        byday=[1, 3],
    ).to_text(True) == 'annually, on the Tue, Thu'


def test_rule_to_text_translates_may():
    rule = Rule(recurrence.YEARLY, bymonth=[5])
    with translation.override('de'):
        assert rule.to_text() == 'jährlich, jeden Mai'
        assert rule.to_text(short=True) == 'jährlich, jeden Mai'
    with translation.override('fr'):
        assert rule.to_text() == 'annuel, chaque mai'


def test_rule_to_text_in_spanish():
    with translation.override('es'):
        assert Rule(
            recurrence.WEEKLY,
            count=1
        ).to_text() == 'semanalmente, ocurre una vez'
        assert Rule(
            recurrence.YEARLY,
            bymonth=[5, 11]
        ).to_text() == 'anualmente, cada Mayo, Noviembre'


def test_rule_to_text_separator_in_brazilian_portuguese():
    with translation.override('pt-br'):
        assert Rule(
            recurrence.WEEKLY,
            count=1
        ).to_text() == 'semanalmente, que ocorre uma vez'


def test_rule_to_text_abbreviates_may():
    rule = Rule(recurrence.YEARLY, bymonth=[5])
    with translation.override('hu'):
        assert rule.to_text() == 'évente, minden Május'
        assert rule.to_text(short=True) == 'évente, minden Máj'
