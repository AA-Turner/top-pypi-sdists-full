from typing import List

import reacton.ipyvuetify as v
import solara


@solara.component
def Thumbnail(width: int = 600, height: int = 300, scale: float = 0.3, children: List = []):
    with v.Sheet(
        class_="domino-thumbnail",
        style_=f"height: calc({height}px * {scale}); width: calc({width}px * {scale}); overflow:hidden; position: relative; user-select: none;",
    ) as main:
        v.Sheet(
            style_=f"height: {height}px; width: {width}px; transform: scale({scale}); transform-origin: top left;",
            children=children,
        )
        solara.Div(style_="position: absolute; top: 0; left: 0; bottom: 0; right: 0")

    return main
