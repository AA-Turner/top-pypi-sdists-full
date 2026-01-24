from .projectbase import ProjectFlow
from .project_events import ProjectEvent, project_trigger

# highlight_card requires metaflow features not available in all versions
try:
    from highlight_card import highlight
except ImportError:
    highlight = None

METAFLOW_PACKAGE_POLICY = "include"
