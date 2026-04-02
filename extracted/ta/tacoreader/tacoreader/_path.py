"""Path resolution for TACO datasets.

Unified handling of local/remote paths with format auto-detection.
"""

from tacoreader._constants import COLLECTION_JSON, FLAT_VIEW_PREFIX, LEVEL_VIEW_PREFIX, TACOZIP_EXTENSIONS
from tacoreader._dataset_types import DatasetOrigin
from tacoreader._exceptions import TacoFormatError
from tacoreader._flat_views import build_flat_views
from tacoreader._format import _file_exists, is_remote
from tacoreader.dataset import TacoDataset
from tacoreader.storage import create_backend


class TacoPath:
    """Resolve path: location + kind + loading."""

    def __init__(self, path: str, base_path: str | None = None):
        self.original = path.rstrip("/")
        self.remote = is_remote(path)
        self.base_path = base_path
        self.kind, self.resolved = self._detect()

    def _detect(self) -> tuple[str, str]:
        # TacoCat explicit
        if self.original.endswith(".tacocat"):
            return "tacocat", self.original

        # TacoZip explicit
        if self.original.endswith(TACOZIP_EXTENSIONS):
            return "zip", self.original

        # Directory with .tacocat inside
        tacocat_path = f"{self.original}/.tacocat"
        if _file_exists(tacocat_path, COLLECTION_JSON):
            return "tacocat", tacocat_path

        # Folder with COLLECTION.json
        if _file_exists(self.original, COLLECTION_JSON):
            return "folder", self.original

        raise TacoFormatError(
            f"COLLECTION.json not found in {self.original}\n"
            f"Expected: .tacozip file, .tacocat folder, or directory with COLLECTION.json"
        )

    def load(self, **opts) -> TacoDataset:
        backend = create_backend(self.kind)
        dataset = backend.load(self.resolved, **opts)

        # Apply base_path override for TacoCat
        if self.base_path is not None and self.kind == "tacocat":
            dataset = self._apply_base_path(dataset, backend, self.base_path)

        return dataset

    def _apply_base_path(self, dataset: TacoDataset, backend, base_path: str) -> TacoDataset:
        """Override vsi_base_path for TacoCat datasets.

        Drops and recreates all views (internal levelN + flat lN) with the
        new base path. Creates new DatasetOrigin since origin is immutable.
        """
        from tacoreader._constants import DEFAULT_VIEW_NAME
        from tacoreader._vsi import to_vsi_root

        base_vsi = to_vsi_root(base_path)
        if not base_vsi.endswith("/"):
            base_vsi += "/"

        max_depth = dataset.pit_schema.max_depth()
        level_ids = list(range(max_depth + 1))

        # Drop existing internal views
        dataset._duckdb.execute(f"DROP VIEW IF EXISTS {DEFAULT_VIEW_NAME}")
        for i in level_ids:
            dataset._duckdb.execute(f"DROP VIEW IF EXISTS {LEVEL_VIEW_PREFIX}{i}")

        # Drop existing flat views
        for i in level_ids:
            dataset._duckdb.execute(f"DROP VIEW IF EXISTS {FLAT_VIEW_PREFIX}{i}")

        # Recreate internal views with new vsi_base_path
        backend.setup_duckdb_views(dataset._duckdb, level_ids, base_vsi)

        # Recreate data alias
        dataset._duckdb.execute(f"CREATE VIEW {DEFAULT_VIEW_NAME} AS SELECT * FROM {LEVEL_VIEW_PREFIX}0")

        # Recreate flat views
        build_flat_views(dataset._duckdb, level_ids)

        # Create new origin with updated vsi_base_path (origin is frozen)
        new_origin = DatasetOrigin(
            path=dataset._origin.path,
            format=dataset._origin.format,
            vsi_base_path=base_vsi,
            collection=dataset._origin.collection,
        )

        return TacoDataset.model_construct(
            id=dataset.id,
            version=dataset.version,
            description=dataset.description,
            tasks=dataset.tasks,
            extent=dataset.extent,
            providers=dataset.providers,
            licenses=dataset.licenses,
            title=dataset.title,
            curators=dataset.curators,
            keywords=dataset.keywords,
            pit_schema=dataset.pit_schema,
            _origin=new_origin,
            _duckdb=dataset._duckdb,
            _owns_connection=True,
            _query=dataset._query,
            _dataframe_backend=dataset._dataframe_backend,
        )