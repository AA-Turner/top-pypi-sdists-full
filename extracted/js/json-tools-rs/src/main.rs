use json_tools_rs::{JSONTools, JsonOutput};

fn main() {
    println!("🚀 JSON Tools RS - Educational Examples");
    println!("========================================\n");
    println!("This demonstrates individual features in a progressive learning format.");
    println!("Each example focuses on a specific capability to help you understand how to use the library effectively.\n");

    // Example 1: Basic flattening operation
    println!("1. Basic Flattening Operation:");
    println!("   Converts nested JSON to flat key-value pairs using default '.' separator");
    let json1 = r#"{"user": {"name": "John", "profile": {"age": 30}}}"#;
    match JSONTools::new().flatten().execute(json1) {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json1);
            println!("   Output: {}", result);
            println!("   Result: Nested structure flattened with dot notation\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 2: Basic unflattening operation
    println!("2. Basic Unflattening Operation:");
    println!("   Converts flat JSON back to nested structure");
    let flat_json = r#"{"user.name": "John", "user.profile.age": 30}"#;
    match JSONTools::new().unflatten().execute(flat_json) {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", flat_json);
            println!("   Output: {}", result);
            println!("   Result: Flat structure converted back to nested JSON\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 3: Custom separator usage
    println!("3. Custom Separator Usage:");
    println!("   Using '::' instead of default '.' separator");
    let json3 = r#"{"company": {"department": {"team": "engineering"}}}"#;
    match JSONTools::new().flatten().separator("::").execute(json3) {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json3);
            println!("   Output: {}", result);
            println!("   Result: Custom separator '::' used instead of '.'\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 4: Key transformations - lowercase keys
    println!("4. Key Transformations - Lowercase Keys:");
    println!("   Convert all keys to lowercase during processing");
    let json4 = r#"{"UserName": "John", "UserProfile": {"FirstName": "John"}}"#;
    match JSONTools::new()
        .flatten()
        .lowercase_keys(true)
        .execute(json4)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json4);
            println!("   Output: {}", result);
            println!("   Result: All keys converted to lowercase\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 5: Key replacement patterns - literal replacement
    println!("5. Key Replacement Patterns - Literal Replacement:");
    println!("   Replace literal strings in keys");
    let json5 = r#"{"user_profile_name": "John", "user_profile_age": 30}"#;
    match JSONTools::new()
        .flatten()
        .key_replacement("user_profile_", "person_")
        .execute(json5)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json5);
            println!("   Output: {}", result);
            println!("   Result: 'user_profile_' replaced with 'person_' in keys\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 6: Key replacement patterns - regex replacement
    println!("6. Key Replacement Patterns - Regex Replacement:");
    println!("   Replace using regex patterns in keys");
    let json6 = r#"{"user_name": "John", "admin_name": "Jane", "guest_name": "Bob"}"#;
    match JSONTools::new()
        .flatten()
        .key_replacement("(user|admin)_", "person_")
        .execute(json6)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json6);
            println!("   Output: {}", result);
            println!("   Result: Regex pattern '(user|admin)_' replaced with 'person_'\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 7: Value replacement patterns - literal replacement
    println!("7. Value Replacement Patterns - Literal Replacement:");
    println!("   Replace literal strings in values");
    let json7 = r#"{"email": "user@example.com", "backup_email": "admin@example.com"}"#;
    match JSONTools::new()
        .flatten()
        .value_replacement("@example.com", "@company.org")
        .execute(json7)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json7);
            println!("   Output: {}", result);
            println!("   Result: '@example.com' replaced with '@company.org' in values\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 8: Value replacement patterns - regex replacement
    println!("8. Value Replacement Patterns - Regex Replacement:");
    println!("   Replace using regex patterns in values");
    let json8 = r#"{"role": "super", "level": "admin", "type": "user"}"#;
    match JSONTools::new()
        .flatten()
        .value_replacement("^(super|admin)$", "administrator")
        .execute(json8)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json8);
            println!("   Output: {}", result);
            println!("   Result: Regex pattern '^(super|admin)$' replaced with 'administrator'\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 9: Filtering options - remove empty strings
    println!("9. Filtering Options - Remove Empty Strings:");
    println!("   Remove keys that have empty string values");
    let json9 = r#"{"name": "John", "nickname": "", "age": 30}"#;
    match JSONTools::new()
        .flatten()
        .remove_empty_strings(true)
        .execute(json9)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json9);
            println!("   Output: {}", result);
            println!("   Result: 'nickname' with empty string value removed\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 10: Filtering options - remove null values
    println!("10. Filtering Options - Remove Null Values:");
    println!("    Remove keys that have null values");
    let json10 = r#"{"name": "John", "age": null, "city": "NYC"}"#;
    match JSONTools::new()
        .flatten()
        .remove_nulls(true)
        .execute(json10)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("    Input:  {}", json10);
            println!("    Output: {}", result);
            println!("    Result: 'age' with null value removed\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
        Err(e) => eprintln!("    Error: {}\n", e),
    }

    // Example 11: Filtering options - remove empty objects and arrays
    println!("11. Filtering Options - Remove Empty Objects and Arrays:");
    println!("    Remove keys that have empty objects or arrays");
    let json11 = r#"{"user": {"name": "John"}, "tags": [], "metadata": {}}"#;
    match JSONTools::new()
        .flatten()
        .remove_empty_objects(true)
        .remove_empty_arrays(true)
        .execute(json11)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("    Input:  {}", json11);
            println!("    Output: {}", result);
            println!("    Result: 'tags' (empty array) and 'metadata' (empty object) removed\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
        Err(e) => eprintln!("    Error: {}\n", e),
    }

    // Example 12: Collision handling - collect into arrays
    println!("12. Collision Handling - Collect Values:");
    println!("    When key replacements cause collisions, collect all values into arrays");
    let collision_json = r#"{"user_name": "John", "admin_name": "Jane"}"#;
    match JSONTools::new()
        .flatten()
        .separator("::")
        .key_replacement("(user|admin)_", "")
        .handle_key_collision(true)
        .execute(collision_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("    Input:  {}", collision_json);
            println!("    Output: {}", result);
            println!("    Result: Colliding values collected into arrays (e.g., \"name\": [..])\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
        Err(e) => eprintln!("    Error: {}\n", e),
    }

    // Example 13: Collision handling - collect values into arrays
    println!("13. Collision Handling - Collect Values into Arrays:");
    println!("    When key replacements cause collisions, collect all values into an array");
    match JSONTools::new()
        .flatten()
        .key_replacement("(user|admin)_", "")
        .handle_key_collision(true)
        .execute(collision_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("    Input:  {}", collision_json);
            println!("    Output: {}", result);
            println!("    Result: Colliding values collected into array [\"John\", \"Jane\"]\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
        Err(e) => eprintln!("    Error: {}\n", e),
    }

    // Example 14: Comprehensive integration example
    println!("14. Comprehensive Integration Example:");
    println!("    Combining multiple features for real-world usage");
    let complex_json = r#"{
        "User_Profile": {
            "Personal_Info": {
                "FirstName": "John",
                "LastName": "",
                "Email": "john@example.com",
                "Age": null
            },
            "Settings": {
                "Theme": "dark",
                "Notifications": {},
                "Tags": []
            }
        }
    }"#;
    match JSONTools::new()
        .flatten()
        .separator("::")
        .lowercase_keys(true)
        .key_replacement("(user_profile|personal_info)::", "person::")
        .value_replacement("@example.com", "@company.org")
        .remove_empty_strings(true)
        .remove_nulls(true)
        .remove_empty_objects(true)
        .remove_empty_arrays(true)
        .execute(complex_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!(
                "    Features: custom separator, lowercase keys, key/value replacements, filtering"
            );
            println!(
                "    Input:  {}",
                complex_json.replace('\n', "").replace("        ", "")
            );
            println!("    Output: {}", result);
            println!("    Result: Comprehensive transformation with multiple features\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
        Err(e) => eprintln!("    Error: {}\n", e),
    }

    // Example 15: Roundtrip demonstration
    println!("15. Roundtrip Demonstration:");
    println!("    Flatten JSON and then unflatten it back to verify data preservation");
    let original = r#"{"user": {"name": "John", "age": 30}, "items": [1, 2, {"nested": "value"}]}"#;
    match JSONTools::new().flatten().execute(original) {
        Ok(JsonOutput::Single(flattened)) => {
            println!("    Original:   {}", original);
            println!("    Flattened:  {}", flattened);

            match JSONTools::new().unflatten().execute(&flattened) {
                Ok(JsonOutput::Single(unflattened)) => {
                    println!("    Unflattened: {}", unflattened);

                    let original_parsed: serde_json::Value =
                        serde_json::from_str(original).unwrap();
                    let result_parsed: serde_json::Value =
                        serde_json::from_str(&unflattened).unwrap();
                    if original_parsed == result_parsed {
                        println!("    ✅ Roundtrip successful - data preserved!\n");
                    } else {
                        println!("    ❌ Roundtrip failed - data not preserved\n");
                    }
                }
                Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
                Err(e) => eprintln!("    Unflatten Error: {}\n", e),
            }
        }
        Ok(JsonOutput::Multiple(_)) => println!("    Unexpected multiple results\n"),
        Err(e) => eprintln!("    Flatten Error: {}\n", e),
    }

    // Example 16: Batch processing
    println!("16. Batch Processing:");
    println!("    Process multiple JSON objects in a single operation");
    let json_list = vec![
        r#"{"user": {"name": "John"}}"#,
        r#"{"user": {"name": "Jane"}}"#,
        r#"{"user": {"name": "Bob"}}"#,
    ];
    match JSONTools::new()
        .flatten()
        .separator("_")
        .execute(json_list.as_slice())
    {
        Ok(JsonOutput::Multiple(results)) => {
            println!("    Processed {} JSON objects:", results.len());
            for (i, output) in results.iter().enumerate() {
                println!("    [{}]: {}", i, output);
            }
            println!();
        }
        Ok(JsonOutput::Single(_)) => println!("    Unexpected single result\n"),
        Err(e) => eprintln!("    Error: {}\n", e),
    }

    // Example 17: Error handling
    println!("17. Error Handling:");
    println!("    Demonstrating proper error handling when operation mode is not set");
    match JSONTools::new().execute(r#"{"test": "data"}"#) {
        Ok(_) => println!("    Unexpected success"),
        Err(e) => println!("    ✅ Correctly caught error: {}\n", e),
    }
}
