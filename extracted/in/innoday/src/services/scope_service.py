"""Service for managing project scope documents and refinement workflow."""

from datetime import datetime, timezone
from typing import List, Optional

from sqlmodel import Session, select

from src.domain.project_update import ProjectUpdate, UpdateType
from src.domain.scope_document import ScopeDocument, ScopeStatus


class ScopeService:
    """Manages scope document lifecycle and refinement workflow."""

    def __init__(self, session: Session):
        self.session = session

    def create_initial_scope(
        self, project_id: str, requirements: str, created_by: str
    ) -> ScopeDocument:
        """Create the initial scope document for a project."""
        # Mark any existing scopes as not current
        existing_scopes = self.session.exec(
            select(ScopeDocument).where(
                ScopeDocument.project_id == project_id, ScopeDocument.is_current == True
            )
        ).all()

        for scope in existing_scopes:
            scope.is_current = False

        # Create new scope document
        scope = ScopeDocument(
            project_id=project_id,
            version=1,
            is_current=True,
            status=ScopeStatus.DRAFT,
            requirements=requirements,
            refined_scope=requirements,  # Start with original requirements
            created_by=created_by,
        )

        self.session.add(scope)
        self.session.commit()
        self.session.refresh(scope)

        return scope

    def get_current_scope(self, project_id: str) -> Optional[ScopeDocument]:
        """Get the current active scope document for a project."""
        return self.session.exec(
            select(ScopeDocument).where(
                ScopeDocument.project_id == project_id, ScopeDocument.is_current == True
            )
        ).first()

    def create_new_version(self, project_id: str, created_by: str) -> ScopeDocument:
        """Create a new version of the scope document."""
        current_scope = self.get_current_scope(project_id)
        if not current_scope:
            raise ValueError(f"No current scope found for project {project_id}")

        # Mark current as not current
        current_scope.is_current = False

        # Create new version
        new_scope = current_scope.create_new_version()
        new_scope.created_by = created_by
        new_scope.is_current = True

        self.session.add(new_scope)
        self.session.commit()
        self.session.refresh(new_scope)

        return new_scope

    def update_scope(self, scope_id: str, **updates) -> ScopeDocument:
        """Update a scope document with new information."""
        scope = self.session.get(ScopeDocument, scope_id)
        if not scope:
            raise ValueError(f"Scope document {scope_id} not found")

        # Only allow updates to non-final scopes
        if scope.status == ScopeStatus.FINAL:
            raise ValueError("Cannot update a finalized scope document")

        # Apply updates
        for key, value in updates.items():
            if hasattr(scope, key):
                setattr(scope, key, value)

        scope.updated_at = datetime.now(timezone.utc)

        self.session.add(scope)
        self.session.commit()
        self.session.refresh(scope)

        return scope

    def finalize_scope(self, scope_id: str) -> ScopeDocument:
        """Mark a scope document as final and ready for approval."""
        scope = self.session.get(ScopeDocument, scope_id)
        if not scope:
            raise ValueError(f"Scope document {scope_id} not found")

        scope.status = ScopeStatus.FINAL
        scope.finalized_at = datetime.now(timezone.utc)
        scope.updated_at = datetime.now(timezone.utc)

        self.session.add(scope)
        self.session.commit()
        self.session.refresh(scope)

        return scope

    def add_project_update(
        self,
        project_id: str,
        update_type: UpdateType,
        content: str,
        created_by: str,
        scope_document_id: Optional[str] = None,
        requires_client_input: bool = False,
    ) -> ProjectUpdate:
        """Add an update to the project requirements workflow."""
        update = ProjectUpdate(
            project_id=project_id,
            update_type=update_type,
            content=content,
            created_by=created_by,
            scope_document_id=scope_document_id,
            requires_client_input=requires_client_input,
        )

        self.session.add(update)
        self.session.commit()
        self.session.refresh(update)

        return update

    def get_pending_updates(self, project_id: str) -> List[ProjectUpdate]:
        """Get unprocessed updates for a project."""
        return self.session.exec(
            select(ProjectUpdate)
            .where(
                ProjectUpdate.project_id == project_id, ProjectUpdate.processed == False
            )
            .order_by(ProjectUpdate.created_at)
        ).all()

    def get_updates_requiring_input(self, project_id: str) -> List[ProjectUpdate]:
        """Get updates that need client input."""
        return self.session.exec(
            select(ProjectUpdate)
            .where(
                ProjectUpdate.project_id == project_id,
                ProjectUpdate.requires_client_input == True,
                ProjectUpdate.processed == False,
            )
            .order_by(ProjectUpdate.created_at)
        ).all()

    def process_update(
        self, update_id: str, response: Optional[str] = None
    ) -> ProjectUpdate:
        """Mark an update as processed with optional response."""
        update = self.session.get(ProjectUpdate, update_id)
        if not update:
            raise ValueError(f"Project update {update_id} not found")

        update.mark_processed(response)

        self.session.add(update)
        self.session.commit()
        self.session.refresh(update)

        return update

    def refine_scope_with_updates(
        self,
        scope_id: str,
        refined_scope: str,
        confidence_score: Optional[float] = None,
    ) -> ScopeDocument:
        """Update scope document after processing updates."""
        scope = self.session.get(ScopeDocument, scope_id)
        if not scope:
            raise ValueError(f"Scope document {scope_id} not found")

        scope.refined_scope = refined_scope
        scope.clarification_rounds += 1

        if confidence_score is not None:
            scope.confidence_score = confidence_score

        scope.updated_at = datetime.now(timezone.utc)

        self.session.add(scope)
        self.session.commit()
        self.session.refresh(scope)

        return scope
