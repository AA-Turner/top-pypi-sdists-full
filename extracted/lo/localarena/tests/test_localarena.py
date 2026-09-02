from __future__ import annotations

import copy
import json
import math
import sys
import unittest
from dataclasses import FrozenInstanceError

from localarena import (
    SCHEMA_VERSION,
    Arena,
    Contestant,
    Match,
    Result,
    Standing,
    expected_score,
    round_robin,
)


class ResultTests(unittest.TestCase):
    def test_result_is_a_string_enum_with_portable_values(self) -> None:
        self.assertEqual(SCHEMA_VERSION, 1)
        self.assertEqual([result.value for result in Result], ["left", "right", "draw"])
        self.assertIsInstance(Result.LEFT, str)
        self.assertEqual(str(Result.DRAW), "draw")
        self.assertEqual(json.dumps(Result.RIGHT), '"right"')


class ExpectedScoreTests(unittest.TestCase):
    def test_expected_score_uses_standard_elo_formula(self) -> None:
        self.assertEqual(expected_score(1000, 1000), 0.5)
        self.assertAlmostEqual(expected_score(1400, 1000), 10 / 11)
        self.assertAlmostEqual(
            expected_score(1250, 900) + expected_score(900, 1250),
            1,
        )

    def test_expected_score_is_stable_for_extreme_finite_ratings(self) -> None:
        self.assertEqual(expected_score(1e308, -1e308), 1)
        self.assertEqual(expected_score(-1e308, 1e308), 0)
        self.assertEqual(expected_score(1000, 1000 + (308 * 400)), 0)
        self.assertGreater(expected_score(1000, 1000 + (307 * 400)), 0)

    def test_expected_score_rejects_invalid_numbers(self) -> None:
        for value in (True, "1000", None, math.inf, -math.inf, math.nan):
            with self.subTest(value=value):
                with self.assertRaises((TypeError, ValueError)):
                    expected_score(value, 1000)  # type: ignore[arg-type]


class RoundRobinTests(unittest.TestCase):
    def test_schedule_preserves_order_and_swaps_orientation(self) -> None:
        self.assertEqual(
            round_robin(["b", "a", "c"], rounds=3),
            (
                ("b", "a"),
                ("b", "c"),
                ("a", "c"),
                ("a", "b"),
                ("c", "b"),
                ("c", "a"),
                ("b", "a"),
                ("b", "c"),
                ("a", "c"),
            ),
        )

    def test_schedule_accepts_one_shot_iterables(self) -> None:
        self.assertEqual(
            round_robin((name for name in ["a", "b"])),
            (("a", "b"),),
        )
        self.assertEqual(round_robin([]), ())
        self.assertEqual(round_robin(["solo"]), ())

    def test_schedule_validates_names_uniqueness_and_rounds(self) -> None:
        invalid_calls = (
            lambda: round_robin(["a", "a"]),
            lambda: round_robin(["a", " "]),
            lambda: round_robin("ab"),
            lambda: round_robin(["a", "b"], rounds=0),
            lambda: round_robin(["a", "b"], rounds=True),
            lambda: round_robin(["a", "b"], rounds=2**53),
        )
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises((TypeError, ValueError)):
                    call()


