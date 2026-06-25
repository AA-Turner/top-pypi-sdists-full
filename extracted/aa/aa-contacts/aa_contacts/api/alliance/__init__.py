from ninja import Router

from .contacts import router as contacts_router
from .tokens import router as token_router

router = Router()

router.add_router("/tokens", token_router, tags=["tokens"])
router.add_router("{int:alliance_id}/contacts", contacts_router, tags=["contacts"])
