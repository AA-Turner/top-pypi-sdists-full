from typing import Optional

import reacton
import reacton.ipyvuetify as v
from solara.lab import Ref

from .state import load_data

_items = {
    "Quick-start": ["carshare", "election", "iris", "medals_long", "medals_wide", "palmerpenguins", "tips", "wind"],
    "Economics": ["gapminder", "stocks", "stocks_long"],
    "Pharma": ["experiment", "small_molecule_drugbank"],
}


@reacton.component
def QuickStart():
    load_data.use()
    demo_df_name = Ref(load_data.fields.demo_df_name)

    def find_selected_index(df_name: str) -> Optional[int]:
        for i, (category, items) in enumerate(_items.items()):
            if df_name in items:
                return i
        return None

    selected_index = find_selected_index(demo_df_name.value)

    expanded, set_expanded = reacton.use_state(selected_index)

    with v.ExpansionPanels(v_model=expanded, on_v_model=set_expanded, accordeon=True, style_="width: 800px") as main:
        for i, category in enumerate(_items.keys()):
            with v.ExpansionPanel():
                v.ExpansionPanelHeader(
                    children=[
                        v.Html(tag="strong", children=[f"{category} ({demo_df_name.value})"]) if selected_index == i and expanded != i else category,
                    ]
                )
                with v.ExpansionPanelContent():
                    with v.List():
                        selected = demo_df_name.get() if demo_df_name.get() in _items[category] else None
                        with v.ListItemGroup(
                            color="primary", v_model=selected, on_v_model=lambda v: demo_df_name.set(v) if v else None, mandatory=expanded == i
                        ):
                            for item in _items[category]:
                                with v.ListItem(value=item).key(item + "|list"):
                                    with v.ListItemAvatar():
                                        v.Icon(children=["mdi-check-box-outline" if demo_df_name.get() == item else "mdi-checkbox-blank-outline"])
                                    with v.ListItemContent():
                                        v.ListItemTitle(children=[item])
    return main