class ArenaConstructionTests(unittest.TestCase):
    def test_constructor_requires_an_explicit_collection(self) -> None:
        with self.assertRaises(TypeError):
            Arena()  # type: ignore[call-arg]

    def test_constructor_accepts_names_or_name_metadata_mapping(self) -> None:
        from_names = Arena(name for name in ["a", "b"])
        self.assertEqual([item.name for item in from_names.contestants], ["a", "b"])

        from_mapping = Arena(
            {
                "a": {"family": "small"},
                "b": None,
            },
            initial_rating=1200,
            k_factor=24,
        )
        self.assertEqual(len(from_mapping), 2)
        self.assertEqual(from_mapping.initial_rating, 1200)
        self.assertEqual(from_mapping.k_factor, 24)
        self.assertEqual(from_mapping.contestants[0].metadata["family"], "small")

    def test_add_registers_a_contestant_and_rejects_duplicates(self) -> None:
        arena = Arena([])
        contestant = arena.add("alpha", {"size": 7})
        self.assertIsInstance(contestant, Contestant)
        self.assertEqual(arena.rating("alpha"), 1000)
        with self.assertRaises(ValueError):
            arena.add("alpha")

    def test_names_and_configuration_are_strongly_validated(self) -> None:
        invalid_calls = (
            lambda: Arena([""]),
            lambda: Arena(["   "]),
            lambda: Arena(["a", "a"]),
            lambda: Arena("ab"),
            lambda: Arena(None),  # type: ignore[arg-type]
            lambda: Arena([], initial_rating=True),
            lambda: Arena([], initial_rating=math.nan),
            lambda: Arena([], k_factor=0),
            lambda: Arena([], k_factor=-1),
            lambda: Arena([], k_factor=math.inf),
        )
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises((TypeError, ValueError)):
                    call()

    def test_unknown_rating_has_a_clear_error(self) -> None:
        with self.assertRaisesRegex(KeyError, "unknown contestant"):
            Arena([]).rating("missing")


class MetadataSafetyTests(unittest.TestCase):
    def test_metadata_is_copied_and_recursively_immutable(self) -> None:
        source = {
            "nested": [{"value": 1}],
            "tuple": ("x", "y"),
        }
        arena = Arena({"alpha": source})
        source["nested"][0]["value"] = 99
        source["tuple"] = ("changed",)

        metadata = arena.contestants[0].metadata
        self.assertEqual(metadata["nested"][0]["value"], 1)  # type: ignore[index]
        self.assertEqual(metadata["tuple"], ("x", "y"))
        with self.assertRaises(TypeError):
            metadata["new"] = True  # type: ignore[index]
        with self.assertRaises(TypeError):
            metadata["nested"][0]["value"] = 2  # type: ignore[index]

    def test_public_records_are_frozen_and_deepcopy_safe(self) -> None:
        arena = Arena(["a", "b"])
        match = arena.record("a", "b", Result.LEFT, {"tags": ["one"]})
        standing = arena.standings()[0]

        with self.assertRaises(FrozenInstanceError):
            match.left = "b"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            standing.rating = 0  # type: ignore[misc]
        cloned = copy.deepcopy(match)
        self.assertEqual(cloned, match)
        self.assertEqual(cloned.metadata["tags"], ("one",))

    def test_snapshot_returns_detached_mutable_json_data(self) -> None:
        arena = Arena({"a": {"nested": [{"value": 1}]}, "b": {}})
        arena.record("a", "b", "draw", {"note": {"value": 2}})
        snapshot = arena.snapshot()

        snapshot["contestants"][0]["metadata"]["nested"][0]["value"] = 99  # type: ignore[index]
        snapshot["matches"][0]["metadata"]["note"]["value"] = 99  # type: ignore[index]
        fresh = arena.snapshot()
        self.assertEqual(
            fresh["contestants"][0]["metadata"]["nested"][0]["value"],  # type: ignore[index]
            1,
        )
        self.assertEqual(
            fresh["matches"][0]["metadata"]["note"]["value"],  # type: ignore[index]
            2,
        )

    def test_metadata_requires_portable_json_values(self) -> None:
        invalid_metadata = (
            [],
            {1: "non-string key"},
            {"value": object()},
            {"value": math.nan},
            {"value": math.inf},
            {"value": 2**53},
            {"value": float(2**53)},
        )
        for metadata in invalid_metadata:
            with self.subTest(metadata=metadata):
                arena = Arena([])
                with self.assertRaises((TypeError, ValueError)):
                    arena.add("a", metadata)  # type: ignore[arg-type]
                self.assertEqual(len(arena), 0)

        circular: dict[str, object] = {}
        circular["self"] = circular
        with self.assertRaises(ValueError):
            Arena({"a": circular})


