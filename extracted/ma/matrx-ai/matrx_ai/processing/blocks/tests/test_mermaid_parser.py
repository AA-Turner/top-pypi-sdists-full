"""Tests for mermaid_parser.py — forgiving metadata extraction, verbatim source."""

from matrx_ai.processing.blocks.block_detector import split_content_into_blocks
from matrx_ai.processing.blocks.parsers.mermaid_parser import parse_mermaid


class TestDiagramTypeDetection:
    def test_flowchart(self):
        assert parse_mermaid("flowchart TD\n  A --> B").diagram_type == "flowchart"

    def test_graph_alias(self):
        assert parse_mermaid("graph LR\n  A --> B").diagram_type == "flowchart"

    def test_sequence(self):
        assert parse_mermaid("sequenceDiagram\n  A->>B: hi").diagram_type == "sequence"

    def test_class(self):
        assert parse_mermaid("classDiagram\n  Animal <|-- Duck").diagram_type == "class"

    def test_state_v2(self):
        assert parse_mermaid("stateDiagram-v2\n  [*] --> Idle").diagram_type == "state"

    def test_er(self):
        assert parse_mermaid("erDiagram\n  USER ||--o{ ORDER : places").diagram_type == "er"

    def test_journey(self):
        assert parse_mermaid("journey\n  title My day").diagram_type == "journey"

    def test_gantt(self):
        assert parse_mermaid("gantt\n  title Plan").diagram_type == "gantt"

    def test_pie(self):
        assert parse_mermaid('pie\n  "A" : 10').diagram_type == "pie"

    def test_mindmap(self):
        assert parse_mermaid("mindmap\n  root((Idea))").diagram_type == "mindmap"

    def test_timeline(self):
        assert parse_mermaid("timeline\n  2024 : event").diagram_type == "timeline"

    def test_quadrant(self):
        assert parse_mermaid("quadrantChart\n  title Q").diagram_type == "quadrant"

    def test_git(self):
        assert parse_mermaid("gitGraph\n  commit").diagram_type == "git"

    def test_c4(self):
        assert parse_mermaid("C4Context\n  title X").diagram_type == "c4"

    def test_sankey_beta(self):
        assert parse_mermaid("sankey-beta\nA,B,10").diagram_type == "sankey"

    def test_xychart_beta(self):
        assert parse_mermaid("xychart-beta\n  title X").diagram_type == "xychart"

    def test_kanban(self):
        assert parse_mermaid("kanban\n  Todo").diagram_type == "kanban"

    def test_architecture_beta(self):
        assert parse_mermaid("architecture-beta\n  group api").diagram_type == "architecture"

    def test_requirement(self):
        assert parse_mermaid("requirementDiagram\n  requirement r1 {}").diagram_type == "requirement"

    def test_skips_comments_and_blanks(self):
        source = "\n%% a comment\n%%{init: {'theme': 'dark'}}%%\nflowchart LR\n  A --> B"
        assert parse_mermaid(source).diagram_type == "flowchart"

    def test_unknown(self):
        assert parse_mermaid("definitely not mermaid").diagram_type == "unknown"


class TestFrontmatter:
    def test_title_extracted(self):
        source = '---\ntitle: My Great Flow\n---\nflowchart TD\n  A --> B'
        result = parse_mermaid(source)
        assert result.title == "My Great Flow"
        assert result.diagram_type == "flowchart"

    def test_quoted_title(self):
        source = '---\ntitle: "Quoted Title"\n---\npie\n  "A" : 1'
        assert parse_mermaid(source).title == "Quoted Title"

    def test_no_frontmatter(self):
        assert parse_mermaid("flowchart TD\n  A --> B").title is None


class TestForgivingContract:
    def test_never_raises_on_garbage(self):
        for garbage in ["", "   ", "\x00\x01", "---\n---", "}{[]"]:
            result = parse_mermaid(garbage)
            assert result.source == garbage  # verbatim, always

    def test_source_verbatim_never_modified(self):
        source = "flowchart TD\n  A[Bad (label] --> B"  # invalid mermaid
        result = parse_mermaid(source)
        assert result.source == source
        assert result.is_valid is None  # server cannot validate


class TestDetectorIntegration:
    def test_mermaid_fence_detected(self):
        content = "intro\n\n```mermaid\nflowchart TD\n  A --> B\n```\n\noutro"
        blocks = split_content_into_blocks(content)
        mermaid_blocks = [b for b in blocks if b.type == "mermaid"]
        assert len(mermaid_blocks) == 1
        assert "flowchart TD" in mermaid_blocks[0].content
        assert mermaid_blocks[0].language == "mermaid"

    def test_mmd_alias_normalizes(self):
        content = "```mmd\ngraph LR\n  A --> B\n```"
        blocks = split_content_into_blocks(content)
        mermaid_blocks = [b for b in blocks if b.type == "mermaid"]
        assert len(mermaid_blocks) == 1
        assert mermaid_blocks[0].language == "mmd"  # original fence language preserved

    def test_json_diagram_block_unaffected(self):
        content = '```json\n{"diagram": {"title": "T", "nodes": [{"id": "a", "label": "A"}]}}\n```'
        blocks = split_content_into_blocks(content)
        assert any(b.type == "diagram" for b in blocks)
        assert not any(b.type == "mermaid" for b in blocks)

    def test_plain_code_fence_unaffected(self):
        content = "```python\nprint('hi')\n```"
        blocks = split_content_into_blocks(content)
        assert any(b.type == "code" and b.language == "python" for b in blocks)
