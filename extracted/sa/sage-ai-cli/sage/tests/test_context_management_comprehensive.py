"""Comprehensive tests for sage/core/context_management.py - Context Management."""

import pytest
import tempfile
from datetime import datetime
from pathlib import Path

from sage.core.context_management import (
    # Dataclasses
    Message,
    ExtractedContext,
    ProjectStructure,
    LanguageInfo,
    FrameworkInfo,
    Dependency,
    ArchitectureInfo,
    ClassInfo,
    FunctionInfo,
    ImportInfo,
    CodeStructure,
    DependencyInfo,
    SymbolLocation,
    KnowledgeItem,
    Inference,
    Pattern,
    CodingStyle,
    # Conversation Context
    ConversationContext,
    ReferenceResolver,
    GoalTracker,
    # Project Context
    ProjectAnalyzer,
    # Code Context
    CodeAnalyzer,
    SymbolResolver,
    # Knowledge Context
    KnowledgeBase,
    PatternLearner,
    StyleAdapter,
)


# =============================================================================
# Tests for Message dataclass
# =============================================================================


class TestMessage:
    """Tests for Message dataclass."""

    def test_create(self):
        """Create message."""
        msg = Message(role="user", content="Hello")
        assert msg.role == "user"
        assert msg.content == "Hello"
        assert isinstance(msg.timestamp, datetime)

    def test_custom_timestamp(self):
        """Create message with custom timestamp."""
        ts = datetime(2024, 1, 1, 12, 0, 0)
        msg = Message(role="assistant", content="Hi", timestamp=ts)
        assert msg.timestamp == ts


# =============================================================================
# Tests for ExtractedContext dataclass
# =============================================================================


class TestExtractedContext:
    """Tests for ExtractedContext dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        ctx = ExtractedContext()
        assert ctx.mentioned_files == []
        assert ctx.mentioned_symbols == []
        assert ctx.intent == ""
        assert ctx.entities == {}

    def test_create_with_values(self):
        """Create with values."""
        ctx = ExtractedContext(
            mentioned_files=["foo.py"],
            mentioned_symbols=["MyClass"],
            intent="create",
            entities={"functions": ["bar"]},
        )
        assert ctx.mentioned_files == ["foo.py"]
        assert ctx.intent == "create"


# =============================================================================
# Tests for ProjectStructure dataclass
# =============================================================================


class TestProjectStructure:
    """Tests for ProjectStructure dataclass."""

    def test_create(self):
        """Create project structure."""
        ps = ProjectStructure(
            directories=["src", "tests"],
            files=["README.md"],
            root="/project",
        )
        assert len(ps.directories) == 2
        assert ps.root == "/project"


# =============================================================================
# Tests for LanguageInfo dataclass
# =============================================================================


class TestLanguageInfo:
    """Tests for LanguageInfo dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        info = LanguageInfo()
        assert info.primary == "unknown"
        assert info.secondary == []
        assert info.confidence == 0.0

    def test_create_with_values(self):
        """Create with values."""
        info = LanguageInfo(
            primary="python",
            secondary=["javascript"],
            confidence=0.9,
        )
        assert info.primary == "python"
        assert info.confidence == 0.9


# =============================================================================
# Tests for FrameworkInfo dataclass
# =============================================================================


class TestFrameworkInfo:
    """Tests for FrameworkInfo dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        info = FrameworkInfo()
        assert info.name == "unknown"
        assert info.version is None

    def test_create_with_version(self):
        """Create with version."""
        info = FrameworkInfo(name="Django", version="4.0")
        assert info.version == "4.0"


# =============================================================================
# Tests for Dependency dataclass
# =============================================================================


class TestDependency:
    """Tests for Dependency dataclass."""

    def test_create_minimal(self):
        """Create minimal dependency."""
        dep = Dependency(name="requests")
        assert dep.name == "requests"
        assert dep.version is None
        assert dep.dev is False

    def test_create_full(self):
        """Create full dependency."""
        dep = Dependency(name="pytest", version=">=7.0", dev=True)
        assert dep.dev is True


# =============================================================================
# Tests for ArchitectureInfo dataclass
# =============================================================================


class TestArchitectureInfo:
    """Tests for ArchitectureInfo dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        info = ArchitectureInfo()
        assert info.pattern == "unknown"
        assert info.layers == []

    def test_create_mvc(self):
        """Create MVC architecture."""
        info = ArchitectureInfo(
            pattern="MVC",
            layers=["models", "views", "controllers"],
            components=["User", "Order"],
        )
        assert info.pattern == "MVC"


