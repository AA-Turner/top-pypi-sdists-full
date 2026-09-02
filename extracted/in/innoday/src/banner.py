import os
import sys

import pyfiglet
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


def _supports_color():
    """Check if the terminal supports color output."""
    # Check if we're in a known environment that doesn't support colors
    if os.getenv("NO_COLOR") or os.getenv("TERM") == "dumb":
        return False

    # Check if stdout is a TTY
    if not sys.stdout.isatty():
        return False

    # Check for common color-supporting terminals
    term = os.getenv("TERM", "").lower()
    if any(t in term for t in ["color", "ansi", "xterm", "screen", "tmux", "linux"]):
        return True

    # Default to True on most systems
    return True


def create_banner(component_name="InnoDay", url=None):
    """Create a properly formatted InnoDay ASCII art banner using pyfiglet

    Args:
        component_name: The name of the component (e.g., "InnoDay Vision", "InnoDay Connector")
        url: The URL where the component is running (optional)
    """
    # Check if colors are supported
    use_colors = _supports_color()

    # Generate ASCII art using pyfiglet
    ascii_art = pyfiglet.figlet_format("InnoDay", font="slant")

    # Color the ASCII art with gradient colors (if supported)
    lines = ascii_art.strip().split("\n")
    colored_lines = []

    if use_colors:
        # Define gradient colors
        colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.YELLOW, Fore.MAGENTA, Fore.RED]

        for i, line in enumerate(lines):
            if line.strip():  # Only color non-empty lines
                color = colors[i % len(colors)]
                colored_lines.append(f"{color}{Style.BRIGHT}{line}{Style.RESET_ALL}")
            else:
                colored_lines.append(line)
    else:
        # No colors - use plain text
        colored_lines = lines

    # Calculate the width for the border (use the longest line)
    max_width = (
        max(
            len(
                line.replace("\033[", "")
                .replace("m", "")
                .replace("[0", "")
                .replace("[1", "")
            )
            for line in lines
            if line.strip()
        )
        if lines
        else 0
    )

    # Ensure minimum width for the description text but respect terminal width
    import shutil

    terminal_width = shutil.get_terminal_size().columns
    # Use a reasonable minimum width but don't exceed terminal width
    MIN_BORDER_WIDTH = 78
    border_width = max(min(max_width + 4, terminal_width - 2), MIN_BORDER_WIDTH)

    # Create the banner with proper alignment
    banner_lines = []

    # Define colors or empty strings based on support
    if use_colors:
        border_color = f"{Fore.CYAN}"
        reset_color = f"{Style.RESET_ALL}"
    else:
        border_color = ""
        reset_color = ""

    banner_lines.append(f"{border_color}╔{'═' * (border_width - 2)}╗{reset_color}")
    banner_lines.append(f"{border_color}║{' ' * (border_width - 2)}║{reset_color}")

    # Add the ASCII art lines with proper centering
    import re

    for line in colored_lines:
        if line.strip():
            # Remove all ANSI escape codes for accurate width calculation
            clean_line = re.sub(r"\x1b\[[0-9;]*m", "", line)
            content_length = len(clean_line)
            total_padding = border_width - 2 - content_length
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            banner_lines.append(
                f"{border_color}║{' ' * left_padding}{line}{' ' * right_padding}║{reset_color}"
            )
        else:
            banner_lines.append(
                f"{border_color}║{' ' * (border_width - 2)}║{reset_color}"
            )

    banner_lines.append(f"{border_color}║{' ' * (border_width - 2)}║{reset_color}")

    # Add description with proper centering
    if use_colors:
        description_lines = [
            f"{Fore.YELLOW}{Style.BRIGHT}🤖 {component_name} {Style.RESET_ALL}",
            "",
            f"{Fore.GREEN}AI-Powered Team Orchestration Platform{Style.RESET_ALL}",
            f"{Fore.GREEN}Capture updates • Prepare SCRUM meetings • Direct workloads{Style.RESET_ALL}",
            f"{Fore.GREEN}Organize releases • Connect people to information{Style.RESET_ALL}",
            "",
        ]
    else:
        description_lines = [
            f"🤖 {component_name}",
            "",
            "AI-Powered Team Orchestration Platform",
            "Capture updates • Prepare SCRUM meetings • Direct workloads",
            "Organize releases • Connect people to information",
            "",
        ]

    # Add URL if provided
    if url:
        if use_colors:
            description_lines.extend(
                [
                    f"{Fore.CYAN}🌐 Running at: {Style.BRIGHT}{url}{Style.RESET_ALL}",
                    "",
                ]
            )
        else:
            description_lines.extend(
                [
                    f"🌐 Running at: {url}",
                    "",
                ]
            )

    if use_colors:
        description_lines.append(
            f"{Fore.BLUE}🚀 FastAPI  📊 SQLModel  🔗 Multi-platform {Style.RESET_ALL}"
        )
    else:
        description_lines.append("🚀 FastAPI  📊 SQLModel  🔗 Multi-platform")

    for desc_line in description_lines:
        if desc_line:
            # Remove ANSI codes for width calculation
            clean_desc = re.sub(r"\x1b\[[0-9;]*m", "", desc_line)
            content_length = len(clean_desc)

            # If line is too long, truncate or wrap it
            max_content_width = border_width - 4  # Leave space for borders and padding
            if content_length > max_content_width:
                # For long technical descriptions, try to break at logical points
                if "•" in clean_desc:
                    # Split on bullet points
                    parts = [part.strip() for part in clean_desc.split("•")]
                    if len(parts) > 1:
                        BULLET_AND_ELLIPSIS_LENGTH = 5  # Length of ' • ' + '...'
                        shortened = (
                            parts[0]
                            + " • "
                            + parts[1][
                                : max_content_width
                                - len(parts[0])
                                - BULLET_AND_ELLIPSIS_LENGTH
                            ]
                            + "..."
                        )
                    else:
                        shortened = (
                            parts[0][: max_content_width - 3] + "..."
                        )  # Fallback to truncating the first part
                    desc_line = shortened
                    clean_desc = shortened
                    content_length = len(clean_desc)
                else:
                    # Simple truncation
                    desc_line = clean_desc[: max_content_width - 3] + "..."
                    clean_desc = desc_line
                    content_length = len(clean_desc)

            total_padding = border_width - 2 - content_length
            left_padding = total_padding // 2
            right_padding = total_padding - left_padding
            banner_lines.append(
                f"{border_color}║{' ' * left_padding}{desc_line}{' ' * right_padding}║{reset_color}"
            )
        else:
            banner_lines.append(
                f"{border_color}║{' ' * (border_width - 2)}║{reset_color}"
            )

    banner_lines.append(f"{border_color}║{' ' * (border_width - 2)}║{reset_color}")
    banner_lines.append(f"{border_color}╚{'═' * (border_width - 2)}╝{reset_color}")

    return "\n".join(banner_lines)


