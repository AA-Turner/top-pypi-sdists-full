"""Tests for scope document and project update management."""

from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.organization import Organization
from src.domain.project import Project, ProjectStatus
from src.domain.project_update import UpdateType
from src.domain.scope_document import ScopeStatus
from src.services.scope_service import ScopeService
from tests.db_helpers import build_test_engine


@pytest.fixture
def test_session():
    """Create a test database session."""

    engine = build_test_engine()

    with Session(engine) as session:
        yield session


@pytest.fixture
def test_organization(test_session):
    """Create a test organization."""
    org = Organization(
        id=str(uuid4()),
        name="Test Organization",
        contact_email="test@example.com",
    )
    test_session.add(org)
    test_session.commit()
    return org


@pytest.fixture
def test_project(test_session, test_organization):
    """Create a test project."""
    project = Project(
        id=str(uuid4()),
        organization_id=test_organization.id,
        alias="TEST",
        name="Test Project",
        description="A test project for scope management",
        status=ProjectStatus.PLANNING,
    )
    test_session.add(project)
    test_session.commit()
    return project


@pytest.fixture
def scope_service(test_session):
    """Create a scope service instance."""
    return ScopeService(test_session)


class TestScopeDocument:
    """Test scope document management."""

    def test_create_initial_scope(self, scope_service, test_project):
        """Test creating initial scope document."""
        requirements = "Build a web application with user authentication"

        scope = scope_service.create_initial_scope(
            project_id=test_project.id, requirements=requirements, created_by="user123"
        )

        assert scope.id is not None
        assert scope.project_id == test_project.id
        assert scope.version == 1
        assert scope.is_current is True
        assert scope.status == ScopeStatus.DRAFT
        assert scope.requirements == requirements
        assert scope.refined_scope == requirements
        assert scope.created_by == "user123"

    def test_get_current_scope(self, scope_service, test_project):
        """Test getting current active scope."""
        # Create initial scope
        scope1 = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Initial requirements",
            created_by="user123",
        )

        # Get current scope
        current = scope_service.get_current_scope(test_project.id)
        assert current.id == scope1.id
        assert current.is_current is True

    def test_create_new_version(self, scope_service, test_project):
        """Test creating new version of scope document."""
        # Create initial scope
        scope1 = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Initial requirements",
            created_by="user123",
        )

        # Create new version
        scope2 = scope_service.create_new_version(
            project_id=test_project.id, created_by="user456"
        )

        assert scope2.version == 2
        assert scope2.is_current is True
        assert scope2.status == ScopeStatus.DRAFT
        assert scope2.requirements == scope1.requirements

        # Verify old version is not current
        scope_service.session.refresh(scope1)
        assert scope1.is_current is False

    def test_update_scope(self, scope_service, test_project):
        """Test updating scope document."""
        scope = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Initial requirements",
            created_by="user123",
        )

        updated_scope = scope_service.update_scope(
            scope_id=scope.id,
            refined_scope="Refined scope with more details",
            deliverables="- User authentication\n- Dashboard\n- Reports",
            estimated_hours=120,
            confidence_score=0.85,
        )

        assert updated_scope.refined_scope == "Refined scope with more details"
        assert (
            updated_scope.deliverables
            == "- User authentication\n- Dashboard\n- Reports"
        )
        assert updated_scope.estimated_hours == 120
        assert updated_scope.confidence_score == 0.85

    def test_finalize_scope(self, scope_service, test_project):
        """Test finalizing scope document."""
        scope = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Initial requirements",
            created_by="user123",
        )

        finalized = scope_service.finalize_scope(scope.id)

        assert finalized.status == ScopeStatus.FINAL
        assert finalized.finalized_at is not None

    def test_cannot_update_finalized_scope(self, scope_service, test_project):
        """Test that finalized scope cannot be updated."""
        scope = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Initial requirements",
            created_by="user123",
        )

        scope_service.finalize_scope(scope.id)

        with pytest.raises(ValueError) as exc:
            scope_service.update_scope(
                scope_id=scope.id, refined_scope="Trying to update"
            )

        assert "Cannot update a finalized scope" in str(exc.value)


