import dataclasses
import importlib
import typing
from typing import Type, get_args, get_origin

import chalk.features
from chalk.features._encoding.converter import canonicalize_typ


@dataclasses.dataclass
class SerializedRichType:
    module_name: str
    qualname: str
    type_params: "tuple[SerializedRichType, ...]"

    @classmethod
    def from_typ(cls, typ: Type) -> "SerializedRichType":
        # Special case for chalk DataFrames
        if isinstance(typ, type) and issubclass(  # pyright: ignore[reportUnnecessaryIsInstance]
            typ, chalk.features.DataFrame
        ):
            params = tuple()
            try:
                if typ.references_feature_set is not None:  # pyright: ignore[reportUnnecessaryComparison]
                    params = (typ.references_feature_set,)
            except:
                pass
            return SerializedRichType(
                module_name="chalk.features",
                qualname="DataFrame",
                type_params=tuple(SerializedRichType.from_typ(p) for p in params),
            )

        typ = typing.cast(typing.Type, canonicalize_typ(typ))
        origin = get_origin(typ)
        if origin is not None:
            typ_module = getattr(origin, "__module__", None)
            typ_qualname = getattr(origin, "__qualname__", None)
        else:
            typ_module = getattr(typ, "__module__", None)
            typ_qualname = getattr(typ, "__qualname__", None)

        if typ_module is None or typ_qualname is None:
            raise ValueError(
                f"Can't serialize type {typ} since it doesn't have a module/qualname: module={typ_module}, qualname={typ_qualname}"
            )
        params = tuple(SerializedRichType.from_typ(p) for p in get_args(typ))
        return SerializedRichType(module_name=typ_module, qualname=typ_qualname, type_params=params)

    def to_typ(self) -> Type:
        if self.module_name == "builtins" and self.qualname == "NoneType":
            return type(None)

        module = importlib.import_module(self.module_name)
        path = self.qualname.split(".")
        current: typing.Any = module
        for p in path:
            current = getattr(current, p)
        typ = current
        if len(self.type_params) > 0:
            params = tuple(p.to_typ() for p in self.type_params)
            typ = typ[params]
        return typ
