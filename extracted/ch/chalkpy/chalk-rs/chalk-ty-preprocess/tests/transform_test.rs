use chalk_proto::chalk::arrow::v1::{arrow_type::ArrowTypeEnum, ArrowType, EmptyMessage};
use chalk_proto::chalk::graph::v1::{
    feature_type, FeatureSet, FeatureType, Graph, HasManyFeatureType, HasOneFeatureType,
    ScalarFeatureType,
};
use chalk_ty_preprocess::transform::{generate_feature_stubs, transform_source};
use chalk_ty_preprocess::type_map::build_type_map;
use prost::Message;
use std::fs;
use std::path::PathBuf;
use std::process::Command;

fn fixtures_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures")
}

/// Build a simple Graph proto for testing.
fn build_test_graph(features: &[(&str, &[(&str, ArrowTypeEnum, bool)])]) -> Graph {
    let mut feature_sets = Vec::new();
    for (namespace, fields) in features {
        let mut fts = Vec::new();
        for (name, arrow_type, is_nullable) in *fields {
            fts.push(FeatureType {
                r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                    name: name.to_string(),
                    namespace: namespace.to_string(),
                    attribute_name: name.to_string(),
                    arrow_type: Some(ArrowType {
                        arrow_type_enum: Some(arrow_type.clone()),
                    }),
                    is_nullable: *is_nullable,
                    ..Default::default()
                })),
            });
        }
        feature_sets.push(FeatureSet {
            name: namespace.to_string(),
            features: fts,
            ..Default::default()
        });
    }
    Graph {
        feature_sets,
        ..Default::default()
    }
}

fn e() -> EmptyMessage {
    EmptyMessage {}
}

/// Discover and run all fixture-based tests in tests/fixtures/.
/// For each `x.before.py`, load `x.graph` (or generate from defaults) and
/// compare the transform output against `x.after.py`.
fn run_fixture(name: &str, graph: &Graph) {
    let dir = fixtures_dir();
    let before_path = dir.join(format!("{name}.before.py"));
    let after_path = dir.join(format!("{name}.after.py"));
    let graph_path = dir.join(format!("{name}.graph"));

    // Write the graph file for reference / manual inspection.
    let graph_bytes = graph.encode_to_vec();
    fs::write(&graph_path, &graph_bytes).expect("failed to write graph fixture");

    let before = fs::read_to_string(&before_path)
        .unwrap_or_else(|_| panic!("missing fixture: {}", before_path.display()));
    let expected = fs::read_to_string(&after_path)
        .unwrap_or_else(|_| panic!("missing fixture: {}", after_path.display()));

    let type_map = build_type_map(graph);
    let actual = transform_source(&before, &type_map)
        .unwrap_or_else(|| panic!("transform_source returned None for {name}"));

    if actual != expected {
        // Show a readable diff.
        let actual_lines: Vec<&str> = actual.lines().collect();
        let expected_lines: Vec<&str> = expected.lines().collect();
        let max_lines = actual_lines.len().max(expected_lines.len());
        let mut diff = String::new();
        for i in 0..max_lines {
            let a = actual_lines.get(i).unwrap_or(&"<missing>");
            let e = expected_lines.get(i).unwrap_or(&"<missing>");
            if a != e {
                diff.push_str(&format!(
                    "  line {}: \n    expected: {e:?}\n    actual:   {a:?}\n",
                    i + 1
                ));
            }
        }
        panic!(
            "fixture mismatch for {name}:\n{diff}\n\n--- full actual ---\n{actual}\n--- full expected ---\n{expected}"
        );
    }
}

