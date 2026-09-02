"""Unit tests for Project functionality"""

from unittest.mock import Mock
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.project import (
    Project,
    ProjectPriority,
    ProjectRepository,
    ProjectStatus,
    RepositoryLayer,
)
from src.services.project_service import ProjectService
from tests.db_helpers import build_test_engine


@pytest.fixture
def memory_session():
    """Create an in-memory SQLite session for testing"""
    engine = build_test_engine()
    with Session(engine) as session:
        yield session


class TestProjectModel:
    """Test Project domain model"""

    def test_create_project(self):
        """Test creating a basic project"""
        project = Project(
            id=str(uuid4()),
            organization_id="org-123",
            alias="TEST",
            name="Test Project",
            description="A test project",
            status=ProjectStatus.PLANNING,
            priority=ProjectPriority.MEDIUM,
        )

        assert project.name == "Test Project"
        assert project.status == ProjectStatus.PLANNING
        assert project.priority == ProjectPriority.MEDIUM
        assert project.tags == []
        assert project.goals is None
        assert project.ticket_creation_config is None

    def test_project_with_all_fields(self):
        """Test project with all optional fields"""
        project = Project(
            id=str(uuid4()),
            organization_id="org-123",
            alias="FULL",
            name="Full Project",
            description="A complete project",
            goals="- Goal 1\n- Goal 2",
            scope_limitations="Not included: Feature X",
            spec="A project that does X for Y users.",
            project_context="## Repos\n- repo-a\n- repo-b",
            status=ProjectStatus.ACTIVE,
            priority=ProjectPriority.HIGH,
            tags=["important", "q1"],
            ticket_creation_config={"board_id": "board-123", "labels": ["bug"]},
        )

        assert project.goals == "- Goal 1\n- Goal 2"
        assert project.scope_limitations == "Not included: Feature X"
        assert project.spec == "A project that does X for Y users."
        assert project.project_context == "## Repos\n- repo-a\n- repo-b"
        assert "important" in project.tags
        assert "q1" in project.tags
        assert project.ticket_creation_config == {
            "board_id": "board-123",
            "labels": ["bug"],
        }

    def test_get_repositories_by_layer(self):
        """Test filtering repositories by layer"""
        project = Project(
            id=str(uuid4()),
            organization_id="org-123",
            alias="TEST",
            name="Test Project",
            description="Test",
        )

        # Add mock repositories
        ui_repo = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id="repo-1",
            layer=RepositoryLayer.UI,
        )
        api_repo = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id="repo-2",
            layer=RepositoryLayer.API,
        )
        data_repo = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id="repo-3",
            layer=RepositoryLayer.DATA,
        )

        project.repositories = [ui_repo, api_repo, data_repo]

        ui_repos = project.get_repositories_by_layer(RepositoryLayer.UI)
        assert len(ui_repos) == 1
        assert ui_repos[0].layer == RepositoryLayer.UI

        api_repos = project.get_repositories_by_layer(RepositoryLayer.API)
        assert len(api_repos) == 1
        assert api_repos[0].layer == RepositoryLayer.API

        legacy_repos = project.get_repositories_by_layer(RepositoryLayer.LEGACY)
        assert len(legacy_repos) == 0

    def test_get_primary_repository(self):
        """Test getting the primary repository"""
        project = Project(
            id=str(uuid4()),
            organization_id="org-123",
            alias="TEST",
            name="Test Project",
            description="Test",
        )

        # Add repositories with one primary
        repo1 = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id="repo-1",
            layer=RepositoryLayer.UI,
            is_primary=False,
        )
        repo2 = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id="repo-2",
            layer=RepositoryLayer.API,
            is_primary=True,
        )

        project.repositories = [repo1, repo2]

        primary = project.get_primary_repository()
        assert primary is not None
        assert primary.is_primary is True
        assert primary.repository_id == "repo-2"

    def test_get_primary_repository_none(self):
        """Test getting primary repository when none exists"""
        project = Project(
            id=str(uuid4()),
            organization_id="org-123",
            alias="TEST",
            name="Test Project",
            description="Test",
        )

        repo = ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id="repo-1",
            layer=RepositoryLayer.UI,
            is_primary=False,
        )

        project.repositories = [repo]

        primary = project.get_primary_repository()
        assert primary is None


