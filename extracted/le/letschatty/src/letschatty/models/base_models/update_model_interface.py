import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, ClassVar, FrozenSet, Tuple, TypeVar

from pydantic import BaseModel, model_validator

from .helpers import _normalize_precision

T = TypeVar('T', bound='UpdateableMixin')

logger = logging.getLogger("UpdateableMixin")


class UpdateableMixin(BaseModel):
    """Interface for models that can be updated, creating a new instance. It automatically handles the updated_at timestamp and mantains the frozen fields.

    Update rule (single place for every asset): `update(other)` applies ONLY the fields `other` was
    built with (`other.model_fields_set`). A field the caller did not send keeps its stored value; it is
    not reset to the model default. A field that WAS sent is applied as sent, an explicit `None`
    included (that is how a client clears an optional field). To clear a field, send it.

    Scope fields (`scope_fields`: `account_id`, `account_ids`) are the exception: `None` for them means
    "not sent", so a full save can never erase the account scoping a migration stamped. The only way to
    widen `account_ids` to "all the accounts" is an explicit `[]`.
    """

    #: Fields that tie an asset to WhatsApp account(s). A null for them is never written: it is read as
    #: "not sent". Declared once here so no asset needs its own guard.
    scope_fields: ClassVar[FrozenSet[str]] = frozenset({"account_id", "account_ids"})

    @model_validator(mode='before')
    @classmethod
    def _null_scope_is_not_sent(cls, data: Any) -> Any:
        """`{"account_id": None}` is built as if `account_id` were not in the body: it is not in
        `model_fields_set`, so `update()` keeps the stored value, and the field takes its default."""
        if isinstance(data, dict) and any(data.get(name, False) is None for name in cls.scope_fields):
            return {key: value for key, value in data.items() if not (key in cls.scope_fields and value is None)}
        return data

    def update_from_dict(self: T, **kwargs) -> T:
        """
        Updates non-frozen fields of the model with new values.
        Automatically handles the updated_at timestamp.

        The result remembers which fields were set: the ones this model had plus the ones updated
        here, so an instance rebuilt in between (normalising a payload, for instance) does not
        turn into "everything was sent".

        Args:
            **kwargs: Fields to update and their new values

        Returns:
            A new instance of the model with updated values
        """
        # Get current model data
        current_data = self.model_dump(by_alias=True)

        # Get frozen field names
        frozen_fields = {
            field.alias or field_name for field_name, field in self.__class__.model_fields.items()
            if field.frozen
        }

        # Remove any frozen fields from updates
        updates = {k: v for k, v in kwargs.items() if k not in frozen_fields}

        # Always update the updated_at timestamp if it exists in the model
        if 'updated_at' in self.__class__.model_fields:
            updates['updated_at'] = _normalize_precision(datetime.now(ZoneInfo("UTC")))

        # Merge current data with updates
        new_data = {**current_data, **updates}

        # Create new instance
        new = self.__class__(**new_data)
        names_updated = {
            name for name, field in self.__class__.model_fields.items()
            if (field.alias or name) in updates or name in updates
        }
        fields_set = new.model_fields_set
        fields_set.clear()
        fields_set.update(self.model_fields_set | names_updated)
        return new

    def patch_from_dict(self: T, **kwargs) -> T:
        """Like `update_from_dict`, but the result is marked as carrying ONLY `kwargs` (+ `updated_at`).

        For "load, change two fields, save" flows: `service.update(id, loaded.patch_from_dict(name=...))`
        writes `name` and nothing else. A loaded model (a cached one above all) has every field set, so
        passing it as is would write back all of them, stale ones included.
        """
        patch = self.update_from_dict(**kwargs)
        model_fields = self.__class__.model_fields
        sent = {name for name, field in model_fields.items() if (field.alias or name) in kwargs or name in kwargs}
        if "updated_at" in model_fields:
            sent.add("updated_at")
        fields_set = patch.model_fields_set
        fields_set.clear()
        fields_set.update(sent)
        return patch

    def merge(self: T, other: T) -> Tuple[T, FrozenSet[str]]:
        """Applies the fields `other` was built with on top of this model.

        Returns the merged model and the names of the fields a database write has to persist: the
        ones sent, plus any other that the merge changed on its own (a derived field), plus
        `updated_at`. Everything else is left as stored.
        """
        model_fields = self.__class__.model_fields
        frozen = {name for name, field in model_fields.items() if field.frozen}
        sent = {name for name in other.model_fields_set if name in model_fields and name not in frozen}
        dumped = other.model_dump(by_alias=True)
        updates = {
            (model_fields[name].alias or name): dumped[model_fields[name].alias or name]
            for name in sent
            if (model_fields[name].alias or name) in dumped
        }
        self._log_scope_changes(other)
        merged = self.update_from_dict(**updates)
        derived = {name for name in model_fields if name not in frozen and getattr(merged, name) != getattr(self, name)}
        return merged, frozenset(sent | derived | ({"updated_at"} if "updated_at" in model_fields else set()))

    def update(self: T, other: T) -> T:
        """
        Updates the model with the fields of another model that were actually sent (see the class doc).
        """
        return self.merge(other)[0]

    def _log_scope_changes(self, other: 'UpdateableMixin') -> None:
        """A write that, under the old whole-document merge, would have erased the account scope."""
        for name in self.scope_fields & set(self.__class__.model_fields):
            stored = getattr(self, name)
            if not stored:
                continue
            if name not in other.model_fields_set:
                logger.warning(
                    "account scope kept: %s of %s %s was not sent (or null); a whole-document save would have erased it",
                    name, type(self).__name__, getattr(self, "id", None),
                    extra={"event": "account_scope_kept", "asset": type(self).__name__, "asset_id": getattr(self, "id", None),
                           "field": name, "stored": stored},
                )
            elif not getattr(other, name):
                logger.info(
                    "account scope cleared on purpose: %s of %s %s set to empty",
                    name, type(self).__name__, getattr(self, "id", None),
                    extra={"event": "account_scope_cleared", "asset": type(self).__name__, "asset_id": getattr(self, "id", None),
                           "field": name, "stored": stored},
                )