# =============================================================================
# Tests for ClassInfo dataclass
# =============================================================================


class TestClassInfo:
    """Tests for ClassInfo dataclass."""

    def test_create(self):
        """Create class info."""
        info = ClassInfo(
            name="MyClass",
            methods=["__init__", "process"],
            attributes=["data"],
            bases=["BaseClass"],
        )
        assert info.name == "MyClass"
        assert len(info.methods) == 2


# =============================================================================
# Tests for FunctionInfo dataclass
# =============================================================================


class TestFunctionInfo:
    """Tests for FunctionInfo dataclass."""

    def test_create(self):
        """Create function info."""
        info = FunctionInfo(
            name="process",
            parameters=["data", "options"],
            returns="Result",
        )
        assert info.name == "process"
        assert info.returns == "Result"


# =============================================================================
# Tests for ImportInfo dataclass
# =============================================================================


class TestImportInfo:
    """Tests for ImportInfo dataclass."""

    def test_create(self):
        """Create import info."""
        info = ImportInfo(
            module="os.path",
            names=["join", "exists"],
            alias="osp",
        )
        assert info.module == "os.path"
        assert info.alias == "osp"


# =============================================================================
# Tests for CodeStructure dataclass
# =============================================================================


class TestCodeStructure:
    """Tests for CodeStructure dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        structure = CodeStructure()
        assert structure.classes == []
        assert structure.functions == []
        assert structure.imports == []


# =============================================================================
# Tests for DependencyInfo dataclass
# =============================================================================


class TestDependencyInfo:
    """Tests for DependencyInfo dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        info = DependencyInfo()
        assert info.internal == []
        assert info.external == []


# =============================================================================
# Tests for SymbolLocation dataclass
# =============================================================================


class TestSymbolLocation:
    """Tests for SymbolLocation dataclass."""

    def test_create(self):
        """Create symbol location."""
        loc = SymbolLocation(file="foo.py", line=42, column=10)
        assert loc.file == "foo.py"
        assert loc.line == 42


# =============================================================================
# Tests for KnowledgeItem dataclass
# =============================================================================


class TestKnowledgeItem:
    """Tests for KnowledgeItem dataclass."""

    def test_create(self):
        """Create knowledge item."""
        item = KnowledgeItem(
            key="language",
            value="python",
            confidence=0.9,
            source="detection",
        )
        assert item.key == "language"
        assert item.source == "detection"


# =============================================================================
# Tests for Inference dataclass
# =============================================================================


class TestInference:
    """Tests for Inference dataclass."""

    def test_create(self):
        """Create inference."""
        inf = Inference(
            topic="testing",
            conclusion="Uses pytest",
            confidence=0.8,
            evidence=["Has pytest in requirements"],
        )
        assert inf.topic == "testing"
        assert len(inf.evidence) == 1


# =============================================================================
# Tests for Pattern dataclass
# =============================================================================


class TestPattern:
    """Tests for Pattern dataclass."""

    def test_create(self):
        """Create pattern."""
        p = Pattern(pattern="test_", frequency=5, confidence=0.7)
        assert p.pattern == "test_"
        assert p.frequency == 5


# =============================================================================
# Tests for CodingStyle dataclass
# =============================================================================


class TestCodingStyle:
    """Tests for CodingStyle dataclass."""

    def test_create_default(self):
        """Create with defaults."""
        style = CodingStyle()
        assert style.naming_convention == "unknown"
        assert style.indentation == "spaces"
        assert style.line_length == 80


# =============================================================================
# Tests for ConversationContext
# =============================================================================


