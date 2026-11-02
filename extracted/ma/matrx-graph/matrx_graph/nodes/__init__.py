"""Built-in node packs: control, data, tool, subgraph, ...

AI, agent, and LLM nodes live in the matrx-ai package and register themselves
at import time via `matrx_ai.graph_nodes.register_with(registry)`.

Helper:
    register_builtin_nodes(registry) — registers all built-in node executors
    against the given registry (defaults to the engine's global registry).
"""

from matrx_graph.executor.registry import NodeRegistry, default_registry
from matrx_graph.nodes.control.branch import BranchExecutor
from matrx_graph.nodes.control.gather import GatherExecutor
from matrx_graph.nodes.control.human_input import HumanInputExecutor
from matrx_graph.nodes.control.loop import LoopExecutor
from matrx_graph.nodes.control.map import MapExecutor
from matrx_graph.nodes.control.send import SendExecutor
from matrx_graph.nodes.control.work_queue import WorkQueueExecutor
from matrx_graph.nodes.control.work_seed import WorkSeedExecutor
from matrx_graph.nodes.crypto import (
    HashExecutor,
    RandomStringExecutor,
    UuidExecutor,
)
from matrx_graph.nodes.data.assert_ import AssertExecutor
from matrx_graph.nodes.data.collections import (
    AggregateExecutor,
    BatchExecutor,
    DedupeExecutor,
    LimitExecutor,
    SortExecutor,
)
from matrx_graph.nodes.data.apportion import ApportionExecutor
from matrx_graph.nodes.data.check_items import CheckItemsExecutor
from matrx_graph.nodes.data.choose import ChooseExecutor
from matrx_graph.nodes.data.join import DataJoinExecutor
from matrx_graph.nodes.data.criteria_gate import CriteriaGateExecutor
from matrx_graph.nodes.data.filter import FilterExecutor
from matrx_graph.nodes.data.flatten import FlattenExecutor
from matrx_graph.nodes.data.json_io import ParseJsonExecutor, StringifyJsonExecutor
from matrx_graph.nodes.data.map_template import MapTemplateExecutor
from matrx_graph.nodes.data.merge import MergeExecutor
from matrx_graph.nodes.data.pick_omit import OmitExecutor, PickExecutor
from matrx_graph.nodes.data.read_record import ReadRecordExecutor
from matrx_graph.nodes.data.group import GroupExecutor
from matrx_graph.nodes.data.rules import RulesExecutor
from matrx_graph.nodes.data.shuffle import ShuffleExecutor
from matrx_graph.nodes.data.spread_rank import SpreadRankExecutor
from matrx_graph.nodes.data.tabular import ParseCsvExecutor, ParseYamlExecutor
from matrx_graph.nodes.data.transform import TransformExecutor
from matrx_graph.nodes.datetime_ import (
    DatetimeAddExecutor,
    DatetimeFormatExecutor,
    DatetimeNowExecutor,
    DatetimeParseExecutor,
)
from matrx_graph.nodes.flow import (
    NoopExecutor,
    SleepExecutor,
    ThrottleExecutor,
    WaitUntilExecutor,
)
from matrx_graph.nodes.http import (
    CustomApiExecutor,
    HttpGetExecutor,
    HttpGraphQLExecutor,
    HttpPostExecutor,
)
from matrx_graph.nodes.content_ir import ValidateKindExecutor
from matrx_graph.nodes.io.user_input import UserInputExecutor
from matrx_graph.nodes.log import RecordIssueExecutor
from matrx_graph.nodes.math_ import MathEvaluateExecutor
from matrx_graph.nodes.settings import SettingReadExecutor
from matrx_graph.nodes.speech import SpeechBudgetExecutor
from matrx_graph.nodes.output.to_frontend import ToFrontendExecutor
from matrx_graph.nodes.pipe.step import PipeStepExecutor
from matrx_graph.nodes.plan.step import PlanStepExecutor
from matrx_graph.nodes.subgraph.call import SubgraphCallExecutor
from matrx_graph.nodes.text.case import TextCaseExecutor
from matrx_graph.nodes.text.similarity import SimilarityExecutor
from matrx_graph.nodes.text.key_phrases import KeyPhrasesExecutor
from matrx_graph.nodes.text.term_scan import TermScanExecutor
from matrx_graph.nodes.text import (
    CustomExtractExecutor,
    JoinExecutor,
    JsonPathExecutor,
    RegexExtractExecutor,
    RegexReplaceExecutor,
    RemoveRepeatedLinesExecutor,
    RenderListExecutor,
    SectionsPatchExecutor,
    SlugExecutor,
    SplitExecutor,
    TemplateExecutor,
    WordCountExecutor,
)
from matrx_graph.nodes.tool.call import ToolCallExecutor


