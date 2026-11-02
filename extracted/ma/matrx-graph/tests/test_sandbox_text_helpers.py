"""The sandbox's text helpers: ``lower``, ``casefold``, ``startswith``, ``endswith``.

Added 2026-10-27 (generic-only playbook gap: a never-say list or a url test could not compare
case-insensitively, and ``.lower()`` is attribute access, which the sandbox bans outright).
They are bare-name helpers like ``coalesce`` — no method call becomes possible.
"""

from __future__ import annotations

import pytest

from matrx_graph.errors import ExecutionError
from matrx_graph.nodes._sandbox import safe_eval, validate_expression


def test_sandbox_lower_and_casefold():
    assert safe_eval("lower(inputs['name']) == 'riverbend dental'", {"name": "Riverbend DENTAL"}) is True
    # casefold is the stronger fold: German sharp s becomes "ss".
    assert safe_eval("casefold(inputs['w'])", {"w": "Straße"}) == "strasse"
    assert safe_eval("lower(inputs['w'])", {"w": "Straße"}) == "straße"


def test_sandbox_startswith_and_endswith():
    row = {"url": "https://example.com/blog/post.pdf"}
    assert safe_eval("startswith(inputs['url'], 'https://')", row) is True
    assert safe_eval("endswith(lower(inputs['url']), '.pdf')", row) is True
    assert safe_eval("startswith(inputs['url'], ['http://', 'https://'])", row) is True
    assert safe_eval("endswith(inputs['url'], '.html')", row) is False


def test_sandbox_text_helpers_treat_a_missing_value_as_no_match():
    assert safe_eval("lower(inputs['x'])", {"x": None}) is None
    assert safe_eval("startswith(inputs['x'], 'a')", {"x": None}) is False


def test_sandbox_text_helpers_refuse_a_non_text_value():
    with pytest.raises(ExecutionError, match="lower"):
        safe_eval("lower(inputs['x'])", {"x": 42})


def test_sandbox_text_helpers_stay_bare_names_only():
    validate_expression("lower(inputs['a'])")
    with pytest.raises(ExecutionError):
        validate_expression("inputs['a'].lower()")


# --- list helpers (2026-10-27): compare two lists without a comprehension -----------------------
# Rule 3 users: evidence keys an answer cites must be among the ids sent (AI-visibility), a gate's
# approved ids filter a list (any human gate), link ids already found are skipped (Smart Add).


def test_sandbox_intersection_keeps_the_first_lists_order():
    row = {"cited": ["gsc", "site", "made_up", "gsc"], "sent": ["site", "gsc", "reviews"]}
    assert safe_eval("intersection(inputs['cited'], inputs['sent'])", row) == ["gsc", "site", "gsc"]


def test_sandbox_difference_lists_what_was_never_sent():
    row = {"cited": ["gsc", "made_up"], "sent": ["gsc"]}
    assert safe_eval("difference(inputs['cited'], inputs['sent'])", row) == ["made_up"]
    assert safe_eval("len(difference(inputs['cited'], inputs['sent'])) == 0", row) is False


def test_sandbox_contains_any_and_all():
    row = {"ids": ["a1", "b2"], "approved": ["b2", "c3"]}
    assert safe_eval("contains_any(inputs['ids'], inputs['approved'])", row) is True
    assert safe_eval("contains_all(inputs['ids'], inputs['approved'])", row) is False
    assert safe_eval("contains_all(['b2'], inputs['approved'])", row) is True


def test_sandbox_list_helpers_treat_none_as_an_empty_list():
    assert safe_eval("intersection(inputs['x'], ['a'])", {"x": None}) == []
    assert safe_eval("difference(['a'], inputs['x'])", {"x": None}) == ["a"]
    assert safe_eval("contains_any(inputs['x'], ['a'])", {"x": None}) is False
    # Everything of an empty list is in any list.
    assert safe_eval("contains_all(inputs['x'], ['a'])", {"x": None}) is True


def test_sandbox_list_helpers_refuse_records_with_a_sentence():
    with pytest.raises(ExecutionError, match="intersection"):
        safe_eval("intersection(inputs['x'], ['a'])", {"x": [{"id": "a"}]})
    with pytest.raises(ExecutionError, match="list"):
        safe_eval("difference(inputs['x'], ['a'])", {"x": "abc"})


def test_sandbox_url_host():
    assert safe_eval("url_host(inputs['u'])", {"u": "https://www.Example.com/shop?x=1"}) == "example.com"
    assert safe_eval("url_host(inputs['u'])", {"u": "sarahsday.com/shop"}) == "sarahsday.com"
    assert safe_eval("url_host(inputs['u'])", {"u": "http://blog.example.co.uk:8080/a"}) == "blog.example.co.uk"
    assert safe_eval("url_host(inputs['u'])", {"u": ""}) == ""
    assert safe_eval("url_host(inputs['u'])", {"u": None}) is None
    assert safe_eval("url_host(inputs['u'])", {"u": "http://[bad"}) == ""
    # the weak-name anchor: an own link, never a platform's
    assert safe_eval("endswith(url_host(inputs['u']), ['instagram.com', 'tiktok.com'])",
                     {"u": "https://www.instagram.com/x"}) is True
    with pytest.raises(ExecutionError):
        safe_eval("url_host(inputs['u'])", {"u": 5})