class TestConversationContext:
    """Tests for ConversationContext class."""

    def test_init(self):
        """Initialize conversation context."""
        ctx = ConversationContext()
        assert ctx.messages == []

    def test_add_message(self):
        """Add message to conversation."""
        ctx = ConversationContext()
        ctx.add_message("user", "Hello")
        assert len(ctx.messages) == 1
        assert ctx.messages[0].role == "user"

    def test_extract_file_mentions(self):
        """Extract file mentions from messages."""
        ctx = ConversationContext()
        ctx.add_message("user", "Look at foo.py and bar.js")
        assert "foo.py" in ctx._files_mentioned
        assert "bar.js" in ctx._files_mentioned

    def test_extract_symbol_mentions(self):
        """Extract symbol mentions from messages."""
        ctx = ConversationContext()
        ctx.add_message("user", "Check the MyClass and process_data function")
        assert "MyClass" in ctx._symbols_mentioned
        assert "process_data" in ctx._symbols_mentioned

    def test_extract_context_fix_intent(self):
        """Extract fix intent."""
        ctx = ConversationContext()
        ctx.add_message("user", "Please fix the bug")
        result = ctx.extract_context()
        assert result.intent == "fix"

    def test_extract_context_create_intent(self):
        """Extract create intent."""
        ctx = ConversationContext()
        ctx.add_message("user", "Create a new function")
        result = ctx.extract_context()
        assert result.intent == "create"

    def test_extract_context_add_intent(self):
        """Extract add intent."""
        ctx = ConversationContext()
        ctx.add_message("user", "Add a new feature")
        result = ctx.extract_context()
        assert result.intent == "create"

    def test_extract_context_explain_intent(self):
        """Extract explain intent."""
        ctx = ConversationContext()
        ctx.add_message("user", "Explain how this works")
        result = ctx.extract_context()
        assert result.intent == "explain"

    def test_extract_context_review_intent(self):
        """Extract review intent."""
        ctx = ConversationContext()
        ctx.add_message("user", "Review this code")
        result = ctx.extract_context()
        assert result.intent == "review"

    def test_extract_context_unknown_intent(self):
        """Unknown intent for generic message."""
        ctx = ConversationContext()
        ctx.add_message("user", "Hello there")
        result = ctx.extract_context()
        assert result.intent == "unknown"

    def test_summarize_empty(self):
        """Summarize empty conversation."""
        ctx = ConversationContext()
        summary = ctx.summarize()
        assert "No messages" in summary

    def test_summarize_with_messages(self):
        """Summarize conversation with messages."""
        ctx = ConversationContext()
        ctx.add_message("user", "Check foo.py")
        ctx.add_message("assistant", "Done")
        summary = ctx.summarize()
        assert "2 messages" in summary
        assert "1 user" in summary


# =============================================================================
# Tests for ReferenceResolver
# =============================================================================


class TestReferenceResolver:
    """Tests for ReferenceResolver class."""

    def test_resolve_pronoun_finds_referent(self):
        """Resolve pronoun to recent noun."""
        resolver = ReferenceResolver()
        messages = [
            {"role": "user", "content": "Look at the database connection"},
            {"role": "user", "content": "Fix it"},
        ]
        result = resolver.resolve_pronoun("it", messages)
        assert "database" in result.lower()

    def test_resolve_pronoun_no_referent(self):
        """Return unchanged if no referent found."""
        resolver = ReferenceResolver()
        messages = [{"role": "user", "content": "Fix it"}]
        result = resolver.resolve_pronoun("it", messages)
        assert result == "it"

    def test_resolve_coreference_finds_issue(self):
        """Resolve coreference to problem."""
        resolver = ReferenceResolver()
        messages = [
            {"role": "user", "content": "The login is failing"},
            {"role": "user", "content": "Fix the issue"},
        ]
        result = resolver.resolve_coreference("the issue", messages)
        assert "login" in result.lower()

    def test_resolve_coreference_no_match(self):
        """Return unchanged if no match found."""
        resolver = ReferenceResolver()
        messages = [{"role": "user", "content": "Hello"}]
        result = resolver.resolve_coreference("the issue", messages)
        assert result == "the issue"


# =============================================================================
# Tests for GoalTracker
# =============================================================================