def print_startup_banner(name="InnoDay", host=None, port=None):
    """Print startup banner for InnoDay components

    Args:
        name: Component name ("Connector", "Agent", "Vision", or full name)
        host: Host address (optional)
        port: Port number (optional)
    """
    import os

    from .version import get_display_version

    # ANSI color codes
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    # Build component name and URL
    if name in ["Connector", "Agent", "Vision"]:
        component_name = f"InnoDay {name}"
    else:
        component_name = name

    # Build URL if host and port provided
    url = None
    if host and port:
        url = f"http://{host}:{port}"

    # Print the banner
    print(create_banner(component_name, url))

    # Print startup information
    print(
        f"{BOLD}{GREEN}🌟 Starting {component_name} {get_display_version()}...{RESET}"
    )

    # Add environment info
    env_type = "Development" if os.getenv("DEBUG", "False") == "True" else "Production"
    print(f"\n{YELLOW}🔧 Environment: {env_type}{RESET}")
    print(f"{MAGENTA}💾 Database: {_safe_database_target()}{RESET}")
    print()


def _safe_database_target() -> str:
    """Where we are connected, with no credential in it.

    This line used to print `DATABASE_URL` verbatim, so every start-up wrote the
    database password to stdout -- and on a deployed service stdout is the
    platform's log stream, retained and readable by anyone with log access. A
    password is not less exposed for being in a log rather than a file.

    Host, port and database name are the useful part anyway: they answer "am I
    pointed at the right database", which is the only question this banner was
    trying to answer.
    """
    raw = os.getenv("DATABASE_URL", "sqlite:///./innoday.db")

    scheme, sep, rest = raw.partition("://")
    if not sep or "@" not in rest:
        # No credentials to strip -- sqlite paths, or a host-only URL.
        return raw

    # Split on the LAST `@`, not the first, and do not go through urlsplit.
    # Passwords legitimately contain `@`, `/` and `:`, and a password with a `/`
    # in it makes urlsplit read the netloc as ending early -- it then reports a
    # "hostname" taken from the middle of the password and reconstructing from
    # its parts leaks the tail. The final `@` is the one real delimiter here.
    _userinfo, _, host_and_path = rest.rpartition("@")
    return f"{scheme}://{host_and_path}"
