import textwrap

import numpy as np


class PrettyTable:
    def __init__(self, header: list, padding: int = 18) -> None:
        self.header = header
        self.padding = padding
        self.row_separator = None
        self.format_string = [".2f" for _ in self.header]
        self.format_string[0] = "d"
        self.header_lines = self._get_header_lines()
        self.width = len(self.get_header_separator())
        self.wrapper = textwrap.TextWrapper()
        self.wrapper.width = self.width - 2
        self.wrapper.subsequent_indent = "    "

    def get_header(self) -> str:
        return (
            "|"
            + "|".join(self.aligned_to_center(self.padding, header) for header in self.header)
            + "|"
        )

    def get_row(self, *args) -> str:
        return (
            "|"
            + "|".join(self.aligned_to_center(self.padding, val) for ii, val in enumerate(args))
            + "|"
        )

    def get_row_separator(self) -> str:
        if not self.row_separator:
            self.row_separator = self._get_separator()
        return self.row_separator

    def get_header_separator(self) -> str:
        return self._get_separator(fill="=")

    def _get_separator(self, column_sign="+", fill="-") -> str:
        return "".join(column_sign + fill * self.padding for _ in self.header) + column_sign

    def get_header_lines(self) -> str:
        return self.header_lines

    def _get_header_lines(self) -> str:
        return (
            self.get_row_separator() + "\n" + self.get_header() + "\n" + self.get_header_separator()
        )

    def get_footer(self, footer_text: str):
        footer = self.get_header_separator() + "\n"
        footer_lines = self.wrapper.wrap(" " + footer_text)
        for fl in footer_lines:
            footer += f"{self._get_footer_line(fl)}\n"
        footer += self.get_header_separator() + "\n"
        return footer

    def _get_footer_line(self, footer_line):
        return "| " + footer_line + " " * (self.width - len(footer_line) - 3) + "|"

    @staticmethod
    def aligned_to_center(padding: int, content: str, fill: str = " ") -> str:
        shift = 0

        if content.startswith("-"):
            shift = 1

        return (
            fill * (int(np.ceil((padding - len(content)) / 2)) - shift)
            + content
            + fill * (padding - len(content) - int(np.ceil((padding - len(content)) / 2)) + shift)
        )


if __name__ == "__main__":
    t = PrettyTable(["Acq.", "samx", "samy"])
    t.get_header()
