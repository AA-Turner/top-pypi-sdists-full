use criterion::{criterion_group, criterion_main, BenchmarkId, Criterion};
use json_tools_rs::{JSONTools, JsonOutput};
use std::hint::black_box;
use std::time::Duration;

// ============================================================================
// Inline Test Data - Four sizes for comprehensive performance analysis
// ============================================================================

/// Small JSON (~1KB) - Simple nested user profile
fn small_json() -> &'static str {
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

/// Medium JSON (~10KB) - E-commerce order with products
fn medium_json() -> &'static str {
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
                },
                "billingAddress": {
                    "street": "456 Oak Ave",
                    "city": "San Francisco",
                    "state": "CA",
                    "zipCode": "94103",
                    "country": "USA"
                }
            },
            "items": [
                {
                    "productId": "PROD-001",
                    "name": "Wireless Keyboard",
                    "category": "Electronics",
                    "price": "$59.99",
                    "quantity": "2",
                    "discount": "10",
                    "total": "$107.98",
                    "inStock": "true",
                    "specifications": {
                        "brand": "TechCorp",
                        "model": "WK-2000",
                        "color": "Black",
                        "wireless": "true",
                        "batteryLife": "12 months"
                    }
                },
                {
                    "productId": "PROD-002",
                    "name": "USB Mouse",
                    "category": "Electronics",
                    "price": "$29.99",
                    "quantity": "1",
                    "discount": "0",
                    "total": "$29.99",
                    "inStock": "true",
                    "specifications": {
                        "brand": "TechCorp",
                        "model": "UM-500",
                        "color": "Silver",
                        "wireless": "false",
                        "dpi": "1600"
                    }
                },
                {
                    "productId": "PROD-003",
                    "name": "Monitor Stand",
                    "category": "Accessories",
                    "price": "$39.99",
                    "quantity": "1",
                    "discount": "15",
                    "total": "$33.99",
                    "inStock": "true",
                    "specifications": {
                        "brand": "ErgoDesk",
                        "model": "MS-100",
                        "material": "Aluminum",
                        "adjustable": "true",
                        "maxWeight": "20"
                    }
                }
            ],
            "shipping": {
                "method": "Express",
                "cost": "$15.00",
                "carrier": "FastShip",
                "trackingNumber": "TRACK-987654321",
                "estimatedDelivery": "2024-01-15",
                "address": {
                    "street": "123 Main St",
                    "city": "San Francisco",
                    "state": "CA",
                    "zipCode": "94102",
                    "country": "USA"
                }
            },
            "payment": {
                "method": "Credit Card",
                "cardType": "Visa",
                "lastFourDigits": "1234",
                "amount": "$186.96",
                "currency": "USD",
                "transactionId": "TXN-ABC123XYZ",
                "status": "completed",
                "timestamp": "2024-01-10T14:30:00Z"
            },
            "totals": {
                "subtotal": "$171.96",
                "tax": "$15.00",
                "shipping": "$15.00",
                "discount": "$14.00",
                "total": "$186.96"
            },
            "status": "processing",
            "createdAt": "2024-01-10T14:30:00Z",
            "updatedAt": "2024-01-10T15:45:00Z"
        }
    }"#
}

