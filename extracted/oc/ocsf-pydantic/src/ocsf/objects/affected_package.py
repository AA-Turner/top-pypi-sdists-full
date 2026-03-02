from .package import SoftwarePackage

from .remediation import Remediation


class AffectedSoftwarePackage(SoftwarePackage):
    """
    The Affected Package object describes details about a software package
    identified as affected by a vulnerability/vulnerabilities.
    """

    # Optional:
    fixed_in_version: str | None = None
    package_manager: str | None = None
    path: str | None = None # The installation path of the affected package.
    remediation: Remediation | None = None
