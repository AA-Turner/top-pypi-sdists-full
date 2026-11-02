from agentic_devtools.ai_providers.availability import _split_error_clauses


def test_split_error_clauses_preserves_punctuation_inside_quotes() -> None:
    segments = _split_error_clauses("base_ref 'refs/heads/feature;foo,but.1' was not found; custom_agent failed")
    assert segments == ["base_ref 'refs/heads/feature;foo,but.1' was not found", " custom_agent failed"]


def test_split_error_clauses_keeps_apostrophes_and_non_matching_quotes_stable() -> None:
    segments = _split_error_clauses('base_ref wasn\'t found. custom_agent says "ok" but model failed')
    assert segments == ["base_ref wasn't found", ' custom_agent says "ok" but model failed']


def test_split_error_clauses_ignores_non_matching_quote_type_inside_quoted_span() -> None:
    segments = _split_error_clauses("base_ref 'refs/heads/feature\"but' was not found; model context")
    assert segments == ["base_ref 'refs/heads/feature\"but' was not found", " model context"]


def test_split_error_clauses_preserves_semicolons_inside_backticks() -> None:
    segments = _split_error_clauses("base_ref `refs/heads/feature;foo,but.1` was not found; custom_agent failed")
    assert segments == ["base_ref `refs/heads/feature;foo,but.1` was not found", " custom_agent failed"]


def test_split_error_clauses_requires_word_boundary_for_contrast_clause_split() -> None:
    segments = _split_error_clauses("base_ref is valid, buttering custom_agent is not found")
    assert segments == ["base_ref is valid, buttering custom_agent is not found"]
