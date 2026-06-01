# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 CERN.
#
# Invenio-Requests is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Validation utilities for request records."""

from ..errors import ChildrenNotSupportedError


def validate_children_allowed(event):
    """Validate that an event type allows children before setting parent_id.

    :param event: The RequestEvent instance to validate.
    :raises ChildrenNotSupportedError: If the event type doesn't support children
                                       but has a parent_id set.
    """
    if event.parent_id is not None:
        # Check if event type supports children
        if hasattr(event, "type") and event.type:
            if not getattr(event.type, "allow_children", False):
                raise ChildrenNotSupportedError(
                    event.type.type_id,
                    f"Event type '{event.type.type_id}' does not support children. "
                    f"Cannot set parent_id for this event type.",
                )
