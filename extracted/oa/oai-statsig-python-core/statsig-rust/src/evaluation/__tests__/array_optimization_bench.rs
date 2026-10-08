//! Synthetic full-function benchmark, not an end-to-end CPU savings estimate.
//! Run with `cargo test -p oai-statsig-rust --release --features testing --lib
//! benchmark_array_optimizations -- --ignored --nocapture --test-threads=1`.
//! Construction, mmap loading, and parity checks are outside timed regions.
//! STATSIG_ARRAY_BENCH_SCOPE=all (default, alias general) times the original
//! general corpus; small, large, membership, and equality select its subsets.
//! small requires both arrays <=128 items. Supplemental medium-boundary cases
//! are timed only with scope=medium, alongside the general 64/64 membership cases.
//! Medium uses 4ms samples; STATSIG_ARRAY_BENCH_SAMPLE_US may override that only
//! in medium scope, subject to a 40s nominal sample budget. Use
//! STATSIG_ARRAY_BENCH_FILTER to narrow case names for longer samples. Repeat
//! runs as separate invocations of the same compiled binary. Every fixture,
//! including medium cases, passes parity/expected checks before any timing.

use rusty_fork::rusty_fork_test;
use serde_json::{Value, json};
use std::{
    collections::{BTreeMap, BTreeSet},
    hint::black_box,
    time::{Duration, Instant},
};

use crate::{
    DynamicValue,
    evaluation::{
        comparisons::compare_arrays,
        evaluator_value::{
            EvaluatorValue, EvaluatorValueInner, EvaluatorValueRef, EvaluatorValueType,
            MemoizedEvaluatorValue,
        },
    },
    interned_values::{
        InternedStore,
        interned_store::{preload_mmap_v2_for_test, write_mmap_v2_for_test},
        mmap_data_v2::ArchivedMmapEvaluatorValueType,
    },
    specs_response::spec_types::ConditionOperator,
    user::user_value::{UserValue, UserValueRef},
};

const BASELINE_COMMIT: &str = "60c94705fda0334ce12af9cfc57e64595a8251f1";
const SAMPLES: usize = 5;
const SAMPLE_TIME: Duration = Duration::from_millis(1);
const MEDIUM_SAMPLE_TIME: Duration = Duration::from_millis(4);
const MEDIUM_SAMPLE_BUDGET_US: u128 = 40_000_000;
const MAX_ITERATIONS: usize = 1 << 20;
const ARRAY_OPS: [ConditionOperator; 4] = [
    ConditionOperator::ArrayContainsAny,
    ConditionOperator::ArrayContainsNone,
    ConditionOperator::ArrayContainsAll,
    ConditionOperator::NotArrayContainsAll,
];

// Full historical membership function from 60c94705fda0334ce12af9cfc57e64595a8251f1.
// Only module nesting/formatting differs; preserve its generic call boundary.
mod before {
    use crate::{
        evaluation::evaluator_value::EvaluatorValueRef,
        specs_response::spec_types::ConditionOperator, unwrap_or_return,
        user::user_value::UserValueRef,
    };
    use ahash::AHashSet;

    pub(crate) fn compare_arrays<'a>(
        value: UserValueRef<'_>,
        target_value: impl Into<EvaluatorValueRef<'a>>,
        op: ConditionOperator,
    ) -> bool {
        let target_value = target_value.into();
        unwrap_or_return!(target_value.array_len(), false);
        let value_len = unwrap_or_return!(value.array_len(), false);
        let value_set: AHashSet<&str> = AHashSet::from_iter((0..value_len).map(|index| {
            value
                .array_item(index)
                .and_then(UserValueRef::string_value)
                .unwrap_or_default()
        }));

        let short_circuit = target_value.any_array_string(false, |item| match op {
            ConditionOperator::ArrayContainsAll => !value_set.contains(item),
            ConditionOperator::ArrayContainsAny => value_set.contains(item),
            ConditionOperator::ArrayContainsNone => value_set.contains(item),
            ConditionOperator::NotArrayContainsAll => !value_set.contains(item),
            _ => true,
        });

        match op {
            ConditionOperator::ArrayContainsAll => !short_circuit,
            ConditionOperator::ArrayContainsAny => short_circuit,
            ConditionOperator::ArrayContainsNone => !short_circuit,
            ConditionOperator::NotArrayContainsAll => short_circuit,
            _ => false,
        }
    }
}