def test_sandbox_on_site_matches_the_site_and_its_subdomains_only():
    targets = ["patagonia.com", "WWW.Worn-Wear.com"]
    cases = {
        "patagonia.com": True,
        "https://www.patagonia.com/shop": True,
        "eu.Patagonia.com": True,
        "worn-wear.com": True,
        "notpatagonia.com": False,
        "patagonia.com.evil.io": False,
        "": False,
    }
    for host, want in cases.items():
        assert safe_eval("on_site(inputs['h'], inputs['t'])", {"h": host, "t": targets}) is want, host
    assert safe_eval("on_site(inputs['h'], 'patagonia.com')", {"h": "a.patagonia.com"}) is True
    assert safe_eval("on_site(inputs['h'], inputs['t'])", {"h": None, "t": targets}) is False


def test_lower_and_casefold_take_a_list_of_texts_and_give_a_list():
    # Added 2026-10-27: a never-say list folded in one call, then compared with contains_any.
    assert safe_eval("lower(inputs['xs'])", {"xs": ["Riverbend", "DENTAL", None]}) == [
        "riverbend",
        "dental",
        None,
    ]
    assert safe_eval("casefold(inputs['xs'])", {"xs": ["Straße", "ÜBER"]}) == ["strasse", "über"]
    assert safe_eval(
        "contains_any(casefold(inputs['said']), casefold(inputs['never']))",
        {"said": ["We are CHEAP"], "never": ["we are cheap"]},
    ) is True


def test_list_helpers_refuse_a_non_text_item_with_its_position():
    with pytest.raises(ExecutionError, match=r"casefold\(\) needs text or a list of texts; item 1 is a int"):
        safe_eval("casefold(inputs['xs'])", {"xs": ["a", 3]})


def test_nfkc_turns_compatibility_forms_into_plain_letters():
    assert safe_eval("nfkc(inputs['w'])", {"w": "Ｃａｆé"}) == "Café"
    assert safe_eval("nfkc(inputs['w'])", {"w": "ﬁle ①"}) == "file 1"
    assert safe_eval("nfkc(inputs['ws'])", {"ws": ["Ｃａｆé", None]}) == ["Café", None]
    # Case and spacing are NOT nfkc's job.
    assert safe_eval("nfkc(inputs['w'])", {"w": "A  B"}) == "A  B"
    assert safe_eval("nfkc(inputs['w'])", {"w": None}) is None
    validate_expression("casefold(nfkc(inputs['w'])) == 'café'")


def test_collapse_spaces_joins_whitespace_runs():
    assert safe_eval("collapse_spaces(inputs['w'])", {"w": "  a \n\t b  "}) == "a b"
    assert safe_eval("collapse_spaces(inputs['ws'])", {"ws": [" x  y ", ""]}) == ["x y", ""]


def test_word_count_and_sha256_match_the_steps_they_replace() -> None:
    """A question set's per-question word count and fingerprint were a For Each each (Check a question
    set: 6 steps); the helpers give exactly what text.word_count and crypto.hash (sha256) give."""
    import hashlib

    from matrx_graph.checks import text_metrics
    from matrx_graph.nodes._sandbox import safe_eval

    texts = ["How do I fix a dense loaf?", "  one   two\nthree ", "", "naïve café — what's best?"]
    assert safe_eval("[word_count(t) for t in inputs['t']]", {"t": texts}) == [text_metrics(t)["words"] for t in texts]
    assert safe_eval("[sha256(t) for t in inputs['t']]", {"t": texts}) == [
        hashlib.sha256(t.encode("utf-8")).hexdigest() for t in texts
    ]


def test_sandbox_everyday_words_picks_dictionary_names_only():
    out = safe_eval(
        "everyday_words(inputs['names'])",
        {"names": ["Atoms", "Rothys", None, "", "Atoms", "Allbirds", "Render"]},
    )
    assert "Atoms" in out and "Render" in out
    assert "Rothys" not in out
    assert out.count("Atoms") == 1


def test_sha1_reproduces_the_stored_smart_add_evidence_keys() -> None:
    """Smart Add's code keys a description / address as ``<field>:<sha1-12>`` (matrx_social.identity.field_key);
    a workflow builds the same key with sha1 + collapse_spaces + lower, so a later round meets the stored row."""
    import hashlib

    import pytest

    from matrx_graph.nodes._sandbox import safe_eval

    field_key = pytest.importorskip("matrx_social.identity").field_key  # the host's key code, when installed

    texts = ["Small-batch coffee  roasted in\nSan Francisco.", "  123 Main St,\tSuite 4 ", "Naïve Café — OK", ""]
    expr = "[('description:' + sha1(collapse_spaces(lower(t)))[:12]) for t in inputs['t']]"
    assert safe_eval(expr, {"t": texts}) == [field_key("description", t) for t in texts]
    expr = "[('address:' + sha1(collapse_spaces(lower(t)))[:12]) for t in inputs['t']]"
    assert safe_eval(expr, {"t": texts}) == [field_key("address", t) for t in texts]
    assert safe_eval("sha1(inputs['t'])", {"t": "abc"}) == hashlib.sha1(b"abc").hexdigest()
