from typing import NamedTuple


class JobMetadata(NamedTuple):
    job_id: str | None
    job_queue: str
    compute_environment: str


class EnvironmentMetadata(NamedTuple):
    product_id: str
    environment: str
    version: str
