"""
Speckit CLI commands.

Provides ``agdt-speckit-*`` entry points that read the corresponding
``.github/prompts/speckit.<name>.prompt.md`` template, substitute
``$ARGUMENTS`` with the user-supplied text, and launch an interactive
``gh copilot`` session.
"""

from .commands import (
    speckit_analyze,
    speckit_checklist,
    speckit_clarify,
    speckit_constitution,
    speckit_implement,
    speckit_plan,
    speckit_specify,
    speckit_tasks,
    speckit_taskstoissues,
)
from .cross_ref import cross_ref_command as speckit_cross_ref
from .pass_e2.validator import test_coverage_command as speckit_test_coverage
from .request_artifact_fix import request_artifact_fix_command as speckit_request_artifact_fix
from .scaffold_check_prereqs import (
    scaffold_check_prereqs_async as speckit_scaffold_check_prereqs_async,
)
from .scaffold_check_prereqs import (
    scaffold_check_prereqs_command as speckit_scaffold_check_prereqs,
)
from .scaffold_new_feature import (
    scaffold_new_feature_async as speckit_scaffold_new_feature_async,
)
from .scaffold_new_feature import (
    scaffold_new_feature_command as speckit_scaffold_new_feature,
)
from .scaffold_plan import (
    scaffold_plan_async as speckit_scaffold_plan_async,
)
from .scaffold_plan import (
    scaffold_plan_command as speckit_scaffold_plan,
)
from .scaffold_tasks import (
    scaffold_tasks_async as speckit_scaffold_tasks_async,
)
from .scaffold_tasks import (
    scaffold_tasks_command as speckit_scaffold_tasks,
)
from .scaffold_update_agent_context import (
    scaffold_update_agent_context_async,
)
from .scaffold_update_agent_context import (
    scaffold_update_agent_context_command as speckit_scaffold_update_agent_context,
)
from .validate_checklists import validate_checklists_command as speckit_validate_checklists
from .validate_frs import validate_frs_command as speckit_validate_frs
from .verify_artifacts import verify_artifacts_command as speckit_verify_artifacts

__all__ = [
    "speckit_analyze",
    "speckit_checklist",
    "speckit_clarify",
    "speckit_constitution",
    "speckit_cross_ref",
    "speckit_implement",
    "speckit_test_coverage",
    "speckit_plan",
    "speckit_request_artifact_fix",
    "speckit_scaffold_check_prereqs",
    "speckit_scaffold_check_prereqs_async",
    "speckit_scaffold_new_feature",
    "speckit_scaffold_new_feature_async",
    "speckit_scaffold_plan",
    "speckit_scaffold_plan_async",
    "speckit_scaffold_tasks",
    "speckit_scaffold_tasks_async",
    "speckit_scaffold_update_agent_context",
    "scaffold_update_agent_context_async",
    "speckit_specify",
    "speckit_tasks",
    "speckit_taskstoissues",
    "speckit_validate_checklists",
    "speckit_validate_frs",
    "speckit_verify_artifacts",
]
