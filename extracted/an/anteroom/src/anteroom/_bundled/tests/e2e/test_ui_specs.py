"""E2E tests for specs REST API endpoints and browser UI panel.

Tests the real server (no mocking of middleware or routing).
Verifies spec lifecycle API: list, create, show, approve, diff, stale,
dashboard endpoint, and browser Specs panel (#1016).
"""

from __future__ import annotations

import pytest

pytestmark = [pytest.mark.e2e]

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""

VALID_BUGFIX_YAML = """\
mode: bugfix
requirements: |
  Widget crashes on empty input.
design: |
  Missing null check in parser.
tasks:
  - id: t1
    summary: Add null check
"""

INVALID_MODE_YAML = """\
mode: hotfix
requirements: |
  Some requirement.
design: |
  Some design.
tasks:
  - id: t1
    summary: Some task
"""

UPDATED_SPEC_YAML = """\
requirements: |
  Must support widgets AND gadgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


class TestSpecsAPIEndpoints:
    """Verify specs REST API returns correct responses."""

    def test_list_specs_empty(self, api_client) -> None:
        """GET /api/specs returns empty list when no specs exist."""
        resp = api_client.get("/api/specs")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_create_spec(self, api_client) -> None:
        """POST /api/specs creates a new spec artifact."""
        resp = api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "test-spec", "content": VALID_SPEC_YAML},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["fqn"] == "@e2e/spec/test-spec"
        assert data["type"] == "spec"

    def test_list_specs_after_create(self, api_client) -> None:
        """GET /api/specs returns created spec."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "listed", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs")
        assert resp.status_code == 200
        data = resp.json()
        fqns = [s["fqn"] for s in data]
        assert "@e2e/spec/listed" in fqns

    def test_get_spec_detail(self, api_client) -> None:
        """GET /api/specs/{fqn} returns spec with phase info."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "detail", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/@e2e/spec/detail")
        assert resp.status_code == 200
        data = resp.json()
        assert data["fqn"] == "@e2e/spec/detail"
        assert "phase_info" in data
        assert data["phase_info"]["requirements"]["status"] == "draft"

    def test_get_spec_404(self, api_client) -> None:
        """GET /api/specs/{fqn} returns 404 for nonexistent spec."""
        resp = api_client.get("/api/specs/@e2e/spec/nonexistent")
        assert resp.status_code == 404

    def test_approve_phase(self, api_client) -> None:
        """POST /api/specs/{fqn}/phases/{phase}/approve approves a phase."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "approve-test", "content": VALID_SPEC_YAML},
        )
        resp = api_client.post("/api/specs/@e2e/spec/approve-test/phases/design/approve")
        assert resp.status_code == 200
        assert resp.json()["status"] == "approved"

    def test_approve_invalid_phase(self, api_client) -> None:
        """POST .../phases/invalid/approve returns 400."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "bad-phase", "content": VALID_SPEC_YAML},
        )
        resp = api_client.post("/api/specs/@e2e/spec/bad-phase/phases/invalid/approve")
        assert resp.status_code == 400

    def test_stale_endpoint(self, api_client) -> None:
        """GET /api/specs/{fqn}/stale returns phase status."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "stale-test", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/@e2e/spec/stale-test/stale")
        assert resp.status_code == 200
        data = resp.json()
        assert data["phases"]["requirements"]["status"] == "draft"
        assert data["phases"]["requirements"]["reason"] is None

    def test_stale_not_found(self, api_client) -> None:
        """GET /api/specs/{fqn}/stale returns 404 for nonexistent."""
        resp = api_client.get("/api/specs/@e2e/spec/nope/stale")
        assert resp.status_code == 404

    def test_diff_needs_two_versions(self, api_client) -> None:
        """GET /api/specs/{fqn}/diff returns 422 with only one version."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "diff-test", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/@e2e/spec/diff-test/diff")
        assert resp.status_code == 422


class TestSpecsBugfixMode:
    """Verify bugfix mode in specs API."""

    def test_create_bugfix_spec(self, api_client) -> None:
        """POST /api/specs creates a bugfix spec."""
        resp = api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "bug1", "content": VALID_BUGFIX_YAML},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["fqn"] == "@e2e/spec/bug1"

    def test_create_feature_spec_default_mode(self, api_client) -> None:
        """POST /api/specs with no mode field defaults to feature."""
        resp = api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "feat-default", "content": VALID_SPEC_YAML},
        )
        assert resp.status_code == 201

    def test_create_spec_invalid_mode(self, api_client) -> None:
        """POST /api/specs with invalid mode returns 422."""
        resp = api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "bad-mode", "content": INVALID_MODE_YAML},
        )
        assert resp.status_code == 422
        assert "Invalid mode" in resp.json()["detail"]

    def test_list_specs_includes_mode_field(self, api_client) -> None:
        """GET /api/specs includes mode field for each spec."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "mode-list", "content": VALID_BUGFIX_YAML},
        )
        resp = api_client.get("/api/specs")
        assert resp.status_code == 200
        data = resp.json()
        bugfix_specs = [s for s in data if s["fqn"] == "@e2e/spec/mode-list"]
        assert len(bugfix_specs) == 1
        assert bugfix_specs[0]["mode"] == "bugfix"

    def test_get_bugfix_spec_detail(self, api_client) -> None:
        """GET /api/specs/{fqn} includes mode for bugfix spec."""
        api_client.post(
            "/api/specs",
            json={"namespace": "e2e", "name": "bug-detail", "content": VALID_BUGFIX_YAML},
        )
        resp = api_client.get("/api/specs/@e2e/spec/bug-detail")
        assert resp.status_code == 200
        data = resp.json()
        assert data["mode"] == "bugfix"


