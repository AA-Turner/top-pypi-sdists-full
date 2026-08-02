//! Curated multi-feature pipelines, building on `feature_by_feature.rs`.
//!
//! These aren't an exhaustive combinatorial sweep (the builder has ~10
//! independent toggles, so a literal power-set would be 1000+ cases) -- they're
//! realistic groupings of features that are commonly used together, plus one
//! "kitchen sink" example exercising nearly everything at once.
//!
//! Run with: `cargo run --example feature_combinations`

use json_tools_rs::{JSONTools, JsonOutput};

fn single(result: Result<JsonOutput, impl std::fmt::Display>) -> String {
    match result {
        Ok(JsonOutput::Single(s)) => s,
        Ok(JsonOutput::Multiple(_)) => "<unexpected multiple results>".to_string(),
        Err(e) => format!("<error: {}>", e),
    }
}

fn main() {
    println!("JSON Tools RS - Feature Combinations");
    println!("=====================================\n");

    // 1. separator + lowercase_keys + key_replacement + handle_key_collision
    println!("1. separator + lowercase_keys + key_replacement + handle_key_collision");
    let input = r#"{"User":{"Full_Name":"John"},"Admin":{"Full_Name":"Jane"}}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .separator("_")
            .lowercase_keys(true)
            .key_replacement("r'^(user|admin)_'", "")
            .handle_key_collision(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 2. key_replacement + value_replacement together
    println!("2. key_replacement + value_replacement");
    let input = r#"{"usr_nm":"John","usr_eml":"john@old.com"}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .key_replacement("usr_", "user_")
            .value_replacement("@old.com", "@new.com")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 3. All four empty-value filters together
    println!("3. remove_empty_strings + remove_nulls + remove_empty_objects + remove_empty_arrays");
    let input = r#"{"name":"John","bio":"","age":null,"tags":[],"meta":{}}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .remove_empty_strings(true)
            .remove_nulls(true)
            .remove_empty_objects(true)
            .remove_empty_arrays(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 4. Real-world normalization pipeline: replacement + filtering + collision
    println!("4. lowercase_keys + key_replacement + filtering + handle_key_collision");
    let input = r#"{"User_Name":"John","User_Bio":"","Admin_Name":"Jane","Admin_Bio":null}"#;
    let out = single(
        JSONTools::new()
            .flatten()
            .lowercase_keys(true)
            .key_replacement("r'^(user|admin)_'", "")
            .remove_empty_strings(true)
            .remove_nulls(true)
            .handle_key_collision(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 5. unflatten + key_replacement + value_replacement
    println!("5. unflatten + separator + key_replacement + value_replacement");
    let input = r#"{"PREFIX_user_name":"john@OLD.com","PREFIX_user_age":30}"#;
    let out = single(
        JSONTools::new()
            .unflatten()
            .separator("_")
            .key_replacement("PREFIX_user_", "profile_")
            .value_replacement("@OLD.com", "@new.com")
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}\n");

    // 6. normal mode + auto_convert_types + value_replacement + filtering
    println!("6. normal + auto_convert_types + value_replacement + remove_empty_strings");
    let input = r#"{"user":{"status":"ACTIVE","note":"","score":"95.5"}}"#;
    let out = single(
        JSONTools::new()
            .normal()
            .auto_convert_types(true)
            .value_replacement("r'^ACTIVE$'", "enabled")
            .remove_empty_strings(true)
            .execute(input),
    );
    println!("   In:  {input}\n   Out: {out}");
    println!("   Note: nesting preserved, string replaced, empty note dropped, score converted\n");

    // 7. Batch processing + parallel tuning + type conversion together
    println!("7. batch execute + parallel_threshold + num_threads + nested_parallel_threshold + auto_convert_types");
    let batch: Vec<String> = (0..150)
        .map(|i| format!(r#"{{"id":"{i}","active":"true"}}"#))
        .collect();
    let tools = JSONTools::new()
        .flatten()
        .parallel_threshold(50)
        .num_threads(Some(4))
        .nested_parallel_threshold(100)
        .auto_convert_types(true);
    match tools.execute(batch.as_slice()) {
        Ok(JsonOutput::Multiple(results)) => {
            println!("   Processed {} documents", results.len());
            println!("   Sample: {}\n", results[0]);
        }
        _ => println!("   Unexpected result\n"),
    }

    // 8. Kitchen sink: (almost) every feature at once, on a realistic messy batch
    println!("8. Kitchen sink - every applicable feature combined");
    let api_batch = vec![
        r#"{"API_Response":{"User_Data":{"First_Name":"John","Email":"john@old.com","Bio":"","Score":"88.5"}}}"#.to_string(),
        r#"{"API_Response":{"User_Data":{"First_Name":"Jane","Email":"jane@old.com","Bio":null,"Score":"91.2"}}}"#.to_string(),
    ];
    let tools = JSONTools::new()
        .flatten()
        .separator("::")
        .lowercase_keys(true)
        .key_replacement("r'^api_response::user_data::'", "")
        .key_replacement("first_name", "name")
        .value_replacement("@old.com", "@new.com")
        .remove_empty_strings(true)
        .remove_nulls(true)
        .remove_empty_objects(true)
        .remove_empty_arrays(true)
        .auto_convert_types(true)
        .parallel_threshold(50)
        .num_threads(Some(2))
        .nested_parallel_threshold(200);
    match tools.execute(api_batch.as_slice()) {
        Ok(JsonOutput::Multiple(results)) => {
            println!("   Features: separator, lowercase, 2x key_replacement, value_replacement,");
            println!("             4x filtering, auto_convert_types, parallel tuning, batch");
            for (i, r) in results.iter().enumerate() {
                println!("   [{i}]: {r}");
            }
        }
        _ => println!("   Unexpected result"),
    }
}
