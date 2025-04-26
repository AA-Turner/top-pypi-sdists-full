from snowflake.core._internal.utils import normalize_and_unquote_name


def test_fetch(temp_stage, temp_stage_case_sensitive):
    stage = temp_stage.fetch()
    assert stage.name.upper() == temp_stage.name.upper()

    stage = temp_stage_case_sensitive.fetch()
    assert stage.name == normalize_and_unquote_name(temp_stage_case_sensitive.name)
    assert stage.kind == "PERMANENT"
    assert stage.url is not None
    assert stage.storage_integration is None
    assert stage.comment == "created by temp_stage"
    assert stage.created_on is not None
    assert stage.owner_role_type is not None
    assert stage.directory_table is not None
    assert stage.has_credentials is not None
    assert stage.has_encryption_key is not None
