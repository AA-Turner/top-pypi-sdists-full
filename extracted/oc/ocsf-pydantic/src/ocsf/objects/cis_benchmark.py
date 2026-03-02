
from pydantic import BaseModel

from .cis_control import CISControl

class CISBenchmark(BaseModel):
    """
    The CIS Benchmark object describes best practices for securely configuring IT
    systems, software, networks, and cloud infrastructure as defined by the <a
    target='_blank' href='https://www.cisecurity.org/cis-benchmarks/'>Center for
    Internet Security</a>. See also <a target='_blank'
    href='https://www.cisecurity.org/insights/blog/getting-to-know-the-cis-
    benchmarks'>Getting to Know the CIS Benchmarks</a>.
    """

    name: str # The CIS Benchmark name. For example: <i>Ensure mounting of cramfs
              # filesystems is disabled.</i>

    # Recommended:
    cis_controls: list[CISControl] | None = None

    # Optional:
    desc: str | None = None # The CIS Benchmark description. For example: <i>The cramfs filesystem type
                            # is a compressed read-only Linux filesystem embedded in small footprint
                            # systems. A cramfs image can be used without having to first decompress
                            # the image.</i>
