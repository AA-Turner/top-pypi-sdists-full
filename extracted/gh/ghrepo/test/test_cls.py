from ghrepo import GHRepo


def test_stringification() -> None:
    r = GHRepo("octocat", "repository")
    assert str(r) == "octocat/repository"


def test_api_url() -> None:
    r = GHRepo("octocat", "repository")
    assert r.api_url == "https://api.github.com/repos/octocat/repository"
    assert GHRepo.parse_url(r.api_url) == r


def test_clone_url() -> None:
    r = GHRepo("octocat", "repository")
    assert r.clone_url == "https://github.com/octocat/repository.git"
    assert GHRepo.parse_url(r.clone_url) == r


def test_git_url() -> None:
    r = GHRepo("octocat", "repository")
    assert r.git_url == "git://github.com/octocat/repository.git"
    assert GHRepo.parse_url(r.git_url) == r


def test_html_url() -> None:
    r = GHRepo("octocat", "repository")
    assert r.html_url == "https://github.com/octocat/repository"
    assert GHRepo.parse_url(r.html_url) == r


def test_ssh_url() -> None:
    r = GHRepo("octocat", "repository")
    assert r.ssh_url == "git@github.com:octocat/repository.git"
    assert GHRepo.parse_url(r.ssh_url) == r
