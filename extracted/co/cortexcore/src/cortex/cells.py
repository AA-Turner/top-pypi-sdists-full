"""Programmer-facing cell configs composed from a scaffold and a core."""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny

from cortex.config import (
    AGaLiTeCoreConfig,
    AxonCoreConfig,
    CausalConv1dCoreConfig,
    CoreConfig,
    LSTMCoreConfig,
    PassThroughScaffoldConfig,
    PostUpGatedScaffoldConfig,
    PreUpGatedScaffoldConfig,
    ScaffoldConfig,
    XLCoreConfig,
    mLSTMCoreConfig,
    sLSTMCoreConfig,
)


class CellConfig(BaseModel):
    """Public cell config: a scaffold with an optional nested core."""

    model_config = ConfigDict(extra="forbid")

    scaffold: SerializeAsAny[ScaffoldConfig]
    core: SerializeAsAny[CoreConfig | None] = Field(default=None)

    def as_scaffold_config(self) -> ScaffoldConfig:
        scaffold = self.scaffold.model_copy(deep=True)
        if self.core is not None:
            scaffold.core = self.core.model_copy(deep=True)
        return scaffold  # type: ignore[return-value]


class AxonCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PostUpGatedScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=AxonCoreConfig)


class XLCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PostUpGatedScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=XLCoreConfig)


class mLSTMCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PreUpGatedScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=mLSTMCoreConfig)


class sLSTMCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PostUpGatedScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=sLSTMCoreConfig)


class LSTMCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PassThroughScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=LSTMCoreConfig)


class CausalConv1dCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PassThroughScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=CausalConv1dCoreConfig)


class AGaLiTeCellConfig(CellConfig):
    scaffold: SerializeAsAny[ScaffoldConfig] = Field(default_factory=PostUpGatedScaffoldConfig)
    core: SerializeAsAny[CoreConfig] = Field(default_factory=AGaLiTeCoreConfig)


def default_cells() -> List[CellConfig]:
    return [AxonCellConfig(), XLCellConfig(), mLSTMCellConfig(), sLSTMCellConfig()]


__all__ = [
    "CellConfig",
    "AxonCellConfig",
    "XLCellConfig",
    "mLSTMCellConfig",
    "sLSTMCellConfig",
    "LSTMCellConfig",
    "CausalConv1dCellConfig",
    "AGaLiTeCellConfig",
    "default_cells",
]