// Historical equality methods keep their self-based helper boundaries. The
// legacy_ names avoid private inherent-method collisions; bodies and annotations
// otherwise match the parent. The trait is benchmark-only.
trait BeforeEvaluatorValue {
    fn legacy_all_array_entries(self, predicate: impl FnMut(&str, usize, &str) -> bool) -> bool;
    fn legacy_all_object_entries(self, predicate: impl FnMut(&str, &str) -> bool) -> bool;
    fn legacy_value_type(self) -> EvaluatorValueType;
    fn legacy_is_equal_to_user_value(self, other: UserValueRef<'_>) -> bool;
}

impl BeforeEvaluatorValue for EvaluatorValueRef<'_> {
    fn legacy_all_array_entries(
        self,
        mut predicate: impl FnMut(&str, usize, &str) -> bool,
    ) -> bool {
        match self {
            Self::Owned(value) => value.array_value.as_ref().is_some_and(|array| {
                array.iter().all(|(lowercase, (index, original))| {
                    predicate(lowercase.as_str(), *index, original.as_str())
                })
            }),
            Self::Mmap(value, _) => value.array_value.as_ref().is_some_and(|array| {
                array.iter().all(|(lowercase, entry)| {
                    let Some(lowercase) = InternedStore::get_mmap_string(lowercase.to_native())
                    else {
                        return false;
                    };
                    let Some(original) = InternedStore::get_mmap_string(entry.1.to_native()) else {
                        return false;
                    };
                    predicate(lowercase, entry.0.to_native() as usize, original)
                })
            }),
        }
    }

    fn legacy_all_object_entries(self, mut predicate: impl FnMut(&str, &str) -> bool) -> bool {
        match self {
            Self::Owned(value) => value.object_value.as_ref().is_some_and(|object| {
                object
                    .iter()
                    .all(|(key, value)| predicate(key.as_str(), value.value.as_str()))
            }),
            Self::Mmap(value, _) => value.object_value.as_ref().is_some_and(|object| {
                object.iter().all(|(key, value)| {
                    let Some(key) = InternedStore::get_mmap_string(key.to_native()) else {
                        return false;
                    };
                    let Some(value) = InternedStore::get_mmap_string(value.to_native()) else {
                        return false;
                    };
                    predicate(key, value)
                })
            }),
        }
    }

    fn legacy_value_type(self) -> EvaluatorValueType {
        match self {
            Self::Owned(value) => value.value_type,
            Self::Mmap(value, _) => match value.value_type {
                ArchivedMmapEvaluatorValueType::Null => EvaluatorValueType::Null,
                ArchivedMmapEvaluatorValueType::Bool => EvaluatorValueType::Bool,
                ArchivedMmapEvaluatorValueType::Number => EvaluatorValueType::Number,
                ArchivedMmapEvaluatorValueType::String => EvaluatorValueType::String,
                ArchivedMmapEvaluatorValueType::Array => EvaluatorValueType::Array,
                ArchivedMmapEvaluatorValueType::Object => EvaluatorValueType::Object,
            },
        }
    }

    fn legacy_is_equal_to_user_value(self, other: UserValueRef<'_>) -> bool {
        match self.legacy_value_type() {
            EvaluatorValueType::Null => other.is_null(),
            EvaluatorValueType::Bool => self.bool_value() == other.bool_value(),
            EvaluatorValueType::Number => self.float_value() == other.float_value(),
            EvaluatorValueType::String => self.string_value() == other.string_value(),
            EvaluatorValueType::Array => {
                let Some(len) = self.array_len() else {
                    return other.array_len().is_none();
                };
                if other.array_len() != Some(len) {
                    return false;
                }
                self.legacy_all_array_entries(|_, index, expected| {
                    other.array_item(index).and_then(UserValueRef::string_value) == Some(expected)
                })
            }
            EvaluatorValueType::Object => {
                let Some(len) = self.object_len() else {
                    return other.object_len().is_none();
                };
                if other.object_len() != Some(len) {
                    return false;
                }
                self.legacy_all_object_entries(|key, expected| {
                    other.object_get(key).and_then(UserValueRef::string_value) == Some(expected)
                })
            }
        }
    }
}

#[derive(Clone, Copy, Debug)]
enum Kernel {
    Membership(ConditionOperator),
    Equality,
}

#[inline(never)]
fn production_membership(
    value: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    op: ConditionOperator,
) -> bool {
    compare_arrays(value, target, op)
}

#[inline(never)]
fn legacy_membership(
    value: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    op: ConditionOperator,
) -> bool {
    before::compare_arrays(value, target, op)
}

#[inline(never)]
fn production_equality(value: UserValueRef<'_>, target: EvaluatorValueRef<'_>) -> bool {
    target.is_equal_to_user_value(value)
}

#[inline(never)]
fn legacy_equality(value: UserValueRef<'_>, target: EvaluatorValueRef<'_>) -> bool {
    target.legacy_is_equal_to_user_value(value)
}

