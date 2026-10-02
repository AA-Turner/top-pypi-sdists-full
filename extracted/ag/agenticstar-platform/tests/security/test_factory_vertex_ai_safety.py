"""Refs #1952: factory.py が vertex_ai_safety を GCP として正しく判別することを検証。"""

import pytest

from agenticstar_platform.security.base import (
    GCPSecurityConfig,
    SecurityConfigError,
    SecurityProvider,
)
from agenticstar_platform.security.factory import (
    _create_gcp_client,
    detect_provider,
)


class TestDetectProviderVertexAISafety:
    def test_vertex_ai_safety_is_detected_as_gcp(self):
        config = {
            "service": "vertex_ai_safety",
            "project_id": "test-project",
            "location": "global",
            "judge_model": "gemini-2.5-flash",
        }
        assert detect_provider(config) == SecurityProvider.GCP

    def test_vertex_ai_safety_case_insensitive(self):
        config = {
            "service": "VERTEX_AI_SAFETY",
            "project_id": "test-project",
        }
        assert detect_provider(config) == SecurityProvider.GCP

    def test_model_armor_still_detected_as_gcp(self):
        config = {"service": "model_armor", "project_id": "test-project"}
        assert detect_provider(config) == SecurityProvider.GCP

    def test_dlp_still_detected_as_gcp(self):
        config = {"service": "dlp", "project_id": "test-project"}
        assert detect_provider(config) == SecurityProvider.GCP

    def test_unknown_service_raises(self):
        config = {"service": "some_unknown_service", "project_id": "x"}
        with pytest.raises(SecurityConfigError):
            detect_provider(config)


class TestCreateGCPClientVertexAISafety:
    """_create_gcp_client が vertex_ai_safety 時に GCPSecurityConfig を
    Vertex 経路用に組み立てることを検証。

    実際の GCPSecurityClient 初期化は SecurityConfigError を投げる可能性が
    あるため (google-cloud-dlp が入っていない環境等)、build された config
    のみを検証する目的で GCPSecurityClient.__init__ をパッチする。
    """

    def test_vertex_ai_safety_populates_vertex_fields(self, monkeypatch):
        captured: dict = {}

        class _Stub:
            def __init__(self, cfg: GCPSecurityConfig):
                captured["cfg"] = cfg

        # gcp.py をロードさせずに factory 側の import を差し替える
        monkeypatch.setattr(
            "agenticstar_platform.security.gcp.GCPSecurityClient", _Stub
        )

        config = {
            "service": "vertex_ai_safety",
            "project_id": "mp-global-project",
            "location": "global",
            "judge_model": "gemini-2.5-flash",
            "harm_categories": {
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
                "HARM_CATEGORY_HARASSMENT": "BLOCK_LOW_AND_ABOVE",
            },
        }

        _create_gcp_client(config)

        cfg: GCPSecurityConfig = captured["cfg"]
        assert cfg.content_safety_backend == "vertex_ai_safety"
        assert cfg.project_id == "mp-global-project"
        assert cfg.vertex_ai_location == "global"
        assert cfg.vertex_judge_model == "gemini-2.5-flash"
        assert cfg.vertex_harm_thresholds == {
            "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
            "HARM_CATEGORY_HARASSMENT": "BLOCK_LOW_AND_ABOVE",
        }
        # Vertex 経路では model_armor_region を空文字にしてリージョン制約を持ち込まない
        assert cfg.model_armor_region == ""

    def test_model_armor_populates_model_armor_fields(self, monkeypatch):
        captured: dict = {}

        class _Stub:
            def __init__(self, cfg: GCPSecurityConfig):
                captured["cfg"] = cfg

        monkeypatch.setattr(
            "agenticstar_platform.security.gcp.GCPSecurityClient", _Stub
        )

        config = {
            "service": "model_armor",
            "project_id": "legacy-project",
            "template_name": "projects/x/locations/asia-southeast1/templates/t1",
            "location": "asia-southeast1",
        }

        _create_gcp_client(config)

        cfg: GCPSecurityConfig = captured["cfg"]
        assert cfg.content_safety_backend == "model_armor"
        assert cfg.model_armor_template == "projects/x/locations/asia-southeast1/templates/t1"
        assert cfg.model_armor_region == "asia-southeast1"
        # Model Armor 経路では vertex 系フィールドはデフォルト値のまま
        assert cfg.vertex_harm_thresholds == {}

    def test_non_dict_harm_categories_is_ignored(self, monkeypatch):
        captured: dict = {}

        class _Stub:
            def __init__(self, cfg: GCPSecurityConfig):
                captured["cfg"] = cfg

        monkeypatch.setattr(
            "agenticstar_platform.security.gcp.GCPSecurityClient", _Stub
        )

        config = {
            "service": "vertex_ai_safety",
            "project_id": "p",
            "harm_categories": "not-a-dict",
        }
        _create_gcp_client(config)
        assert captured["cfg"].vertex_harm_thresholds == {}
