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
                f"""\
            sch = ControlHub(
                os.getenv("{self._sch_credential_id_env_name}"),
                os.getenv("{self._sch_token_env_name}"),
                aster_url="{self._aster_url}"
            )"""
            )

        return textwrap.dedent(
            f"""\
        sch = ControlHub(
            os.getenv("{self._sch_credential_id_env_name}"),
            os.getenv("{self._sch_token_env_name}")
        )"""
        )

    def __str__(self) -> str:
        # Hacky way to fulfill linting rules and tests requirements.
        return f"""
import os
from streamsets.sdk import ControlHub


{self.control_hub.strip()}

engine = sch.engines.get(id="{self._source_data.pipeline_config['info']['sdcId']}")
pipeline_builder = sch.get_pipeline_builder(engine_type="COLLECTOR", engine_id=engine.id)""".strip()
