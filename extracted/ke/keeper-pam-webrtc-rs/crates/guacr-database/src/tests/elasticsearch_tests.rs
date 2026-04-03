use crate::elasticsearch::{
    classify_input, flatten_mapping_properties, format_json_value, format_rest_response,
    is_es_modifying_operation, parse_cat_response, parse_es_error, parse_mapping_response,
    parse_rest_call, parse_search_response, parse_sql_response, ElasticsearchConfig,
    ElasticsearchHandler, InputType, ShortcutCommand,
};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_elasticsearch_handler_new() {
    let handler = ElasticsearchHandler::with_defaults();
    assert_eq!(
        <ElasticsearchHandler as ProtocolHandler>::name(&handler),
        "elasticsearch"
    );
}

#[test]
fn test_elasticsearch_config() {
    let config = ElasticsearchConfig::default();
    assert_eq!(config.default_port, 9200);
    assert!(!config.require_auth);
    assert!(!config.require_tls);
}

#[test]
fn test_classify_input_empty() {
    assert!(matches!(classify_input(""), InputType::Empty));
    assert!(matches!(classify_input("   "), InputType::Empty));
}

#[test]
fn test_classify_input_builtin() {
    assert!(matches!(classify_input("help"), InputType::Builtin(_)));
    assert!(matches!(classify_input("?"), InputType::Builtin(_)));
    assert!(matches!(classify_input("quit"), InputType::Builtin(_)));
    assert!(matches!(classify_input("exit"), InputType::Builtin(_)));
}

#[test]
fn test_classify_input_shortcuts() {
    assert!(matches!(
        classify_input("\\indices"),
        InputType::Shortcut(ShortcutCommand::Indices)
    ));
    assert!(matches!(
        classify_input("\\i"),
        InputType::Shortcut(ShortcutCommand::Indices)
    ));
    assert!(matches!(
        classify_input("\\health"),
        InputType::Shortcut(ShortcutCommand::Health)
    ));
    assert!(matches!(
        classify_input("\\h"),
        InputType::Shortcut(ShortcutCommand::Health)
    ));
    assert!(matches!(
        classify_input("\\nodes"),
        InputType::Shortcut(ShortcutCommand::Nodes)
    ));
    assert!(matches!(
        classify_input("\\n"),
        InputType::Shortcut(ShortcutCommand::Nodes)
    ));
    assert!(matches!(
        classify_input("\\d my_index"),
        InputType::Shortcut(ShortcutCommand::Describe(_))
    ));
    if let InputType::Shortcut(ShortcutCommand::Describe(idx)) = classify_input("\\d my_index") {
        assert_eq!(idx, "my_index");
    }
}

#[test]
fn test_classify_input_describe() {
    assert!(matches!(
        classify_input("DESCRIBE my_index"),
        InputType::Shortcut(ShortcutCommand::Describe(_))
    ));
    assert!(matches!(
        classify_input("desc my_index"),
        InputType::Shortcut(ShortcutCommand::Describe(_))
    ));
}

#[test]
fn test_classify_input_sql() {
    assert!(matches!(
        classify_input("SELECT * FROM my_index"),
        InputType::Sql(_)
    ));
    assert!(matches!(classify_input("SHOW TABLES"), InputType::Sql(_)));
}

#[test]
fn test_classify_input_rest_call() {
    assert!(matches!(
        classify_input("GET /_cat/indices"),
        InputType::RestCall { .. }
    ));
    assert!(matches!(
        classify_input("PUT /my-index"),
        InputType::RestCall { .. }
    ));
    assert!(matches!(
        classify_input("DELETE /my-index"),
        InputType::RestCall { .. }
    ));
}

#[test]
fn test_classify_input_rest_call_with_body() {
    let input = "POST /my-index/_doc {\"name\": \"test\"}";
    if let InputType::RestCall { method, path, body } = classify_input(input) {
        assert_eq!(method, "POST");
        assert_eq!(path, "/my-index/_doc");
        assert!(body.is_some());
        assert_eq!(body.unwrap()["name"], "test");
    } else {
        panic!("Expected RestCall");
    }
}

#[test]
fn test_classify_input_json_search() {
    let input = "my_index {\"query\": {\"match_all\": {}}}";
    if let InputType::JsonSearch { index, body } = classify_input(input) {
        assert_eq!(index, "my_index");
        assert!(body.get("query").is_some());
    } else {
        panic!("Expected JsonSearch");
    }
}