// These dispatchers are only used by the untimed parity pass. The timed paths
// select membership/equality before entering run_iterations and its clock.
fn production(value: UserValueRef<'_>, target: EvaluatorValueRef<'_>, kernel: Kernel) -> bool {
    match kernel {
        Kernel::Membership(op) => production_membership(value, target, op),
        Kernel::Equality => production_equality(value, target),
    }
}

fn legacy(value: UserValueRef<'_>, target: EvaluatorValueRef<'_>, kernel: Kernel) -> bool {
    match kernel {
        Kernel::Membership(op) => legacy_membership(value, target, op),
        Kernel::Equality => legacy_equality(value, target),
    }
}

struct Fixture {
    name: String,
    value: Value,
    target: Value,
    kind: FixtureKind,
}

#[derive(Clone, Copy)]
enum FixtureKind {
    AllMembership,
    MediumMembership,
    Equality,
}

impl Fixture {
    fn kernels(&self) -> Vec<Kernel> {
        match self.kind {
            FixtureKind::Equality => vec![Kernel::Equality],
            FixtureKind::AllMembership | FixtureKind::MediumMembership => {
                ARRAY_OPS.into_iter().map(Kernel::Membership).collect()
            }
        }
    }

    fn is_small(&self) -> bool {
        self.value.as_array().map_or(0, Vec::len) <= 128
            && self.target.as_array().map_or(0, Vec::len) <= 128
    }

    fn selected(&self, scope: &str, filter: &str) -> bool {
        if !self.name.contains(filter) {
            return false;
        }
        if scope == "medium" {
            return matches!(self.kind, FixtureKind::MediumMembership)
                || (matches!(self.kind, FixtureKind::AllMembership)
                    && self.value.as_array().map(Vec::len) == Some(64)
                    && self.target.as_array().map(Vec::len) == Some(64));
        }
        // Keep the general corpus's timing budget stable; supplemental cases
        // still participate in the unconditional parity pass in every scope.
        if matches!(self.kind, FixtureKind::MediumMembership) {
            return false;
        }
        match scope {
            "all" | "general" => true,
            "small" => self.is_small(),
            "large" => !self.is_small(),
            "membership" => matches!(self.kind, FixtureKind::AllMembership),
            "equality" => matches!(self.kind, FixtureKind::Equality),
            _ => unreachable!(),
        }
    }

    // Independent, untimed JSON oracle: target normalization retains the last
    // original spelling/index for each lowercase key. No evaluator helpers or
    // measured implementation participate in constructing expected outcomes.
    fn expected(&self, kernel: Kernel) -> bool {
        let Some(entries) = target_entries(&self.target) else {
            assert!(matches!(kernel, Kernel::Membership(_)));
            return false;
        };
        let Some(items) = self.value.as_array() else {
            return false;
        };
        match kernel {
            Kernel::Membership(op) => {
                let strings: BTreeSet<_> = items
                    .iter()
                    .map(|item| user_text(item).unwrap_or_default())
                    .collect();
                let any = entries.values().any(|(_, value)| strings.contains(value));
                let all = entries.values().all(|(_, value)| strings.contains(value));
                match op {
                    ConditionOperator::ArrayContainsAny => any,
                    ConditionOperator::ArrayContainsNone => !any,
                    ConditionOperator::ArrayContainsAll => all,
                    ConditionOperator::NotArrayContainsAll => !all,
                    _ => unreachable!(),
                }
            }
            Kernel::Equality => {
                items.len() == entries.len()
                    && entries.values().all(|(index, expected)| {
                        items.get(*index).and_then(user_text).as_deref() == Some(expected.as_str())
                    })
            }
        }
    }
}

fn user_text(value: &Value) -> Option<String> {
    match value {
        Value::Null | Value::Object(_) => None,
        Value::String(value) => Some(value.clone()),
        Value::Number(value) => {
            // These synthetic fixtures intentionally avoid float formatting
            // differences between target JSON text and user numeric coercion.
            assert!(value.is_i64() || value.is_u64());
            Some(value.to_string())
        }
        value => Some(value.to_string()),
    }
}

fn target_entries(target: &Value) -> Option<BTreeMap<String, (usize, String)>> {
    Some(
        target
            .as_array()?
            .iter()
            .enumerate()
            .map(|(index, value)| {
                let original = value
                    .as_str()
                    .map_or_else(|| value.to_string(), str::to_owned);
                (original.to_lowercase(), (index, original))
            })
            .collect(),
    )
}

fn ids(start: usize, len: usize) -> Value {
    // Synthetic mixed-case IDs require distinct original/lowercase mmap strings.
    json!(
        (start..start + len)
            .map(|i| format!("Org-0000000000000000{i:08x}"))
            .collect::<Vec<_>>()
    )
}

