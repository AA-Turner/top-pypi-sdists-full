use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion};
use json_tools_rs::JSONTools;
use std::hint::black_box;
use std::time::Duration;

// ============================================================================
// PART 4: STRESS TEST BENCHMARKS
// Tests edge cases and extreme scenarios
// ============================================================================

mod stress_data {
    /// Generate deeply nested JSON (N levels deep)
    pub fn deep_nesting(depth: usize) -> String {
        let mut json = String::from("{");
        for i in 0..depth {
            json.push_str(&format!("\"level_{}\": {{", i));
        }
        json.push_str("\"value\": 42");
        for _ in 0..depth {
            json.push('}');
        }
        json.push('}');
        json
    }

    /// Generate wide object (N keys at same level)
    pub fn wide_object(width: usize) -> String {
        let mut json = String::from("{");
        for i in 0..width {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!("\"key_{}\": \"value_{}\"", i, i));
        }
        json.push('}');
        json
    }

    /// Generate large array
    pub fn large_array(size: usize) -> String {
        let mut json = String::from("{\"items\": [");
        for i in 0..size {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!(
                "{{\"id\": {}, \"name\": \"item_{}\", \"value\": {}}}",
                i,
                i,
                i * 10
            ));
        }
        json.push_str("]}");
        json
    }

    /// Unicode-heavy JSON
    pub fn unicode_heavy() -> &'static str {
        r#"{
            "user": {
                "name": "田中太郎",
                "bio": "こんにちは世界 🌍 🚀 ✨",
                "location": "東京",
                "tweets": [
                    "Rust is awesome! 🦀",
                    "Building cool stuff 🏗️",
                    "日本語でプログラミング 💻"
                ]
            },
            "metadata": {
                "emoji_tags": ["😀", "😎", "🔥", "💯"],
                "languages": ["日本語", "English", "中文", "한국어", "Русский"],
                "special_chars": "αβγδε • ◆ ★ ♠ ♥ ♦ ♣"
            },
            "math": {
                "symbols": "∑∫∂∇∞≈≠±×÷",
                "equations": "E=mc² • π≈3.14 • √2≈1.41"
            }
        }"#
    }

    /// Many small objects
    pub fn many_small_objects(count: usize) -> String {
        let mut json = String::from("{\"records\": [");
        for i in 0..count {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!(
                "{{\"id\": {}, \"active\": {}}}",
                i,
                if i % 2 == 0 { "true" } else { "false" }
            ));
        }
        json.push_str("]}");
        json
    }

    /// Mixed data types
    pub fn mixed_types() -> &'static str {
        r#"{
            "string": "hello",
            "number": 42,
            "float": 3.14159,
            "boolean_true": true,
            "boolean_false": false,
            "null_value": null,
            "empty_string": "",
            "empty_object": {},
            "empty_array": [],
            "array_mixed": [1, "two", true, null, {"nested": "object"}],
            "nested": {
                "level1": {
                    "level2": {
                        "level3": {
                            "numbers": [1, 2, 3],
                            "strings": ["a", "b", "c"],
                            "mixed": [1, "two", 3.0, true, null]
                        }
                    }
                }
            }
        }"#
    }

    /// Long string values
    pub fn long_strings() -> String {
        let long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. ".repeat(100);
        format!(
            r#"{{
                "description": "{}",
                "content": "{}",
                "notes": "{}"
            }}"#,
            long_text, long_text, long_text
        )
    }

    /// Many nulls and empty values
    pub fn many_nulls_and_empties() -> &'static str {
        r#"{
            "field1": null,
            "field2": "",
            "field3": {},
            "field4": [],
            "field5": null,
            "nested": {
                "a": null,
                "b": "",
                "c": {},
                "d": [],
                "deeper": {
                    "x": null,
                    "y": "",
                    "z": {}
                }
            },
            "array": [null, "", {}, []],
            "valid": "actual_value"
        }"#
    }

    /// Pathological regex patterns (many potential matches)
    pub fn regex_stress() -> String {
        let mut json = String::from("{");
        for i in 0..100 {
            if i > 0 {
                json.push(',');
            }
            json.push_str(&format!(
                "\"user_id_{}\": {}, \"admin_email_{}\": \"admin{}@example.com\", \"guest_name_{}\": \"Guest{}\"",
                i, i, i, i, i, i
            ));
        }
        json.push('}');
        json
    }
}

// ============================================================================
// STRESS BENCHMARKS
// ============================================================================

