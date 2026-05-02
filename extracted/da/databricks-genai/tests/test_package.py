def test_package():
    import databricks
    del databricks

    from databricks import model_training
    assert model_training
    del model_training

    from databricks.model_training import exceptions
    assert exceptions
    del exceptions

    from databricks.model_training import types
    assert types
    assert types.training_run
    del types
