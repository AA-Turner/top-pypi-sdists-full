//! One isolated example per `JSONTools` builder feature.
//!
//! Companion to `feature_combinations.rs`, which shows curated multi-feature
//! pipelines. Run with: `cargo run --example feature_by_feature`

use json_tools_rs::{
    BooleanConversionConfig, DateConversionConfig, JSONTools, JsonOutput, NullConversionConfig,
    NumberConversionConfig,
};

fn single(result: Result<JsonOutput, impl std::fmt::Display>) -> String {
    match result {
        Ok(JsonOutput::Single(s)) => s,
        Ok(JsonOutput::Multiple(_)) => "<unexpected multiple results>".to_string(),
        Err(e) => format!("<error: {}>", e),
    }
}

fn main() {
    println!("JSON Tools RS - Feature by Feature");
    println!("===================================\n");

    // 1. Mode: flatten
    println!("1. Mode: flatten()");
    let input = r#"{"user":{"name":"John","address":{"city":"NYC","zip":"10001"}}}"#;
    let out = single(JSONTools::new().flatten().execute(input));
    println!("   In:  {input}\n   Out: {out}\n");

    // 2. Mode: unflatten
    println!("2. Mode: unflatten()");
    let input = r#"{"user.name":"John","user.address.city":"NYC"}"#;
    let out = single(JSONTools::new().unflatten().execute(input));
    println!("   In:  {input}\n   Out: {out}\n");

    // 3. Mode: normal (transform in place, no restructuring)
    println!("3. Mode: normal()");
    let input = r#"{"user":{"name":"John","age":null}}"#;
    let out = single(JSONTools::new().normal().remove_nulls(true).execute(input));
    println!("   In:  {input}\n   Out: {out}");
    println!("   Note: nulls removed but nesting preserved (no dot notation)\n");

    // 4. separator()
    println!("4. separator()");
    let input = r#"{"user":{"profile":{"city":"NYC"}}}"#;
    let out = single(JSONTools::new().flatten().separator("::").execute(input));
    println!("   In:  {input}\n   Out: {out}\n");

    // 5. lowercase_keys()
    println!("5. lowercase_keys()");
    let input = r#"{"User":{"Name":"John"}}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 6. key_replacement() - literal
    println!("6. key_replacement() - literal match");
    let input = r#"{"user_name":"John"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .key_replacement("user_", "")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 7. key_replacement() - regex (wrap pattern in r'...')
    println!("7. key_replacement() - regex match");
    let input = r#"{"user_id":1,"account_id":2}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .key_replacement("r'_id$'", "_key")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 8. value_replacement() - literal
    println!("8. value_replacement() - literal match");
    let input = r#"{"email":"john@example.com"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .value_replacement("@example.com", "@company.org")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 9. value_replacement() - regex
    println!("9. value_replacement() - regex match");
    let input = r#"{"phone":"555-1234","fax":"555-5678"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .value_replacement("r'^555-'", "10-555-")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 10. remove_empty_strings()
    println!("10. remove_empty_strings()");
    let input = r#"{"name":"John","bio":""}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .remove_empty_strings(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 11. remove_nulls()
    println!("11. remove_nulls()");
    let input = r#"{"name":"John","age":null}"#;
    let out = single(JSONTools::new().flatten().remove_nulls(true).execute(input));
    println!("   In:  {input}\n   Out: {out}\n");

    // 12. remove_empty_objects()
    println!("12. remove_empty_objects()");
    let input = r#"{"name":"John","meta":{}}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .remove_empty_objects(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 13. remove_empty_arrays()
    println!("13. remove_empty_arrays()");
    let input = r#"{"name":"John","tags":[]}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .remove_empty_arrays(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 14. handle_key_collision()
    println!("14. handle_key_collision()");
    let input = r#"{"user_name":"John","admin_name":"Jane"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .key_replacement("r'^(user|admin)_'", "")
            .handle_key_collision(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}");
    println!("   Note: colliding keys are collected into an array\n");

    // 15. auto_convert_types()
    println!("15. auto_convert_types()");
    let input = r#"{"id":"123","price":"$19.99","active":"true"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .auto_convert_types(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 16. convert_dates() - independent date/datetime conversion
    println!("16. convert_dates() / convert_dates_config()");
    let input = r#"{"d":"2024-01-15T10:30:00","b":"true"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .convert_dates_config(
                DateConversionConfig::new()
                    .enabled(true)
                    .assume_utc_for_naive(false),
            )
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}");
    println!(
        "   Note: only dates convert (assume_utc_for_naive(false) keeps this one unchanged)\n"
    );

    // 17. convert_nulls() - independent null conversion, with extra tokens
    println!("17. convert_nulls() / convert_nulls_config()");
    let input = r#"{"a":"missing","b":"N/A","c":"not_a_token"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .convert_nulls_config(
                NullConversionConfig::new()
                    .enabled(true)
                    .add_extra_token("missing"),
            )
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}");
    println!("   Note: 'missing' is a custom extra token; built-in 'N/A' still works\n");

    // 18. convert_booleans() - independent boolean conversion, with extra tokens
    println!("18. convert_booleans() / convert_booleans_config()");
    let input = r#"{"a":"si","b":"nope","c":"true"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .convert_booleans_config(
                BooleanConversionConfig::new()
                    .enabled(true)
                    .add_extra_true_token("si")
                    .add_extra_false_token("nope"),
            )
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 19. convert_numbers() - independent number conversion, sub-format toggles
    println!("19. convert_numbers() / convert_numbers_config()");
    let input = r#"{"price":"$45.67","count":"1,234.56"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .convert_numbers_config(NumberConversionConfig::new().enabled(true).currency(false))
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}");
    println!("   Note: currency(false) leaves '$45.67' as a string; thousands-separator cleanup is still core\n");

    // 20. max_array_index() - DoS guard during unflatten
    println!("20. max_array_index()");
    let ok_input = r#"{"items.0":"a","items.1":"b"}"#;
    let ok_out = single(
        JSONTools::new()
            .unflatten()
            .max_array_index(10)
            .execute(ok_input),
    );
    println!("   Within limit -> In:  {ok_input}\n                  Out: {ok_out}");
    let bad_input = r#"{"items.9999":"x"}"#;
    match JSONTools::new()
        .unflatten()
        .max_array_index(10)
        .execute(bad_input)
    {
        Ok(_) => println!("   Unexpected success for out-of-range index"),
        Err(e) => println!("   Exceeds limit  -> In:  {bad_input}\n                  Err: {e}\n"),
    }

    // 21. Parallel processing tuning knobs
    println!("21. parallel_threshold() / num_threads() / nested_parallel_threshold()");
    let batch: Vec<String> = (0..200)
        .map(|i| format!(r#"{{"id":{i},"data":{{"value":{}}}}}"#, i * 10))
        .collect();
    let tools = JSONTools::new()
        .flatten()
        .parallel_threshold(50)
        .num_threads(Some(4))
        .nested_parallel_threshold(200);
    match tools.execute(batch.as_slice()) {
        Ok(JsonOutput::Multiple(results)) => {
            println!(
                "   Processed {} documents with tuned parallelism",
                results.len()
            );
            println!("   Sample: {}\n", results[0]);
        }
        _ => println!("   Unexpected result\n"),
    }

    // 22. Batch processing - a single execute() call over many documents
    println!("22. Batch processing (Vec<&str> input -> Vec<String> output)");
    let batch = vec![r#"{"a":{"b":1}}"#, r#"{"c":{"d":2}}"#];
    match JSONTools::new().flatten().execute(batch.as_slice()) {
        Ok(JsonOutput::Multiple(results)) => {
            println!("   In:  {batch:?}");
            println!("   Out: {results:?}\n");
        }
        _ => println!("   Unexpected result\n"),
    }

    // 23. exclude_key() - drop a key and its entire subtree
    println!("23. exclude_key() - drop a container key's entire subtree");
    let input = r#"{"user":{"name":"John","crypto_wallet":{"coin":"BTC","balance":100}}}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .exclude_key("crypto")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 24. exclude_value() - drop a key-value pair by value content
    println!("24. exclude_value() - drop a key-value pair whose value matches");
    let input = r#"{"user":{"name":"John","status":"banned"}}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .exclude_value("banned")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");
}