class MatchAndStandingsTests(unittest.TestCase):
    def test_record_updates_ratings_and_returns_sequential_match_ids(self) -> None:
        arena = Arena(["a", "b"])
        first = arena.record("a", "b", Result.LEFT)
        self.assertEqual(first.id, 1)
        self.assertEqual(arena.rating("a"), 1016)
        self.assertEqual(arena.rating("b"), 984)
        self.assertEqual(arena.rating("a") + arena.rating("b"), 2000)

        second = arena.record("b", "a", "draw")
        self.assertEqual(second.id, 2)
        self.assertEqual(second.result, Result.DRAW)
        self.assertEqual(arena.history(), arena.matches)
        self.assertEqual(len(arena.matches), 2)

    def test_custom_configuration_controls_elo_updates(self) -> None:
        arena = Arena(["a", "b"], initial_rating=1500, k_factor=20)
        arena.record("a", "b", "right")
        self.assertEqual(arena.rating("a"), 1490)
        self.assertEqual(arena.rating("b"), 1510)

    def test_non_finite_rating_update_is_rejected_atomically(self) -> None:
        arena = Arena(
            ["a", "b"],
            initial_rating=sys.float_info.max,
            k_factor=sys.float_info.max,
        )
        before = arena.snapshot()
        with self.assertRaises(OverflowError):
            arena.record("a", "b", "left")
        self.assertEqual(arena.snapshot(), before)

    def test_standings_are_sorted_and_include_complete_stats(self) -> None:
        arena = Arena(["beta", "alpha", "gamma"])
        initial = arena.standings()
        self.assertEqual([row.name for row in initial], ["alpha", "beta", "gamma"])
        self.assertEqual([row.rank for row in initial], [1, 2, 3])

        arena.record("alpha", "beta", "left")
        rows = arena.standings()
        self.assertEqual([row.name for row in rows], ["alpha", "gamma", "beta"])
        alpha = rows[0]
        beta = rows[-1]
        self.assertEqual(
            (
                alpha.matches,
                alpha.played,
                alpha.wins,
                alpha.losses,
                alpha.draws,
                alpha.score,
            ),
            (1, 1, 1, 0, 0, 1),
        )
        self.assertEqual(
            (
                beta.matches,
                beta.played,
                beta.wins,
                beta.losses,
                beta.draws,
                beta.score,
            ),
            (1, 1, 0, 1, 0, 0),
        )
        self.assertEqual(arena.leaderboard(), rows)

    def test_invalid_record_is_atomic(self) -> None:
        arena = Arena(["a", "b"])
        before = arena.snapshot()
        invalid_calls = (
            lambda: arena.record("a", "missing", "left"),
            lambda: arena.record("a", "a", "left"),
            lambda: arena.record("a", "b", "win"),
            lambda: arena.record("a", "b", "left", {"bad": object()}),
        )
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises((KeyError, TypeError, ValueError)):
                    call()
                self.assertEqual(arena.snapshot(), before)

    def test_public_record_constructors_validate_their_invariants(self) -> None:
        with self.assertRaises(ValueError):
            Match(0, "a", "b", Result.LEFT)
        with self.assertRaises(ValueError):
            Match(1, "a", "a", Result.LEFT)
        with self.assertRaises(ValueError):
            Standing(
                rank=1,
                name="a",
                rating=1000,
                wins=1,
                losses=0,
                draws=0,
                matches=2,
            )


