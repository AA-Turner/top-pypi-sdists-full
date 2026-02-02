import click

from task import database
from task import utils


@click.group(
    name='done',
    cls=utils.AliasedGroup,
    default='task-done',
    default_if_no_args=True,
)
def main():
    """Finished task."""


@main.command()
@click.argument('task_id', type=click.INT)
def task_done(task_id: int = 0) -> int:
    """Task is done."""
    if utils.does_db_exist()[0] is False:
        # TODO better prints than this
        utils.error("Database not found")
        return 1

    db = database.sql_init()
    table = database.setup_todo_table(db)

    ret = database.set_task_done(db, table, task_id)
    if ret == 0:
        utils.info(f"Done {task_id}")
    else:
        utils.error(f"Task {task_id} does not exist")
