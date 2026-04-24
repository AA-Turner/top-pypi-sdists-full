#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
from streamsets.sdk.sch_models import Pipeline

from .source import PipelineDto, Source


class PipelineObjectSource(Source):
    def __init__(self, source_data: Pipeline):
        self._source_data = source_data

    def load(self) -> PipelineDto:
        # Trigger lazy loading to obtain pipeline rules
        self._source_data._load_data()  # noqa
        return PipelineDto(
            # TODO: Replace with property call after fixing TLKT-2047.
            pipeline_config=self._source_data._pipeline_definition,  # noqa
            pipeline_rules=self._source_data._rules_definition,  # noqa
            library_definitions=self._source_data.library_definitions,
        )
