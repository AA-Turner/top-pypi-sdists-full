from __future__ import annotations
import pytest
from ghrepo import GHRepo

REPO_URLS = [
    (
        "git://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git://github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git@github.com:jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "git@github.com:jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    ("GIT://GitHub.COM/jwodder/headerparser", GHRepo("jwodder", "headerparser")),
    ("git@github.com:joe-q-coder/my.repo.git", GHRepo("joe-q-coder", "my.repo")),
    ("git@GITHUB.com:joe-q-coder/my.repo.git", GHRepo("joe-q-coder", "my.repo")),
    (
        "ssh://git@github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "ssh://git@github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    ("ssh://git@github.com/-/test", GHRepo("-", "test")),
    ("SSH://git@GITHUB.COM/-/test", GHRepo("-", "test")),
    (
        "https://api.github.com/repos/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://api.github.com/repos/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    ("api.github.com/repos/jwodder/headerparser", GHRepo("jwodder", "headerparser")),
    ("https://api.github.com/repos/none-/-none", GHRepo("none-", "-none")),
    ("HttpS://api.github.com/repos/none-/-none", GHRepo("none-", "-none")),
    ("http://api.github.com/repos/none-/-none", GHRepo("none-", "-none")),
    ("Http://api.github.com/repos/none-/-none", GHRepo("none-", "-none")),
    ("Api.GitHub.Com/repos/jwodder/headerparser", GHRepo("jwodder", "headerparser")),
    (
        "https://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/headerparser.git",
        GHRepo("jwodder", "headerparser"),
    ),
    ("https://github.com/jwodder/headerparser.git/", GHRepo("jwodder", "headerparser")),
    (
        "https://github.com/jwodder/headerparser/",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "http://www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    ("github.com/jwodder/headerparser.git", GHRepo("jwodder", "headerparser")),
    ("github.com/jwodder/headerparser.git/", GHRepo("jwodder", "headerparser")),
    ("github.com/jwodder/headerparser/", GHRepo("jwodder", "headerparser")),
    (
        "www.github.com/jwodder/headerparser",
        GHRepo("jwodder", "headerparser"),
    ),
    (
        "https://github.com/jwodder/none.git",
        GHRepo("jwodder", "none"),
    ),
    ("https://github.com/joe-coder/hello.world", GHRepo("joe-coder", "hello.world")),
    ("http://github.com/joe-coder/hello.world", GHRepo("joe-coder", "hello.world")),
    ("HTTPS://GITHUB.COM/joe-coder/hello.world", GHRepo("joe-coder", "hello.world")),
    (
        "HTTPS://WWW.GITHUB.COM/joe-coder/hello.world",
        GHRepo("joe-coder", "hello.world"),
    ),
    ("https://github.com/-Jerry-/geshi-1.0.git", GHRepo("-Jerry-", "geshi-1.0")),
    ("https://github.com/-Jerry-/geshi-1.0.git/", GHRepo("-Jerry-", "geshi-1.0")),
    ("https://github.com/-Jerry-/geshi-1.0/", GHRepo("-Jerry-", "geshi-1.0")),
    ("https://www.github.com/-Jerry-/geshi-1.0", GHRepo("-Jerry-", "geshi-1.0")),
    ("github.com/-Jerry-/geshi-1.0", GHRepo("-Jerry-", "geshi-1.0")),
    (
        "https://x-access-token:1234567890@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    (
        "https://my.username@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    (
        "https://user%20name@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    (
        "https://user+name@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    (
        "https://~user.name@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    ("https://@github.com/octocat/Hello-World", GHRepo("octocat", "Hello-World")),
    (
        "https://user:@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    (
        "https://:pass@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
    ("https://:@github.com/octocat/Hello-World", GHRepo("octocat", "Hello-World")),
    (
        "https://user:pass:extra@github.com/octocat/Hello-World",
        GHRepo("octocat", "Hello-World"),
    ),
]

BAD_REPOS = [
    "https://github.com/none/headerparser.git",
    "https://github.com/joe.coder/hello-world",
    "/repo",
    "none/repo",
    "jwodder/headerparser.git",
    "jwodder/headerparser.GIT",
    "jwodder/headerparser.Git",
    "jwodder/",
    "https://api.github.com/repos/jwodder/headerparser.git",
    "https://api.github.com/repos/jwodder/headerparser.git/",
    "https://api.github.com/repos/jwodder/headerparser/",
    "api.github.com/REPOS/jwodder/headerparser",
    "https://api.github.com/REPOS/jwodder/headerparser",
    "https://user name@github.com/octocat/Hello-World",
    "https://user/name@github.com/octocat/Hello-World",
    "https://user@name@github.com/octocat/Hello-World",
    "my.username@github.com/octocat/Hello-World",
    "my.username@www.github.com/octocat/Hello-World",
    "my.username:hunter2@github.com/octocat/Hello-World",
    "my.username:hunter2@www.github.com/octocat/Hello-World",
    "https://x-access-token:1234567890@api.github.com/repos/octocat/Hello-World",
    "x-access-token:1234567890@github.com/octocat/Hello-World",
    "git@github.com/jwodder/headerparser",
    "git@GITHUB.com:joe-q-coder/my.repo.GIT",
    "GIT@github.com:joe-q-coder/my.repo.git",
    "git@github.com/joe-q-coder/my.repo.git",
    "ssh://git@github.com:jwodder/headerparser",
    "ssh://git@github.com:jwodder/headerparser/",
    "ssh://git@github.com/jwodder/headerparser/",
    "git://github.com/jwodder/headerparser/",
    "SSH://Git@GITHUB.COM/-/test",
    "ssh://GIT@github.com/-/test",
    "https://http://github.com/joe-coder/hello.world",
    "https://github.com/-Jerry-/geshi-1.0.Git",
]


@pytest.mark.parametrize(
    "spec,repo",
    REPO_URLS
    + [
        ("jwodder/headerparser", GHRepo("jwodder", "headerparser")),
        ("headerparser", GHRepo("jwodder", "headerparser")),
        ("jwodder/none", GHRepo("jwodder", "none")),
        ("none", GHRepo("jwodder", "none")),
        ("nonely/headerparser", GHRepo("nonely", "headerparser")),
        ("none-none/headerparser", GHRepo("none-none", "headerparser")),
        ("nonenone/headerparser", GHRepo("nonenone", "headerparser")),
    ],
)
def test_parse(spec: str, repo: GHRepo) -> None:
    assert GHRepo.parse(spec, default_owner="jwodder") == repo


@pytest.mark.parametrize("spec", BAD_REPOS)
def test_parse_bad_spec(spec: str) -> None:
    with pytest.raises(ValueError):
        GHRepo.parse(spec)


@pytest.mark.parametrize("url,repo", REPO_URLS)
def test_parse_url(url: str, repo: GHRepo) -> None:
    assert GHRepo.parse_url(url) == repo


@pytest.mark.parametrize("url", BAD_REPOS)
def test_parse_bad_url(url: str) -> None:
    with pytest.raises(ValueError):
        GHRepo.parse_url(url)


def test_parse_name_only_no_owner() -> None:
    with pytest.raises(ValueError):
        GHRepo.parse("headerparser")


def test_parse_owner_name_no_default_owner() -> None:
    assert GHRepo.parse("jwodder/headerparser") == GHRepo("jwodder", "headerparser")


def test_parse_name_only_callable_owner() -> None:
    assert GHRepo.parse("headerparser", lambda: "jwodder") == GHRepo(
        "jwodder", "headerparser"
    )


def test_parse_owner_name_callable_default_owner() -> None:
    calls: list[int] = []

    def defowner() -> str:
        calls.append(1)
        return "jwodder"

    assert GHRepo.parse("octocat/Hello-World") == GHRepo("octocat", "Hello-World")
    assert calls == []
