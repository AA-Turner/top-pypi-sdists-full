import importlib.metadata
import platform
from typing import List


def get_environment_dependencies() -> List[str]:
    distributions = importlib.metadata.distributions()
    return sorted(
        [f"{dist.metadata['Name']}=={dist.version}" for dist in distributions]
    )


def get_environment_details() -> List[str]:
    return [
        f"arch={platform.architecture()[0]}",
        f"cpu={platform.processor()}",
        f"platform={platform.platform()}",
        f"python_version={platform.python_version()}",
        f"python_implementation={platform.python_implementation()}",
        f"python_compiler={platform.python_compiler()}",
    ]