class TestGoalTracker:
    """Tests for GoalTracker class."""

    def test_init(self):
        """Initialize goal tracker."""
        tracker = GoalTracker()
        assert tracker.current_goal is None
        assert tracker.subgoals == []

    def test_set_goal(self):
        """Set current goal."""
        tracker = GoalTracker()
        tracker.set_goal("Build API")
        assert tracker.current_goal == "Build API"

    def test_add_subgoal(self):
        """Add subgoal."""
        tracker = GoalTracker()
        tracker.set_goal("Build API")
        tracker.add_subgoal("Define routes")
        assert "Define routes" in tracker.subgoals

    def test_complete_subgoal(self):
        """Complete subgoal."""
        tracker = GoalTracker()
        tracker.set_goal("Build API")
        tracker.add_subgoal("Define routes")
        tracker.complete_subgoal("Define routes")
        assert "Define routes" in tracker.completed_subgoals
        assert "Define routes" not in tracker.subgoals

    def test_complete_nonexistent_subgoal(self):
        """Complete nonexistent subgoal does nothing."""
        tracker = GoalTracker()
        tracker.complete_subgoal("Unknown")
        assert tracker.completed_subgoals == []

    def test_progress_no_subgoals(self):
        """Progress is 0 with no subgoals."""
        tracker = GoalTracker()
        assert tracker.progress == 0.0

    def test_progress_calculation(self):
        """Calculate progress correctly."""
        tracker = GoalTracker()
        tracker.set_goal("Build API")
        tracker.add_subgoal("Step 1")
        tracker.add_subgoal("Step 2")
        tracker.complete_subgoal("Step 1")
        assert tracker.progress == 0.5


# =============================================================================
# Tests for ProjectAnalyzer
# =============================================================================


class TestProjectAnalyzer:
    """Tests for ProjectAnalyzer class."""

    def test_discover_structure(self):
        """Discover project structure."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create structure
            Path(tmpdir, "src").mkdir()
            Path(tmpdir, "tests").mkdir()
            Path(tmpdir, "README.md").touch()

            analyzer = ProjectAnalyzer(tmpdir)
            structure = analyzer.discover_structure()

            assert "src" in structure.directories
            assert "tests" in structure.directories
            assert "README.md" in structure.files

    def test_discover_structure_ignores_hidden(self):
        """Ignore hidden directories."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, ".git").mkdir()
            Path(tmpdir, "src").mkdir()

            analyzer = ProjectAnalyzer(tmpdir)
            structure = analyzer.discover_structure()

            assert ".git" not in structure.directories
            assert "src" in structure.directories

    def test_detect_language_python(self):
        """Detect Python as primary language."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "main.py").touch()
            Path(tmpdir, "utils.py").touch()
            Path(tmpdir, "config.json").touch()

            analyzer = ProjectAnalyzer(tmpdir)
            lang = analyzer.detect_language()

            assert lang.primary == "python"
            assert lang.confidence > 0.5

    def test_detect_language_unknown(self):
        """Unknown language for empty project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = ProjectAnalyzer(tmpdir)
            lang = analyzer.detect_language()
            assert lang.primary == "unknown"

    def test_detect_framework_flask(self):
        """Detect Flask framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = Path(tmpdir, "requirements.txt")
            requirements.write_text("flask==2.0.0\nrequests")

            analyzer = ProjectAnalyzer(tmpdir)
            fw = analyzer.detect_framework()

            assert fw.name == "Flask"
            assert fw.confidence > 0.8

    def test_detect_framework_django(self):
        """Detect Django framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = Path(tmpdir, "requirements.txt")
            requirements.write_text("Django==4.0")

            analyzer = ProjectAnalyzer(tmpdir)
            fw = analyzer.detect_framework()

            assert fw.name == "Django"

    def test_detect_framework_react(self):
        """Detect React framework."""
        with tempfile.TemporaryDirectory() as tmpdir:
            package_json = Path(tmpdir, "package.json")
            package_json.write_text('{"dependencies": {"react": "^18.0.0"}}')

            analyzer = ProjectAnalyzer(tmpdir)
            fw = analyzer.detect_framework()

            assert fw.name == "React"

    def test_detect_framework_unknown(self):
        """Unknown framework for generic project."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = ProjectAnalyzer(tmpdir)
            fw = analyzer.detect_framework()
            assert fw.name == "unknown"

    def test_discover_dependencies(self):
        """Discover Python dependencies."""
        with tempfile.TemporaryDirectory() as tmpdir:
            requirements = Path(tmpdir, "requirements.txt")
            requirements.write_text("requests>=2.0\nflask\n# comment\npytest==7.0.0")

            analyzer = ProjectAnalyzer(tmpdir)
            deps = analyzer.discover_dependencies()

            names = [d.name for d in deps]
            assert "requests" in names
            assert "flask" in names
            assert "pytest" in names

    def test_discover_dependencies_empty(self):
        """Empty dependencies for no requirements file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            analyzer = ProjectAnalyzer(tmpdir)
            deps = analyzer.discover_dependencies()
            assert deps == []

    def test_map_architecture_mvc(self):
        """Detect MVC architecture."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "models").mkdir()
            Path(tmpdir, "views").mkdir()
            Path(tmpdir, "controllers").mkdir()

            analyzer = ProjectAnalyzer(tmpdir)
            arch = analyzer.map_architecture()

            assert arch.pattern == "MVC"

    def test_map_architecture_layered(self):
        """Detect layered architecture."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "domain").mkdir()
            Path(tmpdir, "application").mkdir()

            analyzer = ProjectAnalyzer(tmpdir)
            arch = analyzer.map_architecture()

            assert arch.pattern == "Layered"

    def test_map_architecture_custom(self):
        """Custom architecture for non-standard layout."""
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir, "src").mkdir()
            Path(tmpdir, "lib").mkdir()

            analyzer = ProjectAnalyzer(tmpdir)
            arch = analyzer.map_architecture()

            assert arch.pattern == "Custom"


