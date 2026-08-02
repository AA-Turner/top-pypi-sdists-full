use criterion::{criterion_group, criterion_main, Criterion};
use json_tools_rs::JSONTools;
use std::hint::black_box;
use std::time::Duration;

// ============================================================================
// PART 2: SYSTEMATIC COMBINATION BENCHMARKS
// Tests combinations of features to identify interaction effects
// ============================================================================

mod test_data {
    pub fn medium_json() -> &'static str {
        r#"{
            "order": {
                "id": "ORD-2024-001234",
                "customer": {
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
                        "inStock": "true",
                        "notes": ""
                    },
                    {
                        "productId": "PROD-002",
                        "name": "USB Mouse",
                        "price": "$29.99",
                        "quantity": "1",
                        "inStock": "false",
                        "metadata": null
                    }
                ],
                "totals": {
                    "subtotal": "$171.96",
                    "tax": "$15.00",
                    "shipping": "$15.00",
                    "discount": null,
                    "total": "$186.96"
                }
            }
        }"#
    }
}

// ============================================================================
// 2-FEATURE COMBINATIONS
// ============================================================================

/// Combination: Separator + Lowercase
fn combo_2f_01_separator_lowercase(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_2f_01_separator_lowercase");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    // Baseline
    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Only separator
    group.bench_function("separator_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("::")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Only lowercase
    group.bench_function("lowercase_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Combined
    group.bench_function("combined", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("::")
                .lowercase_keys(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Combination: Lowercase + Key Replacement
fn combo_2f_02_lowercase_key_replacement(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_2f_02_lowercase_key_replacement");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("lowercase_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("key_replacement_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(first|last)Name'", "name")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("combined", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .key_replacement("r'(first|last)name'", "name")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Combination: Key Replacement + Value Replacement
fn combo_2f_03_key_value_replacement(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_2f_03_key_value_replacement");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("key_replacement_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'_id$'", "Id")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("value_replacement_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .value_replacement("@example.com", "@company.org")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("combined", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'_id$'", "Id")
                .value_replacement("@example.com", "@company.org")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Combination: Filters + Auto Type Conversion
fn combo_2f_04_filters_auto_convert(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_2f_04_filters_auto_convert");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("filters_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .remove_nulls(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("auto_convert_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("combined", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .remove_nulls(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Combination: All Filters Together
fn combo_2f_05_all_filters(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_2f_05_all_filters");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Test each pair of filters
    group.bench_function("empty_strings_and_nulls", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .remove_nulls(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("empty_objects_and_arrays", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_objects(true)
                .remove_empty_arrays(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // All 4 filters
    group.bench_function("all_four_filters", |b| {
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

// ============================================================================
// 3-FEATURE COMBINATIONS
// ============================================================================

/// Combination: Separator + Lowercase + Key Replacement
fn combo_3f_01_sep_lower_keyrep(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_3f_01_sep_lower_keyrep");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Each feature alone
    group.bench_function("separator_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("::")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("lowercase_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("key_replacement_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'_id$'", "Id")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // 2-feature combos
    group.bench_function("sep_lower", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("::")
                .lowercase_keys(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("sep_keyrep", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("::")
                .key_replacement("r'_id$'", "Id")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("lower_keyrep", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .key_replacement("r'_id$'", "id")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // All 3 combined
    group.bench_function("all_three", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("::")
                .lowercase_keys(true)
                .key_replacement("r'_id$'", "id")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Combination: Filters + Auto Convert + Collision Handling
fn combo_3f_02_filters_convert_collision(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_3f_02_filters_convert_collision");
    group.measurement_time(Duration::from_secs(3));

    let collision_json = r#"{
        "user_name": "John",
        "admin_name": "Jane",
        "user_age": "30",
        "user_email": "",
        "admin_email": null
    }"#;

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin)_'", "")
                .execute(black_box(collision_json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Individual features
    group.bench_function("filters_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin)_'", "")
                .remove_empty_strings(true)
                .remove_nulls(true)
                .execute(black_box(collision_json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("auto_convert_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin)_'", "")
                .auto_convert_types(true)
                .execute(black_box(collision_json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("collision_only", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin)_'", "")
                .handle_key_collision(true)
                .execute(black_box(collision_json))
                .expect("Failed");
            black_box(result);
        });
    });

    // All 3 combined
    group.bench_function("all_three", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin)_'", "")
                .remove_empty_strings(true)
                .remove_nulls(true)
                .auto_convert_types(true)
                .handle_key_collision(true)
                .execute(black_box(collision_json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Combination: Key Transform + Value Transform + Filters
fn combo_3f_03_key_value_filters(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_3f_03_key_value_filters");
    group.measurement_time(Duration::from_secs(3));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Individual
    group.bench_function("key_transform", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .key_replacement("r'_id$'", "id")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("value_transform", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .value_replacement("@example.com", "@company.org")
                .value_replacement("r'^\\$'", "USD ")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("filters", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .remove_empty_strings(true)
                .remove_nulls(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // All combined
    group.bench_function("all_three", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .lowercase_keys(true)
                .key_replacement("r'_id$'", "id")
                .value_replacement("@example.com", "@company.org")
                .value_replacement("r'^\\$'", "USD ")
                .remove_empty_strings(true)
                .remove_nulls(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

// ============================================================================
// MAXIMUM COMBINATION (All Features)
// ============================================================================

fn combo_max_all_features(c: &mut Criterion) {
    let mut group = c.benchmark_group("combo_max_all_features");
    group.measurement_time(Duration::from_secs(5));

    let json = test_data::medium_json();

    group.bench_function("baseline", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.bench_function("maximum_features", |b| {
        b.iter(|| {
            let result = JSONTools::new()
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
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

criterion_group!(
    combination_benches,
    combo_2f_01_separator_lowercase,
    combo_2f_02_lowercase_key_replacement,
    combo_2f_03_key_value_replacement,
    combo_2f_04_filters_auto_convert,
    combo_2f_05_all_filters,
    combo_3f_01_sep_lower_keyrep,
    combo_3f_02_filters_convert_collision,
    combo_3f_03_key_value_filters,
    combo_max_all_features,
);

criterion_main!(combination_benches);
