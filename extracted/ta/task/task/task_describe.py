import click
from tabulate import tabulate

from task import database
from task import utils


@click.group(
    name='describe',
    cls=utils.AliasedGroup,
    default='describe-task',
    default_if_no_args=True,
)
def main():
    """Describe task."""


def handle_task_description(task: list) -> list:
    """Handle description of one task."""
    status = f"{'done' if task[5] == 1 else 'TODO'}"
    task_table = []
    task_table.append(["ID", task[0]])
    task_table.append(["Project", task[1]])
    task_table.append(["Task", task[2]])
    task_table.append(["Urgency", task[3]])
    task_table.append(["Due", task[4]])
    task_table.append(["Status", status])
    task_table.append(["Create at", task[6]])
    task_table.append(["Last updated", task[7]])
    return task_table


@main.command()
@click.argument('task_id', type=click.INT, required=False)
def describe_task(task_id: int = None) -> int:
    """Describe task."""
    if utils.does_db_exist()[0] is False:
        utils.error("[e] no database found. Please add task first")
        return 1

    db = database.sql_init()
    table = database.setup_todo_table(db)
    try:
        task = database.get_one_task(db, table, task_id)[0]
    except TypeError:
        utils.error(f"No task found with ID {task_id}")
        return 2

    header = ('name', 'value')
    header = utils.prettify_header(header)
    table = handle_task_description(task)

    print(tabulate(table, header, tablefmt='fancy_grid'))
    return 0
