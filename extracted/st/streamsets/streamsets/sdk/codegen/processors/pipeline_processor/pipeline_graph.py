#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2026
import re
from collections import defaultdict
from typing import TYPE_CHECKING, Any, Union

import inflection

if TYPE_CHECKING:
    from streamsets.sdk.codegen.processors.pipeline_processor.pipeline_processor import DefaultStageDefinition


class StageVertex:
    """Represents single stage in pipeline."""

    def __init__(
        self,
        instance_name: str,
        stage_data: dict,
        default_stage_definition: "DefaultStageDefinition",
        number_suffix: Union[int, None] = None,
    ):
        self._instance_name = instance_name
        self._stage_data = stage_data
        self._default_stage_definition = default_stage_definition
        self._number_suffix = number_suffix
        self._output_lane_index = 0

        self.configuration: list[dict[str, Any]] = stage_data["configuration"]

    def __repr__(self):
        return f"{self.instance_name}"

    def __hash__(self):
        return hash(self.instance_name)

    def __eq__(self, other):
        if not isinstance(other, StageVertex):
            return False
        return self.instance_name == other.instance_name

    def __str__(self) -> str:
        """String representation of code to create stage."""
        stage_definition = (
            f'{self.stage_variable_name} = pipeline_builder.add_stage("{self._default_stage_definition.label}", '
            f'type="{self.map_stage_type_to_human_readable(self._default_stage_definition.type)}")'
        )
        return f"{stage_definition}\n{self.stage_configuration()}".strip()

    @staticmethod
    def map_stage_type_to_human_readable(stage_type: str) -> str:
        """Map stage type from library definitions to value used by user."""
        stage_type_map = {"SOURCE": "origin", "TARGET": "destination", "EXECUTOR": "executor", "PROCESSOR": "processor"}
        return stage_type_map[stage_type]

    @property
    def instance_name(self) -> str:
        return self._instance_name

    @property
    def stage_variable_name(self) -> str:
        """Return variable name which will refer to stage in generated script."""
        stage_variable_name = self._default_stage_definition.label.lower().replace(" ", "_")
        if self._number_suffix:
            stage_variable_name = f"{stage_variable_name}_{self._number_suffix}"

        return stage_variable_name

    @property
    def output_lane_index(self) -> int:
        return self._output_lane_index

    @output_lane_index.setter
    def output_lane_index(self, index):
        if index < 0:
            raise ValueError("Index cannot be less than 0")
        self._output_lane_index = index

    def stage_configuration(self) -> str:
        """Return stage configuration properties changed by user."""
        changed_config_values = []

        for stage_config in self.configuration:
            if stage_config.get("value") is None or stage_config.get("value") == "":
                continue

            value = stage_config.get("value")
            name = stage_config.get("name")
            config_definition = self._get_stage_config_definition(config_name=name)

            if value == config_definition["defaultValue"]:
                continue

            human_readable_config_name, _ = self.get_attribute(config_definition)
            processed_value = self._format_config_value(value=value, config_definition=config_definition)

            changed_config_values.append(f"{self.stage_variable_name}.{human_readable_config_name} = {processed_value}")

        return "\n".join(changed_config_values)

    def _get_stage_config_definition(self, config_name: str) -> dict[str, Any]:
        for config in self._default_stage_definition.config_definitions:
            if config["name"] == config_name:
                return config

    def _format_config_value(self, value: Any, config_definition: dict[str, Any]) -> str:
        ctype = config_definition.get("type", "").lower()

        if ctype == "credential":
            return '"***"'

        mode = config_definition.get("mode", "").lower()
        if mode == "text/x-sql":
            sql = "" if value is None else str(value)
            sql = sql.replace('"""', r"\"\"\"")
            return f'"""{sql}"""'

        if ctype in ("string", "text", "char", "password"):
            return self._py_string_literal("" if value is None else str(value))

        if ctype in ("int", "integer", "long", "short"):
            if isinstance(value, (bool, int)):  # noqa: UP038
                return str(value)
            try:
                return str(int(value))
            except (TypeError, ValueError):
                return repr(value)

        if ctype in ("float", "double", "decimal"):
            try:
                return repr(float(value))
            except (TypeError, ValueError):
                return repr(value)

        if ctype in ("boolean", "bool"):
            if isinstance(value, str):
                v = value.strip().lower()
                if v in ("true", "1", "yes", "y", "on"):
                    return "True"
                if v in ("false", "0", "no", "n", "off"):
                    return "False"
            return str(bool(value))

        if ctype in ("list", "array", "map", "dict", "object"):
            return repr(value)

        if ctype == "model":
            model_type = config_definition.get("model", {}).get("modelType", "")
            if model_type.lower() == "value_chooser":
                return self._py_string_literal("" if value is None else str(value))
            return repr(value)

        return repr(value)

    @staticmethod
    def _py_string_literal(s: str) -> str:
        # Multiline -> triple quote
        if "\n" in s or "\r" in s:
            s = s.replace('"""', r"\"\"\"")
            return f'"""{s}"""'

        # Single-line -> double-quoted string
        escaped = s.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'

    @staticmethod
    def get_attribute(config_definition: dict) -> tuple[str, str]:
        """Gets the attribute name for a configuration using its definition in a human-readable format."""
        config_name = config_definition.get("name")
        config_label = config_definition.get("label")
        if config_label:
            replacements = [(r"[\s-]+", "_"), (r"&", "and"), (r"/sec", "_per_sec"), (r"_\((.+)\)", r"_in_\1")]
            attribute_name = config_label.lower()
            for pattern, replacement in replacements:
                attribute_name = re.sub(pattern, replacement, attribute_name)
        else:
            attribute_name = inflection.underscore(config_definition["fieldName"])
        return attribute_name, config_name

    def has_multiple_output_lanes(self) -> bool:
        return len(self._stage_data["outputLanes"]) > 1


class Lane:
    """Represents lane between two stages in pipeline."""

    def __init__(self, source: StageVertex, dest: StageVertex, data: dict):
        self._source = source
        self._dest = dest
        self._data = data

    def __str__(self):
        if self._source.has_multiple_output_lanes():
            return (
                f"{self._source.stage_variable_name}.connect_outputs("
                f"stages=[{self._dest.stage_variable_name}], output_lane_index={self._source.output_lane_index})"
            )
        elif self._data.get("is_event_lane", False):
            return (
                f"{self._source.stage_variable_name}.connect_outputs(stages=[{self._dest.stage_variable_name}], "
                f"event_lane=True)"
            )
        else:
            return f"{self._source.stage_variable_name}.connect_outputs(stages=[{self._dest.stage_variable_name}])"

    def __repr__(self) -> str:
        return f"{repr(self._source)} -> {repr(self._dest)}"


class PipelineGraph:
    """Facade for building StreamSets pipeline DAG based on adjacent list."""

    def __init__(self):
        self._adj_list: dict[StageVertex, list[Lane]] = defaultdict(list)

    def __repr__(self) -> str:
        return repr(self._adj_list)

    @property
    def stage_vertexes(self):
        return self._adj_list.keys()

    @property
    def lanes(self):
        for _, lanes in self._adj_list.items():
            for lane in lanes:
                yield lane

    def add_stage_vertex(self, vertex: StageVertex) -> None:
        _ = self._adj_list[vertex]

    def add_lane(self, source: StageVertex, dest: StageVertex, data: Union[dict, None] = None) -> None:
        edge = Lane(source=source, dest=dest, data=data)
        self._adj_list[source].append(edge)

    def is_empty(self) -> bool:
        """Returns True when graph doesn't have any vertex."""
        return len(self._adj_list) == 0
