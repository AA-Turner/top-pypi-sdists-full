#![cfg(feature = "ffi-support")]

mod utils;

#[path = "utils/synthetic_specs_fixture.rs"]
mod synthetic_specs_fixture;

use crate::utils::mock_event_logging_adapter::MockEventLoggingAdapter;
use crate::utils::mock_specs_adapter::MockSpecsAdapter;
use serde_json::Value;
use statsig_rust::{
    BulkEvaluationOptions, ClientInitResponseOptions, HashAlgorithm, LayerEvaluationOptions,
    Statsig, StatsigOptions, StatsigUser, StatsigUserBuilder,
};
use std::collections::HashMap;
use std::hint::black_box;
use std::process::Command;
use std::sync::Arc;
use std::time::Instant;

const WARMUP: usize = 100;
const ITER: usize = 1_000;
const GCIR_ITER: usize = 100;
const MEMORY_TOKENS: usize = 5_000;

#[derive(Clone)]
struct BenchStats {
    avg_us: f64,
    p50_us: f64,
    p95_us: f64,
    p99_us: f64,
}

#[tokio::test]
#[ignore = "manual benchmark; run with --features ffi-support --ignored --nocapture"]
async fn benchmark_delayed_exposure_bulk_api() {
    let population_json = synthetic_specs_fixture::evaluation_json();
    let population_specs: Value =
        serde_json::from_str(&population_json).expect("population JSON must parse");
    let population = setup("secret-population-bench", population_json).await;
    let token_controls = if std::env::var_os("STATSIG_BENCH_MANIFEST").is_none() {
        Some(
            setup(
                "secret-perf-microcases",
                include_str!("data/perf_proj_dcs.json").to_owned(),
            )
            .await,
        )
    } else {
        None
    };
    let user = make_user("bench-user");

    let opts = ClientInitResponseOptions {
        hash_algorithm: Some(HashAlgorithm::None),
        ..Default::default()
    };
    let EntityCounts {
        feature_gates,
        dynamic_configs,
        experiments,
        layers,
    } = entity_counts_from_gcir(
        &population.get_client_init_response_with_options_as_string(&user, &opts),
        &population_specs,
    );
    drop(population_specs);
    let entity_count = feature_gates + dynamic_configs + experiments + layers;

    assert!(
        entity_count > 0,
        "selected population must produce GCIR entities"
    );
    if experiments == 0 {
        println!("population experiment coverage: unavailable");
    }
    if layers == 0 {
        println!("population layer coverage: unavailable");
    }

    let evaluate_all_stats = bench(GCIR_ITER, WARMUP / 10, || {
        black_box(population.bulk_evaluate_with_delayed_exposures(
            &user,
            BulkEvaluationOptions {
                include_local_override: true,
                ..BulkEvaluationOptions::default()
            },
        ));
    });

    let gcir_stats = bench(GCIR_ITER, WARMUP / 10, || {
        black_box(population.get_client_init_response_with_options_as_string(&user, &opts));
    });

    let gcir_json_parse_stats = bench(GCIR_ITER, WARMUP / 10, || {
        let gcir_json = population.get_client_init_response_with_options_as_string(&user, &opts);
        black_box(serde_json::from_str::<Value>(&gcir_json).expect("GCIR JSON must parse"));
    });

    println!("\nPopulation bulk and GCIR benchmark ({GCIR_ITER} iterations)");
    println!(
        "entities from GCIR(hash=none): gates={feature_gates}, dynamic_configs={dynamic_configs}, experiments={experiments}, layers={layers}, total={entity_count}"
    );
    print_row(
        "bulk_evaluate evaluate_all typed response",
        &evaluate_all_stats,
    );
    print_row("get_client_initialize_response JSON", &gcir_stats);
    print_row(
        "get_client_initialize_response + JSON parse",
        &gcir_json_parse_stats,
    );
    println!(
        "evaluate_all per entity avg: {:.3}us",
        evaluate_all_stats.avg_us / entity_count as f64
    );
    println!(
        "gcir per selected-entity equivalent avg: {:.3}us",
        gcir_stats.avg_us / entity_count as f64
    );
    println!(
        "gcir + JSON parse per selected-entity equivalent avg: {:.3}us",
        gcir_json_parse_stats.avg_us / entity_count as f64
    );
    if let Some(controls) = token_controls {
        benchmark_embedded_token_controls(&controls, &user);
        controls.shutdown().await.unwrap();
    }
    population.shutdown().await.unwrap();
}

