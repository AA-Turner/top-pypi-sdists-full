use std::time::Instant;

use statsig_rust::{
    evaluation::evaluator_context::{EvaluatorContext, IdListResolution},
    gcir::{
        evaluation_plan::GcirEvaluationPlan,
        gcir_formatter::GCIRFormatter,
        timing::{self as gcir_timing, TimingEntry},
    },
    hashing::HashUtil,
    specs_response::spec_types::SpecsResponseFull,
    user::StatsigUserInternal,
    ClientInitResponseOptions, HashAlgorithm, StatsigUser,
};

#[test]
#[ignore = "manual benchmark; run with --release --ignored --nocapture"]
fn benchmark_planned_v1_initialize_format() {
    run_planned_v1_initialize_benchmark("with_checksum", true);
}

#[test]
#[ignore = "manual benchmark; run with --release --ignored --nocapture"]
fn benchmark_planned_v1_initialize_format_no_checksum() {
    run_planned_v1_initialize_benchmark("no_checksum", false);
}

fn run_planned_v1_initialize_benchmark(label: &str, include_previous_response_hash: bool) {
    let iterations = std::env::var("GCIR_BENCH_ITERATIONS")
        .ok()
        .and_then(|value| value.parse::<usize>().ok())
        .unwrap_or(3000);

    let specs: SpecsResponseFull =
        serde_json::from_str(include_str!("data/perf_proj_dcs.json")).unwrap();
    let hashing = HashUtil::new();
    let plan = GcirEvaluationPlan::new(&specs, &hashing);
    let user = StatsigUser::with_user_id("snapi-bench-user");
    let user_internal = StatsigUserInternal::new(&user, None);
    let id_list_callback = |_: &str, _: &str| false;
    let options = ClientInitResponseOptions {
        hash_algorithm: Some(HashAlgorithm::Djb2),
        client_sdk_key: Some("client-benchmark".to_string()),
        previous_response_hash: include_previous_response_hash
            .then(|| "stale-checksum".to_string()),
        ..Default::default()
    };

    let requested_timings = std::env::var("GCIR_BENCH_TIMINGS").is_ok_and(|value| value == "1");
    let capture_timings = requested_timings && cfg!(feature = "gcir-bench-timings");
    if requested_timings && !capture_timings {
        println!(
            "GCIR benchmark timings require --features gcir-bench-timings; running without timings"
        );
    }
    if capture_timings {
        gcir_timing::reset();
        gcir_timing::enable(true);
    }

    let mut checksum = 0usize;
    let started = Instant::now();
    for _ in 0..iterations {
        let mut ctx = EvaluatorContext::new(
            &user_internal,
            &specs,
            IdListResolution::Callback(&id_list_callback),
            &hashing,
            None,
            None,
            false,
            None,
            true,
        );
        let response = GCIRFormatter::generate_v1_format_with_plan(&mut ctx, &options, &plan)
            .expect("planned v1 format should generate");
        checksum ^= response.feature_gates.len();
        checksum ^= response.dynamic_configs.len();
        checksum ^= response.layer_configs.len();
        checksum ^= response.full_checksum.as_ref().map_or(0, String::len);
    }
    let elapsed = started.elapsed();
    if capture_timings {
        gcir_timing::enable(false);
    }
    let total_ms = elapsed.as_secs_f64() * 1000.0;
    let per_request_ms = total_ms / iterations as f64;
    println!(
        "gcir_plan_expansion_bench label={label} iterations={iterations} total_ms={total_ms:.3} per_request_ms={per_request_ms:.6} checksum={checksum}"
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