fn fixtures() -> Vec<Fixture> {
    const MISS_BASE: usize = 1_000_000;
    let mut fixtures = Vec::new();
    // Dense small crossovers include empty and singleton on either side. Empty
    // inputs have explicit labels; overlap means Any may hit while All can fail.
    for user_len in [0, 1, 2, 3, 4, 5, 8, 16] {
        for target_len in [0, 1, 2, 3, 4, 5, 8, 16] {
            let cases: &[(&str, usize)] = if user_len == 0 || target_len == 0 {
                &[("empty", 0)]
            } else {
                &[("overlap", 0), ("miss", MISS_BASE)]
            };
            for &(case, start) in cases {
                fixtures.push(Fixture {
                    name: format!("crossover-{case}-u{user_len}-t{target_len}"),
                    value: ids(start, user_len),
                    target: ids(0, target_len),
                    kind: FixtureKind::AllMembership,
                });
            }
        }
    }
    // Additional small-list boundaries. (8,4) and (8,5) already occur in
    // the dense grid above, so these pairs add only previously missing rows.
    for (user_len, target_len) in [(6, 5), (6, 6), (7, 4), (7, 5), (8, 9), (9, 8), (9, 9)] {
        for (case, start) in [("overlap", 0), ("miss", MISS_BASE)] {
            fixtures.push(Fixture {
                name: format!("small-list-boundary-{case}-u{user_len}-t{target_len}"),
                value: ids(start, user_len),
                target: ids(0, target_len),
                kind: FixtureKind::AllMembership,
            });
        }
    }
    // Small-array cutoff: dense user counts around four and target
    // counts around sixteen. T16 overlap/miss already exist in the grid above.
    for user_len in [3, 4, 5] {
        for target_len in [15, 16, 17] {
            for case in ["overlap", "miss", "late-hit"] {
                if target_len == 16 && case != "late-hit" {
                    continue;
                }
                let mut value = ids(if case == "overlap" { 0 } else { MISS_BASE }, user_len);
                if case == "late-hit" {
                    value[user_len - 1] = ids(0, 1)[0].clone();
                }
                fixtures.push(Fixture {
                    name: format!("cutoff-{case}-u{user_len}-t{target_len}"),
                    value,
                    target: ids(0, target_len),
                    kind: FixtureKind::AllMembership,
                });
            }
        }
    }
    for (user_len, target_len) in [
        (4, 64),
        (4, 6_735),
        (4, 9_033),
        (9_033, 1),
        (9_033, 8),
        (64, 64),
    ] {
        for (case, start) in [("overlap", 0), ("miss", MISS_BASE)] {
            fixtures.push(Fixture {
                name: format!("membership-{case}-u{user_len}-t{target_len}"),
                value: ids(start, user_len),
                target: ids(0, target_len),
                kind: FixtureKind::AllMembership,
            });
        }
    }
    // Late refers to position in the USER array, not randomized target-map
    // iteration order. Existing overlap cases put a matching user first.
    for (user_len, target_len) in [
        (2, 1),
        (3, 1),
        (4, 1),
        (8, 1),
        (16, 1),
        (4, 4),
        (8, 8),
        (16, 16),
        (9_033, 1),
        (9_033, 8),
        (4, 9_033),
    ] {
        let mut value = ids(MISS_BASE, user_len);
        value[user_len - 1] = ids(0, 1)[0].clone();
        fixtures.push(Fixture {
            name: format!("membership-late-hit-u{user_len}-t{target_len}"),
            value,
            target: ids(0, target_len),
            kind: FixtureKind::AllMembership,
        });
    }
    for len in [1, 2, 3, 4, 8, 16, 32, 64] {
        for (case, start) in [("overlap", 0), ("miss", MISS_BASE)] {
            for (family, value, target) in [
                (
                    "numeric",
                    json!((start..start + len).collect::<Vec<_>>()),
                    json!((0..len).collect::<Vec<_>>()),
                ),
                (
                    "unicode",
                    json!(
                        (start..start + len)
                            .map(|i| format!("É{i}"))
                            .collect::<Vec<_>>()
                    ),
                    json!((0..len).map(|i| format!("É{i}")).collect::<Vec<_>>()),
                ),
            ] {
                fixtures.push(Fixture {
                    name: format!("{family}-{case}-u{len}-t{len}"),
                    value,
                    target,
                    kind: FixtureKind::AllMembership,
                });
            }
        }
    }
    for len in [4, 16] {
        let mut numeric = json!((MISS_BASE..MISS_BASE + len).collect::<Vec<_>>());
        numeric[len - 1] = json!(0);
        let mut unicode = json!(
            (MISS_BASE..MISS_BASE + len)
                .map(|i| format!("É{i}"))
                .collect::<Vec<_>>()
        );
        unicode[len - 1] = json!("É0");
        for (family, value, target) in [
            ("numeric", numeric, json!((0..len).collect::<Vec<_>>())),
            (
                "unicode",
                unicode,
                json!((0..len).map(|i| format!("É{i}")).collect::<Vec<_>>()),
            ),
        ] {
            fixtures.push(Fixture {
                name: format!("{family}-late-hit-u{len}-t{len}"),
                value,
                target,
                kind: FixtureKind::AllMembership,
            });
        }
    }
    // Numeric misses immediately around the bounded scratch-array limits.
    for (user_len, target_len) in [(16, 32), (17, 32), (16, 33), (17, 33)] {
        fixtures.push(Fixture {
            name: format!("numeric-small-list-boundary-miss-u{user_len}-t{target_len}"),
            value: json!((MISS_BASE..MISS_BASE + user_len).collect::<Vec<_>>()),
            target: json!((0..target_len).collect::<Vec<_>>()),
            kind: FixtureKind::AllMembership,
        });
    }
    // Expensive-key threshold boundaries and fallback after three ASCII misses.
    // Every numeric miss exceeds ALL target sizes, including future small-list
    // additions; Unicode families are deliberately disjoint.
    for target_len in [15, 16, 17, 31, 32, 63, 64, 128] {
        assert!(target_len < MISS_BASE);
        for (name, value, target) in [
            (
                "numeric-ratio-miss",
                json!((MISS_BASE..MISS_BASE + 4).collect::<Vec<_>>()),
                json!((0..target_len).collect::<Vec<_>>()),
            ),
            (
                "unicode-ratio-miss",
                json!((0..4).map(|i| format!("É{i}")).collect::<Vec<_>>()),
                json!((0..target_len).map(|i| format!("À{i}")).collect::<Vec<_>>()),
            ),
            (
                "numeric-late-key-miss",
                json!(["absent-a", "absent-b", "absent-c", MISS_BASE]),
                json!((0..target_len).collect::<Vec<_>>()),
            ),
            (
                "unicode-late-key-miss",
                json!(["absent-a", "absent-b", "absent-c", "É100"]),
                json!((0..target_len).map(|i| format!("À{i}")).collect::<Vec<_>>()),
            ),
        ] {
            fixtures.push(Fixture {
                name: format!("{name}-u4-t{target_len}"),
                value,
                target,
                kind: FixtureKind::AllMembership,
            });
        }
    }
    for (name, value, target) in [
        (
            "duplicate-heavy-all-possible-u16-t2",
            json!(
                (0..16)
                    .map(|i| if i % 2 == 0 { "a" } else { "b" })
                    .collect::<Vec<_>>()
            ),
            json!(["a", "b"]),
        ),
        (
            "duplicate-heavy-all-impossible-u16-t2",
            json!(vec!["a"; 16]),
            json!(["a", "b"]),
        ),
        (
            "numeric-middle-key-miss-u4-t16",
            json!(["absent-a", MISS_BASE, "absent-c", "absent-d"]),
            json!((0..16).collect::<Vec<_>>()),
        ),
        ("invalid-user-object", json!({"not": "an array"}), ids(0, 8)),
        (
            "invalid-target-object",
            ids(0, 8),
            json!({"not": "an array"}),
        ),
        ("invalid-user-null-empty-target", json!(null), json!([])),
        ("invalid-user-object-empty-target", json!({}), json!([])),
        ("invalid-target-null", ids(0, 8), json!(null)),
        ("invalid-target-string", ids(0, 8), json!("not-an-array")),
        (
            "mixed-entries",
            json!([null, {}, "", true, 42]),
            json!([null, {}, "", true, 42]),
        ),
        (
            "duplicate-spellings",
            json!(["Foo", "foo", "", null]),
            json!(["Foo", "foo", ""]),
        ),
        (
            "duplicate-singleton-target",
            json!(["a"]),
            json!(["a", "a"]),
        ),
        ("boolean-overlap", json!([false, true]), json!([true])),
        ("boolean-miss", json!([false]), json!([true])),
    ] {
        fixtures.push(Fixture {
            name: name.into(),
            value,
            target,
            kind: FixtureKind::AllMembership,
        });
    }
    for len in [0, 1, 2, 3, 4, 5, 8, 16, 32, 64, 128, 256, 9_033] {
        let cases: &[&str] = if len == 0 {
            &["empty-equal", "length-mismatch"]
        } else {
            &[
                "equal",
                "first-mismatch",
                "last-mismatch",
                "length-mismatch",
            ]
        };
        for &case in cases {
            let mut value = ids(0, len);
            match case {
                "first-mismatch" => value[0] = json!("Different-value"),
                "last-mismatch" => value[len - 1] = json!("Different-value"),
                "length-mismatch" => value = ids(0, len + 1),
                _ => {}
            }
            fixtures.push(Fixture {
                name: format!("equality-{case}-n{len}"),
                value,
                target: ids(0, len),
                kind: FixtureKind::Equality,
            });
        }
    }
    for (name, value, target) in [
        ("equality-malformed-user", json!({}), json!(["a"])),
        (
            "equality-mixed-entries",
            json!([null, {}, true, 42]),
            json!([null, {}, true, 42]),
        ),
        (
            "equality-duplicate-spellings",
            json!(["Foo", "foo"]),
            json!(["Foo", "foo"]),
        ),
    ] {
        fixtures.push(Fixture {
            name: name.into(),
            value,
            target,
            kind: FixtureKind::Equality,
        });
    }
    fixtures.extend(medium_fixtures());
    fixtures
}

