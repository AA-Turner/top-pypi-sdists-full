from agentic_devtools.cli.ci.reconciliation.models import ProviderCapacityObservation, WorkerPermit
from agentic_devtools.cli.ci.reconciliation.views import project_global_metrics


def test_project_global_metrics_reports_capacity(foundation):
    fixture = foundation()
    fixture.state.provider_capacity["github"] = ProviderCapacityObservation(
        "github", fixture.now, fixture.now, 10, 2, 1, "e", complete=True, authorized=True
    )
    view = project_global_metrics(fixture.state)
    assert view.worker_limit == 100
    assert view.provider_capacity_status == {"github": "available"}


def test_project_global_metrics_counts_distinct_active_prs(foundation):
    fixture = foundation()
    permit = WorkerPermit(
        "p", "r", fixture.state.repo, 42, "problem", "batch", "w", "github", "luna", 1, fixture.now, fixture.now
    )
    fixture.state.active_permits["p"] = permit
    assert project_global_metrics(fixture.state).active_pr_count == 1


def test_project_global_metrics_reports_unknown_and_exhausted(foundation):
    fixture = foundation()
    fixture.state.provider_capacity["bad"] = ProviderCapacityObservation(
        "bad", fixture.now, fixture.now, 10, 0, 0, "e", complete=False, authorized=False
    )
    fixture.state.provider_capacity["full"] = ProviderCapacityObservation(
        "full", fixture.now, fixture.now, 1, 1, 0, "e"
    )
    view = project_global_metrics(fixture.state)
    assert view.provider_capacity_status == {"bad": "unknown", "full": "exhausted"}
