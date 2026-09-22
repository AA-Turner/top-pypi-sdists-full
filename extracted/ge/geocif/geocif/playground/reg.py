from chainlit import run, UIComponent
from chainlit.components import SidebarPane
from chainlit.widgets import ForestPlot
from database_handler import query_papers
import pandas as pd


def mock_forest_plot_data():
    """
    Provide mock data for the forest plot.
    """
    return [
        {"label": "Agroforestry", "effect_size": 0.45, "ci_lower": 0.30, "ci_upper": 0.60},
        {"label": "Cover Cropping", "effect_size": 0.32, "ci_lower": 0.20, "ci_upper": 0.45},
        {"label": "Reduced Tillage", "effect_size": 0.28, "ci_lower": 0.15, "ci_upper": 0.40},
        {"label": "Organic Amendments", "effect_size": 0.50, "ci_lower": 0.35, "ci_upper": 0.65},
        {"label": "Reforestation", "effect_size": 0.70, "ci_lower": 0.50, "ci_upper": 0.90}
    ]


@run
def main():
    # Initialize the UI components
    ui_component = UIComponent(
        SidebarPane(
            title="Impact Visualization",
            content=ForestPlot(
                data=mock_forest_plot_data(),
                x_label="Effect Size",
                y_label="Intervention",
                title="Forest Plot: Impact of Interventions"
            )
        )
    )
    # Start the application
    ui_component.render()
