"""Auto builder: stacks of Column layers built from explicit cell lists."""

from __future__ import annotations

from typing import Iterable, Sequence, cast

from pydantic import BaseModel

from cortex.cells import CellConfig as PublicCellConfig
from cortex.cells import default_cells
from cortex.config import CortexStackConfig, RoutedAdapterConfig, RouterConfig, ScaffoldConfig
from cortex.scaffolds.column.auto import build_column_auto_config
from cortex.stacks.base import CortexStack


def build_cortex_auto_config(
    *,
    d_hidden: int,
    num_layers: int = 2,
    layers: Sequence[Sequence[PublicCellConfig | ScaffoldConfig]] | None = None,
    router: RouterConfig | None = None,
    post_norm: bool = False,
    compile_scaffolds: bool = True,
    override_global_configs: Iterable[BaseModel] | None = None,
    routed_adapter: RoutedAdapterConfig | None = None,
) -> CortexStackConfig:
    """Build a CortexStackConfig with Column layers from explicit cell lists."""

    configured_layers = _resolve_layers(num_layers=num_layers, layers=layers)

    scaffolds: list[ScaffoldConfig] = []
    for layer_cells in configured_layers:
        col_cfg = build_column_auto_config(d_hidden=d_hidden, cells=layer_cells, router=router)
        scaffolds.append(col_cfg)

    global_configs = tuple(override_global_configs or ())
    if global_configs:
        scaffolds = [cast(ScaffoldConfig, _apply_overrides_model(scaffold, global_configs)) for scaffold in scaffolds]

    return CortexStackConfig(
        scaffolds=scaffolds,
        d_hidden=d_hidden,
        post_norm=post_norm,
        compile_scaffolds=bool(compile_scaffolds),
        routed_adapter=routed_adapter,
    )


def build_cortex_auto_stack(
    *,
    d_hidden: int,
    num_layers: int = 4,
    layers: Sequence[Sequence[PublicCellConfig | ScaffoldConfig]] | None = None,
    router: RouterConfig | None = None,
    post_norm: bool = False,
    compile_scaffolds: bool = True,
    override_global_configs: Iterable[BaseModel] | None = None,
    routed_adapter: RoutedAdapterConfig | None = None,
) -> CortexStack:
    """Build a Column-based CortexStack with per-layer cells."""

    cfg = build_cortex_auto_config(
        d_hidden=d_hidden,
        num_layers=num_layers,
        layers=layers,
        router=router,
        post_norm=post_norm,
        compile_scaffolds=compile_scaffolds,
        override_global_configs=override_global_configs,
        routed_adapter=routed_adapter,
    )
    return CortexStack(cfg)


def _resolve_layers(
    *,
    num_layers: int,
    layers: Sequence[Sequence[PublicCellConfig | ScaffoldConfig]] | None,
) -> list[list[PublicCellConfig | ScaffoldConfig]]:
    if layers is not None:
        configured_layers = [list(layer) for layer in layers]
        if not configured_layers:
            raise ValueError("layers produced no Column scaffolds")
        return configured_layers
    return [[cast(PublicCellConfig, cell.model_copy(deep=True)) for cell in default_cells()] for _ in range(num_layers)]


def _apply_overrides_model(model: BaseModel, overrides: Sequence[BaseModel]) -> BaseModel:
    for override in overrides:
        if isinstance(model, type(override)):
            fields_set = override.model_fields_set
            update = override.model_dump()
            if fields_set:
                update = {key: update[key] for key in fields_set if key in update}
            else:
                update = override.model_dump(exclude_unset=True)
            return model.model_copy(update=update)

    cloned = model.model_copy(deep=True)
    fields = type(cloned).model_fields
    for name in fields:
        value = getattr(cloned, name, None)
        new_value = _apply_overrides_value(value, overrides)
        if new_value is not value:
            setattr(cloned, name, new_value)
    return cloned


def _apply_overrides_value(value, overrides: Sequence[BaseModel]):
    if isinstance(value, BaseModel):
        return _apply_overrides_model(value, overrides)
    if isinstance(value, list):
        changed = False
        out = []
        for item in value:
            new_item = _apply_overrides_value(item, overrides)
            changed = changed or (new_item is not item)
            out.append(new_item)
        return out if changed else value
    return value
