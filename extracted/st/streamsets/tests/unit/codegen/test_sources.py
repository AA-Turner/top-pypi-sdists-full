#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from streamsets.sdk.codegen.sources import source_factory
from streamsets.sdk.codegen.sources.json_file_source import JsonFileSource
from streamsets.sdk.codegen.sources.pipeline_object_source import PipelineObjectSource
from streamsets.sdk.codegen.sources.zip_archive_source import ZipArchiveSource
from streamsets.sdk.sch_models import Pipeline


@pytest.mark.parametrize(
    "source,expected_class",
    [
        ("/tmp/archive.zip", ZipArchiveSource),
        (Path("/tmp/archive.zip"), ZipArchiveSource),
        ("/tmp/pipeline.json", JsonFileSource),
        (Path("/tmp/pipeline.json"), JsonFileSource),
        (
            Pipeline(
                pipeline=MagicMock(), builder=MagicMock, pipeline_definition=MagicMock(), rules_definition=MagicMock()
            ),
            PipelineObjectSource,
        ),
    ],
)
def test_source_factory_function_happy_path(source, expected_class):
    assert isinstance(source_factory(source), expected_class)


@pytest.mark.parametrize(
    "source,expected_exception",
    [
        ("/tmp/archive.invalidExtension", ValueError),
        (Path("/tmp/archive.invalidExtension"), ValueError),
        (12, ValueError),
        (12.5, ValueError),
        ("", ValueError),
        (".", ValueError),
        ("/tmp/dir", ValueError),
        (Path("/tmp/dir"), ValueError),
    ],
)
def test_source_factory_function_unhappy_path(source, expected_exception):
    with pytest.raises(expected_exception):
        source_factory(source)