// Supplemental cases are timed only in medium scope, keeping the original
// general corpus within its fixed timeout. All scopes still validate them.
fn medium_fixtures() -> Vec<Fixture> {
    const MISS_BASE: usize = 1_000_000;
    let mut fixtures = Vec::new();
    for user_len in [63, 64, 65] {
        for target_len in [63, 64, 65] {
            // Four balanced numeric/Unicode cases already exist in general.
            if user_len == 64 && target_len == 64 {
                continue;
            }
            for (case, start) in [("overlap", 0), ("miss", MISS_BASE)] {
                for (family, value, target) in [
                    (
                        "numeric",
                        json!((start..start + user_len).collect::<Vec<_>>()),
                        json!((0..target_len).collect::<Vec<_>>()),
                    ),
                    (
                        "unicode",
                        json!(
                            (start..start + user_len)
                                .map(|i| format!("É{i}"))
                                .collect::<Vec<_>>()
                        ),
                        json!((0..target_len).map(|i| format!("É{i}")).collect::<Vec<_>>()),
                    ),
                ] {
                    fixtures.push(Fixture {
                        name: format!("medium-{family}-{case}-u{user_len}-t{target_len}"),
                        value,
                        target,
                        kind: FixtureKind::MediumMembership,
                    });
                }
            }
        }
    }
    for (position, index) in [("first", 0), ("middle", 32), ("last", 63)] {
        for (family, key, target) in [
            (
                "numeric",
                json!(MISS_BASE),
                json!((0..64).collect::<Vec<_>>()),
            ),
            (
                "unicode",
                json!(format!("É{MISS_BASE}")),
                json!((0..64).map(|i| format!("É{i}")).collect::<Vec<_>>()),
            ),
        ] {
            let mut value = json!((0..64).map(|i| format!("absent-{i}")).collect::<Vec<_>>());
            value[index] = key;
            fixtures.push(Fixture {
                name: format!("medium-{family}-{position}-key-miss-u64-t64"),
                value,
                target,
                kind: FixtureKind::MediumMembership,
            });
        }
    }
    for (case, key) in [("overlap", 0), ("miss", MISS_BASE)] {
        for (family, value, target) in [
            (
                "numeric",
                json!(vec![key; 64]),
                json!((0..64).collect::<Vec<_>>()),
            ),
            (
                "unicode",
                json!(vec![format!("É{key}"); 64]),
                json!((0..64).map(|i| format!("É{i}")).collect::<Vec<_>>()),
            ),
        ] {
            fixtures.push(Fixture {
                name: format!("medium-{family}-duplicate-heavy-{case}-u64-t64"),
                value,
                target,
                kind: FixtureKind::MediumMembership,
            });
        }
    }
    for (user_len, target_len) in [(64, 127), (64, 128), (64, 129), (65, 128)] {
        fixtures.push(Fixture {
            name: format!("medium-numeric-miss-u{user_len}-t{target_len}"),
            value: json!((MISS_BASE..MISS_BASE + user_len).collect::<Vec<_>>()),
            target: json!((0..target_len).collect::<Vec<_>>()),
            kind: FixtureKind::MediumMembership,
        });
    }
    assert_eq!(fixtures.len(), 46);
    fixtures
}