/// Run a fixture that includes diagnostics checking.
/// Transforms the source, writes it to a temp file, runs `ty check`,
/// and compares the diagnostic output against `x.diagnostics`.
///
/// The `.diagnostics` file contains one error per line in the format:
///   error[rule-name]: message
/// Lines are sorted for stable comparison. Only `error[...]` lines are compared.
fn run_fixture_with_diagnostics(name: &str, graph: &Graph) {
    let dir = fixtures_dir();
    let before_path = dir.join(format!("{name}.before.py"));
    let diagnostics_path = dir.join(format!("{name}.diagnostics"));
    let graph_path = dir.join(format!("{name}.graph"));

    // Write graph file.
    let graph_bytes = graph.encode_to_vec();
    fs::write(&graph_path, &graph_bytes).expect("failed to write graph fixture");

    let before = fs::read_to_string(&before_path)
        .unwrap_or_else(|_| panic!("missing fixture: {}", before_path.display()));

    let type_map = build_type_map(graph);
    let transformed = transform_source(&before, &type_map)
        .unwrap_or_else(|| panic!("transform_source returned None for {name}"));

    // Write transformed source to a temp directory for ty to check.
    let tmp_dir = tempfile::tempdir().expect("failed to create temp dir");
    let tmp_file = tmp_dir.path().join(format!("{name}.py"));
    fs::write(&tmp_file, &transformed).expect("failed to write temp file");

    // Also write feature stubs so ty can resolve feature class constructors.
    let stubs = generate_feature_stubs(&type_map);
    let stubs_file = tmp_dir.path().join("_chalk_stubs.py");
    fs::write(&stubs_file, &stubs).expect("failed to write stubs file");

    // Run ty check.
    let output = Command::new("ty")
        .args([
            "check",
            &tmp_file.to_string_lossy(),
            "--extra-search-path",
            &tmp_dir.path().to_string_lossy(),
        ])
        .output()
        .expect("failed to run ty — is it installed?");

    let stderr = String::from_utf8_lossy(&output.stderr);
    let stdout = String::from_utf8_lossy(&output.stdout);
    let full_output = format!("{stdout}{stderr}");

    // Extract error lines and normalize paths out (just keep the rule + message).
    let mut actual_errors: Vec<String> = full_output
        .lines()
        .filter(|line| line.starts_with("error["))
        .map(|line| line.to_string())
        .collect();
    actual_errors.sort();

    let expected_diagnostics = fs::read_to_string(&diagnostics_path)
        .unwrap_or_else(|_| panic!("missing fixture: {}", diagnostics_path.display()));
    let mut expected_errors: Vec<String> = expected_diagnostics
        .lines()
        .filter(|line| !line.is_empty() && !line.starts_with('#'))
        .map(|line| line.to_string())
        .collect();
    expected_errors.sort();

    if actual_errors != expected_errors {
        let mut msg = format!("diagnostics mismatch for {name}:\n");
        msg.push_str("\n--- expected errors ---\n");
        for e in &expected_errors {
            msg.push_str(&format!("  {e}\n"));
        }
        msg.push_str("\n--- actual errors ---\n");
        for e in &actual_errors {
            msg.push_str(&format!("  {e}\n"));
        }
        panic!("{msg}");
    }
}

#[test]
fn test_basic_resolver() {
    let graph = build_test_graph(&[(
        "user",
        &[
            ("id", ArrowTypeEnum::Int64(e()), false),
            ("name", ArrowTypeEnum::LargeUtf8(e()), false),
            ("score", ArrowTypeEnum::Float64(e()), false),
            ("today", ArrowTypeEnum::Date64(e()), false),
            ("is_active", ArrowTypeEnum::Bool(e()), false),
        ],
    )]);
    run_fixture("basic_resolver", &graph);
}

#[test]
fn test_nullable_features() {
    let graph = build_test_graph(&[(
        "user",
        &[
            ("id", ArrowTypeEnum::Int64(e()), false),
            ("name", ArrowTypeEnum::LargeUtf8(e()), true),
            ("age", ArrowTypeEnum::Int64(e()), true),
        ],
    )]);
    run_fixture("nullable_features", &graph);
}

#[test]
fn test_no_chalk_imports() {
    // An empty graph — the file has no chalk imports so should return None.
    let graph = Graph::default();
    let dir = fixtures_dir();
    let before = fs::read_to_string(dir.join("no_chalk.before.py")).unwrap();
    let type_map = build_type_map(&graph);
    assert!(
        transform_source(&before, &type_map).is_none(),
        "non-chalk files should return None"
    );
}

#[test]
fn test_features_decorator_with_args() {
    let graph = build_test_graph(&[(
        "account",
        &[
            ("id", ArrowTypeEnum::LargeUtf8(e()), false),
            ("balance", ArrowTypeEnum::Float64(e()), false),
            (
                "created_at",
                ArrowTypeEnum::Timestamp(chalk_proto::chalk::arrow::v1::Timestamp {
                    time_unit: 3, // microsecond
                    timezone: "UTC".to_string(),
                }),
                true,
            ),
        ],
    )]);
    run_fixture("decorator_args", &graph);
}

