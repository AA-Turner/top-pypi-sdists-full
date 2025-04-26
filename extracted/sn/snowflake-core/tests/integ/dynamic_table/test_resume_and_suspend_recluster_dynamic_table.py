

def test_resume_and_suspend_recluster(dynamic_table_handle, dynamic_tables):
    dynamic_tables["dummy___table"].suspend_recluster(if_exists=True)
    dynamic_tables["dummy___table"].resume_recluster(if_exists=True)
    assert dynamic_table_handle.fetch().automatic_clustering is True
    dynamic_table_handle.suspend_recluster()
    assert dynamic_table_handle.fetch().automatic_clustering is False
    dynamic_table_handle.resume_recluster()
    assert dynamic_table_handle.fetch().automatic_clustering is True
