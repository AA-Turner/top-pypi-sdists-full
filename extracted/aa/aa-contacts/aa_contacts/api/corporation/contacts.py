from ninja import Path, Router

from aa_contacts.api import common
from aa_contacts.api.schema import (
    ContactSchema,
    ServerLinkInputSchema,
    ServerLinkSchema,
    UpdateContactSchema,
)

router = Router()


@router.get("/", response={200: list[ContactSchema], 403: None, 404: None})
def list_contacts(request, corporation_id: int = Path(...)):
    return common.list_contacts(common.CORPORATION, corporation_id, request.user)


@router.post("/update", response={200: None, 403: None, 404: None})
def update_contacts(request, corporation_id: int = Path(...)):
    return common.update_contacts(common.CORPORATION, corporation_id, request.user)


@router.patch("/{int:contact_pk}", response={200: None, 403: None, 404: None})
def edit_contact(
    request, data: UpdateContactSchema, contact_pk: int, corporation_id: int = Path(...)
):
    return common.edit_contact(
        common.CORPORATION, corporation_id, contact_pk, data, request.user
    )


@router.post(
    "/{int:contact_pk}/server-links",
    response={200: ServerLinkSchema, 403: None, 404: None},
)
def create_server_link(
    request,
    data: ServerLinkInputSchema,
    contact_pk: int,
    corporation_id: int = Path(...),
):
    return common.create_server_link(
        common.CORPORATION, corporation_id, contact_pk, data, request.user
    )


@router.put(
    "/{int:contact_pk}/server-links/{int:link_pk}",
    response={200: ServerLinkSchema, 403: None, 404: None},
)
def update_server_link(
    request,
    data: ServerLinkInputSchema,
    contact_pk: int,
    link_pk: int,
    corporation_id: int = Path(...),
):
    return common.update_server_link(
        common.CORPORATION, corporation_id, contact_pk, link_pk, data, request.user
    )


@router.delete(
    "/{int:contact_pk}/server-links/{int:link_pk}",
    response={200: None, 403: None, 404: None},
)
def delete_server_link(
    request,
    contact_pk: int,
    link_pk: int,
    corporation_id: int = Path(...),
):
    return common.delete_server_link(
        common.CORPORATION, corporation_id, contact_pk, link_pk, request.user
    )
