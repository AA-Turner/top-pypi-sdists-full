"""Board secrets already on disk are removed on load, from every profile (#609).

The CLI stopped *writing* board credentials to ``~/.innoday/config.json`` and
stopped *reading* them from it. Neither helps the machines that already hold
one, and those cannot be reached by hand -- so the cleanup has to happen on
config load: silent, idempotent, and safe on a real user's file.

Four properties, three of which a by-hand audit of one machine got wrong first
and which are therefore each pinned by name below:

1. **Every profile.** The audit cleaned ``dev``, reported done, and left
   ``default`` still holding ``bp -> jira``.
2. **The keyring value, under the owning profile's namespace.** The JSON holds
   a pointer, ``encrypted:<key>``; the secret is in the OS keyring. Dropping
   the pointer alone orphans the secret. And the keyring username is
   profile-prefixed (``CLIConfig._keyring_key``), so purging a ``default``
   entry while running on ``dev`` must still delete
   ``default_<key>`` -- ``self.delete_credential()`` would delete
   ``dev_<key>``, i.e. somebody else's. **Real keyrings hold plenty of
   entries that are not prefixed at all** (#614), so the bare name is tried
   too, and the notice now says what was actually deleted -- see
   ``TestLegacyUnprefixedKeyringEntriesAreRemovedToo`` and
   ``TestTheReportSaysWhatActuallyHappened``.
3. **Nothing unrelated is lost.** This rewrites a file holding identity, org
   list and every profile.
4. **A malformed file must not break CLI startup**, and must not be written
   over.

``keyring`` is patched in every test that could otherwise reach a real
backend: these must not touch the developer's own keyring.
"""

import ast
import json
import os
import stat
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import keyring.errors as keyring_errors
import pytest

from src.cli.config import CLIConfig


@pytest.fixture
def config_path(tmp_path):
    return tmp_path / "config.json"


@pytest.fixture(autouse=True)
def no_real_keyring():
    """Never touch the developer's own keyring, in any test in this module.

    A call-recorder, not a keyring: it accepts every delete and reports the
    name gone afterwards. Good enough for "which names were asked for", and
    that is all the tests using it directly assert.

    It is **not** good enough for anything about *naming*, because the store
    it models has no contents -- every name deletes successfully, so a wrong
    name is indistinguishable from a right one. That is the shape of the
    hole #614 fell through, and `FakeKeyring` below is the fixture that
    closes it.
    """
    with patch("src.cli.config.keyring") as fake:
        fake.delete_password.return_value = None
        fake.get_password.return_value = None
        yield fake


class FakeKeyring:
    """A keyring with actual contents, keyed exactly like the real one.

    `delete_password` raises `PasswordDeleteError` for a name that is not
    there, as every real backend does -- which is what makes a name mismatch
    *visible* rather than silently successful.

    Seeded by writing `entries` directly, never through `CLIConfig`: a
    fixture built by the code under test can only ever agree with it (#614's
    "how it was found").
    """

    def __init__(self, entries=None):
        self.entries = dict(entries or {})
        self.errors = keyring_errors

    def get_password(self, service, username):
        return self.entries.get((service, username))

    def set_password(self, service, username, password):
        self.entries[(service, username)] = password

    def delete_password(self, service, username):
        if (service, username) not in self.entries:
            raise keyring_errors.PasswordDeleteError(username)
        del self.entries[(service, username)]


@pytest.fixture
def fake_keyring():
    """Install a `FakeKeyring`, overriding the module-wide mock."""

    def _install(entries=None):
        fake = FakeKeyring(entries)
        patcher = patch("src.cli.config.keyring", fake)
        patcher.start()
        installed.append(patcher)
        return fake

    installed = []
    try:
        yield _install
    finally:
        for patcher in reversed(installed):
            patcher.stop()


def _write(path, payload):
    path.write_text(json.dumps(payload, indent=2))
    return path


def _both_profiles_hold_a_board_secret():
    """The exact shape observed on the machine that motivated #609: the same
    org carrying a `jira` entry in two different profiles."""
    return {
        "current_profile": "dev",
        "profiles": {
            "default": {
                "organizations": {
                    "bp": {
                        "id": "org-bp",
                        "integrations": {
                            "jira": {
                                "base_url": "https://bp.atlassian.net",
                                "email": "dev@example.com",
                                "api_token": "encrypted:brightpower_jira_api_token",
                            }
                        },
                    }
                },
            },
            "dev": {
                "organizations": {
                    "bp": {
                        "id": "org-bp",
                        "integrations": {
                            "jira": {
                                "email": "dev@example.com",
                                "api_token": "encrypted:bp_jira_api_token",
                            }
                        },
                    }
                },
            },
        },
    }


def _integrations(path, profile, org):
    data = json.loads(path.read_text())
    return data["profiles"][profile]["organizations"][org].get("integrations", {})


class TestEveryProfileIsPurged:
    def test_a_board_secret_in_a_non_active_profile_is_removed_too(self, config_path):
        """The bug an audit of `current_profile` alone would leave behind."""
        _write(config_path, _both_profiles_hold_a_board_secret())

        CLIConfig(config_path=str(config_path), profile="dev")

        assert _integrations(config_path, "dev", "bp") == {}
        assert _integrations(config_path, "default", "bp") == {}

    @pytest.mark.parametrize(
        "board_type,stored",
        [
            ("jira", {"email": "a@b.c", "api_token": "encrypted:o_jira_api_token"}),
            ("trello", {"api_key": "k", "token": "encrypted:o_trello_token"}),
            ("linear", {"token": "encrypted:o_linear_token"}),
            ("notion", {"token": "encrypted:o_notion_token"}),
        ],
    )
    def test_all_four_board_types_are_purged(self, config_path, board_type, stored):
        """Not just the two the wizard wrote. `board sync`'s loop read all
        four, so all four are credentials a sync path could have picked up."""
        _write(
            config_path,
            {
                "current_profile": "default",
                "profiles": {
                    "default": {
                        "organizations": {"o": {"integrations": {board_type: stored}}}
                    }
                },
            },
        )

        CLIConfig(config_path=str(config_path))

        assert _integrations(config_path, "default", "o") == {}

    def test_a_capitalised_board_type_is_purged_too(self, config_path):
        """`"Jira"` is the same secret as `"jira"`.

        These keys are lowercase by convention only -- `_lookup_organization_entry`
        already carries a comment about files written before that convention
        held, or edited by hand. An exact-match purge leaves the capitalised
        one on disk, which is the one shape of survivor nobody would think to
        look for.
        """
        _write(
            config_path,
            {
                "profiles": {
                    "default": {
                        "organizations": {
                            "o": {
                                "integrations": {
                                    "Jira": {"api_token": "encrypted:o_jira_api_token"},
                                    "LINEAR": {"token": "encrypted:o_linear_token"},
                                }
                            }
                        }
                    }
                }
            },
        )

        CLIConfig(config_path=str(config_path))

        assert _integrations(config_path, "default", "o") == {}


