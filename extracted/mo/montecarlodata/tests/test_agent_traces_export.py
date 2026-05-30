"""Tests for `montecarlo agent-traces export`."""

import tempfile
from pathlib import Path
from typing import Optional
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

import click
import pytest
from box import Box

from montecarlodata.agent_traces.export_service import AgentTraceExportService
from montecarlodata.common.data import MonolithResponse
from montecarlodata.utils import GqlWrapper
from tests.test_common_user import _SAMPLE_CONFIG

SAMPLE_MCON = "MCON++aaaa-bbbb-cccc-dddd++eeee-ffff-gggg-hhhh++table++db:schema.traces"
SAMPLE_TRACE_ID = "abcdef1234567890abcdef1234567890"
SAMPLE_JOB_ID = "11111111-2222-3333-4444-555555555555"
SAMPLE_URL = "https://signed.example/job.json.gz"
SAMPLE_TRACE_LINK = (
    f"https://app.getmontecarlo.com/agents/{SAMPLE_MCON}/ai-agent/traces/{SAMPLE_TRACE_ID}"
)
GZIPPED_BODY = b"\x1f\x8b\x08\x00fake-gzip-bytes"


def _mutation_response(job_id: str = SAMPLE_JOB_ID) -> MonolithResponse:
    # GraphQL response keys are camelCase; Box uses exact-key attribute access.
    return MonolithResponse(data=Box({"jobId": job_id}), errors=None)


def _status_response(
    status: str,
    url: Optional[str] = None,
    error: Optional[str] = None,
) -> MonolithResponse:
    return MonolithResponse(
        data=Box(
            {
                "status": status,
                "url": url,
                "error": error,
                "createdTime": "2026-05-19T12:00:00+00:00",
                "expiresAt": None,
            }
        ),
        errors=None,
    )


def _error_response(message: str) -> MonolithResponse:
    """A poll-time error: server returned 200 with `errors:[]` and null data.
    Models the gateway / middleware error path (e.g. "Request timed out")
    that the poll loop should tolerate as transient up to the threshold."""
    return MonolithResponse(data=None, errors=[{"message": message}])


