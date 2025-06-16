from importlib.metadata import version

import rich_click as click
from rich.console import Console
from rich.table import Table

from pycnpj_cpf.core import cnpj_or_cpf_is_valid

click.rich_click.USE_RICH_MARKUP = True
click.rich_click.USE_MARKDOWN = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.SHOW_METAVARS_COLUMN = True
click.rich_click.APPEND_METAVARS_HELP = True


@click.group()
@click.version_option(version('pycnpj-cpf'))
def main():
    """CNPJ and CPF validator.
    This cli application validates if the CNPJ/CPF entered is valid.
    """


@main.command()
@click.option('-v', '--value', help='Value to be validated.', required=True)
def validate(value: str) -> bool:
    table = Table(title='CNPJ and CPF validator')
    headers = ['CNPJ/CPF', 'Is Valid?']
    for header in headers:
        table.add_column(header, style='magenta')

    result = cnpj_or_cpf_is_valid(value)
    table.add_row(f'{value}', str(result))
    console = Console()
    console.print(table)
