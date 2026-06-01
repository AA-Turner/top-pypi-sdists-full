# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Firestore client for managing GitHub subscriptions."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from google.cloud import firestore  # type: ignore[attr-defined]
from google.cloud.firestore_v1.base_query import FieldFilter

from agent_message_bus.models import (
    DEFAULT_TTL_HOURS,
    CreateSubscriptionRequest,
    Subscription,
    WatchEvent,
)
from agent_message_bus.url_parser import (
    extract_session_id,
    parse_github_url,
)

logger = logging.getLogger(__name__)

COLLECTION_NAME = "subscriptions"


class SubscriptionStore:
    """Firestore-backed subscription storage."""

    def __init__(self, project: str | None = None) -> None:
        """Initialize the Firestore client.

        Args:
            project: GCP project ID. If None, uses the default project
                     from the environment (GOOGLE_CLOUD_PROJECT or ADC).
        """
        self._db = firestore.Client(project=project)
        self._collection = self._db.collection(COLLECTION_NAME)

    def create_or_update(self, request: CreateSubscriptionRequest) -> Subscription:
        """Create or upsert a subscription.

        If a subscription already exists for the same session + github_url,
        it is updated (TTL extended, watch_events merged). Otherwise a new
        document is created.

        Args:
            request: The subscription creation request.

        Returns:
            The created or updated Subscription.
        """
        parsed = parse_github_url(request.github_url)
        session_id = extract_session_id(request.session_url)
        watch_events = (
            request.watch_events if request.watch_events is not None else WatchEvent.all_events()
        )
        now = datetime.now(tz=timezone.utc)
        expires_at = now + timedelta(
            hours=request.ttl_hours if request.ttl_hours is not None else DEFAULT_TTL_HOURS
        )

        # Check for existing subscription (same session + same issue/PR)
        existing = self._find_existing(
            session_url=request.session_url,
            owner=parsed.owner,
            repo=parsed.repo,
            number=parsed.number,
        )

        if existing:
            # Upsert: extend TTL and merge watch events
            doc_ref = self._collection.document(existing.id)
            merged_events = list(set(existing.watch_events) | set(watch_events))
            doc_ref.update(
                {
                    "watch_events": [e.value for e in merged_events],
                    "expires_at": expires_at,
                    "slack_users_cc": request.slack_users_cc or existing.slack_users_cc,
                }
            )
            existing.watch_events = merged_events
            existing.expires_at = expires_at
            if request.slack_users_cc:
                existing.slack_users_cc = request.slack_users_cc
            return existing

        # Create new subscription
        doc_ref = self._collection.document()
        subscription = Subscription(
            id=doc_ref.id,
            session_url=request.session_url,
            session_id=session_id,
            owner=parsed.owner,
            repo=parsed.repo,
            number=parsed.number,
            type=parsed.type,
            github_url=request.github_url,
            watch_events=watch_events,
            created_at=now,
            expires_at=expires_at,
            slack_users_cc=request.slack_users_cc,
            created_by=request.created_by,
        )
        # Use model_dump() without mode="json" to preserve native datetime objects
        # so Firestore stores them as Timestamps (needed for queries and TTL).
        # Enum values need manual serialization since Firestore doesn't handle them.
        data = subscription.model_dump()
        data["watch_events"] = [e.value for e in subscription.watch_events]
        data["type"] = subscription.type.value
        doc_ref.set(data)
        logger.info(
            "Created subscription %s for %s/%s#%d -> session %s",
            doc_ref.id,
            parsed.owner,
            parsed.repo,
            parsed.number,
            session_id,
        )
        return subscription

    def find_by_issue(
        self,
        owner: str,
        repo: str,
        number: int,
    ) -> list[Subscription]:
        """Find all active subscriptions for a given issue/PR.

        Args:
            owner: GitHub repo owner.
            repo: GitHub repo name.
            number: Issue or PR number.

        Returns:
            List of active (non-expired) Subscription objects.
        """
        now = datetime.now(tz=timezone.utc)
        query = (
            self._collection.where(filter=FieldFilter("owner", "==", owner))
            .where(filter=FieldFilter("repo", "==", repo))
            .where(filter=FieldFilter("number", "==", number))
            .where(filter=FieldFilter("expires_at", ">", now))
        )
        docs = query.stream()
        return [self._doc_to_subscription(doc) for doc in docs]

    def find_by_session(self, session_url: str) -> list[Subscription]:
        """Find all active subscriptions for a Devin session.

        Args:
            session_url: The Devin session URL.

        Returns:
            List of active Subscription objects for the session.
        """
        now = datetime.now(tz=timezone.utc)
        query = self._collection.where(filter=FieldFilter("session_url", "==", session_url)).where(
            filter=FieldFilter("expires_at", ">", now)
        )
        docs = query.stream()
        return [self._doc_to_subscription(doc) for doc in docs]

    def delete_by_id(self, subscription_id: str) -> bool:
        """Delete a subscription by its document ID.

        Args:
            subscription_id: Firestore document ID.

        Returns:
            True if the document existed and was deleted.
        """
        doc_ref = self._collection.document(subscription_id)
        doc = doc_ref.get()
        if doc.exists:
            doc_ref.delete()
            logger.info("Deleted subscription %s", subscription_id)
            return True
        return False

    def delete_by_match(
        self,
        session_url: str,
        github_url: str | None = None,
    ) -> int:
        """Delete subscriptions matching session URL and optionally GitHub URL.

        Args:
            session_url: The Devin session URL.
            github_url: Optional GitHub URL to narrow the match.

        Returns:
            Number of subscriptions deleted.
        """
        query = self._collection.where(filter=FieldFilter("session_url", "==", session_url))
        if github_url:
            query = query.where(filter=FieldFilter("github_url", "==", github_url))

        deleted = 0
        for doc in query.stream():
            doc.reference.delete()
            deleted += 1
            logger.info("Deleted subscription %s", doc.id)

        return deleted

    def _find_existing(
        self,
        session_url: str,
        owner: str,
        repo: str,
        number: int,
    ) -> Subscription | None:
        """Find an existing subscription for the same session + issue/PR."""
        query = (
            self._collection.where(filter=FieldFilter("session_url", "==", session_url))
            .where(filter=FieldFilter("owner", "==", owner))
            .where(filter=FieldFilter("repo", "==", repo))
            .where(filter=FieldFilter("number", "==", number))
        )
        docs = list(query.stream())
        if docs:
            return self._doc_to_subscription(docs[0])
        return None

    @staticmethod
    def _doc_to_subscription(doc: firestore.DocumentSnapshot) -> Subscription:
        """Convert a Firestore document to a Subscription model."""
        data = doc.to_dict()
        data["id"] = doc.id
        # Convert Firestore Timestamp objects to datetime if needed
        for field in ("created_at", "expires_at", "last_notified_at"):
            if field in data and data[field] is not None and not isinstance(data[field], datetime):
                data[field] = data[field].replace(tzinfo=timezone.utc)
        # Convert string watch_events back to enum values
        if data.get("watch_events"):
            data["watch_events"] = [WatchEvent(e) for e in data["watch_events"]]
        return Subscription.model_validate(data)
