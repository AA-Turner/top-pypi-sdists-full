import uuid
from typing import List, Optional, Union


def uuid4_examples(n: int = 10, *, uuids_as_strings: bool = True) -> Union[List[str], List[uuid.UUID]]:
    """Create n uuids."""
    from d8s_hypothesis import hypothesis_get_strategy_results
    from hypothesis.strategies import uuids

    uuid_objects = hypothesis_get_strategy_results(uuids, n=n)
    if uuids_as_strings:
        return [str(uuid) for uuid in uuid_objects]
    else:
        return uuid_objects


def uuid4() -> str:
    """Create a random UUID."""
    return str(uuid.uuid4())


def uuid3(name: str, *, namespace: Optional[uuid.UUID] = None) -> str:
    """Create a random uuid based on the given name."""
    if namespace is None:
        namespace = uuid.NAMESPACE_DNS

    return str(uuid.uuid3(namespace, name))


def uuid5(name: str, *, namespace: Optional[uuid.UUID] = None) -> str:
    """Create a random uuid based on the given name."""
    if namespace is None:
        namespace = uuid.NAMESPACE_DNS

    return str(uuid.uuid5(namespace, name))


def is_uuid(possible_uuid: Union[str, uuid.UUID], *, version: Optional[int] = None) -> bool:
    """Return whether or not the possible_uuid is a uuid."""
    try:
        new_uuid = uuid.UUID(str(possible_uuid))
    except ValueError:
        return False
    else:
        if version and new_uuid.version != version:
            return False
        return True
