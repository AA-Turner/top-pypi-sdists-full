"""Navigation branch — typed filters returning TacoDataset.

Two main branches in tacoreader:
    nav/   -> ds.filter_*() -> TacoDataset  (this package)
    sql/   -> ds.sql(query) -> DataFrame
"""

from tacoreader.nav.filters import apply_bbox_filter, apply_datetime_filter

__all__ = ["apply_bbox_filter", "apply_datetime_filter"]