def register_builtin_nodes(
    registry: NodeRegistry | None = None, overwrite: bool = False
) -> NodeRegistry:
    """Register all built-in node executors against a registry and return it.

    Called once during application startup. Idempotent when overwrite=True.
    """
    registry = registry or default_registry()
    for executor in (
        # Control flow
        BranchExecutor(),
        SendExecutor(),
        HumanInputExecutor(),
        MapExecutor(),
        GatherExecutor(),
        LoopExecutor(),
        WorkSeedExecutor(),
        WorkQueueExecutor(),
        # Data
        TransformExecutor(),
        MapTemplateExecutor(),
        MergeExecutor(),
        PickExecutor(),
        OmitExecutor(),
        FilterExecutor(),
        FlattenExecutor(),
        AssertExecutor(),
        CriteriaGateExecutor(),
        CheckItemsExecutor(),
        DataJoinExecutor(),
        GroupExecutor(),
        RulesExecutor(),
        ParseJsonExecutor(),
        StringifyJsonExecutor(),
        DedupeExecutor(),
        SortExecutor(),
        LimitExecutor(),
        ChooseExecutor(),
        ShuffleExecutor(),
        SpreadRankExecutor(),
        BatchExecutor(),
        ApportionExecutor(),
        AggregateExecutor(),
        ParseCsvExecutor(),
        ParseYamlExecutor(),
        # Records — read ONE platform Record as the run's operator
        ReadRecordExecutor(),
        # Flow pacing — durable timers + pass-through junctions
        SleepExecutor(),
        WaitUntilExecutor(),
        ThrottleExecutor(),
        NoopExecutor(),
        # Diagnostics — the workflow's own record of what went wrong
        RecordIssueExecutor(),
        # Shapes — ask whether a value really matches a registered kind
        ValidateKindExecutor(),
        # Math
        MathEvaluateExecutor(),
        # Speech — spoken length from the speaking-pace setting
        SpeechBudgetExecutor(),
        SettingReadExecutor(),
        # HTTP
        HttpGetExecutor(),
        HttpPostExecutor(),
        HttpGraphQLExecutor(),
        CustomApiExecutor(),
        # Text extraction + manipulation
        RegexExtractExecutor(),
        RegexReplaceExecutor(),
        JsonPathExecutor(),
        CustomExtractExecutor(),
        TemplateExecutor(),
        RenderListExecutor(),
        SplitExecutor(),
        JoinExecutor(),
        SlugExecutor(),
        TextCaseExecutor(),
        WordCountExecutor(),
        SectionsPatchExecutor(),
        RemoveRepeatedLinesExecutor(),
        TermScanExecutor(),
        KeyPhrasesExecutor(),
        SimilarityExecutor(),
        # Datetime
        DatetimeNowExecutor(),
        DatetimeParseExecutor(),
        DatetimeFormatExecutor(),
        DatetimeAddExecutor(),
        # Crypto / identity
        HashExecutor(),
        UuidExecutor(),
        RandomStringExecutor(),
        # Tool dispatch
        ToolCallExecutor(),
        # Subgraph
        SubgraphCallExecutor(),
        # Plan — a step that hasn't resolved yet
        PlanStepExecutor(),
        # THE THREE PIPES — one contract, swappable executor
        PipeStepExecutor(),
        # I/O — collect user input at the start, send results back mid-run
        UserInputExecutor(),
        ToFrontendExecutor(),
    ):
        declared = BUILTIN_VALUES_ARE.get(executor.spec.node_type)
        if declared is not None and executor.spec.values_are != declared:
            executor.spec = executor.spec.model_copy(update={"values_are": declared})
        registry.register(executor, overwrite=overwrite)
    return registry


