from pydantic import AnyUrl, BaseModel

class CWE(BaseModel):
    """
    The CWE object represents a weakness in a software system that can be exploited
    by a threat actor to perform an attack. The CWE object is based on the 
    Common Weakness Enumeration catalog ( https://cwe.mitre.org/ )
    """

    uid: str # The Common Weakness Enumeration unique number assigned to a specific
             # weakness. A CWE Identifier begins "CWE" followed by a sequence of digits
             # that acts as a unique identifier. For example: `CWE-123`.


    # Optional:
    caption: str | None = None # The caption assigned to the Common Weakness Enumeration unique
                               # identifier.
    src_url: AnyUrl | None = None # URL pointing to the CWE Specification
                                  # See: https://cwe.mitre.org/
