from datetime import datetime

import click
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

from task import database
from task import utils


@click.group(
    name='ls',
    cls=utils.AliasedGroup,
    default='list-tasks',
    default_if_no_args=True,
)
def main():
    """List tasks."""


def get_due_percent(due: datetime, created_at: datetime) -> int:
    """Convert due of task to percent."""

    if due is None:
        return 0
    ts_now = datetime.timestamp(datetime.now())
    ts_created_at = datetime.timestamp(created_at)
    ts_due = datetime.timestamp(due)
    ts_spent_time = ts_now - ts_created_at
    ts_duration = ts_due - ts_created_at

    spent_time = ts_spent_time / ts_duration
    spent_time_percent = spent_time * 100
    return int(spent_time_percent)


def get_date_age(task_date: str, is_due: bool = False) -> str:
    """Get age of date."""
    if is_due:
        if task_date is None or task_date == "":
            return ""
        else:
            task_date = f"{str(task_date).split('.')[0]}"
            utils.debug(type(task_date))
            utils.debug((task_date))
            task_date = datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S')
    now = datetime.now()
    if is_due:
        age = relativedelta(task_date, now)
    else:
        age = relativedelta(now, task_date)

    if age.years != 0:
        age = age.years
        age_type = "year"
    elif age.months != 0:
        age = age.months
        age_type = "month"
    elif age.days != 0:
        age = age.days
        age_type = "day"
    elif age.hours != 0:
        age = age.hours
        age_type = "hour"
    elif age.minutes != 0:
        age = age.minutes
        age_type = "minute"
    else:
        age = age.seconds
        age_type = "second"
    return f"{age} {age_type + 's' if age != 1 or age != -1 else age_type}"


def colorize_task_by_percent(task: list, percent: int):
    """Colorize a task by its due percent."""
    reset = '\033[0m'
    red = '\033[91m'
    orange = '\033[93m'
    green = '\033[0;32m'

    # TODO make color a var
    if percent >= 5 and percent <= 8:
        color = orange
    elif percent >= 8:
        color = red
    else:
        color = green
    task[0] = f'{color}{task[0]}'
    task[-1] = f'{task[-1]}{reset}'

    return task


def handle_task_age(due: datetime, dt_row: datetime, task: list):
    """Handle task's age."""
    age = get_date_age(dt_row)
    due_age = get_date_age(due, True)
    task[-1] = f"{age}\x1b[0m"
    task[4] = due_age

    return task


def prettify_tasks(tasks: list) -> list:
    """Set black background
    and red tasks when needed.
    """
    cnt = 0
    new_tasks = list()
    for task in tasks:
        due_percent = get_due_percent(task[4], task[5])
        row_cnt = 0
        new_task = list()
        for row in task:
            if (cnt % 2) != 0:
                new_task.append(f'\x1b[40m{row}')
            else:
                new_task.append(f'{row}')
            if row_cnt == 4:
                due = row
            row_cnt += 1
        new_task = handle_task_age(due, row, new_task)
        new_task = colorize_task_by_percent(new_task, due_percent)
        new_tasks.append(new_task)
        cnt += 1
    return new_tasks


@main.command()
@click.argument('what', type=click.STRING, required=False)
@click.option('-p', '--project', help="list by project")
def list_tasks(what: str = None, project: str = None) -> int:
    """List tasks. You specify 'all' or 'done'"""
    if utils.does_db_exist()[0] is False:
        utils.error("No database found")
        return 1
    db = database.sql_init()
    table = database.setup_todo_table(db)
    tasks = database.get_tasks_list(db, table, what, project)
    header = ("ID", "Project", "Task", "Urgency", "Due", "Age")
    header = utils.prettify_header(header)
    pretty_tasks = prettify_tasks(tasks)
    print(tabulate(pretty_tasks, headers=header, tablefmt="plain"))
