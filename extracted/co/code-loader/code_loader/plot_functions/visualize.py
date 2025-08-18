# mypy: ignore-errors

import sys

from code_loader.contract.datasetclasses import LeapData

from typing import Optional

from code_loader.plot_functions.plot_functions import plot_switch, run_only_on_non_mapping_mode


@run_only_on_non_mapping_mode()
def visualize(leap_data: LeapData, title: Optional[str] = None) -> None:
    vis_function = plot_switch.get(leap_data.type)
    if vis_function is None:
        print(f"Error: leap data type is not supported, leap data type: {leap_data.type}")
        sys.exit(1)

    if not title:
        title = f"Leap {leap_data.type.name} Visualization"
    vis_function(leap_data, title)  # type: ignore[operator]

