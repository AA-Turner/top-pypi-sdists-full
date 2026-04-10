from chalk._gen.chalk.enginestorage.v1 import adhoc_query_pb2 as _adhoc_query_pb2
from chalk._gen.chalk.planner.v1 import batch_operator_pb2 as _batch_operator_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateBatchPlanRequest(_message.Message):
    __slots__ = ("all_planning_inputs",)
    ALL_PLANNING_INPUTS_FIELD_NUMBER: _ClassVar[int]
    all_planning_inputs: _adhoc_query_pb2.AllPlanningInputsProto
    def __init__(
        self, all_planning_inputs: _Optional[_Union[_adhoc_query_pb2.AllPlanningInputsProto, _Mapping]] = ...
    ) -> None: ...

class CreateBatchPlanResponse(_message.Message):
    __slots__ = ("batch_plan",)
    BATCH_PLAN_FIELD_NUMBER: _ClassVar[int]
    batch_plan: _batch_operator_pb2.BatchPlan
    def __init__(self, batch_plan: _Optional[_Union[_batch_operator_pb2.BatchPlan, _Mapping]] = ...) -> None: ...