#[test]
fn test_has_one_path() {
    // Build a graph with User -> CreditReport has-one relationship.
    let credit_report_features = vec![
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "id".to_string(),
                namespace: "credit_report".to_string(),
                attribute_name: "id".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Int64(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "credit_score".to_string(),
                namespace: "credit_report".to_string(),
                attribute_name: "credit_score".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Int64(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "agency".to_string(),
                namespace: "credit_report".to_string(),
                attribute_name: "agency".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::LargeUtf8(e())),
                }),
                ..Default::default()
            })),
        },
    ];

    let user_features = vec![
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "id".to_string(),
                namespace: "user".to_string(),
                attribute_name: "id".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Int64(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "name".to_string(),
                namespace: "user".to_string(),
                attribute_name: "name".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::LargeUtf8(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::HasOne(HasOneFeatureType {
                name: "credit_report".to_string(),
                namespace: "user".to_string(),
                foreign_namespace: "credit_report".to_string(),
                is_nullable: false,
                ..Default::default()
            })),
        },
    ];

    let graph = Graph {
        feature_sets: vec![
            FeatureSet {
                name: "credit_report".to_string(),
                features: credit_report_features,
                ..Default::default()
            },
            FeatureSet {
                name: "user".to_string(),
                features: user_features,
                ..Default::default()
            },
        ],
        ..Default::default()
    };

    run_fixture("has_one_path", &graph);
}

#[test]
fn test_dataframe() {
    let transaction_features = vec![
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "id".to_string(),
                namespace: "transaction".to_string(),
                attribute_name: "id".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Int64(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "user_id".to_string(),
                namespace: "transaction".to_string(),
                attribute_name: "user_id".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Int64(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "amount".to_string(),
                namespace: "transaction".to_string(),
                attribute_name: "amount".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Float64(e())),
                }),
                ..Default::default()
            })),
        },
    ];

    let user_features = vec![
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "id".to_string(),
                namespace: "user".to_string(),
                attribute_name: "id".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::Int64(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
                name: "name".to_string(),
                namespace: "user".to_string(),
                attribute_name: "name".to_string(),
                arrow_type: Some(ArrowType {
                    arrow_type_enum: Some(ArrowTypeEnum::LargeUtf8(e())),
                }),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::HasMany(HasManyFeatureType {
                name: "transactions".to_string(),
                namespace: "user".to_string(),
                foreign_namespace: "transaction".to_string(),
                ..Default::default()
            })),
        },
    ];

    let graph = Graph {
        feature_sets: vec![
            FeatureSet {
                name: "transaction".to_string(),
                features: transaction_features,
                ..Default::default()
            },
            FeatureSet {
                name: "user".to_string(),
                features: user_features,
                ..Default::default()
            },
        ],
        ..Default::default()
    };

    run_fixture("dataframe", &graph);
}

