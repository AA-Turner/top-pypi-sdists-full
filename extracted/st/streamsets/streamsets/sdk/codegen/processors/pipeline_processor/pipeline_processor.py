#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import copy
import textwrap
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Union

from streamsets.sdk.codegen.preambles import PipelinePreamble
from streamsets.sdk.codegen.processors.pipeline_processor.pipeline_graph import PipelineGraph, StageVertex
from streamsets.sdk.codegen.processors.processor import Code, Processor
from streamsets.sdk.codegen.sources.source import PipelineDto


@dataclass(frozen=True)
class DefaultStageDefinition:
    """Wrapper structure for stage definition."""

    label: str
    type: str
    config_definitions: list[dict[str, Any]]


class PipelineProcessor(Processor):
    def __init__(
        self, source_data: PipelineDto, sch_credential_id: str, sch_token: str, aster_url: Union[str, None] = None
    ):
        self._source_data = source_data
        self._sch_credential_id = sch_credential_id
        self._sch_token = sch_token
        self._definitions = None

        self._preamble = PipelinePreamble(source_data, sch_credential_id, sch_token, aster_url)

        self._graph = PipelineGraph()
        self._stage_counter: dict[str, int] = defaultdict(int)
        self._lanes_to_vertex_lookup = dict()

    def _extract_stages(self):
        for stage in self._source_data.pipeline_config["stages"]:
            self._stage_counter[stage["stageName"]] += 1

            for index, output_lane_id in enumerate(stage["outputLanes"]):
                vertex = StageVertex(
                    instance_name=stage["instanceName"],
                    stage_data=stage,
                    default_stage_definition=self.definitions[stage["stageName"]],
                    number_suffix=self._stage_counter[stage["stageName"]],
                )
                vertex.output_lane_index = index
                self._lanes_to_vertex_lookup[output_lane_id] = vertex

            for event_lane_id in stage["eventLanes"]:
                vertex = StageVertex(
                    instance_name=stage["instanceName"],
                    stage_data=stage,
                    default_stage_definition=self.definitions[stage["stageName"]],
                    number_suffix=self._stage_counter[stage["stageName"]],
                )
                self._lanes_to_vertex_lookup[event_lane_id] = vertex

            for input_lane_id in stage["inputLanes"]:
                is_event_lane = True if "eventlane" in input_lane_id.lower() else False

                vertex = StageVertex(
                    instance_name=stage["instanceName"],
                    stage_data=stage,
                    default_stage_definition=self.definitions[stage["stageName"]],
                    number_suffix=self._stage_counter[stage["stageName"]],
                )
                source = self._lanes_to_vertex_lookup[input_lane_id]

                # Code order dependency here: first edge then vertex
                self._graph.add_lane(source, vertex, {"is_event_lane": is_event_lane})
                self._graph.add_stage_vertex(vertex)

    @property
    def definitions(self) -> dict[str, DefaultStageDefinition]:
        """Parsed stage definitions with configuration definition."""
        if not self._definitions:
            self._definitions = self._parse_raw_library_definitions(self._source_data.library_definitions)

        return self._definitions

    @property
    def graph(self) -> PipelineGraph:
        """Returns streaming flow DAG structure."""
        if self._graph.is_empty():
            self._extract_stages()

        return self._graph

    @staticmethod
    def _parse_raw_library_definitions(definition_json: dict) -> dict[str, DefaultStageDefinition]:
        result = dict()
        for stage_definition in definition_json["stages"]:
            stage_name = stage_definition["name"]
            result[stage_name] = DefaultStageDefinition(
                label=stage_definition["label"],
                type=stage_definition["type"],
                config_definitions=copy.deepcopy(stage_definition["configDefinitions"]),
            )

        return result

    def stages_as_str(self) -> str:
        """Collect string representation of all stages.

        Returns:
            A string representation of create stage code for all stages.
        """
        result = []
        for stage in self.graph.stage_vertexes:
            result.append(str(stage))

        return "\n".join(result)

    def stages_connection_as_str(self) -> str:
        """Collect string representation of connection between stages.

        Returns:
            A string representation of connection between stages.
        """
        result = []
        for lane in self.graph.lanes:
            result.append(str(lane))

        return "\n".join(result)

    @property
    def script_footer(self) -> str:
        """Return generated script footer."""
        return textwrap.dedent(f"""\
        pipeline = pipeline_builder.build("{self._source_data.pipeline_config["title"]}")
        sch.publish_pipeline(pipeline)""")

    def run(self) -> Code:
        """Returns object holding generated python script."""
        content = textwrap.dedent(f"""\
{self._preamble}

{self.stages_as_str()}

{self.stages_connection_as_str()}

{self.script_footer}
""")
        return Code(content)
