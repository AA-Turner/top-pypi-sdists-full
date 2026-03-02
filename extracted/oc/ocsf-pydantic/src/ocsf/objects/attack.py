
from pydantic import BaseModel

from .technique import Technique, SubTechnique, Tactic

class MITREATTCK(BaseModel):
    """
    The MITRE ATT&CK object describes the tactic, technique
    & sub-technique associated to an attack as defined in ATT&CK Matrix.
    """

    # Recommended:
    version: str | None = None # The ATT&CK Matrix version.

    # Optional:
    tactic: Tactic | None = None
    tactics: list[Tactic] | None = None
    technique: Technique | None = None
    sub_technique: SubTechnique | None = None