fn benchmark_embedded_token_controls(statsig: &Statsig, user: &StatsigUser) {
    let regular_gate_stats = bench(ITER, WARMUP, || {
        black_box(statsig.get_feature_gate(user, "test_public"));
    });

    let delayed_gate_tokens: Vec<String> = (0..ITER + WARMUP)
        .filter_map(|i| {
            let user = make_user(&format!("delayed-gate-{i}"));
            let (_, token) =
                statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());
            token
        })
        .collect();
    let mut delayed_gate_index = 0usize;
    let delayed_gate_log_stats = bench(ITER, WARMUP, || {
        let token = &delayed_gate_tokens[delayed_gate_index];
        delayed_gate_index += 1;
        black_box(statsig.log_delayed_exposure(token));
    });

    let regular_layer_param_stats = bench(ITER, WARMUP, || {
        let layer = statsig.get_layer(user, "big_layer");
        black_box(layer.get_raw_value("a_string"));
    });

    let (_, layer_token) = statsig.use_raw_layer_with_delayed_exposure(
        &make_user("layer-token"),
        "big_layer",
        LayerEvaluationOptions::default(),
        |_| (),
    );
    let layer_token = layer_token.expect("expected layer token");
    let delayed_layer_distinct_stats = bench(ITER, WARMUP, || {
        let param = format!("param_{}", rand_index());
        black_box(statsig.log_delayed_layer_parameter_exposure(&layer_token, &param));
    });

    let delayed_layer_repeat_stats = bench(ITER, WARMUP, || {
        black_box(statsig.log_delayed_layer_parameter_exposure(&layer_token, "a_string"));
    });

    let gate_memory = measure_gate_token_memory(statsig);
    let layer_memory = measure_layer_token_memory(statsig);

    println!(
        "\nDelayed exposure controls: perf_proj_dcs.json ({ITER} iterations, warmup={WARMUP})"
    );
    print_row("get_feature_gate regular", &regular_gate_stats);
    print_row(
        "log_delayed_exposure existing token",
        &delayed_gate_log_stats,
    );
    print_row(
        "get_layer(...).get_raw_value regular",
        &regular_layer_param_stats,
    );
    print_row(
        "log_delayed_layer_parameter_exposure distinct",
        &delayed_layer_distinct_stats,
    );
    print_row(
        "log_delayed_layer_parameter_exposure repeat",
        &delayed_layer_repeat_stats,
    );
    println!(
        "memory gate/config/experiment token: {:.1} bytes/token over {} tokens (rss delta {} KB)",
        gate_memory.bytes_per_token, MEMORY_TOKENS, gate_memory.rss_delta_kb
    );
    println!(
        "memory layer token + param dedupe: {:.1} bytes/param over {} params (rss delta {} KB)",
        layer_memory.bytes_per_token, MEMORY_TOKENS, layer_memory.rss_delta_kb
    );
}

struct EntityCounts {
    feature_gates: usize,
    dynamic_configs: usize,
    experiments: usize,
    layers: usize,
}

fn entity_counts_from_gcir(gcir_json: &str, specs: &Value) -> EntityCounts {
    let gcir: Value = serde_json::from_str(gcir_json).expect("GCIR JSON must parse");
    let entities = |field: &str| gcir[field].as_object().expect("expected object");
    let configs = entities("dynamic_configs");
    let config_specs = &specs["dynamic_configs"];
    let experiments = configs
        .keys()
        .filter(|name| config_specs[*name]["entity"].as_str() == Some("experiment"))
        .count();
    EntityCounts {
        feature_gates: entities("feature_gates").len(),
        dynamic_configs: configs.len() - experiments,
        experiments,
        layers: entities("layer_configs").len(),
    }
}

