"""Tests for architecture_modules — cross-cutting infrastructure files."""

from __future__ import annotations

from sage.core.architecture_modules import architecture_files
from sage.core.spec_decomposer import ProjectPlan, StackProfile


def _plan(**stack_kwargs) -> ProjectPlan:
    return ProjectPlan(title="t", features=[], stack=StackProfile(**stack_kwargs))


class TestFastapiInfra:
    def test_emits_db_layer(self) -> None:
        files = architecture_files(_plan(backend="fastapi", database="postgres"))
        paths = [f.path for f in files]
        assert "backend/app/db/base.py" in paths
        assert "backend/app/db/session.py" in paths
        assert "backend/app/db/seed.py" in paths

    def test_emits_auth_dependencies(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/auth/dependencies.py" in paths
        assert "backend/app/auth/oauth.py" in paths

    def test_emits_middleware_layer(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/middleware/request_id.py" in paths
        assert "backend/app/middleware/rate_limit.py" in paths
        assert "backend/app/middleware/security_headers.py" in paths
        assert "backend/app/middleware/tenant.py" in paths

    def test_emits_exception_layer(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/core/exceptions.py" in paths
        assert "backend/app/core/exception_handlers.py" in paths

    def test_emits_celery_for_queue_stack(self) -> None:
        files = architecture_files(_plan(backend="fastapi", queue="celery"))
        paths = [f.path for f in files]
        assert "backend/app/tasks/celery_app.py" in paths
        assert "backend/app/tasks/beat_schedule.py" in paths
        assert "backend/worker.py" in paths

    def test_emits_alembic_for_postgres(self) -> None:
        files = architecture_files(_plan(backend="fastapi", database="postgres"))
        paths = [f.path for f in files]
        assert "backend/alembic.ini" in paths
        assert "backend/alembic/env.py" in paths

    def test_emits_ai_layer(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/ai/client.py" in paths
        assert "backend/app/ai/prompts.py" in paths
        assert "backend/app/ai/segmentation.py" in paths
        assert "backend/app/ai/scoring.py" in paths

    def test_emits_webhooks_layer(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/webhooks/dispatcher.py" in paths
        assert "backend/app/webhooks/handlers.py" in paths

    def test_emits_health_endpoints(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/api/v1/health.py" in paths

    def test_emits_observability(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "backend/app/observability/metrics.py" in paths

    def test_at_least_15_infra_files(self) -> None:
        files = architecture_files(_plan(backend="fastapi", queue="celery",
                                          database="postgres", cache="redis"))
        # Sanity: a full FastAPI stack needs A LOT of cross-cutting files
        assert len(files) >= 25


class TestRnwInfra:
    def test_emits_shared_layer(self) -> None:
        files = architecture_files(_plan(frontend="react-native-web"))
        paths = [f.path for f in files]
        assert "frontend/src/shared/api.ts" in paths
        assert "frontend/src/shared/queryClient.ts" in paths
        assert "frontend/src/shared/auth.tsx" in paths
        assert "frontend/src/shared/theme.ts" in paths

    def test_emits_ui_kit(self) -> None:
        files = architecture_files(_plan(frontend="react-native-web"))
        paths = [f.path for f in files]
        assert "frontend/src/components/ui/Button.tsx" in paths
        assert "frontend/src/components/ui/TextField.tsx" in paths
        assert "frontend/src/components/ui/EmptyState.tsx" in paths
        assert "frontend/src/components/ui/ErrorBoundary.tsx" in paths

    def test_emits_root_layouts(self) -> None:
        files = architecture_files(_plan(frontend="react-native-web"))
        paths = [f.path for f in files]
        assert "frontend/app/_layout.tsx" in paths
        assert "frontend/app/(auth)/login.tsx" in paths
        assert "frontend/app/(auth)/register.tsx" in paths
        assert "frontend/app/(tabs)/_layout.tsx" in paths


class TestDeployment:
    def test_emits_k8s_manifests(self) -> None:
        files = architecture_files(
            _plan(backend="fastapi", frontend="react-native-web", queue="celery")
        )
        paths = [f.path for f in files]
        assert "deploy/k8s/backend.yaml" in paths
        assert "deploy/k8s/celery.yaml" in paths
        assert "deploy/k8s/frontend.yaml" in paths
        assert "deploy/k8s/ingress.yaml" in paths

    def test_emits_terraform(self) -> None:
        files = architecture_files(_plan(backend="fastapi"))
        paths = [f.path for f in files]
        assert "deploy/terraform/main.tf" in paths
