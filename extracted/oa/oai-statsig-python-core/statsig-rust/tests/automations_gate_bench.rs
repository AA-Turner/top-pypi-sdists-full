//! Manual, offline benchmark. See data/automations_gate_bench.md for the fixture contract.

#![cfg(feature = "ffi-support")]

#[allow(dead_code)]
#[path = "utils/mock_event_logging_adapter.rs"]
mod mock_event_logging_adapter;
#[allow(dead_code)]
#[path = "utils/mock_specs_adapter.rs"]
mod mock_specs_adapter;

use serde_json::{Value, json};
use statsig_rust::{
    FeatureGateEvaluationOptions, Statsig, StatsigOptions, StatsigUser,
    sdk_event_emitter::SdkEvent,
    user::{
        StatsigUserInternal,
        fast_statsig_user::{FastStatsigUser, FastUserData},
        user_data::UserData,
    },
};
use std::{
    collections::HashSet,
    hint::black_box,
    sync::{
        Arc,
        atomic::{AtomicU64, Ordering},
    },
    time::Instant,
};

const GATE: &str = "automation_widget";
const EXPERIMENT: &str = "automation_widgets_experiment";
const FIXTURE: &str = include_str!("data/automations_gate_bench_specs.json");
const REUSE_FLAG: &str = "enable_nested_evaluation_reuse";

#[derive(Clone, Copy, Debug)]
enum Listener {
    None,
    Metadata,
    Json,
}

#[derive(Clone, Copy, Debug)]
enum Api {
    Public,
    Fast,
    FastFresh,
}

#[derive(Clone, Copy, Debug)]
enum Branch {
    FreeTreatment,
    FreeUnallocated,
    FreeOutOfRollout,
    Paid,
    OldMobile,
    Holdout,
    LegacyFallback,
    ColdMixed,
}

const BRANCHES: [Branch; 8] = [
    Branch::FreeTreatment,
    Branch::FreeUnallocated,
    Branch::FreeOutOfRollout,
    Branch::Paid,
    Branch::OldMobile,
    Branch::Holdout,
    Branch::LegacyFallback,
    Branch::ColdMixed,
];

struct User {
    public: StatsigUser,
    fast: FastStatsigUser,
}

fn user(id: &str, branch: Branch) -> User {
    let data = json!({
        "userID": id,
        "appVersion": if matches!(branch, Branch::OldMobile) { "1.2026.100" } else { "1.2026.300" },
        "custom": {
            "plan_type": if matches!(branch, Branch::Paid) { "paid" } else { "free" },
            "client_type": if matches!(branch, Branch::OldMobile) { "ios" } else { "web" },
            "anonymous": "false",
            "holdout": if matches!(branch, Branch::Holdout) { "true" } else { "false" },
            "legacy_member": if matches!(branch, Branch::LegacyFallback) { "true" } else { "false" },
            "test_cohort": "ordinary"
        }
    });
    User {
        public: StatsigUser::new(serde_json::from_value::<UserData>(data.clone()).unwrap()),
        fast: FastStatsigUser::new(serde_json::from_value::<FastUserData>(data).unwrap()),
    }
}

fn check(statsig: &Statsig, user: &User, api: Api, gate: &str) -> bool {
    let options = FeatureGateEvaluationOptions {
        // Keep exposure queues out of this evaluation/reporting benchmark. Both
        // variants still perform the same non-exposure-check bookkeeping.
        disable_exposure_logging: true,
    };
    match api {
        Api::Public => {
            statsig.use_raw_feature_gate_with_options(&user.public, gate, options, |result| {
                black_box(result.value)
            })
        }
        Api::Fast | Api::FastFresh => {
            // Python's StatsigUserPy uses FastStatsigUser. Recreate the internal
            // view on every call, as the binding does; reuse only the user data.
            let fresh;
            let fast = if matches!(api, Api::FastFresh) {
                fresh = FastStatsigUser::new((*user.fast.data).clone());
                &fresh
            } else {
                &user.fast
            };
            let internal = StatsigUserInternal::from_fast_user(fast, Some(statsig));
            statsig.use_raw_feature_gate_with_options_for_internal_user(
                &internal,
                gate,
                options,
                |result| black_box(result.value),
            )
        }
    }
}

// This is a benchmark driver setting, not a production SDK environment control.
fn requested_reuse() -> bool {
    matches!(
        std::env::var("AUTOMATIONS_BENCH_REUSE").as_deref(),
        Ok("true" | "1")
    )
}

fn experimental_flags(reuse: bool) -> Option<HashSet<String>> {
    reuse.then(|| HashSet::from([REUSE_FLAG.to_string()]))
}

