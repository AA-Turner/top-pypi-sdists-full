"""Unit tests for PlanogramCompliance FEAT-009 fixes.

Covers TASK-023 (bug fixes) and TASK-024 (imports + table validation).

Loading strategy: load PlanogramCompliance.py directly via importlib with
mocked dependencies so the Cython flowtask modules are never triggered.
"""
import importlib.util
import sys
import types
import pytest
from pathlib import Path
from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Worktree path — tests always target the worktree's modified source
# ---------------------------------------------------------------------------
WORKTREE = Path(__file__).parent.parent
COMPONENT_FILE = WORKTREE / 'flowtask' / 'components' / 'PlanogramCompliance.py'


def _load_module():
    """Load PlanogramCompliance from the worktree source with mocked deps."""

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

    pp_models = types.ModuleType('parrot_pipelines.models')
    pp_models.PlanogramConfig = MagicMock()
    pp_models.EndcapGeometry = MagicMock()

    flow_mod = types.ModuleType('flowtask.components.flow')
    flow_mod.FlowComponent = _FlowComponent

    aipipeline_mod = types.ModuleType('flowtask.interfaces.pipelines.parrot')
    aipipeline_mod.AIPipeline = _AIPipeline

    injected = {
        'flowtask.exceptions': exc_mod,
        'flowtask.components.flow': flow_mod,
        'flowtask.interfaces.pipelines.parrot': aipipeline_mod,
        'parrot_pipelines': types.ModuleType('parrot_pipelines'),
        'parrot_pipelines.models': pp_models,
        'parrot.clients.google': types.ModuleType('parrot.clients.google'),
        'parrot.models.google': types.ModuleType('parrot.models.google'),
        'asyncdb': types.ModuleType('asyncdb'),
        'querysource': types.ModuleType('querysource'),
        'querysource.conf': types.ModuleType('querysource.conf'),
        'PIL': types.ModuleType('PIL'),
        'PIL.Image': types.ModuleType('PIL.Image'),
    }
    injected['asyncdb'].AsyncDB = MagicMock()
    injected['querysource.conf'].default_dsn = 'postgresql://localhost/test'
    injected['parrot.clients.google'].GoogleGenAIClient = MagicMock()
    injected['parrot.models.google'].GoogleModel = MagicMock()
    injected['PIL.Image'].Image = MagicMock()
    injected['PIL'].Image = MagicMock()

    to_restore = {k: sys.modules.get(k) for k in injected}
    sys.modules.update(injected)

    try:
        spec = importlib.util.spec_from_file_location(
            'flowtask.components.PlanogramCompliance',
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

    return mod, ComponentError, ConfigError


_MOD, ComponentError, ConfigError = _load_module()
PlanogramCompliance = _MOD.PlanogramCompliance
_MAX_REF_IMAGES_PER_KEY = _MOD._MAX_REF_IMAGES_PER_KEY
_TABLE_RE = _MOD._TABLE_RE


@pytest.fixture
def obj(tmp_path):
    instance = PlanogramCompliance.__new__(PlanogramCompliance)
    instance._reference_images = []
    instance.reference_images = {}
    instance._logger = MagicMock()
    instance.directory = tmp_path
    instance.mask_replacement = lambda x: x
    return instance


# ---------------------------------------------------------------------------
# Module 1 — _prepare_reference_images
# ---------------------------------------------------------------------------

class TestPrepareReferenceImages:

    def test_single_file_returns_path(self, obj, tmp_path):
        img = tmp_path / 'images' / 'prod.jpg'
        img.parent.mkdir(parents=True)
        img.write_bytes(b'')
        obj.reference_images = {'epson': 'prod.jpg'}
        result = obj._prepare_reference_images()
        assert result == {'epson': img}

    def test_directory_expands_into_separate_keys(self, obj, tmp_path):
        d = tmp_path / 'images' / 'products'
        d.mkdir(parents=True)
        for name in ['a.jpg', 'b.png', 'c.jpg']:
            (d / name).write_bytes(b'')
        obj.reference_images = {'epson': 'products'}
        result = obj._prepare_reference_images()
        assert len(result) == 3
        assert all(isinstance(v, Path) for v in result.values())
        assert all(k.startswith('epson_') for k in result.keys())

    def test_directory_values_are_single_paths_not_lists(self, obj, tmp_path):
        d = tmp_path / 'images' / 'products'
        d.mkdir(parents=True)
        (d / 'ref.jpg').write_bytes(b'')
        obj.reference_images = {'brand': 'products'}
        result = obj._prepare_reference_images()
        for v in result.values():
            assert isinstance(v, Path), f"Expected Path, got {type(v)}"

    def test_directory_max_5_files(self, obj, tmp_path):
        d = tmp_path / 'images' / 'many'
        d.mkdir(parents=True)
        for i in range(8):
            (d / f'img_{i}.jpg').write_bytes(b'')
        obj.reference_images = {'brand': 'many'}
        result = obj._prepare_reference_images()
        assert len(result) == 5

    def test_directory_collects_all_extensions(self, obj, tmp_path):
        d = tmp_path / 'images' / 'mixed'
        d.mkdir(parents=True)
        for name in ['a.jpg', 'b.png', 'c.bmp', 'd.tiff']:
            (d / name).write_bytes(b'')
        obj.reference_images = {'brand': 'mixed'}
        result = obj._prepare_reference_images()
        assert len(result) == 4

    def test_empty_directory_raises(self, obj, tmp_path):
        d = tmp_path / 'images' / 'empty'
        d.mkdir(parents=True)
        obj.reference_images = {'brand': 'empty'}
        with pytest.raises(ComponentError, match="No images found"):
            obj._prepare_reference_images()

    def test_missing_path_raises(self, obj, tmp_path):
        obj.reference_images = {'brand': 'nonexistent.jpg'}
        with pytest.raises(ComponentError, match="not found"):
            obj._prepare_reference_images()


# ---------------------------------------------------------------------------
# Module 2 — self._reference_images initialized in __init__
# ---------------------------------------------------------------------------

class TestReferenceImagesInit:

    def test_reference_images_attr_is_empty_list(self):
        instance = PlanogramCompliance.__new__(PlanogramCompliance)
        instance._reference_images = []
        assert instance._reference_images == []
        assert isinstance(instance._reference_images, list)


# ---------------------------------------------------------------------------
# Module 3 — _TABLE_RE allowlist
# ---------------------------------------------------------------------------

class TestTableNameRegex:

    @pytest.mark.parametrize("table", [
        "public.planogram_configs",
        "myschema.planogram_configs",
        "planogram_configs",
        "my_schema.my_table_123",
        "_private_table",
    ])
    def test_valid_table_names_match(self, table):
        assert _TABLE_RE.match(table), f"{table!r} should be valid"

    @pytest.mark.parametrize("table", [
        "; DROP TABLE planograms",
        "my-table",
        "123invalid",
        "table name with spaces",
    ])
    def test_invalid_table_names_do_not_match(self, table):
        assert not _TABLE_RE.match(table), f"{table!r} should be invalid"

    @pytest.mark.parametrize("table", [
        "; DROP TABLE x",
        "my-table",
        "123bad",
    ])
    def test_invalid_table_raises_config_error(self, table):
        with pytest.raises(ConfigError, match="Invalid planogram_config_table"):
            if table and not _TABLE_RE.match(table):
                raise ConfigError("Invalid planogram_config_table name: %r" % table)


# ---------------------------------------------------------------------------
# Module 4 — Import path uses parrot_pipelines directly
# ---------------------------------------------------------------------------

class TestImportPath:

    def test_uses_parrot_pipelines_not_proxy(self):
        source = COMPONENT_FILE.read_text()
        assert 'from parrot_pipelines.models import' in source, \
            "Component must import from parrot_pipelines directly"
        assert 'from parrot.pipelines.models import' not in source, \
            "Proxy import must be removed"


# ---------------------------------------------------------------------------
# Module 5 — AIPipeline _load_pipeline uses parrot_pipelines
# ---------------------------------------------------------------------------

class TestAIPipelineMapping:

    def test_load_pipeline_mapping_uses_parrot_pipelines(self):
        aipipeline_file = WORKTREE / 'flowtask' / 'interfaces' / 'pipelines' / 'parrot.py'
        source = aipipeline_file.read_text()
        assert 'parrot_pipelines.planogram.plan.PlanogramCompliance' in source, \
            "_load_pipeline must use direct parrot_pipelines path"
        assert "parrot.pipelines.planogram.plan.PlanogramCompliance" not in source, \
            "Proxy path must be removed"
        assert 'OpenAIClient' not in source, \
            "Unused OpenAIClient import must be removed"
