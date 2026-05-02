from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

STARTUP_SEQUENCE_STEPS = (
    ("bind.identity", "Locking the Aegis identity and companion posture"),
    ("recover.memory", "Recovering durable memory and recent clone context"),
    ("score.next_move", "Scoring the next long-horizon move"),
    ("enter.dialogue", "Opening the branded dialogue surface"),
)


@dataclass(frozen=True, slots=True)
class BootFrameContext:
    display_name: str
    growth_stage_title: str
    growth_level: int
    provider_model: str
    viewport_width: int
    viewport_height: int


def render_boot_frame(
    *,
    context: BootFrameContext,
    steps: tuple[tuple[str, str], ...],
    active: int,
    rich_available: bool,
    table_cls: Any,
    group_cls: Any,
    text_cls: Any,
    panel_cls: Any,
    align_cls: Any,
    brand_accent: str,
    brand_accent_strong: str,
    brand_light: str,
    brand_muted: str,
    brand_dark: str,
    center_brand_block: Callable[[Any], Any],
    brand_mark: Any,
):
    if not rich_available or table_cls is None or group_cls is None:
        return text_cls("Aegis booting...")
    current_index = max(0, min(active, len(steps) - 1))
    current_label, current_detail = steps[current_index]

    heading = text_cls(justify="center", no_wrap=True)
    heading.append("AEGIS // wake\n", style=f"bold {brand_accent}")
    heading.append("Opening the persistent dialogue surface", style=brand_muted)

    meta = text_cls(justify="center", no_wrap=True)
    meta.append(f"{context.display_name}\n", style=f"bold {brand_light}")
    meta.append("persistent memory · long-horizon decisions · long context\n", style=brand_muted)
    meta.append(
        f"{context.growth_stage_title} · Lv.{context.growth_level} · {context.provider_model or '<unset>'}",
        style=brand_accent_strong,
    )

    active_step = text_cls(justify="center", no_wrap=True)
    active_step.append(f"{current_label}\n", style=f"bold {brand_accent}")
    active_step.append(current_detail, style=brand_light)

    progress = text_cls(justify="center", no_wrap=True)
    for index, (label, _) in enumerate(steps):
        if index < current_index:
            marker = "●"
            style = brand_accent
        elif index == current_index:
            marker = "◉"
            style = f"bold {brand_accent_strong}"
        else:
            marker = "○"
            style = "#4f5560"
        progress.append(f"{marker} {label}", style=style)
        if index < len(steps) - 1:
            progress.append("   ", style=brand_dark)

    footer = text_cls(justify="center", no_wrap=True)
    footer.append("init seeds the identity · wake opens the live thread", style=brand_muted)

    boot = table_cls.grid(expand=True)
    boot.add_column(no_wrap=True)
    boot.add_row(center_brand_block(heading))
    boot.add_row(text_cls(" "))
    boot.add_row(center_brand_block(brand_mark))
    boot.add_row(text_cls(" "))
    boot.add_row(center_brand_block(meta))
    boot.add_row(text_cls(" "))
    boot.add_row(center_brand_block(active_step))
    boot.add_row(text_cls(" "))
    boot.add_row(center_brand_block(progress))
    boot.add_row(text_cls(" "))
    boot.add_row(center_brand_block(footer))

    panel_width = None
    if context.viewport_width >= 88:
        panel_width = min(108, max(72, context.viewport_width - 10))
    panel = panel_cls(
        boot,
        title=f"[bold {brand_accent}]Boot sequence[/bold {brand_accent}]",
        subtitle=f"[bold {brand_light}]Here with you, built to stay.[/bold {brand_light}]",
        border_style=brand_accent,
        padding=(1, 3),
        width=panel_width,
    )
    if align_cls is None:
        return panel
    return align_cls(panel, align="center", vertical="middle", height=max(24, context.viewport_height))
