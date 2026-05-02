"""Integration tests for PlanogramCompliance FEAT-009 — TASK-026.

Verifies:
1. parrot_pipelines.models is directly importable (no proxy needed).
2. parrot_pipelines.planogram.plan.PlanogramCompliance is loadable.
3. get_planogram_config() called before start() does not raise AttributeError.
"""
import sys
import types
import importlib.util
import pytest
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock

WORKTREE = Path(__file__).parent.parent
COMPONENT_FILE = WORKTREE / 'flowtask' / 'components' / 'PlanogramCompliance.py'

FAKE_DB_ROW = {
    'planogram_id': 1,
    'aspect_ratio': 1.35,
    'left_margin_ratio': 0.01,
    'right_margin_ratio': 0.03,
    'top_margin_ratio': 0.02,
    'bottom_margin_ratio': 0.05,
    'inter_shelf_padding': 0.02,
    'width_margin_percent': 0.25,
    'height_margin_percent': 0.30,
    'top_margin_percent': 0.05,
    'side_margin_percent': 0.05,
    'planogram_config': {'brand': 'Epson', 'shelves': []},
    'roi_detection_prompt': 'Find the endcap.',
    'object_identification_prompt': 'Identify products.',
    'confidence_threshold': 0.20,
    'detection_model': 'yolo11l.pt',
    'planogram_type': 'product_on_shelves',
}


def _load_component():
    """Load PlanogramCompliance with real parrot/* and mocked flowtask chain only."""

    class ComponentError(Exception):
        pass

    class ConfigError(Exception):
        pass

    class _FlowComponent:
        def __init__(self, *a, **kw):
            pass

    class _AIPipeline:
        def __init__(self, *a, **kw):
            pass

    exc_mod = types.ModuleType('flowtask.exceptions')
    exc_mod.ComponentError = ComponentError
    exc_mod.ConfigError = ConfigError

    flow_mod = types.ModuleType('flowtask.components.flow')
    flow_mod.FlowComponent = _FlowComponent

    aipipeline_mod = types.ModuleType('flowtask.interfaces.pipelines.parrot')
    aipipeline_mod.AIPipeline = _AIPipeline

    mock_asyncdb_cls = MagicMock()
    asyncdb_mod = types.ModuleType('asyncdb')
    asyncdb_mod.AsyncDB = mock_asyncdb_cls

    qs_mod = types.ModuleType('querysource')
    qs_conf = types.ModuleType('querysource.conf')
    qs_conf.default_dsn = 'postgresql://localhost/test'

    # Only mock flowtask internals and asyncdb — let real parrot.* load
    injected = {
        'flowtask.exceptions': exc_mod,
        'flowtask.components.flow': flow_mod,
        'flowtask.interfaces.pipelines.parrot': aipipeline_mod,
        'asyncdb': asyncdb_mod,
        'querysource': qs_mod,
        'querysource.conf': qs_conf,
    }

    to_restore = {k: sys.modules.get(k) for k in injected}
    sys.modules.update(injected)

    try:
        spec = importlib.util.spec_from_file_location(
            'flowtask.components.PlanogramCompliance_integ',
            COMPONENT_FILE,
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    finally:
        for k, orig in to_restore.items():
            if orig is None:
                sys.modules.pop(k, None)
            else:
                sys.modules[k] = orig

    return mod, ComponentError, ConfigError, mock_asyncdb_cls


_MOD, ComponentError, ConfigError, MockAsyncDB = _load_component()
PlanogramCompliance = _MOD.PlanogramCompliance


# ---------------------------------------------------------------------------
# Smoke tests — parrot_pipelines imports work without proxy
# ---------------------------------------------------------------------------

def test_parrot_pipelines_models_import():
    """PlanogramConfig and EndcapGeometry importable directly from parrot_pipelines."""
    from parrot_pipelines.models import PlanogramConfig, EndcapGeometry
    assert PlanogramConfig is not None
    assert EndcapGeometry is not None


def test_parrot_pipelines_pipeline_importable():
    """Pipeline class loadable from parrot_pipelines directly."""
    from parrot_pipelines.planogram.plan import PlanogramCompliance as PPCompliance
    assert PPCompliance is not None


# ---------------------------------------------------------------------------
# Integration — get_planogram_config before start()
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_get_planogram_config_before_start_no_attribute_error():
    """get_planogram_config() must not raise AttributeError before start()."""
    from parrot_pipelines.models import PlanogramConfig

    instance = PlanogramCompliance.__new__(PlanogramCompliance)
    instance._planogram_name = 'test_planogram'
    instance._planogram_config_table = 'public.planogram_configs'
    instance._planogram_type = 'product_on_shelves'
    instance._reference_images = []   # the TASK-023 fix
    instance.confidence_threshold = 0.15
    instance.detection_model = 'yolo11l.pt'
    instance._logger = MagicMock()

    mock_conn = AsyncMock()
    mock_conn.fetch_one = AsyncMock(return_value=dict(FAKE_DB_ROW))
    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_ctx.__aexit__ = AsyncMock(return_value=False)
    MockAsyncDB.return_value.connection = AsyncMock(return_value=mock_ctx)

    result = await instance.get_planogram_config(reference_images=None)
    assert isinstance(result, PlanogramConfig)
