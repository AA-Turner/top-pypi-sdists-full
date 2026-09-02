"""Name → gender resolution — THE GENDER CHAIN's lookup table.

Lives in ``config`` (not in the podcast runner that grew it) because TWO layers
need the same answer and must never disagree:

* ``matrx_ai.agent_runners.podcast_generator`` — resolves each speaker's gender
  BEFORE a voice is drawn, so a female-named host never draws a male voice.
* ``matrx_ai.config.tts_config`` — decides which configured speaker adopts which
  drifted SCRIPT label. Pairing those by position alone inverts genders (config
  [Sarah→female voice, Owen→male voice] + script [Marcus, Elena] gave Marcus a
  female voice), because the script's labels are the only thing that says who is
  actually speaking.

Deterministic by construction: the same name always yields the same gender, on
the first run and on every resume, in-process or in a new worker. A random or
stateful answer would re-cast a resumed run and desync it from audio already
rendered.
"""

from __future__ import annotations

import re

__all__ = [
    "COMMON_NAME_GENDERS",
    "HONORIFICS",
    "gender_for_name",
    "normalize_gender",
]


def normalize_gender(value: str | None) -> str:
    """Map any declared gender string onto the three buckets the voice pool
    understands. Unknown / empty → ``neutral`` (any voice eligible)."""
    v = (value or "").strip().lower()
    if v in ("m", "male", "man", "boy", "masculine"):
        return "male"
    if v in ("f", "female", "woman", "girl", "feminine"):
        return "female"
    return "neutral"


