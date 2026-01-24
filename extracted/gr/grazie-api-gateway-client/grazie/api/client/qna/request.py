import attrs


@attrs.define(auto_attribs=True)
class PrioritizedSource:
    name: str
    priority: int
