import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.stage import Stage
from tests.utils import random_string


def test_drop(stages):
    comment = "my comment"
    new_stage = Stage(
        name=random_string(5, "test_stage_"),
        comment=comment,
    )
    try:
        s = stages.create(new_stage)
        assert s.fetch().comment == comment
    finally:
        s.drop()

    with pytest.raises(
        NotFoundError,
    ):
        s.fetch()
    try:
        s = stages.create(new_stage)
        assert s.fetch().comment == comment
    finally:
        s.drop()

    # check if exists
    with pytest.raises(
        NotFoundError,
    ):
        stages["RANDOM"].drop()

    stages["RANDOM"].drop(if_exists=True)
