//! Quick, hand-timed benchmark sanity check (no Criterion wait) that doubles as the
//! generator for `benches/history.csv`'s persistent, cross-commit benchmark record.
//!
//! ```bash
//! cargo run --release --example bench_quick             # human-readable table
//! cargo run --release --example bench_quick -- --csv    # CSV rows to stdout
//! ```
//!
//! This is deliberately informational, not statistically rigorous — see
//! `benches/*.rs` (Criterion) for that. Scenarios mirror BENCHMARKS.md's
//! "Performance Targets" table so this tool tracks exactly those numbers over time.

use json_tools_rs::JSONTools;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

mod test_data {
    // Mirrors benches/isolation_benchmarks.rs::test_data::small_json() / medium_json()
    // and benches/comprehensive_benchmark.rs::large_json() — kept as separate literals
    // here since examples can't depend on the benches/ target's modules.
    pub fn small_json() -> &'static str {
        r#"{
            "user": {
                "id": 12345,
                "name": "John Doe",
                "email": "john.doe@example.com",
                "profile": {
                    "age": 30,
                    "city": "New York",
                    "country": "USA",
                    "bio": "",
                    "website": null,
                    "preferences": {
                        "theme": "dark",
                        "language": "en",
                        "notifications": true
                    }
                },
                "tags": ["developer", "rust", "json"],
                "metadata": {}
            }
        }"#
    }

    pub fn medium_json() -> &'static str {
        r#"{
            "order": {
                "id": "ORD-2024-001234",
                "customer": {
                    "id": "CUST-98765",
                    "firstName": "Jane",
                    "lastName": "Smith",
                    "email": "jane.smith@example.com",
                    "phone": "+1-555-0123",
                    "address": {
                        "street": "123 Main St",
                        "city": "San Francisco",
                        "state": "CA",
                        "zipCode": "94102",
                        "country": "USA"
                    }
                },
                "items": [
                    {
                        "productId": "PROD-001",
                        "name": "Wireless Keyboard",
                        "price": "$59.99",
                        "quantity": "2",
                        "inStock": "true"
                    },
                    {
                        "productId": "PROD-002",
                        "name": "USB Mouse",
                        "price": "$29.99",
                        "quantity": "1",
                        "inStock": "true"
                    }
                ],
                "totals": {
                    "subtotal": "$171.96",
                    "tax": "$15.00",
                    "total": "$186.96"
                }
            }
        }"#
    }

    pub fn large_json() -> &'static str {
        r#"{
            "api_response": {
                "metadata": {
                    "requestId": "req_a1b2c3d4e5f6",
                    "timestamp": "2024-01-10T12:00:00Z",
                    "version": "v2.0",
                    "environment": "production",
                    "region": "us-west-2",
                    "server": "api-server-42"
                },
                "data": {
                    "company": {
                        "id": "COMP-12345",
                        "name": "TechCorp International",
                        "type": "Corporation",
                        "founded": "1995",
                        "employees": "5000",
                        "revenue": "$500000000",
                        "headquarters": {
                            "address": {
                                "street": "1000 Tech Plaza",
                                "city": "San Francisco",
                                "state": "CA",
                                "zipCode": "94105",
                                "country": "USA"
                            }
                        },
                        "departments": [
                            {"name": "Engineering", "headcount": "1500", "budget": "$50000000"},
                            {"name": "Sales", "headcount": "800", "budget": "$20000000"},
                            {"name": "Marketing", "headcount": "300", "budget": "$10000000"},
                            {"name": "Support", "headcount": "400", "budget": "$8000000"}
                        ]
                    },
                    "products": [
                        {"id": "P1", "name": "Widget Pro", "price": "$99.99", "inStock": "true"},
                        {"id": "P2", "name": "Widget Lite", "price": "$49.99", "inStock": "true"},
                        {"id": "P3", "name": "Widget Max", "price": "$199.99", "inStock": "false"}
                    ]
                }
            }
        }"#
    }
}

/// Run `f` for at least `min_duration` (subject to `max_iters`), after one untimed
/// warm-up call. Returns average seconds per call. Adaptive iteration count (rather
/// than a fixed count) because scenario costs here range from ~1us to ~1ms.
fn time_it<F: FnMut()>(mut f: F, min_duration: Duration, max_iters: u32) -> f64 {
    f(); // warm-up: page faults, cache/branch-predictor warm-up, regex-cache population
    let start = Instant::now();
    let mut iters = 0u32;
    loop {
        f();
        iters += 1;
        if iters >= max_iters || start.elapsed() >= min_duration {
            break;
        }
    }
    start.elapsed().as_secs_f64() / iters as f64
}

/// Resolves the commit this run should be tagged as in `--csv` mode: an explicit
/// `BENCH_COMMIT` env var (CI passes `$GITHUB_SHA`) takes priority, falling back to a
/// best-effort `git rev-parse` for zero-config local use, and finally `"unknown"`.
fn resolve_commit() -> String {
    if let Ok(c) = std::env::var("BENCH_COMMIT") {
        return c;
    }
    std::process::Command::new("git")
        .args(["rev-parse", "--short", "HEAD"])
        .output()
        .ok()
        .filter(|o| o.status.success())
        .and_then(|o| String::from_utf8(o.stdout).ok())
        .map(|s| s.trim().to_string())
        .filter(|s| !s.is_empty())
        .unwrap_or_else(|| "unknown".to_string())
}

