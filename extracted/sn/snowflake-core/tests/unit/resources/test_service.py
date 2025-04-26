from textwrap import dedent

import pytest

from snowflake.core.service import ServiceSpec, ServiceSpecInlineText, ServiceSpecStageFile
from snowflake.core.service._service import _parse_spec_path, _validate_inline_spec


_INLINE_SERVICE_SPEC = dedent("""
    spec:
      containers:
      - name: hello-world
        image: repo/hello-world:latest
""")
_INLINE_SERVICE_SPEC_NO_SPEC_FIELD = dedent("""
    containers:
    - name: hello-world
      image: repo/hello-world:latest
""")
_INLINE_SERVICE_SPEC_BAD_INDENTATION = dedent("""
    spec:
    containers:
        - name: hello-world
        image: repo/hello-world:latest
    - name: goodbye-world
    image: repo/goodbye-world:latest
""")


@pytest.mark.parametrize("spec, expected", [
    ("@stage/spec.yaml", ServiceSpecStageFile(stage="stage", spec_file="spec.yaml")),
    ("@stage/path/to/spec.yaml", ServiceSpecStageFile(stage="stage", spec_file="path/to/spec.yaml")),
    (" @stage/path/with/spaces  ", ServiceSpecStageFile(stage="stage", spec_file="path/with/spaces")),
    (_INLINE_SERVICE_SPEC, ServiceSpecInlineText(spec_text=_INLINE_SERVICE_SPEC.rstrip()))
])
def test_service_spec(spec, expected):
    assert ServiceSpec(spec) == expected


@pytest.mark.parametrize("spec", [
    "@stage",  # no forward slash followed by file path
    "@stage/",  # no file path after forward slash
    "@stage//spec.yaml",  # doubled forward slash
    "@stage/spec.yaml/",  # trailing forward slash
    "stage/path/spec.yaml",  # no leading @, gets interpreted as invalid inline spec
    _INLINE_SERVICE_SPEC_NO_SPEC_FIELD,
    _INLINE_SERVICE_SPEC_BAD_INDENTATION
])
def test_service_spec_invalid(spec):
    with pytest.raises(ValueError):
        ServiceSpec(spec)


@pytest.mark.parametrize("spec_path, stage, path", [
    ("stage/spec.yaml", "stage", "spec.yaml"),
    ("stage/path/to/spec.yaml", "stage", "path/to/spec.yaml"),
])
def test_parse_spec_path(spec_path, stage, path):
    assert _parse_spec_path(spec_path) == (stage, path)


@pytest.mark.parametrize("spec_path", [
    "stage",  # no forward slash followed by file path
    "stage/",  # no file path after forward slash
    "stage//invalid.yaml",  # doubled forward slash
    "stage/spec.yaml/",  # trailing forward slash
    "/path/to/spec.yaml",  # leading forward slash
    "stage/<invalid>/spec.yaml",  # invalid characters in file path
    "?name/spec.yaml"  # invalid character in stage name
    r"stage\path\to\spec.yaml",  # backslash instead of forward slash
    ""  # empty
])
def test_parse_spec_path_invalid(spec_path):
    with pytest.raises(ValueError):
        _parse_spec_path(spec_path)


def test_validate_inline_spec():
    assert _validate_inline_spec(_INLINE_SERVICE_SPEC)


@pytest.mark.parametrize("spec_str", [
    _INLINE_SERVICE_SPEC_NO_SPEC_FIELD,
    _INLINE_SERVICE_SPEC_BAD_INDENTATION,
    ""  # empty
])
def test_validate_inline_spec_invalid(spec_str):
    assert not _validate_inline_spec(spec_str)


