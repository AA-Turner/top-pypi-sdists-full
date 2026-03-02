from pydantic import BaseModel

from .remediation import Remediation
from .rule import Rule

class CISBenchmarkResult(BaseModel):
    """
    The CIS Benchmark Result object contains information as defined by the Center
    for Internet Security (https://www.cisecurity.org/cis-benchmarks/) benchmark result.
    CIS Benchmarks are a collection of best practices for securely configuring IT systems,
    software, networks, and cloud infrastructure.
    """

    name: str # The CIS benchmark name.


    # Optional:
    desc: str | None = None # The CIS benchmark description.
    remediation: Remediation | None = None
    rule: Rule | None = None # The CIS benchmark rule.