async fn setup(
    before_dependency: bool,
    listener: Listener,
    reuse: bool,
) -> (Statsig, Arc<AtomicU64>) {
    let mut specs: Value = serde_json::from_str(FIXTURE).unwrap();
    if before_dependency {
        specs["feature_gates"][GATE]["rules"]
            .as_array_mut()
            .unwrap()
            .remove(0);
    }
    let options = StatsigOptions {
        specs_adapter: Some(Arc::new(
            mock_specs_adapter::MockSpecsAdapter::with_json_data(
                serde_json::to_string(&specs).unwrap(),
            ),
        )),
        event_logging_adapter: Some(Arc::new(
            mock_event_logging_adapter::MockEventLoggingAdapter::new_with_background_flush(false),
        )),
        disable_network: Some(true),
        output_log_level: Some("none".into()),
        experimental_flags: experimental_flags(reuse),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(
        "secret-offline-automations-benchmark",
        Some(Arc::new(options)),
    );
    let callbacks = Arc::new(AtomicU64::new(0));
    if !matches!(listener, Listener::None) {
        let count = callbacks.clone();
        statsig.subscribe(SdkEvent::EXPERIMENT_EVALUATED, move |event| {
            if let SdkEvent::ExperimentEvaluated {
                experiment_name,
                rule_id,
                group_name,
                value,
                ..
            } = event
            {
                black_box((experiment_name, rule_id, group_name));
                black_box(value.map(|value| value.get_hash()));
                if matches!(listener, Listener::Json) {
                    black_box(value.and_then(|value| value.get_json()));
                }
                count.fetch_add(1, Ordering::Relaxed);
            }
        });
    }
    statsig.initialize().await.unwrap();
    (statsig, callbacks)
}

fn select_user(statsig: &Statsig, branch: Branch, prefix: &str) -> User {
    if matches!(branch, Branch::Paid | Branch::OldMobile | Branch::Holdout) {
        return user(prefix, branch);
    }
    for index in 0..100_000 {
        let candidate = user(&format!("{prefix}-{index}"), branch);
        let rollout = check(statsig, &candidate, Api::Public, "scheduled_tasks_rollout");
        let target = check(statsig, &candidate, Api::Public, "scheduled_tasks_target");
        let experiment = statsig.get_experiment(&candidate.public, EXPERIMENT);
        let group = experiment.group_name.as_deref();
        let selected = match branch {
            Branch::FreeTreatment => rollout && matches!(group, Some("UI" | "UI and suggestions")),
            Branch::FreeUnallocated => rollout && group.is_none(),
            Branch::FreeOutOfRollout => !rollout && !target,
            Branch::LegacyFallback => !rollout && target && group.is_none(),
            _ => unreachable!(),
        };
        if selected {
            return candidate;
        }
    }
    panic!("could not find a deterministic user for {branch:?}");
}

#[tokio::test]
async fn sanitized_automations_fixture_exercises_expected_branches() {
    let reuse = requested_reuse();
    let (after, callbacks) = setup(false, Listener::Metadata, reuse).await;
    let (before, _) = setup(true, Listener::None, reuse).await;
    for branch in BRANCHES {
        if matches!(branch, Branch::ColdMixed) {
            continue;
        }
        let candidate = select_user(&after, branch, &format!("smoke-{branch:?}"));
        for api in [Api::Public, Api::Fast, Api::FastFresh] {
            assert!(!check(&before, &candidate, api, GATE));
            let expected = matches!(branch, Branch::FreeTreatment);
            assert_eq!(check(&after, &candidate, api, GATE), expected, "{branch:?}");
        }
    }
    assert!(callbacks.load(Ordering::Relaxed) > 0);
    before.shutdown().await.unwrap();
    after.shutdown().await.unwrap();
}

fn positive_env(name: &str, default: usize) -> usize {
    std::env::var(name)
        .ok()
        .and_then(|value| value.parse().ok())
        .filter(|value| *value > 0)
        .unwrap_or(default)
}

fn selected<T: Copy + std::fmt::Debug>(name: &str, defaults: &[T], all: &[T]) -> Vec<T> {
    let Ok(filter) = std::env::var(name) else {
        return defaults.to_vec();
    };
    let mut result = Vec::new();
    for requested in filter.split(',') {
        let value = all
            .iter()
            .find(|value| format!("{value:?}") == requested.trim())
            .unwrap_or_else(|| panic!("unsupported {name} value: {requested}"));
        result.push(*value);
    }
    assert!(!result.is_empty(), "{name} must select at least one value");
    result
}

fn selected_graph(before: bool) -> bool {
    match std::env::var("AUTOMATIONS_BENCH_GRAPH").as_deref() {
        Err(_) | Ok("both") => true,
        Ok("before") => before,
        Ok("after") => !before,
        Ok(value) => panic!("unsupported AUTOMATIONS_BENCH_GRAPH value: {value}"),
    }
}

#[tokio::test]
#[ignore = "manual full matrix; select exact test; see data/automations_gate_bench.md"]
async fn benchmark_sanitized_automations_dependency_graph() {
    run_benchmark(
        &[positive_env("AUTOMATIONS_BENCH_REPEATS", 262)],
        &[Api::Public, Api::Fast, Api::FastFresh],
        &[Listener::None, Listener::Metadata, Listener::Json],
    )
    .await;
}

#[tokio::test]
#[ignore = "manual admission benchmark; see data/automations_gate_bench.md"]
async fn benchmark_sanitized_automations_repeat_sweep() {
    run_benchmark(
        &[1, 2, 3, 4, 16, 262],
        &[Api::FastFresh],
        &[Listener::Metadata],
    )
    .await;
}

async fn run_benchmark(
    repeat_counts: &[usize],
    default_apis: &[Api],
    default_listeners: &[Listener],
) {
    let rounds = positive_env("AUTOMATIONS_BENCH_ROUNDS", 5);
    let requests = positive_env("AUTOMATIONS_BENCH_REQUESTS", 16);
    let reuse = requested_reuse();
    let apis = selected(
        "AUTOMATIONS_BENCH_APIS",
        default_apis,
        &[Api::Public, Api::Fast, Api::FastFresh],
    );
    let listeners = selected(
        "AUTOMATIONS_BENCH_LISTENERS",
        default_listeners,
        &[Listener::None, Listener::Metadata, Listener::Json],
    );
    let branches = selected("AUTOMATIONS_BENCH_BRANCHES", &BRANCHES, &BRANCHES);
    for &repeated_checks in repeat_counts {
        for &listener in &listeners {
            // Alternating the graph order per row avoids a fixed before/after order.
            for (branch_index, &branch) in branches.iter().enumerate() {
                // Select cohorts using a separate, unopted-in SDK. Measured SDKs
                // have never evaluated any of these identities before timing.
                let (selector, _) = setup(false, Listener::None, false).await;
                let checks_per_user = if matches!(branch, Branch::ColdMixed) {
                    1
                } else {
                    repeated_checks
                };
                let users_per_round = requests * repeated_checks / checks_per_user;
                // Preconstruct every user outside timing. Distinct identities per
                // request/round prevent a supposedly cold case from becoming warm.
                let users: Vec<User> = (0..rounds * users_per_round)
                    .map(|index| {
                        let prefix = format!("bench-{listener:?}-{branch:?}-{index}");
                        if matches!(branch, Branch::ColdMixed) {
                            let kind = match index % 4 {
                                0 => Branch::Paid,
                                1 => Branch::OldMobile,
                                2 => Branch::Holdout,
                                _ => Branch::FreeUnallocated,
                            };
                            user(&prefix, kind)
                        } else {
                            select_user(&selector, branch, &prefix)
                        }
                    })
                    .collect();
                selector.shutdown().await.unwrap();
                for &api in &apis {
                    let order = if branch_index % 2 == 0 {
                        [true, false]
                    } else {
                        [false, true]
                    };
                    for before in order {
                        if !selected_graph(before) {
                            continue;
                        }
                        // Each repeat count, branch, API and graph gets a fresh
                        // SDK. Cohorts cannot warm later sweep rows accidentally.
                        let (statsig, callbacks) = setup(before, listener, reuse).await;
                        let warmup = user("benchmark-warmup-only", Branch::Paid);
                        for _ in 0..repeated_checks {
                            black_box(check(&statsig, &warmup, api, GATE));
                        }
                        let initial_callbacks = callbacks.load(Ordering::Relaxed);
                        let mut durations_ns = Vec::with_capacity(rounds);
                        let mut positives = 0_u64;
                        for chunk in users.chunks_exact(users_per_round) {
                            let start = Instant::now();
                            for candidate in chunk {
                                for _ in 0..checks_per_user {
                                    positives += u64::from(check(&statsig, candidate, api, GATE));
                                }
                            }
                            durations_ns.push(start.elapsed().as_nanos() as u64);
                        }
                        let mut sorted = durations_ns.clone();
                        sorted.sort_unstable();
                        let checks_per_round = users_per_round * checks_per_user;
                        println!(
                            "{}",
                            json!({
                                "benchmark": "sanitized_automations_dependency_graph_v2",
                                "before_dependency": before,
                                "api": format!("{api:?}"),
                                "listener": format!("{listener:?}"),
                                "branch": format!("{branch:?}"),
                                "rounds": rounds,
                                "users_per_round": users_per_round,
                                "checks_per_user": checks_per_user,
                                "requested_repeats": repeated_checks,
                                "checks_per_round": checks_per_round,
                                "round_ns": durations_ns,
                                "median_ns_per_check": sorted[sorted.len()/2] as f64 / checks_per_round as f64,
                                "positive_results": positives,
                                "experiment_callbacks": callbacks.load(Ordering::Relaxed)-initial_callbacks,
                                "exposure_logging": false,
                                "harness_reuse": reuse,
                                "experimental_flags": experimental_flags(reuse).unwrap_or_default()
                            })
                        );
                        statsig.shutdown().await.unwrap();
                    }
                }
            }
        }
    }
}