class TestTheKeyringValueIsClearedToo:
    def test_the_pointer_is_resolved_under_the_owning_profiles_namespace(
        self, config_path, no_real_keyring
    ):
        """Both halves at once: the keyring is cleared, and each entry is
        cleared under the profile it was found in -- not under the active one.

        With `self.delete_credential()` here (which prefixes
        `self._current_profile`) the `default` entry would be deleted as
        `dev_brightpower_jira_api_token`: a key that does not exist, while the
        real secret stays in the keyring with nothing pointing at it.
        """
        _write(config_path, _both_profiles_hold_a_board_secret())

        CLIConfig(config_path=str(config_path), profile="dev")

        deleted = {call.args for call in no_real_keyring.delete_password.call_args_list}
        assert deleted == {
            ("innoday-cli", "default_brightpower_jira_api_token"),
            ("innoday-cli", "dev_bp_jira_api_token"),
            # ...and the unprefixed name of each, which real keyrings hold
            # (#614). The prefixed name is still tried first and is still the
            # *owning* profile's, which is what this test is about.
            ("innoday-cli", "brightpower_jira_api_token"),
            ("innoday-cli", "bp_jira_api_token"),
        }

    def test_a_plaintext_value_is_not_treated_as_a_keyring_pointer(
        self, config_path, no_real_keyring
    ):
        """Only `encrypted:` values name a keyring entry. `email`/`base_url`
        are stored in the clear and must not be passed to the keyring."""
        _write(
            config_path,
            {
                "current_profile": "default",
                "profiles": {
                    "default": {
                        "organizations": {
                            "o": {
                                "integrations": {
                                    "jira": {
                                        "email": "dev@example.com",
                                        "base_url": "https://x.atlassian.net",
                                        "api_token": "encrypted:o_jira_api_token",
                                    }
                                }
                            }
                        }
                    }
                },
            },
        )

        CLIConfig(config_path=str(config_path))

        deleted = [
            call.args[1] for call in no_real_keyring.delete_password.call_args_list
        ]
        # Both naming conventions for the one pointer (#614), and nothing else:
        # `email`/`base_url` never reach the keyring at all.
        assert deleted == ["default_o_jira_api_token", "o_jira_api_token"]

    def test_a_broken_keyring_backend_does_not_break_cli_startup(
        self, config_path, no_real_keyring
    ):
        """A locked or absent keyring is not a reason for every command to
        fail. The JSON entry still goes."""
        no_real_keyring.delete_password.side_effect = RuntimeError("no backend")
        _write(config_path, _both_profiles_hold_a_board_secret())

        CLIConfig(config_path=str(config_path), profile="dev")

        assert _integrations(config_path, "dev", "bp") == {}
        assert _integrations(config_path, "default", "bp") == {}


SERVICE = "innoday-cli"


def _one_board_secret(pointer="brightpower_jira_api_token", profile="default"):
    """A config holding a single board pointer, in `profile`."""
    return {
        "current_profile": profile,
        "profiles": {
            profile: {
                "organizations": {
                    "bp": {
                        "id": "org-bp",
                        "integrations": {
                            "jira": {
                                "email": "dev@example.com",
                                "api_token": f"encrypted:{pointer}",
                            }
                        },
                    }
                }
            }
        },
    }


class TestLegacyUnprefixedKeyringEntriesAreRemovedToo:
    """The keyring holds two naming conventions, and #610 knew about one.

    Measured on a real machine (existence probed, never read):
    `brightpower_jira_api_token`, `developer_claude_api_key` and
    `haviland-software:github:token` all exist **unprefixed**, while
    `dev_brightpower_jira_api_token` exists prefixed -- the same logical
    secret under both. So the prefix-only delete raised
    `PasswordDeleteError`, the pointer went anyway, the secret stayed, and
    the operator was told it had been removed.

    Every test here seeds `FakeKeyring` **by hand**, with names written out
    in full. That is the point: #610's suite built its keyring with the same
    code that read it, so the naming agreed with itself by construction and
    this mismatch could not appear in any of them.
    """

    def test_a_legacy_unprefixed_secret_is_actually_removed(
        self, config_path, fake_keyring, capsys
    ):
        """The bug. The pointer says `brightpower_jira_api_token`; the keyring
        holds exactly that name and no prefixed variant."""
        keyring = fake_keyring({(SERVICE, "brightpower_jira_api_token"): "s3cret"})
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        assert keyring.entries == {}
        assert "Removed locally-stored jira board credential" in " ".join(
            capsys.readouterr().err.split()
        )

    def test_a_prefixed_secret_is_still_removed(
        self, config_path, fake_keyring, capsys
    ):
        """Trying the bare name may not cost the prefixed one its delete."""
        keyring = fake_keyring(
            {(SERVICE, "default_brightpower_jira_api_token"): "s3cret"}
        )
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        assert keyring.entries == {}
        assert "Removed locally-stored jira board credential" in " ".join(
            capsys.readouterr().err.split()
        )

    def test_both_are_removed_when_the_machine_holds_both(
        self, config_path, fake_keyring
    ):
        """The measured state: one logical secret, two entries. Deleting
        either one alone leaves a live secret behind."""
        keyring = fake_keyring(
            {
                (SERVICE, "brightpower_jira_api_token"): "s3cret",
                (SERVICE, "dev_brightpower_jira_api_token"): "s3cret",
            }
        )
        _write(config_path, _one_board_secret(profile="dev"))

        CLIConfig(config_path=str(config_path), profile="dev")

        assert keyring.entries == {}

    def test_an_unrelated_secret_is_never_touched(self, config_path, fake_keyring):
        """Why trying two names is safe where using the *active* profile is
        not: both candidates carry the same pointer text, so neither can name
        somebody else's secret."""
        keyring = fake_keyring(
            {
                (SERVICE, "brightpower_jira_api_token"): "s3cret",
                (SERVICE, "dev_some_other_api_token"): "keep-me",
                (SERVICE, "innoday_token"): "keep-me-too",
            }
        )
        _write(config_path, _one_board_secret(profile="dev"))

        CLIConfig(config_path=str(config_path), profile="dev")

        assert keyring.entries == {
            (SERVICE, "dev_some_other_api_token"): "keep-me",
            (SERVICE, "innoday_token"): "keep-me-too",
        }


