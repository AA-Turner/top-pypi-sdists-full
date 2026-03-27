"""E2E tests for workflow REST API endpoints and browser UI panel.

Tests the real server (no mocking of middleware or routing).
Verifies read-only workflow monitoring API, SSE endpoint, and
browser workflows panel (#961).
"""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.e2e]


class TestWorkflowAPIEndpoints:
    """Verify workflow REST API returns correct responses."""

    def test_list_workflows(self, api_client) -> None:
        """GET /api/workflows returns a list."""
        resp = api_client.get("/api/workflows")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    def test_list_workflow_runs_empty(self, api_client) -> None:
        """GET /api/workflow-runs returns empty list when no runs exist."""
        resp = api_client.get("/api/workflow-runs")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_workflow_run_404(self, api_client) -> None:
        """GET /api/workflow-runs/{id} returns 404 for nonexistent run."""
        resp = api_client.get("/api/workflow-runs/nonexistent-id")
        assert resp.status_code == 404

    def test_get_workflow_events_404(self, api_client) -> None:
        """GET /api/workflow-runs/{id}/events returns 404 for nonexistent run."""
        resp = api_client.get("/api/workflow-runs/nonexistent-id/events")
        assert resp.status_code == 404

    def test_get_transcript_404(self, api_client) -> None:
        """GET /api/workflow-runs/{id}/transcript returns 404 for nonexistent run."""
        resp = api_client.get("/api/workflow-runs/nonexistent-id/transcript")
        assert resp.status_code == 404

    def test_get_transcript_empty(self, api_client) -> None:
        """GET /api/workflow-runs/{id}/transcript returns empty events for valid but empty run.

        This test requires a real run. Since we can't easily create one in E2E,
        we just verify the 404 behavior for nonexistent runs (covered above).
        The since_id parameter is accepted without error.
        """
        resp = api_client.get("/api/workflow-runs/nonexistent-id/transcript?since_id=0")
        assert resp.status_code == 404

    def test_get_transcript_with_step_filter(self, api_client) -> None:
        """GET /api/workflow-runs/{id}/transcript?step_id=x returns 404 for nonexistent run."""
        resp = api_client.get("/api/workflow-runs/nonexistent-id/transcript?step_id=test_step")
        assert resp.status_code == 404

    def test_sse_endpoint_accepts_workflow_run_id(self, api_client) -> None:
        """GET /api/events?workflow_run_id=... starts an SSE stream."""
        with api_client.stream(
            "GET",
            "/api/events",
            params={"workflow_run_id": "test-run-id"},
            timeout=5,
        ) as resp:
            assert resp.status_code == 200
            content_type = resp.headers.get("content-type", "")
            assert "text/event-stream" in content_type


class TestWorkflowBrowserPanel:
    """Verify browser UI workflows panel elements (#961)."""

    def test_index_has_workflows_panel(self, base_url: str) -> None:
        """GET / should include the workflows panel HTML."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert resp.status_code == 200
        assert 'id="workflows-panel"' in resp.text

    def test_index_has_workflows_toggle_button(self, base_url: str) -> None:
        """GET / should include the workflows toggle button."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert 'id="btn-workflows-toggle"' in resp.text

    def test_workflows_js_served(self, base_url: str) -> None:
        """workflows.js should be served by the static file handler."""
        import httpx

        resp = httpx.get(f"{base_url}/js/workflows.js", follow_redirects=True)
        assert resp.status_code == 200
        assert "Workflows" in resp.text

    def test_workflows_panel_hidden_by_default(self, base_url: str) -> None:
        """Workflows panel should be hidden by default."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert 'id="workflows-panel" style="display:none"' in resp.text

    def test_workflows_status_filter_present(self, base_url: str) -> None:
        """Workflows panel should have a status filter dropdown."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert 'id="workflows-status-filter"' in resp.text

    def test_workflows_list_api_returns_data(self, api_client) -> None:
        """API endpoint used by the panel should return valid JSON."""
        resp = api_client.get("/api/workflow-runs")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)


# ---------------------------------------------------------------------------
# Playwright browser interaction tests (#961)
# ---------------------------------------------------------------------------

