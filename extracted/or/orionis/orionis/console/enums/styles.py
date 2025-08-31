from enum import Enum

class ANSIColors(Enum):
    """
    ANSI escape codes for styling text and backgrounds in terminal applications.

    This Enum provides a comprehensive set of ANSI escape codes for coloring and styling
    text output in console applications. It includes codes for foreground (text) colors,
    background colors, bold and underlined styles, as well as additional effects such as
    dim, italic, and magenta. These codes can be used to enhance the readability and
    emphasis of console messages, such as errors, warnings, informational, and success messages.

    Attributes
    ----------
    DEFAULT : str
        ANSI code to reset all colors and styles to the terminal's default.
    BG_INFO : str
        ANSI code for a blue background, typically used for informational messages.
    BG_ERROR : str
        ANSI code for a red background, typically used for error messages.
    BG_FAIL : str
        ANSI code for a specific red background, often used for failure messages.
    BG_WARNING : str
        ANSI code for a yellow background, typically used for warnings.
    BG_SUCCESS : str
        ANSI code for a green background, typically used for success messages.
    TEXT_INFO : str
        ANSI code for blue foreground text, used for informational messages.
    TEXT_ERROR : str
        ANSI code for bright red foreground text, used for errors.
    TEXT_WARNING : str
        ANSI code for yellow foreground text, used for warnings.
    TEXT_SUCCESS : str
        ANSI code for green foreground text, used for success messages.
    TEXT_WHITE : str
        ANSI code for white foreground text, useful for contrast.
    TEXT_MUTED : str
        ANSI code for gray (muted) foreground text, used for secondary information.
    TEXT_BOLD_INFO : str
        ANSI code for bold blue foreground text, emphasizing informational messages.
    TEXT_BOLD_ERROR : str
        ANSI code for bold red foreground text, emphasizing errors.
    TEXT_BOLD_WARNING : str
        ANSI code for bold yellow foreground text, emphasizing warnings.
    TEXT_BOLD_SUCCESS : str
        ANSI code for bold green foreground text, emphasizing success messages.
    TEXT_BOLD_WHITE : str
        ANSI code for bold white foreground text, for strong contrast.
    TEXT_BOLD_MUTED : str
        ANSI code for bold gray (muted) foreground text, for emphasized secondary information.
    TEXT_BOLD : str
        ANSI code for bold text style.
    TEXT_STYLE_UNDERLINE : str
        ANSI code for underlined text style.
    TEXT_RESET : str
        ANSI code to reset text styles to default settings.
    CYAN : str
        ANSI code for cyan foreground text, for special emphasis.
    DIM : str
        ANSI code for dimmed foreground text, for subtle emphasis.
    MAGENTA : str
        ANSI code for magenta foreground text, for special emphasis.
    ITALIC : str
        ANSI code for italicized foreground text, for special emphasis.

    Returns
    -------
    str
        The ANSI escape code string corresponding to the selected color or style.
    """

    DEFAULT = '\033[0m'                 # Reset all colors and styles

    # Background Colors
    BG_INFO = '\033[44m'                # Blue background for informational messages
    BG_ERROR = '\033[41m'               # Red background for error messages
    BG_FAIL = '\033[48;5;166m'          # Specific red background for failure messages
    BG_WARNING = '\033[43m'             # Yellow background for warning messages
    BG_SUCCESS = '\033[42m'             # Green background for success messages

    # Foreground Text Colors
    TEXT_INFO = '\033[34m'              # Blue text for informational messages
    TEXT_ERROR = '\033[91m'             # Bright red text for errors
    TEXT_WARNING = '\033[33m'           # Yellow text for warnings
    TEXT_SUCCESS = '\033[32m'           # Green text for success messages
    TEXT_WHITE = '\033[97m'             # White text for high contrast
    TEXT_MUTED = '\033[90m'             # Gray (muted) text for secondary information

    # Bold Foreground Text Colors
    TEXT_BOLD_INFO = '\033[1;34m'       # Bold blue text for informational emphasis
    TEXT_BOLD_ERROR = '\033[1;91m'      # Bold red text for error emphasis
    TEXT_BOLD_WARNING = '\033[1;33m'    # Bold yellow text for warning emphasis
    TEXT_BOLD_SUCCESS = '\033[1;32m'    # Bold green text for success emphasis
    TEXT_BOLD_WHITE = '\033[1;97m'      # Bold white text for strong contrast
    TEXT_BOLD_MUTED = '\033[1;90m'      # Bold gray (muted) text for emphasized secondary info

    # Additional Text Styles
    TEXT_BOLD = "\033[1m"               # Bold text style
    TEXT_STYLE_UNDERLINE = '\033[4m'    # Underlined text style
    TEXT_RESET = "\033[0m"              # Reset all text styles to default
    CYAN = "\033[36m"                   # Cyan text for special emphasis
    DIM = "\033[2m"                     # Dim text for subtle emphasis
    MAGENTA = "\033[35m"                # Magenta text for special emphasis
    ITALIC = "\033[3m"                  # Italic text for special emphasis