fn run_iterations(mut run: impl FnMut() -> bool, iterations: usize) -> Duration {
    let started = Instant::now();
    for _ in 0..iterations {
        black_box(run());
    }
    started.elapsed()
}

fn calibrated_iterations(mut run: impl FnMut(usize) -> Duration, sample_time: Duration) -> usize {
    let mut iterations = 1;
    loop {
        let elapsed = run(iterations);
        if elapsed >= Duration::from_micros(150) || iterations == MAX_ITERATIONS {
            let ratio = sample_time.as_secs_f64() / elapsed.as_secs_f64().max(1e-9);
            return ((iterations as f64 * ratio) as usize).clamp(1, MAX_ITERATIONS);
        }
        iterations = (iterations * 2).min(MAX_ITERATIONS);
    }
}

fn median(mut samples: [f64; SAMPLES]) -> f64 {
    samples.sort_by(f64::total_cmp);
    samples[SAMPLES / 2]
}

fn benchmark_row(
    value: UserValueRef<'_>,
    target: EvaluatorValueRef<'_>,
    kernel: Kernel,
    label: &str,
    row: usize,
    sample_time: Duration,
) {
    let new = |iterations| match kernel {
        Kernel::Membership(op) => run_iterations(
            || production_membership(black_box(value), black_box(target), black_box(op)),
            iterations,
        ),
        Kernel::Equality => run_iterations(
            || production_equality(black_box(value), black_box(target)),
            iterations,
        ),
    };
    let old = |iterations| match kernel {
        Kernel::Membership(op) => run_iterations(
            || legacy_membership(black_box(value), black_box(target), black_box(op)),
            iterations,
        ),
        Kernel::Equality => run_iterations(
            || legacy_equality(black_box(value), black_box(target)),
            iterations,
        ),
    };
    let new_iterations = calibrated_iterations(new, sample_time);
    let old_iterations = calibrated_iterations(old, sample_time);
    let mut new_samples = [0.0; SAMPLES];
    let mut old_samples = [0.0; SAMPLES];
    for sample in 0..SAMPLES {
        let (new_time, old_time) = if (row + sample).is_multiple_of(2) {
            (new(new_iterations), old(old_iterations))
        } else {
            let old_time = old(old_iterations);
            (new(new_iterations), old_time)
        };
        new_samples[sample] = new_time.as_secs_f64() * 1e9 / new_iterations as f64;
        old_samples[sample] = old_time.as_secs_f64() * 1e9 / old_iterations as f64;
    }
    let production_ns = median(new_samples);
    let legacy_ns = median(old_samples);
    let production_samples = new_samples
        .iter()
        .map(|ns| format!("{ns:.3}"))
        .collect::<Vec<_>>()
        .join(",");
    let legacy_samples = old_samples
        .iter()
        .map(|ns| format!("{ns:.3}"))
        .collect::<Vec<_>>()
        .join(",");
    println!(
        "array_optimization {label} kernel={kernel:?} samples={SAMPLES} production_ns={production_ns:.3} legacy_ns={legacy_ns:.3} speedup={:.3} production_iters={new_iterations} legacy_iters={old_iterations} production_samples_ns={production_samples} legacy_samples_ns={legacy_samples} first={}",
        legacy_ns / production_ns,
        if row.is_multiple_of(2) {
            "production"
        } else {
            "legacy"
        },
    );
}