class TestTheReportSaysWhatActuallyHappened:
    """ "Removed" has to mean the secret is gone from this machine.

    Announcing a removal that did not happen is the failure the whole purge
    exists to prevent -- the same shape as the symlink bug #610's review
    caught before merge.
    """

    def test_a_dangling_pointer_is_not_reported_as_a_removal(
        self, config_path, fake_keyring, capsys
    ):
        """Nothing existed under either name. The end state is the one the
        operator wants, so this is reported as a stale entry rather than a
        failure -- but it must not claim a credential was removed."""
        fake_keyring({})
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "Removed a stale jira board credential entry" in err
        assert "nothing was found in the keyring to delete" in err
        assert "Removed locally-stored" not in err

    def test_a_surviving_secret_is_reported_as_a_failure(
        self, config_path, fake_keyring, capsys
    ):
        """A backend whose delete returns quietly and changes nothing.

        This is why the delete is verified with a read instead of trusted:
        #614 was found only because a hand-run delete failed *loudly*, and
        nothing in the code depended on it doing so.
        """
        keyring = fake_keyring({(SERVICE, "brightpower_jira_api_token"): "s3cret"})
        keyring.delete_password = lambda service, username: None
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "could NOT delete its keyring value" in err
        assert "'default_brightpower_jira_api_token' or " in err
        assert "'brightpower_jira_api_token'" in err
        assert "delete it by hand" in err
        assert "Removed locally-stored" not in err
        assert keyring.entries  # the precondition: the secret really survived

    def test_a_delete_that_cannot_be_verified_is_reported_as_a_failure(
        self, config_path, fake_keyring, capsys
    ):
        """The delete did not raise, but the backend will not answer the read.

        Either answer is defensible; this is the one that is pinned, and it is
        the one consistent with the rest of the purge -- "removed" means
        *verified* gone, so a delete nobody can confirm is not a removal. The
        cost is a false alarm on a backend with a flaky read; the alternative
        cost is silence on a backend whose delete quietly did nothing, which
        is #614 itself.
        """
        keyring = fake_keyring({(SERVICE, "brightpower_jira_api_token"): "s3cret"})

        def unreadable(service, username):
            raise RuntimeError("backend will not answer a read")

        keyring.get_password = unreadable
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "could NOT delete its keyring value" in err
        assert "Removed locally-stored" not in err

    def test_a_delete_that_errors_is_reported_as_a_failure(
        self, config_path, fake_keyring, capsys
    ):
        """A locked keyring still must not break startup (the JSON entry
        goes), but it may not be reported as a removal either."""

        def explode(service, username):
            raise RuntimeError("keyring is locked")

        keyring = fake_keyring({(SERVICE, "brightpower_jira_api_token"): "s3cret"})
        keyring.delete_password = explode
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "could NOT delete its keyring value" in err
        assert "Removed locally-stored" not in err
        assert _integrations(config_path, "default", "bp") == {}

    def test_one_stuck_value_makes_the_whole_entry_a_failure(
        self, config_path, fake_keyring, capsys
    ):
        """An entry with several values, only one of which is stuck.

        The aggregation has to be "failed outranks removed", not "the last one
        wins": the stuck value is deleted *first* here, so an aggregation that
        let a later success overwrite it would announce a removal with the
        secret still in the keyring -- #614 verbatim.
        """
        keyring = fake_keyring(
            {
                (SERVICE, "stuck_token"): "s3cret",
                (SERVICE, "clean_token"): "also-secret",
            }
        )
        real_delete = keyring.delete_password

        def delete(service, username):
            if username.endswith("stuck_token"):
                raise RuntimeError("keyring is locked for this one")
            real_delete(service, username)

        keyring.delete_password = delete
        _write(config_path, _one_board_secret())
        # Two pointers in the one integration entry, the stuck one first.
        raw = json.loads(config_path.read_text())
        raw["profiles"]["default"]["organizations"]["bp"]["integrations"]["jira"] = {
            "api_token": "encrypted:stuck_token",
            "refresh_token": "encrypted:clean_token",
        }
        _write(config_path, raw)

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "could NOT delete its keyring value" in err
        assert "Removed locally-stored" not in err
        # The preconditions: one really survived, the other really went.
        assert keyring.entries == {(SERVICE, "stuck_token"): "s3cret"}

    def test_a_machine_with_no_keyring_backend_is_not_a_red_alarm(
        self, config_path, fake_keyring, capsys
    ):
        """`keyring.backends.fail.Keyring` -- a headless box with no Secret
        Service -- raises `NoKeyringError` from every call.

        There is no keyring, so there is no secret on that machine to delete by
        hand. Telling the operator otherwise is the inverse of the bug being
        fixed, in the same message.
        """

        def no_backend(service, username):
            raise keyring_errors.NoKeyringError("no backend available")

        keyring = fake_keyring({})
        keyring.delete_password = no_backend
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "could NOT delete" not in err
        assert "delete it by hand" not in err
        assert "Removed a stale jira board credential entry" in err

    def test_an_unreachable_backend_is_not_reported_as_an_empty_one(
        self, config_path, fake_keyring, capsys
    ):
        """`NoKeyringError` means "no backend answered", not "no secret".

        A headless box genuinely has nothing to delete. A box whose D-Bus is
        down, or whose `PYTHON_KEYRING_BACKEND` is misset, raises the *same*
        exception with the secret still sitting in gnome-keyring. Reporting
        both as "nothing was found in the keyring to delete" is a false
        negative of exactly #614's kind, in the branch added to remove a false
        alarm -- so the wording must claim only that no delete was attempted.
        """

        def no_backend(service, username):
            raise keyring_errors.NoKeyringError("no backend available")

        keyring = fake_keyring({(SERVICE, "brightpower_jira_api_token"): "s3cret"})
        keyring.delete_password = no_backend
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "no keyring backend could be reached" in err
        assert "nothing was deleted there" in err
        assert "nothing was found in the keyring to delete" not in err
        # It has to name what may still be there, or there is nothing to act on.
        assert "'default_brightpower_jira_api_token'" in err
        # The precondition: the secret really did survive.
        assert keyring.entries == {(SERVICE, "brightpower_jira_api_token"): "s3cret"}