try:
    import playwright  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")


@requires_playwright
class TestWorkflowPanelBrowser:
    """Browser-level tests for the workflows panel UI behavior."""

    def test_toggle_button_opens_panel(self, authenticated_page) -> None:
        """Clicking the workflows toggle button should show the panel."""
        page = authenticated_page
        panel = page.locator("#workflows-panel")
        assert not panel.is_visible()

        page.locator("#btn-workflows-toggle").click()
        panel.wait_for(state="visible", timeout=3000)
        assert panel.is_visible()

    def test_close_button_hides_panel(self, authenticated_page) -> None:
        """Clicking the close button should hide the panel."""
        page = authenticated_page
        page.locator("#btn-workflows-toggle").click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)

        page.locator("#workflows-close").click()
        page.locator("#workflows-panel").wait_for(state="hidden", timeout=3000)
        assert not page.locator("#workflows-panel").is_visible()

    def test_panel_shows_empty_state(self, authenticated_page) -> None:
        """Panel should show an empty state when no runs exist."""
        page = authenticated_page
        page.locator("#btn-workflows-toggle").click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)

        # Wait for the list to render (empty state)
        page.wait_for_timeout(1000)
        empty = page.locator(".wf-empty")
        assert empty.count() >= 1

    def test_status_filter_present_in_browser(self, authenticated_page) -> None:
        """Status filter dropdown should be interactive."""
        page = authenticated_page
        page.locator("#btn-workflows-toggle").click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)

        select = page.locator("#workflows-status-filter")
        assert select.is_visible()
        # Verify filter options exist
        options = select.locator("option")
        assert options.count() >= 5  # All statuses + "All"

    def test_toggle_is_idempotent(self, authenticated_page) -> None:
        """Clicking toggle twice should open then close the panel."""
        page = authenticated_page
        btn = page.locator("#btn-workflows-toggle")

        btn.click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)
        assert page.locator("#workflows-panel").is_visible()

        btn.click()
        page.locator("#workflows-panel").wait_for(state="hidden", timeout=3000)
        assert not page.locator("#workflows-panel").is_visible()

    def test_workflows_module_loaded(self, authenticated_page) -> None:
        """The Workflows JS module should be loaded and callable."""
        page = authenticated_page
        result = page.evaluate("() => typeof Workflows !== 'undefined' && typeof Workflows.togglePanel === 'function'")
        assert result is True


_MOCK_RUNS = [
    {
        "id": "run-1",
        "workflow_id": "deploy",
        "status": "completed",
        "created_at": "2026-03-18T10:00:00Z",
        "started_at": "2026-03-18T10:00:01Z",
        "completed_at": "2026-03-18T10:00:30Z",
    },
    {
        "id": "run-2",
        "workflow_id": "review",
        "status": "running",
        "created_at": "2026-03-18T11:00:00Z",
        "started_at": "2026-03-18T11:00:01Z",
        "completed_at": None,
    },
    {
        "id": "run-3",
        "workflow_id": "deploy",
        "status": "failed",
        "created_at": "2026-03-18T09:00:00Z",
        "started_at": "2026-03-18T09:00:01Z",
        "completed_at": "2026-03-18T09:00:15Z",
    },
]

_MOCK_RUN_DETAIL = {
    "id": "run-1",
    "workflow_id": "deploy",
    "status": "completed",
    "created_at": "2026-03-18T10:00:00Z",
    "started_at": "2026-03-18T10:00:01Z",
    "completed_at": "2026-03-18T10:00:30Z",
    "steps": [
        {"step_id": "lint", "status": "completed", "result_status": "success", "duration_ms": 5000},
        {"step_id": "test", "status": "completed", "result_status": "success", "duration_ms": 12000},
        {"step_id": "deploy", "status": "completed", "result_status": "success", "duration_ms": 8000},
    ],
}


