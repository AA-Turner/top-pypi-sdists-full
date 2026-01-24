from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from fitrequest.method_models import AttrSignature, FlattenedModelSignature


class Deadline(BaseModel):
    objectives: list[str] | None = None
    timestamp: datetime = Field(alias='finalDate')


class Tasks(BaseModel):
    name: str
    details: str
    done: bool = Field(alias='isDone', default=False)
    deadline: Deadline = Field(alias='deadLine')


class Person(BaseModel):
    age: int
    task: Tasks
    sex: Literal['M', 'F']
    name: str = 'Toto'
    alive: bool = Field(default=True, alias='isAlive')
    job: str | None = None
    tags: list[str] = Field(default_factory=list, alias='tagList')


def test_model_attributes_signature():
    assert FlattenedModelSignature(model=Person).attr_signatures == [
        AttrSignature(name='age', annotation='int', attr_type='arg'),
        AttrSignature(name='sex', annotation="typing.Literal['M', 'F']", attr_type='arg'),
        AttrSignature(
            name='task_deadline_timestamp', alias='task_deadLine_finalDate', annotation='datetime', attr_type='arg'
        ),
        AttrSignature(name='task_details', annotation='str', attr_type='arg'),
        AttrSignature(name='task_name', annotation='str', attr_type='arg'),
        AttrSignature(name='alive', alias='isAlive', annotation='bool', attr_type='kwarg', default_value='True'),
        AttrSignature(name='job', annotation='str | None', attr_type='kwarg', default_value='None'),
        AttrSignature(name='name', annotation='str', attr_type='kwarg', default_value="'Toto'"),
        AttrSignature(name='tags', alias='tagList', annotation='list[str]', attr_type='kwarg', default_value='[]'),
        AttrSignature(
            name='task_deadline_objectives',
            alias='task_deadLine_objectives',
            annotation='list[str] | None',
            attr_type='kwarg',
            default_value='None',
        ),
        AttrSignature(
            name='task_done', alias='task_isDone', annotation='bool', attr_type='kwarg', default_value='False'
        ),
    ]


def test_model_signature():
    # Model signature never uses the aliases, it's only for params
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
        'task_deadLine_finalDate',
        'task_details',
        'task_name',
        'isAlive',
        'job',
        'name',
        'tagList',
        'task_deadLine_objectives',
        'task_isDone',
    }