class TestTheReportSaysWhatHappenedWhenTheRewriteFails:
    """The write path has to hold the same standard as the keyring path.

    It used to print "removed locally-stored board credentials from the
    keyring, but could not rewrite …" whatever had actually happened -- the
    same false claim #614 is about, sitting next to carefully-worded honest
    ones.

    The write is failed the way `TestTheWriteIsAtomic` does it -- a real
    `OSError` out of `json.dump`, not a patched-out `_write_raw_atomically`.
    """

    def test_it_never_claims_the_keyring_was_cleared(
        self, config_path, fake_keyring, capsys
    ):
        """The literal old wording, in the case where it was false: nothing
        was in the keyring, yet it announced a removal from it. And no alarm
        either -- the entry left behind is a stale pointer, retried next run."""
        fake_keyring({})
        _write(config_path, _one_board_secret())

        with patch(
            "src.cli.config.json.dump",
            side_effect=OSError(28, "No space left on device"),
        ):
            CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "removed locally-stored board credentials from the keyring" not in err
        assert "could not rewrite" in err
        assert "still in the file" in err
        assert "delete it by hand" not in err
        # The precondition: the file really was left holding the entry.
        assert _integrations(config_path, "default", "bp") != {}

    def test_it_says_the_secret_survived_when_the_delete_failed_too(
        self, config_path, fake_keyring, capsys
    ):
        """Nothing changed at all: pointer on disk, secret in the keyring."""
        keyring = fake_keyring({(SERVICE, "brightpower_jira_api_token"): "s3cret"})
        keyring.delete_password = lambda service, username: None
        _write(config_path, _one_board_secret())

        with patch(
            "src.cli.config.json.dump",
            side_effect=OSError(28, "No space left on device"),
        ):
            CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "jira (default profile, org bp) could not be deleted either" in err
        assert "delete it by hand" in err
        assert keyring.entries  # the precondition: the secret really survived


class TestNothingUnrelatedIsLost:
    def _full_config(self):
        return {
            "current_profile": "dev",
            "default_profile": "dev",
            "profiles": {
                "default": {
                    "platform": {"api_url": "http://localhost:9999"},
                    "organizations": {
                        "bp": {
                            "id": "org-bp",
                            "integrations": {
                                "jira": {"api_token": "encrypted:bp_jira_api_token"},
                                "slack": {"bot_token": "xoxb-plain"},
                            },
                        }
                    },
                },
                "dev": {
                    "platform": {"api_url": "https://innoday-dev.example"},
                    "user": {
                        "id": "u-1",
                        "email": "someone@example.com",
                        "name": "Someone",
                    },
                    "organizations": {
                        "hs": {
                            "id": "org-hs",
                            "integrations": {"slack": {"bot_token": "xoxb-hs"}},
                        }
                    },
                },
            },
        }

    def test_only_the_board_entry_is_removed(self, config_path):
        _write(config_path, self._full_config())

        CLIConfig(config_path=str(config_path), profile="dev")

        after = json.loads(config_path.read_text())
        # The board secret is gone...
        assert (
            "jira"
            not in after["profiles"]["default"]["organizations"]["bp"]["integrations"]
        )
        # ...and everything sharing the file with it survived.
        assert after["default_profile"] == "dev"
        assert after["profiles"]["default"]["platform"]["api_url"] == (
            "http://localhost:9999"
        )
        assert after["profiles"]["dev"]["user"] == {
            "id": "u-1",
            "email": "someone@example.com",
            "name": "Someone",
        }
        assert after["profiles"]["dev"]["platform"]["api_url"] == (
            "https://innoday-dev.example"
        )
        assert after["profiles"]["default"]["organizations"]["bp"]["id"] == "org-bp"
        assert after["profiles"]["dev"]["organizations"]["hs"]["id"] == "org-hs"

    def test_a_sibling_non_board_integration_in_the_same_org_survives(
        self, config_path
    ):
        """The narrowest version of the same property: `slack` sits in the
        very `integrations` dict the `jira` entry is popped out of."""
        _write(config_path, self._full_config())

        CLIConfig(config_path=str(config_path), profile="dev")

        assert _integrations(config_path, "default", "bp") == {
            "slack": {"bot_token": "xoxb-plain"}
        }


class TestDeadSecretsArePurgedToo:
    """`github` and `claude` were written by a wizard and read by nothing.

    #609 removed the board half of that and left these two reported-only,
    because deleting somebody's GitHub PAT unasked was not that change's call.
    #729 deletes the wizard that minted them, which settles it: a credential
    with no writer and no reader is not a preference anybody is expressing, it
    is litter with a real secret behind it. They now go the same way a board
    secret does -- entry popped, keyring value cleared, and the notice says
    which.
    """

    def _config_with_dead_secrets(self):
        return {
            "current_profile": "dev",
            "profiles": {
                "dev": {
                    "organizations": {
                        "hs": {
                            "integrations": {
                                "github": {"token": "encrypted:hs_github_token"}
                            }
                        },
                        "developer": {
                            "integrations": {
                                "claude": {"api_key": "encrypted:dev_claude_api_key"}
                            }
                        },
                    }
                }
            },
        }

    def test_they_are_removed_from_the_file(self, config_path, no_real_keyring):
        _write(config_path, self._config_with_dead_secrets())

        CLIConfig(config_path=str(config_path), profile="dev")

        assert _integrations(config_path, "dev", "hs") == {}
        assert _integrations(config_path, "dev", "developer") == {}

    # Four tests were here -- the keyring value being cleared, a capitalised
    # `GitHub`/`Claude` still matching, the #614 "removed" notice not claiming a
    # keyring delete that failed, and idempotency. All four are gone because
    # #729 made `doomed = board_secrets + dead` a single removal pass, so each
    # was re-running one shared code path under a different integration name:
    # the board classes above cover case-folding
    # (`test_a_capitalised_board_type_is_purged_too`), keyring clearing
    # (`TestTheKeyringValueIsClearedToo`), the failure vocabulary
    # (`TestTheReportSaysWhatActuallyHappened`) and idempotency
    # (`test_it_is_idempotent_and_leaves_a_clean_file_untouched`) against the
    # same helpers.
    #
    # What stays here is only what is *different* about the dead half: that
    # `github`/`claude` reach `doomed` at all, and the three surfaces that then
    # describe them. `test_they_are_removed_from_the_file` is the one that dies
    # if somebody narrows `doomed` back to board secrets, which is the
    # regression this class exists for.

    def test_they_are_reported(self, config_path):
        _write(config_path, self._config_with_dead_secrets())

        config = CLIConfig(config_path=str(config_path), profile="dev")

        reported = {
            (e["organization"], e["integration"]) for e in config.dead_local_secrets
        }
        assert reported == {("hs", "github"), ("developer", "claude")}

    def test_the_notice_says_they_were_removed(self, config_path, capsys):
        """On stderr, because this fires during `CLIConfig.__init__` -- see
        `TestNothingReachesStdout`."""
        _write(config_path, self._config_with_dead_secrets())

        CLIConfig(config_path=str(config_path), profile="dev")

        captured = capsys.readouterr()
        err = " ".join(captured.err.split())
        assert "github" in err
        assert "claude" in err
        assert "Removed" in err
        assert captured.out == ""

    def test_config_show_lists_what_went(self, config_path, capsys):
        """The load-time notice is a single stderr line; `config show` is where
        the same entries are laid out properly."""
        _write(config_path, self._config_with_dead_secrets())

        CLIConfig(config_path=str(config_path), profile="dev").display_config()

        out = " ".join(capsys.readouterr().out.split())
        assert "github" in out
        assert "claude" in out


