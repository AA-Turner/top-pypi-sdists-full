from datetime import datetime
from pydantic import AnyUrl, BaseModel

from .product import Product
from .cvss import CVSSScore
from .epss import EPSS
from .cwe import CWE


class CVE(BaseModel):
    """
    The Common Vulnerabilities and Exposures (CVE) object represents publicly
    disclosed cybersecurity vulnerabilities defined in CVE Program catalog (<a
    target='_blank' href='https://cve.mitre.org/'>CVE</a>). There is one CVE Record
    for each vulnerability in the catalog.
    """

    uid: str # The Common Vulnerabilities and Exposures unique number assigned to a
             # specific computer vulnerability. A CVE Identifier begins with 4 digits
             # representing the year followed by a sequence of digits that acts as a
             # unique identifier. For example: `CVE-2021-12345`.

    # Recommended:
    created_time: datetime | None = None # The Record Creation Date identifies when the CVE ID was
                                         # issued to a CVE Numbering Authority (CNA) or the CVE Record
                                         # was published on the CVE List. Note that the Record Creation
                                         # Date does not necessarily indicate when this vulnerability
                                         # was discovered, shared with the affected vendor, publicly
                                         # disclosed, or updated in CVE.
    cvss: list[CVSSScore] | None = None
    references: list[str] | None = None # A list of reference URLs with additional information about
                                        # the CVE Record.
    title: str | None = None # A title or a brief phrase summarizing the CVE record.
    type: str | None = None # <p>The vulnerability type as selected from a large dropdown menu during
                            # CVE refinement.</p>Most frequently used vulnerability types are:
                            # `DoS`, `Code Execution`, `Overflow`,
                            # `Memory Corruption`, `Sql Injection`,
                            # `XSS`, `Directory Traversal`, `Http Response
                            # Splitting`, `Bypass something`, `Gain
                            # Information`, `Gain Privileges`, `CSRF`,
                            # `File Inclusion`. For more information see <a target='_blank'
                            # href='https://www.cvedetails.com/vulnerabilities-by-
                            # types.php'>Vulnerabilities By Type</a> distributions.

    # Optional:
    cwe: CWE | None = None
    cwe_uid: str | None = None
    cwe_url: AnyUrl | None = None
    desc: str | None = None # A brief description of the CVE Record.
    epss: EPSS | None = None
    modified_time: datetime | None = None # The Record Modified Date identifies when the CVE record was
                                          # last updated.
    product: Product | None = None # The product where the vulnerability was discovered.
