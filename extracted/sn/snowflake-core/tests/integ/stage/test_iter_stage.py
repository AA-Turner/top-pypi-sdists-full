from operator import attrgetter

from snowflake.core._internal.utils import normalize_and_unquote_name


def test_iter(stages, temp_stage, temp_stage_case_sensitive):
    stage_names = tuple(
        map(
            attrgetter("name"),
            stages.iter(),
        )
    )
    assert any(
        map(
            lambda e: e in stage_names,
            (
                temp_stage.name.upper(),  # for upper/lower case names
                normalize_and_unquote_name(temp_stage_case_sensitive.name),
            ),
        )
    )


def test_iter_like(stages, temp_stage, temp_stage_case_sensitive):
    stage_names = tuple(
        map(
            attrgetter("name"),
            stages.iter(like="test_stage%"),
        )
    )
    assert any(
        map(
            lambda e: e in stage_names,
            (
                temp_stage.name.upper(),  # for upper/lower case names
                normalize_and_unquote_name(temp_stage_case_sensitive.name),
            ),
        )
    )

    # no result for random
    stage_names = list(stages.iter(like="RANDOM"))
    assert len(stage_names) == 0
