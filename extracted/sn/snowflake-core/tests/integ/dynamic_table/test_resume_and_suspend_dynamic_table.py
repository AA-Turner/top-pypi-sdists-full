import pytest


def test_resume_and_suspend(dynamic_table_handle, dynamic_tables):
    dynamic_tables["dummy___table"].suspend(if_exists=True)
    dynamic_tables["dummy___table"].resume(if_exists=True)
    assert dynamic_table_handle.fetch().scheduling_state == 'RUNNING'
    dynamic_table_handle.suspend()
    assert dynamic_table_handle.fetch().scheduling_state == 'SUSPENDED'
    dynamic_table_handle.resume()
    assert dynamic_table_handle.fetch().scheduling_state == 'RUNNING'

@pytest.mark.skip("Enable when the DT supports bind parameters")
def test_refresh(dynamic_table_handle, dynamic_tables):
    dynamic_tables["dummy___table"].refresh(if_exists=True)
    dynamic_table_handle.refresh()
