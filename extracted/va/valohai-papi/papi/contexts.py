import dataclasses


@dataclasses.dataclass
class APIContext:
    commit_identifier: str = "master"


@dataclasses.dataclass
class YAMLContext:
    pass
