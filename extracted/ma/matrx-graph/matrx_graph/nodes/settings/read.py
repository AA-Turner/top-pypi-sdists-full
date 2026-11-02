"""``settings.read`` — one setting's current value for the run's organization.

Wire its ``value`` into any step input that is a limit (pages to read, items to
keep, a length floor) so the limit is a setting, not a number in the definition.
See :mod:`matrx_graph.settings`."""

from __future__ import annotations

from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.settings import get_feature_settings_reader, get_setting_reader
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success


class SettingReadInput(BaseModel):
    model_config = ConfigDict(extra="ignore")

    feature: str = Field(min_length=1, description="The setting's feature, e.g. research.deep_research_workflow.")
    key: str | None = Field(
        default=None,
        description=(
            "The setting's key within that feature. Leave empty to read EVERY setting of the feature: "
            "the value is then a map of setting name to its value and where it came from "
            "(platform, organization or user)."
        ),
    )


class SettingReadConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")


class SettingValueOutput(KindModel, kind="setting_value"):
    feature: str = Field(description="The setting's feature.")
    key: str = Field(description="The setting's key (empty when the whole feature was read).")
    value: JsonValue = Field(description="The setting's value for this run's organization.")


class SettingReadExecutor:
    """Read one setting's effective value for the run's organization."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="settings.read",
        category=NodeCategory.DATA,
        display_name="Read a Setting",
        description="Use one of your organization's settings in this run.",
        input_schema=SettingReadInput,
        output_schema=SettingValueOutput,
        output_kind="setting_value",
        config_schema=SettingReadConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.IDEMPOTENT,
        icon="sliders-horizontal",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SettingReadInput,
        config: SettingReadConfig,
    ) -> NodeResult[SettingValueOutput]:
        _ = config
        if not inputs.key:
            return await self._read_feature(ctx, inputs.feature)
        name = f"{inputs.feature}/{inputs.key}"
        reader = get_setting_reader()
        if reader is None:
            return failure(
                "setting_reader_missing",
                f"Setting {name} cannot be read: this server installed no setting reader "
                "(matrx_graph.settings.set_setting_reader).",
            )
        org = ctx.organization_id
        try:
            user = getattr(ctx, "user_id", None)
            value = await reader(inputs.feature, inputs.key, str(org) if org else None, str(user) if user else None)
        except Exception as e:  # noqa: BLE001 — named failure, never a silent default
            return failure(
                "setting_unreadable",
                f"Setting {name} could not be read ({type(e).__name__}: {e}).",
                details={"feature": inputs.feature, "key": inputs.key},
            )
        return success(SettingValueOutput(feature=inputs.feature, key=inputs.key, value=value))

    async def _read_feature(self, ctx: NodeExecutionContext, feature: str) -> NodeResult[SettingValueOutput]:
        """Every setting of ``feature`` in one call: ``{name: {"value": ..., "source": ...}}``."""
        feature_reader = get_feature_settings_reader()
        if feature_reader is None:
            return failure(
                "setting_reader_missing",
                f"The settings of {feature} cannot be read: this server installed no feature-settings reader "
                "(matrx_graph.settings.set_feature_settings_reader).",
            )
        org = ctx.organization_id
        user = getattr(ctx, "user_id", None)
        try:
            found = await feature_reader(feature, str(org) if org else None, str(user) if user else None)
        except Exception as e:  # noqa: BLE001 — named failure, never a silent default
            return failure(
                "setting_unreadable",
                f"The settings of {feature} could not be read ({type(e).__name__}: {e}).",
                details={"feature": feature},
            )
        value: dict[str, JsonValue] = {name: {"value": v, "source": src} for name, (v, src) in found.items()}
        return success(SettingValueOutput(feature=feature, key="", value=value))
