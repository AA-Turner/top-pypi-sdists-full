"""`RegistrationTrail` on `registration_activity`: the same writes that `ChattyAssetCollectionInterface.insert` and
`update` ran for api-chatty's `RegistrationActivity` (the form dumped with `SerializerType.DATABASE`, an `insert_one`; an
`update_now()`, a `$set` by `ObjectId(id)` and `NotFoundError` when nothing matched), with their logs. The company is
not in the filter, as before: the form's id names the document. No cache."""
from __future__ import annotations

import logging

from bson import ObjectId

from ...models.forms.company.meta_register import MetaRegister
from ...models.utils.custom_exceptions.custom_exceptions import NotFoundError
from ...models.utils.types.serializer_type import SerializerType

COLLECTION = "registration_activity"

# The logger and the texts of `ChattyAssetCollectionInterface`, which wrote this collection before.
logger = logging.getLogger("CollectionInterface")


class MongoRegistrationTrail:
    """On a Motor collection, resolved by whoever wires it."""

    def __init__(self, collection):
        self.collection = collection

    async def open(self, company_id: str, form: MetaRegister) -> None:
        if not isinstance(form, MetaRegister):
            raise ValueError(f"Asset must be of type {MetaRegister.__name__}")
        document = form.model_dump_json(serializer=SerializerType.DATABASE)
        logger.debug(f"Inserting document: {document}")
        result = await self.collection.insert_one(document)
        if not result.inserted_id:
            raise Exception("Failed to insert document")
        logger.debug(f"Inserted document with id {result.inserted_id}")

    async def save(self, company_id: str, form: MetaRegister) -> None:
        logger.debug(f"Updating document with id {form.id}")
        if not isinstance(form, MetaRegister):
            raise ValueError(f"Asset must be of type {MetaRegister.__name__}")
        form.update_now()
        document = form.model_dump_json(serializer=SerializerType.DATABASE)
        document.pop('_id', None)
        result = await self.collection.update_one({"_id": ObjectId(form.id)}, {"$set": document})
        if result.matched_count == 0:
            raise NotFoundError(f"No document found with id {form.id}")
        if result.modified_count == 0:
            logger.debug(f"No changes were made to the document with id {form.id} probably because the values were the same")
