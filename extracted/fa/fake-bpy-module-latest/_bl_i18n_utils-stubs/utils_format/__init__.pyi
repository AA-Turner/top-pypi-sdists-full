import typing
import collections.abc
import typing_extensions
import numpy.typing as npt

class FormatToken:
    fmt_format_codes: typing.Any
    fmt_format_widthprec: typing.Any
    key: typing.Any
    printf_format_codes: typing.Any
    printf_format_datasize: typing.Any
    printf_format_flags: typing.Any
    printf_format_widthprec: typing.Any
    quick_re_check: typing.Any
    start_index: typing.Any
    token: typing.Any

    @classmethod
    def has_potential_formatting(cls, string, start=0) -> None:
        """

        :param string:
        :param start:
        """

    @classmethod
    def next_potential_formatting_index(cls, string, start=0) -> None:
        """

        :param string:
        :param start:
        """

    @classmethod
    def parse_string(cls, string) -> None:
        """Iterator over specific formatting sequences (like %s, {:.4f}, etc.) in the given string,
        yielding instances of FormatToken.NOTE: This is not covering all exotic syntax cases of printf or format!

                :param string:
        """

    @classmethod
    def parse_string_lookup_first_token(
        cls, string, start_idx, token_idx=0, only_at_start_idx=False
    ) -> None:
        """Search for the first instance of a formatting sequences (like %s, {:.4f}, etc.) in the given string,
        and return a FormatToken for it (or None is none is found).NOTE: This is not covering all exotic syntax cases of printf or format!If only_at_start_idx is True, this function will only return a valid token if it starts at given start_idx.
        Useful e.g. for code already calling next_potential_formatting_index itself.

                :param string:
                :param start_idx:
                :param token_idx:
                :param only_at_start_idx:
        """
