use json_tools_rs::{JSONTools, JsonOutput};

fn main() {
    println!("🚀 JSON Tools RS - Advanced Usage Examples");
    println!("==========================================\n");

    // Example 1: Complex key and value replacements
    println!("1. Advanced Pattern Replacements:");
    let complex_json = r#"{
        "user_profile_name": "John",
        "user_profile_email": "john@example.com",
        "admin_profile_name": "Jane",
        "admin_profile_role": "super"
    }"#;

    match JSONTools::new()
        .flatten()
        .key_replacement("r'(user|admin)_profile_'", "person_")
        .value_replacement("@example.com", "@company.org")
        .value_replacement("r'^super$'", "administrator")
        .execute(complex_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!(
                "   Input:  {}",
                complex_json.replace('\n', "").replace("        ", "")
            );
            println!("   Output: {}", result);
            println!("   ✅ Regex patterns applied to both keys and values\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 2: Key collision handling - collect strategy (only supported)
    println!("2. Key Collision Handling - Collect Strategy:");
    let collision_json = r#"{"user_name": "John", "admin_name": "Jane", "guest_name": "Bob"}"#;

    match JSONTools::new()
        .flatten()
        .separator("::")
        .key_replacement("r'(user|admin|guest)_'", "")
        .handle_key_collision(true)
        .execute(collision_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", collision_json);
            println!("   Output: {}", result);
            println!("   ✅ Colliding values collected into arrays\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 3: Key collision handling - collect strategy
    println!("3. Key Collision Handling - Collect Strategy:");
    match JSONTools::new()
        .flatten()
        .key_replacement("r'(user|admin|guest)_'", "")
        .handle_key_collision(true)
        .execute(collision_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Input:  {}", collision_json);
            println!("   Output: {}", result);
            println!("   ✅ Colliding values collected into arrays\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 4: Comprehensive filtering
    println!("4. Comprehensive Filtering:");
    let messy_json = r#"{
        "user": {
            "name": "John",
            "bio": "",
            "age": null,
            "tags": [],
            "metadata": {},
            "settings": {
                "theme": "dark",
                "notifications": {}
            }
        }
    }"#;

    match JSONTools::new()
        .flatten()
        .remove_empty_strings(true)
        .remove_nulls(true)
        .remove_empty_arrays(true)
        .remove_empty_objects(true)
        .execute(messy_json)
    {
        Ok(JsonOutput::Single(result)) => {
            println!(
                "   Input:  {}",
                messy_json.replace('\n', "").replace("        ", "")
            );
            println!("   Output: {}", result);
            println!("   ✅ All empty values filtered out\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 5: Batch processing
    println!("5. Batch Processing:");
    let json_batch = vec![
        r#"{"user": {"name": "Alice", "role": "admin"}}"#,
        r#"{"user": {"name": "Bob", "role": "user"}}"#,
        r#"{"user": {"name": "Charlie", "role": "guest"}}"#,
    ];

    match JSONTools::new()
        .flatten()
        .separator("_")
        .lowercase_keys(true)
        .execute(json_batch.as_slice())
    {
        Ok(JsonOutput::Multiple(results)) => {
            println!(
                "   Processed {} JSON objects with lowercase keys:",
                results.len()
            );
            for (i, output) in results.iter().enumerate() {
                println!("   [{}]: {}", i, output);
            }
            println!("   ✅ Batch processing completed\n");
        }
        Ok(JsonOutput::Single(_)) => println!("   Unexpected single result\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }

    // Example 6: Real-world data transformation
    println!("6. Real-World Data Transformation:");
    let api_response = r#"{
        "API_Response": {
            "User_Data": {
                "Personal_Info": {
                    "First_Name": "John",
                    "Last_Name": "Doe",
                    "Email_Address": "john.doe@example.com",
                    "Phone_Number": null,
                    "Bio": ""
                },
                "Account_Settings": {
                    "Theme_Preference": "dark",
                    "Notification_Settings": {},
                    "Privacy_Level": "high"
                }
            },
            "Metadata": {
                "Request_ID": "req_123",
                "Timestamp": "2024-01-01T00:00:00Z",
                "Version": "v1.0"
            }
        }
    }"#;

    match JSONTools::new()
        .flatten()
        .separator("::")
        .lowercase_keys(true)
        .key_replacement(
            "r'(api_response|user_data|personal_info|account_settings)::'",
            "",
        )
        .key_replacement("_", ".")
        .value_replacement("@example.com", "@company.org")
        .remove_empty_strings(true)
        .remove_nulls(true)
        .remove_empty_objects(true)
        .execute(api_response)
    {
        Ok(JsonOutput::Single(result)) => {
            println!("   Features: custom separator, lowercase, key normalization, value replacement, filtering");
            println!(
                "   Input:  [Complex API Response - {} chars]",
                api_response.len()
            );
            println!("   Output: {}", result);
            println!("   ✅ Complex real-world transformation completed\n");
        }
        Ok(JsonOutput::Multiple(_)) => println!("   Unexpected multiple results\n"),
        Err(e) => eprintln!("   Error: {}\n", e),
    }
}
