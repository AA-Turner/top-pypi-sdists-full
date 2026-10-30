from importlib.util import find_spec

import pytest

from mistralai.workflows._mistral_http import MISTRAL_HTTP

# mistralai-evaluations still pins mistralai<3, so the mistralai 3 compatibility environment
# (workflow_sdk_tests/compat_mistral_v3) cannot install the evaluations plugin, and these tests
# cannot even be imported there. Everywhere else the plugin must be present.
_ON_MISTRALAI_3 = MISTRAL_HTTP.__name__ == "httpx2"
_HAS_EVALUATIONS_PLUGIN = find_spec("mistralai.workflows.plugins.evaluations") is not None

if _ON_MISTRALAI_3 and _HAS_EVALUATIONS_PLUGIN:
    # Fails the run on purpose rather than silently keeping these tests skipped.
    raise pytest.UsageError(
        "The evaluations plugin is now installed under mistralai 3: remove the skip in "
        "workflow_sdk/tests/evaluations/conftest.py so these tests run in the mistralai 3 lane."
    )
if not _ON_MISTRALAI_3 and not _HAS_EVALUATIONS_PLUGIN:
    raise pytest.UsageError(
        "The evaluations plugin is missing: install mistralai-workflows with the evaluations extra."
    )

collect_ignore_glob = ["test_*.py"] if _ON_MISTRALAI_3 else []
