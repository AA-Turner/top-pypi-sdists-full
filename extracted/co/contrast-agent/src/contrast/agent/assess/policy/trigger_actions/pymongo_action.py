# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

from collections.abc import Mapping
from contrast.agent.assess.policy.trigger_actions.default_action import DefaultAction
from contrast.agent.assess.utils import is_trackable


class PyMongoAction(DefaultAction):
    """
    The DefaultAction would report findings for NoSQLi if any value in the
    query were an untrusted string. This would be a false positive (and if
    it were a true finding, then the database could never hold user data).

    This action will only report findings if a dictionary exists that contains
    all untrusted keys and values. In that case, the dictionary is fully under
    user control and a malicious user could use object expansion to perform NoSQL
    injection.
    """

    unwind_source = False
    unwind_source_recurse = False

    def is_violated(self, source, required_tags, disallowed_tags, **kwargs):
        return self._is_violated(source, required_tags, disallowed_tags, **kwargs)

    def _is_violated(self, doc_field, required_tags, disallowed_tags, **kwargs):
        if isinstance(doc_field, Mapping):
            # if a JSON object contains another JSON object, we need to check
            # whether any inner JSON object is fully under user control
            object_fields = [
                field
                for field in doc_field.values()
                if isinstance(field, (Mapping, list))
            ]
            if object_fields:
                return any(
                    self._is_violated(obj, required_tags, disallowed_tags, **kwargs)
                    for obj in object_fields
                )

            # otherwise, check if this JSON object is fully under user control
            else:
                return all(
                    self._is_violated(key, required_tags, disallowed_tags)
                    and self._is_violated(value, required_tags, disallowed_tags)
                    for key, value in doc_field.items()
                    if key != "_id"  # ignore MongoDB's internal _id field
                )

        if isinstance(doc_field, list):
            return any(
                self._is_violated(doc, required_tags, disallowed_tags, **kwargs)
                for doc in doc_field
            )

        return not is_trackable(doc_field) or super().is_violated(
            doc_field, required_tags, disallowed_tags, **kwargs
        )
