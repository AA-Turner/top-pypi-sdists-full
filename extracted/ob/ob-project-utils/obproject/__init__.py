from .projectbase import ProjectFlow
from .project_events import ProjectEvent, project_trigger
from .project_schedule import project_schedule
from .assets import AssetInstance, EntityRef, promote_assets

# highlight_card requires metaflow features not available in all versions
try:
    from highlight_card import highlight
except ImportError:
    highlight = None

METAFLOW_PACKAGE_POLICY = "include"
