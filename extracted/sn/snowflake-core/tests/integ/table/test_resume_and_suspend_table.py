import pytest

from snowflake.core.exceptions import NotFoundError


def test_resume_and_suspend_cluster(tables, table_handle):
    # verify resume
    table_handle.resume_recluster()
    table_handle.drop()
    table_handle.resume_recluster(if_exists=True)
    with pytest.raises(NotFoundError):
        table_handle.resume_recluster()
    table_handle.undrop()
    # check resume after suspend
    table_handle.suspend_recluster()
    table_handle.resume_recluster()

    # verify suspend
    # verify suspend when it is resumed
    table_handle.suspend_recluster()

    # verify suspend when it is suspended
    table_handle.suspend_recluster()

    # verify suspend when it is dropped
    table_handle.drop()
    with pytest.raises(NotFoundError):
        table_handle.suspend_recluster()
    table_handle.suspend_recluster(if_exists=True)