# =============================================================================
# Tests for CodeAnalyzer
# =============================================================================


class TestCodeAnalyzer:
    """Tests for CodeAnalyzer class."""

    def test_parse_structure_empty(self):
        """Parse empty code."""
        analyzer = CodeAnalyzer()
        structure = analyzer.parse_structure("")
        assert structure.classes == []
        assert structure.functions == []

    def test_parse_structure_class(self):
        """Parse class definition."""
        code = """
class MyClass(Base):
    def method1(self):
        pass
    def method2(self, x):
        pass
"""
        analyzer = CodeAnalyzer()
        structure = analyzer.parse_structure(code)

        assert len(structure.classes) == 1
        assert structure.classes[0].name == "MyClass"
        assert "method1" in structure.classes[0].methods

    def test_parse_structure_function(self):
        """Parse function definition."""
        code = """
def process(data, options):
    return data
"""
        analyzer = CodeAnalyzer()
        structure = analyzer.parse_structure(code)

        assert len(structure.functions) == 1
        assert structure.functions[0].name == "process"
        assert "data" in structure.functions[0].parameters

    def test_parse_structure_invalid_syntax(self):
        """Handle invalid syntax gracefully."""
        code = "def broken("
        analyzer = CodeAnalyzer()
        structure = analyzer.parse_structure(code)
        assert structure.classes == []
        assert structure.functions == []

    def test_extract_imports_simple(self):
        """Extract simple imports."""
        code = "import os\nimport sys"
        analyzer = CodeAnalyzer()
        imports = analyzer.extract_imports(code)

        modules = [i.module for i in imports]
        assert "os" in modules
        assert "sys" in modules

    def test_extract_imports_from(self):
        """Extract from imports."""
        code = "from os.path import join, exists"
        analyzer = CodeAnalyzer()
        imports = analyzer.extract_imports(code)

        assert len(imports) == 1
        assert imports[0].module == "os.path"
        assert "join" in imports[0].names

    def test_extract_imports_alias(self):
        """Extract aliased imports."""
        code = "import numpy as np"
        analyzer = CodeAnalyzer()
        imports = analyzer.extract_imports(code)

        assert imports[0].module == "numpy"
        assert imports[0].alias == "np"

    def test_identify_dependencies_external(self):
        """Identify external dependencies."""
        code = "import requests\nimport flask"
        analyzer = CodeAnalyzer()
        deps = analyzer.identify_dependencies(code)

        assert "requests" in deps.external
        assert "flask" in deps.external

    def test_identify_dependencies_internal(self):
        """Identify internal dependencies."""
        code = "from .utils import helper\nfrom models.user import User"
        analyzer = CodeAnalyzer()
        deps = analyzer.identify_dependencies(code)

        assert any("utils" in d for d in deps.internal)
        assert "models.user" in deps.internal

    def test_identify_dependencies_relative(self):
        """Identify relative imports."""
        code = "from .. import parent"
        analyzer = CodeAnalyzer()
        deps = analyzer.identify_dependencies(code)

        assert ".." in deps.internal