class TestItIsSafeOnARealFile:
    def test_file_permissions_are_preserved(self, config_path):
        """0o640, deliberately, and not 0o600.

        The purge writes through a `tempfile.mkstemp` file, which is created
        0o600 -- so asserting on 0o600 passes whether or not the mode is
        actually carried across, and the test cannot fail. (It was written
        that way first; dropping the `os.chmod` left it green.) 0o640 is a
        mode `mkstemp` will not produce by accident.
        """
        _write(config_path, _both_profiles_hold_a_board_secret())
        os.chmod(config_path, 0o640)

        CLIConfig(config_path=str(config_path), profile="dev")

        assert stat.S_IMODE(config_path.stat().st_mode) == 0o640

    def test_it_is_idempotent_and_leaves_a_clean_file_untouched(self, config_path):
        _write(config_path, _both_profiles_hold_a_board_secret())
        CLIConfig(config_path=str(config_path), profile="dev")

        after_first = config_path.read_text()
        mtime = config_path.stat().st_mtime_ns

        CLIConfig(config_path=str(config_path), profile="dev")

        assert config_path.read_text() == after_first
        # Not rewritten at all -- a purge with nothing to do must not touch
        # the file, or every CLI invocation churns a file other shells read.
        assert config_path.stat().st_mtime_ns == mtime

    def test_an_unparseable_file_is_left_exactly_as_it_was(self, config_path):
        """End-to-end: a damaged file survives CLI startup untouched."""
        original = "{ this is not json"
        config_path.write_text(original)

        CLIConfig(config_path=str(config_path))  # must not raise

        assert config_path.read_text() == original

    def test_the_purge_refuses_to_write_when_the_load_degraded(self, config_path):
        """The `_load_degraded` guard specifically, exercised on its own.

        The test above passes with or without that guard: when the load
        degrades, `_raw` is `DEFAULT_CONFIG`, which holds no board secret, so
        nothing is purged and nothing is written for a second reason. That
        makes it silent coverage of the guard -- so drive the guard directly
        instead, with a `_raw` that *would* be written.

        Why the guard matters: `save()` refuses to overwrite an unreadable
        file because doing so once destroyed a working `dev` profile
        (`test_cli_config_does_not_clobber.py`). A purge that wrote anyway
        would be a second, quieter path to exactly that data loss.
        """
        original = "{ this is not json"
        config_path.write_text(original)

        config = CLIConfig(config_path=str(config_path))
        assert config._load_degraded  # precondition of what follows

        config._raw = {
            "profiles": {
                "default": {
                    "organizations": {
                        "o": {
                            "integrations": {
                                "jira": {"api_token": "encrypted:o_jira_api_token"}
                            }
                        }
                    }
                }
            }
        }
        config._purge_local_board_secrets()

        assert config_path.read_text() == original

    @pytest.mark.parametrize(
        "payload",
        [
            {"profiles": []},
            {"profiles": {"default": "not-a-dict"}},
            {"profiles": {"default": {"organizations": "not-a-dict"}}},
            {"profiles": {"default": {"organizations": {"o": ["not-a-dict"]}}}},
            {"profiles": {"default": {"organizations": {"o": {"integrations": 7}}}}},
            {
                "profiles": {
                    "default": {
                        "organizations": {
                            "o": {"integrations": {"jira": "bare-string"}}
                        }
                    }
                }
            },
        ],
    )
    def test_a_structurally_malformed_file_does_not_raise_at_startup(
        self, config_path, payload
    ):
        """A half-written or hand-edited file is a bad reason for every
        command on the machine to start failing."""
        _write(config_path, payload)

        CLIConfig(config_path=str(config_path))  # must not raise

    def test_a_malformed_board_entry_is_still_removed(self, config_path):
        """Tolerating the shape is not the same as leaving it: a `jira` entry
        that is a bare string is still a board entry, and still goes."""
        _write(
            config_path,
            {
                "profiles": {
                    "default": {
                        "organizations": {
                            "o": {"integrations": {"jira": "bare-string"}}
                        }
                    }
                }
            },
        )

        CLIConfig(config_path=str(config_path))

        assert _integrations(config_path, "default", "o") == {}


class TestNothingReachesStdout:
    """Building a `CLIConfig` must not write a byte to fd 1.

    `src/mcp/server.py` calls `load_config()` at **module scope**, so a
    CLIConfig is constructed during import — and that server speaks JSON-RPC
    over stdio, where stdout **is** the protocol channel (the rule is already
    written down in `src/mcp/server.py`, about blastoff's `print()` calls).
    The purge printed there, so the first start after upgrading emitted three
    lines of prose ahead of the handshake — on precisely the machines the
    purge exists for.

    stderr is safe there and still reaches a human running `innoday`, which is
    what keeps this from becoming a silent credential deletion.

    Every notice on the construction path is covered, not just the purge:
    the degraded-load warning and both stale-default migrations predate #609
    and have the same defect.
    """

    def test_the_purge_notice_goes_to_stderr(self, config_path, capsys):
        _write(config_path, _both_profiles_hold_a_board_secret())

        CLIConfig(config_path=str(config_path), profile="dev")

        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Removed locally-stored jira board credential" in " ".join(
            captured.err.split()
        )

    def test_the_degraded_load_warning_goes_to_stderr(self, config_path, capsys):
        config_path.write_text("{ this is not json")

        CLIConfig(config_path=str(config_path))

        captured = capsys.readouterr()
        assert captured.out == ""
        assert "Could not load config" in captured.err

    def test_the_stale_api_url_migration_goes_to_stderr(self, config_path, capsys):
        _write(
            config_path,
            {
                "profiles": {
                    "default": {"platform": {"api_url": "http://localhost:8002"}}
                }
            },
        )

        CLIConfig(config_path=str(config_path))

        captured = capsys.readouterr()
        assert captured.out == ""
        assert "api_url" in captured.err

    def test_the_dead_block_strip_goes_to_stderr(self, config_path, capsys):
        _write(
            config_path,
            {
                "profiles": {"default": {"session": {"current_thread_id": None}}},
                "platform_server": {"api_port": 8002},
            },
        )

        CLIConfig(config_path=str(config_path))

        captured = capsys.readouterr()
        assert captured.out == ""
        assert "platform_server" in captured.err
        assert "session" in captured.err

    def test_importing_the_mcp_server_prints_nothing_on_stdout(self, tmp_path):
        """The real thing, end to end, in a subprocess.

        In-process assertions above cover each notice; this covers the
        *import*, which is what actually breaks — anything else on that path
        that learns to print would be caught here and nowhere else. The config
        is rigged to fire every notice at once: a board secret to purge, a
        dead secret to purge, a stale api_url to migrate, and a dead
        `platform_server` block to strip.
        """
        home = tmp_path / "home"
        (home / ".innoday").mkdir(parents=True)
        _write(
            home / ".innoday" / "config.json",
            {
                "current_profile": "default",
                "profiles": {
                    "default": {
                        "platform": {"api_url": "http://localhost:8002"},
                        "organizations": {
                            "bp": {
                                "integrations": {
                                    "jira": {
                                        "email": "dev@example.com",
                                        "api_token": "encrypted:pytest_never_a_real_key",
                                    }
                                }
                            },
                            "hs": {
                                "integrations": {
                                    "github": {
                                        "token": "encrypted:pytest_never_a_real_key_2"
                                    }
                                }
                            },
                        },
                    }
                },
                "platform_server": {"api_port": 8002},
            },
        )

        repo_root = Path(__file__).resolve().parents[1]
        env = {
            **os.environ,
            "HOME": str(home),
            "PYTHONPATH": str(repo_root),
            # Never reach a real keyring backend from a subprocess: the purge
            # calls delete_password, and this test must not be able to touch
            # the developer's own keyring.
            "PYTHON_KEYRING_BACKEND": "keyring.backends.null.Keyring",
        }
        env.pop("FORCE_COLOR", None)

        result = subprocess.run(
            [sys.executable, "-c", "import src.mcp.server"],
            cwd=str(repo_root),
            env=env,
            capture_output=True,
            text=True,
            timeout=180,
        )

        assert result.returncode == 0, result.stderr
        assert result.stdout == "", (
            "the MCP server emitted non-JSON on stdout during import; stdio "
            f"transport uses stdout as the JSON-RPC channel:\n{result.stdout}"
        )
        # The precondition: this config really did trigger the purge, so an
        # empty stdout means "routed to stderr" and not "nothing happened".
        assert "Removed locally-stored jira board credential" in " ".join(
            result.stderr.split()
        )