class TestProjectRepository:
    """Test ProjectRepository junction model"""

    def test_create_project_repository(self):
        """Test creating a project-repository link"""
        pr = ProjectRepository(
            id=str(uuid4()),
            project_id="project-123",
            repository_id="repo-456",
            layer=RepositoryLayer.API,
            is_primary=False,
            purpose="Backend API service",
        )

        assert pr.project_id == "project-123"
        assert pr.repository_id == "repo-456"
        assert pr.layer == RepositoryLayer.API
        assert pr.is_primary is False
        assert pr.purpose == "Backend API service"

    def test_repository_layers(self):
        """Test all repository layer values"""
        layers = [
            RepositoryLayer.UI,
            RepositoryLayer.API,
            RepositoryLayer.DATA,
            RepositoryLayer.AI,
            RepositoryLayer.LEGACY,
            RepositoryLayer.UNASSIGNED,
        ]

        for layer in layers:
            pr = ProjectRepository(
                id=str(uuid4()),
                project_id="project-123",
                repository_id="repo-456",
                layer=layer,
            )
            assert pr.layer == layer

    def test_default_values(self):
        """Test default values for ProjectRepository"""
        pr = ProjectRepository(
            id=str(uuid4()),
            project_id="project-123",
            repository_id="repo-456",
        )

        assert pr.layer == RepositoryLayer.UNASSIGNED
        assert pr.is_primary is False
        assert pr.purpose is None