class AgentTraceExportServiceTest(TestCase):
    def setUp(self) -> None:
        # Production uses two GqlWrappers — strict for the mutation,
        # lenient (abort_on_error=False) for polling. Tests alias them
        # to a single mock so the existing `_set_responses(mutation,
        # *polls)` ordering still works: side_effect is consumed in
        # call-order across both wrappers.
        self._request_wrapper = Mock(autospec=GqlWrapper)
        self._service = AgentTraceExportService(
            _SAMPLE_CONFIG,
            command_name="test",
            request_wrapper=self._request_wrapper,
            polling_wrapper=self._request_wrapper,
        )

    def _set_responses(self, *responses: MonolithResponse) -> None:
        self._request_wrapper.make_request_v2.side_effect = list(responses)

    @patch("montecarlodata.agent_traces.export_service.requests.get")
    @patch("montecarlodata.agent_traces.export_service.click.echo")
    def test_happy_path_downloads_to_default_output(self, _echo, mock_get):
        self._set_responses(
            _mutation_response(),
            _status_response("DONE", url=SAMPLE_URL),
        )
        # Mock the streamed download to write a known byte sequence
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = [GZIPPED_BODY]
        mock_resp.__enter__.return_value = mock_resp
        mock_get.return_value = mock_resp

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / f"trace-{SAMPLE_TRACE_ID}.json.gz"
            self._service.export(
                mcon=SAMPLE_MCON,
                trace_id=SAMPLE_TRACE_ID,
                output=str(output),
                timeout_seconds=10,
                poll_interval_seconds=0,
            )

            # File written, non-empty, contents match what we streamed
            self.assertTrue(output.exists())
            self.assertEqual(output.read_bytes(), GZIPPED_BODY)

        mock_get.assert_called_once_with(SAMPLE_URL, stream=True)
        self.assertEqual(self._request_wrapper.make_request_v2.call_count, 2)

    @patch("montecarlodata.agent_traces.export_service.click.echo")
    def test_polls_until_done(self, _echo):
        # 3 polls before DONE
        self._set_responses(
            _mutation_response(),
            _status_response("PENDING"),
            _status_response("RUNNING"),
            _status_response("DONE", url=SAMPLE_URL),
        )

        with patch("montecarlodata.agent_traces.export_service.requests.get") as mock_get:
            mock_resp = MagicMock()
            mock_resp.iter_content.return_value = [GZIPPED_BODY]
            mock_resp.__enter__.return_value = mock_resp
            mock_get.return_value = mock_resp

            with tempfile.TemporaryDirectory() as tmpdir:
                self._service.export(
                    mcon=SAMPLE_MCON,
                    trace_id=SAMPLE_TRACE_ID,
                    output=str(Path(tmpdir) / "out.gz"),
                    timeout_seconds=10,
                    poll_interval_seconds=0,
                )

        # 1 mutation + 3 status calls
        self.assertEqual(self._request_wrapper.make_request_v2.call_count, 4)

    @patch("montecarlodata.agent_traces.export_service.click.echo")
    def test_failed_status_aborts(self, _echo):
        self._set_responses(
            _mutation_response(),
            _status_response("FAILED", error="Trace not found"),
        )

        with self.assertRaises(click.Abort):
            self._service.export(
                mcon=SAMPLE_MCON,
                trace_id=SAMPLE_TRACE_ID,
                timeout_seconds=10,
                poll_interval_seconds=0,
            )

    @patch("montecarlodata.agent_traces.export_service.requests.get")
    @patch("montecarlodata.agent_traces.export_service.click.echo")
    def test_done_partial_downloads_then_returns_false_with_warning(self, mock_echo, mock_get):
        """DONE_PARTIAL is terminal — the artifact is downloaded just like
        DONE, but the service emits a loud stderr warning and returns False
        so the command layer exits 2. Downstream tooling (Agent Preflight,
        shell pipelines) can detect that the export is unusable as complete
        golden data."""
        partial_reason = (
            "1 span(s) dropped at single-span payload limit; "
            "88 additional span(s) not fetched after abort"
        )
        self._set_responses(
            _mutation_response(),
            _status_response("DONE_PARTIAL", url=SAMPLE_URL, error=partial_reason),
        )
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = [GZIPPED_BODY]
        mock_resp.__enter__.return_value = mock_resp
        mock_get.return_value = mock_resp

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / f"trace-{SAMPLE_TRACE_ID}.json.gz"
            completed = self._service.export(
                mcon=SAMPLE_MCON,
                trace_id=SAMPLE_TRACE_ID,
                output=str(output),
                timeout_seconds=10,
                poll_interval_seconds=0,
            )

            # Artifact still downloaded — partial data has debug value.
            self.assertTrue(output.exists())
            self.assertEqual(output.read_bytes(), GZIPPED_BODY)

        # Returns False → command layer translates to Exit(2).
        self.assertFalse(completed)

        # Warning surfaced to stderr (err=True), carrying the structured
        # reason verbatim so users can copy/paste.
        warning_calls = [
            call for call in mock_echo.call_args_list if call.kwargs.get("err") is True
        ]
        self.assertTrue(
            any(
                "PARTIAL" in str(c.args[0]) and partial_reason in str(c.args[0])
                for c in warning_calls
            ),
            f"Expected PARTIAL warning with reason on stderr; got: {warning_calls}",
        )

    @patch("montecarlodata.agent_traces.export_service.requests.get")
    @patch("montecarlodata.agent_traces.export_service.click.echo")
    @patch("montecarlodata.agent_traces.export_service.time.sleep")
    def test_poll_tolerates_transient_errors_then_succeeds(self, _sleep, mock_echo, mock_get):
        """A streak of poll errors shorter than the threshold should be
        absorbed — the loop logs a retry message, continues, and reaches
        DONE normally. Validates the resilience fix for the previously-
        observed CLI bug where a single 'Request timed out' GraphQL
        error from the gateway killed the export tracking even though
        the server-side job was running fine."""
        self._set_responses(
            _mutation_response(),
            _error_response("Request timed out"),
            _error_response("Request timed out"),
            _status_response("RUNNING"),
            _error_response("502 Bad Gateway"),
            _status_response("DONE", url=SAMPLE_URL),
        )
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = [GZIPPED_BODY]
        mock_resp.__enter__.return_value = mock_resp
        mock_get.return_value = mock_resp

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / f"trace-{SAMPLE_TRACE_ID}.json.gz"
            completed = self._service.export(
                mcon=SAMPLE_MCON,
                trace_id=SAMPLE_TRACE_ID,
                output=str(output),
                timeout_seconds=60,
                poll_interval_seconds=0,
            )

        # Reached DONE despite the error streaks.
        self.assertTrue(completed)
        # 1 mutation + 5 poll attempts (3 errors + 2 successes).
        self.assertEqual(self._request_wrapper.make_request_v2.call_count, 6)

        # Each transient error logged a "Poll failed (...) retrying" message
        # to stderr; the counter reset on the RUNNING success, so the second
        # error starts fresh at 1/5 not 3/5.
        retry_messages = [
            str(c.args[0])
            for c in mock_echo.call_args_list
            if c.kwargs.get("err") is True and "Poll failed" in str(c.args[0])
        ]
        self.assertEqual(len(retry_messages), 3)
        self.assertIn("1/5", retry_messages[0])  # first error
        self.assertIn("2/5", retry_messages[1])  # second consecutive
        # Third error comes after a successful RUNNING poll, so the counter
        # reset; this error is again 1/5 not 3/5.
        self.assertIn("1/5", retry_messages[2])

    @patch("montecarlodata.agent_traces.export_service.click.echo")
    @patch("montecarlodata.agent_traces.export_service.time.sleep")
    def test_poll_aborts_after_max_consecutive_errors(self, _sleep, mock_echo):
        """Five consecutive poll errors (the threshold) without a successful
        poll in between triggers complain_and_abort. The user gets a clear
        lost-contact message naming the job_id so they can investigate."""
        self._set_responses(
            _mutation_response(),
            *([_error_response("Request timed out")] * 5),
        )

        with self.assertRaises(click.Abort):
            self._service.export(
                mcon=SAMPLE_MCON,
                trace_id=SAMPLE_TRACE_ID,
                timeout_seconds=60,
                poll_interval_seconds=0,
            )

        # Abort message names the job_id and the last error summary.
        abort_messages = [
            str(c.args[0])
            for c in mock_echo.call_args_list
            if c.kwargs.get("err") is True and "Lost contact" in str(c.args[0])
        ]
        self.assertEqual(len(abort_messages), 1)
        self.assertIn(SAMPLE_JOB_ID, abort_messages[0])
        self.assertIn("Request timed out", abort_messages[0])

    @patch("montecarlodata.agent_traces.export_service.click.echo")
    def test_timeout_returns_false(self, _echo):
        # Mutation responds, then status returns RUNNING repeatedly. Service
        # returns False on timeout — the Click command function translates
        # that into Exit(2) at the command layer (see test_command_exits_2_on_timeout).
        # Exit raised inside @manage_errors would be swallowed and re-raised
        # as Abort; the return-then-Exit pattern matches run_validations in
        # collector/commands.py.
        self._set_responses(
            _mutation_response(),
            _status_response("RUNNING"),
            _status_response("RUNNING"),
            _status_response("RUNNING"),
        )

        completed = self._service.export(
            mcon=SAMPLE_MCON,
            trace_id=SAMPLE_TRACE_ID,
            timeout_seconds=0,  # immediate timeout
            poll_interval_seconds=0,
        )

        self.assertFalse(completed)


