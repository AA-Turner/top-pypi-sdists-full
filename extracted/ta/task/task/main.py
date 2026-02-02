import platform

import click
from rich import traceback

from task import task_add
from task import task_describe
from task import task_done
from task import task_list
from task import task_rm
from task import utils


__version__ = "0.2.5"

traceback.install()


@click.group(invoke_without_command=True, cls=utils.AliasedGroup)
@click.pass_context
@click.option("-v", "--version", is_flag=True, help="print version")
@click.option("-d", "--debug", is_flag=True, help="debug mode")
def main(ctx, version, debug) -> int:
    if debug:
        utils.log.setLevel("DEBUG")
        utils.debug(f"task {__version__}")
        python = platform.python_implementation()
        python_version = platform.python_version()
        os = platform.uname()
        utils.debug(f"Python: {python} {python_version}")
        utils.debug(f"OS: {os[0]} {os[2]}")
    if version:
        print("task version %s" % __version__)
        print("~matteyeux")
    elif ctx.invoked_subcommand is None:
        click.echo(main.get_help(ctx))
    return 0


main.add_command(task_add.main)
main.add_command(task_list.main)
main.add_command(task_rm.main)
main.add_command(task_done.main)
main.add_command(task_describe.main)


if __name__ == '__main__':
    exit(main())
