import logging

from fluidattacks_core.logging.utils import get_job_metadata, is_trunk_branch


class NoProductionFilter(logging.Filter):
    """If `CI_COMMIT_REF_NAME` is `trunk`, logs will be excluded."""

    def filter(self, _record: logging.LogRecord) -> bool:
        return not is_trunk_branch()


class ProductionOnlyFilter(logging.Filter):
    """If `CI_COMMIT_REF_NAME` is `trunk`, logs will be included."""

    def filter(self, _record: logging.LogRecord) -> bool:
        return is_trunk_branch()


class BatchOnlyFilter(logging.Filter):
    def filter(self, _record: logging.LogRecord) -> bool:
        return get_job_metadata().job_id is not None


class NoBatchFilter(logging.Filter):
    def filter(self, _record: logging.LogRecord) -> bool:
        return get_job_metadata().job_id is None
