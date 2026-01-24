import os
import sys

import click


def detect_terminal_capabilities():
    """Detect terminal color and Unicode capabilities"""
    # Check for true color support
    colorterm = os.environ.get("COLORTERM", "").lower()
    term = os.environ.get("TERM", "").lower()
    term_program = os.environ.get("TERM_PROGRAM", "").lower()

    # Known terminals with good true color support
    modern_terminals = ["warp", "ghostty", "iterm2", "alacritty", "kitty", "hyper"]

    # Check for true color support
    has_truecolor = (
        colorterm in ["truecolor", "24bit"]
        or term_program in modern_terminals
        or "truecolor" in term
        or "24bit" in term
    )

    # Check if it's standard macOS Terminal
    is_macos_terminal = term_program == "apple_terminal"

    # Check for Unicode support (most modern terminals support this)
    has_unicode = sys.stdout.encoding and "utf" in sys.stdout.encoding.lower()

    return {
        "truecolor": has_truecolor and not is_macos_terminal,
        "unicode": has_unicode,
        "is_macos_terminal": is_macos_terminal,
    }


def display_banner():
    reset = "\033[0m"
    capabilities = detect_terminal_capabilities()

    click.echo("\n")

    banner = [
        "  ████████╗██╗███╗   ██╗██╗   ██╗██████╗ ██╗██████╗ ██████╗     ██████╗ ██████╗ ██████╗ ███████╗",
        "  ╚══██╔══╝██║████╗  ██║╚██╗ ██╔╝██╔══██╗██║██╔══██╗██╔══██╗   ██╔════╝██╔═══██╗██╔══██╗██╔════╝",
        "     ██║   ██║██╔██╗ ██║ ╚████╔╝ ██████╔╝██║██████╔╝██║  ██║   ██║     ██║   ██║██║  ██║█████╗  ",
        "     ██║   ██║██║╚██╗██║  ╚██╔╝  ██╔══██╗██║██╔══██╗██║  ██║   ██║     ██║   ██║██║  ██║██╔══╝  ",
        "     ██║   ██║██║ ╚████║   ██║   ██████╔╝██║██║  ██║██████╔╝   ╚██████╗╚██████╔╝██████╔╝███████╗",
        "     ╚═╝   ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═════╝ ╚═╝╚═╝  ╚═╝╚═════╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝",
    ]

    def rgb_to_ansi(r: int, g: int, b: int, use_truecolor: bool):
        """Convert RGB values to ANSI escape code"""
        if use_truecolor:
            return f"\033[38;2;{r};{g};{b}m"

        # Convert to 8-bit color (256 color palette)
        # Simple approximation: map RGB to 216-color cube + grayscale
        if r == g == b:
            # Grayscale
            gray = int(r / 255 * 23) + 232
            return f"\033[38;5;{gray}m"

        # Color cube (6x6x6)
        r_idx = int(r / 255 * 5)
        g_idx = int(g / 255 * 5)
        b_idx = int(b / 255 * 5)
        color_idx = 16 + (36 * r_idx) + (6 * g_idx) + b_idx
        return f"\033[38;5;{color_idx}m"

    # Define solid color (corresponding to #27f795)
    solid_color = [39, 247, 149]  # #27f795 in RGB

    # Print each line with solid color for all terminals
    for line in banner:
        colored_line = ""
        color_code = rgb_to_ansi(*solid_color, use_truecolor=capabilities["truecolor"])  # type: ignore

        for char in line:
            if char == " ":
                colored_line += char
            else:
                colored_line += f"{color_code}{char}"

        click.echo(colored_line + reset)
    click.echo("")