# ── Name → gender (THE GENDER CHAIN, 2026-08-20) ────────────────────────────
#
# A speaker's gender must be KNOWN before a voice is drawn, or a female-named
# host gets a male voice and the co-host calls a man "Sarah" — the exact defect
# reported 2026-08-20. It was reachable because the pipeline SUGGESTS a cast
# (_speaker_names_json -> _default_cast, which knows every name's gender), sends
# only the NAMES to the script agent, and then throws the genders away: the
# audio stage re-derived the cast from the dialogue labels with no gender at
# all, so every speaker resolved "neutral" and drew from the MIXED pool. A coin
# flip per host, every run that didn't pin a cast in the UI.
#
# Gender now resolves through a deterministic chain (request -> the agent's
# <speaker_settings> -> this table), so the same name always yields the same
# gender — on the first run and on every resume, in-process or in a new worker.
# Deterministic matters: a random or stateful answer would re-cast a resumed run
# and desync it from the audio already rendered.
COMMON_NAME_GENDERS: dict[str, str] = {
    # female
    "sarah": "female",
    "maria": "female",
    "priya": "female",
    "lena": "female",
    "nina": "female",
    "tara": "female",
    "ivy": "female",
    "zara": "female",
    "maya": "female",
    "rosa": "female",
    "emma": "female",
    "olivia": "female",
    "ava": "female",
    "sophia": "female",
    "isabella": "female",
    "mia": "female",
    "amelia": "female",
    "harper": "female",
    "evelyn": "female",
    "abigail": "female",
    "emily": "female",
    "elizabeth": "female",
    "sofia": "female",
    "grace": "female",
    "chloe": "female",
    "victoria": "female",
    "riley": "female",
    "aria": "female",
    "lily": "female",
    "hannah": "female",
    "zoe": "female",
    "nora": "female",
    "layla": "female",
    "eleanor": "female",
    "naomi": "female",
    "ruby": "female",
    "clara": "female",
    "julia": "female",
    "anna": "female",
    "elena": "female",
    "claire": "female",
    "alice": "female",
    "diana": "female",
    "laura": "female",
    "rachel": "female",
    "rebecca": "female",
    "jessica": "female",
    "amanda": "female",
    "michelle": "female",
    "nicole": "female",
    "katherine": "female",
    "catherine": "female",
    "megan": "female",
    "amy": "female",
    "linda": "female",
    "susan": "female",
    "karen": "female",
    "nancy": "female",
    "lisa": "female",
    "betty": "female",
    "sandra": "female",
    "ashley": "female",
    "kimberly": "female",
    "donna": "female",
    "carol": "female",
    "michele": "female",
    "dana": "female",
    "fatima": "female",
    "aisha": "female",
    "leila": "female",
    "yasmin": "female",
    "sana": "female",
    "ana": "female",
    "carmen": "female",
    "lucia": "female",
    "valentina": "female",
    "camila": "female",
    "yuki": "female",
    "mei": "female",
    "ling": "female",
    "keiko": "female",
    "ingrid": "female",
    "astrid": "female",
    "freya": "female",
    "sonia": "female",
    "vera": "female",
    "iris": "female",
    "hazel": "female",
    "willow": "female",
    "delia": "female",
    "rita": "female",
    "paula": "female",
    # male
    "alex": "male",
    "ben": "male",
    "sam": "male",
    "omar": "male",
    "david": "male",
    "marcus": "male",
    "noah": "male",
    "leo": "male",
    "owen": "male",
    "felix": "male",
    "liam": "male",
    "james": "male",
    "oliver": "male",
    "william": "male",
    "benjamin": "male",
    "lucas": "male",
    "henry": "male",
    "theodore": "male",
    "jack": "male",
    "levi": "male",
    "daniel": "male",
    "matthew": "male",
    "michael": "male",
    "ethan": "male",
    "jacob": "male",
    "logan": "male",
    "mason": "male",
    "elijah": "male",
    "aiden": "male",
    "carter": "male",
    "ryan": "male",
    "nathan": "male",
    "isaac": "male",
    "caleb": "male",
    "julian": "male",
    "hunter": "male",
    "adam": "male",
    "andrew": "male",
    "joshua": "male",
    "christopher": "male",
    "john": "male",
    "robert": "male",
    "thomas": "male",
    "charles": "male",
    "george": "male",
    "edward": "male",
    "peter": "male",
    "paul": "male",
    "mark": "male",
    "steven": "male",
    "kevin": "male",
    "brian": "male",
    "eric": "male",
    "jason": "male",
    "jeff": "male",
    "greg": "male",
    "carlos": "male",
    "diego": "male",
    "miguel": "male",
    "javier": "male",
    "raj": "male",
    "arjun": "male",
    "amir": "male",
    "hassan": "male",
    "ahmed": "male",
    "ali": "male",
    "yusuf": "male",
    "ibrahim": "male",
    "hiroshi": "male",
    "kenji": "male",
    "wei": "male",
    "chen": "male",
    "lars": "male",
    "erik": "male",
    "anders": "male",
    "viktor": "male",
    "dmitri": "male",
    "pavel": "male",
    "tomas": "male",
    "rafael": "male",
    "gabriel": "male",
    "victor": "male",
    "simon": "male",
    "martin": "male",
    "oscar": "male",
    "hugo": "male",
    "milo": "male",
    "theo": "male",
    "silas": "male",
    "desmond": "male",
    "malik": "male",
    "andre": "male",
}

# Skip honorifics so "Dr Sarah" resolves on "Sarah".
HONORIFICS: frozenset[str] = frozenset(
    {"dr", "mr", "mrs", "ms", "miss", "prof", "professor", "sir", "captain"}
)


def gender_for_name(name: str, declared: str = "", table: dict[str, str] | None = None) -> str:
    """Resolve one speaker's gender. Declared value wins; else the name table;
    else "" (unknown — the caller decides how loudly to complain).

    ``table`` lets a caller layer its own authoritative names over the shared
    one (the podcast runner's default cast IS the pairing it suggests).

    Only the FIRST non-honorific token is looked up, so "Dr. Sarah Chen" and
    "Sarah" agree."""
    if declared and declared.strip():
        return normalize_gender(declared)
    lookup = COMMON_NAME_GENDERS if table is None else table
    tokens = [t for t in re.split(r"[^A-Za-z]+", name or "") if t]
    for token in tokens:
        found = lookup.get(token.lower())
        if found and token.lower() not in HONORIFICS:
            return found
    return ""