rusty_fork_test! {
    #![rusty_fork(timeout_ms = 55_000)]
    #[test]
    #[ignore = "manual release benchmark; run --release --ignored --nocapture"]
    fn benchmark_array_optimizations() {
        if cfg!(debug_assertions) {
            eprintln!("Warning: use --release for meaningful array timings");
        }
        let scope = std::env::var("STATSIG_ARRAY_BENCH_SCOPE").unwrap_or_else(|_| "all".into());
        assert!(matches!(scope.as_str(), "all" | "general" | "small" | "large" | "membership" | "equality" | "medium"), "STATSIG_ARRAY_BENCH_SCOPE must be all, general, small, large, membership, equality, or medium");
        let filter = std::env::var("STATSIG_ARRAY_BENCH_FILTER").unwrap_or_default();
        let fixtures = fixtures();
        let sample_override = std::env::var("STATSIG_ARRAY_BENCH_SAMPLE_US").ok();
        assert!(sample_override.is_none() || scope == "medium", "STATSIG_ARRAY_BENCH_SAMPLE_US is supported only in medium scope");
        let sample_time = if scope == "medium" {
            sample_override.map_or(MEDIUM_SAMPLE_TIME, |value| {
                let micros = value.parse::<u64>().expect("STATSIG_ARRAY_BENCH_SAMPLE_US must be a positive integer");
                assert!(micros > 0, "STATSIG_ARRAY_BENCH_SAMPLE_US must be positive");
                Duration::from_micros(micros)
            })
        } else {
            SAMPLE_TIME
        };
        let selected_rows: usize = fixtures.iter().filter(|f| f.selected(&scope, &filter))
            .map(|f| f.kernels().len() * 2 * if f.target.is_null() { 1 } else { 2 }).sum();
        if scope == "medium" {
            let nominal_sample_us = selected_rows as u128 * SAMPLES as u128 * 2 * sample_time.as_micros();
            assert!(nominal_sample_us <= MEDIUM_SAMPLE_BUDGET_US, "medium nominal sample budget exceeds 40s; narrow STATSIG_ARRAY_BENCH_FILTER or lower STATSIG_ARRAY_BENCH_SAMPLE_US");
        }
        // Owned targets must be built before installing the global mmap source.
        let owned: Vec<_> = fixtures.iter().map(|f| MemoizedEvaluatorValue::from(f.target.clone())).collect();
        let users: Vec<_> = fixtures.iter().map(|f| UserValue::from(f.value.clone())).collect();
        let dynamics: Vec<_> = fixtures.iter().map(|f| DynamicValue::from_json_value(f.value.clone())).collect();
        let conditions: serde_json::Map<_, _> = fixtures.iter().enumerate().map(|(i, f)| {
            (i.to_string(), json!({
                "type": "user_field", "targetValue": f.target,
                "operator": if matches!(f.kind, FixtureKind::Equality) { "eq" } else { "array_contains_any" },
                "field": "memberships", "additionalValues": {}, "idType": "userID"
            }))
        }).collect();
        let payload = serde_json::to_vec(&json!({
            "condition_map": conditions, "feature_gates": {}, "dynamic_configs": {},
            "layer_configs": {}, "experiment_to_layer": {}, "has_updates": true, "time": 1
        })).unwrap();
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("array-optimization-bench.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();
        // Null targetValue is absent in the serialized specs, so only owned
        // storage can represent that invalid operand.
        let mapped: Vec<_> = fixtures.iter().map(|f| {
            (!f.target.is_null()).then(|| EvaluatorValue::from_json_value(f.target.clone()))
        }).collect();
        for target in mapped.iter().flatten() {
            assert!(matches!(target.inner, EvaluatorValueInner::Mmap(_)));
        }

        // Validate every representation and operation before reporting ANY timings.
        for (i, fixture) in fixtures.iter().enumerate() {
            let kernels = fixture.kernels();
            let expected: Vec<_> = kernels.iter().map(|&kernel| fixture.expected(kernel)).collect();
            if matches!(fixture.kind, FixtureKind::AllMembership | FixtureKind::MediumMembership) {
                if fixture.name.contains("miss") {
                    assert!(!expected[0], "mislabeled miss: {}", fixture.name);
                }
                if fixture.name.contains("overlap") || fixture.name.contains("late-hit") {
                    assert!(expected[0], "mislabeled hit: {}", fixture.name);
                }
            } else if fixture.name.contains("mismatch") {
                assert!(!expected[0], "mislabeled mismatch: {}", fixture.name);
            } else if fixture.name.starts_with("equality-equal-") || fixture.name.starts_with("equality-empty-equal-") {
                assert!(expected[0], "mislabeled equality: {}", fixture.name);
            }
            for value in [UserValueRef::from(&users[i]), UserValueRef::from(&dynamics[i])] {
                for target in [Some(EvaluatorValueRef::from(&owned[i])), mapped[i].as_ref().map(EvaluatorValue::as_value_ref)].into_iter().flatten() {
                    for (kernel_index, &kernel) in kernels.iter().enumerate() {
                        let actual = production(value, target, kernel);
                        assert_eq!(actual, legacy(value, target, kernel), "parity: {}, {kernel:?}", fixture.name);
                        assert_eq!(actual, expected[kernel_index], "expected outcome: {}, {kernel:?}", fixture.name);
                    }
                }
            }
        }

        println!("Synthetic full-function benchmark; baseline={BASELINE_COMMIT}; scope={scope}; filter={filter}; selected_rows={selected_rows}; sample_time_us={}; symmetric non-inlined outer wrappers; user/target construction excluded; all parity/expected outcomes checked; medians of 5 samples; alternating order; ratios are not end-to-end CPU savings.", sample_time.as_micros());
        let mut row = 0;
        for (i, fixture) in fixtures.iter().enumerate() {
            if !fixture.selected(&scope, &filter) {
                continue;
            }
            let kernels = fixture.kernels();
            for (representation, value) in [("user", UserValueRef::from(&users[i])), ("dynamic", UserValueRef::from(&dynamics[i]))] {
                for (storage, target) in [Some(("owned", EvaluatorValueRef::from(&owned[i]))), mapped[i].as_ref().map(|target| ("mmap", target.as_value_ref()))].into_iter().flatten() {
                    let label = format!("case={} storage={storage} user={representation} user_len={:?} target_len={:?}", fixture.name, value.array_len(), target.array_len());
                    for &kernel in &kernels {
                        benchmark_row(value, target, kernel, &label, row, sample_time);
                        row += 1;
                    }
                }
            }
        }
        assert_eq!(row, selected_rows);
        println!("array_optimization_complete rows={row} scope={scope} baseline={BASELINE_COMMIT}");
    }
}
