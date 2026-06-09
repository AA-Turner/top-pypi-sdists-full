"""Create an inline SVG sparkline string for the given sequence of numbers.

Usage:
    python svg_sparkline.py 1 2 3 4 5
    python svg_sparkline.py 1 2 3 4 5 --width 200 --color blue --line-width 2.0
"""

import argparse
from typing import List, Union


def sparkline0(
    numbers: List[Union[int, float]],
    width: int = 100,
    height: int = 30,
    color: str = "red",
    line_width: float = 1.0,
) -> str:
    """Create an inline SVG sparkline string for the given sequence of numbers.

    Parameters
    ----------
    numbers : List[Union[int, float]]
        Sequence of numeric values to plot
    width : int, optional
        Width of the SVG in pixels (default: 100)
    height : int, optional
        Height of the SVG in pixels (default: 30)
    color : str, optional
        color color in CSS format (default: "red")
    line_width : float, optional
        Thickness of the line (default: 1.0)

    Returns
    -------
    str
        Complete SVG string ready to be embedded inline in HTML/Markdown with no newlines.
    """
    if not numbers:
        return f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}"></svg>'

    # Handle constant values or single-element lists gracefully
    if len(numbers) == 1:
        numbers = [numbers[0], numbers[0]]

    min_val = min(numbers)
    max_val = max(numbers)
    value_range = max_val - min_val

    # Avoid division by zero when all values are identical
    if value_range == 0:
        # Center the flat line vertically
        y_mid = height / 2
        path_data = f"M 0 {y_mid} L {width} {y_mid}"
    else:
        # Scale values to [0, height] (inverted y-axis: min → bottom)
        scaled = [(val - min_val) / value_range * (height - 4) + 2 for val in numbers]
        # x-coordinates are evenly spaced
        x_coords = [i * width / (len(numbers) - 1) for i in range(len(numbers))]

        # Build path data: M = move to, L = line to
        commands = [f"M {x_coords[0]:.1f} {height - scaled[0]:.1f}"]
        for x, y in zip(x_coords[1:], scaled[1:]):
            commands.append(f"L {x:.1f} {height - y:.1f}")
        path_data = " ".join(commands)

    # Construct the SVG string
    svg = (
        f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
        f'preserveAspectRatio="none" style="vertical-align: middle;">'
        f'<path d="{path_data}" fill="none" stroke="{color}" stroke-width="{line_width}" '
        f'color-linecap="round" color-linejoin="round"/>'
        f"</svg>"
    )

    return svg


def sparkline(
    numbers: List[Union[int, float]],
    width: int = 100,
    color: str = "red",
    line_width: float = 1.0,
    view_height: int = 20,  # ViewBox height units (controls aspect ratio)
    padding: float = 2.0,  # Vertical padding inside viewBox
) -> str:
    """Generate an inline SVG sparkline string optimized for embedding within paragraph text.

    The resulting SVG has no fixed pixel height attribute; instead, it uses CSS `height: 1.2ex`
    to scale naturally with the surrounding font size. This minimizes layout disruption in
    Markdown renderers such as Obsidian.

    Parameters
    ----------
    numbers : List[Union[int, float]]
        Sequence of numeric values to plot
    width : int, optional
        Width of the SVG in pixels (default: 100)
    color : str, optional
        Stroke color in CSS format (default: "red")
    line_width : float, optional
        Thickness of the line (default: 1.0)
    view_height : int, optional
        Height of the viewBox coordinate system (default: 20); together with width
        this controls the intrinsic aspect ratio
    padding : float, optional
        Vertical padding inside the viewBox (default: 2.0 units)

    Returns
    -------
    str
        Complete SVG string (single line, no newlines) suitable for inline HTML/Markdown
    """
    if not numbers:
        return f'<svg width="{width}" viewBox="0 0 {width} {view_height}"></svg>'

    # Duplicate single value for a visible (flat) line
    if len(numbers) == 1:
        numbers = [numbers[0], numbers[0]]

    min_val = min(numbers)
    max_val = max(numbers)
    value_range = max_val - min_val

    # Effective plotting height inside viewBox
    plot_height = view_height - 2 * padding

    if value_range == 0:
        # Flat line centered vertically
        y_mid = view_height / 2
        path_data = f"M 0 {y_mid:.1f} L {width} {y_mid:.1f}"
    else:
        # Scale values to plot_height and apply padding
        scaled = [
            (val - min_val) / value_range * plot_height + padding for val in numbers
        ]
        # x-coordinates evenly spaced across full width
        x_coords = [i * width / (len(numbers) - 1) for i in range(len(numbers))]

        # Build path (y inverted: 0 at top)
        commands = [f"M {x_coords[0]:.1f} {view_height - scaled[0]:.1f}"]
        for x, y in zip(x_coords[1:], scaled[1:]):
            commands.append(f"L {x:.1f} {view_height - y:.1f}")
        path_data = " ".join(commands)

    # Construct compact inline SVG
    svg = (
        f'<svg viewBox="0 0 {width} {view_height}" '
        f'width="{width}" '
        f'style="height:2.0ex; vertical-align:middle; margin:0 0.3em;" '
        f'preserveAspectRatio="xMidYMid meet">'
        f'<path d="{path_data}" fill="none" stroke="{color}" stroke-width="{line_width}" '
        f'stroke-linecap="round" stroke-linejoin="round"/>'
        f"</svg>"
    )

    return svg


