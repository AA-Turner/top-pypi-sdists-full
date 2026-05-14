"""Tests for feature_files — multi-file feature scaffolding."""

from __future__ import annotations

from sage.core.feature_files import files_for_feature
from sage.core.spec_decomposer import Feature


class TestBackendFeatureFiles:
    def test_produces_full_vertical_slice(self) -> None:
        feat = Feature(
            name="campaign_builder",
            description="Create and manage ad campaigns",
            layer="backend",
            acceptance=["POST /campaigns creates a campaign"],
        )
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        paths = [f.path for f in files]
        # Each layer must be present
        assert any("models/campaign.py" in p for p in paths), paths
        assert any("schemas/campaign.py" in p for p in paths), paths
        assert any("repositories/campaign.py" in p for p in paths), paths
        assert any("services/campaign.py" in p for p in paths), paths
        assert any("api/v1/campaigns.py" in p for p in paths), paths
        # Tests: service + repository + integration
        assert any("test_campaign_service.py" in p for p in paths), paths
        assert any("test_campaign_repository.py" in p for p in paths), paths
        assert any("test_campaigns_api.py" in p for p in paths), paths

    def test_at_least_eight_files_per_backend_feature(self) -> None:
        feat = Feature(name="auth_system", description="Auth", layer="backend", acceptance=[])
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        assert len(files) >= 8, f"only {len(files)} files generated"

    def test_test_files_marked_as_test(self) -> None:
        feat = Feature(name="x", description="x", layer="backend", acceptance=[])
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        test_files = [f for f in files if f.is_test]
        assert len(test_files) >= 3

    def test_adds_celery_task_for_background_features(self) -> None:
        feat = Feature(
            name="campaign_performance_analyzer",
            description="Analyzes campaign results scheduled hourly",
            layer="backend",
            acceptance=["Runs hourly via celery beat"],
        )
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        paths = [f.path for f in files]
        assert any("tasks/" in p for p in paths), paths
        assert any("test_" in p and "tasks" in p for p in paths), paths

    def test_skips_celery_for_pure_crud_features(self) -> None:
        feat = Feature(name="settings", description="User settings CRUD",
                       layer="backend", acceptance=["GET /settings"])
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        paths = [f.path for f in files]
        assert not any("tasks/" in p for p in paths)


class TestFrontendFeatureFiles:
    def test_rnw_feature_produces_12_files(self) -> None:
        feat = Feature(name="user_dashboard", description="Dashboard UI",
                       layer="frontend", acceptance=["Renders KPI cards"])
        files = files_for_feature(feat, frontend="react-native-web", backend="fastapi")
        # 12 = types, api, hooks, store, 3 components, _layout, index, [id], 2 tests
        assert len(files) >= 10, f"only {len(files)} files"

    def test_rnw_feature_has_screens_and_components(self) -> None:
        feat = Feature(name="user_dashboard", description="x",
                       layer="frontend", acceptance=[])
        files = files_for_feature(feat, frontend="react-native-web", backend=None)
        paths = [f.path for f in files]
        assert any("app/(tabs)/" in p and "index.tsx" in p for p in paths), paths
        assert any("app/(tabs)/" in p and "[id].tsx" in p for p in paths), paths
        assert any("Card.tsx" in p for p in paths), paths
        assert any("List.tsx" in p for p in paths), paths
        assert any("Form.tsx" in p for p in paths), paths

    def test_rnw_feature_has_hook_and_api_and_store(self) -> None:
        feat = Feature(name="campaign_builder", description="x",
                       layer="frontend", acceptance=[])
        files = files_for_feature(feat, frontend="react-native-web", backend=None)
        paths = [f.path for f in files]
        assert any("hooks/useCampaignBuilder.ts" in p or "hooks/useCampaign.ts" in p
                   for p in paths), paths
        assert any(".api.ts" in p for p in paths), paths
        assert any(".store.ts" in p for p in paths), paths

    def test_frontend_files_under_frontend_root(self) -> None:
        feat = Feature(name="x", description="x", layer="frontend", acceptance=[])
        files = files_for_feature(feat, frontend="react-native-web", backend=None)
        for f in files:
            assert f.path.startswith("frontend/"), f.path


class TestPluralization:
    def test_simple_plural(self) -> None:
        feat = Feature(name="campaign", description="x", layer="backend", acceptance=[])
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        api_path = next(f.path for f in files if "/api/v1/" in f.path)
        assert "/api/v1/campaigns.py" in api_path

    def test_y_to_ies(self) -> None:
        feat = Feature(name="entity", description="x", layer="backend", acceptance=[])
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        api_path = next(f.path for f in files if "/api/v1/" in f.path)
        assert "/api/v1/entities.py" in api_path

    def test_s_to_es(self) -> None:
        feat = Feature(name="business", description="x", layer="backend", acceptance=[])
        files = files_for_feature(feat, frontend=None, backend="fastapi")
        api_path = next(f.path for f in files if "/api/v1/" in f.path)
        # business → businesses
        assert "businesses" in api_path