class BradleyTerryTests(unittest.TestCase):
    def test_batch_ratings_are_order_invariant_for_a_cycle(self) -> None:
        matches = [
            ("a", "b", Result.LEFT),
            ("a", "c", Result.RIGHT),
            ("b", "c", Result.LEFT),
        ]
        forward = Arena(["a", "b", "c"])
        reverse = Arena(["a", "b", "c"])
        for match in matches:
            forward.record(*match)
        for match in reversed(matches):
            reverse.record(*match)

        self.assertNotEqual(forward.standings(), reverse.standings())
        forward_rows = forward.bradley_terry(
            bootstrap_samples=64,
            seed=42,
        )
        reverse_rows = reverse.bradley_terry(
            bootstrap_samples=64,
            seed=42,
        )
        self.assertEqual(forward_rows, reverse_rows)
        self.assertEqual([row["rank"] for row in forward_rows], [1, 1, 1])
        self.assertEqual(
            [row["rating"] for row in forward_rows],
            [1000.0, 1000.0, 1000.0],
        )
        self.assertTrue(all(row["inconclusive"] for row in forward_rows))

    def test_confidence_bounds_separate_strong_evidence(self) -> None:
        arena = Arena(["a", "b"])
        for index in range(40):
            if index % 2:
                result = Result.RIGHT if index < 30 else Result.LEFT
                arena.record("b", "a", result)
            else:
                result = Result.LEFT if index < 30 else Result.RIGHT
                arena.record("a", "b", result)

        before = arena.snapshot()
        rows = arena.bradley_terry(
            confidence=0.95,
            bootstrap_samples=256,
            seed=7,
        )
        self.assertEqual(arena.snapshot(), before)
        self.assertEqual([row["name"] for row in rows], ["a", "b"])
        self.assertEqual([row["rank"] for row in rows], [1, 2])
        self.assertTrue(
            rows[0]["confidence_lower"] > rows[1]["confidence_upper"]
        )
        self.assertEqual([row["matches"] for row in rows], [40, 40])
        self.assertEqual([row["component"] for row in rows], [1, 1])
        self.assertFalse(any(row["inconclusive"] for row in rows))
        self.assertAlmostEqual(
            rows[0]["rating"] + rows[1]["rating"],
            2000,
        )

    def test_one_match_remains_inconclusive(self) -> None:
        arena = Arena(["a", "b"])
        arena.record("a", "b", Result.LEFT)

        rows = arena.bradley_terry(
            bootstrap_samples=256,
            seed=11,
        )

        self.assertTrue(all(row["inconclusive"] for row in rows))
        self.assertLessEqual(
            rows[0]["confidence_lower"],
            rows[1]["confidence_upper"],
        )
        self.assertLessEqual(
            rows[1]["confidence_lower"],
            rows[0]["confidence_upper"],
        )

    def test_sparse_chain_fit_converges_to_the_closed_form(self) -> None:
        size = 100
        arena = Arena([str(index) for index in range(size)])
        for index in range(size - 1):
            arena.record(str(index), str(index + 1), Result.LEFT)

        rows = arena.bradley_terry(
            bootstrap_samples=2,
            seed=3,
        )

        expected_top = 1000 + (
            ((size - 1) / 2) * 400 * math.log10(3)
        )
        by_name = {row["name"]: row for row in rows}
        self.assertLess(
            abs(by_name["0"]["rating"] - expected_top),
            0.02,
        )

    def test_disconnected_components_are_visible_and_not_globally_ranked(
        self,
    ) -> None:
        arena = Arena(["solo", "d", "c", "b", "a"])
        for _ in range(6):
            arena.record("a", "b", Result.LEFT)
            arena.record("c", "d", Result.RIGHT)

        rows = arena.bradley_terry(bootstrap_samples=32, seed=9)
        by_name = {row["name"]: row for row in rows}
        self.assertEqual(by_name["a"]["component"], 1)
        self.assertEqual(by_name["b"]["component"], 1)
        self.assertEqual(by_name["c"]["component"], 2)
        self.assertEqual(by_name["d"]["component"], 2)
        self.assertEqual(by_name["solo"]["component"], 3)
        self.assertEqual(by_name["solo"]["rank"], 1)
        self.assertEqual(by_name["solo"]["rating"], 1000)
        self.assertEqual(by_name["solo"]["confidence_lower"], 1000)
        self.assertEqual(by_name["solo"]["confidence_upper"], 1000)
        self.assertEqual(by_name["solo"]["matches"], 0)
        self.assertTrue(all(row["inconclusive"] for row in rows))

    def test_task_cluster_bootstrap_does_not_treat_pair_rows_as_independent(
        self,
    ) -> None:
        def interval_width(repetitions: int) -> float:
            arena = Arena(["a", "b"])
            for task_id, result in (
                ("one", Result.LEFT),
                ("two", Result.RIGHT),
            ):
                for _ in range(repetitions):
                    arena.record(
                        "a",
                        "b",
                        result,
                        {
                            "localarena": {
                                "kind": "task-score",
                                "task_id": task_id,
                            }
                        },
                    )
            row = arena.bradley_terry(
                bootstrap_samples=128,
                seed=11,
            )[0]
            return (
                float(row["confidence_upper"])
                - float(row["confidence_lower"])
            )

        self.assertGreaterEqual(interval_width(10), interval_width(1))

    def test_options_are_validated_and_empty_arena_is_supported(self) -> None:
        self.assertEqual(
            Arena([]).bradley_terry(bootstrap_samples=2),
            (),
        )
        arena = Arena(["a"])
        invalid_calls = (
            lambda: arena.bradley_terry(confidence=True),
            lambda: arena.bradley_terry(confidence=0),
            lambda: arena.bradley_terry(confidence=1),
            lambda: arena.bradley_terry(bootstrap_samples=True),
            lambda: arena.bradley_terry(bootstrap_samples=1),
            lambda: arena.bradley_terry(seed=True),
            lambda: arena.bradley_terry(seed=-1),
            lambda: arena.bradley_terry(seed=2**32),
        )
        for call in invalid_calls:
            with self.subTest(call=call):
                with self.assertRaises((TypeError, ValueError)):
                    call()


