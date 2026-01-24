from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from fitrequest.method_models import AttrSignature, FlattenedModelSignature


class Deadline(BaseModel):
    objectives: list[str] | None = None
    timestamp: datetime


class Tasks(BaseModel):
    name: str
    details: str
    done: bool = False
    deadline: Deadline


class Person(BaseModel):
    age: int
    task: Tasks
    sex: Literal['M', 'F']
    name: str = 'Toto'
    alive: bool = True
    job: str | None = None
    tags: list[str] = Field(default_factory=list)


def test_model_attributes_signature():
    assert FlattenedModelSignature(model=Person).attr_signatures == [
        AttrSignature(name='age', annotation='int', attr_type='arg'),
        AttrSignature(name='sex', annotation="typing.Literal['M', 'F']", attr_type='arg'),
        AttrSignature(name='task_deadline_timestamp', annotation='datetime', attr_type='arg'),
        AttrSignature(name='task_details', annotation='str', attr_type='arg'),
        AttrSignature(name='task_name', annotation='str', attr_type='arg'),
        AttrSignature(name='alive', annotation='bool', attr_type='kwarg', default_value='True'),
        AttrSignature(name='job', annotation='str | None', attr_type='kwarg', default_value='None'),
        AttrSignature(name='name', annotation='str', attr_type='kwarg', default_value="'Toto'"),
        AttrSignature(name='tags', annotation='list[str]', attr_type='kwarg', default_value='[]'),
        AttrSignature(
            name='task_deadline_objectives', annotation='list[str] | None', attr_type='kwarg', default_value='None'
        ),
        AttrSignature(name='task_done', annotation='bool', attr_type='kwarg', default_value='False'),
    ]


def test_model_signature():
    assert FlattenedModelSignature(model=Person).signature == [
        'age: int',
        "sex: typing.Literal['M', 'F']",
        'task_deadline_timestamp: datetime',
        'task_details: str',
        'task_name: str',
        'alive: bool = True',
        'job: str | None = None',
        "name: str = 'Toto'",
        'tags: list[str] = []',
        'task_deadline_objectives: list[str] | None = None',
        'task_done: bool = False',
    ]


def test_model_params_names():
    assert FlattenedModelSignature(model=Person).params_varnames == {
        'age',
        'sex',
        'task_deadline_timestamp',
        'task_details',
        'task_name',
        'alive',
        'job',
        'name',
        'tags',
        'task_deadline_objectives',
        'task_done',
    }