class TestASymlinkedConfigIsWrittenThrough:
    """`~/.innoday/config.json` symlinked into a dotfiles repo is ordinary.

    `os.replace` swaps **the name it is given**. Given the link, it replaces
    the link — so the purge produced four bad outcomes at once: the secret
    survived in the target, the keyring value was deleted anyway (leaving a
    pointer to nothing), the notice said it had been removed, and the
    operator's dotfiles link was silently severed so every later `config set`
    wrote somewhere their repo no longer saw.

    It was also a regression against `main`, where every write to this file
    goes through `save()`'s `open(path, "w")` — which follows the link.
    """

    def _linked(self, tmp_path):
        target = tmp_path / "dotfiles" / "config.json"
        target.parent.mkdir()
        _write(target, _both_profiles_hold_a_board_secret())
        link = tmp_path / "config.json"
        link.symlink_to(target)
        return link, target

    def test_the_secret_is_removed_from_the_link_target(self, tmp_path):
        link, target = self._linked(tmp_path)

        CLIConfig(config_path=str(link), profile="dev")

        # The file that actually holds the bytes, read directly rather than
        # through the link — reading through it would pass even if the link
        # had been replaced by a fresh regular file.
        assert _integrations(target, "dev", "bp") == {}
        assert _integrations(target, "default", "bp") == {}

    def test_the_link_survives_as_a_link(self, tmp_path):
        link, target = self._linked(tmp_path)

        CLIConfig(config_path=str(link), profile="dev")

        assert link.is_symlink()
        assert link.resolve() == target.resolve()

    def test_no_temp_file_is_left_in_either_directory(self, tmp_path):
        link, target = self._linked(tmp_path)

        CLIConfig(config_path=str(link), profile="dev")

        for directory in (link.parent, target.parent):
            leftovers = [p.name for p in directory.iterdir() if ".config-" in p.name]
            assert leftovers == []


class TestTheWriteIsAtomic:
    """Atomicity is the property the "no `.bak`" decision rests on.

    Nothing pinned it: replacing the whole temp-file dance with a plain
    `open(path, "w")` left the suite green (mutation M17 in review), which
    means the design's own justification — "the corruption risk a backup would
    cover is handled by writing atomically instead" — was resting on an
    untested claim about a file holding a user's identity and every profile.

    Note this cannot be satisfied by the same wrong implementation as
    `TestASymlinkedConfigIsWrittenThrough`: the naive direct write follows a
    symlink (so it passes those) and truncates before it can fail (so it fails
    these), while an atomic write on an unresolved path does the reverse.
    """

    def test_a_failure_mid_write_leaves_the_original_byte_identical(self, config_path):
        _write(config_path, _both_profiles_hold_a_board_secret())
        original = config_path.read_bytes()

        with patch(
            "src.cli.config.json.dump",
            side_effect=OSError(28, "No space left on device"),
        ):
            CLIConfig(config_path=str(config_path), profile="dev")  # must not raise

        assert config_path.read_bytes() == original

    def test_a_failed_write_leaves_no_temp_file_behind(self, config_path):
        _write(config_path, _both_profiles_hold_a_board_secret())

        with patch(
            "src.cli.config.json.dump",
            side_effect=OSError(28, "No space left on device"),
        ):
            CLIConfig(config_path=str(config_path), profile="dev")

        leftovers = [
            p.name for p in config_path.parent.iterdir() if p.name != "config.json"
        ]
        assert leftovers == []

    def test_the_real_path_never_holds_a_partial_file(self, config_path):
        """The property directly, rather than by proxy.

        Every write to the config path is observed as it happens; the content
        at that path must go from the old complete JSON to the new complete
        JSON with nothing in between. A non-atomic write shows up here as an
        empty (truncated) read, or as a parse failure.
        """
        _write(config_path, _both_profiles_hold_a_board_secret())
        seen = []

        real_replace = os.replace

        def observing_replace(src, dst):
            seen.append(config_path.read_text())
            real_replace(src, dst)
            seen.append(config_path.read_text())

        with patch("src.cli.config.os.replace", side_effect=observing_replace):
            CLIConfig(config_path=str(config_path), profile="dev")

        assert seen, "the config file was never replaced — nothing was written"
        for snapshot in seen:
            json.loads(snapshot)  # complete JSON at every observed instant
        assert "jira" in seen[0]  # before: the old file, untouched
        assert "jira" not in seen[-1]  # after: the purged file, complete


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permission bits")
class TestAReadOnlyDirectoryChangesNothing:
    """Neither half happens, rather than one half.

    The purge used to delete the keyring values, fail the rewrite, warn, and
    return — leaving a pointer on disk to a secret that no longer existed,
    permanently (the next invocation re-deleted an absent keyring entry and
    re-failed the same write, forever). The file and the keyring now stay
    consistent with each other, and the warning names something the operator
    can actually act on.
    """

    @pytest.fixture
    def read_only_dir(self, tmp_path):
        _write(tmp_path / "config.json", _both_profiles_hold_a_board_secret())
        os.chmod(tmp_path, 0o500)
        try:
            yield tmp_path / "config.json"
        finally:
            os.chmod(tmp_path, 0o700)

    def test_the_keyring_is_not_cleared(self, read_only_dir, no_real_keyring):
        """The keyring half is the only half this code decides.

        There is deliberately no companion assertion that the file still holds
        the entry: with the directory read-only, the file cannot change
        whatever the implementation does, so such a test would pass for a
        reason that has nothing to do with the code and could never go red.
        """
        CLIConfig(config_path=str(read_only_dir), profile="dev")  # must not raise

        no_real_keyring.delete_password.assert_not_called()

    def test_it_says_what_to_do_about_it(self, read_only_dir, capsys):
        CLIConfig(config_path=str(read_only_dir), profile="dev")

        err = " ".join(capsys.readouterr().err.split())
        assert "not writable" in err
        assert "nothing has been removed" in err


