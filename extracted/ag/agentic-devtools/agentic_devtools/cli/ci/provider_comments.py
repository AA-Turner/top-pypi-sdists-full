"""Pull-request comment and identity capabilities."""

from __future__ import annotations

from abc import ABC, abstractmethod


class _ProviderCommentsMixin(ABC):
    """Pull-request comment and identity capabilities."""

    @abstractmethod
    def post_comment(self, pr_number: int, body: str) -> int:
        """Post a comment on a pull request.

        Args:
            pr_number: Pull request number.
            body: Comment body text.

        Returns:
            The ID of the created comment.
        """

    def post_comment_as_pr_token(self, pr_number: int, body: str) -> int:
        """Post a comment using the PR-token identity when supported.

        Providers that support multiple comment identities can override this
        to force the same identity used by ``dispatch_conflict_repair`` and
        marker-authenticated dedup checks.  The default implementation falls
        back to ``post_comment`` for backward compatibility.

        Args:
            pr_number: Pull request number.
            body: Comment body text.

        Returns:
            The ID of the created comment.
        """
        return self.post_comment(pr_number, body)

    @abstractmethod
    def update_comment(self, comment_id: int, body: str) -> int | None:
        """Update an existing comment.

        Args:
            comment_id: ID of the comment to update.
            body: New comment body text.

        Returns:
            The current comment ID when the provider migrates or redirects the comment,
            otherwise ``None`` when it updates in place.
        """

    def update_comment_as_pr_token(self, comment_id: int, body: str) -> int | None:
        """Update a comment using the PR-token identity when supported.

        Providers with a single comment identity may use ``update_comment``.
        Providers that separate bookkeeping from dispatch identities should
        override this method to preserve PR-token-authored records.
        """
        return self.update_comment(comment_id, body)

    def delete_comment(self, comment_id: int) -> None:
        """Delete an issue comment.

        Args:
            comment_id: ID of the comment to delete.

        Raises:
            NotImplementedError: When the provider does not support deleting comments.
        """
        raise NotImplementedError(f"{type(self).__name__} does not implement delete_comment")

    @abstractmethod
    def find_comment(self, pr_number: int, marker: str) -> tuple[int, str] | None:
        """Find a comment containing a specific marker string.

        Args:
            pr_number: Pull request number.
            marker: Marker string to search for in comment bodies.

        Returns:
            Tuple of (comment_id, comment_body) if found, None otherwise.
        """

    def get_approver_login(self) -> str:
        """Return the approver identity login/name for this provider.

        Best-effort helper for providers that can resolve the identity used for
        automated PR approval. Returns an empty string when the approver
        identity is not configured, resolution fails, or the provider does not
        support identity lookup. Callers must handle the ``""`` case.

        Returns:
            Provider-specific approver login/name, or ``""`` when unavailable.
        """
        return ""

    def get_pr_token_login(self) -> str:
        """Return the default workflow-token identity login used for comments and dispatch.

        Best-effort helper for providers that can resolve the identity used for
        posting comments and dispatching trusted workflow actions. Returns an
        empty string when the token is absent, resolution fails, or the provider
        does not support identity lookup. Callers must handle the ``""`` case.

        Returns:
            Provider-specific default workflow-token login/name, or ``""`` when unavailable.
        """
        return ""

    def get_bookkeeping_token_login(self) -> str:
        """Return the verified AI PR Loop bookkeeping identity, when supported."""
        return ""

    def get_trusted_loop_comment_logins(self) -> set[str]:
        """Return normalized identities trusted to own AI PR Loop state comments."""
        login = self.get_pr_token_login().strip()
        return {login.casefold()} if login else set()

    def get_dispatch_login(self) -> str:
        """Return the identity used for trusted AI PR Loop dispatch comments."""
        return self.get_pr_token_login()