#[test]
fn test_realistic() {
    // Realistic test covering:
    // - Mixed default/non-default fields (dataclass-field-order)
    // - Has-one and has-many relationships
    // - Forward references between classes
    // - DataFrame as return type and input
    // - Features[...] with nullable types
    // - Decorator with keyword arguments
    let ts = chalk_proto::chalk::arrow::v1::Timestamp {
        time_unit: 3,
        timezone: "UTC".to_string(),
    };

    let user_features = vec![
        scalar("user", "id", ArrowTypeEnum::Int64(e()), false),
        scalar("user", "name", ArrowTypeEnum::LargeUtf8(e()), false),
        scalar("user", "email", ArrowTypeEnum::LargeUtf8(e()), true),
        scalar("user", "score", ArrowTypeEnum::Float64(e()), false),
        scalar(
            "user",
            "created_at",
            ArrowTypeEnum::Timestamp(ts.clone()),
            false,
        ),
        FeatureType {
            r#type: Some(feature_type::Type::HasMany(HasManyFeatureType {
                name: "transactions".to_string(),
                namespace: "user".to_string(),
                foreign_namespace: "transaction".to_string(),
                ..Default::default()
            })),
        },
        FeatureType {
            r#type: Some(feature_type::Type::HasOne(HasOneFeatureType {
                name: "account".to_string(),
                namespace: "user".to_string(),
                foreign_namespace: "account".to_string(),
                is_nullable: false,
                ..Default::default()
            })),
        },
    ];

    let account_features = vec![
        scalar("account", "id", ArrowTypeEnum::LargeUtf8(e()), false),
        scalar("account", "balance", ArrowTypeEnum::Float64(e()), false),
        scalar("account", "is_active", ArrowTypeEnum::Bool(e()), false),
    ];

    let transaction_features = vec![
        scalar("transaction", "id", ArrowTypeEnum::Int64(e()), false),
        scalar("transaction", "user_id", ArrowTypeEnum::Int64(e()), false),
        scalar("transaction", "amount", ArrowTypeEnum::Float64(e()), false),
        scalar("transaction", "ts", ArrowTypeEnum::Timestamp(ts), false),
    ];

    let graph = Graph {
        feature_sets: vec![
            FeatureSet {
                name: "user".to_string(),
                features: user_features,
                ..Default::default()
            },
            FeatureSet {
                name: "account".to_string(),
                features: account_features,
                ..Default::default()
            },
            FeatureSet {
                name: "transaction".to_string(),
                features: transaction_features,
                ..Default::default()
            },
        ],
        ..Default::default()
    };

    run_fixture("realistic", &graph);
}

#[test]
fn test_stubs_no_dataclass_field_order() {
    // Verify stubs don't use @dataclass (which would cause field-order errors
    // when required fields follow fields with defaults).
    let graph = build_test_graph(&[(
        "user",
        &[
            ("id", ArrowTypeEnum::Int64(e()), false),
            ("name", ArrowTypeEnum::LargeUtf8(e()), true),
            ("score", ArrowTypeEnum::Float64(e()), false),
        ],
    )]);
    let type_map = build_type_map(&graph);
    let stubs = generate_feature_stubs(&type_map);

    // Must NOT contain @dataclass
    assert!(
        !stubs.contains("@dataclass"),
        "stubs should not use @dataclass to avoid field-order errors"
    );
    // Must define DataFrame
    assert!(
        stubs.contains("class DataFrame"),
        "stubs should define a DataFrame class"
    );
    // Must contain the class
    assert!(
        stubs.contains("class User:"),
        "stubs should contain User class"
    );
    // Must contain fields
    assert!(
        stubs.contains("    id: int"),
        "stubs should contain id field"
    );
    assert!(
        stubs.contains("    name: str"),
        "stubs should contain name field"
    );
}

#[test]
fn test_chalk_types() {
    // Tests:
    // - FeatureTime -> datetime.datetime in class fields and resolver params
    // - Primary[int] -> int in class fields
    // - No `import datetime` in header when file has `from datetime import datetime`
    let ts = chalk_proto::chalk::arrow::v1::Timestamp {
        time_unit: 3,
        timezone: "UTC".to_string(),
    };

    let graph = Graph {
        feature_sets: vec![
            FeatureSet {
                name: "user".to_string(),
                features: vec![
                    scalar("user", "id", ArrowTypeEnum::Int64(e()), false),
                    scalar("user", "name", ArrowTypeEnum::LargeUtf8(e()), false),
                    scalar("user", "email", ArrowTypeEnum::LargeUtf8(e()), true),
                    scalar(
                        "user",
                        "created_at",
                        ArrowTypeEnum::Timestamp(ts.clone()),
                        false,
                    ),
                    scalar("user", "score", ArrowTypeEnum::Float64(e()), false),
                ],
                ..Default::default()
            },
            FeatureSet {
                name: "transaction".to_string(),
                features: vec![
                    scalar("transaction", "id", ArrowTypeEnum::Int64(e()), false),
                    scalar("transaction", "user_id", ArrowTypeEnum::Int64(e()), false),
                    scalar("transaction", "amount", ArrowTypeEnum::Float64(e()), false),
                    scalar("transaction", "ts", ArrowTypeEnum::Timestamp(ts), false),
                ],
                ..Default::default()
            },
        ],
        ..Default::default()
    };

    run_fixture("chalk_types", &graph);
}

