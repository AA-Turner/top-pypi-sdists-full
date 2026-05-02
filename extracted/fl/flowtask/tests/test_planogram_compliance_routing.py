"""Unit tests for PlanogramCompliance planogram_type routing (FEAT-003 / TASK-009-010).

Tests verify the fallback chain:
  DB result['planogram_type'] → YAML kwarg → default "product_on_shelves"
"""
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Paths to the source files under test (worktree-relative, resolved at import time)
_REPO_ROOT = Path(__file__).parent.parent
_COMPONENT_SRC = _REPO_ROOT / 'flowtask' / 'components' / 'PlanogramCompliance.py'
_PIPELINE_SRC = _REPO_ROOT / 'flowtask' / 'interfaces' / 'pipelines' / 'parrot.py'


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_component(**kwargs):
    """Instantiate PlanogramCompliance by replicating __init__ kwarg extraction,
    bypassing parent chains that require a live DB or event loop."""
    from flowtask.components.PlanogramCompliance import PlanogramCompliance

    obj = object.__new__(PlanogramCompliance)
    obj._planogram_name = kwargs.get('name', 'test_planogram')
    obj._planogram_type = kwargs.get('planogram_type', 'product_on_shelves')
    obj.planogram_config = None
    obj.reference_images = kwargs.get('reference_images', {})
    obj.image_column = kwargs.get('image_column', 'image_data')
    obj._id_column = kwargs.get('id_column', 'photo_id')
    obj.llm_config = kwargs.get('llm_config', {})
    obj.detection_model = kwargs.get('detection_model', 'yolo11l.pt')
    obj.confidence_threshold = kwargs.get('confidence_threshold', 0.15)
    obj.overlay_output = kwargs.get('overlay_output_path', 'identified')
    obj._logger = MagicMock()
    obj._reference_images = {}
    return obj


def _make_db_result(**extra) -> dict:
    """Return a minimal fake DB row dict matching troc.planograms_configurations."""
    base = {
        'planogram_id': 42,
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
        'planogram_config': {},
        'roi_detection_prompt': 'find the endcap',
        'object_identification_prompt': 'identify products',
        'confidence_threshold': 0.15,
        'detection_model': 'yolo11l.pt',
    }
    base.update(extra)
    return base


def _make_db_mock(db_result: dict):
    """Build a mock for AsyncDB that matches `async with await db.connection() as conn:`."""
    mock_conn = AsyncMock()
    mock_conn.fetch_one = AsyncMock(return_value=db_result)

    mock_ctx = AsyncMock()
    mock_ctx.__aenter__ = AsyncMock(return_value=mock_conn)
    mock_ctx.__aexit__ = AsyncMock(return_value=False)

    mock_db_instance = MagicMock()
    mock_db_instance.connection = AsyncMock(return_value=mock_ctx)

    mock_db_class = MagicMock(return_value=mock_db_instance)
    return mock_db_class


# ---------------------------------------------------------------------------
# Default planogram_type
# ---------------------------------------------------------------------------

class TestPlanogramTypeDefault:
    def test_defaults_to_product_on_shelves(self):
        """planogram_type defaults to 'product_on_shelves' when not provided."""
        comp = _make_component()
        assert comp._planogram_type == 'product_on_shelves'

    def test_explicit_yaml_kwarg_is_stored(self):
        """planogram_type YAML kwarg is stored on the instance."""
        comp = _make_component(planogram_type='ink_wall')
        assert comp._planogram_type == 'ink_wall'


# ---------------------------------------------------------------------------
# DB resolution
# ---------------------------------------------------------------------------

