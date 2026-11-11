#[path = "utils/synthetic_specs_fixture.rs"]
mod synthetic_specs_fixture;

use std::{hint::black_box, sync::Mutex, time::Instant};

use statsig_rust::{
    ClientInitResponseOptions, HashAlgorithm, StatsigUser,
    evaluation::evaluator_context::{EvaluatorContext, IdListResolution},
    gcir::{
        evaluation_plan::GcirEvaluationPlan,
        gcir_formatter::GCIRFormatter,
        timing::{self as gcir_timing, TimingEntry},
    },
    hashing::HashUtil,
    specs_response::spec_types::SpecsResponseFull,
    user::StatsigUserInternal,
};

#[test]
#[ignore = "manual benchmark; run with --release --ignored --nocapture"]
fn benchmark_planned_v1_initialize_format() {
    run_planned_v1_initialize_benchmark("with_checksum", Some("stale-checksum"));
}

#[test]
#[ignore = "manual benchmark; run with --release --ignored --nocapture"]
fn benchmark_planned_v1_initialize_format_no_checksum() {
    run_planned_v1_initialize_benchmark("no_checksum", None);
}

fn run_planned_v1_initialize_benchmark(label: &str, previous_hash: Option<&str>) {
    // The formatter's timing counters are shared by both tests in this process.
    static BENCHMARK: Mutex<()> = Mutex::new(());
    let _guard = BENCHMARK.lock().unwrap();
    let iterations = std::env::var("GCIR_BENCH_ITERATIONS")
        .ok()
        .and_then(|value| value.parse::<usize>().ok())
        .filter(|value| *value > 0)
        .unwrap_or(3000);

    let specs: SpecsResponseFull =
        serde_json::from_str(&synthetic_specs_fixture::evaluation_json()).unwrap();
    let hashing = HashUtil::new();
    let plan = GcirEvaluationPlan::new(&specs, &hashing);
    let experiments = specs
        .dynamic_configs
        .iter()
        .filter(|(_, spec)| spec.as_spec_ref().entity.as_str() == "experiment")
        .count();
    let configs = specs
        .dynamic_configs
        .iter()
        .filter(|(_, spec)| spec.as_spec_ref().entity.as_str() == "dynamic_config")
        .count();
    println!(
        "available population: gates={} configs={configs} experiments={experiments} layers={}",
        specs.feature_gates.len(),
        specs.layer_configs.len(),
    );
    if experiments == 0 {
        println!("experiment coverage: unavailable in selected population");
    }
    if specs.layer_configs.is_empty() {
        println!("layer coverage: unavailable in selected population");
    }

    let requested_timings = std::env::var("GCIR_BENCH_TIMINGS").is_ok_and(|value| value == "1");
    let capture_timings = requested_timings && cfg!(feature = "gcir-bench-timings");
    if requested_timings && !capture_timings {
        println!(
            "GCIR benchmark timings require --features gcir-bench-timings; running without timings"
        );
    }
    let user = StatsigUser::with_user_id("snapshot-bench-user");
    let user_internal = StatsigUserInternal::new(&user, None);
    let options = ClientInitResponseOptions {
        hash_algorithm: Some(HashAlgorithm::Djb2),
        client_sdk_key: Some("client-benchmark".to_string()),
        previous_response_hash: previous_hash.map(str::to_owned),
        ..Default::default()
    };
    let generate = || {
        let mut ctx = EvaluatorContext::new(
            &user_internal,
            &specs,
            IdListResolution::Callback(&|_, _| false),
            &hashing,
            None,
            None,
            false,
            false,
        );
        GCIRFormatter::generate_v1_format_with_plan(&mut ctx, &options, &plan)
            .expect("planned v1 format should generate")
    };
    let response = generate();
    let gates = response.feature_gates.len();
    let configs = response.dynamic_configs.len();
    let layers = response.layer_configs.len();
    assert!(
        gates + configs + layers > 0,
        "selected population must produce a nonempty GCIR response"
    );
    assert_eq!(response.full_checksum.is_some(), previous_hash.is_some());
    println!(
        "{label}: GCIR returned gates={gates} configs_and_experiments={configs} layers={layers}"
    );
    drop(response);

    if capture_timings {
        gcir_timing::reset();
        gcir_timing::enable(true);
    }
    let started = Instant::now();
    for _ in 0..iterations {
        black_box(generate());
    }
    let elapsed = started.elapsed();
    if capture_timings {
        gcir_timing::enable(false);
    }
    let total_ms = elapsed.as_secs_f64() * 1000.0;
    let per_request_ms = total_ms / iterations as f64;
    println!(
        "gcir_plan_expansion_bench label={label} iterations={iterations} total_ms={total_ms:.3} per_request_ms={per_request_ms:.6}"
    );
    if capture_timings {
        print_timing_table(&gcir_timing::take(), elapsed.as_nanos(), iterations);
    }
}

fn print_timing_table(entries: &[TimingEntry], total_ns: u128, iterations: usize) {
    println!(
        "{:<36} {:>12} {:>14} {:>10} {:>10}",
        "label", "total_ms", "per_req_us", "pct_total", "count"
    );
    for entry in entries {
        let total_ms = entry.total_ns as f64 / 1_000_000.0;
        let per_request_us = entry.total_ns as f64 / iterations as f64 / 1_000.0;
        let pct_total = if total_ns == 0 {
            0.0
        } else {
            entry.total_ns as f64 * 100.0 / total_ns as f64
        };
        println!(
            "{:<36} {:>12.3} {:>14.3} {:>9.2}% {:>10}",
            entry.label, total_ms, per_request_us, pct_total, entry.count
        );
    }
}
