from ocsf.events.findings import Finding

from ocsf.objects.compliance import Compliance
from ocsf.objects.remediation import Remediation
from ocsf.objects.resource_details import ResourceDetails

class ComplianceFinding(Finding):
    """
    Compliance Finding events describe results of evaluations performed against
    resources, to check compliance with various Industry Frameworks or Security
    Standards such as NIST SP 800-53, CIS AWS Foundations Benchmark v1.4.0,
    ISO/IEC 27001 etc.
    """

    class_uid: int = 2003
    class_name: str = 'Compliance Finding'

    compliance: Compliance

    # Recommended:
    remediation: Remediation | None = None
    resource: ResourceDetails | None = None # Describes details about the resource that is the subject
                                            # of the compliance check.