#[test]
fn test_classify_input_json_search_no_index() {
    let input = "{\"query\": {\"match_all\": {}}}";
    if let InputType::JsonSearch { index, body } = classify_input(input) {
        assert_eq!(index, "_all");
        assert!(body.get("query").is_some());
    } else {
        panic!("Expected JsonSearch");
    }
}

#[test]
fn test_is_es_modifying_operation() {
    assert!(is_es_modifying_operation("PUT /my-index"));
    assert!(is_es_modifying_operation("DELETE /my-index"));
    assert!(is_es_modifying_operation("POST /my-index/_doc"));
    assert!(!is_es_modifying_operation("GET /_cat/indices"));
    assert!(!is_es_modifying_operation("POST /_sql"));
    assert!(!is_es_modifying_operation("POST /my-index/_search"));
    assert!(!is_es_modifying_operation("POST /my-index/_msearch"));
}

#[test]
fn test_format_json_value() {
    assert_eq!(format_json_value(&serde_json::Value::Null), "NULL");
    assert_eq!(format_json_value(&serde_json::Value::Bool(true)), "true");
    assert_eq!(format_json_value(&serde_json::json!(42)), "42");
    assert_eq!(format_json_value(&serde_json::json!("hello")), "hello");
    assert_eq!(
        format_json_value(&serde_json::json!([1, 2, 3])),
        "[1, 2, 3]"
    );
}

#[test]
fn test_parse_sql_response() {
    let json = serde_json::json!({
        "columns": [
            {"name": "id", "type": "integer"},
            {"name": "name", "type": "text"}
        ],
        "rows": [
            [1, "Alice"],
            [2, "Bob"]
        ]
    });

    let result = parse_sql_response(&json).unwrap();
    assert_eq!(result.columns, vec!["id", "name"]);
    assert_eq!(result.rows.len(), 2);
    assert_eq!(result.rows[0], vec!["1", "Alice"]);
    assert_eq!(result.rows[1], vec!["2", "Bob"]);
}

#[test]
fn test_parse_sql_response_empty() {
    let json = serde_json::json!({
        "columns": [
            {"name": "id", "type": "integer"}
        ],
        "rows": []
    });

    let result = parse_sql_response(&json).unwrap();
    assert_eq!(result.columns, vec!["id"]);
    assert_eq!(result.rows.len(), 0);
}

#[test]
fn test_parse_search_response() {
    let json = serde_json::json!({
        "hits": {
            "total": {"value": 2},
            "hits": [
                {
                    "_id": "1",
                    "_source": {"name": "Alice", "age": 30}
                },
                {
                    "_id": "2",
                    "_source": {"name": "Bob", "age": 25}
                }
            ]
        }
    });

    let result = parse_search_response(&json).unwrap();
    assert!(result.columns.contains(&"_id".to_string()));
    assert!(result.columns.contains(&"name".to_string()));
    assert!(result.columns.contains(&"age".to_string()));
    assert_eq!(result.rows.len(), 2);
    assert_eq!(result.affected_rows, Some(2));
}

#[test]
fn test_parse_search_response_empty() {
    let json = serde_json::json!({
        "hits": {
            "total": {"value": 0},
            "hits": []
        }
    });

    let result = parse_search_response(&json).unwrap();
    assert_eq!(result.columns, vec!["(no results)"]);
    assert_eq!(result.rows.len(), 1);
}

#[test]
fn test_parse_search_response_mixed_fields() {
    let json = serde_json::json!({
        "hits": {
            "total": {"value": 2},
            "hits": [
                {
                    "_id": "1",
                    "_source": {"name": "Alice"}
                },
                {
                    "_id": "2",
                    "_source": {"name": "Bob", "email": "bob@test.com"}
                }
            ]
        }
    });

    let result = parse_search_response(&json).unwrap();
    // Both name and email should be columns
    assert!(result.columns.contains(&"name".to_string()));
    assert!(result.columns.contains(&"email".to_string()));
    // First row should have NULL for email
    let email_idx = result.columns.iter().position(|c| c == "email").unwrap();
    assert_eq!(result.rows[0][email_idx], "NULL");
    assert_eq!(result.rows[1][email_idx], "bob@test.com");
}

#[test]
fn test_parse_cat_response() {
    let json = serde_json::json!([
        {"health": "green", "index": "test-index", "docs.count": "100"},
        {"health": "yellow", "index": "other-index", "docs.count": "50"}
    ]);

    let result = parse_cat_response(&json).unwrap();
    assert!(result.columns.contains(&"health".to_string()));
    assert!(result.columns.contains(&"index".to_string()));
    assert_eq!(result.rows.len(), 2);
}

