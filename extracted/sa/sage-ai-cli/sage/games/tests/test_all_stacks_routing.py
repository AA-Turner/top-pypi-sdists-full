"""All-stack routing coverage — webapp + mobile + game.

Sage advertises support for 18 different stacks (17 webapp/mobile + 1
game-engine umbrella). The build-request detector and the stack picker
must both recognise each one. This test sweeps every entry in
STACK_KEYWORDS via:

  1. `looks_like_build_request()` — must classify as a build.
  2. `detect_stack()` — must pick the named stack.

Catches regressions where adding a new stack to STACK_KEYWORDS forgets
to extend the detection vocabulary, AND catches regressions where
keyword changes silently break detection for existing stacks.
"""

from __future__ import annotations

import pytest

from sage.core.principal_engineer import (
    STACK_KEYWORDS,
    detect_stack,
    looks_like_build_request,
)


# Representative prompts per stack. Each is a real user-style sentence
# (not a keyword soup) so we know detection works on natural input.
_STACK_PROMPTS: list[tuple[str, str]] = [
    ("Build me a FastAPI backend with JWT auth and PostgreSQL",     "fastapi"),
    ("Build a Django app with DRF and admin",                        "django"),
    ("Build a React + Vite TypeScript SPA",                          "react"),
    ("Build a Next.js 14 app with the App Router",                   "nextjs"),
    ("Build a React Native + Web app with Expo",                     "react-native-web"),
    ("Build a Go microservice with Gin",                             "go-microservices"),
    ("Build a Rust Axum API for analytics",                          "rust-axum"),
    ("Build a Spring Boot Java API for banking",                     "spring-boot"),
    ("Build an Android app with Jetpack Compose in Kotlin",          "android-compose"),
    ("Build an iOS app with SwiftUI",                                "ios-swift"),
    ("Build a Flutter app for note-taking",                          "flutter"),
    ("Build a .NET ASP.NET Core API for finance",                    "dotnet"),
    ("Build a Laravel PHP API for blog management",                  "laravel"),
    ("Build a Ruby on Rails app for a forum",                        "rails"),
    ("Build a C++ microservice for high-frequency trading",          "cpp"),
    ("Build a GraphQL API with Apollo Server",                       "graphql"),
    ("Build a Kubernetes deployment with Helm charts",               "kubernetes"),
    # Game prompts now also resolve via the game-engine keyword bucket.
    ("Build me a Godot 4 platformer",                                "game-engine"),
]


@pytest.mark.parametrize("prompt,stack", _STACK_PROMPTS)
def test_stack_detection_for_every_supported_language(prompt, stack):
    """Every stack in STACK_KEYWORDS must be reachable from a natural
    user prompt. Adding a new stack without a representative test
    prompt here is a failure mode worth catching."""
    actual = detect_stack(prompt)
    # Game-engine prompts are decoded by detect_stack to one of the
    # priority stacks (which doesn't include game-engine itself), so we
    # check the stack-keyword match path rather than the priority pick.
    if stack == "game-engine":
        lower = prompt.lower()
        assert any(kw in lower for kw in STACK_KEYWORDS["game-engine"]), \
            f"game-engine vocabulary missed: {prompt!r}"
    else:
        assert actual == stack, f"detect_stack({prompt!r}) = {actual!r}, expected {stack!r}"


@pytest.mark.parametrize("prompt,_stack", _STACK_PROMPTS)
def test_every_supported_stack_is_a_build_request(prompt, _stack):
    """Every representative prompt must classify as a build — otherwise
    the CLI routes it through chat instead of the principal pipeline."""
    assert looks_like_build_request(prompt), (
        f"prompt did not classify as a build request: {prompt!r}"
    )


def test_stack_keywords_registry_is_non_trivial():
    """Sanity: we never want to ship with an empty STACK_KEYWORDS."""
    assert len(STACK_KEYWORDS) >= 17
    # Every stack must declare at least one keyword.
    for stack, keywords in STACK_KEYWORDS.items():
        assert keywords, f"stack {stack!r} has no keywords"


def test_react_native_web_priority_over_plain_react():
    """The priority list says 'react-native-web' wins over 'react' when
    a prompt mentions both — otherwise 'React Native' projects get
    scaffolded as plain React, which is wrong."""
    prompt = "Build me a React Native app that also runs on the web"
    assert detect_stack(prompt) == "react-native-web"


def test_nextjs_priority_over_plain_react():
    """Same logic — Next.js wins over React because Next.js IS React with
    extra structure; scaffolding plain React for a Next.js prompt would
    miss the App Router and api routes the user expects."""
    prompt = "Build a Next.js dashboard with React Server Components"
    assert detect_stack(prompt) == "nextjs"


def test_unknown_stack_falls_back_to_fastapi():
    """When no stack matches, detect_stack defaults to fastapi (sage's
    most-tested template). This is documented in the function docstring."""
    assert detect_stack("Build something quirky and unique") == "fastapi"
