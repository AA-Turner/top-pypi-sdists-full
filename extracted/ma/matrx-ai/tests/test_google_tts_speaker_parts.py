"""Gemini 3 speech models need every text part of a multi-speaker request to name its speaker."""

from google.genai import types

from matrx_ai.providers.google.google_api import _speaker_tagged_parts


def test_each_line_names_its_speaker_and_drops_the_label() -> None:
    text = "Alex: Hello there.\nSarah: Hi!\ncontinued line\nAlex: Bye."
    parts = _speaker_tagged_parts(text, ["Alex", "Sarah"])
    assert [p["speech_metadata"]["speaker"] for p in parts] == ["Alex", "Sarah", "Alex"]
    assert parts[0]["text"] == "Hello there."
    assert parts[1]["text"] == "Hi!\ncontinued line"
    # The SDK accepts the shape (a wrong key would be dropped or rejected).
    built = types.Part(**parts[0])
    assert built.speech_metadata is not None and built.speech_metadata.speaker == "Alex"


def test_title_direction_and_tags_are_not_spoken() -> None:
    text = "My Title\n<podcast_dialogue>\nRead it as an interview:\nAlex: One.\nSarah: Two.\n</podcast_dialogue>"
    parts = _speaker_tagged_parts(text, ["Alex", "Sarah"])
    assert [p["text"] for p in parts] == ["One.", "Two."]
    assert "interview" in parts[0]["speech_metadata"]["style"]
