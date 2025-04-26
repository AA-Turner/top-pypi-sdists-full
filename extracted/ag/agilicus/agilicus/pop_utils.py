from agilicus.agilicus_api import FeatureFlag


def _make_set(pop_str: str) -> set:
    if pop_str is None:
        pop_str = ""
    return set(sorted([pop.strip() for pop in pop_str.split(",") if pop]))


def _make_str(pop_set: set) -> str:
    return ",".join(sorted(list(pop_set)))


def add_pop_to_str(pop_str: str, pop: str) -> str:
    if pop_str is None:
        pop_str = ""
    if not pop:
        return pop_str
    pop_set = _make_set(pop_str)
    pop_set.add(pop)
    return _make_str(pop_set)


def remove_pop_from_str(pop_str: str, pop: str) -> str:
    if pop_str is None:
        pop_str = ""
    pop_set = set([pop.strip() for pop in pop_str.split(",")])
    if pop in pop_set:
        pop_set.remove(pop)
    return _make_str(pop_set)


def make_feature_pop_result(feature_obj: FeatureFlag) -> dict:
    result = {}
    result["enabled"] = False
    result["pops"] = []
    if feature_obj:
        result["enabled"] = feature_obj.enabled
        result["pops"] = list(_make_set(feature_obj.setting))
    return result