class TestConfigShowNeverClaimsARemovalThatDidNotHappen:
    """The `config show` panel is held to the same standard as the notice.

    The panel is titled "Secrets removed from this config file", so it may only
    ever list entries whose removal actually reached disk. On a load that could
    not write, *nothing* was removed: the entry is still in the file and the
    secret is still in the keyring. Announcing it anyway is the #614
    false-claim class on the one surface that had escaped it -- and it is the
    worse half of the pair, because the same invocation's stderr correctly says
    nothing has been removed.
    """

    def _one_dead_secret(self):
        return {
            "current_profile": "dev",
            "profiles": {
                "dev": {
                    "organizations": {
                        "hs": {
                            "integrations": {
                                "github": {"token": "encrypted:hs_github_token"}
                            }
                        }
                    }
                }
            },
        }

    @pytest.mark.skipif(
        os.geteuid() == 0, reason="root ignores directory permission bits"
    )
    def test_a_read_only_directory_lists_nothing_as_removed(
        self, tmp_path, no_real_keyring, capsys
    ):
        config_path = _write(tmp_path / "config.json", self._one_dead_secret())
        os.chmod(tmp_path, 0o500)
        try:
            config = CLIConfig(config_path=str(config_path), profile="dev")
            config.display_config()
        finally:
            os.chmod(tmp_path, 0o700)

        captured = capsys.readouterr()
        assert "nothing has been removed" in " ".join(captured.err.split())
        assert config.dead_local_secrets == []
        assert "Secrets removed" not in captured.out
        assert "github" not in captured.out

    def test_a_failed_write_lists_nothing_as_removed(
        self, config_path, no_real_keyring, capsys
    ):
        """The write failing for any other reason is the same false claim: the
        entry is demonstrably still on disk afterwards."""
        _write(config_path, self._one_dead_secret())

        with patch(
            "src.cli.config.json.dump",
            side_effect=OSError(28, "No space left on device"),
        ):
            config = CLIConfig(config_path=str(config_path), profile="dev")
        config.display_config()

        out = capsys.readouterr().out
        assert _integrations(config_path, "dev", "hs") == {
            "github": {"token": "encrypted:hs_github_token"}
        }
        assert config.dead_local_secrets == []
        assert "Secrets removed" not in out
        assert "github" not in out


def _two_entries_share_one_pointer(pointer="shared_ptr"):
    """One org whose `jira` (purged) and `slack` (kept) name the same secret.

    Not reachable through the wizard that used to write these -- it minted
    `{org}_{type}_{key}`, so the type was always in the name. Reachable in a
    hand-edited or legacy-written file, which is the population this purge is
    aimed at, and which is where #614's entries came from too.
    """
    return {
        "current_profile": "default",
        "profiles": {
            "default": {
                "organizations": {
                    "bp": {
                        "id": "org-bp",
                        "integrations": {
                            "jira": {
                                "email": "dev@example.com",
                                "api_token": f"encrypted:{pointer}",
                            },
                            "slack": {"bot_token": f"encrypted:{pointer}"},
                        },
                    }
                }
            }
        },
    }


class TestASecretASurvivingEntryStillNeedsIsKept:
    """Deleting by pointer text destroys whatever else points at it.

    `_clear_keyring_pointers` reasons that the two candidate names cannot
    "name a different secret" -- true within one logical entry, and false
    across entries. Purging `jira` deleted the value the surviving `slack`
    entry resolved, leaving it dangling: a config that looked intact and a
    credential that had silently stopped working.
    """

    def test_the_keyring_value_survives(self, config_path, fake_keyring):
        keyring = fake_keyring(
            {
                (SERVICE, "default_shared_ptr"): "s3cret",
                (SERVICE, "shared_ptr"): "s3cret",
            }
        )
        _write(config_path, _two_entries_share_one_pointer())

        CLIConfig(config_path=str(config_path))

        assert keyring.entries == {
            (SERVICE, "default_shared_ptr"): "s3cret",
            (SERVICE, "shared_ptr"): "s3cret",
        }

    def test_the_board_entry_still_goes_and_the_other_stays(
        self, config_path, fake_keyring
    ):
        """Keeping the secret is not a licence to keep the board entry: the
        pointer on disk is what #609 is removing, and `slack` is neither a
        board credential nor a dead one this purge removes (#605 owns it)."""
        fake_keyring({(SERVICE, "default_shared_ptr"): "s3cret"})
        _write(config_path, _two_entries_share_one_pointer())

        CLIConfig(config_path=str(config_path))

        assert _integrations(config_path, "default", "bp") == {
            "slack": {"bot_token": "encrypted:shared_ptr"}
        }

    def test_it_says_the_value_was_left_and_why(
        self, config_path, fake_keyring, capsys
    ):
        fake_keyring({(SERVICE, "default_shared_ptr"): "s3cret"})
        _write(config_path, _two_entries_share_one_pointer())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "left its keyring value" in err
        assert "still points at the same secret" in err
        # And must not read as a clean removal, which is what the operator
        # would otherwise take away.
        assert "Removed locally-stored jira board credential (default" not in err

    def test_an_unshared_pointer_beside_it_is_still_deleted(
        self, config_path, fake_keyring
    ):
        """The guard is per pointer, not per file. A second org whose board
        secret nothing else references must not be spared by proximity."""
        raw = _two_entries_share_one_pointer()
        raw["profiles"]["default"]["organizations"]["acme"] = {
            "id": "org-acme",
            "integrations": {"trello": {"api_token": "encrypted:lonely_ptr"}},
        }
        keyring = fake_keyring(
            {
                (SERVICE, "default_shared_ptr"): "s3cret",
                (SERVICE, "default_lonely_ptr"): "other",
            }
        )
        _write(config_path, raw)

        CLIConfig(config_path=str(config_path))

        assert keyring.entries == {(SERVICE, "default_shared_ptr"): "s3cret"}


