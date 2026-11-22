from datetime import datetime
from recurrence import Recurrence, Rule
import recurrence


RULE = Rule(
    recurrence.DAILY
)

PATTERN = Recurrence(
    dtstart=datetime(2014, 1, 2, 0, 0, 0),
    dtend=datetime(2014, 1, 3, 0, 0, 0),
    rrules=[RULE]
)


def test_occurrences_with_implicit_start_and_end():
    occurrences = [
        instance for instance in
        PATTERN.occurrences()
    ]

    assert occurrences == [
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 3, 0, 0, 0),
    ]

    assert 2 == PATTERN.count()


def test_occurrences_with_explicit_start():
    occurrences = [
        instance for instance in
        PATTERN.occurrences(
            dtstart=datetime(2014, 1, 1, 0, 0, 0),
        )
    ]

    # If you specify dtstart, you get occurrences based on the rules
    # from the Recurrence object, which may be outside of the
    # Recurrence object's range.
    assert occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 3, 0, 0, 0),
    ]

    assert 3 == PATTERN.count(
        dtstart=datetime(2014, 1, 1, 0, 0, 0),
    )


def test_occurrences_with_explicit_end():
    occurrences = [
        instance for instance in
        PATTERN.occurrences(
            dtend=datetime(2014, 1, 4, 0, 0, 0),
        )
    ]

    # If you specify dtend, you get occurrences based on the rules
    # from the Recurrence object, which may be outside of the
    # Recurrence object's range.
    assert occurrences == [
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 3, 0, 0, 0),
        datetime(2014, 1, 4, 0, 0, 0),
    ]

    assert 3 == PATTERN.count(
        dtend=datetime(2014, 1, 4, 0, 0, 0),
    )


def test_occurrences_with_explicit_start_and_end():
    occurrences = [
        instance for instance in
        PATTERN.occurrences(
            dtstart=datetime(2014, 1, 1, 0, 0, 0),
            dtend=datetime(2014, 1, 4, 0, 0, 0),
        )
    ]

    # If you specify dtstart or dtend, you get occurrences based on
    # the rules from the Recurrence object, which may be outside of
    # the Recurrence object's range.
    assert occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 3, 0, 0, 0),
        datetime(2014, 1, 4, 0, 0, 0),
    ]

    assert 4 == PATTERN.count(
        dtstart=datetime(2014, 1, 1, 0, 0, 0),
        dtend=datetime(2014, 1, 4, 0, 0, 0),
    )


def test_occurrences_with_specific_include_dates():
    pattern = Recurrence(
        rdates=[
            datetime(2014, 1, 1, 0, 0, 0),
            datetime(2014, 1, 2, 0, 0, 0),
        ]
    )

    occurrences = [
        instance for instance in
        pattern.occurrences(
            dtstart=datetime(2014, 1, 1, 0, 0, 0),
            dtend=datetime(2014, 1, 4, 0, 0, 0),
        )
    ]

    assert occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 4, 0, 0, 0),
    ]

    assert 3 == pattern.count(
        dtstart=datetime(2014, 1, 1, 0, 0, 0),
        dtend=datetime(2014, 1, 4, 0, 0, 0),
    )

    all_occurrences = [
        instance for instance in
        pattern.occurrences()
    ]

    assert all_occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
    ]

    assert 2 == pattern.count()


def test_occurrences_with_include_date_on_dtend():
    # A date that is listed explicitly is an occurrence, also when it
    # falls on dtend and dtend itself is not included.
    for include_dtend in (True, False):
        pattern = Recurrence(
            rdates=[
                datetime(2014, 1, 2, 0, 0, 0),
                datetime(2014, 1, 4, 0, 0, 0),
            ],
            include_dtstart=False,
            include_dtend=include_dtend,
        )

        occurrences = [
            instance for instance in
            pattern.occurrences(
                dtstart=datetime(2014, 1, 1, 0, 0, 0),
                dtend=datetime(2014, 1, 4, 0, 0, 0),
            )
        ]

        assert occurrences == [
            datetime(2014, 1, 2, 0, 0, 0),
            datetime(2014, 1, 4, 0, 0, 0),
        ]


def test_occurrences_with_exclude_date_on_dtend():
    def occurrences(include_dtend):
        pattern = Recurrence(
            rrules=[Rule(recurrence.DAILY)],
            exdates=[datetime(2014, 1, 3, 0, 0, 0)],
            include_dtend=include_dtend,
        )
        return [
            instance for instance in
            pattern.occurrences(
                dtstart=datetime(2014, 1, 1, 0, 0, 0),
                dtend=datetime(2014, 1, 3, 0, 0, 0),
            )
        ]

    # An included dtend is always an occurrence
    assert occurrences(include_dtend=True) == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 3, 0, 0, 0),
    ]

    # Without it, an exclusion on dtend applies like any other
    assert occurrences(include_dtend=False) == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
    ]


def test_occurrences_until():
    rule = Rule(
        recurrence.DAILY,
        until=datetime(2014, 1, 3, 0, 0, 0)
    )

    pattern = Recurrence(
        rrules=[
            rule
        ]
    )

    occurrences = [
        instance for instance in
        pattern.occurrences(
            dtstart=datetime(2014, 1, 1, 0, 0, 0),
            dtend=datetime(2014, 1, 5, 0, 0, 0),
        )
    ]

    assert occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
        datetime(2014, 1, 3, 0, 0, 0),
        # We always get dtend, for reasons that aren't entirely clear
        datetime(2014, 1, 5, 0, 0, 0),
    ]

    assert 4 == pattern.count(
        dtstart=datetime(2014, 1, 1, 0, 0, 0),
        dtend=datetime(2014, 1, 5, 0, 0, 0),
    )

    occurrences = [
        instance for instance in
        pattern.occurrences(
            dtstart=datetime(2014, 1, 1, 0, 0, 0),
            dtend=datetime(2014, 1, 2, 0, 0, 0),
        )
    ]

    assert occurrences == [
        datetime(2014, 1, 1, 0, 0, 0),
        datetime(2014, 1, 2, 0, 0, 0),
    ]

    assert 2 == pattern.count(
        dtstart=datetime(2014, 1, 1, 0, 0, 0),
        dtend=datetime(2014, 1, 2, 0, 0, 0),
    )


def test_before():
    assert PATTERN.before(
        datetime(2014, 1, 3, 0, 0, 0)
    ) == datetime(2014, 1, 2, 0, 0, 0)

    assert PATTERN.before(
        datetime(2014, 1, 3, 0, 0, 0),
        inc=True
    ) == datetime(2014, 1, 3, 0, 0, 0)


def test_after():
    assert PATTERN.after(
        datetime(2014, 1, 2, 0, 0, 0)
    ) == datetime(2014, 1, 3, 0, 0, 0)

    assert PATTERN.after(
        datetime(2014, 1, 2, 0, 0, 0),
        inc=True
    ) == datetime(2014, 1, 2, 0, 0, 0)
