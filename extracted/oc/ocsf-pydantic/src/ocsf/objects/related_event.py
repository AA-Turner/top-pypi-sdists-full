from pydantic import BaseModel

from .kill_chain_phase import KillChainPhase
from .observable import Observable
from .attack import MITREATTCK

class RelatedEvent(BaseModel):
    """
    The Related Event object describes an OCSF event related to a finding.
    """

    uid: str # The unique identifier of the related OCSF event. This value must be equal
             # to `metadata.uid` in the corresponding related event.

    # Recommended:
    type_uid: int | None = None # The unique identifier of the related OCSF event type. <p>For example:
                                # `100701.`</p>

    # Optional:
    attacks: list[MITREATTCK] | None = None
    kill_chain: list[KillChainPhase] | None = None
    observables: list[Observable] | None = None
    product_uid: str | None = None # The unique identifier of the product that reported the related
                                   # event.
    type: str | None = None # The type of the related event, as defined by `type_uid`.
                            # <p>For example: `Process Activity: Launch.`</p>
    type_name: str | None = None # The type of the related OCSF event, as defined by
                                 # `type_uid`. <p>For example: `Process Activity:
                                 # Launch.`</p>
