import os

def is_buildkite_itests() -> bool:
    return os.environ.get('BUILDKITE_PIPELINE_NAME') == 'pipebio-integration-tests'
