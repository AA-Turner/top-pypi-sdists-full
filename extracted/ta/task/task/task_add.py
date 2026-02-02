import click

from task import database
from task import utils


@click.group(
    name='add',
    cls=utils.AliasedGroup,
    default='new-task',
    default_if_no_args=True,
)
def main():
    """Add task"""


@main.command()
@click.argument('task', type=click.STRING)
@click.option('-p', '--project', help="specyfiy project")
@click.option('-u', '--urgency', help="urgency")
@click.option('-d', '--due', help="due date")
def new_task(
    task: str, project: str = None, urgency: int = 0, due: str = None
):
    """Add task to database."""
    db = database.sql_init()
    table = database.setup_todo_table(db)
    task_data = dict()
    task_data['task'] = task
    task_data['project'] = project
    task_data['urgency'] = urgency
    task_data['due'] = utils.parse_due(due)
    task_data['created_at'] = utils.format_current_time()
    task_data['updated_at'] = utils.format_current_time()
    task_id = database.insert_task(db, table, task_data)
    utils.info(f"added task {task_id}")
