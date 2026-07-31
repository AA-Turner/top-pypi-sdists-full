import pandas as pd
import pytest
import sqlalchemy as sqla
import tentaclio
from tentaclio import credentials

import tentaclio_postgres

TEST_TABLE_NAME = "test_table"
TEST_COLUMNS = ["col_1", "col_2", "col_3"]
TEST_VALUES = [0, 1, 2]


@pytest.fixture
def fixture_client(db_client):
    test_meta = sqla.MetaData()
    sqla.Table(
        # Meta
        TEST_TABLE_NAME,
        test_meta,
        # Columns
        sqla.Column(TEST_COLUMNS[0], sqla.Integer),
        sqla.Column(TEST_COLUMNS[1], sqla.Integer),
        sqla.Column(TEST_COLUMNS[2], sqla.Integer),
    )
    db_client.set_schema(test_meta)
    # Commit the schema creation so other connections can see the table
    db_client.conn.commit()
    yield db_client
    db_client.delete_schema(test_meta)
    db_client.conn.commit()


@pytest.fixture
def fixture_df():
    df = pd.DataFrame(data=[TEST_VALUES], columns=TEST_COLUMNS)
    return df


def test_authenticated_api_calls(fixture_client, fixture_df):
    with tentaclio.open(
        f"postgresql://hostname{fixture_client.url.path}::{TEST_TABLE_NAME}", mode="w"
    ) as writer:
        fixture_df.to_csv(writer, index=False)

    with tentaclio_postgres.PostgresClient(
        credentials.authenticate(f"postgresql://hostname{fixture_client.url.path}")
    ) as client:
        retrieved_df = client.get_df(f"select * from {TEST_TABLE_NAME}")

    assert retrieved_df.equals(fixture_df)
