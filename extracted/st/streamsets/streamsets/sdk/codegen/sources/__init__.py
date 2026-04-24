#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
from pathlib import Path
from typing import Union

from streamsets.sdk.codegen.sources.json_file_source import JsonFileSource
from streamsets.sdk.codegen.sources.pipeline_object_source import PipelineObjectSource
from streamsets.sdk.codegen.sources.source import Source
from streamsets.sdk.codegen.sources.zip_archive_source import ZipArchiveSource
from streamsets.sdk.sch_models import Pipeline


def source_factory(source: Union[str, Path, Pipeline]) -> Source:
    """
    Args:
        source (:obj:`str` or :py:class:`pathlib.Path` or :py:class:`streamsets.sdk.sch_models.Pipeline):
            Path to input data or pipeline instance itself.

    Returns:
        An input data wrapped with :py:class:`streamsets.sdk.codegen.sources.base_source.Source` class.

    Raises:
        ValueError: If provided source is not instance of supported type.
                    If provided source file has not supported extension.
    """
    if isinstance(source, Pipeline):
        return PipelineObjectSource(source_data=source)
    elif isinstance(source, str) or isinstance(source, Path):
        file_path = Path(source)
        extension = file_path.suffix
        if extension.lower() == ".zip":
            return ZipArchiveSource(source)
        elif extension.lower() == ".json":
            return JsonFileSource(source)
        else:
            raise ValueError(f"File with extension {extension} not supported.")
    else:
        raise ValueError("Invalid source input type.")