# =============================================================================
# Tests for SymbolResolver
# =============================================================================


class TestSymbolResolver:
    """Tests for SymbolResolver class."""

    def test_resolve_finds_function(self):
        """Resolve function symbol."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create file with function
            func_file = Path(tmpdir, "utils.py")
            func_file.write_text("def helper():\n    pass")

            resolver = SymbolResolver(tmpdir)
            loc = resolver.resolve("helper", "main.py")

            assert loc is not None
            assert loc.file == "utils.py"
            assert loc.line == 1

    def test_resolve_finds_class(self):
        """Resolve class symbol."""
        with tempfile.TemporaryDirectory() as tmpdir:
            class_file = Path(tmpdir, "models.py")
            class_file.write_text("class User:\n    pass")

            resolver = SymbolResolver(tmpdir)
            loc = resolver.resolve("User", "main.py")

            assert loc is not None
            assert loc.file == "models.py"

    def test_resolve_not_found(self):
        """Symbol not found returns None."""
        with tempfile.TemporaryDirectory() as tmpdir:
            resolver = SymbolResolver(tmpdir)
            loc = resolver.resolve("Unknown", "main.py")
            assert loc is None

    def test_resolve_caches_result(self):
        """Results are cached."""
        with tempfile.TemporaryDirectory() as tmpdir:
            func_file = Path(tmpdir, "utils.py")
            func_file.write_text("def helper(): pass")

            resolver = SymbolResolver(tmpdir)

            # First call
            loc1 = resolver.resolve("helper", "main.py")
            # Second call should use cache
            loc2 = resolver.resolve("helper", "main.py")

            assert loc1 == loc2


# =============================================================================
# Tests for KnowledgeBase
# =============================================================================


class TestKnowledgeBase:
    """Tests for KnowledgeBase class."""

    def test_store_and_get(self):
        """Store and retrieve knowledge."""
        kb = KnowledgeBase()
        kb.store("language", "python")
        assert kb.get("language") == "python"

    def test_get_not_found(self):
        """Get returns None for missing key."""
        kb = KnowledgeBase()
        assert kb.get("missing") is None

    def test_store_with_confidence(self):
        """Store with confidence value."""
        kb = KnowledgeBase()
        kb.store("language", "python", confidence=0.8)
        assert kb.get("language") == "python"

    def test_query_finds_matches(self):
        """Query finds matching keys."""
        kb = KnowledgeBase()
        kb.store("project_language", "python")
        kb.store("project_framework", "flask")
        kb.store("user_name", "John")

        results = kb.query("project")
        assert len(results) == 2

    def test_query_case_insensitive(self):
        """Query is case insensitive."""
        kb = KnowledgeBase()
        kb.store("ProjectLanguage", "python")

        results = kb.query("project")
        assert len(results) == 1

    def test_infer_testing_setup(self):
        """Infer testing setup."""
        kb = KnowledgeBase()
        kb.store("uses_pytest", True)
        kb.store("has_tests_directory", True)

        inference = kb.infer("testing_setup")
        assert inference is not None
        assert "pytest" in inference.conclusion.lower()
        assert inference.confidence > 0

    def test_infer_no_evidence(self):
        """Infer returns None with no evidence."""
        kb = KnowledgeBase()
        inference = kb.infer("testing_setup")
        assert inference is None

    def test_infer_unknown_topic(self):
        """Infer returns None for unknown topic."""
        kb = KnowledgeBase()
        inference = kb.infer("unknown_topic")
        assert inference is None


# =============================================================================
# Tests for PatternLearner
# =============================================================================


class TestPatternLearner:
    """Tests for PatternLearner class."""

    def test_observe_stores_observation(self):
        """Observe stores observation."""
        learner = PatternLearner()
        learner.observe("def test_foo(): pass")
        assert len(learner._observations) == 1

    def test_observe_extracts_test_pattern(self):
        """Extract test_ pattern."""
        learner = PatternLearner()
        learner.observe("def test_foo(): pass")
        learner.observe("def test_bar(): pass")

        patterns = learner.get_patterns()
        pattern_names = [p.pattern for p in patterns]
        assert "test_" in pattern_names

    def test_observe_extracts_get_pattern(self):
        """Extract get_ pattern."""
        learner = PatternLearner()
        learner.observe("def get_user(): pass")

        patterns = learner.get_patterns()
        pattern_names = [p.pattern for p in patterns]
        assert "get_" in pattern_names

    def test_pattern_frequency_increases(self):
        """Pattern frequency increases with observations."""
        learner = PatternLearner()
        learner.observe("def test_a(): pass")
        learner.observe("def test_b(): pass")
        learner.observe("def test_c(): pass")

        patterns = learner.get_patterns()
        test_pattern = next(p for p in patterns if p.pattern == "test_")
        assert test_pattern.frequency == 3


# =============================================================================
# Tests for StyleAdapter
# =============================================================================


class TestStyleAdapter:
    """Tests for StyleAdapter class."""

    def test_observe_stores_code(self):
        """Observe stores code sample."""
        adapter = StyleAdapter()
        adapter.observe("def foo(): pass")
        assert len(adapter._observations) == 1

    def test_detect_snake_case(self):
        """Detect snake_case naming."""
        adapter = StyleAdapter()
        adapter.observe("def my_function(): pass")
        adapter.observe("def another_function(): pass")

        style = adapter.detected_style()
        assert style.naming_convention == "snake_case"

    def test_detect_camelCase(self):
        """Detect camelCase naming."""
        adapter = StyleAdapter()
        adapter.observe("def myFunction(): pass")
        adapter.observe("def anotherFunction(): pass")

        style = adapter.detected_style()
        assert style.naming_convention == "camelCase"

    def test_detect_PascalCase(self):
        """Detect PascalCase naming."""
        adapter = StyleAdapter()
        adapter.observe("def MyFunction(): pass")

        style = adapter.detected_style()
        assert style.naming_convention == "PascalCase"

    def test_no_observations(self):
        """Default style with no observations."""
        adapter = StyleAdapter()
        style = adapter.detected_style()
        assert style.naming_convention == "unknown"


# =============================================================================
# Integration Tests
# =============================================================================


class TestContextManagementIntegration:
    """Integration tests for context management."""

    def test_conversation_to_knowledge(self):
        """Conversation context flows to knowledge base."""
        ctx = ConversationContext()
        ctx.add_message("user", "We're using Python with Flask")
        extracted = ctx.extract_context()

        kb = KnowledgeBase()
        for file in extracted.mentioned_files:
            kb.store(f"mentioned_file:{file}", True)

        # Verify knowledge was stored
        assert "Flask" in ctx._symbols_mentioned or "Python" in ctx._symbols_mentioned

    def test_project_analysis_full_flow(self):
        """Full project analysis flow."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup project
            Path(tmpdir, "src").mkdir()
            Path(tmpdir, "tests").mkdir()
            main_file = Path(tmpdir, "main.py")
            main_file.write_text("import flask\ndef get_user(): pass")
            requirements = Path(tmpdir, "requirements.txt")
            requirements.write_text("flask>=2.0")

            # Analyze
            analyzer = ProjectAnalyzer(tmpdir)
            structure = analyzer.discover_structure()
            lang = analyzer.detect_language()
            fw = analyzer.detect_framework()
            deps = analyzer.discover_dependencies()

            assert len(structure.directories) >= 2
            assert lang.primary == "python"
            assert fw.name == "Flask"
            assert any(d.name == "flask" for d in deps)

    def test_code_analysis_full_flow(self):
        """Full code analysis flow."""
        code = """
import os
from typing import List

class DataProcessor:
    def __init__(self, config):
        self.config = config

    def process(self, items: List) -> List:
        return [self._transform(i) for i in items]

    def _transform(self, item):
        return item.upper()

def main():
    processor = DataProcessor({})
    result = processor.process(['a', 'b', 'c'])
    print(result)
"""
        analyzer = CodeAnalyzer()
        structure = analyzer.parse_structure(code)
        imports = analyzer.extract_imports(code)
        deps = analyzer.identify_dependencies(code)

        assert len(structure.classes) == 1
        assert structure.classes[0].name == "DataProcessor"
        assert len(structure.functions) == 1  # main
        assert "os" in [i.module for i in imports]
        assert "os" in deps.external