#: WHERE EACH BUILT-IN STEP'S OUTPUT VALUES COME FROM (``NodeSpec.values_are``, lane 11
#: round 5). Deny-by-default: a built-in not listed here keeps ``'ai'`` — ``control.work_queue``
#: (its items come from ``workflow.work_item``, still owner-writable: B3, waiting on the chair),
#: ``data.read_record`` (a platform record an agent may have written unheld) and
#: ``io.user_input`` (its bound values live on client-writable trigger/run rows) — round 8:
#: lineage follows where the data came from, not the step kind —, ``control.human_input``
#: (a person or an agent answers it), ``pipe.step`` / ``plan.step`` / ``subgraph.call`` (what
#: runs inside is configuration) and ``tool.call`` (resolved per use from its ``action_name``).
#: Every listed step computes its output from its inputs and config alone (``http.*`` fetches
#: from where the owner pointed it: ``'outside'``). The census test in aidream lists every
#: registered node and its value so this cannot drift silently.
BUILTIN_VALUES_ARE: dict[str, str] = {
    **{t: "deterministic" for t in (
        "content_ir.validate",
        "control.branch", "control.gather", "control.loop", "control.map", "control.send",
        "control.work_seed",
        "crypto.hash", "crypto.random_string", "crypto.uuid",
        "data.aggregate", "data.apportion", "data.assert", "data.batch", "data.check_items", "data.criteria_gate", "data.dedupe",
        "data.choose", "data.filter", "data.flatten", "data.group", "data.join", "data.limit", "data.map_template", "data.merge",
        "data.omit", "data.parse_csv", "data.parse_json", "data.parse_yaml", "data.pick", "data.rules",
        "data.shuffle", "data.sort", "data.spread_rank", "data.stringify_json", "data.transform",
        "datetime.add", "datetime.format", "datetime.now", "datetime.parse",
        "flow.noop", "flow.sleep", "flow.throttle", "flow.wait_until",
        "log.record", "math.evaluate", "output.to_frontend", "settings.read", "speech.budget",
        "text.case", "text.custom_extract", "text.join", "text.json_path", "text.regex_extract",
        "text.regex_replace", "text.similarity", "text.term_scan", "text.key_phrases", "text.remove_repeated_lines", "text.render_list", "text.sections.patch", "text.slug", "text.split", "text.template",
        "text.word_count",
    )},
    **{t: "outside" for t in ("http.custom_api", "http.get", "http.graphql", "http.post")},
}


__all__ = [
    "BUILTIN_VALUES_ARE",
    "AggregateExecutor",
    "ApportionExecutor",
    "AssertExecutor",
    "BatchExecutor",
    "BranchExecutor",
    "DedupeExecutor",
    "LimitExecutor",
    "ChooseExecutor",
    "MathEvaluateExecutor",
    "SpeechBudgetExecutor",
    "SettingReadExecutor",
    "NoopExecutor",
    "ParseCsvExecutor",
    "ParseYamlExecutor",
    "SleepExecutor",
    "ShuffleExecutor",
    "SpreadRankExecutor",
    "SortExecutor",
    "ThrottleExecutor",
    "WaitUntilExecutor",
    "CustomApiExecutor",
    "CustomExtractExecutor",
    "CriteriaGateExecutor",
    "DatetimeAddExecutor",
    "DatetimeFormatExecutor",
    "DatetimeNowExecutor",
    "DatetimeParseExecutor",
    "CheckItemsExecutor",
    "DataJoinExecutor",
    "FilterExecutor",
    "GroupExecutor",
    "RulesExecutor",
    "FlattenExecutor",
    "GatherExecutor",
    "HashExecutor",
    "HttpGetExecutor",
    "HttpGraphQLExecutor",
    "HttpPostExecutor",
    "HumanInputExecutor",
    "JoinExecutor",
    "JsonPathExecutor",
    "LoopExecutor",
    "MapExecutor",
    "MapTemplateExecutor",
    "MergeExecutor",
    "OmitExecutor",
    "ParseJsonExecutor",
    "PickExecutor",
    "PipeStepExecutor",
    "RandomStringExecutor",
    "ReadRecordExecutor",
    "RegexExtractExecutor",
    "RegexReplaceExecutor",
    "RenderListExecutor",
    "PlanStepExecutor",
    "SectionsPatchExecutor",
    "SendExecutor",
    "SimilarityExecutor",
    "TermScanExecutor",
    "KeyPhrasesExecutor",
    "RemoveRepeatedLinesExecutor",
    "SlugExecutor",
    "TextCaseExecutor",
    "SplitExecutor",
    "StringifyJsonExecutor",
    "SubgraphCallExecutor",
    "TemplateExecutor",
    "ToFrontendExecutor",
    "ToolCallExecutor",
    "TransformExecutor",
    "UserInputExecutor",
    "UuidExecutor",
    "WordCountExecutor",
    "WorkQueueExecutor",
    "WorkSeedExecutor",
    "register_builtin_nodes",
]
