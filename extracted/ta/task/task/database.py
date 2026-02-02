"""Database module working with SQLachemy."""
import datetime

import sqlalchemy
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker

from task import utils


def sql_init(database: str = 'task.db') -> sqlalchemy.engine.base.Engine:
    """Init SQLite3 stuff."""
    db_string = f"sqlite:///{database}"
    utils.debug(db_string)
    db = create_engine(db_string)
    return db


def setup_todo_table(
    db: sqlalchemy.engine.base.Engine,
) -> sqlalchemy.sql.schema.Table:
    """Setup and return todo table."""
    meta = MetaData(db)
    todo_table = Table(
        "todo",
        meta,
        Column("id", Integer, primary_key=True),
        Column("project", String(30), nullable=True, default=""),
        Column("task", String(100), nullable=False),
        Column("urgency", Integer, default=0),
        Column("due", DateTime, nullable=True),
        Column("done", Boolean, default=False),
        Column("created_at", DateTime, default=datetime.datetime.now()),
        Column("updated_at", DateTime, default=datetime.datetime.now()),
    )

    meta.create_all(db)
    return todo_table


def insert_task(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
    task_data: dict,
):
    """Initial function to insert devices in database."""
    for data in task_data:
        if task_data[data] is None:
            task_data[data] = ""

    if task_data["urgency"] == "":
        task_data["urgency"] = 0

    """Workaround until I find a way
    to espace the quote character.
    """
    if "'" in task_data["task"]:
        task_data["task"] = task_data["task"].replace("'", " ")

    if task_data['due'] == "":
        task_data['due'] = None

    query = todo_table.insert().values(
        project=task_data['project'],
        task=task_data['task'],
        urgency=task_data['urgency'],
        due=task_data['due'],
        created_at=datetime.datetime.today(),
        updated_at=datetime.datetime.today(),
    )

    sql_out = db.connect().execute(query)
    return sql_out.lastrowid


def get_tasks_list(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
    what: str = None,
    project: str = None,
) -> list:
    """Return a list of tasks."""
    if what == 'done':
        query = todo_table.select().where(todo_table.c.done == 1)
    elif what == 'all':
        query = todo_table.select()
    else:
        query = todo_table.select().where(todo_table.c.done == 0)

    if project is not None:
        query = query.where(todo_table.c.project == project)

    tasks = db.connect().execute(query)
    tasks_list = []
    for task in tasks:
        task_list = []
        task_list.append(task.id)
        task_list.append(task.project)
        task_list.append(task.task)
        task_list.append(task.urgency)
        task_list.append(task.due)
        task_list.append(task.created_at)
        tasks_list.append(task_list)
    return tasks_list


def get_max_id(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
) -> int:
    """Get max id of task in TODO table."""
    sm = sessionmaker(db)
    session = sm()
    maxid_query = session.query(func.max(todo_table.c.id))
    maxid = session.execute(maxid_query).scalar()
    return maxid


def get_one_task(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
    task_id: int = None,
) -> list:
    """Grab one task by ID."""
    if does_task_exist(db, todo_table, task_id) is False:
        utils.error("task does not exist")
        return -1

    if task_id is None:
        maxid = get_max_id(db, todo_table)
        query = todo_table.select().where(todo_table.c.id == maxid)
    else:
        query = todo_table.select().where(todo_table.c.id == task_id)

    task = db.connect().execute(query)
    return task.fetchall()


def does_task_exist(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
    task_id: int,
) -> bool:
    """check if task exist before doing anything."""
    query = todo_table.select().where(todo_table.c.id == task_id)
    task = db.connect().execute(query)

    out = task.fetchall()
    if len(out) == 0:
        return False
    else:
        return True
    return False


def set_task_done(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
    task_id: int = None,
) -> int:
    """Update task."""
    if does_task_exist(db, todo_table, task_id) is False:
        return -1

    query = (
        todo_table.update().where(todo_table.c.id == task_id).values(done=True)
    )
    db.connect().execute(query)
    return 0


def remove_task(
    db: sqlalchemy.engine.base.Engine,
    todo_table: sqlalchemy.sql.schema.Table,
    task_id: int = None,
) -> int:
    """Remove task."""
    if does_task_exist(db, todo_table, task_id) is False:
        return -1
    query = todo_table.delete().where(todo_table.c.id == task_id)
    db.connect().execute(query)
    return 0