class TestSpecsDashboardAPI:
    """Verify specs dashboard REST API (#1016)."""

    def test_dashboard_empty(self, api_client) -> None:
        """GET /api/specs/dashboard returns valid structure even with no specs."""
        resp = api_client.get("/api/specs/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        assert "specs" in data
        assert "totals" in data
        assert isinstance(data["specs"], list)
        assert isinstance(data["totals"], dict)

    def test_dashboard_after_create(self, api_client) -> None:
        """Dashboard includes created specs with overall_status and phases."""
        api_client.post(
            "/api/specs",
            json={"namespace": "dash", "name": "s1", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/dashboard")
        assert resp.status_code == 200
        data = resp.json()
        fqns = [s["fqn"] for s in data["specs"]]
        assert "@dash/spec/s1" in fqns
        spec = next(s for s in data["specs"] if s["fqn"] == "@dash/spec/s1")
        assert spec["overall_status"] == "draft"
        assert "phases" in spec
        assert "run_summary" in spec

    def test_dashboard_filter_by_status(self, api_client) -> None:
        """Dashboard filters by overall_status."""
        api_client.post(
            "/api/specs",
            json={"namespace": "dash", "name": "s2", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/dashboard?status=all_approved")
        assert resp.status_code == 200
        data = resp.json()
        for spec in data["specs"]:
            assert spec["overall_status"] == "all_approved"

    def test_dashboard_filter_by_namespace(self, api_client) -> None:
        """Dashboard filters by namespace."""
        api_client.post(
            "/api/specs",
            json={"namespace": "nsfilter", "name": "x", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/dashboard?namespace=nsfilter")
        assert resp.status_code == 200
        data = resp.json()
        for spec in data["specs"]:
            assert "nsfilter" in spec["fqn"]

    def test_dashboard_filter_by_phase(self, api_client) -> None:
        """Dashboard filters by phase and phase_status."""
        api_client.post(
            "/api/specs",
            json={"namespace": "phase", "name": "pf1", "content": VALID_SPEC_YAML},
        )
        resp = api_client.get("/api/specs/dashboard?phase=requirements&phase_status=draft")
        assert resp.status_code == 200
        data = resp.json()
        for spec in data["specs"]:
            assert spec["phases"].get("requirements") == "draft"

    def test_dashboard_totals(self, api_client) -> None:
        """Dashboard totals reflect spec counts."""
        resp = api_client.get("/api/specs/dashboard")
        assert resp.status_code == 200
        totals = resp.json()["totals"]
        assert "total_specs" in totals
        assert totals["total_specs"] >= 0

    def test_dashboard_has_runs_filter(self, api_client) -> None:
        """Dashboard has_runs=true returns only specs with workflow runs."""
        resp = api_client.get("/api/specs/dashboard?has_runs=true")
        assert resp.status_code == 200
        data = resp.json()
        for spec in data["specs"]:
            assert spec["run_summary"]["total"] > 0

    def test_dashboard_filters_applied_echo(self, api_client) -> None:
        """Dashboard echoes back applied filters."""
        resp = api_client.get("/api/specs/dashboard?status=draft&namespace=test")
        assert resp.status_code == 200
        data = resp.json()
        assert data["filters_applied"]["status"] == "draft"
        assert data["filters_applied"]["namespace"] == "test"


class TestSpecsBrowserPanel:
    """Verify browser UI specs panel elements (#1016)."""

    def test_index_has_specs_panel(self, base_url: str) -> None:
        """GET / should include the specs panel HTML."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert resp.status_code == 200
        assert 'id="specs-panel"' in resp.text

    def test_index_has_specs_toggle_button(self, base_url: str) -> None:
        """GET / should include the specs toggle button."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert 'id="btn-specs-toggle"' in resp.text

    def test_specs_js_served(self, base_url: str) -> None:
        """specs.js should be served by the static file handler."""
        import httpx

        resp = httpx.get(f"{base_url}/js/specs.js", follow_redirects=True)
        assert resp.status_code == 200
        assert "Specs" in resp.text

    def test_specs_panel_hidden_by_default(self, base_url: str) -> None:
        """Specs panel should be hidden by default."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert 'id="specs-panel"' in resp.text
        assert 'style="display:none"' in resp.text.split('id="specs-panel"')[1][:50]

    def test_specs_filter_controls_present(self, base_url: str) -> None:
        """Specs panel should have all filter controls."""
        import httpx

        resp = httpx.get(f"{base_url}/", follow_redirects=True)
        assert 'id="specs-filter-status"' in resp.text
        assert 'id="specs-filter-phase"' in resp.text
        assert 'id="specs-filter-phase-status"' in resp.text
        assert 'id="specs-filter-namespace"' in resp.text
        assert 'id="specs-filter-has-runs"' in resp.text


try:
    import playwright  # noqa: F401

    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False

requires_playwright = pytest.mark.skipif(not HAS_PLAYWRIGHT, reason="playwright not installed")


@requires_playwright
class TestSpecsPanelBrowser:
    """Browser-level tests for the specs panel UI behavior (#1016)."""

    _MOCK_DASHBOARD = {
        "specs": [
            {
                "fqn": "@test/spec/widget",
                "mode": "feature",
                "source": "local",
                "phases": {"requirements": "approved", "design": "approved", "tasks": "approved"},
                "overall_status": "all_approved",
                "stale_reasons": {},
                "run_summary": {"total": 2, "completed": 2, "failed": 0, "running": 0, "blocked": 0},
                "conformant": None,
                "updated_at": "2026-03-20T10:00:00Z",
            },
            {
                "fqn": "@test/spec/gadget",
                "mode": "feature",
                "source": "local",
                "phases": {"requirements": "approved", "design": "draft", "tasks": "draft"},
                "overall_status": "in_progress",
                "stale_reasons": {},
                "run_summary": {"total": 0, "completed": 0, "failed": 0, "running": 0, "blocked": 0},
                "conformant": None,
                "updated_at": "2026-03-19T10:00:00Z",
            },
            {
                "fqn": "@test/spec/broken",
                "mode": "bugfix",
                "source": "local",
                "phases": {"requirements": "stale", "design": "draft", "tasks": "draft"},
                "overall_status": "stale",
                "stale_reasons": {"requirements": "upstream changed"},
                "run_summary": {"total": 1, "completed": 0, "failed": 1, "running": 0, "blocked": 0},
                "conformant": None,
                "updated_at": "2026-03-18T10:00:00Z",
            },
        ],
        "totals": {
            "total_specs": 3,
            "all_approved": 1,
            "in_progress": 1,
            "stale": 1,
            "blocked": 0,
            "draft": 0,
        },
        "filters_applied": {},
    }

    _MOCK_SPEC_DETAIL = {
        "fqn": "@test/spec/widget",
        "type": "spec",
        "mode": "feature",
        "version": 3,
        "phase_info": {
            "requirements": {"status": "approved", "reason": None},
            "design": {"status": "approved", "reason": None},
            "tasks": {"status": "approved", "reason": None},
        },
    }

    def _setup_mock_routes(self, page, dashboard=None, detail=None) -> None:
        """Intercept specs API calls with mock data."""
        import json as _json

        mock_dashboard = dashboard if dashboard is not None else self._MOCK_DASHBOARD
        mock_detail = detail if detail is not None else self._MOCK_SPEC_DETAIL

        def handle_dashboard(route):
            route.fulfill(
                status=200,
                body=_json.dumps(mock_dashboard),
                headers={"Content-Type": "application/json"},
            )

        def handle_detail(route):
            route.fulfill(
                status=200,
                body=_json.dumps(mock_detail),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", handle_dashboard)
        page.route("**/api/specs/@*", handle_detail)

    def test_toggle_button_opens_panel(self, authenticated_page) -> None:
        """Clicking the specs toggle button should show the panel."""
        page = authenticated_page
        panel = page.locator("#specs-panel")
        assert not panel.is_visible()

        page.locator("#btn-specs-toggle").click()
        panel.wait_for(state="visible", timeout=3000)
        assert panel.is_visible()

    def test_close_button_hides_panel(self, authenticated_page) -> None:
        """Clicking the close button should hide the panel."""
        page = authenticated_page
        page.locator("#btn-specs-toggle").click()
        page.locator("#specs-panel").wait_for(state="visible", timeout=3000)

        page.locator("#btn-specs-close").click()
        page.locator("#specs-panel").wait_for(state="hidden", timeout=3000)
        assert not page.locator("#specs-panel").is_visible()

    def test_panel_shows_empty_state(self, authenticated_page) -> None:
        """Panel should show empty state when no specs exist."""
        import json as _json

        page = authenticated_page
        empty_dashboard = {
            "specs": [],
            "totals": {
                "total_specs": 0,
                "all_approved": 0,
                "in_progress": 0,
                "stale": 0,
                "blocked": 0,
                "draft": 0,
            },
            "filters_applied": {},
        }

        def handle_dashboard(route):
            route.fulfill(status=200, body=_json.dumps(empty_dashboard), headers={"Content-Type": "application/json"})

        page.route("**/api/specs/dashboard*", handle_dashboard)
        page.locator("#btn-specs-toggle").click()
        page.locator("#specs-panel").wait_for(state="visible", timeout=3000)
        page.wait_for_timeout(1000)

        empty = page.locator(".specs-empty")
        assert empty.count() >= 1

    def test_list_renders_spec_cards(self, authenticated_page) -> None:
        """Opening panel with mock specs should render spec cards."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-specs-toggle").click()
        page.locator("#specs-panel").wait_for(state="visible", timeout=3000)
        page.wait_for_selector(".spec-card", timeout=5000)

        cards = page.locator(".spec-card")
        assert cards.count() == 3

    def test_spec_card_shows_status_badge(self, authenticated_page) -> None:
        """Spec cards should display status badges."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)

        badges = page.locator(".spec-status-badge")
        assert badges.count() == 3
        badge_texts = [badges.nth(i).text_content() for i in range(badges.count())]
        assert "all_approved" in badge_texts
        assert "in_progress" in badge_texts
        assert "stale" in badge_texts

    def test_click_spec_shows_detail(self, authenticated_page) -> None:
        """Clicking a spec card should show the detail view."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)
        page.locator(".spec-card").first.click()

        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)
        assert page.locator("#specs-detail").is_visible()
        assert not page.locator("#specs-list-items").is_visible()

    def test_back_button_returns_to_list(self, authenticated_page) -> None:
        """Clicking back in detail view should return to the list."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)
        page.locator(".spec-card").first.click()
        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)

        page.locator("#specs-detail-back").click()
        page.locator("#specs-list-items").wait_for(state="visible", timeout=3000)
        assert page.locator("#specs-list-items").is_visible()
        assert not page.locator("#specs-detail").is_visible()

    def test_status_filter_changes_request(self, authenticated_page) -> None:
        """Changing the status filter should issue a new API request with the filter param."""
        import json as _json

        page = authenticated_page
        captured_urls: list[str] = []

        def capture_dashboard(route):
            captured_urls.append(route.request.url)
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_DASHBOARD),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", capture_dashboard)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)
        captured_urls.clear()

        page.locator("#specs-filter-status").select_option("stale")
        page.wait_for_timeout(1000)

        assert len(captured_urls) >= 1
        assert any("status=stale" in url for url in captured_urls)

    def test_phase_filter_changes_request(self, authenticated_page) -> None:
        """Changing the phase filter should issue a new API request with phase params."""
        import json as _json

        page = authenticated_page
        captured_urls: list[str] = []

        def capture_dashboard(route):
            captured_urls.append(route.request.url)
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_DASHBOARD),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", capture_dashboard)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)
        captured_urls.clear()

        page.locator("#specs-filter-phase").select_option("design")
        page.wait_for_timeout(1000)

        assert len(captured_urls) >= 1
        assert any("phase=design" in url for url in captured_urls)

    def test_has_runs_filter_changes_request(self, authenticated_page) -> None:
        """Checking the has_runs checkbox should issue a request with has_runs=true."""
        import json as _json

        page = authenticated_page
        captured_urls: list[str] = []

        def capture_dashboard(route):
            captured_urls.append(route.request.url)
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_DASHBOARD),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", capture_dashboard)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)
        captured_urls.clear()

        page.locator("#specs-filter-has-runs").check()
        page.wait_for_timeout(1000)

        assert len(captured_urls) >= 1
        assert any("has_runs=true" in url for url in captured_urls)

    def test_totals_bar_rendered(self, authenticated_page) -> None:
        """Totals summary bar should render spec counts."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".specs-totals", timeout=5000)

        totals_text = page.locator(".specs-totals").text_content()
        assert "3 specs" in totals_text

    def test_specs_module_loaded(self, authenticated_page) -> None:
        """The Specs JS module should be loaded and callable."""
        page = authenticated_page
        result = page.evaluate("() => typeof Specs !== 'undefined' && typeof Specs.togglePanel === 'function'")
        assert result is True

    def test_detail_view_survives_auto_refresh(self, authenticated_page) -> None:
        """Auto-refresh should not clobber the detail view back to list.

        Patches setInterval to use 500ms instead of 30s, then clicks into
        detail and waits for the timer to fire. Detail must stay visible.
        """
        import json as _json

        page = authenticated_page

        def handle_dashboard(route):
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_DASHBOARD),
                headers={"Content-Type": "application/json"},
            )

        def handle_detail(route):
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_SPEC_DETAIL),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", handle_dashboard)
        page.route("**/api/specs/@*", handle_detail)

        # Patch setInterval before opening panel so the 30s timer becomes 500ms
        page.evaluate("""() => {
            const orig = window.setInterval;
            window.setInterval = (fn, ms, ...args) => {
                return orig(fn, ms === 30000 ? 500 : ms, ...args);
            };
        }""")

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)

        # Click into detail view
        page.locator(".spec-card").first.click()
        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)

        # Wait for at least two auto-refresh cycles (500ms each)
        page.wait_for_timeout(1500)

        # Detail view should still be visible, NOT switched back to list
        assert page.locator("#specs-detail").is_visible()
        assert not page.locator("#specs-list-items").is_visible()

    def test_detail_to_list_to_detail_no_stale_state(self, authenticated_page) -> None:
        """Switching between list and detail repeatedly should not leak state."""
        page = authenticated_page
        self._setup_mock_routes(page)

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)

        # Click into detail
        page.locator(".spec-card").first.click()
        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)
        assert page.locator("#specs-detail").is_visible()

        # Go back to list
        page.locator("#specs-detail-back").click()
        page.locator("#specs-list-items").wait_for(state="visible", timeout=3000)
        assert page.locator("#specs-list-items").is_visible()
        assert not page.locator("#specs-detail").is_visible()

        # Click into detail again (different card)
        cards = page.locator(".spec-card")
        if cards.count() > 1:
            cards.nth(1).click()
        else:
            cards.first.click()
        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)
        assert page.locator("#specs-detail").is_visible()

        # Back again
        page.locator("#specs-detail-back").click()
        page.locator("#specs-list-items").wait_for(state="visible", timeout=3000)
        assert page.locator("#specs-list-items").is_visible()

    def test_filter_change_returns_to_list_and_stays(self, authenticated_page) -> None:
        """Changing a filter while in detail view should return to list,
        and the next auto-refresh tick must NOT jump back to detail.

        Patches setInterval to 500ms so we can wait through a tick after
        the filter change.
        """
        import json as _json

        page = authenticated_page

        def handle_dashboard(route):
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_DASHBOARD),
                headers={"Content-Type": "application/json"},
            )

        def handle_detail(route):
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_SPEC_DETAIL),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", handle_dashboard)
        page.route("**/api/specs/@*", handle_detail)

        # Shorten auto-refresh to 500ms
        page.evaluate("""() => {
            const orig = window.setInterval;
            window.setInterval = (fn, ms, ...args) => {
                return orig(fn, ms === 30000 ? 500 : ms, ...args);
            };
        }""")

        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)

        # Click into detail
        page.locator(".spec-card").first.click()
        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)

        # Change a filter — this is a manual refresh, should go to list
        page.locator("#specs-filter-status").select_option("stale")
        page.wait_for_timeout(1000)

        # Should be back on list view
        assert page.locator("#specs-list-items").is_visible()
        assert not page.locator("#specs-detail").is_visible()

        # Wait through 2+ auto-refresh ticks — must stay on list, not jump to detail
        page.wait_for_timeout(1500)
        assert page.locator("#specs-list-items").is_visible()
        assert not page.locator("#specs-detail").is_visible()

    def test_close_and_reopen_clears_stale_detail(self, authenticated_page) -> None:
        """Closing panel while in detail, then reopening, must not jump to old detail.

        Patches setInterval to 500ms and waits through a tick after reopen.
        """
        import json as _json

        page = authenticated_page

        def handle_dashboard(route):
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_DASHBOARD),
                headers={"Content-Type": "application/json"},
            )

        def handle_detail(route):
            route.fulfill(
                status=200,
                body=_json.dumps(self._MOCK_SPEC_DETAIL),
                headers={"Content-Type": "application/json"},
            )

        page.route("**/api/specs/dashboard*", handle_dashboard)
        page.route("**/api/specs/@*", handle_detail)

        # Shorten auto-refresh to 500ms
        page.evaluate("""() => {
            const orig = window.setInterval;
            window.setInterval = (fn, ms, ...args) => {
                return orig(fn, ms === 30000 ? 500 : ms, ...args);
            };
        }""")

        # Open and click into detail
        page.locator("#btn-specs-toggle").click()
        page.wait_for_selector(".spec-card", timeout=5000)
        page.locator(".spec-card").first.click()
        page.locator("#specs-detail").wait_for(state="visible", timeout=5000)

        # Close panel while detail is showing
        page.locator("#btn-specs-close").click()
        page.locator("#specs-panel").wait_for(state="hidden", timeout=3000)

        # Reopen — should show list, not old detail
        page.locator("#btn-specs-toggle").click()
        page.locator("#specs-panel").wait_for(state="visible", timeout=3000)
        page.wait_for_selector(".spec-card", timeout=5000)

        cards = page.locator(".spec-card")
        assert cards.count() == 3
        assert page.locator("#specs-list-items").is_visible()

        # Wait through 2+ auto-refresh ticks — must stay on list
        page.wait_for_timeout(1500)
        assert page.locator("#specs-list-items").is_visible()
        assert not page.locator("#specs-detail").is_visible()

    def test_toggle_is_idempotent(self, authenticated_page) -> None:
        """Clicking toggle twice should open then close the panel."""
        page = authenticated_page
        btn = page.locator("#btn-specs-toggle")

        btn.click()
        page.locator("#specs-panel").wait_for(state="visible", timeout=3000)
        assert page.locator("#specs-panel").is_visible()

        btn.click()
        page.locator("#specs-panel").wait_for(state="hidden", timeout=3000)
        assert not page.locator("#specs-panel").is_visible()
