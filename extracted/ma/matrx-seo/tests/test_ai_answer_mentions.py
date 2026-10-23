from matrx_seo.providers.dataforseo.ai_answers import answer_mentions_target


def test_brand_name_matches_longer_recommendation_subject() -> None:
    mentioned, terms = answer_mentions_target(
        "1. Cosmetic Injectables Center Medspa — a strong local option.",
        ["Cosmetic Injectables", "Dr. Example"],
    )
    assert mentioned is True
    assert terms == ["Cosmetic Injectables", "Dr. Example"]


def test_doctor_alias_counts_as_same_brand_identity() -> None:
    mentioned, _ = answer_mentions_target(
        "Patients often recommend Dr. Armani Sadeghi.",
        ["Cosmetic Injectables Medspa", "Dr Armani Sadeghi"],
    )
    assert mentioned is True


def test_punctuation_and_spacing_are_tolerated() -> None:
    mentioned, _ = answer_mentions_target("Built with A.I. Matrx.", ["AI Matrx"])
    assert mentioned is True


def test_substring_inside_unrelated_word_is_not_a_mention() -> None:
    mentioned, _ = answer_mentions_target("The injectable market is growing.", ["Table"])
    assert mentioned is False


def test_short_brands_match_as_their_owners_write_them() -> None:
    """W3C, IBM, HP, AMD and 3M are real brands under four characters. Before
    2026-09-28 every one of them was refused outright, so ai_visibility reported
    them as never mentioned — a screen that lies."""
    cases = [
        ("The W3C publishes the HTML standard.", "W3C"),
        ("IBM and Google both ship quantum hardware.", "IBM"),
        ("Laptops from HP, Dell and Lenovo lead the list.", "HP"),
        ("AMD's Ryzen line competes on price.", "AMD"),
        ("3M makes the respirators most hospitals stock.", "3M"),
    ]
    for text, alias in cases:
        mentioned, terms = answer_mentions_target(text, [alias])
        assert mentioned is True, alias
        assert terms == [alias]


def test_short_alias_never_matches_an_ordinary_word() -> None:
    """The false positive the old four-character floor guarded against: once case
    is thrown away, a short brand collides with ordinary words and with the
    inside of longer tokens. A short alias matches case-sensitively, whole token."""
    assert answer_mentions_target("It is 90 hp and it runs on AI.", ["IT"])[0] is False
    assert answer_mentions_target("The engine makes 90 hp.", ["HP"])[0] is False
    assert answer_mentions_target("HPE sells servers.", ["HP"])[0] is False
    assert answer_mentions_target("The amd64 build is ready.", ["AMD"])[0] is False
    assert answer_mentions_target("Mention the w3c spec casually.", ["W3C"])[0] is False


def test_all_lowercase_short_alias_is_refused() -> None:
    """A bare domain root ("hp" from hp.com, "it" from it.com) is not how any
    brand writes its name; matching it would hit every 'it' in the text."""
    mentioned, terms = answer_mentions_target("Go to it, and to HP.", ["it", "hp"])
    assert mentioned is False
    assert terms == []


def test_an_everyday_word_name_opening_a_list_item_or_sentence_is_named() -> None:
    """Break: a list item or sentence that opens with the brand ("1. Render — …", "- Render: …",
    "Render offers …") read as the everyday word, so the answer counted the brand absent."""
    from matrx_seo.name_matching import proper_name_match

    for text in (
        "1. Render — managed hosting",
        "- Render: good for small teams",
        "Render offers managed Postgres.",
        "Render is a hosting platform.",
        "* **Render**: fast deploys",
        "- Render\n- Fly",
    ):
        assert proper_name_match("Render", text) == "Render", text
        assert answer_mentions_target(text, ["Render"])[0] is True, text
    assert answer_mentions_target("Acme is one option.", ["Acme"])[0] is True


def test_the_everyday_word_opening_a_sentence_is_still_not_the_name() -> None:
    from matrx_seo.name_matching import proper_name_match

    for text in ("Render the video at 4k.", "- Render the scene twice", "Stream it tonight."):
        assert proper_name_match("Render", text) is None, text
    assert proper_name_match("Render", "Render the page", verbs=()) is None
    assert proper_name_match("Render", "Render offers hosting", verbs=()) is None  # the knob decides


def test_an_everyday_word_name_with_only_a_verb_cue_is_not_the_brand() -> None:
    """Break: "Monday is the best day to post", "Signal has to be strong", "Linear is fine" each
    counted as a brand mention — a sentence-opening everyday word plus a verb is how English opens
    any sentence. A verb cue now needs a second signal."""
    from matrx_seo.name_matching import proper_name_match

    for term, text in (
        ("Monday", "Monday is the best day to post."),
        ("Signal", "Signal has to be strong for the call to work."),
        ("Linear", "Linear is fine for this regression."),
    ):
        assert proper_name_match(term, text) is None, text
        # the register flags each as an everyday word ("Monday" is a proper noun to the dictionary)
        assert answer_mentions_target(text, [term], common_word_terms=[term])[0] is False, text


def test_a_verb_cue_with_a_second_signal_is_the_brand() -> None:
    from matrx_seo.name_matching import proper_name_match

    # a product word in the same sentence
    assert proper_name_match("Linear", "Linear is a project tracking tool.") == "Linear"
    assert proper_name_match("Signal", "Signal is a messaging app with end-to-end encryption.") == "Signal"
    # the name written as a domain elsewhere in the text
    assert proper_name_match("Linear", "Linear is fine.\nSee linear.app for details.") == "Linear"
    # a tracked competitor named in the same answer
    text = "1. Jira\n2. Linear is fine for small teams"
    assert proper_name_match("Linear", text) is None
    assert proper_name_match("Linear", text, co_terms=["Jira", "Linear"]) == "Linear"
    # the product words are the knob's, not constants
    assert proper_name_match("Linear", "Linear is a project tracking tool.", context_words=()) is None
