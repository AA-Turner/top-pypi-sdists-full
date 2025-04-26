import logging

import pytest

from snowflake.core.exceptions import NotFoundError


def test_request_id_logging_negative(root, caplog):
    with caplog.at_level(logging.DEBUG, "snowflake.core"):
        with pytest.raises(NotFoundError) as e:
            root.databases["nonexistent_db"].fetch()
        request_id = e.value.request_id
    assert any(request_id in m for m in caplog.messages)
