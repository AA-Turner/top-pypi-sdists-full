import re
import pytest
from ghrepo import GH_REPO_RGX, GH_USER_RGX


@pytest.mark.parametrize(
    "name",
    [
        "steven-universe",
        "steven",
        "s",
        "s-u",
        "7152",
        "s-t-e-v-e-n",
        "s-t-eeeeee-v-e-n",
        "peridot-2F5L-5XG",
        "nonely",
        "none-one",
        "none-none",
        "nonenone",
        "none0",
        "0none",
        # The following are actual usernames on GitHub that violate the current
        # username restrictions:
        "-",
        "-Jerry-",
        "-SFT-Clan",
        "123456----",
        "FirE-Fly-",
        "None-",
        "alex--evil",
        "johan--",
        "pj_nitin",
        "up_the_irons",
    ],
)
def test_good_users(name: str) -> None:
    assert bool(re.fullmatch(GH_USER_RGX, name))


@pytest.mark.parametrize(
    "name",
    [
        "steven.universe",
        "steven-universe@beachcity.dv",
        "steven-univerß",
        "",
        "none",
        "NONE",
    ],
)
def test_bad_users(name: str) -> None:
    assert re.fullmatch(GH_USER_RGX, name) is None


@pytest.mark.parametrize(
    "repo",
    [
        "steven-universe",
        "steven",
        "s",
        "s-u",
        "7152",
        "s-t-e-v-e-n",
        "s-t-eeeeee-v-e-n",
        "peridot-2F5L-5XG",
        "...",
        "-steven",
        "steven-",
        "-steven-",
        "steven.universe",
        "steven_universe",
        "steven--universe",
        "s--u",
        "git.steven",
        "steven.git.txt",
        "steven.gitt",
        ".gitt",
        "..gitt",
        "...gitt",
        "git",
        "-",
        "_",
        "---",
        ".---",
        ".steven",
        "..steven",
        "...steven",
    ],
)
def test_good_repos(repo: str) -> None:
    assert bool(re.fullmatch(GH_REPO_RGX, repo))


@pytest.mark.parametrize(
    "repo",
    [
        "steven-univerß",
        ".",
        "..",
        "...git",
        "..git",
        ".git",
        "",
        "steven.git",
        "steven.GIT",
        "steven.Git",
    ],
)
def test_bad_repos(repo: str) -> None:
    assert re.fullmatch(GH_REPO_RGX, repo) is None
