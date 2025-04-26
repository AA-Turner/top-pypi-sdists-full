"""Utils for formatting event messages"""
import shutil
import textwrap

from mcli.utils.utils_date import format_timestamp
from mcli.utils.utils_event_type import EventType


def calculate_max_event_line_width(events, time_header_width, resumption_header_width, width_padding=4):
    table_width = shutil.get_terminal_size()[0] - width_padding
    max_event_time_width = max(len(format_timestamp(event.event_time)) for event in events)
    time_column_width = max(time_header_width, max_event_time_width) + width_padding
    max_resumption_event_width = max(len(str(event.resumption_index)) for event in events)
    resumption_column_width = max(resumption_header_width, max_resumption_event_width) + width_padding
    max_line_width = table_width - time_column_width - resumption_column_width - width_padding
    return max_line_width


def format_event_message(event_message, event_type, max_line_width, indent_size=2):
    if event_type != EventType.FAILED_EXCEPTION:
        return event_message

    wrapper = textwrap.TextWrapper(width=max_line_width,
                                   initial_indent='',
                                   subsequent_indent=' ' * indent_size,
                                   break_long_words=False)
    lines = event_message.splitlines()
    formatted_lines = []

    for idx, line in enumerate(lines):
        if idx == 0:
            line = f"[red]{line}[/]"

        if len(line) > max_line_width:
            # If line exceeds max_line_width, wrap and indent
            wrapped_lines = wrapper.wrap(line)
            formatted_lines.extend(wrapped_lines)
        else:
            formatted_lines.append(line)

    return '\n'.join(formatted_lines)
