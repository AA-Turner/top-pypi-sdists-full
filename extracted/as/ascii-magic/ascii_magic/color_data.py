class ColorData:
    def __init__(
        self,
        character: str,
        terminal_color: str,
        terminal_hex_color: str,
        full_hex_color: str,
    ):
        self.character = character
        self.terminal_color = terminal_color
        self.terminal_hex_color = terminal_hex_color
        self.full_hex_color = full_hex_color
