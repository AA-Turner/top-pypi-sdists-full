#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
from pathlib import Path
from typing import Union

from streamsets.sdk.codegen.processors import PipelineProcessor
from streamsets.sdk.codegen.sources import Source, source_factory
from streamsets.sdk.sch_models import Pipeline


class PythonGenerator:
    """Pipeline code generation entrypoint.

    Args:
        source (:obj:`Union[str, Path, Pipeline]`): Source from which pipeline definition will be load.
        destination (:obj:`Union[str, Path]`): Location where save generated script.
        **kwargs (:obj:`Union[str, object]`): Additional configuration values.
    """

    def __init__(
        self,
        source: Union[str, Path, Pipeline],
        destination: Union[str, Path],
        **kwargs: Union[str, object],
    ) -> None:
        self._source: Source = source_factory(source)
        self._destination = Path(destination)

        sch_credential_id = kwargs.get("sch_credential_id", "SCH_CREDENTIAL_ID")
        sch_token = kwargs.get("sch_token", "SCH_TOKEN")
        aster_url = kwargs.get("aster_url")
        self._processor = PipelineProcessor(
            source_data=self._source.load(),
            sch_credential_id=sch_credential_id,
            sch_token=sch_token,
            aster_url=aster_url,
        )

    def save(self) -> Path:
        """Run code generation then save it to destination.

        Returns:
            Path to the location where the generated script was saved.
        """
        code = self._processor.run()
        return code.save(self._destination)
