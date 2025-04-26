import re


def validate_memorystore_instance_name(memorystore_instance_name: str) -> bool:
    if (
        re.search("projects/.+/locations/.+/instances/.+", memorystore_instance_name)
        is None
    ):
        return False
    return True