#[test]
fn test_foreign_keys() {
    // Tests:
    // - String-quoted foreign key refs: "Jar.jar_id" -> str
    // - Bare foreign key refs: User.id -> int in class field annotations
    // - Aliased datetime import: `import datetime as dt` doesn't prevent
    //   our header from adding `import datetime`
    // - FeatureTime resolved to datetime.datetime (qualified, since no
    //   `from datetime import datetime` in this file)
    let ts = chalk_proto::chalk::arrow::v1::Timestamp {
        time_unit: 3,
        timezone: "UTC".to_string(),
    };

    let graph = Graph {
        feature_sets: vec![
            FeatureSet {
                name: "jar".to_string(),
                features: vec![
                    scalar("jar", "jar_id", ArrowTypeEnum::LargeUtf8(e()), false),
                    scalar("jar", "name", ArrowTypeEnum::LargeUtf8(e()), false),
                ],
                ..Default::default()
            },
            FeatureSet {
                name: "bean".to_string(),
                features: vec![
                    scalar("bean", "bean_id", ArrowTypeEnum::Int64(e()), false),
                    scalar("bean", "jar_id", ArrowTypeEnum::LargeUtf8(e()), false),
                    scalar("bean", "name", ArrowTypeEnum::LargeUtf8(e()), false),
                    scalar("bean", "timestamp", ArrowTypeEnum::Timestamp(ts), false),
                ],
                ..Default::default()
            },
            FeatureSet {
                name: "confirmed_fraud".to_string(),
                features: vec![
                    scalar("confirmed_fraud", "id", ArrowTypeEnum::Int64(e()), false),
                    scalar(
                        "confirmed_fraud",
                        "is_fraud",
                        ArrowTypeEnum::Int64(e()),
                        false,
                    ),
                ],
                ..Default::default()
            },
            FeatureSet {
                name: "transaction".to_string(),
                features: vec![
                    scalar("transaction", "id", ArrowTypeEnum::Int64(e()), false),
                    scalar("transaction", "amount", ArrowTypeEnum::Float64(e()), false),
                    scalar("transaction", "user_id", ArrowTypeEnum::Int64(e()), false),
                ],
                ..Default::default()
            },
            FeatureSet {
                name: "user".to_string(),
                features: vec![
                    scalar("user", "id", ArrowTypeEnum::Int64(e()), false),
                    scalar("user", "name", ArrowTypeEnum::LargeUtf8(e()), false),
                ],
                ..Default::default()
            },
        ],
        ..Default::default()
    };

    run_fixture("foreign_keys", &graph);
}

#[test]
fn test_type_errors() {
    // Verifies that ty catches genuine type errors in resolver bodies
    // after our transformation.
    let graph = build_test_graph(&[(
        "user",
        &[
            ("id", ArrowTypeEnum::Int64(e()), false),
            ("name", ArrowTypeEnum::LargeUtf8(e()), false),
            ("score", ArrowTypeEnum::Float64(e()), false),
            ("is_active", ArrowTypeEnum::Bool(e()), false),
        ],
    )]);
    run_fixture_with_diagnostics("type_errors", &graph);
}

#[test]
fn test_correct_code_no_errors() {
    // Verifies that correct resolver code produces zero diagnostics.
    let graph = build_test_graph(&[(
        "user",
        &[
            ("id", ArrowTypeEnum::Int64(e()), false),
            ("name", ArrowTypeEnum::LargeUtf8(e()), false),
            ("score", ArrowTypeEnum::Float64(e()), false),
        ],
    )]);
    run_fixture_with_diagnostics("correct_code", &graph);
}

/// Helper to create a scalar FeatureType.
fn scalar(namespace: &str, name: &str, arrow_type: ArrowTypeEnum, nullable: bool) -> FeatureType {
    FeatureType {
        r#type: Some(feature_type::Type::Scalar(ScalarFeatureType {
            name: name.to_string(),
            namespace: namespace.to_string(),
            attribute_name: name.to_string(),
            arrow_type: Some(ArrowType {
                arrow_type_enum: Some(arrow_type),
            }),
            is_nullable: nullable,
            ..Default::default()
        })),
    }
}
