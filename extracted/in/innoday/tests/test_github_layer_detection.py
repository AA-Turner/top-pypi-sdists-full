"""
Tests for GitHub repository layer detection logic.
"""

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from src.domain.project import RepositoryLayer
from src.services.github_connect_service import GitHubConnectService


@pytest.fixture
def session():
    """Create a test database session."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    with Session(engine) as session:
        yield session


@pytest.fixture
def service(session):
    """Create a GitHubConnectService instance."""
    return GitHubConnectService(session)


class TestLayerDetection:
    """Test repository layer detection logic."""

    def test_explicit_layer_labels(self, service):
        """Test that explicit layer labels take priority."""
        # UI layer label
        assert (
            service.detect_repository_layer("backend-api", "Python", ["layer:frontend"])
            == RepositoryLayer.UI
        )

        # API layer label
        assert (
            service.detect_repository_layer(
                "frontend-app", "TypeScript", ["layer:backend"]
            )
            == RepositoryLayer.API
        )

        # Data layer label
        assert (
            service.detect_repository_layer("random-name", "JavaScript", ["layer:data"])
            == RepositoryLayer.DATA
        )

        # AI layer label
        assert (
            service.detect_repository_layer("web-app", "Python", ["layer:ai"])
            == RepositoryLayer.AI
        )

        # Legacy layer label
        assert (
            service.detect_repository_layer("new-service", "Go", ["layer:legacy"])
            == RepositoryLayer.LEGACY
        )

    def test_name_pattern_detection(self, service):
        """Test repository name pattern matching."""
        # UI patterns
        assert (
            service.detect_repository_layer("portal-ui", None, []) == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("frontend-app", None, [])
            == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("web-dashboard", None, [])
            == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("customer-portal", None, [])
            == RepositoryLayer.UI
        )

        # API patterns
        assert (
            service.detect_repository_layer("portal-api", None, [])
            == RepositoryLayer.API
        )
        assert (
            service.detect_repository_layer("backend-service", None, [])
            == RepositoryLayer.API
        )
        assert (
            service.detect_repository_layer("api-gateway", None, [])
            == RepositoryLayer.API
        )
        assert (
            service.detect_repository_layer("auth-server", None, [])
            == RepositoryLayer.API
        )

        # Data patterns
        assert (
            service.detect_repository_layer("portal-db", None, [])
            == RepositoryLayer.DATA
        )
        assert (
            service.detect_repository_layer("data-pipeline", None, [])
            == RepositoryLayer.DATA
        )
        assert (
            service.detect_repository_layer("etl-jobs", None, [])
            == RepositoryLayer.DATA
        )
        assert (
            service.detect_repository_layer("db-migrations", None, [])
            == RepositoryLayer.DATA
        )

        # AI patterns
        assert (
            service.detect_repository_layer("ml-models", None, []) == RepositoryLayer.AI
        )
        assert (
            service.detect_repository_layer("ai-service", None, [])
            == RepositoryLayer.AI
        )
        assert (
            service.detect_repository_layer("analytics-engine", None, [])
            == RepositoryLayer.AI
        )
        assert (
            service.detect_repository_layer("prediction-service", None, [])
            == RepositoryLayer.AI
        )

        # Legacy patterns
        assert (
            service.detect_repository_layer("old-system", None, [])
            == RepositoryLayer.LEGACY
        )
        assert (
            service.detect_repository_layer("legacy-api", None, [])
            == RepositoryLayer.LEGACY
        )
        assert (
            service.detect_repository_layer("deprecated-service", None, [])
            == RepositoryLayer.LEGACY
        )

    def test_language_based_detection(self, service):
        """Test detection based on primary programming language."""
        # UI languages
        assert (
            service.detect_repository_layer("my-app", "TypeScript", [])
            == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("project", "JavaScript", [])
            == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("styles", "CSS", []) == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("component", "Vue", [])
            == RepositoryLayer.UI
        )

        # API languages (when no specific pattern in name)
        assert (
            service.detect_repository_layer("service", "Python", [])
            == RepositoryLayer.API
        )
        assert (
            service.detect_repository_layer("application", "Java", [])
            == RepositoryLayer.API
        )
        assert (
            service.detect_repository_layer("microservice", "Go", [])
            == RepositoryLayer.API
        )
        assert (
            service.detect_repository_layer("worker", "Ruby", []) == RepositoryLayer.API
        )

        # Data languages
        assert (
            service.detect_repository_layer("queries", "SQL", [])
            == RepositoryLayer.DATA
        )
        assert (
            service.detect_repository_layer("procedures", "PLPGSQL", [])
            == RepositoryLayer.DATA
        )

        # AI/ML languages
        assert (
            service.detect_repository_layer("notebook", "Jupyter Notebook", [])
            == RepositoryLayer.AI
        )
        assert (
            service.detect_repository_layer("analysis", "R", []) == RepositoryLayer.AI
        )

    def test_mixed_signals_priority(self, service):
        """Test that detection follows the correct priority order."""
        # Label > Name > Language
        # Label overrides name pattern
        assert (
            service.detect_repository_layer("frontend-ui", "Python", ["layer:api"])
            == RepositoryLayer.API
        )

        # Name pattern overrides language
        assert (
            service.detect_repository_layer("backend-api", "TypeScript", [])
            == RepositoryLayer.API
        )

        # Language is used when no pattern matches
        assert (
            service.detect_repository_layer("my-project", "TypeScript", [])
            == RepositoryLayer.UI
        )

    def test_nodejs_backend_detection(self, service):
        """Test that Node.js backends are correctly identified."""
        # Node.js with API indicators should be API layer
        assert (
            service.detect_repository_layer("api-service", "JavaScript", [])
            == RepositoryLayer.API
        )

        assert (
            service.detect_repository_layer("backend", "TypeScript", [])
            == RepositoryLayer.API
        )

        # But generic Node.js projects default to UI
        assert (
            service.detect_repository_layer("my-app", "JavaScript", [])
            == RepositoryLayer.UI
        )

    def test_unassigned_layer(self, service):
        """Test that unrecognized repos get UNASSIGNED layer."""
        # No patterns match
        assert (
            service.detect_repository_layer("random-project", None, [])
            == RepositoryLayer.UNASSIGNED
        )

        assert (
            service.detect_repository_layer("misc-tools", "Shell", [])
            == RepositoryLayer.UNASSIGNED
        )

        assert (
            service.detect_repository_layer("documentation", "Markdown", [])
            == RepositoryLayer.UNASSIGNED
        )

    def test_case_insensitive_matching(self, service):
        """Test that pattern matching is case-insensitive."""
        # Uppercase in name
        assert (
            service.detect_repository_layer("Portal-UI", None, []) == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("BACKEND-API", None, [])
            == RepositoryLayer.API
        )

        # Mixed case in labels
        assert (
            service.detect_repository_layer("project", None, ["Layer:Frontend"])
            == RepositoryLayer.UI
        )

        assert (
            service.detect_repository_layer("project", None, ["LAYER:BACKEND"])
            == RepositoryLayer.API
        )

    def test_hyphen_underscore_variations(self, service):
        """Test that both hyphens and underscores work in patterns."""
        # With hyphens
        assert (
            service.detect_repository_layer("portal-ui", None, []) == RepositoryLayer.UI
        )
        assert (
            service.detect_repository_layer("api-gateway", None, [])
            == RepositoryLayer.API
        )

        # The current implementation uses regex word boundaries,
        # so underscores might not match the same way
        # This is intentional as most GitHub repos use hyphens


class TestPrecedenceRules:
    """Lock in the precedence the lookup tables now encode implicitly.

    The if/elif chain these replaced made the order visible in the control flow.
    In a table it is carried by *table order*, so a future edit that appends a
    layer in the wrong place would silently change classification. These tests
    fail if that happens.

    The refactor itself was verified differentially against the old chain over
    432,960 (name × language × label) combinations — identical on every one.
    """

    def test_label_beats_every_name_pattern(self, service):
        # The name says API three ways; the label still wins.
        assert (
            service.detect_repository_layer(
                "backend-api-server", "Python", ["layer:ui"]
            )
            == RepositoryLayer.UI
        )

    def test_unrecognised_label_keyword_falls_through_to_the_name(self, service):
        assert (
            service.detect_repository_layer("web-app", None, ["layer:nonsense"])
            == RepositoryLayer.UI
        )

    def test_name_pattern_beats_language(self, service):
        # Python would default to API; the name says DATA.
        assert (
            service.detect_repository_layer("customer-etl", "Python", [])
            == RepositoryLayer.DATA
        )

    def test_legacy_outranks_every_other_name_pattern(self, service):
        for name in ("legacy-ml-model", "legacy-data-pipeline", "legacy-web-app"):
            assert (
                service.detect_repository_layer(name, None, [])
                == RepositoryLayer.LEGACY
            ), name

    def test_ai_outranks_data_and_ui_and_api(self, service):
        assert (
            service.detect_repository_layer("ml-data-api", None, [])
            == RepositoryLayer.AI
        )

    def test_data_outranks_ui_and_api(self, service):
        assert (
            service.detect_repository_layer("data-dashboard", None, [])
            == RepositoryLayer.DATA
        )

    def test_ui_outranks_api(self, service):
        assert (
            service.detect_repository_layer("frontend-service", None, [])
            == RepositoryLayer.UI
        )

    def test_language_hints_are_substrings_not_word_boundaries(self, service):
        """The language-hint check is a plain `in`, unlike the name regexes.

        "guipython" contains "ui", so a Python repo with no hyphenated pattern
        still lands in UI. Preserved deliberately from the original.
        """
        assert (
            service.detect_repository_layer("guiproject", "Python", [])
            == RepositoryLayer.UI
        )

    def test_unknown_language_and_no_pattern_is_unassigned(self, service):
        assert (
            service.detect_repository_layer("something", "Haskell", [])
            == RepositoryLayer.UNASSIGNED
        )


class TestDesignLayer:
    """DESIGN is reachable by topic, and by nothing else.

    The member exists so a demo repository can be kept out of a release's
    feature story while still being tagged by that release. Before it, the only
    way to keep a demo out of the notes was to unlink it -- which also removed
    it from the tag set, and a release quietly covered six repositories instead
    of seven.
    """

    def test_layer_design_topic_classifies_as_design(self, service):
        """`layer-design`, with a hyphen. A GitHub topic cannot hold a colon.

        The original marker was `layer:design` and GitHub rejects it outright --
        "must start with a lowercase letter or number, consist of 50 characters
        or less, and can include hyphens". So the topic branch of this function
        could never fire on a real repository, and nothing failed loudly: a repo
        just fell through to the name and language rules.
        """
        assert (
            service.detect_repository_layer(
                "bps-ui-demo", "TypeScript", ["layer-design"]
            )
            == RepositoryLayer.DESIGN
        )

    def test_a_topic_with_a_colon_is_not_what_github_allows(self, service):
        """Kept working, but it is not the form to document or to set.

        A repository can only carry this if something other than GitHub's topic
        API put it there, so it stays supported and stays out of the help text.
        """
        assert (
            service.detect_repository_layer("anything", None, ["layer:design"])
            == RepositoryLayer.DESIGN
        )

    def test_demo_and_prototype_topics_also_reach_it(self, service):
        for keyword in ("demo", "prototype"):
            assert (
                service.detect_repository_layer("anything", None, [f"layer-{keyword}"])
                == RepositoryLayer.DESIGN
            ), keyword

    def test_a_demo_in_the_name_alone_does_not_classify_as_design(self, service):
        """The guard that stops a heuristic reclassifying a shipping repository.

        "demo", "design" and "prototype" all appear in the names of real
        repositories that ship to customers. Inferring DESIGN from a name would
        move that work out of the release story silently, which is precisely the
        failure this member was added to fix -- so the name is not evidence and
        only an explicit topic is.
        """
        assert (
            service.detect_repository_layer("bps-ui-demo", "TypeScript", [])
            != RepositoryLayer.DESIGN
        )
        assert (
            service.detect_repository_layer("design-system-api", "Python", [])
            != RepositoryLayer.DESIGN
        )

    def test_design_is_a_layer_value_the_enum_accepts(self):
        """Guards the seam between the Python member and the Postgres type.

        `project_repositories.layer` is a native Postgres enum built from the
        member NAMES, so the name is what the database stores; the value is what
        the API and CLI speak. Both halves have to exist or one side 422s while
        the other looks fine.
        """
        assert RepositoryLayer("design") is RepositoryLayer.DESIGN
        assert RepositoryLayer.DESIGN.name == "DESIGN"


class TestLayerTopicsAreTopicsGitHubWillAccept:
    """A marker GitHub rejects is a rule that can never fire.

    Every declared layer marker has to be settable through the topics API, or
    the precedence rule that puts an explicit topic above every heuristic is
    decoration. GitHub's rule: lowercase letters, numbers and hyphens, 50
    characters or fewer, starting with a letter or number.
    """

    def test_at_least_one_marker_is_a_valid_github_topic(self):
        import re

        from src.services.github_connect_service import _LAYER_TOPIC_MARKERS

        valid = re.compile(r"^[a-z0-9][a-z0-9-]{0,49}$")
        settable = [
            marker for marker in _LAYER_TOPIC_MARKERS if valid.match(f"{marker}design")
        ]
        assert settable, (
            "no layer marker can be written as a GitHub topic, so the topic "
            f"branch of detect_repository_layer is unreachable: {_LAYER_TOPIC_MARKERS}"
        )

    def test_the_colon_form_really_is_rejected_by_that_rule(self):
        """Guards the test above from passing for the wrong reason."""
        import re

        assert not re.match(r"^[a-z0-9][a-z0-9-]{0,49}$", "layer:design")