class NextPairTests(unittest.TestCase):
    def test_next_pair_uses_documented_deterministic_priority(self) -> None:
        arena = Arena(["c", "b", "a"])
        self.assertEqual(arena.next_pair(), ("a", "b"))

        arena.record("b", "a", "left")
        self.assertEqual(arena.next_pair(), ("a", "c"))

        arena.record("a", "c", "draw")
        self.assertEqual(arena.next_pair(), ("b", "c"))

        arena.record("c", "b", "right")
        self.assertEqual(arena.next_pair(), ("a", "b"))

    def test_next_pair_returns_none_for_fewer_than_two_contestants(self) -> None:
        self.assertIsNone(Arena([]).next_pair())
        self.assertIsNone(Arena(["only"]).next_pair())


class SnapshotTests(unittest.TestCase):
    def make_arena(self) -> Arena:
        arena = Arena(
            {
                "α": {"family": "one", "nested": [1, {"ok": True}]},
                "beta": {"family": "two"},
            },
            initial_rating=1200,
            k_factor=24,
        )
        arena.record("α", "beta", "left", {"prompt": "café"})
        arena.add("later", {"registered": "after-match"})
        arena.record("later", "α", "draw")
        return arena

    def test_snapshot_has_exact_schema_v1_shape(self) -> None:
        snapshot = self.make_arena().snapshot()
        self.assertEqual(
            list(snapshot),
            [
                "schema_version",
                "initial_rating",
                "k_factor",
                "contestants",
                "matches",
            ],
        )
        self.assertEqual(snapshot["schema_version"], 1)
        self.assertEqual(snapshot["initial_rating"], 1200)
        self.assertEqual(snapshot["k_factor"], 24)
        self.assertEqual(
            list(snapshot["contestants"][0]),  # type: ignore[index]
            ["name", "metadata"],
        )
        self.assertEqual(
            list(snapshot["matches"][0]),  # type: ignore[index]
            ["id", "left", "right", "result", "metadata"],
        )
        self.assertEqual(
            [match["id"] for match in snapshot["matches"]],  # type: ignore[union-attr]
            [1, 2],
        )
        self.assertEqual(
            [item["name"] for item in snapshot["contestants"]],  # type: ignore[union-attr]
            ["beta", "later", "α"],
        )

    def test_snapshot_and_json_roundtrips_replay_history(self) -> None:
        arena = self.make_arena()
        from_snapshot = Arena.from_snapshot(arena.snapshot())
        payload = arena.to_json()
        from_json = Arena.from_json(payload)

        self.assertNotIn("\\u03b1", payload)
        self.assertNotIn(" ", payload)
        for restored in (from_snapshot, from_json):
            self.assertEqual(restored.snapshot(), arena.snapshot())
            self.assertEqual(restored.standings(), arena.standings())
            self.assertEqual(restored.rating("α"), arena.rating("α"))

    def test_pretty_json_is_supported_and_validated(self) -> None:
        arena = Arena(["a"])
        self.assertIn("\n", arena.to_json(indent=2))
        with self.assertRaises(TypeError):
            arena.to_json(indent=True)
        with self.assertRaises(ValueError):
            arena.to_json(indent=-1)

    def test_from_snapshot_rejects_invalid_schema_data(self) -> None:
        valid = Arena(["a", "b"]).snapshot()

        cases: list[dict[str, object]] = []

        missing = copy.deepcopy(valid)
        del missing["matches"]
        cases.append(missing)

        extra = copy.deepcopy(valid)
        extra["extra"] = True
        cases.append(extra)

        wrong_version = copy.deepcopy(valid)
        wrong_version["schema_version"] = 2
        cases.append(wrong_version)

        wrong_contestants = copy.deepcopy(valid)
        wrong_contestants["contestants"] = {}
        cases.append(wrong_contestants)

        duplicate = copy.deepcopy(valid)
        duplicate["contestants"].append({"name": "a", "metadata": {}})  # type: ignore[union-attr]
        cases.append(duplicate)

        unknown_contestant = copy.deepcopy(valid)
        unknown_contestant["matches"] = [
            {
                "id": 1,
                "left": "a",
                "right": "missing",
                "result": "left",
                "metadata": {},
            }
        ]
        cases.append(unknown_contestant)

        bad_id = copy.deepcopy(valid)
        bad_id["matches"] = [
            {
                "id": 2,
                "left": "a",
                "right": "b",
                "result": "left",
                "metadata": {},
            }
        ]
        cases.append(bad_id)

        bad_result = copy.deepcopy(valid)
        bad_result["matches"] = [
            {
                "id": 1,
                "left": "a",
                "right": "b",
                "result": "win",
                "metadata": {},
            }
        ]
        cases.append(bad_result)

        extra_match_field = copy.deepcopy(valid)
        extra_match_field["matches"] = [
            {
                "id": 1,
                "left": "a",
                "right": "b",
                "result": "draw",
                "metadata": {},
                "unexpected": 1,
            }
        ]
        cases.append(extra_match_field)

        for snapshot in cases:
            with self.subTest(snapshot=snapshot):
                with self.assertRaises((KeyError, TypeError, ValueError)):
                    Arena.from_snapshot(snapshot)

    def test_from_json_is_strict(self) -> None:
        valid_tail = (
            '"initial_rating":1000,"k_factor":32,'
            '"contestants":[],"matches":[]}'
        )
        duplicate = '{"schema_version":1,"schema_version":1,' + valid_tail
        nonstandard = '{"schema_version":NaN,' + valid_tail
        trailing = '{"schema_version":1,' + valid_tail + " trailing"

        for payload in (duplicate, nonstandard, trailing, "[]"):
            with self.subTest(payload=payload):
                with self.assertRaises((TypeError, ValueError)):
                    Arena.from_json(payload)

        with self.assertRaises(TypeError):
            Arena.from_json(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
