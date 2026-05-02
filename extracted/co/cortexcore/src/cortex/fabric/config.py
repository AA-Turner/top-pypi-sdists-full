from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class FabricFamilyConfig(BaseModel):
    family_type: Literal["slstm", "axoncell"]
    num_heads: int | None = Field(default=None, ge=1)


class FabricConfig(BaseModel):
    width: int = Field(ge=1)
    height: int = Field(ge=1)
    depth: int = Field(default=1, ge=1)

    hidden_size: int = Field(default=8, ge=1)
    d_public: int | None = Field(default=None, ge=1)
    d_msg: int | None = Field(default=None, ge=1)
    d_slot: int | None = Field(default=None, ge=1)

    num_heads: int | None = Field(default=None, ge=1)
    head_dim: int = Field(default=4, ge=1)

    local_radius: float = Field(default=1.5, gt=0.0)
    patch_edges_per_cell: int = Field(default=0, ge=0)
    patch_min_dist: float = Field(default=4.0, ge=0.0)
    patch_max_dist: float = Field(default=12.0, ge=0.0)
    distance_logit_scale: float = Field(default=0.5, ge=0.0)
    wrap: bool = Field(default=True)

    conduction_speed: float | None = Field(default=None, gt=0.0)
    max_delay: int | None = Field(default=None, ge=1)

    projection_region_shape: tuple[int, ...] | None = None
    cell_arrangement: Literal["random", "x_bands"] = Field(default="random")

    families: dict[str, FabricFamilyConfig] = Field(
        default_factory=lambda: {"slstm": FabricFamilyConfig(family_type="slstm")}
    )
    cell_mix: dict[str, float] = Field(default_factory=lambda: {"slstm": 1.0})

    input_band_width: int = Field(default=1, ge=1)
    output_band_width: int = Field(default=1, ge=1)
    readout_pool: Literal["mean", "attn", "flatten"] = Field(default="mean")
    readout_slots: int = Field(default=4, ge=1)
    execution_mode: Literal["stream", "diffusion"] = Field(default="stream")

    k_max: int = Field(default=8, ge=0)
    default_k: int = Field(default=4, ge=0)
    inject_every_step: bool = Field(default=True)
    use_family_cuda_streams: bool = Field(default=False)
    family_init_noise_std: float = Field(default=0.0, ge=0.0)
    seed: int = Field(default=0)

    @property
    def coord_shape(self) -> tuple[int, ...]:
        if self.depth == 1:
            return (self.width, self.height)
        return (self.width, self.height, self.depth)

    @property
    def coord_dim(self) -> int:
        return 2 if self.depth == 1 else 3

    @model_validator(mode="after")
    def _apply_defaults_and_validate(self) -> FabricConfig:
        if self.d_public is None:
            self.d_public = self.hidden_size
        if self.d_msg is None:
            self.d_msg = self.hidden_size
        if self.d_slot is None:
            self.d_slot = 2 * self.hidden_size
        if self.num_heads is None:
            self.num_heads = 1

        if self.d_msg <= 0 or self.d_public <= 0 or self.d_slot <= 0:
            raise ValueError("derived dimensions must be positive")
        if self.default_k > self.k_max:
            raise ValueError(f"default_k={self.default_k} must be <= k_max={self.k_max}")
        if not self.families:
            raise ValueError("families must not be empty")
        if len(self.families) > 2:
            raise ValueError("v1 supports at most two fabric families")
        family_keys = set(self.families.keys())
        mix_keys = set(self.cell_mix.keys())
        if family_keys != mix_keys:
            raise ValueError(f"families keys {sorted(family_keys)} must match cell_mix keys {sorted(mix_keys)}")
        mix_total = float(sum(self.cell_mix.values()))
        if mix_total <= 0.0:
            raise ValueError("cell_mix weights must sum to a positive value")
        if self.projection_region_shape is not None and len(self.projection_region_shape) != self.coord_dim:
            raise ValueError(
                "projection_region_shape length "
                f"{len(self.projection_region_shape)} must match coord_dim={self.coord_dim}"
            )
        if self.patch_edges_per_cell > 0 and self.patch_max_dist < self.patch_min_dist:
            raise ValueError(f"patch_max_dist={self.patch_max_dist} must be >= patch_min_dist={self.patch_min_dist}")
        return self


__all__ = ["FabricConfig", "FabricFamilyConfig"]
