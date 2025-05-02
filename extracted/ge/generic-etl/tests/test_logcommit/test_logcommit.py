import logging
import os
from etl.utils.log import LogCommit
from etl.utils.database import Database
import pytest
import csv

import logging


@pytest.fixture(scope="module")
def logger(tmpdir_factory):
    # Create a temporary log file path
    log_file = tmpdir_factory.mktemp("logs").join("test_log.txt")

    # Create an instance of the InjectingLogger with file streaming
    logger = LogCommit("Log_Commit", log_file)
    logger.setLevel(logging.DEBUG)
    return logger


@pytest.fixture(scope="module")
def database_url():
    # Use an in-memory SQLite database for testing
    return "sqlite:///:memory:"


def test_log_messages(logger):
    # Log some messages
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")

    # Ensure log messages are stored in log_data

    with open(logger.log_file, "r") as f:
        data = list(csv.reader(f))

    assert len(data) == 3
    print(data[0][1])
    assert data[0][1] == "This is an info message"
    assert data[1][1] == "This is a warning message"
    assert data[2][1] == "This is an error message"


def test_log_commit(logger, database_url):
    # Log some messages
    logger.info("Log message 1")
    logger.warning("Log message 2")
    logger.error("Log message 3")

    secrets = {"sqlite": {"type": "sqlite", "dbfile": ":memory:"}}
    inserts = logger.log_commit(secrets, "sqlite")
    # assert inserts.rowcount == 3

    secrets = {"sqlite": {"type": "sqlite", "dbfile": ":memory:"}}
    expected_messages = ["Log message 1", "Log message 2", "Log message 3"]
    with Database(secrets, "sqlite") as db:
        ret = db.execute("SELECT * FROM log_data")
        print(list(ret["log_entry"]))
        for item1, item2 in zip(expected_messages, list(ret["log_entry"])):
            assert item1 == item2


# Run the tests
if __name__ == "__main__":
    pytest.main()