class TestProjectService:
    """Test ProjectService business logic"""

    @pytest.mark.asyncio
    async def test_create_project(self, memory_session):
        """Test creating a project via service"""
        service = ProjectService(memory_session)

        project = await service.create_project(
            organization_id="org-123",
            alias="NEW",
            name="New Project",
            description="Test project creation",
            goals="Test goals",
            spec="A one-paragraph project spec.",
            project_context="## Repos\n- repo-a",
            priority=ProjectPriority.HIGH,
            status=ProjectStatus.ACTIVE,
            tags=["test", "new"],
        )

        assert project.name == "New Project"
        assert project.organization_id == "org-123"
        assert project.alias == "NEW"
        assert project.priority == ProjectPriority.HIGH
        assert project.status == ProjectStatus.ACTIVE
        assert "test" in project.tags
        assert project.spec == "A one-paragraph project spec."
        assert project.project_context == "## Repos\n- repo-a"

    @pytest.mark.asyncio
    async def test_create_project_without_spec_defaults_to_none(self, memory_session):
        """Test that spec and project_context default to None when omitted"""
        service = ProjectService(memory_session)

        project = await service.create_project(
            organization_id="org-123",
            alias="NOSPEC",
            name="No Spec Project",
            description="Test project creation without spec",
        )

        assert project.spec is None
        assert project.project_context is None

    @pytest.mark.asyncio
    async def test_duplicate_alias_in_org_raises(self, memory_session):
        """Alias must be unique per-organization; a collision raises ValueError.

        (Replaces the old slug auto-suffixing test -- slug generation was
        removed; alias is now the required, per-org-unique identifier and
        _normalize_alias raises on collision instead of appending -1/-2.)
        """
        service = ProjectService(memory_session)

        # Create first project with alias "DUP"
        await service.create_project(
            organization_id="org-123",
            alias="DUP",
            name="Test Project",
            description="First project",
        )

        # Second project in the SAME org with the same alias must raise
        with pytest.raises(ValueError, match="already used"):
            await service.create_project(
                organization_id="org-123",
                alias="DUP",
                name="Another Project",
                description="Second project",
            )

        # Same alias in a DIFFERENT org is allowed (per-org uniqueness)
        other = await service.create_project(
            organization_id="org-456",
            alias="DUP",
            name="Other Org Project",
            description="Different org, same alias",
        )
        assert other.alias == "DUP"

    @pytest.mark.asyncio
    async def test_update_project(self, memory_session):
        """Test updating project fields"""
        service = ProjectService(memory_session)

        # Create project
        project = await service.create_project(
            organization_id="org-123",
            alias="ORIG",
            name="Original Name",
            description="Original description",
            priority=ProjectPriority.LOW,
        )

        # Update project
        updated = await service.update_project(
            project_id=project.id,
            name="Updated Name",
            description="Updated description",
            priority=ProjectPriority.HIGH,
            tags=["updated"],
        )

        assert updated.name == "Updated Name"
        assert updated.description == "Updated description"
        assert updated.priority == ProjectPriority.HIGH
        assert "updated" in updated.tags

    @pytest.mark.asyncio
    async def test_update_project_spec_and_project_context(self, memory_session):
        """Test updating only spec doesn't clobber project_context, and vice versa"""
        service = ProjectService(memory_session)

        project = await service.create_project(
            organization_id="org-123",
            alias="SPEC",
            name="Spec Project",
            description="Original description",
        )

        updated = await service.update_project(
            project_id=project.id,
            spec="Updated spec paragraph.",
        )
        assert updated.spec == "Updated spec paragraph."
        assert updated.project_context is None

        updated = await service.update_project(
            project_id=project.id,
            project_context="## Repos\n- repo-a",
        )
        assert updated.spec == "Updated spec paragraph."
        assert updated.project_context == "## Repos\n- repo-a"

    @pytest.mark.asyncio
    async def test_update_project_persists_ticket_creation_config(self, memory_session):
        """Regression test: ticket_creation_config must be in allowed_fields"""
        service = ProjectService(memory_session)

        project = await service.create_project(
            organization_id="org-123",
            alias="CONFIG",
            name="Config Project",
            description="Has ticket creation config",
        )

        config = {"board_id": "board-abc", "labels": ["bug"], "issue_type": "Task"}
        updated = await service.update_project(
            project_id=project.id,
            ticket_creation_config=config,
        )

        assert updated.ticket_creation_config == config

    @pytest.mark.asyncio
    async def test_delete_project_archives(self, memory_session):
        """Test that delete actually archives the project"""
        service = ProjectService(memory_session)

        # Create project
        project = await service.create_project(
            organization_id="org-123",
            alias="ARCH",
            name="To Archive",
            description="Will be archived",
            status=ProjectStatus.ACTIVE,
        )

        # Delete (archive) project
        await service.delete_project(project.id)

        # Check it's archived
        memory_session.refresh(project)
        assert project.status == ProjectStatus.ARCHIVED

    @pytest.mark.asyncio
    async def test_archived_project_still_holds_its_alias(self, memory_session):
        """Archiving keeps the alias, and the error points at reactivation.

        The uniqueness constraint (uq_project_org_alias) is unconditional, so
        an archived project keeps blocking its alias. The holder is often a
        project the caller was just told was "deleted", so the message has to
        name it AND give the one-step way forward -- reactivating is nearly
        always what they want, since creating under a different alias abandons
        the archived project's tickets, boards and repos.
        """
        service = ProjectService(memory_session)

        project = await service.create_project(
            organization_id="org-123",
            alias="HELD",
            name="To Archive",
            description="Will be archived, then its alias reused",
            status=ProjectStatus.ACTIVE,
        )
        await service.delete_project(project.id)

        with pytest.raises(ValueError, match="held by archived project") as exc:
            await service.create_project(
                organization_id="org-123",
                alias="HELD",
                name="Reuse Attempt",
                description="Same alias as the archived project",
            )

        # The message must identify the blocker and hand over a runnable
        # remedy -- not just explain that the alias is taken.
        message = str(exc.value)
        assert project.id in message
        assert f"--project-id {project.id} --status active" in message

        # A different alias in the same org is unaffected.
        fresh = await service.create_project(
            organization_id="org-123",
            alias="HELD2",
            name="Different Alias",
            description="Not blocked",
        )
        assert fresh.alias == "HELD2"

    @pytest.mark.asyncio
    async def test_list_projects_with_filters(self, memory_session):
        """Test listing projects with various filters"""
        service = ProjectService(memory_session)

        # Create multiple projects
        await service.create_project(
            organization_id="org-123",
            alias="HIGH",
            name="High Priority",
            description="Test",
            priority=ProjectPriority.HIGH,
            status=ProjectStatus.ACTIVE,
            tags=["urgent"],
        )

        await service.create_project(
            organization_id="org-123",
            alias="LOW",
            name="Low Priority",
            description="Test",
            priority=ProjectPriority.LOW,
            status=ProjectStatus.PLANNING,
            tags=["backlog"],
        )

        await service.create_project(
            organization_id="org-456",
            alias="OTHER",
            name="Other Org",
            description="Test",
        )

        # Test filtering by organization
        org_projects = await service.list_projects(organization_id="org-123")
        assert len(org_projects) == 2

        # Test filtering by priority
        high_priority = await service.list_projects(
            organization_id="org-123",
            priority=ProjectPriority.HIGH,
        )
        assert len(high_priority) == 1
        assert high_priority[0].name == "High Priority"

        # Test filtering by status
        planning = await service.list_projects(
            organization_id="org-123",
            status=ProjectStatus.PLANNING,
        )
        assert len(planning) == 1
        assert planning[0].name == "Low Priority"

        # Test filtering by tags
        urgent = await service.list_projects(
            organization_id="org-123",
            tags=["urgent"],
        )
        assert len(urgent) == 1
        assert urgent[0].name == "High Priority"

    def test_parse_github_url(self):
        """Test parsing GitHub repository URLs"""
        service = ProjectService(Mock())

        # Test standard HTTPS URL
        result = service._parse_github_url("https://github.com/owner/repo")
        assert result["owner"] == "owner"
        assert result["name"] == "repo"
        assert result["full_name"] == "owner/repo"

        # Test with .git extension
        result = service._parse_github_url("https://github.com/owner/repo.git")
        assert result["owner"] == "owner"
        assert result["name"] == "repo"
        assert result["full_name"] == "owner/repo"

        # Test SSH URL
        result = service._parse_github_url("git@github.com:owner/repo.git")
        assert result["owner"] == "owner"
        assert result["name"] == "repo"
        assert result["full_name"] == "owner/repo"

        # Test invalid URL
        with pytest.raises(ValueError, match="Invalid GitHub URL"):
            service._parse_github_url("https://example.com/not/github")


class TestProjectStatusAndPriority:
    """Test Project enums"""

    def test_project_status_values(self):
        """Test all ProjectStatus values"""
        assert ProjectStatus.PLANNING.value == "planning"
        assert ProjectStatus.ACTIVE.value == "active"
        assert ProjectStatus.ARCHIVED.value == "archived"

    def test_project_priority_values(self):
        """Test all ProjectPriority values"""
        assert ProjectPriority.HIGH.value == "high"
        assert ProjectPriority.MEDIUM.value == "medium"
        assert ProjectPriority.LOW.value == "low"

    def test_repository_layer_values(self):
        """Test all RepositoryLayer values"""
        assert RepositoryLayer.UI.value == "ui"
        assert RepositoryLayer.API.value == "api"
        assert RepositoryLayer.DATA.value == "data"
        assert RepositoryLayer.AI.value == "ai"
        assert RepositoryLayer.LEGACY.value == "legacy"
        assert RepositoryLayer.UNASSIGNED.value == "unassigned"
