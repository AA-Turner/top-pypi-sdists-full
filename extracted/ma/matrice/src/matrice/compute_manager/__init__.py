"""Module providing __init__ functionality."""


from matrice.utils import dependencies_check

dependencies_check(["docker", "psutil", "cryptography", "notebook"])
from matrice.compute_manager.instance_manager import InstanceManager  # noqa: E402

__all__ = ["InstanceManager"]
