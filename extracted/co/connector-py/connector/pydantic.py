from pydantic import BaseModel


def is_pydantic_model(cls: type | None) -> bool:
    if cls is None:
        return False
    for _base_model in PydanticModel:
        if issubclass(cls, _base_model):
            return True
    return False


def get_pydantic_model(annotations: dict[str, type]) -> type[BaseModel]:
    for key, val in annotations.items():
        if key in ("return",):
            continue
        if is_pydantic_model(val):
            return val  # type: ignore
    raise ValueError("No Pydantic model found in annotations.")


def _set_pydantic_model() -> frozenset[type]:
    models: list[type] = [BaseModel]

    try:
        from pydantic.v1 import BaseModel as BaseModelV1

        models.append(BaseModelV1)
    except ImportError:
        pass

    return frozenset(models)


PydanticModel = _set_pydantic_model()
