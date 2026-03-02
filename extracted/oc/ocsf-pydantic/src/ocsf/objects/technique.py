from pydantic import AnyUrl
from ._entity import Entity


class Technique(Entity):
    """
    The Technique object describes the technique ID and/or name associated to an
    attack, as defined by https://attack.mitre.org/wiki/ATT&CK_Matrix
    """

    # Optional:
    name: str | None = None # The name of the attack technique
                            # For example: `Active Scanning`.
    src_url: AnyUrl | None = None # The versioned permalink of the attack technique
                                  # For example: `https://attack.mitre.org/versions/v14/techniques/T1595/`
    uid: str | None = None # The unique identifier of the attack technique. For example: `T1595`.

class SubTechnique(Technique):
    pass

class Tactic(Technique):
    pass
