"""Guard tests for the code-output integrity validators.

Reproduces the failure mode from 2026-05-15: openrouter:qwen/qwen3-coder:free
emitted Python code containing Chinese identifiers (`ai广告生成器`) plus
aider-style `<<<<<<< SEARCH … >>>>>>> REPLACE` markers that sage couldn't
apply. Both must be hard-rejected so the model gets a retry with explicit
guidance instead of "processing anyway".
"""

import pytest

from sage.main import (
    _detect_aider_style_diff_garbage,
    _detect_non_english_code_identifiers,
)


class TestNonEnglishIdentifiers:
    """CJK characters in identifiers are unconditional failures."""

    def test_cjk_in_python_import(self):
        bad = (
            "```python\n"
            "from ai广告生成器 import AdGenerator\n"
            "```\n"
        )
        has, offenders = _detect_non_english_code_identifiers(bad)
        assert has
        assert any("广告" in o for o in offenders)

    def test_cjk_in_function_name(self):
        bad = (
            "```python\n"
            "def 测试_generate():\n"
            "    pass\n"
            "```\n"
        )
        has, offenders = _detect_non_english_code_identifiers(bad)
        assert has

    def test_cjk_in_typescript_class(self):
        bad = (
            "```typescript\n"
            "class 广告Service {}\n"
            "```\n"
        )
        has, _ = _detect_non_english_code_identifiers(bad)
        assert has

    def test_cjk_in_string_literal_is_fine(self):
        """String literals (and i18n labels) may contain any language."""
        ok = (
            "```python\n"
            "greeting = \"你好世界\"\n"
            "label = '広告キャンペーン'\n"
            "```\n"
        )
        has, _ = _detect_non_english_code_identifiers(ok)
        assert not has

    def test_cjk_in_prose_outside_code_is_fine(self):
        """Marketing copy referencing Chinese support shouldn't trigger."""
        ok = "The platform supports 中文 language. Here is code:\n"
        ok += "```python\ndef normal_function():\n    pass\n```\n"
        has, _ = _detect_non_english_code_identifiers(ok)
        assert not has

    def test_pure_english_passes(self):
        ok = (
            "```python\n"
            "from ai_module import AdGenerator\n"
            "def generate_banner_ad():\n"
            "    pass\n"
            "```\n"
        )
        has, _ = _detect_non_english_code_identifiers(ok)
        assert not has

    def test_no_code_blocks_returns_false(self):
        has, _ = _detect_non_english_code_identifiers("Just prose, no code.")
        assert not has

    def test_file_block_with_cjk_caught(self):
        """sage's own FILE: block format is also scanned."""
        bad = (
            "FILE: app/services/ad_service.py\n"
            "```python\n"
            "from 广告 import 生成器\n"
            "```\n"
        )
        has, _ = _detect_non_english_code_identifiers(bad)
        assert has

    def test_offenders_capped(self):
        """Don't spam the user with 50 offenders — cap at 5."""
        many = "```python\n" + "\n".join(f"def 函数_{i}(): pass" for i in range(20)) + "\n```\n"
        has, offenders = _detect_non_english_code_identifiers(many)
        assert has
        assert len(offenders) <= 5


class TestAiderStyleDiffGarbage:
    """The `<<<<<<< SEARCH … >>>>>>> REPLACE` format is unsupported."""

    def test_detects_aider_block(self):
        diff = (
            "<<<<<<< SEARCH\n"
            "=======\n"
            "import pytest\n"
            ">>>>>>> REPLACE\n"
        )
        assert _detect_aider_style_diff_garbage(diff)

    def test_requires_both_markers(self):
        """Either marker alone (e.g. a merge conflict snippet in a doc) is fine."""
        only_search = "<<<<<<< SEARCH\n=======\nstuff\n"
        only_replace = "=======\nstuff\n>>>>>>> REPLACE\n"
        assert not _detect_aider_style_diff_garbage(only_search)
        assert not _detect_aider_style_diff_garbage(only_replace)

    def test_normal_file_block_passes(self):
        ok = "FILE: app/main.py\n```python\nprint('hi')\n```\n"
        assert not _detect_aider_style_diff_garbage(ok)

    def test_user_actual_response_rejected(self):
        """The exact garbage from the 2026-05-15 transcript should be caught."""
        actual = (
            "```python\n"
            "<<<<<<< SEARCH\n"
            "=======\n"
            "import pytest\n"
            "from ai广告生成器 import AdGenerator\n"
            "from ai营销代理 import MarketingAgent\n"
            ">>>>>>> REPLACE\n"
            "```\n"
        )
        assert _detect_aider_style_diff_garbage(actual)
        has, offenders = _detect_non_english_code_identifiers(actual)
        assert has
        assert offenders  # at least one
