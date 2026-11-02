import importlib
import logging
from typing import Any

logger = logging.getLogger(__name__)


def can_import_class(class_path: str) -> bool:
    """Check if a class can be imported

    Args:
        class_path: Full path to the class (e.g., 'module.submodule.ClassName')

    Returns:
        True if class can be imported, False otherwise
    """
    try:
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        getattr(module, class_name)
        return True
    except Exception as e:
        logger.error(f"Failed to import class {class_path}: {e}")
        return False


def safe_import_class(class_path: str) -> Any | None:
    """Safely import a class

    Args:
        class_path: Full path to the class (e.g., 'module.submodule.ClassName')

    Returns:
        The class if successfully imported, None otherwise
    """
    if can_import_class(class_path):
        module_path, class_name = class_path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)
        return cls
    else:
        return None
