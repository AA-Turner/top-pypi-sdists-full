import os

import ipyvuetify as vy
import solara
import traitlets

images = [
    solara.util.load_file_as_data_url(os.path.join(os.path.dirname(__file__), name), "image/png")
    for name in [
        "hover_cell.png",
        "hover_icon.png",
        "menu.png",
        "load_data.png",
        "code_inserted.png",
        "menu_transform.png",
        "transform.png",
        "menu_visualizations.png",
        "visualizations.png",
        "menu_app.png",
        "app.png",
    ]
]


class TourWidget(vy.VuetifyTemplate):
    template_file = (__file__, "tour.vue")

    texts = traitlets.List(
        default_value=[
            "To start using Code Assist, hover over a code cell and the Code Assist button will appear.",
            "Hover over the Domino icon to open the Code Assist menu.",
            "The menu items are in the order of a general data science workflow. First, you can load data.",
            "Each menu item opens a dialog that guides you through the process and generates code for you.",
            (
                "The generated code is inserted into the notebook and executed. The output of this can be the input of the next step in the menu."
                " You can also edit or add to the code if you want."
            ),
            "Next we can transform the data in Transformations.",
            "Let's remove missing values.",
            "Now we can visualize the data.",
            "Now we can visualize the data.",
            "And finally we can create an app.",
            "And finally we can create an app.",
        ]
    ).tag(sync=True)
    images = traitlets.List(default_value=images).tag(sync=True)
    widths = traitlets.List(default_value=[722, 722, 722, 706, 804, 226.5, 790, 225, 950, 225.5, 853]).tag(sync=True)
    step = traitlets.Int(0).tag(sync=True)
    opened = traitlets.Bool(False).tag(sync=True)
