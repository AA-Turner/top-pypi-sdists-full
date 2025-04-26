from uuid import UUID

from pycarlo.common import MCONParser

TEST_ACCOUNT_ID = "12345678-1234-5678-1234-567812345678"
TEST_RESOURCE_ID = "21345678-1234-5678-1234-567812345678"
TEST_TABLE_ID = "db:sch.tbl"


def test_valid_table_mcon():
    mcon = f"MCON++{TEST_ACCOUNT_ID}++{TEST_RESOURCE_ID}++table++{TEST_TABLE_ID}"
    parsed_mcon = MCONParser.parse_mcon(mcon)
    assert parsed_mcon is not None
    assert UUID(TEST_ACCOUNT_ID) == parsed_mcon.account_id
    assert UUID(TEST_RESOURCE_ID) == parsed_mcon.resource_id
    assert "table" == parsed_mcon.object_type
    assert TEST_TABLE_ID == parsed_mcon.object_id


def test_invalid_mcon():
    mcon = "invalid"
    parsed_mcon = MCONParser.parse_mcon(mcon)
    assert parsed_mcon is None


def test_valid_field_mcon():
    field_id = f"{TEST_TABLE_ID}+++field_id"
    mcon = f"MCON++{TEST_ACCOUNT_ID}++{TEST_RESOURCE_ID}++field++{field_id}"
    parsed_mcon = MCONParser.parse_mcon(mcon)
    assert parsed_mcon is not None
    assert UUID(TEST_ACCOUNT_ID) == parsed_mcon.account_id
    assert UUID(TEST_RESOURCE_ID) == parsed_mcon.resource_id
    assert "field" == parsed_mcon.object_type
    assert field_id == parsed_mcon.object_id