class AgentTraceExportCommandTest(TestCase):
    """Command-layer tests: verify the Click command translates the service's
    return value into the right exit code. Uses Click's CliRunner so we exercise
    the @click.pass_obj + Exit(2) wiring end-to-end."""

    def _run(self, mock_service_export_return: bool) -> "click.testing.Result":
        from click.testing import CliRunner

        from montecarlodata.agent_traces.commands import agent_traces

        runner = CliRunner()
        with patch(
            "montecarlodata.agent_traces.commands.AgentTraceExportService"
        ) as mock_service_cls:
            mock_service_cls.return_value.export.return_value = mock_service_export_return
            return runner.invoke(
                agent_traces,
                [
                    "export",
                    "--trace-link",
                    SAMPLE_TRACE_LINK,
                    "--timeout",
                    "0",
                    "--poll-interval",
                    "0",
                ],
                obj={"config": _SAMPLE_CONFIG},
            )

    def test_command_exits_0_on_success(self):
        result = self._run(mock_service_export_return=True)
        self.assertEqual(result.exit_code, 0, msg=result.output)

    def test_command_exits_2_on_incomplete(self):
        # service.export returns False for two distinct cases: timeout
        # (poll loop deadline hit) and DONE_PARTIAL (terminal but artifact
        # incomplete). Both translate to Exit(2). Translating
        # service-returns-False into Exit(2) is the whole reason we don't
        # raise Exit inside the @manage_errors-decorated service method.
        # Pin the contract here.
        result = self._run(mock_service_export_return=False)
        self.assertEqual(result.exit_code, 2, msg=result.output)


