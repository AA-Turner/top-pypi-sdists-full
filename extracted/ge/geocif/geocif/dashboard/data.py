"""Data loading layer for the GeoCIF Panel dashboard.

Provides DashboardData: a lazy loader that wraps a SQLite database
(local or fetched from HuggingFace Hub) and an optional agmet PNG root.
"""

import json
import logging
import re
import sqlite3
from functools import lru_cache
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

# Known crop suffixes for parsing table names like "south_africa_maize"
_KNOWN_CROPS = [
    "winter_wheat", "spring_wheat", "maize", "rice", "soybean",
    "sorghum", "millet", "teff", "wheat", "barley", "cassava",
    "groundnut", "sesame", "cotton", "sugarcane",
]

# Tables that are NOT country_crop prediction tables
_SYSTEM_TABLES = {
    "country_metrics", "regional_metrics", "regional_metrics_by_year",
    "shap_values", "feature_importance", "models", "sqlite_master",
}


def _parse_table_name(table: str):
    """Split a prediction table name into (country, crop).

    Tries longest crop suffix first so 'winter_wheat' beats 'wheat'.
    Returns (country, crop) or None if no known crop matches.
    """
    for crop in sorted(_KNOWN_CROPS, key=len, reverse=True):
        if table.endswith(f"_{crop}"):
            country = table[: -len(f"_{crop}")]
            return country, crop
    return None


class DashboardData:
    """Lazy data loader for the GeoCIF Panel dashboard."""

    def __init__(
        self,
        db_path=None,
        hf_repo_id=None,
        agmet_root=None,
        outlook_root=None,
    ):
        if db_path:
            self.db_path = Path(db_path)
        elif hf_repo_id:
            self.db_path = self._download_db_from_hf(hf_repo_id)
        else:
            self.db_path = None

        self.agmet_root = Path(agmet_root) if agmet_root else None
        self.outlook_root = Path(outlook_root) if outlook_root else None
        self.hf_repo_id = hf_repo_id
        self._table_cache: dict[str, bool] = {}

    # ── helpers ───────────────────────────────────────────────────────

    def _table_exists(self, table_name: str) -> bool:
        if self.db_path is None:
            return False
        if table_name not in self._table_cache:
            with sqlite3.connect(self.db_path) as con:
                cur = con.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table_name,),
                )
                self._table_cache[table_name] = cur.fetchone() is not None
        return self._table_cache[table_name]

    @staticmethod
    def _download_db_from_hf(repo_id: str) -> Path:
        from huggingface_hub import hf_hub_download

        manifest_path = hf_hub_download(
            repo_id=repo_id, filename="manifest.json", repo_type="dataset",
        )
        with open(manifest_path) as f:
            manifest = json.load(f)

        latest = manifest["databases"][-1]["filename"]
        local_path = hf_hub_download(
            repo_id=repo_id, filename=latest, repo_type="dataset",
        )
        return Path(local_path)

    # ── prediction tables ─────────────────────────────────────────────

    @lru_cache(maxsize=1)
    def list_prediction_tables(self) -> list[tuple[str, str, str]]:
        """Return [(country, crop, table_name), ...] for prediction tables."""
        if self.db_path is None:
            return []
        with sqlite3.connect(self.db_path) as con:
            tables = pd.read_sql(
                "SELECT name FROM sqlite_master WHERE type='table'", con,
            )["name"].tolist()
        results = []
        for t in tables:
            if t in _SYSTEM_TABLES or t.startswith("config_"):
                continue
            parsed = _parse_table_name(t)
            if parsed:
                results.append((*parsed, t))
        return results

    def query_predictions(self, table: str) -> pd.DataFrame:
        with sqlite3.connect(self.db_path) as con:
            df = pd.read_sql(f'SELECT * FROM "{table}"', con)
        for col in ["Harvest Year"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        for col in ["Predicted Yield (tn per ha)", "Observed Yield (tn per ha)"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df

    # ── metrics ───────────────────────────────────────────────────────

    def query_country_metrics(self) -> pd.DataFrame:
        if not self._table_exists("country_metrics"):
            return pd.DataFrame()
        with sqlite3.connect(self.db_path) as con:
            return pd.read_sql("SELECT * FROM country_metrics", con)

    def query_regional_metrics(self) -> pd.DataFrame:
        if not self._table_exists("regional_metrics"):
            return pd.DataFrame()
        with sqlite3.connect(self.db_path) as con:
            return pd.read_sql("SELECT * FROM regional_metrics", con)

    # ── SHAP ──────────────────────────────────────────────────────────

    def query_feature_importance(self) -> pd.DataFrame:
        if not self._table_exists("feature_importance"):
            return pd.DataFrame()
        with sqlite3.connect(self.db_path) as con:
            return pd.read_sql("SELECT * FROM feature_importance", con)

    @lru_cache(maxsize=1)
    def query_shap_values(self) -> pd.DataFrame:
        if not self._table_exists("shap_values"):
            return pd.DataFrame()
        with sqlite3.connect(self.db_path) as con:
            return pd.read_sql("SELECT * FROM shap_values", con)

    # ── agmet PNGs ────────────────────────────────────────────────────

    @lru_cache(maxsize=1)
    def discover_agmet_pngs(self) -> dict:
        """Walk agmet_root and build a nested index.

        Returns: {country: {crop_season_year: {level: [region_stem, ...]}}}
        Also stores a flat lookup: self._png_lookup[(country, folder, level, region)] = Path
        """
        index = {}
        self._png_lookup = {}

        if self.agmet_root is None or not self.agmet_root.exists():
            return index

        for png in self.agmet_root.rglob("*.png"):
            rel = png.relative_to(self.agmet_root)
            parts = rel.parts

            # Expected: .../{country}/{crop_s{n}_{year}}/condition/{level}/{region}.png
            # Walk backwards to find the "condition" marker
            try:
                cond_idx = parts.index("condition")
            except ValueError:
                continue

            if cond_idx < 2 or cond_idx + 2 >= len(parts):
                continue

            country = parts[cond_idx - 2]
            folder = parts[cond_idx - 1]  # e.g. "mz_s1_2026"
            level = parts[cond_idx + 1]   # "adm1" or "district"
            region = png.stem

            index.setdefault(country, {}).setdefault(folder, {}).setdefault(level, [])
            if region not in index[country][folder][level]:
                index[country][folder][level].append(region)

            self._png_lookup[(country, folder, level, region)] = png

        # Sort region lists
        for country in index:
            for folder in index[country]:
                for level in index[country][folder]:
                    index[country][folder][level].sort()

        return index

    def get_agmet_png(self, country, folder, level, region) -> Path | None:
        self.discover_agmet_pngs()  # ensure _png_lookup is populated
        return self._png_lookup.get((country, folder, level, region))

    # ── outlook PNGs ──────────────────────────────────────────────────

    def discover_outlook_pngs(self) -> list[Path]:
        if self.outlook_root is None or not self.outlook_root.exists():
            return []
        return sorted(self.outlook_root.rglob("yield_outlook_*.png"))

    # ── availability flags ────────────────────────────────────────────

    @property
    def has_predictions(self) -> bool:
        return len(self.list_prediction_tables()) > 0

    @property
    def has_shap(self) -> bool:
        return (
            self._table_exists("shap_values")
            or self._table_exists("feature_importance")
        )

    @property
    def has_metrics(self) -> bool:
        return self._table_exists("country_metrics")

    @property
    def has_agmet(self) -> bool:
        if self.agmet_root and self.agmet_root.exists():
            return any(self.agmet_root.rglob("*.png"))
        return False
