"""Everything a project depends on lines up, or the reader compares shapes.

`projects health` answered the same question in three formats: the database as a
dim suffix on the status line, the GitHub credential as a sentence, and the
boards as a table. A project with one board therefore showed a paragraph above a
single row -- and "is GitHub reachable" and "is Linear reachable" are one
question asked twice, rendered two different ways.
"""

from __future__ import annotations

from src.cli.utils.health_table import health_table, reach_mark, sync_age

HEALTHY = {
    "status": "healthy",
    "database": "connected",
    "github": {"reachable": True, "github_org": "havilandsoftware"},
    "boards": [
        {
            "name": "PixelFuel (PF)",
            "board_type": "linear",
            "reachable": True,
            "latency_ms": 1203,
            "last_sync_age_seconds": 8 * 86400,
        }
    ],
}


def _cells(table):
    return [[str(c) for c in col._cells] for col in table.columns]


class TestOneTableForEveryDependency:
    def test_the_database_and_github_are_rows_beside_the_boards(self):
        names = _cells(health_table(HEALTHY))[0]
        assert names == ["innoday", "havilandsoftware", "PixelFuel (PF)"]

    def test_they_are_ordered_by_how_the_project_fails(self):
        """Without the database nothing else means anything; without GitHub no
        code can be read; a board is the last thing to go. A reader scanning for
        the first ❌ should hit the most fundamental one first."""
        names = _cells(health_table(HEALTHY))[0]
        assert (
            names.index("innoday")
            < names.index("havilandsoftware")
            < names.index("PixelFuel (PF)")
        )

    def test_the_first_column_has_no_header(self):
        """The rows are a database, a credential and some boards. There is no
        honest one-word name for that set, and "Board" was wrong for two of the
        three."""
        assert [c.header for c in health_table(HEALTHY).columns] == [
            "",
            "Type",
            "Reachable",
            "Latency",
            "Last real sync",
        ]

    def test_a_project_with_no_boards_still_gets_a_table(self):
        """It used to return before building one, so the two dependencies that
        always exist were reported only as prose."""
        names = _cells(health_table({**HEALTHY, "boards": []}))[0]
        assert names == ["innoday", "havilandsoftware"]


class TestReachabilityIsThreeValued:
    def test_nothing_proved_is_not_a_failure(self):
        """`None` means probing was skipped, no credential is stored, or the
        budget ran out. Collapsing that into ❌ reports a working board as
        broken."""
        assert "❌" not in reach_mark(None)
        assert "✅" not in reach_mark(None)
        assert "❌" in reach_mark(False)
        assert "✅" in reach_mark(True)

    def test_a_disconnected_database_shows_as_failed(self):
        row = _cells(health_table({**HEALTHY, "database": "disconnected"}))
        assert "❌" in row[2][0]


class TestGitHubSaysWhyWhenItMatters:
    def test_a_refusal_shows_its_reason_rather_than_the_org(self):
        """The organisation name is the useful half on the happy path. When the
        credential was refused, the reason is the only thing worth the column."""
        table = health_table(
            {
                **HEALTHY,
                "github": {
                    "reachable": False,
                    "detail": "401 bad credentials",
                    "github_org": "havilandsoftware",
                },
            }
        )
        assert "401 bad credentials" in _cells(table)[1][1]

    def test_an_unchecked_credential_says_so_rather_than_going_blank(self):
        table = health_table(
            {**HEALTHY, "github": {"reachable": None, "detail": "no credential"}}
        )
        assert "no credential" in _cells(table)[1][1]

    def test_the_happy_path_names_the_organisation(self):
        assert "havilandsoftware" in _cells(health_table(HEALTHY))[0][1]


