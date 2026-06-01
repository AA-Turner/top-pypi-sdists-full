# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2022-2025 Graz University of Technology.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks for requests."""

from datetime import datetime, timezone

from celery import shared_task
from flask import current_app
from invenio_access.permissions import system_identity
from invenio_search.engine import dsl

from invenio_requests.proxies import current_user_moderation_service
from invenio_requests.services.user_moderation.errors import OpenRequestAlreadyExists

from .proxies import current_requests_service


@shared_task
def check_expired_requests():
    """Retrieve expired requests and perform expired action."""
    service = current_requests_service
    now = datetime.now(timezone.utc).isoformat()

    # using scan to get all requests
    requests_list = service.scan(
        identity=system_identity,
        extra_filter=dsl.query.Bool(
            "must",
            must=[
                # somehow querying for '"term", **{"is_expired: True"}' will not return any requests # noqa
                dsl.Q("range", **{"expires_at": {"lte": now}}),
                dsl.Q("term", **{"is_open": True}),
            ],
        ),
    )
    for r in requests_list:
        try:
            service.execute_action(
                identity=system_identity, id_=r["id"], action="expire"
            )
        except Exception as e:
            current_app.logger.warning(e)
            pass


@shared_task(ignore_result=True)
def request_moderation(user_id):
    """Creates a task to request moderation for a user.

    Why this task: when specific actions happen e.g record is published or community
    created, we want to request moderation for a user. However, the moderation service
    might implement heavier operations (e.g. querying) and we don't want to delay the
    publishing of the record.
    """
    try:
        current_user_moderation_service.request_moderation(
            system_identity, user_id=user_id
        )
    except OpenRequestAlreadyExists as ex:
        current_app.logger.warning(ex.description)
