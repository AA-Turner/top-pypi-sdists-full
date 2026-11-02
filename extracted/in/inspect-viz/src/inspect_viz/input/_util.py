from typing import Any

from inspect_viz._core.component import Component


def input_component(config: dict[str, Any]) -> Component:
    return Component(config=config, bind_spec=True, bind_tables="empty")