/// One measured row: (operation, scenario, size, time_us).
type Row = (&'static str, &'static str, &'static str, f64);

fn run_scenarios() -> Vec<Row> {
    const MIN_DUR: Duration = Duration::from_millis(150);
    const MAX_ITERS: u32 = 20_000;

    let small = test_data::small_json();
    let medium = test_data::medium_json();
    let large = test_data::large_json();
    let batch_10: Vec<&str> = (0..10).map(|_| small).collect();
    let batch_100: Vec<&str> = (0..100).map(|_| small).collect();

    let mut rows = Vec::new();
    let mut secs = |op, scenario, size, f: &mut dyn FnMut()| {
        let avg_s = time_it(&mut *f, MIN_DUR, MAX_ITERS);
        rows.push((op, scenario, size, avg_s * 1_000_000.0));
    };

    // "Basic flatten (medium)" target: no transformations.
    secs("flatten", "baseline", "small", &mut || {
        JSONTools::new().flatten().execute(small).unwrap();
    });
    secs("flatten", "baseline", "medium", &mut || {
        JSONTools::new().flatten().execute(medium).unwrap();
    });
    secs("flatten", "baseline", "large", &mut || {
        JSONTools::new().flatten().execute(large).unwrap();
    });

    // "With transformations" target: every feature enabled at once.
    secs("flatten", "all_transforms", "medium", &mut || {
        JSONTools::new()
            .flatten()
            .separator("::")
            .lowercase_keys(true)
            .key_replacement("r'_id$'", "id")
            .key_replacement("name", "fullname")
            .value_replacement("@example.com", "@company.org")
            .value_replacement("r'^\\$'", "USD ")
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .auto_convert_types(true)
            .handle_key_collision(true)
            .execute(medium)
            .unwrap();
    });

    // "Regex replacements" target: caching-sensitive path in isolation.
    secs("flatten", "regex_replacements", "medium", &mut || {
        JSONTools::new()
            .flatten()
            .key_replacement("r'_id$'", "id")
            .value_replacement("r'^\\$'", "USD ")
            .execute(medium)
            .unwrap();
    });

    secs("unflatten", "baseline", "medium", &mut || {
        let flat = JSONTools::new().flatten().execute(medium).unwrap();
        let flat_str = match flat {
            json_tools_rs::JsonOutput::Single(s) => s,
            _ => unreachable!(),
        };
        JSONTools::new()
            .unflatten()
            .execute(flat_str.as_str())
            .unwrap();
    });

    secs("normal", "baseline", "medium", &mut || {
        JSONTools::new()
            .normal()
            .lowercase_keys(true)
            .auto_convert_types(true)
            .execute(medium)
            .unwrap();
    });

    // "Roundtrip" target: flatten + unflatten timed together.
    secs("roundtrip", "baseline", "medium", &mut || {
        let flat = JSONTools::new().flatten().execute(medium).unwrap();
        let flat_str = match flat {
            json_tools_rs::JsonOutput::Single(s) => s,
            _ => unreachable!(),
        };
        JSONTools::new()
            .unflatten()
            .execute(flat_str.as_str())
            .unwrap();
    });

    // "Batch processing" targets: parallel path (threshold=1 forces it).
    secs("batch_flatten", "parallel", "10", &mut || {
        JSONTools::new()
            .flatten()
            .parallel_threshold(1)
            .execute(batch_10.as_slice())
            .unwrap();
    });
    secs("batch_flatten", "parallel", "100", &mut || {
        JSONTools::new()
            .flatten()
            .parallel_threshold(1)
            .execute(batch_100.as_slice())
            .unwrap();
    });
    // Sequential counterpart at the same size, so bench_compare / manual reading can
    // see the parallel speedup directly rather than inferring it across two runs.
    secs("batch_flatten", "sequential", "100", &mut || {
        JSONTools::new()
            .flatten()
            .parallel_threshold(usize::MAX)
            .execute(batch_100.as_slice())
            .unwrap();
    });

    rows
}

fn main() {
    let csv_mode = std::env::args().any(|a| a == "--csv");
    let rows = run_scenarios();

    if csv_mode {
        // Deliberately no date/time crate dependency for a single integer column —
        // Unix seconds sorts and diffs fine.
        let timestamp = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_secs())
            .unwrap_or(0);
        let commit = resolve_commit();
        let os = std::env::consts::OS;
        let arch = std::env::consts::ARCH;
        let threads = std::thread::available_parallelism()
            .map(|p| p.get())
            .unwrap_or(1);

        println!("timestamp,commit,os,arch,threads,operation,scenario,size,time_us");
        for (operation, scenario, size, time_us) in rows {
            println!(
                "{timestamp},{commit},{os},{arch},{threads},{operation},{scenario},{size},{time_us:.3}"
            );
        }
        return;
    }

    println!(
        "{:<14} {:<18} {:>6} | {:>10}",
        "operation", "scenario", "size", "time_us"
    );
    for (operation, scenario, size, time_us) in &rows {
        println!("{operation:<14} {scenario:<18} {size:>6} | {time_us:>10.3}");
    }
}