class TestPlanogramTypeDBResolution:
    """Tests for the planogram_type fallback chain in get_planogram_config()."""

    def _make_fake_config_class(self, captured: dict):
        """Return a fake PlanogramConfig class that records constructor kwargs
        and passes isinstance() checks (it IS the class being checked against)."""
        class FakePlanogramConfig:
            def __init__(self, **kwargs):
                captured['planogram_type'] = kwargs.get('planogram_type')
        return FakePlanogramConfig

    @pytest.mark.asyncio
    async def test_db_value_wins_over_yaml_kwarg(self):
        """DB planogram_type takes precedence over the YAML kwarg."""
        comp = _make_component(planogram_type='ink_wall')
        db_result = _make_db_result(planogram_type='product_on_shelves')
        captured = {}
        FakeConfig = self._make_fake_config_class(captured)

        with patch('flowtask.components.PlanogramCompliance.AsyncDB', _make_db_mock(db_result)), \
             patch('flowtask.components.PlanogramCompliance.PlanogramConfig', FakeConfig), \
             patch('flowtask.components.PlanogramCompliance.EndcapGeometry', return_value=MagicMock()):
            await comp.get_planogram_config()

        assert captured['planogram_type'] == 'product_on_shelves'

    @pytest.mark.asyncio
    async def test_yaml_fallback_when_db_column_missing(self):
        """YAML planogram_type used when DB record lacks the column."""
        comp = _make_component(planogram_type='ink_wall')
        db_result = _make_db_result()  # no planogram_type key
        captured = {}
        FakeConfig = self._make_fake_config_class(captured)

        with patch('flowtask.components.PlanogramCompliance.AsyncDB', _make_db_mock(db_result)), \
             patch('flowtask.components.PlanogramCompliance.PlanogramConfig', FakeConfig), \
             patch('flowtask.components.PlanogramCompliance.EndcapGeometry', return_value=MagicMock()):
            await comp.get_planogram_config()

        assert captured['planogram_type'] == 'ink_wall'

    @pytest.mark.asyncio
    async def test_default_when_neither_yaml_nor_db_provide_type(self):
        """Default 'product_on_shelves' when neither YAML nor DB define type."""
        comp = _make_component()
        db_result = _make_db_result()
        captured = {}
        FakeConfig = self._make_fake_config_class(captured)

        with patch('flowtask.components.PlanogramCompliance.AsyncDB', _make_db_mock(db_result)), \
             patch('flowtask.components.PlanogramCompliance.PlanogramConfig', FakeConfig), \
             patch('flowtask.components.PlanogramCompliance.EndcapGeometry', return_value=MagicMock()):
            await comp.get_planogram_config()

        assert captured['planogram_type'] == 'product_on_shelves'

    @pytest.mark.asyncio
    async def test_unknown_type_raises_config_error(self):
        """Unknown planogram_type raises ConfigError."""
        from flowtask.exceptions import ConfigError

        comp = _make_component()
        db_result = _make_db_result(planogram_type='nonexistent_type')

        class BrokenConfig:
            def __init__(self, **kwargs):
                raise KeyError(kwargs.get('planogram_type'))

        with patch('flowtask.components.PlanogramCompliance.AsyncDB', _make_db_mock(db_result)), \
             patch('flowtask.components.PlanogramCompliance.PlanogramConfig', BrokenConfig), \
             patch('flowtask.components.PlanogramCompliance.EndcapGeometry', return_value=MagicMock()):
            with pytest.raises(ConfigError):
                await comp.get_planogram_config()


# ---------------------------------------------------------------------------
# No print() in source files
# ---------------------------------------------------------------------------

class TestNoPrintStatements:
    def test_no_print_in_aipipeline(self):
        """AIPipeline source must not contain print() calls."""
        source = _PIPELINE_SRC.read_text()
        assert 'print(' not in source, (
            f"Found print() in {_PIPELINE_SRC} — use self.logger.debug() instead."
        )

    def test_no_print_in_planogram_compliance(self):
        """PlanogramCompliance source must not contain print() calls."""
        source = _COMPONENT_SRC.read_text()
        assert 'print(' not in source, (
            f"Found print() in {_COMPONENT_SRC} — use self._logger instead."
        )
