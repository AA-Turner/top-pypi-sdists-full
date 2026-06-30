#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
import textwrap
from typing import Union

from streamsets.sdk.codegen.sources.source import PipelineDto


class PipelinePreamble:
    def __init__(
        self,
        source_data: PipelineDto,
        sch_credential_id_env_name: str = "SCH_CREDENTIAL_ID",
        sch_token_env_name: str = "SCH_TOKEN",
        aster_url: Union[str, None] = None,
    ) -> None:
        self._source_data = source_data
        self._sch_credential_id_env_name = sch_credential_id_env_name
        self._sch_token_env_name = sch_token_env_name
        self._aster_url = aster_url

    @property
    def control_hub(self) -> str:
        if self._aster_url:
            return textwrap.dedent(
                """\
            sch = ControlHub(
                os.getenv("%(sch_credential_id_env_name)s"),
                os.getenv("%(sch_token_env_name)s"),
                aster_url="%(aster_url)s"
            )"""
                % {
                    'sch_credential_id_env_name': self._sch_credential_id_env_name,
                    'sch_token_env_name': self._sch_token_env_name,
                    'aster_url': self._aster_url,
                }
            )

        return textwrap.dedent(
            """\
        sch = ControlHub(
            os.getenv("%(sch_credential_id_env_name)s"),
            os.getenv("%(sch_token_env_name)s")
        )"""
            % {
                'sch_credential_id_env_name': self._sch_credential_id_env_name,
                'sch_token_env_name': self._sch_token_env_name,
            }
        )

    def __str__(self) -> str:
        # Hacky way to fulfill linting rules and tests requirements.
        return """
import os
from streamsets.sdk import ControlHub


%(control_hub)s

engine = sch.engines.get(id="%(sdcId)s")
pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)""".strip() % {
            'control_hub': self.control_hub.strip(),
            'sdcId': self._source_data.pipeline_config['info']['sdcId'],
        }