/// Large JSON (~50KB) - Complex API response with deep nesting
fn large_json() -> &'static str {
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
                            "state": "California",
                            "zipCode": "94105",
                            "country": "USA"
                        },
                        "contact": {
                            "phone": "+1-555-0100",
                            "email": "info@techcorp.com",
                            "website": "https://techcorp.com",
                            "support": ""
                        }
                    },
                    "departments": [
                        {
                            "id": "DEPT-001",
                            "name": "Engineering",
                            "headCount": "1200",
                            "budget": "$50000000",
                            "manager": {
                                "id": "EMP-10001",
                                "name": "Alice Johnson",
                                "title": "VP of Engineering",
                                "email": "alice.j@techcorp.com",
                                "phone": "+1-555-0101",
                                "startDate": "2010-03-15",
                                "salary": "$250000"
                            },
                            "teams": [
                                {
                                    "id": "TEAM-001",
                                    "name": "Backend Services",
                                    "size": "25",
                                    "lead": "Bob Smith",
                                    "projects": [
                                        {
                                            "id": "PROJ-001",
                                            "name": "API Gateway",
                                            "status": "active",
                                            "priority": "high",
                                            "startDate": "2023-01-01",
                                            "endDate": null,
                                            "budget": "$1000000",
                                            "progress": "75"
                                        },
                                        {
                                            "id": "PROJ-002",
                                            "name": "Database Migration",
                                            "status": "completed",
                                            "priority": "critical",
                                            "startDate": "2022-06-01",
                                            "endDate": "2023-12-31",
                                            "budget": "$500000",
                                            "progress": "100"
                                        }
                                    ]
                                },
                                {
                                    "id": "TEAM-002",
                                    "name": "Frontend Development",
                                    "size": "20",
                                    "lead": "Carol White",
                                    "projects": [
                                        {
                                            "id": "PROJ-003",
                                            "name": "Dashboard Redesign",
                                            "status": "active",
                                            "priority": "medium",
                                            "startDate": "2023-09-01",
                                            "endDate": null,
                                            "budget": "$300000",
                                            "progress": "50"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "id": "DEPT-002",
                            "name": "Sales",
                            "headCount": "500",
                            "budget": "$20000000",
                            "manager": {
                                "id": "EMP-10002",
                                "name": "David Brown",
                                "title": "VP of Sales",
                                "email": "david.b@techcorp.com",
                                "phone": "+1-555-0102",
                                "startDate": "2012-07-20",
                                "salary": "$300000"
                            },
                            "teams": [
                                {
                                    "id": "TEAM-003",
                                    "name": "Enterprise Sales",
                                    "size": "50",
                                    "lead": "Eve Davis",
                                    "projects": []
                                },
                                {
                                    "id": "TEAM-004",
                                    "name": "SMB Sales",
                                    "size": "30",
                                    "lead": "Frank Miller",
                                    "projects": []
                                }
                            ]
                        },
                        {
                            "id": "DEPT-003",
                            "name": "Marketing",
                            "headCount": "200",
                            "budget": "$15000000",
                            "manager": {
                                "id": "EMP-10003",
                                "name": "Grace Wilson",
                                "title": "VP of Marketing",
                                "email": "grace.w@techcorp.com",
                                "phone": "+1-555-0103",
                                "startDate": "2015-02-10",
                                "salary": "$220000"
                            },
                            "teams": [
                                {
                                    "id": "TEAM-005",
                                    "name": "Digital Marketing",
                                    "size": "15",
                                    "lead": "Henry Taylor",
                                    "projects": [
                                        {
                                            "id": "PROJ-004",
                                            "name": "Social Media Campaign",
                                            "status": "active",
                                            "priority": "high",
                                            "startDate": "2024-01-01",
                                            "endDate": "2024-06-30",
                                            "budget": "$500000",
                                            "progress": "10"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "financials": {
                        "year": 2023,
                        "quarter": "Q4",
                        "revenue": {
                            "total": "$150000000",
                            "product": "$100000000",
                            "services": "$50000000",
                            "byRegion": {
                                "northAmerica": "$90000000",
                                "europe": "$40000000",
                                "asia": "$20000000"
                            }
                        },
                        "expenses": {
                            "total": "$100000000",
                            "salaries": "$60000000",
                            "operations": "$25000000",
                            "marketing": "$10000000",
                            "rd": "$5000000"
                        },
                        "profit": {
                            "gross": "$50000000",
                            "net": "$40000000",
                            "margin": "26.67"
                        }
                    }
                }
            },
            "pagination": {
                "page": "1",
                "pageSize": "50",
                "totalPages": "1",
                "totalRecords": "1",
                "hasNext": "false",
                "hasPrevious": "false"
            },
            "links": {
                "self": "https://api.techcorp.com/v2/companies/COMP-12345",
                "departments": "https://api.techcorp.com/v2/companies/COMP-12345/departments",
                "employees": "https://api.techcorp.com/v2/companies/COMP-12345/employees"
            }
        }
    }"#
}

/// XLarge JSON (~500KB) - Large dataset with many records
fn xlarge_json() -> String {
    let mut json =
        String::from(r#"{"dataset": {"name": "user_database", "version": "1.0", "records": ["#);

    for i in 0..1000 {
        if i > 0 {
            json.push(',');
        }
        json.push_str(&format!(
            r#"{{"id": "{}", "firstName": "User{}", "lastName": "LastName{}", "email": "user{}@example.com", "age": "{}", "city": "City{}", "country": "Country{}", "phone": "+1-555-{:04}", "active": "{}", "balance": "${}.{:02}", "registeredDate": "2023-{:02}-{:02}", "tags": ["tag1", "tag2", "tag3"], "preferences": {{"theme": "dark", "language": "en", "notifications": "true"}}, "address": {{"street": "{} Main St", "city": "City{}", "state": "State{}", "zipCode": "{:05}", "country": "Country{}"}}, "orders": [{{"orderId": "ORD-{}", "amount": "${}", "status": "completed"}}, {{"orderId": "ORD-{}", "amount": "${}", "status": "pending"}}]}}"#,
            i,
            i,
            i,
            i,
            20 + (i % 50),
            i % 100,
            i % 20,
            i,
            if i % 2 == 0 { "true" } else { "false" },
            1000 + (i % 9000),
            i % 100,
            1 + (i % 12),
            1 + (i % 28),
            100 + i,
            i % 100,
            i % 50,
            10000 + i,
            i % 20,
            i * 10,
            100 + (i % 500),
            (i * 10) + 1,
            50 + (i % 300)
        ));
    }

    json.push_str(r#"]}}"#);
    json
}

// ============================================================================
// Benchmark Groups
// ============================================================================

/// Benchmark 1: Baseline - Basic flatten/unflatten operations
fn bench_baseline(c: &mut Criterion) {
    let mut group = c.benchmark_group("01_baseline");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("flatten", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });

        // Create flattened version for unflatten benchmark
        let flattened = JSONTools::new()
            .flatten()
            .execute(&json)
            .expect("Flatten failed");

        if let JsonOutput::Single(flattened_str) = flattened {
            group.bench_with_input(
                BenchmarkId::new("unflatten", size),
                &flattened_str,
                |b, json| {
                    b.iter(|| {
                        let result = JSONTools::new()
                            .unflatten()
                            .execute(black_box(json.as_str()))
                            .expect("Unflatten failed");
                        black_box(result);
                    });
                },
            );
        }
    }

    group.finish();
}

/// Benchmark 2: Separator configurations
fn bench_separator(c: &mut Criterion) {
    let mut group = c.benchmark_group("02_separator");
    group.measurement_time(Duration::from_secs(5));

    let separators = vec![
        ("dot", "."),
        ("double_colon", "::"),
        ("underscore", "_"),
        ("double_underscore", "__"),
    ];

    for (name, sep) in &separators {
        group.bench_with_input(
            BenchmarkId::new("medium", name),
            &(medium_json(), *sep),
            |b, (json, sep)| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .separator(black_box(*sep))
                        .execute(black_box(*json))
                        .expect("Flatten failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

/// Benchmark 3: Lowercase keys
fn bench_lowercase_keys(c: &mut Criterion) {
    let mut group = c.benchmark_group("03_lowercase_keys");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("enabled", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .lowercase_keys(true)
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 4: Key replacement (literal and regex)
fn bench_key_replacement(c: &mut Criterion) {
    let mut group = c.benchmark_group("04_key_replacement");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        // Literal replacement
        group.bench_with_input(BenchmarkId::new("literal", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .key_replacement("name", "fullName")
                    .key_replacement("email", "emailAddress")
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });

        // Regex replacement
        group.bench_with_input(BenchmarkId::new("regex", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .key_replacement("r'(first|last)Name'", "name")
                    .key_replacement("r'_id$'", "Id")
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 5: Value replacement (literal and regex)
fn bench_value_replacement(c: &mut Criterion) {
    let mut group = c.benchmark_group("05_value_replacement");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        // Literal replacement
        group.bench_with_input(BenchmarkId::new("literal", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .value_replacement("@example.com", "@company.org")
                    .value_replacement("USA", "United States")
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });

        // Regex replacement
        group.bench_with_input(BenchmarkId::new("regex", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .value_replacement("r'@example\\.com$'", "@company.org")
                    .value_replacement("r'^\\+1-555-'", "+1-800-")
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 6: Individual filters
fn bench_individual_filters(c: &mut Criterion) {
    let mut group = c.benchmark_group("06_individual_filters");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(
            BenchmarkId::new("remove_empty_strings", size),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .remove_empty_strings(true)
                        .execute(black_box(json.as_str()))
                        .expect("Flatten failed");
                    black_box(result);
                });
            },
        );

        group.bench_with_input(BenchmarkId::new("remove_nulls", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .remove_nulls(true)
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });

        group.bench_with_input(
            BenchmarkId::new("remove_empty_objects", size),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .remove_empty_objects(true)
                        .execute(black_box(json.as_str()))
                        .expect("Flatten failed");
                    black_box(result);
                });
            },
        );

        group.bench_with_input(
            BenchmarkId::new("remove_empty_arrays", size),
            &json,
            |b, json| {
                b.iter(|| {
                    let result = JSONTools::new()
                        .flatten()
                        .remove_empty_arrays(true)
                        .execute(black_box(json.as_str()))
                        .expect("Flatten failed");
                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

/// Benchmark 7: All filters combined
fn bench_all_filters(c: &mut Criterion) {
    let mut group = c.benchmark_group("07_all_filters");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("combined", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .remove_empty_strings(true)
                    .remove_nulls(true)
                    .remove_empty_objects(true)
                    .remove_empty_arrays(true)
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 8: Key collision handling
fn bench_key_collision(c: &mut Criterion) {
    let mut group = c.benchmark_group("08_key_collision");
    group.measurement_time(Duration::from_secs(5));

    // JSON designed to create collisions
    let collision_json = r#"{
        "user_name": "John",
        "admin_name": "Jane",
        "guest_name": "Bob",
        "user_email": "john@example.com",
        "admin_email": "jane@example.com",
        "guest_email": "bob@example.com",
        "user_age": "30",
        "admin_age": "35",
        "guest_age": "25"
    }"#;

    group.bench_function("without_collision_handling", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin|guest)_'", "")
                .execute(black_box(collision_json))
                .expect("Flatten failed");
            black_box(result);
        });
    });

    group.bench_function("with_collision_handling", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'(user|admin|guest)_'", "")
                .handle_key_collision(true)
                .execute(black_box(collision_json))
                .expect("Flatten failed");
            black_box(result);
        });
    });

    group.finish();
}

/// Benchmark 9: Auto type conversion
fn bench_auto_type_conversion(c: &mut Criterion) {
    let mut group = c.benchmark_group("09_auto_type_conversion");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("disabled", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });

        group.bench_with_input(BenchmarkId::new("enabled", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .auto_convert_types(true)
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 10: All key transformations combined
fn bench_all_key_transformations(c: &mut Criterion) {
    let mut group = c.benchmark_group("10_all_key_transformations");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("combined", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .separator("::")
                    .lowercase_keys(true)
                    .key_replacement("r'_id$'", "Id")
                    .key_replacement("name", "fullName")
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 11: All value transformations combined
fn bench_all_value_transformations(c: &mut Criterion) {
    let mut group = c.benchmark_group("11_all_value_transformations");
    group.measurement_time(Duration::from_secs(5));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("combined", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .value_replacement("@example.com", "@company.org")
                    .value_replacement("r'^USA$'", "United States")
                    .value_replacement("r'^\\+1-555-'", "+1-800-")
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 12: Comprehensive transformation (all features)
fn bench_comprehensive(c: &mut Criterion) {
    let mut group = c.benchmark_group("12_comprehensive");
    group.measurement_time(Duration::from_secs(7));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        group.bench_with_input(BenchmarkId::new("all_features", size), &json, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .separator("::")
                    .lowercase_keys(true)
                    .key_replacement("r'_id$'", "Id")
                    .key_replacement("name", "fullName")
                    .value_replacement("@example.com", "@company.org")
                    .value_replacement("r'^USA$'", "United States")
                    .remove_empty_strings(true)
                    .remove_nulls(true)
                    .remove_empty_objects(true)
                    .remove_empty_arrays(true)
                    .auto_convert_types(true)
                    .handle_key_collision(true)
                    .execute(black_box(json.as_str()))
                    .expect("Comprehensive flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 13: Roundtrip (flatten → unflatten)
fn bench_roundtrip(c: &mut Criterion) {
    let mut group = c.benchmark_group("13_roundtrip");
    group.measurement_time(Duration::from_secs(7));

    let test_cases = vec![
        ("small", small_json().to_string()),
        ("medium", medium_json().to_string()),
        ("large", large_json().to_string()),
        ("xlarge", xlarge_json()),
    ];

    for (size, json) in test_cases {
        // Basic roundtrip
        group.bench_with_input(BenchmarkId::new("basic", size), &json, |b, json| {
            b.iter(|| {
                let flattened = JSONTools::new()
                    .flatten()
                    .execute(black_box(json.as_str()))
                    .expect("Flatten failed");

                let flattened_str = match flattened {
                    JsonOutput::Single(s) => s,
                    JsonOutput::Multiple(_) => panic!("Unexpected multiple output"),
                };

                let result = JSONTools::new()
                    .unflatten()
                    .execute(black_box(&flattened_str))
                    .expect("Unflatten failed");

                black_box(result);
            });
        });

        // Roundtrip with transformations
        group.bench_with_input(
            BenchmarkId::new("with_transformations", size),
            &json,
            |b, json| {
                b.iter(|| {
                    let flattened = JSONTools::new()
                        .flatten()
                        .separator("::")
                        .lowercase_keys(true)
                        .remove_empty_strings(true)
                        .remove_nulls(true)
                        .auto_convert_types(true)
                        .execute(black_box(json.as_str()))
                        .expect("Flatten failed");

                    let flattened_str = match flattened {
                        JsonOutput::Single(s) => s,
                        JsonOutput::Multiple(_) => panic!("Unexpected multiple output"),
                    };

                    let result = JSONTools::new()
                        .unflatten()
                        .separator("::")
                        .execute(black_box(&flattened_str))
                        .expect("Unflatten failed");

                    black_box(result);
                });
            },
        );
    }

    group.finish();
}

/// Benchmark 14: Batch processing (parallel vs sequential)
fn bench_batch_processing(c: &mut Criterion) {
    let mut group = c.benchmark_group("14_batch_processing");
    group.measurement_time(Duration::from_secs(10));

    let batch_sizes = vec![1, 5, 10, 50, 100];

    for &size in &batch_sizes {
        // Create batch by repeating small JSON
        let batch: Vec<&str> = (0..size).map(|_| small_json()).collect();

        // Sequential (threshold = usize::MAX to disable parallel)
        group.bench_with_input(BenchmarkId::new("sequential", size), &batch, |b, batch| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .parallel_threshold(usize::MAX)
                    .execute(black_box(batch.as_slice()))
                    .expect("Sequential batch failed");
                black_box(result);
            });
        });

        // Parallel (threshold = 1 to always use parallel)
        group.bench_with_input(BenchmarkId::new("parallel", size), &batch, |b, batch| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .parallel_threshold(1)
                    .execute(black_box(batch.as_slice()))
                    .expect("Parallel batch failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

/// Benchmark 15: Nested parallelism (large documents)
fn bench_nested_parallelism(c: &mut Criterion) {
    let mut group = c.benchmark_group("15_nested_parallelism");
    group.measurement_time(Duration::from_secs(10));

    let xlarge = xlarge_json();

    let thresholds = vec![
        ("sequential", usize::MAX),
        ("threshold_50", 50),
        ("threshold_100", 100),
        ("threshold_500", 500),
    ];

    for (name, threshold) in &thresholds {
        group.bench_with_input(BenchmarkId::new("xlarge", name), &xlarge, |b, json| {
            b.iter(|| {
                let result = JSONTools::new()
                    .flatten()
                    .nested_parallel_threshold(*threshold)
                    .execute(black_box(json))
                    .expect("Flatten failed");
                black_box(result);
            });
        });
    }

    group.finish();
}

criterion_group!(
    benches,
    bench_baseline,
    bench_separator,
    bench_lowercase_keys,
    bench_key_replacement,
    bench_value_replacement,
    bench_individual_filters,
    bench_all_filters,
    bench_key_collision,
    bench_auto_type_conversion,
    bench_all_key_transformations,
    bench_all_value_transformations,
    bench_comprehensive,
    bench_roundtrip,
    bench_batch_processing,
    bench_nested_parallelism
);

criterion_main!(benches);