class TestProjectUpdate:
    """Test project update management."""

    def test_add_project_update(self, scope_service, test_project):
        """Test adding project update."""
        update = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.REQUIREMENT,
            content="Need to add payment processing",
            created_by="user123",
            requires_client_input=False,
        )

        assert update.id is not None
        assert update.project_id == test_project.id
        assert update.update_type == UpdateType.REQUIREMENT
        assert update.content == "Need to add payment processing"
        assert update.processed is False
        assert update.requires_client_input is False

    def test_get_pending_updates(self, scope_service, test_project):
        """Test getting pending updates."""
        # Add some updates
        update1 = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.REQUIREMENT,
            content="Requirement 1",
            created_by="user123",
        )

        update2 = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.CLARIFICATION,
            content="Clarification 1",
            created_by="user456",
        )

        # Process one update
        scope_service.process_update(update1.id)

        # Get pending updates
        pending = scope_service.get_pending_updates(test_project.id)

        assert len(pending) == 1
        assert pending[0].id == update2.id

    def test_get_updates_requiring_input(self, scope_service, test_project):
        """Test getting updates that need client input."""
        # Add updates with different requirements
        scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.FEEDBACK,
            content="General feedback",
            created_by="user123",
            requires_client_input=False,
        )

        update2 = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.QUESTION,
            content="What database should we use?",
            created_by="agent",
            requires_client_input=True,
        )

        # Get updates requiring input
        requiring_input = scope_service.get_updates_requiring_input(test_project.id)

        assert len(requiring_input) == 1
        assert requiring_input[0].id == update2.id

    def test_process_update(self, scope_service, test_project):
        """Test processing an update."""
        update = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.QUESTION,
            content="What authentication method?",
            created_by="agent",
            requires_client_input=True,
        )

        processed = scope_service.process_update(
            update_id=update.id, response="Use OAuth 2.0 with Google and GitHub"
        )

        assert processed.processed is True
        assert processed.processed_at is not None
        assert processed.response == "Use OAuth 2.0 with Google and GitHub"

    def test_refine_scope_with_updates(self, scope_service, test_project):
        """Test refining scope after processing updates."""
        # Create initial scope
        scope = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Build a web app",
            created_by="user123",
        )

        # Add and process some updates
        scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.CLARIFICATION,
            content="Need user roles",
            created_by="user123",
            scope_document_id=scope.id,
        )

        # Refine scope
        refined = scope_service.refine_scope_with_updates(
            scope_id=scope.id,
            refined_scope="Build a web app with role-based access control",
            confidence_score=0.75,
        )

        assert refined.refined_scope == "Build a web app with role-based access control"
        assert refined.clarification_rounds == 1
        assert refined.confidence_score == 0.75


class TestWorkflow:
    """Test complete scope refinement workflow."""

    def test_complete_workflow(self, scope_service, test_project):
        """Test complete workflow from requirements to finalized scope."""
        # 1. Create initial scope from requirements
        scope = scope_service.create_initial_scope(
            project_id=test_project.id,
            requirements="Build an e-commerce platform",
            created_by="client",
        )

        # 2. Agent asks clarifying questions
        q1 = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.QUESTION,
            content="What payment methods should be supported?",
            created_by="agent",
            scope_document_id=scope.id,
            requires_client_input=True,
        )

        q2 = scope_service.add_project_update(
            project_id=test_project.id,
            update_type=UpdateType.QUESTION,
            content="Will international shipping be needed?",
            created_by="agent",
            scope_document_id=scope.id,
            requires_client_input=True,
        )

        # 3. Client provides answers
        scope_service.process_update(
            update_id=q1.id, response="Credit cards, PayPal, and Apple Pay"
        )

        scope_service.process_update(
            update_id=q2.id, response="Yes, to US, Canada, and EU countries"
        )

        # 4. Agent refines scope based on answers
        scope_service.refine_scope_with_updates(
            scope_id=scope.id,
            refined_scope="""
            Build an e-commerce platform with:
            - Multiple payment methods (Credit cards, PayPal, Apple Pay)
            - International shipping to US, Canada, and EU
            - Product catalog with search and filtering
            - Shopping cart and checkout
            - Order management system
            """,
            confidence_score=0.9,
        )

        # 5. Update with deliverables and estimates
        scope_service.update_scope(
            scope_id=scope.id,
            deliverables="""
            - Product catalog system
            - Shopping cart functionality
            - Payment integration (3 providers)
            - Shipping calculator
            - Order management dashboard
            """,
            estimated_hours=320,
            estimated_cost=32000.0,
        )

        # 6. Finalize scope for approval
        final = scope_service.finalize_scope(scope.id)

        # Verify final state
        assert final.status == ScopeStatus.FINAL
        assert final.clarification_rounds == 1
        assert final.confidence_score == 0.9
        assert final.estimated_hours == 320
        assert final.finalized_at is not None

        # Verify all updates are processed
        pending = scope_service.get_pending_updates(test_project.id)
        assert len(pending) == 0