def main():
    parser = argparse.ArgumentParser(
        description="Generate an SVG sparkline for the given numbers"
    )
    parser.add_argument(
        "numbers", nargs="+", type=float, help="The numbers to generate a sparkline for"
    )
    parser.add_argument(
        "--width", type=int, default=100, help="The width of the sparkline in pixels"
    )
    parser.add_argument(
        "--color", type=str, default="red", help="The color of the sparkline"
    )
    parser.add_argument(
        "--line-width", type=float, default=1.0, help="The width of the line"
    )
    args = parser.parse_args()
    svg_code = sparkline(
        args.numbers, width=args.width, color=args.color, line_width=args.line_width
    )
    print(svg_code)


def test_sparkline():
    html = """
<html>
    <body>
    <p>
        <b>This is a test of the SVG sparkline function.</b>
    </p>

{svg_code}

    <p>
        The quick brown fox jumps {svg_code2} over the lazy dog.
        The quick brown fox jumps {svg_code2} over the lazy dog.
        The quick brown fox jumps {svg_code2} over the lazy dog.
        The quick brown fox jumps {svg_code2} over the lazy dog.
    </p>

    </body>
</html>
"""
    data = [
        [(0, 100), {"width": 100, "color": "red", "line_width": 1.0}],
        [(0, 100, 0), {"width": 100, "color": "red", "line_width": 1.0}],
        [
            (0, 25, 0, 50, 0, 75, 0, 100),
            {"width": 100, "color": "red", "line_width": 1.0},
        ],
        [
            (0, 25, 0, 50, 0, 75, 0, 100),
            {"width": 200, "color": "red", "line_width": 1.0},
        ],
        [(3, 1, 4, 1, 5, 9, 2, 6), {"width": 100, "color": "red", "line_width": 1.0}],
        [(3, 1, 4, 1, 5, 9, 2, 6), {"width": 100, "color": "red", "line_width": 2.0}],
        [(3, 1, 4, 1, 5, 9, 2, 6), {"width": 100, "color": "green", "line_width": 2.0}],
    ]
    svg_snippets = [
        "    <p>%s %s</p>\n    <p>%s</p>\n<br/>"
        % (numbers, params, sparkline(numbers, **params))
        for numbers, params in data
    ]
    svg_code2 = sparkline(
        [0, 25, 0, 50, 0, 75, 0, 100], width=100, color="green", line_width=2.0
    )
    html = html.format(svg_code="\n".join(svg_snippets), svg_code2=svg_code2)
    with open("test_sparkline.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    # main()
    test_sparkline()
