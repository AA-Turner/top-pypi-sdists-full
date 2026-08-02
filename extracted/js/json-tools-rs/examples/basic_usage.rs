use json_tools_rs::{JSONTools, JsonOutput};

fn main() {
    println!("🚀 JSON Tools RS - Basic Usage Examples");
    println!("=======================================\n");

    // Example 1: Basic flattening
    println!("1. Basic Flattening:");
    let nested_json = r#"{"user": {"name": "John", "profile": {"age": 30, "city": "NYC"}}}"#;

    match JSONTools::new().flatten().execute(nested_json) {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", nested_json);
            println!("   Output: {}", result);
            println!("   ✅ Nested JSON flattened to dot notation\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 2: Basic unflattening
    println!("2. Basic Unflattening:");
    let flat_json = r#"{"user.name": "John", "user.profile.age": 30, "user.profile.city": "NYC"}"#;

    match JSONTools::new().unflatten().execute(flat_json) {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", flat_json);
            println!("   Output: {}", result);
            println!("   ✅ Flat JSON converted back to nested structure\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 3: Custom separator
    println!("3. Custom Separator:");
    let json_with_custom_sep =
        r#"{"company": {"department": {"team": "engineering", "size": 10}}}"#;

    match JSONTools::new()
        .flatten()
        .separator("::")
        .execute(json_with_custom_sep)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json_with_custom_sep);
            println!("   Output: {}", result);
            println!("   ✅ Using '::' separator instead of default '.'\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 4: Simple filtering
    println!("4. Simple Filtering:");
    let json_with_nulls = r#"{"name": "John", "age": null, "city": "NYC", "nickname": ""}"#;

    match JSONTools::new()
        .flatten()
        .remove_nulls(true)
        .remove_empty_strings(true)
        .execute(json_with_nulls)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", json_with_nulls);
            println!("   Output: {}", result);
            println!("   ✅ Null values and empty strings removed\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 5: Roundtrip demonstration
    println!("5. Roundtrip Demonstration:");
    let original = r#"{"user": {"name": "Alice", "details": {"age": 25, "location": "SF"}}}"#;

    // First flatten
    match JSONTools::new().flatten().execute(original) {
        Ok(JsonOutput::Single(flattened)) => {
            println!("   Original:   {}", original);
            println!("   Flattened:  {}", flattened);

            // Then unflatten back
            match JSONTools::new().unflatten().execute(&flattened) {
                Ok(JsonOutput::Single(unflattened)) => {
                    println!("   Unflattened: {}", unflattened);

                    // Verify they're equivalent
                    let original_parsed: serde_json::Value =
                        serde_json::from_str(original).unwrap();
                    let result_parsed: serde_json::Value =
                        serde_json::from_str(&unflattened).unwrap();

                    if original_parsed == result_parsed {
                        println!("   ✅ Perfect roundtrip - data preserved!\n");
                    } else {
                        println!("   ❌ Roundtrip failed\n");
                    }
                }
                Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
                Err(e) => eprintln!("   Unflatten Error: {}\n", e),
            }
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Flatten Error: {}\n", e),
    }

    // Example 6: Error handling
    println!("6. Error Handling:");
    println!("   Attempting to execute without setting operation mode...");
    match JSONTools::new().execute(r#"{"test": "data"}"#) {
        Ok(_) => println!("   Unexpected success"),
        Err(e) => println!("   ✅ Correctly caught error: {}\n", e),
    }
}