class TestSyncAge:
    def test_never_synced_is_the_one_age_worth_colouring(self):
        """Every other value is a number whose staleness is the reader's policy:
        a board synced hourly and one synced weekly are both correct."""
        assert "never" in sync_age(None)
        assert sync_age(900) == "15m ago"
        assert sync_age(7200) == "2h ago"
        assert sync_age(8 * 86400) == "8d ago"

    def test_the_boundaries_land_on_the_larger_unit(self):
        """3599s is still minutes and 3600s is an hour -- an off-by-one here
        reads as a board that has not synced in 59 minutes when it just did."""
        assert sync_age(3599) == "59m ago"
        assert sync_age(3600) == "1h ago"
        assert sync_age(86399) == "23h ago"
        assert sync_age(86400) == "1d ago"


class TestTheNumbersWereAlreadyMeasured:
    """A dash beside a row showing `1203ms` is a claim, and it was the wrong one.

    The GitHub probe has always timed its own round trip and repository
    discovery has always recorded when it last ran. The row printed a dash over
    each, which reads as "not applicable to GitHub" — a stronger statement than
    "nobody looked", and not even that, since both had been measured.
    """

    def test_github_shows_the_latency_the_probe_measured(self):
        table = health_table(
            {
                **HEALTHY,
                "github": {
                    "reachable": True,
                    "github_org": "havilandsoftware",
                    "latency_ms": 284,
                },
            }
        )
        assert "284ms" in _cells(table)[3][1]

    def test_github_shows_when_its_repositories_were_last_discovered(self):
        table = health_table(
            {
                **HEALTHY,
                "github": {
                    "reachable": True,
                    "github_org": "havilandsoftware",
                    "last_sync_age_seconds": 6 * 86400,
                },
            }
        )
        assert "6d ago" in _cells(table)[4][1]

    def test_a_project_whose_repositories_never_synced_says_never(self):
        table = health_table(
            {**HEALTHY, "github": {"reachable": True, "github_org": "acme"}}
        )
        assert "never" in _cells(table)[4][1]

    def test_the_database_reports_its_own_round_trip(self):
        """Free -- the query was already being run -- and it is what stops the
        database being the one row with a blank where every other dependency
        has a number."""
        table = health_table({**HEALTHY, "database_latency_ms": 3})
        assert "3ms" in _cells(table)[3][0]

    def test_the_database_has_no_sync_and_says_so_with_a_dash(self):
        """The only dash left in that column, and it means "not a thing" rather
        than "not measured"."""
        cell = _cells(health_table({**HEALTHY, "database_latency_ms": 3}))[4][0]
        assert "never" not in cell and "ago" not in cell


class TestIdentityThenType:
    """Column one says *which*, column two says *what kind* — on every row.

    The GitHub row had them the other way round: `GitHub | BrightPowerSoftware`
    sat above `Bright Power (BPAI) | linear`, so the column naming the board
    named a category for GitHub, and the type column held an account name. Two
    rows of a three-row table disagreeing about what a column means costs more
    than either row gains.
    """

    def test_every_row_types_itself_second(self):
        kinds = _cells(health_table({**HEALTHY, "database_dialect": "postgresql"}))[1]
        assert "postgresql" in kinds[0]
        assert kinds[1:] == ["github", "linear"]

    def test_the_database_types_itself_from_the_live_connection(self):
        """Not a hardcoded "postgres": the fixtures run SQLite, and a health
        table asserting the engine it exists to check would be stating the one
        thing it cannot assume."""
        kinds = _cells(health_table({**HEALTHY, "database_dialect": "sqlite"}))[1]
        assert "sqlite" in kinds[0]

    def test_an_unknown_dialect_falls_back_without_lying(self):
        assert "database" in _cells(health_table(HEALTHY))[1][0]

    def test_a_github_failure_keeps_the_type_and_adds_the_reason(self):
        """The reason used to replace the type. It now joins it, so the column
        still answers "what kind of thing is this" on the row where something
        has gone wrong."""
        cell = _cells(
            health_table(
                {
                    **HEALTHY,
                    "github": {
                        "reachable": False,
                        "detail": "401 bad credentials",
                        "github_org": "havilandsoftware",
                    },
                }
            )
        )[1][1]
        assert "github" in cell and "401 bad credentials" in cell