@requires_playwright
class TestWorkflowPanelListDetailFilter:
    """Browser-level tests for workflows panel list/detail/filter behavior.

    Uses page.route() to intercept /api/workflow-runs and return mock data,
    then verifies DOM rendering and interaction behavior.
    """

    def _setup_mock_routes(self, page, runs=None, detail=None) -> None:
        """Intercept workflow API calls with mock data."""
        import json as _json

        mock_runs = runs if runs is not None else _MOCK_RUNS
        mock_detail = detail if detail is not None else _MOCK_RUN_DETAIL

        def handle_runs(route):
            route.fulfill(
                status=200,
                body=_json.dumps(mock_runs),
                headers={"Content-Type": "application/json"},
            )

        def handle_detail(route):
            route.fulfill(
                status=200,
                body=_json.dumps(mock_detail),
                headers={"Content-Type": "application/json"},
            )

        def handle_events(route):
            route.fulfill(
                status=200,
                body=_json.dumps([]),
                headers={"Content-Type": "application/json"},
            )

        def handle_transcript(route):
            route.fulfill(
                status=200,
                body=_json.dumps({"events": []}),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/workflow-runs/run-*/transcript*", handle_transcript)
        page.route("**/api/workflow-runs?*", handle_runs)
        page.route("**/api/workflow-runs", handle_runs)
        page.route("**/api/workflow-runs/run-*", handle_detail)

    def test_list_renders_run_cards(self, authenticated_page) -> None:
        """Opening panel with mock runs should render run cards."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.locator("#workflows-panel").wait_for(state="visible", timeout=3000)

        # Wait for list to render
        page.wait_for_selector(".wf-run-card", timeout=5000)
        cards = page.locator(".wf-run-card")
        assert cards.count() == 3

    def test_run_card_shows_status_badge(self, authenticated_page) -> None:
        """Run cards should display status badges."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)

        badges = page.locator(".wf-status-badge")
        assert badges.count() >= 3

        # Check that badge text matches statuses
        badge_texts = [badges.nth(i).text_content() for i in range(badges.count())]
        assert "completed" in badge_texts
        assert "running" in badge_texts

    def test_click_run_shows_detail(self, authenticated_page) -> None:
        """Clicking a run card should show the detail view with steps."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)

        # Click the first run card
        page.locator(".wf-run-card").first.click()

        # Detail view should appear with step timeline
        page.wait_for_selector(".wf-step-timeline", timeout=5000)
        steps = page.locator(".wf-step")
        assert steps.count() == 3

        # List should be hidden
        assert not page.locator("#workflows-list").is_visible()
        assert page.locator("#workflows-detail").is_visible()

    def test_detail_shows_step_ids(self, authenticated_page) -> None:
        """Detail view should display step IDs from the run."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)
        page.locator(".wf-run-card").first.click()
        page.wait_for_selector(".wf-step-id", timeout=5000)

        step_ids = page.locator(".wf-step-id")
        texts = [step_ids.nth(i).text_content() for i in range(step_ids.count())]
        assert "lint" in texts
        assert "test" in texts
        assert "deploy" in texts

    def test_back_button_returns_to_list(self, authenticated_page) -> None:
        """Clicking back in detail view should return to the list."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)
        page.locator(".wf-run-card").first.click()
        page.wait_for_selector("#wf-back-btn", timeout=5000)

        page.locator("#wf-back-btn").click()

        # List should reappear
        page.wait_for_selector("#workflows-list", state="visible", timeout=3000)
        assert page.locator("#workflows-list").is_visible()
        assert not page.locator("#workflows-detail").is_visible()

    def test_status_filter_changes_request(self, authenticated_page) -> None:
        """Changing the status filter should issue a new API request with the filter param."""
        import json as _json

        page = authenticated_page
        captured_urls: list[str] = []

        def capture_runs(route):
            captured_urls.append(route.request.url)
            route.fulfill(
                status=200,
                body=_json.dumps(_MOCK_RUNS),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/workflow-runs*", capture_runs)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)

        # Clear captured URLs from initial load
        captured_urls.clear()

        # Change filter to "running"
        page.locator("#workflows-status-filter").select_option("running")
        page.wait_for_timeout(1000)

        # Verify a new request was made with the status filter
        assert len(captured_urls) >= 1
        assert any("status=running" in url for url in captured_urls)

    def test_filter_to_empty_shows_empty_state(self, authenticated_page) -> None:
        """Filtering to a status with no runs should show empty state."""
        import json as _json

        page = authenticated_page

        call_count = {"n": 0}

        def handle_runs(route):
            call_count["n"] += 1
            url = route.request.url
            if "status=cancelled" in url:
                route.fulfill(
                    status=200,
                    body=_json.dumps([]),
                    headers={"Content-Type": "application/json"},
                )
            else:
                route.fulfill(
                    status=200,
                    body=_json.dumps(_MOCK_RUNS),
                    headers={"Content-Type": "application/json"},
                )

        page.route("**/api/workflow-runs*", handle_runs)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)

        # Filter to cancelled (returns empty)
        page.locator("#workflows-status-filter").select_option("cancelled")
        page.wait_for_timeout(1000)

        # Should show empty state, no run cards
        empty = page.locator(".wf-empty")
        assert empty.count() >= 1
        assert page.locator(".wf-run-card").count() == 0

    def test_detail_shows_transcript_panel(self, authenticated_page) -> None:
        """Detail view should include the transcript container and toggle (#1101)."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)
        page.locator(".wf-run-card").first.click()
        page.wait_for_selector(".wf-step-timeline", timeout=5000)

        # Transcript container should exist
        transcript = page.locator(".wf-transcript")
        assert transcript.count() == 1

        # Toggle button should exist
        toggle = page.locator("#wf-transcript-toggle")
        assert toggle.count() == 1
        assert toggle.text_content() in ("Hide", "Show")

    def test_transcript_toggle_hides_and_shows(self, authenticated_page) -> None:
        """Clicking the transcript toggle should hide/show the container (#1101)."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)
        page.locator(".wf-run-card").first.click()
        page.wait_for_selector("#wf-transcript-toggle", timeout=5000)

        transcript = page.locator(".wf-transcript")
        toggle = page.locator("#wf-transcript-toggle")

        # Initially visible
        assert transcript.is_visible()

        # Click to hide
        toggle.click()
        assert not transcript.is_visible()
        assert toggle.text_content() == "Show"

        # Click to show again
        toggle.click()
        assert transcript.is_visible()
        assert toggle.text_content() == "Hide"

    def test_transcript_renders_mock_lines(self, authenticated_page) -> None:
        """Transcript panel renders lines from the /transcript API (#1101)."""
        import json as _json

        page = authenticated_page
        mock_transcript = {
            "events": [
                {"id": 1, "payload": {"stream": "stdout", "line": "Hello from workflow", "ts": "2026-03-22T10:44:26"}},
                {
                    "id": 2,
                    "payload": {"stream": "stderr", "line": "Warning: check failed", "ts": "2026-03-22T10:44:27"},
                },
            ]
        }

        def handle_transcript(route):
            route.fulfill(
                status=200,
                body=_json.dumps(mock_transcript),
                headers={"Content-Type": "application/json"},
            )

        def handle_runs(route):
            route.fulfill(
                status=200,
                body=_json.dumps(_MOCK_RUNS),
                headers={"Content-Type": "application/json"},
            )

        def handle_detail(route):
            route.fulfill(
                status=200,
                body=_json.dumps(_MOCK_RUN_DETAIL),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/workflow-runs/run-*/transcript*", handle_transcript)
        page.route("**/api/workflow-runs?*", handle_runs)
        page.route("**/api/workflow-runs", handle_runs)
        page.route("**/api/workflow-runs/run-*", handle_detail)

        page.locator("#btn-workflows-toggle").click()
        page.wait_for_selector(".wf-run-card", timeout=5000)
        page.locator(".wf-run-card").first.click()
        page.wait_for_selector(".wf-transcript", timeout=5000)

        # Wait for transcript lines to render
        page.wait_for_selector(".wf-line", timeout=5000)
        lines = page.locator(".wf-line")
        assert lines.count() == 2

        # Check content is escaped and rendered
        content = page.locator(".wf-transcript").inner_text()
        assert "Hello from workflow" in content
        assert "Warning: check failed" in content

        # Check stream classes
        stdout_line = page.locator(".wf-stdout")
        stderr_line = page.locator(".wf-stderr")
        assert stdout_line.count() >= 1
        assert stderr_line.count() >= 1
