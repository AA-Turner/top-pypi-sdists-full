import click

from task import database
from task import utils


@click.group(
    name='rm',
    cls=utils.AliasedGroup,
    default='remove-task',
    default_if_no_args=True,
)
def main():
    """Remove a task."""


@main.command()
@click.argument('task_id', type=click.INT)
def remove_task(task_id: int = 0) -> int:
    """Remove a task."""
    if utils.does_db_exist()[0] is False:
        utils.error("Database not found")
        return 1
    db = database.sql_init()
    table = database.setup_todo_table(db)

    if database.does_task_exist(db, table, task_id) is False:
        utils.error(f"task {task_id} does not exist")
        return 2

    database.remove_task(db, table, task_id)
    utils.info(f"Removed task {task_id}")
    return task_id
