import html
import sys

import click
from prompt_toolkit import print_formatted_text, HTML

def colored_text(s: str, text_color: str):
    return HTML(f'<ansi{text_color}>{html.escape(s)}</ansi{text_color}>')

def colored_print(s: str, nl = True, text_color: str = None, err = False):
    try:
        print_formatted_text(colored_text(s, text_color), file=sys.stderr if err else None, end='\n' if nl else '')
    except:
        click.echo(s, err=err, nl=nl)

class Color:
    gray = 'gray'
    brightblue = 'brightblue'