async fn setup(sdk_key: &str, json: String) -> Statsig {
    let specs_adapter = Arc::new(MockSpecsAdapter::with_json_data(json));
    let logging_adapter = Arc::new(MockEventLoggingAdapter::new());
    let options = StatsigOptions {
        specs_adapter: Some(specs_adapter),
        event_logging_adapter: Some(logging_adapter),
        event_logging_max_queue_size: Some(1_000_000),
        ..StatsigOptions::new()
    };
    let statsig = Statsig::new(sdk_key, Some(Arc::new(options)));
    statsig.initialize().await.unwrap();
    statsig
}

fn make_user(id: &str) -> StatsigUser {
    StatsigUserBuilder::new_with_user_id(id.to_string())
        .custom_ids(Some(HashMap::from([(
            "companyID".to_string(),
            "employee".to_string(),
        )])))
        .country(Some("US".to_string()))
        .build()
}

fn bench(iterations: usize, warmup: usize, mut f: impl FnMut()) -> BenchStats {
    for _ in 0..warmup {
        f();
    }

    let mut samples = Vec::with_capacity(iterations);
    for _ in 0..iterations {
        let start = Instant::now();
        f();
        samples.push(start.elapsed().as_nanos() as f64 / 1000.0);
    }

    samples.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let avg_us = samples.iter().sum::<f64>() / samples.len() as f64;
    BenchStats {
        avg_us,
        p50_us: percentile(&samples, 0.50),
        p95_us: percentile(&samples, 0.95),
        p99_us: percentile(&samples, 0.99),
    }
}

fn percentile(samples: &[f64], percentile: f64) -> f64 {
    let index = ((samples.len() - 1) as f64 * percentile).round() as usize;
    samples[index]
}

fn print_row(name: &str, stats: &BenchStats) {
    println!(
        "{name:<48} avg={:>8.3}us p50={:>8.3}us p95={:>8.3}us p99={:>8.3}us",
        stats.avg_us, stats.p50_us, stats.p95_us, stats.p99_us
    );
}

struct MemoryResult {
    rss_delta_kb: i64,
    bytes_per_token: f64,
}

fn measure_gate_token_memory(statsig: &Statsig) -> MemoryResult {
    let before = current_rss_kb();
    let mut tokens = Vec::with_capacity(MEMORY_TOKENS);
    for i in 0..MEMORY_TOKENS {
        let user = make_user(&format!("memory-gate-{i}"));
        let (_, token) =
            statsig.use_raw_feature_gate_with_delayed_exposure(&user, "test_public", |_| ());
        if let Some(token) = token {
            tokens.push(token);
        }
    }
    let after = current_rss_kb();
    let released = statsig.release_delayed_exposures(&tokens);
    assert_eq!(released, tokens.len());
    let delta = (after - before).max(0);
    MemoryResult {
        rss_delta_kb: delta,
        bytes_per_token: delta as f64 * 1024.0 / tokens.len().max(1) as f64,
    }
}

fn measure_layer_token_memory(statsig: &Statsig) -> MemoryResult {
    let (_, token) = statsig.use_raw_layer_with_delayed_exposure(
        &make_user("memory-layer"),
        "big_layer",
        LayerEvaluationOptions::default(),
        |_| (),
    );
    let token = token.expect("expected layer token");
    let before = current_rss_kb();
    for i in 0..MEMORY_TOKENS {
        let param = format!("memory_param_{i}");
        assert!(statsig.log_delayed_layer_parameter_exposure(&token, &param));
    }
    let after = current_rss_kb();
    assert!(statsig.release_delayed_exposure(&token));
    let delta = (after - before).max(0);
    MemoryResult {
        rss_delta_kb: delta,
        bytes_per_token: delta as f64 * 1024.0 / MEMORY_TOKENS as f64,
    }
}

fn current_rss_kb() -> i64 {
    let pid = std::process::id().to_string();
    let output = Command::new("ps")
        .args(["-o", "rss=", "-p", &pid])
        .output()
        .expect("failed to run ps");
    String::from_utf8_lossy(&output.stdout)
        .trim()
        .parse::<i64>()
        .unwrap_or(0)
}

fn rand_index() -> usize {
    use std::sync::atomic::{AtomicUsize, Ordering};
    static NEXT: AtomicUsize = AtomicUsize::new(0);
    NEXT.fetch_add(1, Ordering::Relaxed)
}
