"""Who named a run, and whether the server is still allowed to improve it.

Written because `name_customized` was TRUE on all 620 runs in the fleet -- every
run ever created -- which made the flag carry no information and left
`app/generation/kinds/title.py` inert since 0080: it bails on
`name_customized` at read (`:162`) and re-asserts `name_customized = false` in
its UPDATE (`:236`), so a fleet with no false rows is a fleet where the title
kind has never once fired.

The cause was one line in `_run_impl` fabricating `run-<timestamp>` whenever the
caller left the name unset. That is invisible to any assertion on `name` alone --
a fabricated name is a perfectly good-looking string, and after the fix a
slug-named run looks much the same. THE FLAG IS THE ONLY OBSERVABLE THAT TELLS
THE TWO APART, which is why every test here asserts on it.
"""

from __future__ import annotations

import json
import re

from tests.conftest import open_run

#: What the server mints when nobody chose a slug. The fake stands in for a real
#: petname (`weightless-lizard-119`); the shape that matters to these tests is
#: only that it is server-derived, never a timestamp.
_TIMESTAMP_NAME = re.compile(r"^run-\d{8}-\d{6}$")


class TestAnUnnamedRunStaysServerNamed:
    def test_slug_becomes_the_name_and_the_flag_stays_false(self, client):
        """The exact shape Oded's `probe run start --slug ... ` produced.

        He supplied a slug and no name, which the server would have honoured --
        `write_run` binds `name := slug` when `name is None`. The SDK overwrote
        it with a timestamp and stamped the run human-named, permanently.
        """
        run = open_run(client, experiment="e1", slug="inghest-v0-manifest-v1", heartbeat=False)
        row = client.get_run(run.id)
        assert row["name"] == "inghest-v0-manifest-v1"
        assert row["name_customized"] is False

    def test_no_name_and_no_slug_still_leaves_the_flag_false(self, client):
        """Nothing to derive from is not a licence to invent one."""
        run = open_run(client, experiment="e1", heartbeat=False)
        row = client.get_run(run.id)
        assert row["name_customized"] is False
        assert not _TIMESTAMP_NAME.match(row["name"]), (
            f"{row['name']!r} is a fabricated timestamp; the server names unnamed runs"
        )

    def test_the_name_key_is_omitted_from_the_wire_not_sent_as_null(self, client, app):
        """`min_length=1` on the server field makes null and absent different.

        Asserted on the request body rather than the stored row because the fake
        would happily normalise a null away, and then this would pass against a
        client that still sends one.
        """
        open_run(client, experiment="e1", slug="omits-the-key", heartbeat=False)
        creates = [
            r
            for r in app.requests
            if r.method == "POST" and re.search(r"/(experiments|projects)/[^/]+/runs$", r.url.path)
        ]
        assert creates, "no run-create request reached the fake"
        body = json.loads(creates[-1].content)
        assert "name" not in body, f"name should be absent, got {body.get('name')!r}"

    def test_project_direct_runs_take_the_same_door(self, client):
        """122 of 506 fleet runs are project-direct, and they build their body
        through the same `_run_create_body` -- so the fix has to hold on both."""
        project = client.create_project("proj-naming", kind="general")
        run = client.run(project="proj-naming", slug="project-direct-slug", heartbeat=False)
        row = client.get_run(run.id)
        assert row["project_id"] == project["id"]
        assert row["name"] == "project-direct-slug"
        assert row["name_customized"] is False


class TestANamedRunIsFrozenOnPurpose:
    def test_an_explicit_name_still_stamps_the_flag(self, client):
        """The guarantee in title.py: generation never renames what a human named.

        The fix must not overshoot into "the server always picks", or every
        deliberately-named run becomes fair game for a generated title.
        """
        run = open_run(client, experiment="e1", name="inghest geometry validation v1")
        row = client.get_run(run.id)
        assert row["name"] == "inghest geometry validation v1"
        assert row["name_customized"] is True

    def test_a_name_equal_to_the_slug_is_still_a_choice_for_runs(self, client):
        """Runs deliberately differ from projects/experiments here.

        Those two route through `chosen_name()`, which nulls a name equal to the
        slug. Runs never do -- `write_run` keys on `name is None` and nothing
        else -- so passing the slug as the name is a CHOICE, and this is the
        trap in "just make it `name or slug`" as the SDK fix.
        """
        run = open_run(client, experiment="e1", name="same-string", slug="same-string")
        row = client.get_run(run.id)
        assert row["name_customized"] is True