#[test]
fn test_parse_cat_response_empty() {
    let json = serde_json::json!([]);
    let result = parse_cat_response(&json).unwrap();
    assert_eq!(result.columns, vec!["(empty)"]);
}

#[test]
fn test_parse_mapping_response() {
    let json = serde_json::json!({
        "test-index": {
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "age": {"type": "integer"},
                    "address": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "keyword"},
                            "zip": {"type": "keyword"}
                        }
                    }
                }
            }
        }
    });

    let result = parse_mapping_response(&json, "test-index").unwrap();
    assert_eq!(result.columns, vec!["field", "type"]);
    let field_names: Vec<&String> = result.rows.iter().map(|r| &r[0]).collect();
    assert!(field_names.contains(&&"name".to_string()));
    assert!(field_names.contains(&&"age".to_string()));
    assert!(field_names.contains(&&"address".to_string()));
    assert!(field_names.contains(&&"address.city".to_string()));
    assert!(field_names.contains(&&"address.zip".to_string()));
}

#[test]
fn test_parse_mapping_response_fallback() {
    // Test with different index name in response (alias scenario)
    let json = serde_json::json!({
        "actual-index-name": {
            "mappings": {
                "properties": {
                    "field1": {"type": "text"}
                }
            }
        }
    });

    let result = parse_mapping_response(&json, "alias-name").unwrap();
    assert_eq!(result.rows.len(), 1);
    assert_eq!(result.rows[0][0], "field1");
}

#[test]
fn test_parse_es_error() {
    let body = r#"{"error":{"type":"parsing_exception","reason":"Unknown query"},"status":400}"#;
    let msg = parse_es_error(body, 400);
    assert!(msg.contains("parsing_exception"));
    assert!(msg.contains("Unknown query"));
}

#[test]
fn test_parse_es_error_string() {
    let body = r#"{"error":"something went wrong"}"#;
    let msg = parse_es_error(body, 500);
    assert!(msg.contains("something went wrong"));
}

#[test]
fn test_parse_es_error_plain_text() {
    let body = "Not Found";
    let msg = parse_es_error(body, 404);
    assert!(msg.contains("Not Found"));
    assert!(msg.contains("404"));
}

#[test]
fn test_format_rest_response_json() {
    let text = r#"{"status":"green","cluster_name":"test"}"#;
    let formatted = format_rest_response(text);
    assert!(formatted.contains('\n'));
    assert!(formatted.contains("green"));
}

#[test]
fn test_format_rest_response_plain() {
    let text = "Not JSON content";
    let formatted = format_rest_response(text);
    assert_eq!(formatted, text);
}

#[test]
fn test_flatten_mapping_properties() {
    let properties: serde_json::Map<String, serde_json::Value> = serde_json::from_str(
        r#"{
            "name": {"type": "text"},
            "nested": {
                "type": "object",
                "properties": {
                    "inner": {"type": "keyword"}
                }
            }
        }"#,
    )
    .unwrap();

    let mut rows = Vec::new();
    flatten_mapping_properties(&properties, "", &mut rows);

    assert_eq!(rows.len(), 3);
    let field_names: Vec<&String> = rows.iter().map(|r| &r[0]).collect();
    assert!(field_names.contains(&&"name".to_string()));
    assert!(field_names.contains(&&"nested".to_string()));
    assert!(field_names.contains(&&"nested.inner".to_string()));
}

#[test]
fn test_parse_rest_call_method_path() {
    if let InputType::RestCall {
        method, path, body, ..
    } = parse_rest_call("GET /_cluster/health")
    {
        assert_eq!(method, "GET");
        assert_eq!(path, "/_cluster/health");
        assert!(body.is_none());
    } else {
        panic!("Expected RestCall");
    }
}

#[test]
fn test_parse_rest_call_with_json_body() {
    if let InputType::RestCall {
        method, path, body, ..
    } = parse_rest_call("PUT /my-index {\"settings\": {\"number_of_shards\": 1}}")
    {
        assert_eq!(method, "PUT");
        assert_eq!(path, "/my-index");
        assert!(body.is_some());
        let b = body.unwrap();
        assert_eq!(b["settings"]["number_of_shards"], 1);
    } else {
        panic!("Expected RestCall");
    }
}