fn stress_01_deep_nesting(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_01_deep_nesting");
    group.measurement_time(Duration::from_secs(5));

    let depths = vec![10, 25, 50, 100];

    for depth in depths {
        let json = stress_data::deep_nesting(depth);

        group.bench_with_input(BenchmarkId::new("flatten", depth), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Failed");
                black_box(result);
            });
        });

        // With transformations
        group.bench_with_input(
            BenchmarkId::new("flatten_transform", depth),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .lowercase_keys(true)
                        .key_replacement("level_", "l")
                        .execute(black_box(json.as_str()))
                        .expect("Failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

fn stress_02_wide_objects(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_02_wide_objects");
    group.measurement_time(Duration::from_secs(5));

    let widths = vec![100, 500, 1000, 5000];

    for width in widths {
        let json = stress_data::wide_object(width);

        group.bench_with_input(BenchmarkId::new("flatten", width), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Failed");
                black_box(result);
            });
        });

        // With transformations
        group.bench_with_input(
            BenchmarkId::new("flatten_transform", width),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .lowercase_keys(true)
                        .key_replacement("key_", "k")
                        .value_replacement("value_", "v")
                        .execute(black_box(json.as_str()))
                        .expect("Failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

fn stress_03_large_arrays(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_03_large_arrays");
    group.measurement_time(Duration::from_secs(7));

    let sizes = vec![100, 500, 1000, 5000];

    for size in sizes {
        let json = stress_data::large_array(size);

        group.bench_with_input(BenchmarkId::new("flatten", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Failed");
                black_box(result);
            });
        });

        // With auto type conversion
        group.bench_with_input(
            BenchmarkId::new("flatten_auto_convert", size),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .auto_convert_types(true)
                        .execute(black_box(json.as_str()))
                        .expect("Failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

fn stress_04_unicode_heavy(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_04_unicode_heavy");
    group.measurement_time(Duration::from_secs(5));

    let json = stress_data::unicode_heavy();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Lowercase (Unicode case handling)
    group.bench_function("flatten_lowercase", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // With replacements
    group.bench_function("flatten_replacements", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .value_replacement("🚀", "rocket")
                .value_replacement("日本語", "Japanese")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn stress_05_many_small_objects(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_05_many_small_objects");
    group.measurement_time(Duration::from_secs(7));

    let counts = vec![1000, 5000, 10000];

    for count in counts {
        let json = stress_data::many_small_objects(count);

        group.bench_with_input(BenchmarkId::new("flatten", count), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Failed");
                black_box(result);
            });
        });

        // With parallel processing
        group.bench_with_input(
            BenchmarkId::new("flatten_parallel", count),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .nested_parallel_threshold(100)
                        .execute(black_box(json.as_str()))
                        .expect("Failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

fn stress_06_mixed_types(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_06_mixed_types");
    group.measurement_time(Duration::from_secs(5));

    let json = stress_data::mixed_types();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // With all filters
    group.bench_function("flatten_all_filters", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .remove_nulls(true)
                .remove_empty_objects(true)
                .remove_empty_arrays(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Roundtrip
    group.bench_function("roundtrip", |b| {
        b.iter(|| {
            let flattened = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Flatten failed");

            if let json_tools_rs::JsonOutput::Single(flat_str) = flattened {
                let result = JSONTools::new()
                    .unflatten()
                    .execute(black_box(&flat_str))
                    .expect("Unflatten failed");
                black_box(result);
            }
        });
    });

    group.finish();
}

fn stress_07_long_strings(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_07_long_strings");
    group.measurement_time(Duration::from_secs(5));

    let json = stress_data::long_strings();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    // With value replacement
    group.bench_function("flatten_value_replacement", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .value_replacement("Lorem ipsum", "Text")
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    // With regex replacement
    group.bench_function("flatten_regex_replacement", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .value_replacement("r'Lorem.*?\\.'", "Shortened.")
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn stress_08_nulls_and_empties(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_08_nulls_and_empties");
    group.measurement_time(Duration::from_secs(5));

    let json = stress_data::many_nulls_and_empties();

    // No filters (baseline)
    group.bench_function("no_filters", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Individual filters
    group.bench_function("remove_nulls_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_nulls(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("remove_empty_strings_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // All filters combined
    group.bench_function("all_filters", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .remove_nulls(true)
                .remove_empty_objects(true)
                .remove_empty_arrays(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn stress_09_regex_heavy(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_09_regex_heavy");
    group.measurement_time(Duration::from_secs(7));

    let json = stress_data::regex_stress();

    // Baseline
    group.bench_function("no_regex", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    // Single regex replacement (many matches)
    group.bench_function("single_regex", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'_id_'", "_")
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    // Multiple regex replacements
    group.bench_function("multiple_regex", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin|guest)_'", "")
                .value_replacement("r'@example\\.com$'", "@company.org")
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    // Complex regex with collision handling
    group.bench_function("regex_with_collision", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin|guest)_(id|email|name)_\\d+'", "$2")
                .handle_key_collision(true)
                .execute(black_box(json.as_str()))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn stress_10_parallel_thresholds(c: &mut Criterion) {
    let mut group = c.benchmark_group("stress_10_parallel_thresholds");
    group.measurement_time(Duration::from_secs(7));

    let json = stress_data::large_array(1000);

    let thresholds = vec![
        ("sequential", usize::MAX),
        ("threshold_50", 50),
        ("threshold_100", 100),
        ("threshold_500", 500),
        ("threshold_1000", 1000),
    ];

    for (name, threshold) in thresholds {
        group.bench_with_input(
            BenchmarkId::new("nested_parallel", name),
            &threshold,
            |b, &threshold| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .nested_parallel_threshold(threshold)
                        .lowercase_keys(true)
                        .auto_convert_types(true)
                        .execute(black_box(json.as_str()))
                        .expect("Failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

criterion_group!(
    stress_benches,
    stress_01_deep_nesting,
    stress_02_wide_objects,
    stress_03_large_arrays,
    stress_04_unicode_heavy,
    stress_05_many_small_objects,
    stress_06_mixed_types,
    stress_07_long_strings,
    stress_08_nulls_and_empties,
    stress_09_regex_heavy,
    stress_10_parallel_thresholds,
);

criterion_main!(stress_benches);
