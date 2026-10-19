from functools import lru_cache
from typing import Optional

from anyscale.cli_logger import BlockLogger


log = BlockLogger()


# Six months of notice, plus two weeks of slack: users only see the warning once
# a release carries it, and 0.26.110 shipped the day this was written. Before
# acting on this date, confirm the release that first carried the warning is at
# least six months old -- nothing removes the field automatically.
RAY_VERSION_REMOVAL_DATE = "2027-04-19"

# Single source for the `ray_version` deprecation wording, shared by the runtime
# warning, the CLI flags' doc metadata, and the config fields' doc metadata.
RAY_VERSION_DEPRECATION_MESSAGE = (
    f"'ray_version' is deprecated and will be removed on {RAY_VERSION_REMOVAL_DATE}. "
    "It doesn't control which version of Ray or RayTurbo runs; that's determined by "
    "the image, and Anyscale detects it at runtime. Declare the Ray version on the "
    "image instead (`anyscale image build/register --ray-version`)."
)

# Doc-spec lifecycle for the `ray_version` config fields. The status mirrors
# ReleaseStatus.DEPRECATED as a literal to keep this module off the commands
# layer; cli_docgen validates the value when it regenerates the spec, so a typo
# fails the docgen gate rather than silently dropping the annotation.
RAY_VERSION_FIELD_DEPRECATION = {
    "status": "deprecated",
    "deprecation_info": {"message": RAY_VERSION_DEPRECATION_MESSAGE},
}


# Configs are rebuilt by `.options()` on most code paths, so warn once per process.
@lru_cache(maxsize=None)
def warn_ray_version_deprecated() -> None:
    log.warning(RAY_VERSION_DEPRECATION_MESSAGE)


# GRS scheduling priority bounds for the user-facing `priority` field. None = unset;
# 0 is valid (distinct from unset). Single CLI source of truth, mirroring the backend
# `SCHEDULING_PRIORITY_MIN/MAX` in backend/server/common/models/validation.py.
SCHEDULING_PRIORITY_MIN = 0
SCHEDULING_PRIORITY_MAX = 1000


def validate_scheduling_priority(priority: Optional[int]) -> None:
    """Validate the GRS `priority` field, shared across workload config models."""
    if priority is None:
        return

    if not isinstance(priority, int):
        raise TypeError(f"'priority' must be an int (it is {type(priority)}).")

    if priority < SCHEDULING_PRIORITY_MIN or priority > SCHEDULING_PRIORITY_MAX:
        raise ValueError(
            f"'priority' must be >= {SCHEDULING_PRIORITY_MIN} and <= {SCHEDULING_PRIORITY_MAX}."
        )