class TestARewriteAgainstTheFilesOwnState:
    """Two things `os.replace` does that `save()`'s `open(path, "w")` did not.

    Both are decided in favour of writing -- the purge exists because these
    machines cannot be reached by hand, and refusing would leave the secret in
    place and re-warn on every command forever. What was wrong is that neither
    was visible: a `chmod 444` config came back rewritten with its mode intact,
    so nothing about it looked touched.
    """

    def test_a_read_only_file_is_rewritten_and_said_so(
        self, config_path, no_real_keyring, capsys
    ):
        _write(config_path, _one_board_secret())
        os.chmod(config_path, 0o444)
        try:
            CLIConfig(config_path=str(config_path))
        finally:
            os.chmod(config_path, 0o600)

        assert _integrations(config_path, "default", "bp") == {}
        err = " ".join(capsys.readouterr().err.split())
        assert "was read-only" in err
        assert "rewritten anyway" in err

    def test_the_read_only_mode_is_preserved(self, config_path, no_real_keyring):
        """Carried across like any other mode -- which is precisely why the
        notice above is needed: the file afterwards is indistinguishable from
        one that was never written."""
        _write(config_path, _one_board_secret())
        os.chmod(config_path, 0o444)
        try:
            CLIConfig(config_path=str(config_path))
            assert stat.S_IMODE(config_path.stat().st_mode) == 0o444
        finally:
            os.chmod(config_path, 0o600)

    def test_a_hard_linked_file_says_the_link_was_severed(
        self, tmp_path, no_real_keyring, capsys
    ):
        """`os.replace` swaps the name, so the other name keeps the old inode.

        Atomicity is load-bearing (there is no `.bak`, deliberately), so the
        write is not changed to preserve links -- but the operator has to be
        told, because the second name still holds a config whose board pointer
        no longer resolves.
        """
        primary = tmp_path / "config.json"
        _write(primary, _one_board_secret())
        other = tmp_path / "config-dotfiles.json"
        os.link(primary, other)

        CLIConfig(config_path=str(primary))

        assert _integrations(primary, "default", "bp") == {}
        assert json.loads(other.read_text())["profiles"]["default"]["organizations"][
            "bp"
        ]["integrations"].get("jira"), "precondition: the other name kept the old file"
        err = " ".join(capsys.readouterr().err.split())
        assert "hard links" in err
        assert "no longer resolves" in err

    def test_an_ordinary_file_gets_neither_notice(
        self, config_path, no_real_keyring, capsys
    ):
        """The common case stays silent about the write. A notice that fires
        every time is one nobody reads."""
        _write(config_path, _one_board_secret())

        CLIConfig(config_path=str(config_path))

        err = " ".join(capsys.readouterr().err.split())
        assert "read-only" not in err
        assert "hard links" not in err


class TestTheLocalCredentialReaderIsGone:
    def test_get_organization_integration_no_longer_exists(self):
        """Deleted rather than left callerless. Every one of its five callers
        was a sync/register path attaching a laptop-resident board credential
        to a request; a credential reader with no callers is not retired, it
        is dormant, and it reads like existing infrastructure to whoever
        comes next.
        """
        assert not hasattr(CLIConfig, "get_organization_integration")

    def test_add_organization_integration_no_longer_exists(self):
        """The writer goes for the same reason, and the purge needs it to.

        `add_organization_integration` was the only thing that put a
        credential in this file. It used to refuse *board* types and accept
        `github`/`claude`, which is precisely the pair #729 now deletes on
        load -- leaving the writer would mean the next `innoday config
        integrations` run put back what the purge had just removed, forever.
        Its wizard (`config integrations`) went with it.
        """
        assert not hasattr(CLIConfig, "add_organization_integration")

    def test_the_integrations_wizard_is_gone(self):
        from src.cli.commands.config import ConfigCommands

        for name in (
            "_handle_integrations",
            "_configure_github",
            "_configure_slack",
            "_configure_claude",
            "_validate_github_token",
            "_validate_slack_token",
            "_validate_claude_credentials",
        ):
            assert not hasattr(ConfigCommands, name), name

    def test_nothing_under_src_cli_writes_the_integrations_key(self):
        """The wizard was not the only writer.

        `innoday orgs setup` wrote `"integrations": {}` into every new org
        entry -- no credential, but it re-minted the shape #729 set out to
        remove, on a path the purge never cleans (an empty container is left
        alone deliberately). Static, because the alternative is driving the
        whole interactive setup command to observe one dict key.

        **Parsed rather than grepped.** The first version of this test matched
        the literal text `'"integrations":'`, which three of the four ways to
        re-introduce the key walk straight past: `x["integrations"] = {}`,
        single quotes, and `.setdefault("integrations", {})`. Only the exact
        shape that had just been deleted was caught -- the test would have gone
        green against a writer spelled any other way.

        It looks for **writes** specifically, which is what makes it need no
        exemption list. `src/cli/commands/platform.py` reads `"integrations"`
        out of a *health response* and `config.py`'s purge reads it out of the
        config; neither creates the key, so neither is a false positive, and
        nobody has to remember to keep an allowlist accurate.
        """
        cli = Path(__file__).resolve().parents[1] / "src" / "cli"
        KEY = "integrations"

        def _is_key(node) -> bool:
            return isinstance(node, ast.Constant) and node.value == KEY

        offenders = []
        for path in sorted(cli.rglob("*.py")):
            tree = ast.parse(path.read_text(), filename=str(path))
            for node in ast.walk(tree):
                # {"integrations": ...} -- constructs the key outright
                if isinstance(node, ast.Dict) and any(
                    _is_key(k) for k in node.keys if k is not None
                ):
                    offenders.append(f"{path.relative_to(cli)}:{node.lineno} dict")
                # x["integrations"] = ... / += ... / : T = ...
                elif isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
                    targets = (
                        node.targets if isinstance(node, ast.Assign) else [node.target]
                    )
                    for target in targets:
                        if isinstance(target, ast.Subscript) and _is_key(target.slice):
                            offenders.append(
                                f"{path.relative_to(cli)}:{node.lineno} subscript"
                            )
                # x.setdefault("integrations", ...)
                elif (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "setdefault"
                    and node.args
                    and _is_key(node.args[0])
                ):
                    offenders.append(
                        f"{path.relative_to(cli)}:{node.lineno} setdefault"
                    )

        assert offenders == []
