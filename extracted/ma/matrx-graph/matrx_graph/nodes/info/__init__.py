"""``info.*`` — information nodes: notes, frames, media, kinds, records and reference cards.

They are stored in a graph's ``nodes`` and NEVER run (``NodeSpec.executes = False``): the
engine seam (``matrx_graph.information.split_information``) takes them out before validation and
compile, so none of them is ever scheduled. An information node's own fields live directly in
``node.data`` (``data.text``, ``data.title`` …); the ``config_schema`` below documents those fields
for the palette and the node's form. ``parentId`` puts a node inside an ``info.frame``; a
``relation`` connection attaches one to anything.

Reference cards (``info.agent`` / ``info.workflow`` / ``info.position`` / ``info.topic``) point at a
feature's record and are placeable on graphs beyond their home graph (``allowed_graphs``).
"""

from matrx_graph.nodes.info.specs import (
    INFO_EXECUTORS,
    InfoAgentExecutor,
    InfoFrameExecutor,
    InfoKindExecutor,
    InfoMediaExecutor,
    InfoNoteExecutor,
    InfoPositionExecutor,
    InfoRecordExecutor,
    InfoTopicExecutor,
    InfoWorkflowExecutor,
)

__all__ = [
    "INFO_EXECUTORS",
    "InfoAgentExecutor",
    "InfoFrameExecutor",
    "InfoKindExecutor",
    "InfoMediaExecutor",
    "InfoNoteExecutor",
    "InfoPositionExecutor",
    "InfoRecordExecutor",
    "InfoTopicExecutor",
    "InfoWorkflowExecutor",
]