class ParseTraceLinkTest(TestCase):
    """Tests for parsing the UI's trace-page URL into (mcon, trace_id)."""

    def test_canonical_prod_url(self):
        from montecarlodata.agent_traces.export_service import parse_trace_link

        link = (
            f"https://app.getmontecarlo.com/agents/{SAMPLE_MCON}/ai-agent/traces/{SAMPLE_TRACE_ID}"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))

    def test_url_with_query_string(self):
        """Trace URLs from the UI carry traceStartTime/traceEndTime/etc. in
        the query string. Those should be ignored — only the path matters."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        link = (
            f"https://app.getmontecarlo.com/agents/{SAMPLE_MCON}"
            f"/ai-agent/traces/{SAMPLE_TRACE_ID}"
            "?traceStartTime=2026-05-21T23%3A38%3A26.189312%2B00%3A00"
            "&traceEndTime=2026-05-21T23%3A48%3A31.421613%2B00%3A00"
            "&conversationId=c008354b-4551-433d-9b2f-77cbbad46661"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))

    def test_local_dev_url_with_port(self):
        """Local dev URLs (https://local.getmontecarlo.com:3000/...) should
        parse the same way as prod — only the path matters."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        link = (
            f"https://local.getmontecarlo.com:3000/agents/{SAMPLE_MCON}"
            f"/ai-agent/traces/{SAMPLE_TRACE_ID}"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))

    def test_trailing_slash_tolerated(self):
        from montecarlodata.agent_traces.export_service import parse_trace_link

        link = (
            f"https://app.getmontecarlo.com/agents/{SAMPLE_MCON}/ai-agent/traces/{SAMPLE_TRACE_ID}/"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))

    def test_percent_encoded_mcon_is_decoded_before_match(self):
        """A user copying from some browsers may paste an address-bar URL
        where '+' and ':' in the MCON are percent-encoded. unquote() the
        path before regex matching so encoded and decoded forms both work."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        # Same MCON as SAMPLE_MCON but with `+` encoded as `%2B` and `:` as `%3A`.
        encoded_mcon = SAMPLE_MCON.replace("+", "%2B").replace(":", "%3A")
        link = (
            f"https://app.getmontecarlo.com/agents/{encoded_mcon}/ai-agent/traces/{SAMPLE_TRACE_ID}"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))

    def test_realistic_mcon_with_otel_traces_table_id(self):
        """The MCON's table_id portion can contain colons (e.g.
        'otel_traces:otel_traces.spans_normalized') and dots — neither is
        a path separator so the capture group should grab the whole MCON."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        otel_mcon = (
            "MCON++a5cbd8cc-8e91-4a41-aca4-4bf5bd320578"
            "++c9c40f4c-df08-4e9c-8c93-659179fdf3d7"
            "++table++otel_traces:otel_traces.spans_normalized"
        )
        trace_id = "c8d79870780415bc290612f09950fc5e"
        link = f"https://app.getmontecarlo.com/agents/{otel_mcon}/ai-agent/traces/{trace_id}"
        self.assertEqual(parse_trace_link(link), (otel_mcon, trace_id))

    def test_customer_agent_slug_in_path(self):
        """The path segment between <MCON> and /traces/ is the agent's
        URL-friendly slug, not the literal string "ai-agent". Real customer
        agents have descriptive slugs like "parts-procurement-agent" — the
        regex must accept any alphanumeric+hyphen slug, not just one specific
        name."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        customer_mcon = (
            "MCON++1a371a1e-42a0-4817-8a25-dc1487a7b0d0"
            "++fe164ca3-1b7f-4c77-b1ba-e802c44eba69"
            "++external++awsdatacatalog:mcd-otel-athena-ao-sample-telemetry-db.traces"
        )
        trace_id = "50bb1604927f4e959c30d5fee47d82ce"
        link = (
            f"https://getmontecarlo.com/agents/{customer_mcon}"
            f"/parts-procurement-agent/traces/{trace_id}"
            "?traceStartTime=2026-05-22T00%3A43%3A04.507000%2B00%3A00"
            "&conversationId=7fd47e8c-8ca6-488c-a5f9-91ffc0708992"
        )
        self.assertEqual(parse_trace_link(link), (customer_mcon, trace_id))

    def test_agent_slug_with_only_letters(self):
        """Slug needn't contain a hyphen; bare alphanumeric should also match."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        link = (
            f"https://app.getmontecarlo.com/agents/{SAMPLE_MCON}/myagent/traces/{SAMPLE_TRACE_ID}"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))

    def test_wrong_path_shape_raises_with_echoed_input(self):
        """Pasting the wrong URL (e.g. the monitor page) should raise with
        the offending input echoed so the user can see what was wrong."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        bad = "https://app.getmontecarlo.com/monitors/123"
        with self.assertRaises(ValueError) as ctx:
            parse_trace_link(bad)
        self.assertIn(bad, str(ctx.exception))

    def test_bare_string_not_a_url_raises(self):
        from montecarlodata.agent_traces.export_service import parse_trace_link

        with self.assertRaises(ValueError):
            parse_trace_link("not-a-url")

    def test_non_montecarlo_host_raises(self):
        """Host must be `getmontecarlo.com` or a subdomain. Pasting a URL
        from another product (or the wrong tab) should fail with a clear
        message rather than silently sending random values to the API."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        bad = f"https://example.com/agents/{SAMPLE_MCON}/ai-agent/traces/{SAMPLE_TRACE_ID}"
        with self.assertRaises(ValueError) as ctx:
            parse_trace_link(bad)
        self.assertIn("getmontecarlo.com", str(ctx.exception))

    def test_typosquat_host_with_no_dot_separator_raises(self):
        """`evilgetmontecarlo.com` ends with the literal string
        'getmontecarlo.com' but isn't the real apex — the strict subdomain
        check (`.getmontecarlo.com`) rejects it correctly."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        bad = (
            f"https://evilgetmontecarlo.com/agents/{SAMPLE_MCON}/ai-agent/traces/{SAMPLE_TRACE_ID}"
        )
        with self.assertRaises(ValueError):
            parse_trace_link(bad)

    def test_host_validation_is_case_insensitive(self):
        """Browsers may normalize the hostname case on copy. Both forms
        should work."""
        from montecarlodata.agent_traces.export_service import parse_trace_link

        link = (
            f"https://APP.GetMonteCarlo.COM/agents/{SAMPLE_MCON}/ai-agent/traces/{SAMPLE_TRACE_ID}"
        )
        self.assertEqual(parse_trace_link(link), (SAMPLE_MCON, SAMPLE_TRACE_ID))


class AgentTraceExportServicePathResolutionTest(TestCase):
    """Tests for the default-output and path-expansion behavior."""

    def test_default_output_path_uses_trace_id_in_cwd(self):
        path = AgentTraceExportService._resolve_output_path(output=None, trace_id=SAMPLE_TRACE_ID)
        self.assertEqual(path.name, f"trace-{SAMPLE_TRACE_ID}.json.gz")
        self.assertEqual(path.parent, Path.cwd())

    def test_explicit_output_path_is_used_as_given(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "subdir" / "my-export.gz"
            path = AgentTraceExportService._resolve_output_path(
                output=str(target), trace_id=SAMPLE_TRACE_ID
            )
            self.assertEqual(path, target.resolve())

    def test_explicit_output_path_expands_tilde(self):
        path = AgentTraceExportService._resolve_output_path(
            output="~/my-export.gz", trace_id=SAMPLE_TRACE_ID
        )
        # ~ should expand to a real home dir (not literal "~")
        self.assertNotIn("~", str(path))


class AgentTraceExportServiceDownloadTest(TestCase):
    """Tests for the streamed download specifically."""

    @patch("montecarlodata.agent_traces.export_service.requests.get")
    def test_empty_response_aborts(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = []  # empty
        mock_resp.__enter__.return_value = mock_resp
        mock_get.return_value = mock_resp

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "out.gz"
            with self.assertRaises(click.Abort):
                AgentTraceExportService._download_to_path(url=SAMPLE_URL, output_path=output_path)

    @patch("montecarlodata.agent_traces.export_service.requests.get")
    def test_creates_parent_directories(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.iter_content.return_value = [GZIPPED_BODY]
        mock_resp.__enter__.return_value = mock_resp
        mock_get.return_value = mock_resp

        with tempfile.TemporaryDirectory() as tmpdir:
            nested = Path(tmpdir) / "deep" / "nested" / "out.gz"
            self.assertFalse(nested.parent.exists())

            AgentTraceExportService._download_to_path(url=SAMPLE_URL, output_path=nested)

            self.assertTrue(nested.exists())
            self.assertTrue(nested.parent.is_dir())


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
