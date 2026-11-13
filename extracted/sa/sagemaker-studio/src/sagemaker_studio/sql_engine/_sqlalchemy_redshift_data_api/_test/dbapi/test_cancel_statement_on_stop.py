"""
Tests for cancel-statement-on-stop on the Redshift Data API driver.

Stopping a SQL cell delivers a SIGINT, which becomes a ``KeyboardInterrupt`` inside
``_poll_statement_completion`` -- the frame that holds the in-flight statement's id. That frame
now asks the service to cancel the statement before letting the interrupt continue, so the
query stops server-side instead of running on unattended.

The boto3 client is a Mock; no AWS call is made.
"""

from unittest.mock import Mock, patch

import pytest

from ...dbapi.connection import Connection
from ...dbapi.connection_params import ConnectionParams
from ...dbapi.cursor import StatementExecutor

STATEMENT_ID = "stmt-cancel-on-stop"


@pytest.fixture
def statement_executor():
    connection = Mock(spec=Connection)
    connection.client = Mock()
    connection.connection_params = ConnectionParams(
        cluster_identifier="test-cluster",
        database_name="testdb",
        db_user="test_user",
        region="us-east-1",
    )
    connection.get_transaction_id.return_value = None
    connection._closed = False
    return StatementExecutor(connection)


class TestInterruptCancelsTheStatement:
    def test_interrupt_while_polling_cancels_the_in_flight_statement(
        self, statement_executor, capsys
    ):
        """The interrupt reaches the caller unchanged, and exactly one cancel is issued."""
        statement_executor.client.describe_statement.side_effect = KeyboardInterrupt
        statement_executor.client.cancel_statement.return_value = {"Status": True}

        with pytest.raises(KeyboardInterrupt) as raised:
            statement_executor._poll_statement_completion(STATEMENT_ID, {})

        assert raised.value.__cause__ is None
        statement_executor.client.cancel_statement.assert_called_once_with(Id=STATEMENT_ID)
        # The cell shows why it stopped, above the traceback.
        assert "cancel request accepted by Redshift" in capsys.readouterr().err

    def test_a_rejected_cancel_tells_the_user_the_query_may_still_run(
        self, statement_executor, capsys
    ):
        """
        The case the removed swallow used to hide: CancelStatement is rejected, so the
        statement may still be running and the user is the only one who can act on that.
        """
        statement_executor.client.describe_statement.side_effect = KeyboardInterrupt
        statement_executor.client.cancel_statement.side_effect = RuntimeError("AccessDenied")

        with pytest.raises(KeyboardInterrupt):
            statement_executor._poll_statement_completion(STATEMENT_ID, {})

        err = capsys.readouterr().err
        assert "cancel request to Redshift did not complete" in err
        assert "may still be running" in err

    @pytest.mark.parametrize(
        "response, expected",
        [
            pytest.param({"Status": True}, "cancel request accepted by Redshift", id="true"),
            pytest.param(
                {"Status": False}, "cancel request to Redshift did not complete", id="false"
            ),
            pytest.param({}, "cancel request to Redshift did not complete", id="missing"),
        ],
    )
    def test_the_reported_outcome_follows_the_cancel_status(
        self, statement_executor, capsys, response, expected
    ):
        """Only an explicit `Status: True` is reported as accepted."""
        statement_executor.client.describe_statement.side_effect = KeyboardInterrupt
        statement_executor.client.cancel_statement.return_value = response

        with pytest.raises(KeyboardInterrupt):
            statement_executor._poll_statement_completion(STATEMENT_ID, {})

        assert expected in capsys.readouterr().err

    def test_interrupt_before_the_loop_still_cancels(self, statement_executor):
        """The handler wraps the pre-loop setup too, which runs with the statement in flight."""
        with patch.object(
            statement_executor, "_long_poll_supported", side_effect=KeyboardInterrupt
        ):
            with pytest.raises(KeyboardInterrupt):
                statement_executor._poll_statement_completion(STATEMENT_ID, {})

        statement_executor.client.cancel_statement.assert_called_once_with(Id=STATEMENT_ID)

    def test_a_statement_that_finishes_issues_no_cancel(self, statement_executor):
        statement_executor.client.describe_statement.return_value = {
            "Status": "FINISHED",
            "HasResultSet": True,
        }

        result = statement_executor._poll_statement_completion(STATEMENT_ID, {})

        assert result["status"] == "FINISHED"
        statement_executor.client.cancel_statement.assert_not_called()
